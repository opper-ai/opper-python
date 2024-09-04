import asyncio
from typing import List

from opperai import fn
from opperai.types import ImageInput
from pydantic import BaseModel


@fn(model="openai/gpt-4o")
async def fn_bare_minimum_async(question: str) -> str:
    """answer the following question"""


@fn(model="openai/gpt-4o")
def fn_bare_minimum(question: str) -> str:
    """answer the following question"""


class StructuredInput(BaseModel):
    x: int
    y: int


class StructuredOutput(BaseModel):
    sum: int


@fn(model="openai/gpt-4o")
async def fn_addition_async(input: StructuredInput) -> StructuredOutput:
    """given x and y compute their sum"""


@fn(model="openai/gpt-4o")
def fn_addition(input: StructuredInput) -> StructuredOutput:
    """given x and y compute their sum"""


@fn(model="openai/gpt-4o")
async def fn_multimodal_async(image: ImageInput) -> str:
    """describe the image"""


@fn(model="openai/gpt-4o")
def fn_multimodal(image: ImageInput) -> str:
    """describe the image"""


class ImagePair(BaseModel):
    image1: ImageInput
    image2: ImageInput


class ThingsInCommon(BaseModel):
    things: List[str]


@fn(model="openai/gpt-4o")
async def fn_image_pair_async(image_pair: ImagePair) -> ThingsInCommon:
    """find things in common between the two images"""


@fn(model="openai/gpt-4o")
def fn_image_pair(image_pair: ImagePair) -> ThingsInCommon:
    """find things in common between the two images"""


@fn(model="openai/gpt-4o")
async def fn_image_list_async(image_list: List[ImageInput]) -> ThingsInCommon:
    """find things in common between the images"""


@fn(model="openai/gpt-4o")
def fn_image_list(image_list: List[ImageInput]) -> ThingsInCommon:
    """find things in common between the images"""


async def _wrap(desc: str, f):
    res = await f()
    print(desc, res)
    return res


async def run_async():
    await asyncio.gather(
        _wrap("fn_bare_minimum_async:", lambda: fn_bare_minimum_async("what is 2+2")),
        _wrap(
            "fn_addition_async:", lambda: fn_addition_async(StructuredInput(x=2, y=2))
        ),
        _wrap(
            "fn_multimodal_async:",
            lambda: fn_multimodal_async(
                ImageInput(path="tests/fixtures/images/cat1.png")
            ),
        ),
        _wrap(
            "fn_image_pair_async:",
            lambda: fn_image_pair_async(
                ImagePair(
                    image1=ImageInput(path="tests/fixtures/images/cat1.png"),
                    image2=ImageInput(path="tests/fixtures/images/cat2.png"),
                )
            ),
        ),
        _wrap(
            "fn_image_list_async:",
            lambda: fn_image_list_async(
                [
                    ImageInput(path="tests/fixtures/images/cat1.png"),
                    ImageInput(path="tests/fixtures/images/cat2.png"),
                ]
            ),
        ),
    )


async def run_sync():
    res = fn_bare_minimum("what is 2+2")
    print(f"fn_bare_minimum: {res}")
    res = fn_addition(StructuredInput(x=2, y=2))
    print(f"fn_addition: {res}")
    res = fn_multimodal(ImageInput(path="tests/fixtures/images/cat1.png"))
    print(f"fn_multimodal: {res}")
    res = fn_image_pair(
        ImagePair(
            image1=ImageInput(path="tests/fixtures/images/cat1.png"),
            image2=ImageInput(path="tests/fixtures/images/cat2.png"),
        )
    )
    print(f"fn_image_pair: {res}")
    res = fn_image_list(
        [
            ImageInput(path="tests/fixtures/images/cat1.png"),
            ImageInput(path="tests/fixtures/images/cat2.png"),
        ]
    )
    print(f"fn_image_list: {res}")


async def main(run_type: str = "both"):
    run_type = run_type.strip().lower()
    if run_type == "sync":
        print("running sync")
        await run_sync()
    elif run_type == "async":
        print("running async")
        await run_async()
    else:
        print("running both sync and async concurrently...")
        await asyncio.gather(run_async(), run_sync())


if __name__ == "__main__":
    import sys

    run_type = sys.argv[1] if len(sys.argv) > 1 else "both"
    asyncio.run(main(run_type))
