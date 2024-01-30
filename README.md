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

## Calling functions manually

To call a function you created at [https://platform.opper.ai](https://platform.opper.ai) you can use the following code:


```python
from opperai import Client
from opperai.types import ChatPayload, Message

# Use AsyncClient for async operations
client = Client(api_key="your-api-key") 
response = client.functions.chat("your-function-path", 
 ChatPayload(messages=[Message(role="user", content="hello")])
)

print(response)

```

This more traditional API is better targeted for chat use cases.

## Configuration

### Environment variable

The `OPPER_API_KEY` environment variable is read by the SDK if no `api_key` is provided to the `Client` object. 

When using the `fn` decorator the SDK client is automatically initialized with the `OPPER_API_KEY` environment variable.
