import asyncio
import time
from datetime import datetime, timezone

from opperai import AsyncOpper, Opper


def compute():
    time.sleep(1)


async def compute_async():
    await asyncio.sleep(1)


async def run_async():
    print("Running async")
    opper = AsyncOpper()
    spans = opper.spans

    async with spans.start("transform", input="Hello, world!") as span:
        t0 = datetime.now(timezone.utc)
        await compute_async()
        t1 = datetime.now(timezone.utc)
        await span.save_generation(
            called_at=t0,
            duration_ms=int((t1 - t0).total_seconds() * 1000),
            response="I'm happy because I'm happy",
            model="anthropic/claude-3-haiku",
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world!",
                }
            ],
            cost=3.1,
            prompt_tokens=10,
            completion_tokens=10,
            total_tokens=20,
        )


def run():
    print("Running sync")
    opper = Opper()
    spans = opper.spans

    with spans.start("transform", input="Hello, world!") as span:
        t0 = datetime.now(timezone.utc)
        compute()
        t1 = datetime.now(timezone.utc)
        span.save_generation(
            called_at=t0,
            duration_ms=int((t1 - t0).total_seconds() * 1000),
            response="I'm happy because I'm happy",
            model="anthropic/claude-3-haiku",
            messages=[
                {
                    "role": "user",
                    "content": "Hello, world!",
                }
            ],
            cost=3.1,
            prompt_tokens=10,
            completion_tokens=10,
            total_tokens=20,
        )


run()
asyncio.run(run_async())
