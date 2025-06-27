from opperai import Opper
from pydantic import BaseModel, Field
from typing import Literal
import asyncio
import os

opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))


def linecount_evaluator(text, min_lines=10, max_lines=20):
    """Evaluator that checks if the text has enough lines."""
    lines = [line for line in str(text).strip().split("\n") if line.strip()]
    line_count = len(lines)

    if line_count < min_lines:
        score = line_count / min_lines
    elif line_count > max_lines:
        excess = line_count - max_lines
        max_excess = max_lines
        score = max(0, 1 - (excess / max_excess))
    else:
        score = 1.0

    return [
        {
            "dimension": "line_count-score",
            "value": score,
            "comment": "Line count score",
        },
        {
            "dimension": "line_count-count",
            "value": min(1.0, line_count / max_lines),
            "comment": f"Found {line_count} lines",
        },
    ]


async def sentiment_evaluator(text, target="positive", span_id=None):
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
    response = await opper.call_async(  # type: ignore
        name="sentiment_analysis",
        instructions="Analyze the sentiment of the text.",
        input=text,
        output_schema=SentimentAnalysis,
        parent_span_id=span_id,
    )

    # Check for target sentiment
    success = response.json_payload["sentiment"] == target

    # Return metrics
    return [
        {
            "dimension": "sentiment-score",
            "value": response.json_payload["score"],
            "comment": "Sentiment score (0.0-1.0)",
        },
        {
            "dimension": "sentiment-match",
            "value": 1.0 if success else 0.0,
            "comment": f"Target sentiment: {target}",
        },
    ]


async def main():
    """Simple example showing how to build your own evaluators and use them with Opper."""

    # Generate content to evaluate
    instructions = "Write a rhyming poem about the input. Make it at least 12 lines with a positive tone."
    input = "VR Headset"

    result = await opper.call_async(  # type: ignore
        name="poem_generation",
        instructions=instructions,
        input=input,
    )

    print(f"\n--- Generated Poem ---\n{result}\n")

    # Add metrics to Opper
    linecount_metrics = linecount_evaluator(text=result, min_lines=4, max_lines=10)
    sentiment_metrics = await sentiment_evaluator(text=result, target="positive")
    metrics = linecount_metrics + sentiment_metrics

    for metric in metrics:
        opper.span_metrics.create_metric(
            dimension=metric["dimension"],
            value=metric["value"],
            comment=metric["comment"],
            span_id=result.span_id,
        )

    # Retrieve metrics from Opper and display
    print("\n--- Evaluation Results ---")

    # Show metrics for each evaluator group
    retrieved_metrics = opper.span_metrics.list(span_id=result.span_id).data
    for metric in retrieved_metrics:
        print(f"\n{metric.dimension}:")
        print(f"  Value: {metric.value}")
        print(f"  Comment: {metric.comment}")
        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())
