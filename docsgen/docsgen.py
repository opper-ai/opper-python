import sys
sys.path.append('../src')
from opperai import AsyncClient
from opperai import fn
import inspect

client = AsyncClient()

template = """ 
## Create a Function {{ label: 'client.functions.create' }}

<Row>
  <Col>

  The `functions.create` method allows you to create a new function or update an existing one in the OpperAI service. This is essential for defining your custom logic for handling different types of requests.

  ### Required Parameters

  <Properties>
    <Property name="function" type="FunctionDescription">
      A description of the function including its path, inputs, and outputs.
    </Property>
  </Properties>

  ### Optional Parameters

  <Properties>
    <Property name="update" type="bool" default="True">
      If set to true, the existing function will be updated when a function with the same path already exists.
    </Property>
    <Property name="kwargs" type="object">
      Additional keyword arguments that will be included in the request payload.
    </Property>
  </Properties>

  ### Returns

  - **int**: The ID of the created or updated function.

  ### Exceptions

  - Throws **APIError**: If the function creation or update fails.

  </Col>
  <Col sticky>

```python
from opperai import Client
from opperai.types import FunctionDescription

client = Client(api_key="YOUR_API_KEY")

try:
    function = FunctionDescription(
        path="test/function",
        description="A function to translate text to French",
        instructions="Translate the given text to French."
    )
    
    response = client.functions.create(function, update=True)
    print(f"Function created: {response}")
except Exception as e:
    print(f"An error occurred: {e}")
```

  </Col>
</Row> """


@fn(path="test/docgen", model="openai/gpt4-turbo")
def generate_doc(docstring=str, template=str ) -> str:
    """ Given docstring, generate documentation in line with template. 
    The docstring contains the facts, the template is only for structural guidence.
    Make sure to put examples in a col sticky element """

def write_method_docs(client_attrs):
    with open("docs.mdx", 'w') as file:
        for client_attr in client_attrs:
            for func_name in dir(client_attr):
                func = getattr(client_attr, func_name)
                # Check if func is a bound method
                if callable(func) and inspect.ismethod(func):
                    docstring = func.__doc__
                    if docstring and len(docstring) > 50:
                        print(f"{func_name} method docstring:")
                        doc = generate_doc(docstring=docstring, template=template)
                        print(doc)
                        file.write(doc + "\n\n" + "---" +"\n\n")

write_method_docs([client.functions, client.indexes])
