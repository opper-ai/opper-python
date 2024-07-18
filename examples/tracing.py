import asyncio

from opperai import fn, trace
from pydantic import BaseModel


class TranslationInput(BaseModel):
    text: str
    language: str


class TranslationResult(BaseModel):
    translation: str
    sentiment: str


class HappyTranslationResult(BaseModel):
    text: str


@trace
@fn(model="anthropic/claude-3-haiku")
def translate(input: TranslationInput) -> TranslationResult:
    """Translate the input text to the specified language"""


@trace
@fn(model="anthropic/claude-3-haiku")
async def translate_async(input: TranslationInput) -> TranslationResult:
    """Translate the input text to the specified language"""


@trace
@fn
def happify(input: TranslationResult) -> HappyTranslationResult:
    """Make the input text happier!"""


@trace
@fn
async def happify_async(input: TranslationResult) -> HappyTranslationResult:
    """Make the input text happier!"""


@trace
def transform():
    print("Transforming sync")
    result = translate(TranslationInput(text="Hello, world!", language="French"))
    happified, response = happify.call(result)
    print(happified)

    response.span.save_metric("happiness", len(happified.text))


@trace
async def transform_async():
    print("Transforming async")
    result = await translate_async(
        TranslationInput(text="Hello, world!", language="French")
    )
    happified, response = await happify_async.call(result)
    print(happified)

    await response.span.save_metric("happiness", len(happified.text))


transform()
asyncio.run(transform_async())
