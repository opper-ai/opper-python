import asyncio
import os
from tempfile import NamedTemporaryFile
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
import base64
from opperai import Opper


opper = Opper(
    http_bearer=os.getenv("OPPER_API_KEY"),
)


def save_file(bytes: bytes, path: Optional[str] = None) -> str:
    if path is None:
        with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            path = temp_file.name

    with open(path, "wb") as f:
        f.write(bytes)
        f.close()

    return path


def generate_image(description: str):
    response = opper.call(
        name="generate_image",
        input=description,
        model="openai/gpt-image-1",
    )
    return response.images[0]


class Description(BaseModel):
    observations: List[str] = Field(description="The observations of the image")
    original_description: str = Field(
        description="The original description of the image"
    )
    improved_description: str = Field(
        description="The improved description of the image"
    )


def describe_image(media_input: str, proposed_description: str) -> str:
    response = opper.call(
        name="describe_image",
        instructions="given an image and a description of the image, improve the description, make sure the description is a list of observations of the image and that the description matches the content of the image",
        output_schema=Description,
        input={
            "_opper_media_input": media_input,  # this field name is required by opper
            "proposed_description": proposed_description,
        },
        model="openai/gpt-4o",
    )
    return response


async def async_generate_image(description: str) -> str:
    response = await opper.call_async(
        name="async_generate_image",
        input=description,
        model="openai/gpt-image-1",
    )
    return response.images[0]


async def async_describe_image(media_input: str, proposed_description: str) -> str:
    response = await opper.call_async(
        name="async_describe_image",
        instructions="given an image and a description of the image, improve the description, make sure the description is a list of observations of the image and that the description matches the content of the image",
        output_schema=Description,
        input={
            "_opper_media_input": media_input,  # this field name is required by opper
            "proposed_description": proposed_description,
        },
        model="openai/gpt-4o",
    )
    return response


def run_sync():
    print("Running sync examples...")
    description = "a cat with a hat and a hat on the cat and a hat on the cat"
    generated_image_str = generate_image(description)
    path = save_file(base64.b64decode(generated_image_str))
    print(f"sync generated image based on description: {description} -> {path}")

    media_input = f"data:image/png;base64,{generated_image_str}"
    proposed_description = "a cat with a hat"

    result = describe_image(media_input, proposed_description)
    print(f"sync describe_image result: {result}")


async def run_async():
    print("Running async examples...")
    description = "a cat with a hat and a hat on the cat and a hat on the cat"
    generated_image_str = await async_generate_image(description)
    path = save_file(base64.b64decode(generated_image_str))
    print(f"async generated image based on description: {description} -> {path}")

    media_input = f"data:image/png;base64,{generated_image_str}"
    proposed_description = "a cat with a hat"

    result = await async_describe_image(media_input, proposed_description)
    print(f"async describe_image result: {result}")


def main(run_type: str = "both"):
    run_type = run_type.strip().lower()
    if run_type == "sync":
        run_sync()
    elif run_type == "async":
        asyncio.run(run_async())
    else:
        print("running both sync and async...")
        run_sync()
        asyncio.run(run_async())


if __name__ == "__main__":
    import sys

    run_type = sys.argv[1] if len(sys.argv) > 1 else "both"
    main(run_type)
