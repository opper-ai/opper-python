import asyncio
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field

from opperai import AsyncOpper, BaseEvaluator
from opperai.evaluations._base import Evaluation
from opperai.types.spans import SpanMetric

opper = AsyncOpper()


class SentimentEvaluator(BaseEvaluator):
    """Evaluator that checks sentiment of text."""

    def __init__(self, target: Literal["positive", "negative", "neutral"] = "positive"):
        super().__init__("sentiment")
        self.target = target

    async def evaluate(self, context: Dict[str, Any], **kwargs) -> Evaluation:
        result_text = str(context.get("result", ""))
        parent_span_id = context.get("span_id")

        class SentimentAnalysis(BaseModel):
            sentiment: Literal["positive", "negative", "neutral"] = Field(
                description="The sentiment of the text"
            )
            score: float = Field(description="Sentiment score", ge=0.0, le=1.0)
            explanation: str = Field(
                description="Brief explanation of the sentiment analysis"
            )

        # Call LLM for sentiment analysis
        response = await opper.call(  # type: ignore
            name="sentiment_analysis",
            instructions="Analyze the sentiment of the text as positive, negative, or neutral. Return score as 0.0-1.0 where 0.0 is very negative, 0.5 is neutral, and 1.0 is very positive.",
            input=result_text,
            output_type=SentimentAnalysis,
            parent_span_id=parent_span_id,
        )

        # Get sentiment result from the response
        sentiment_result = response[0]  # type: ignore

        # Check for target sentiment
        success = sentiment_result.sentiment == self.target

        metrics = [
            SpanMetric(
                dimension=f"eval.{self.name}.score",
                value=sentiment_result.score,
                comment="Sentiment score (0.0-1.0)",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.success",
                value=1.0 if success else 0.0,
                comment=f"Target sentiment: {self.target}",
            ),
        ]

        return Evaluation(
            success=success, score=sentiment_result.score, metrics={self.name: metrics}
        )


class LineCountEvaluator(BaseEvaluator):
    """Evaluator that checks if the text has enough lines."""

    def __init__(self, min_lines: int = 10, max_lines: int = 30):
        super().__init__("line_count")
        self.min_lines = min_lines
        self.max_lines = max_lines

    async def evaluate(self, context: Dict[str, Any], **kwargs) -> Evaluation:
        result_text = str(context.get("result", ""))

        # Count non-empty lines
        lines = [line for line in result_text.strip().split("\n") if line.strip()]
        line_count = len(lines)

        # Check if count is within acceptable range
        success = self.min_lines <= line_count <= self.max_lines

        # Calculate score
        if line_count < self.min_lines:
            score = line_count / self.min_lines
        elif line_count > self.max_lines:
            excess = line_count - self.max_lines
            max_excess = self.max_lines
            score = max(0, 1 - (excess / max_excess))
        else:
            score = 1.0

        metrics = [
            SpanMetric(
                dimension=f"eval.{self.name}.score",
                value=score,
                comment="Line count score",
            ),
            SpanMetric(
                dimension=f"eval.{self.name}.line_count",
                value=float(line_count),
                comment=f"Found {line_count} lines",
            ),
        ]

        return Evaluation(success=success, score=score, metrics={self.name: metrics})


async def run_evaluations(text_to_evaluate: str, span_id: str) -> None:
    """Run evaluations on the provided text."""

    # Create a context dictionary with the result
    context = {"result": text_to_evaluate, "span_id": span_id}

    # Create a list of evaluators
    evaluators = [
        SentimentEvaluator(target="positive"),
        LineCountEvaluator(min_lines=10, max_lines=20),
    ]

    # Run the evaluation
    evaluation = await opper.evaluate(
        span_id=span_id,  # type: ignore
        evaluators=evaluators,
        context=context,
    )

    # Display results
    print("\n--- Evaluation Results ---")
    print(f"Overall success: {evaluation.success}")
    print(f"Overall score: {evaluation.score:.2f}")

    # Show individual evaluator results
    for name, result in evaluation.results.items():
        if name != "overall":
            print(f"\n{name}:")
            print(f"  Success: {result['success']}")
            print(f"  Score: {result['score']:.2f}")


async def main():
    """Simple example showing how to use evaluations with Opper."""

    instructions = "Write a rhyming poem about the input. Make it at least 12 lines with a positive tone."
    input = "VR Headset"

    result, response = await opper.call(  # type: ignore
        name="poem_generation",
        instructions=instructions,
        input=input,
    )

    print(f"\n--- Generated Poem ---\n{result}\n")

    # Run evaluations on the text
    await run_evaluations(result, response.span_id)


if __name__ == "__main__":
    asyncio.run(main())
