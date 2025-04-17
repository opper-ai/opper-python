import asyncio
from typing import Any, Dict

from opperai import AsyncOpper, BaseEvaluator
from opperai.evaluations._base import Evaluation
from opperai.types.spans import SpanMetric
from pydantic import BaseModel, Field


# Example evaluators
class RhymesEvaluator(BaseEvaluator):
    """Evaluator that checks for rhymes in text."""

    def __init__(self, min_count: int = 3):
        """Initialize the rhymes evaluator.

        Args:
            min_count: Minimum number of rhyming pairs required
        """
        super().__init__("rhymes")
        self.min_count = min_count

    async def evaluate(self, context: Dict[str, Any], **kwargs) -> Evaluation:
        """Check for rhymes in the response.

        Args:
            context: Dictionary containing the result and other context
            **kwargs: Additional keyword arguments

        Returns:
            Tuple of (success, score, metrics)
        """
        result_text = str(context["result"])

        # Simple implementation counting line pairs as potential rhymes
        lines = result_text.strip().split("\n")
        line_count = len([line for line in lines if line.strip()])
        rhyme_pairs = max(0, line_count // 2 - 1)  # Simple heuristic

        success = rhyme_pairs >= self.min_count
        score = min(1.0, rhyme_pairs / self.min_count)  # Normalize to 0-1 scale

        # Create metrics
        metrics = [
            SpanMetric(
                dimension=f"eval.{self.name}.score",
                value=score,
                comment=f"Evaluation score for {self.name}",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.success",
                value=1.0 if success else 0.0,
                comment=f"Success status for {self.name}",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.found",
                value=float(rhyme_pairs),
                comment=f"Found rhyming pairs for {self.name}",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.required",
                value=float(self.min_count),
                comment=f"Required rhyming pairs for {self.name}",
            ),
        ]

        return Evaluation(success=success, score=score, metrics={self.name: metrics})


class SentimentEvaluator(BaseEvaluator):
    """Evaluator that checks sentiment of text."""

    def __init__(self, target: str = "positive"):
        """Initialize the sentiment evaluator.

        Args:
            target: Target sentiment ("positive", "negative", or "neutral")
        """
        super().__init__("sentiment")
        self.target = target
        self._opper = AsyncOpper()

    async def evaluate(self, context: Dict[str, Any], **kwargs) -> Evaluation:
        """Check sentiment of the response using an LLM with structured output.

        Args:
            context: Dictionary containing the result and other context
            **kwargs: Additional keyword arguments

        Returns:
            Tuple of (success, score, metrics)
        """
        result_text = str(context["result"])

        # Get parent span id for tracing
        parent_span_id = context.get("span_id")

        # Define a structured output type for the sentiment analysis
        class SentimentAnalysis(BaseModel):
            sentiment: str = Field(
                description="The sentiment of the text: 'positive', 'negative', or 'neutral'"
            )
            score: float = Field(
                description="A score from 0-10 where 0-3 is negative, 4-6 is neutral, 7-10 is positive"
            )
            explanation: str = Field(
                description="A brief explanation of the sentiment analysis"
            )

        # Make the call with structured output and pass parent span
        sentiment_result, _ = await self._opper.call(  # type: ignore
            name="sentiment_analysis",
            model="azure/gpt-4o-eu",
            instructions="""
            Analyze the sentiment of the provided text, determining if it's primarily positive, negative, or neutral.
            Consider emotional tone, word choice, and overall message.
            
            Rate the sentiment on a scale of 0-10, where:
            - 0-3: Negative
            - 4-6: Neutral
            - 7-10: Positive
            """,
            input=result_text,
            output_type=SentimentAnalysis,
            parent_span_id=parent_span_id,  # Pass the parent span ID to link to the trace
        )

        # Determine success based on the target sentiment
        if self.target == "positive":
            success = sentiment_result.sentiment == "positive"
        elif self.target == "negative":
            success = sentiment_result.sentiment == "negative"
        else:  # neutral
            success = sentiment_result.sentiment == "neutral"

        # Normalize score to 0-1 scale
        normalized_score = sentiment_result.score / 10.0

        # Create metrics
        metrics = [
            SpanMetric(
                dimension=f"eval.{self.name}.score",
                value=normalized_score,
                comment=f"Evaluation score for {self.name}",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.success",
                value=1.0 if success else 0.0,
                comment=f"Success status for {self.name}",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.sentiment_value",
                value=sentiment_result.score,
                comment=f"Raw sentiment score for {self.name}",
            ),
        ]

        return Evaluation(
            success=success, score=normalized_score, metrics={self.name: metrics}
        )


class LineCountEvaluator(BaseEvaluator):
    """Evaluator that checks if the text has enough lines."""

    def __init__(self, min_lines: int = 10, max_lines: int = 30):
        """Initialize the line count evaluator.

        Args:
            min_lines: Minimum number of lines required
            max_lines: Maximum number of lines allowed
        """
        super().__init__("line_count")
        self.min_lines = min_lines
        self.max_lines = max_lines

    async def evaluate(self, context: Dict[str, Any], **kwargs) -> Evaluation:
        """Check if the text has an appropriate number of lines.

        Args:
            context: Dictionary containing the result and other context
            **kwargs: Additional keyword arguments

        Returns:
            Tuple of (success, score, metrics)
        """
        result_text = str(context["result"])

        # Count non-empty lines
        lines = [line for line in result_text.strip().split("\n") if line.strip()]
        line_count = len(lines)

        # Check if line count is within acceptable range
        too_short = line_count < self.min_lines
        too_long = line_count > self.max_lines
        success = not (too_short or too_long)

        # Calculate score based on how close to ideal range
        if too_short:
            # Score decreases as we get fewer lines than minimum
            raw_score = line_count / self.min_lines
        elif too_long:
            # Score decreases as we exceed maximum
            excess = line_count - self.max_lines
            max_excess = self.max_lines  # At 2x max_lines, score becomes 0
            raw_score = max(0, 1 - (excess / max_excess))
        else:
            # Perfect score when within range
            raw_score = 1.0

        # Create metrics
        metrics = [
            SpanMetric(
                dimension=f"eval.{self.name}.score",
                value=raw_score,
                comment=f"Evaluation score for {self.name}",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.success",
                value=1.0 if success else 0.0,
                comment=f"Success status for {self.name}",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.line_count",
                value=float(line_count),
                comment=f"Line count for {self.name}",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.min_lines",
                value=float(self.min_lines),
                comment=f"Minimum lines for {self.name}",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.max_lines",
                value=float(self.max_lines),
                comment=f"Maximum lines for {self.name}",
            ),
        ]

        return Evaluation(
            success=success, score=raw_score, metrics={self.name: metrics}
        )


async def main():
    """Example showing how to use Evaluation with Opper."""
    # Create an Opper client
    opper = AsyncOpper()

    instructions = "Write a rhyming poem about the input. Make it at least 12 lines with a positive tone."
    input = "VR Headset"

    result, response = await opper.call(
        name="poem_generation",
        instructions=instructions,
        input=input,
    )

    print("--------------------------------")
    print(f"Poem to evaluate:\n{result}\n")
    print("--------------------------------")

    # Create context for evaluation
    context = {
        "result": result,
        "instructions": instructions,
        "input": input,
    }

    # Create evaluation with evaluators
    evaluation = await opper.evaluate(
        span_id=response.span_id,
        evaluators=[
            RhymesEvaluator(min_count=3),
            SentimentEvaluator(target="positive"),
            LineCountEvaluator(min_lines=10, max_lines=20),
        ],
        context=context,
    )

    print(f"Overall evaluation success: {evaluation.success}")
    print(f"Overall score: {evaluation.score:.1f}")
    print("--------------------------------")

    # Print metrics for each evaluator
    for name, metrics in evaluation.metrics.items():
        if name != "overall":
            eval_result = evaluation.results[name]
            print(
                f"{name}: Success={eval_result['success']}, Score={eval_result['score']:.1f}"
            )
            for metric in metrics[:3]:  # Show first few metrics
                print(f"  {metric.dimension}: {metric.value}")
            print()

    print("--------------------------------")

    if evaluation.success:
        print("✅ All evaluation checks passed!")
    else:
        print("❌ Some evaluation checks failed.")


if __name__ == "__main__":
    asyncio.run(main())
