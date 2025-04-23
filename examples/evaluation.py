import asyncio
from typing import Literal

from pydantic import BaseModel, Field

from opperai import AsyncOpper, evaluator
from opperai.types import Metric

opper = AsyncOpper()


@evaluator
def linecount_evaluator(result, min_lines=10, max_lines=20):
    """Evaluator that checks if the text has enough lines."""
    # Count non-empty lines
    lines = [line for line in str(result).strip().split("\n") if line.strip()]
    line_count = len(lines)

    # Calculate score
    if line_count < min_lines:
        score = line_count / min_lines
    elif line_count > max_lines:
        excess = line_count - max_lines
        max_excess = max_lines
        score = max(0, 1 - (excess / max_excess))
    else:
        score = 1.0

    return [
        Metric(dimension="line_count.score", value=score, comment="Line count score"),
        Metric(
            dimension="line_count.count",
            value=min(1.0, line_count / max_lines),
            comment=f"Found {line_count} lines",
        ),
    ]


@evaluator
async def sentiment_evaluator(result, target="positive", span_id=None):
    """Evaluator that checks sentiment of text using an LLM call."""

    # Define output schema for sentiment analysis
    class SentimentAnalysis(BaseModel):
        sentiment: Literal["positive", "negative", "neutral"] = Field(
            description="The sentiment of the text"
        )
        score: float = Field(description="Sentiment score", ge=0.0, le=1.0)
        explanation: str = Field(
            description="Brief explanation of the sentiment analysis"
        )

    # Call LLM for sentiment analysis
    response, _ = await opper.call(  # type: ignore
        name="sentiment_analysis",
        instructions="Analyze the sentiment of the text.",
        input=result,
        output_type=SentimentAnalysis,
        parent_span_id=span_id,
    )

    # Check for target sentiment
    success = response.sentiment == target

    # Return metrics
    return [
        Metric(
            dimension="sentiment.score",
            value=response.score,
            comment="Sentiment score (0.0-1.0)",
        ),
        Metric(
            dimension="sentiment.match",
            value=1.0 if success else 0.0,
            comment=f"Target sentiment: {target}",
        ),
    ]


async def main():
    """Simple example showing how to use evaluations with Opper."""

    # Generate content to evaluate
    instructions = "Write a rhyming poem about the input. Make it at least 12 lines with a positive tone."
    input = "VR Headset"

    result, response = await opper.call(  # type: ignore
        name="poem_generation",
        instructions=instructions,
        input=input,
    )

    print(f"\n--- Generated Poem ---\n{result}\n")

    # Run evaluation using decorated evaluators
    evaluation = await opper.evaluate(
        span_id=response.span_id,  # type: ignore
        evaluators=[
            linecount_evaluator(result=result, min_lines=4, max_lines=10),
            sentiment_evaluator(
                result=result, target="positive", span_id=response.span_id
            ),
        ],
    )

    # Display results
    print("\n--- Evaluation Results ---")

    # Show metrics for each evaluator group
    for group_name, metrics_list in evaluation.metrics.items():
        print(f"\n{group_name}:")
        # Calculate average score safely
        values = [m.value for m in metrics_list if m.value is not None]
        avg_score = sum(values) / len(values) if values else 0
        print(f"  Average Score: {avg_score:.2f}")
        print("  Metrics:")
        for metric in metrics_list:
            print(f"    - {metric.dimension}: {metric.value:.2f} ({metric.comment})")


if __name__ == "__main__":
    asyncio.run(main())
