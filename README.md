# [Opper](https//opper.ai) Python SDK

## Install

```bash
pip install opperai
```

## Functions

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

