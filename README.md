# Opper Python SDK

## Install

```bash
pip install opperai
```

## Using the `fn` decorator

```python
from opperai import fn

@fn()
def translate(text: str, target_language: str) -> str:
    """Translate text to a target language."""


print(translate("Hello","fr"))

>>> "Bonjour"
```

The `fn` decorator automatically creates an Opper function ready to be called like any other function in your code. They're no different than any other function!

## Calling functions

To call a function you created at [https://platform.opper.ai](https://platform.opper.ai) you can use the following code:


```python
from opperai import Client
from opperai.types import ChatPayload, Message

client = Client(api_key="your-api-key") 
response = client.functions.chat("your-function-path", 
  ChatPayload(messages=[Message(role="user", content="hello")])
)

print(response)
```

## Async function calling

```python
import asyncio
from opperai import AsyncClient
from opperai.types import ChatPayload, Message

opper = AsyncClient(api_key="your-api-key")

async def main():
    message = ""
    async for response in await opper.functions.chat(
        "your-function-path",
        ChatPayload(messages=[Message(role="user", content="Hello, world!")]),
        stream=True,
    ):
        if response.delta is not None:
            message += response.delta

    print(message)

if __name__ == "__main__":
    asyncio.run(main())
```

## Streaming responses

```python
from opperai import Client
from opperai.types import ChatPayload, Message

client = Client(api_key="op-xxxx")
response = client.functions.chat(
    "joch/test",
    ChatPayload(
        messages=[Message(role="user", content="tell me a story.")],
    ),
    stream=True,
)
for data in response:
    print(data.delta, end="", flush=True)
```

## Async streaming responses

```python
import asyncio
from opperai import AsyncClient
from opperai.types import ChatPayload, Message

client = AsyncClient(api_key="your-api-key")

async def main():
    async for response in await client.functions.chat(
        "your-function-path",
        ChatPayload(
            messages=[Message(role="user", content="tell me a story.")],
        ),
        stream=True,
    ):
        print(response.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
```

## Retrieval

```python
client.indexes.retrieve(index_id=42, "Who is the president of the USA?", 3)

```

## Configuration

### Environment variable

The `OPPER_API_KEY` environment variable is read by the SDK if no `api_key` is provided to the `Client` object. 

When using the `fn` decorator the SDK client is automatically initialized with the `OPPER_API_KEY` environment variable.
