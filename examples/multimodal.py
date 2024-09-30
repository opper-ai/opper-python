import asyncio
from tempfile import NamedTemporaryFile
from typing import List

from pydantic import BaseModel, Field

from opperai import AsyncOpper, Opper
from opperai.types import AudioInput, CallConfiguration, ImageInput, ImageOutput

opper = Opper()


def save_file(bytes: bytes, path: str = None) -> str:
    if path is None:
        with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            path = temp_file.name

    with open(path, "wb") as f:
        f.write(bytes)
        f.close()

    return path


def generate_image(description: str, model: str = "azure/dall-e-3-eu") -> ImageOutput:
    image, _ = opper.call(
        name="generate_image",
        output_type=ImageOutput,
        input=description,
        model=model,
        configuration=CallConfiguration(
            model_parameters={
                "size": "1792x1024",
                "quality": "hd",
            }
        ),
    )
    return image


description = "a cat with a hat and a hat on the cat and a hat on the cat"
path = save_file(generate_image(description).bytes)
print(f"generated image based on description: {description} -> {path}")


class Description(BaseModel):
    observations: List[str] = Field(description="The observations of the image")
    original_description: str = Field(
        description="The original description of the image"
    )
    improved_description: str = Field(
        description="The improved description of the image"
    )


class Image(BaseModel):
    image: ImageInput = Field(description="The image to describe")
    proposed_description: str = Field(
        description="The proposed description of the image"
    )


def describe_image(path: str) -> str:
    description, response = opper.call(
        name="describe_image",
        instructions="given an image and a description of the image, improve the description, make sure the description is a list of observations of the image and that the description matches the content of the image",
        output_type=Description,
        input=Image(
            image=ImageInput.from_path(path),
            proposed_description="a cat with a hat and a hat on the cat and a hat on the cat",
        ),
        model="openai/gpt-4o",
    )
    return description


def common_denominator(paths: List[str]) -> str:
    images = [ImageInput.from_path(path) for path in paths]
    description, response = opper.call(
        name="common_denominator",
        instructions="given a list of images, return the most common denominator of the images",
        output_type=str,
        input=images,
        model="openai/gpt-4o",
    )
    return description


def run_sync():
    image = generate_image("a cat with a hat and a hat on the cat and a hat on the cat")
    path = save_file(image.bytes)

    print(f"path: {path}")

    img1 = "tests/fixtures/images/cat1.png"
    img2 = "tests/fixtures/images/cat2.png"

    print(f"describe_image(img1): {describe_image(img1)}")
    print(f"describe_image(img2): {describe_image(img2)}")
    print(f"common_denominator([img1, img2]): {common_denominator([img1, img2])}")


aopper = AsyncOpper()


async def async_generate_image(
    description: str, model: str = "azure/dall-e-3-eu"
) -> ImageOutput:
    image, _ = await aopper.call(
        name="async_generate_image",
        output_type=ImageOutput,
        input=description,
        model=model,
        configuration=CallConfiguration(
            model_parameters={
                "size": "1792x1024",
                "quality": "hd",
            }
        ),
    )
    return image


async def async_describe_image(path: str) -> str:
    description, response = await aopper.call(
        name="async_describe_image",
        instructions="given an image and a description of the image, improve the description, make sure the description is a list of observations of the image and that the description matches the content of the image",
        output_type=Description,
        input=Image(
            image=ImageInput.from_path(path),
            proposed_description="a cat with a hat and a hat on the cat and a hat on the cat",
        ),
        model="openai/gpt-4o",
    )
    return description


async def async_common_denominator(paths: List[str]) -> str:
    images = [ImageInput.from_path(path) for path in paths]
    description, response = await aopper.call(
        name="async_common_denominator",
        instructions="given a list of images, return the most common denominator of the images",
        output_type=str,
        input=images,
        model="openai/gpt-4o",
    )
    return description


async def async_transcribe_audio(path: str) -> str:
    transcription, response = await aopper.call(
        name="async_transcribe_audio",
        instructions="given an audio file, return the transcription of the audio",
        output_type=str,
        input=AudioInput.from_path(path),
        model="gcp/gemini-1.5-flash-eu",
    )
    return transcription


async def run_async():
    image = await async_generate_image(
        "a cat with a hat and a hat on the cat and a hat on the cat"
    )
    path = save_file(image.bytes)

    print(f"async path: {path}")

    img1 = "tests/fixtures/images/cat1.png"
    img2 = "tests/fixtures/images/cat2.png"

    describe_img1, describe_img2, common_desc = await asyncio.gather(
        async_describe_image(img1),
        async_describe_image(img2),
        async_common_denominator([img1, img2]),
    )

    print(f"async describe_image(img1): {describe_img1}")
    print(f"async describe_image(img2): {describe_img2}")
    print(f"async common_denominator([img1, img2]): {common_desc}")


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
