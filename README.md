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
from opperai import AsyncOpper
from opperai.types import Message

async def main():
    opper = AsyncOpper()

    function = await opper.functions.create(
        "jokes/tell", 
        instructions="given a topic tell a joke",
    )
    
    response = await function.chat(
        messages=[Message(role="user", content="topic: python")],
    )

    print(response)

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
from opperai import AsyncOpper
from opperai.types import Message


async def main():
    opper = AsyncOpper()
    
    function = await opper.functions.create(
        "jokes/tell", 
        instructions="given a topic tell a joke",
        description="tell a joke",
    )

    response = await function.chat(
        messages=[Message(role="user", content="topic: python")],
        stream=True,
    )

    async for delta in response.deltas:
        print(delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
```

## Indexes

```python
from opperai import Opper
from opperai.types import Document, Filter

opper = Opper()

index = opper.indexes.create("my-index")

index.upload_file("file.txt")

index.add(Document(key="key1", content="Hello world 1", metadata={"score": 0}))
index.add(Document(key="key1", content="Hello world 1", metadata={"score": 1}))
index.add(Document(key="key2", content="Hello world 3", metadata={"score": 0}))

response = index.query("Hello")
print(response)

response = index.query("Hello", filters=[Filter(key="score", operation="=", value="1")])
print(response)
```

# Examples

See examples in our [documentation](https://docs.opper.ai)
