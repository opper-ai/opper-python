import sys
sys.path.append('../src')
from opperai import AsyncClient
from opperai import fn, start_span
from opperai.types.indexes import Index, Document
from pydantic import BaseModel, Field
from typing import List, Dict
import inspect
import json

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

class Param(BaseModel):
    param: str = Field(description="The parameters name")
    type: str = Field(description="The parameters type")
    description: str = Field(description="The parameters description")

class Elements(BaseModel):
    heading: str = Field(description="Very short title of the method, for example 'Index a document', 'Create a function', 'Save an Example'")
    label: str
    description: str = Field(description="High level description of what the method does")
    required_parameters: List[Param] = Field(description="List of required parameters and their type and description")
    optional_parameters: List[Param] = Field(description="List of optional parameters and their type and description")
    returns: List[Param] = Field(description="List of returns and their type and description")
    exceptions: List[Param] = Field(description="List of exceptions and their type and description")
    examples: str = Field(description="String of code examples. Remove any >>> syntax")


@fn(path="test/get_elements", model="openai/gpt4-turbo")
def get_elements(docstring=str, template=str ) -> Elements:
  """ Parse the docstring into Elements so that it can be used in template"""

@fn(path="test/docgen", model="openai/gpt4-turbo")
def generate_doc(elements=Elements, template=str ) -> str:
    """ You are an agent that generates documentation snippets in mdx form from docstrings. 
    When called, you are provided a docstring for a function and your task is to use the template to generate a similar snippet of documentation.
    You will notice in the template that all documentation snippets starts with a title and a label highlighting the method name.
    The title should always be a very simple such as "Create a Function" or "Start a trace"
    You will notice that each documentation snippet is wrapped in a <row> element, with two <col> elements.
    In the first col you put heading, label, then a description, then Required Parameters, then Optional Parameters, then Returns, then Exceptions and then other elemens, finally the Examples in a separate col.
    The first col is non sticky, and the second col is.

    Here are rules to follow:
    - The Elements contains the *facts*, use the template only for structural guidence.
    - Make sure to put examples in a col sticky element """

def collect_docstrings(client_attrs):
    docstrings = []
    for client_attr in client_attrs:
        for func_name in dir(client_attr):
            func = getattr(client_attr, func_name)
            # Check if func is a bound method
            if (callable(func) and inspect.ismethod(func)) or func_name == "start_span":
                docstring = func.__doc__
                if docstring and len(docstring) > 25:
                    print(f"{client_attr.__class__.__name__}.{func_name}")
                    docstrings.append((f"{client_attr.__class__.__name__}.{func_name}", docstring))
    return docstrings


def build_docs(docstrings):
    with open("docs.mdx", 'w') as mdx_file, open("docs.json", 'w') as json_file:
        as_dict = {}
        for func_name, docstring in docstrings:
            elements = get_elements(docstring=docstring, template=template)
            doc = generate_doc(elements=elements, template=template)
            mdx_file.write(doc + "\n\n" + "---" + "\n\n")
            as_dict[func_name] = elements.dict()
        
        json_file.write(json.dumps(as_dict))


async def write_method_docs(client_attrs):
    docstrings = collect_docstrings(client_attrs)
    build_docs(docstrings)

                      
import asyncio               
with start_span(name="docsgen"):
      asyncio.run(write_method_docs([client.functions, client.indexes, client.spans]))
