import asyncio
from tempfile import NamedTemporaryFile

from opperai import AsyncOpper, Opper
from opperai.types import ImageOutput

opper = Opper()


def write_bytes(bytes: bytes, path: str = None) -> str:
    if path is None:
        with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            path = temp_file.name

    with open(path, "wb") as f:
        f.write(bytes)
        f.close()

    return path


def generate_image(description: str) -> ImageOutput:
    image, _ = opper.call(
        name="generate_image",
        output_type=ImageOutput,
        input=description,
    )
    return image


image = generate_image("a cat with a hat and a hat on the cat and a hat on the cat")
path = write_bytes(image.bytes)

print(path)

aopper = AsyncOpper()


async def async_generate_image(description: str) -> ImageOutput:
    image, _ = await aopper.call(
        name="async_generate_image",
        output_type=ImageOutput,
        input=description,
    )
    return image


image = asyncio.run(
    async_generate_image("a cat with a hat and a hat on the cat and a hat on the cat")
)
path = write_bytes(image.bytes)

print(path)
