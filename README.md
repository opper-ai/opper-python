# Opper Python SDK

## Install

```bash
pip install opperai
```

## Configuration

### Environment variable

- `OPPER_API_KEY` environment variable is read by the SDK if no `api_key` is provided to the `Client` object. 
- `OPPER_PROJECT` is attached to traces and can be used for filtering in the Opper UI.
- `OPPER_DEFAULT_MODEL` will define the model used by functions created with the `fn` decorator

When using the `fn` decorator the SDK client is automatically initialized with the `OPPER_API_KEY` environment variable.

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
from opperai import Opper
from opperai.types import Message

opper = Opper()
function = opper.functions.create(
    "jokes/tell", 
    instructions="given a topic tell a joke",
)

response = function.chat(
    messages=[Message(role="user", content="topic: python")]
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
        "jokes/tell",
        ChatPayload(messages=[Message(role="user", content="topic: python")]),
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
from opperai import Opper
from opperai.types import Message

opper = Opper()
function = opper.functions.create(
    "jokes/tell", 
    instructions="given a topic tell a joke",
    description="tell a joke",
)
response = function.chat(
    messages=[Message(role="user", content="topic: python")],
    stream=True
)
for delta in response.deltas:
    print(delta, end="", flush=True)
```

## Async streaming responses

```python
import asyncio
from opperai import AsyncClient
from opperai.types import ChatPayload, Message

client = AsyncClient(api_key="your-api-key")

async def main():
    async for response in await client.functions.chat(
        "jokes/tell",
        ChatPayload(
            messages=[Message(role="user", content="topic: python")],
        ),
        stream=True,
    ):
        print(response.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
```

## Indexes

```python
from opperai import Opper
from opperai.types import Document, Filter

opper = Opper()

# create a new (or get existing) index
index = opper.indexes.create("my-index")

# upload a file to the index
index.upload_file("file.txt")

# index a document
index.index(Document(key="key1", content="Hello world", metadata={"score": 0}))

# overwrite a document
index.index(Document(key="key1", content="Hello world", metadata={"score": 1}))

# query the index
response = index.query("Hello")
print(response)

# query the index with a filter
response = index.query("Hello", filters=[Filter(key="score", operation="=", value="1")])
print(response)
```

# Examples

See examples in our [documentation](https://docs.opper.ai)
