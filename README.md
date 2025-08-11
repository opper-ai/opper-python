# opperai



<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=opperai&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<!-- Start Summary [summary] -->
## Summary


<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [opperai](#opperai)
  * [SDK Installation](#sdk-installation)
  * [SDK Example Usage](#sdk-example-usage)
  * [SDK Installation](#sdk-installation-1)
  * [IDE Support](#ide-support)
  * [SDK Example Usage](#sdk-example-usage-1)
  * [Authentication](#authentication)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Server-sent event streaming](#server-sent-event-streaming)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Custom HTTP Client](#custom-http-client)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client-1)
  * [Resource Management](#resource-management)
  * [Debugging](#debugging)
* [Development](#development)
  * [Maturity](#maturity)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation


### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install opperai
```

### Poetry / UV

If you use [UV](https://docs.astral.sh/uv/)

```bash
uv add opperai
```


Poetry

```bash
poetry add opperai
```




## SDK Example Usage
[![Explore Docs](https://img.shields.io/badge/Docs-Read%20the%20Docs-black??style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMTUgMzE1Ij48dGl0bGU+T3BwZXI8L3RpdGxlPjxnIGNsaXAtcGF0aD0idXJsKCNjbGlwMCkiPjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNMTA1LjA0IDE1Ny41MkMxMjAuNiAxNTcuMzQgMTYwLjUyIDE1MS41NCAxNjAuNTIgOTYuNTYwMUMxNjAuNTIgMTUxLjU0IDIwMC40NCAxNTcuMzQgMjE2IDE1Ny41MkMxNjQuMSAxNjEuNjMgMTYwLjUyIDIxNy45OCAxNjAuNTIgMjE3Ljk4QzE2MC41MiAyMTcuOTggMTU2Ljk0IDE2MS42NSAxMDUuMDQgMTU3LjUyWk0xNTkuNzggMzE1QzcxLjUzIDMxNSAwIDI0NC40OSAwIDE1Ny41QzAgLTE4Ljk0OTkgMTU5Ljc4IDAuNjUwMDc1IDE1OS43OCAwLjY1MDA3NUMxNTkuNzggODcuMjIgODguMzYgMTU3LjQgMC4yIDE1Ny41QzE0OS44IDE1Ny42NCAxNTkuNzggMzE1IDE1OS43OCAzMTVaIiBmaWxsPSJ1cmwoI2dyYWQpIi8+PC9nPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZCIgeDE9IjcyLjM4IiB5MT0iNTQuNzgwMSIgeDI9IjEzOS41MiIgeTI9IjI3MC44IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agc3RvcC1jb2xvcj0iIzhDRUNGMiIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI0Y5QjU4QyIvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjwvc3ZnPg==
)](https://docs.opper.ai)

### First steps
Log in at [opper](platform.opper.ai) and create your own API key in the top right menu. Each api key is associated with a project, you will have all calls, functions, indexes and traces associated with this project. There is a default project for each organization but it is recommended to create a new project to better being able to separate the different applications and environments.


For many **examples** and **guides** of how to use our sdks check out our examples folder [examples](./examples/)

### Example

```python
from opperai import Opper
# Our SDK supports Pydantic to provide structured output
from pydantic import BaseModel
import os

# Define the output structure
class RoomDescription(BaseModel):
    room_count: int
    view: str
    bed_size: str
    hotel_name: str

def main():
    opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))

    # Complete a task
    completion = opper.call(
        name="extractRoom",
        instructions="Extract details about the room from the provided text",
        input="The Grand Hotel offers a luxurious suite with 3 spacious rooms, each providing a breathtaking view of the ocean. The suite includes a king-sized bed, an en-suite bathroom, and a private balcony for an unforgettable stay.",
        output_schema=RoomDescription,
    )

    print(completion.json_payload)
    #{'room_count': 3, 'view': 'ocean', 'bed_size': 'king-sized', 'hotel_name': 'The Grand Hotel'}

main()
```
</br>

The same SDK client can also be used to make asychronous requests by importing asyncio. Just add `_async` to the call
<details closed>
<summary>Async example</summary>

```python
# Asynchronous Example
import asyncio
import os
from opperai import Opper
from pydantic import BaseModel

# Define the output structure
class RoomDescription(BaseModel):
    room_count: int
    view: str
    bed_size: str
    hotel_name: str

async def main():
    opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))

    # Complete a task asynchronously
    completion = await opper.call_async(
        name="extractRoom",
        instructions="Extract details about the room from the provided text",
        input="The Grand Hotel offers a luxurious suite with 3 spacious rooms, each providing a breathtaking view of the ocean. The suite includes a king-sized bed, an en-suite bathroom, and a private balcony for an unforgettable stay.",
        output_schema=RoomDescription,
    )

    print(completion.json_payload)
    # {'room_count': 3, 'view': 'ocean', 'bed_size': 'king-sized', 'hotel_name': 'The Grand Hotel'}

# Run the async main function
asyncio.run(main())
```
</details>
<!-- End SDK Example Usage [usage] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!TIP]
> To finish publishing your SDK to PyPI you must [run your first generation action](https://www.speakeasy.com/docs/github-setup#step-by-step-guide).


> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install git+<UNSET>.git
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add git+<UNSET>.git
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from opperai python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "opperai",
# ]
# ///

from opperai import Opper

sdk = Opper(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.call(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
        "properties": {
            "x": {
                "title": "X",
                "type": "integer",
            },
            "y": {
                "title": "Y",
                "type": "integer",
            },
        },
        "required": [
            "x",
            "y",
        ],
        "title": "OpperInputExample",
        "type": "object",
    }, output_schema={
        "properties": {
            "sum": {
                "title": "Sum",
                "type": "integer",
            },
        },
        "required": [
            "sum",
        ],
        "title": "OpperOutputExample",
        "type": "object",
    }, input={
        "x": 4,
        "y": 5,
    }, examples=[
        {
            "input": {
                "x": 1,
                "y": 3,
            },
            "output": {
                "sum": 4,
            },
            "comment": "Adds two numbers",
        },
    ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
        "project": "project_456",
        "user": "company_123",
    }, configuration={})

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from opperai import Opper
import os

async def main():

    async with Opper(
        http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
    ) as opper:

        res = await opper.call_async(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
            "properties": {
                "x": {
                    "title": "X",
                    "type": "integer",
                },
                "y": {
                    "title": "Y",
                    "type": "integer",
                },
            },
            "required": [
                "x",
                "y",
            ],
            "title": "OpperInputExample",
            "type": "object",
        }, output_schema={
            "properties": {
                "sum": {
                    "title": "Sum",
                    "type": "integer",
                },
            },
            "required": [
                "sum",
            ],
            "title": "OpperOutputExample",
            "type": "object",
        }, input={
            "x": 4,
            "y": 5,
        }, examples=[
            {
                "input": {
                    "x": 1,
                    "y": 3,
                },
                "output": {
                    "sum": 4,
                },
                "comment": "Adds two numbers",
            },
        ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
            "project": "project_456",
            "user": "company_123",
        }, configuration={})

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name          | Type | Scheme      | Environment Variable |
| ------------- | ---- | ----------- | -------------------- |
| `http_bearer` | http | HTTP Bearer | `OPPER_HTTP_BEARER`  |

To authenticate with the API the `http_bearer` parameter must be set when initializing the SDK client instance. For example:
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.call(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
        "properties": {
            "x": {
                "title": "X",
                "type": "integer",
            },
            "y": {
                "title": "Y",
                "type": "integer",
            },
        },
        "required": [
            "x",
            "y",
        ],
        "title": "OpperInputExample",
        "type": "object",
    }, output_schema={
        "properties": {
            "sum": {
                "title": "Sum",
                "type": "integer",
            },
        },
        "required": [
            "sum",
        ],
        "title": "OpperOutputExample",
        "type": "object",
    }, input={
        "x": 4,
        "y": 5,
    }, examples=[
        {
            "input": {
                "x": 1,
                "y": 3,
            },
            "output": {
                "sum": 4,
            },
            "comment": "Adds two numbers",
        },
    ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
        "project": "project_456",
        "user": "company_123",
    }, configuration={})

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [analytics](docs/sdks/analytics/README.md)

* [get_usage](docs/sdks/analytics/README.md#get_usage) - Usage

### [datasets](docs/sdks/datasets/README.md)

* [create_entry](docs/sdks/datasets/README.md#create_entry) - Create Dataset Entry
* [list_entries](docs/sdks/datasets/README.md#list_entries) - List Dataset Entries
* [get_entry](docs/sdks/datasets/README.md#get_entry) - Get Dataset Entry
* [delete_entry](docs/sdks/datasets/README.md#delete_entry) - Delete Dataset Entry
* [query_entries](docs/sdks/datasets/README.md#query_entries) - Query Dataset Entries

#### [datasets.entries](docs/sdks/entries/README.md)

* [update](docs/sdks/entries/README.md#update) - Update Dataset Entry

### [embeddings](docs/sdks/embeddings/README.md)

* [create](docs/sdks/embeddings/README.md#create) - Create Embedding

### [functions](docs/sdks/functions/README.md)

* [create](docs/sdks/functions/README.md#create) - Create Function
* [list](docs/sdks/functions/README.md#list) - List Functions
* [get](docs/sdks/functions/README.md#get) - Get Function
* [update](docs/sdks/functions/README.md#update) - Update Function
* [delete](docs/sdks/functions/README.md#delete) - Delete Function
* [get_by_name](docs/sdks/functions/README.md#get_by_name) - Get Function By Name
* [get_by_revision](docs/sdks/functions/README.md#get_by_revision) - Get Function By Revision
* [call](docs/sdks/functions/README.md#call) - Call Function
* [stream](docs/sdks/functions/README.md#stream) - Stream Function
* [call_revision](docs/sdks/functions/README.md#call_revision) - Call Function Revision
* [stream_revision](docs/sdks/functions/README.md#stream_revision) - Stream Function Revision

#### [functions.revisions](docs/sdks/revisions/README.md)

* [list](docs/sdks/revisions/README.md#list) - List Function Revisions

### [knowledge](docs/sdks/knowledge/README.md)

* [create](docs/sdks/knowledge/README.md#create) - Create Knowledge Base
* [list](docs/sdks/knowledge/README.md#list) - List Knowledge Bases
* [get](docs/sdks/knowledge/README.md#get) - Get Knowledge Base
* [delete](docs/sdks/knowledge/README.md#delete) - Delete Knowledge Base
* [get_by_name](docs/sdks/knowledge/README.md#get_by_name) - Get Knowledge Base By Name
* [get_upload_url](docs/sdks/knowledge/README.md#get_upload_url) - Get Upload Url
* [register_file_upload](docs/sdks/knowledge/README.md#register_file_upload) - Register File Upload
* [delete_file](docs/sdks/knowledge/README.md#delete_file) - Delete File From Knowledge Base
* [query](docs/sdks/knowledge/README.md#query) - Query Knowledge Base
* [add](docs/sdks/knowledge/README.md#add) - Add

### [language_models](docs/sdks/languagemodels/README.md)

* [list](docs/sdks/languagemodels/README.md#list) - List Models
* [register_custom](docs/sdks/languagemodels/README.md#register_custom) - Register Custom Model
* [list_custom](docs/sdks/languagemodels/README.md#list_custom) - List Custom Models
* [get_custom](docs/sdks/languagemodels/README.md#get_custom) - Get Custom Model
* [update_custom](docs/sdks/languagemodels/README.md#update_custom) - Update Custom Model
* [delete_custom](docs/sdks/languagemodels/README.md#delete_custom) - Delete Custom Model
* [get_custom_by_name](docs/sdks/languagemodels/README.md#get_custom_by_name) - Get Custom Model By Name

### [openai](docs/sdks/openai/README.md)

* [create_chat_completion](docs/sdks/openai/README.md#create_chat_completion) - Chat Completions

### [Opper SDK](docs/sdks/opper/README.md)

* [call](docs/sdks/opper/README.md#call) - Function Call
* [stream](docs/sdks/opper/README.md#stream) - Function Stream

### [span_metrics](docs/sdks/spanmetrics/README.md)

* [create_metric](docs/sdks/spanmetrics/README.md#create_metric) - Create Metric
* [list](docs/sdks/spanmetrics/README.md#list) - List Metrics
* [get](docs/sdks/spanmetrics/README.md#get) - Get Metric
* [update_metric](docs/sdks/spanmetrics/README.md#update_metric) - Update Metric
* [delete](docs/sdks/spanmetrics/README.md#delete) - Delete Metric

### [spans](docs/sdks/spans/README.md)

* [create](docs/sdks/spans/README.md#create) - Create Span
* [get](docs/sdks/spans/README.md#get) - Get Span
* [update](docs/sdks/spans/README.md#update) - Update Span
* [delete](docs/sdks/spans/README.md#delete) - Delete Span
* [save_examples](docs/sdks/spans/README.md#save_examples) - Save To Dataset

### [traces](docs/sdks/traces/README.md)

* [list](docs/sdks/traces/README.md#list) - List Traces
* [get](docs/sdks/traces/README.md#get) - Get Trace

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Server-sent event streaming [eventstream] -->
## Server-sent event streaming

[Server-sent events][mdn-sse] are used to stream content from certain
operations. These operations will expose the stream as [Generator][generator] that
can be consumed using a simple `for` loop. The loop will
terminate when the server no longer has any events to send and closes the
underlying connection.  

The stream is also a [Context Manager][context-manager] and can be used with the `with` statement and will close the
underlying connection when the context is exited.

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.stream(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
        "properties": {
            "x": {
                "title": "X",
                "type": "integer",
            },
            "y": {
                "title": "Y",
                "type": "integer",
            },
        },
        "required": [
            "x",
            "y",
        ],
        "title": "OpperInputExample",
        "type": "object",
    }, output_schema={
        "properties": {
            "sum": {
                "title": "Sum",
                "type": "integer",
            },
        },
        "required": [
            "sum",
        ],
        "title": "OpperOutputExample",
        "type": "object",
    }, input={
        "x": 4,
        "y": 5,
    }, examples=[
        {
            "input": {
                "x": 1,
                "y": 3,
            },
            "output": {
                "sum": 4,
            },
            "comment": "Adds two numbers",
        },
    ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
        "project": "project_456",
        "user": "company_123",
    }, configuration={})

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

[mdn-sse]: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
[generator]: https://book.pythontips.com/en/latest/generators.html
[context-manager]: https://book.pythontips.com/en/latest/context_managers.html
<!-- End Server-sent event streaming [eventstream] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from opperai import Opper
from opperai.utils import BackoffStrategy, RetryConfig
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.call(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
        "properties": {
            "x": {
                "title": "X",
                "type": "integer",
            },
            "y": {
                "title": "Y",
                "type": "integer",
            },
        },
        "required": [
            "x",
            "y",
        ],
        "title": "OpperInputExample",
        "type": "object",
    }, output_schema={
        "properties": {
            "sum": {
                "title": "Sum",
                "type": "integer",
            },
        },
        "required": [
            "sum",
        ],
        "title": "OpperOutputExample",
        "type": "object",
    }, input={
        "x": 4,
        "y": 5,
    }, examples=[
        {
            "input": {
                "x": 1,
                "y": 3,
            },
            "output": {
                "sum": 4,
            },
            "comment": "Adds two numbers",
        },
    ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
        "project": "project_456",
        "user": "company_123",
    }, configuration={},
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from opperai import Opper
from opperai.utils import BackoffStrategy, RetryConfig
import os


with Opper(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.call(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
        "properties": {
            "x": {
                "title": "X",
                "type": "integer",
            },
            "y": {
                "title": "Y",
                "type": "integer",
            },
        },
        "required": [
            "x",
            "y",
        ],
        "title": "OpperInputExample",
        "type": "object",
    }, output_schema={
        "properties": {
            "sum": {
                "title": "Sum",
                "type": "integer",
            },
        },
        "required": [
            "sum",
        ],
        "title": "OpperOutputExample",
        "type": "object",
    }, input={
        "x": 4,
        "y": 5,
    }, examples=[
        {
            "input": {
                "x": 1,
                "y": 3,
            },
            "output": {
                "sum": 4,
            },
            "comment": "Adds two numbers",
        },
    ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
        "project": "project_456",
        "user": "company_123",
    }, configuration={})

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

[`OpperError`](./src/opperai/errors/oppererror.py) is the base class for all HTTP error responses. It has the following properties:

| Property           | Type             | Description                                                                             |
| ------------------ | ---------------- | --------------------------------------------------------------------------------------- |
| `err.message`      | `str`            | Error message                                                                           |
| `err.status_code`  | `int`            | HTTP response status code eg `404`                                                      |
| `err.headers`      | `httpx.Headers`  | HTTP response headers                                                                   |
| `err.body`         | `str`            | HTTP body. Can be empty string if no body is returned.                                  |
| `err.raw_response` | `httpx.Response` | Raw HTTP response                                                                       |
| `err.data`         |                  | Optional. Some errors may contain structured data. [See Error Classes](#error-classes). |

### Example
```python
from opperai import Opper, errors
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:
    res = None
    try:

        res = opper.call(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
            "properties": {
                "x": {
                    "title": "X",
                    "type": "integer",
                },
                "y": {
                    "title": "Y",
                    "type": "integer",
                },
            },
            "required": [
                "x",
                "y",
            ],
            "title": "OpperInputExample",
            "type": "object",
        }, output_schema={
            "properties": {
                "sum": {
                    "title": "Sum",
                    "type": "integer",
                },
            },
            "required": [
                "sum",
            ],
            "title": "OpperOutputExample",
            "type": "object",
        }, input={
            "x": 4,
            "y": 5,
        }, examples=[
            {
                "input": {
                    "x": 1,
                    "y": 3,
                },
                "output": {
                    "sum": 4,
                },
                "comment": "Adds two numbers",
            },
        ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
            "project": "project_456",
            "user": "company_123",
        }, configuration={})

        # Handle response
        print(res)


    except errors.OpperError as e:
        # The base class for HTTP error responses
        print(e.message)
        print(e.status_code)
        print(e.body)
        print(e.headers)
        print(e.raw_response)

        # Depending on the method different errors may be thrown
        if isinstance(e, errors.BadRequestError):
            print(e.data.type)  # Optional[str]
            print(e.data.message)  # Optional[str]
            print(e.data.detail)  # Any
```

### Error Classes
**Primary errors:**
* [`OpperError`](./src/opperai/errors/oppererror.py): The base class for HTTP error responses.
  * [`BadRequestError`](./src/opperai/errors/badrequesterror.py): Bad Request. Status code `400`.
  * [`UnauthorizedError`](./src/opperai/errors/unauthorizederror.py): Unauthorized. Status code `401`.
  * [`NotFoundError`](./src/opperai/errors/notfounderror.py): Not Found. Status code `404`.
  * [`RequestValidationError`](./src/opperai/errors/requestvalidationerror.py): Request Validation Error. Status code `422`. *

<details><summary>Less common errors (7)</summary>

<br />

**Network errors:**
* [`httpx.RequestError`](https://www.python-httpx.org/exceptions/#httpx.RequestError): Base class for request errors.
    * [`httpx.ConnectError`](https://www.python-httpx.org/exceptions/#httpx.ConnectError): HTTP client was unable to make a request to a server.
    * [`httpx.TimeoutException`](https://www.python-httpx.org/exceptions/#httpx.TimeoutException): HTTP request timed out.


**Inherit from [`OpperError`](./src/opperai/errors/oppererror.py)**:
* [`ConflictError`](./src/opperai/errors/conflicterror.py): Conflict. Status code `409`. Applicable to 3 of 52 methods.*
* [`Error`](./src/opperai/errors/error.py): Request validation error. Applicable to 1 of 52 methods.*
* [`ResponseValidationError`](./src/opperai/errors/responsevalidationerror.py): Type mismatch between the response data and the expected Pydantic model. Provides access to the Pydantic validation error via the `cause` attribute.

</details>

\* Check [the method documentation](#available-resources-and-operations) to see if the error is applicable.
<!-- End Error Handling [errors] -->

## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from opperai import Opper
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Opper(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from opperai import Opper
from opperai.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Opper(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from opperai import Opper
import os


with Opper(
    server_url="https://api.opper.ai/v2",
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.call(name="add_numbers", instructions="Calculate the sum of two numbers", input_schema={
        "properties": {
            "x": {
                "title": "X",
                "type": "integer",
            },
            "y": {
                "title": "Y",
                "type": "integer",
            },
        },
        "required": [
            "x",
            "y",
        ],
        "title": "OpperInputExample",
        "type": "object",
    }, output_schema={
        "properties": {
            "sum": {
                "title": "Sum",
                "type": "integer",
            },
        },
        "required": [
            "sum",
        ],
        "title": "OpperOutputExample",
        "type": "object",
    }, input={
        "x": 4,
        "y": 5,
    }, examples=[
        {
            "input": {
                "x": 1,
                "y": 3,
            },
            "output": {
                "sum": 4,
            },
            "comment": "Adds two numbers",
        },
    ], parent_span_id="123e4567-e89b-12d3-a456-426614174000", tags={
        "project": "project_456",
        "user": "company_123",
    }, configuration={})

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from opperai import Opper
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Opper(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from opperai import Opper
from opperai.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Opper(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Opper` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
from opperai import Opper
import os
def main():

    with Opper(
        http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
    ) as opper:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Opper(
        http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
    ) as opper:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from opperai import Opper
import logging

logging.basicConfig(level=logging.DEBUG)
s = Opper(debug_logger=logging.getLogger("opperai"))
```

You can also enable a default debug logger by setting an environment variable `OPPER_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=opperai&utm_campaign=python)
