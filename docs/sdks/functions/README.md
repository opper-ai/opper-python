# Functions
(*functions*)

## Overview

### Available Operations

* [create](#create) - Create Function
* [list](#list) - List Functions
* [get](#get) - Get Function
* [update](#update) - Update Function
* [delete](#delete) - Delete Function
* [get_by_name](#get_by_name) - Get Function By Name
* [get_by_revision](#get_by_revision) - Get Function By Revision
* [call](#call) - Call Function
* [stream](#stream) - Stream Function
* [call_revision](#call_revision) - Call Function Revision
* [stream_revision](#stream_revision) - Stream Function Revision

## create

Create a function

### Example Usage

<!-- UsageSnippet language="python" operationID="create_function_functions_post" method="post" path="/functions" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.create(name="my-function", instructions="You are a calculator that adds two numbers and returns the result.", description="This function is used to add two numbers and return the result.", input_schema={
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
    }, configuration={})

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                                                                                                    | Type                                                                                                                                                                                                                                                                                                                                                                                                         | Required                                                                                                                                                                                                                                                                                                                                                                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                  | Example                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`                                                                                                                                                                                                                                                                                                                                                                                                       | *str*                                                                                                                                                                                                                                                                                                                                                                                                        | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                           | The name of the function. Must be unique within the project and can only contain letters, numbers, underscores and hyphens.                                                                                                                                                                                                                                                                                  | my-function                                                                                                                                                                                                                                                                                                                                                                                                  |
| `instructions`                                                                                                                                                                                                                                                                                                                                                                                               | *str*                                                                                                                                                                                                                                                                                                                                                                                                        | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                           | The instructions for the function, this is the prompt that will be sent to the model to complete the task. Recommended to be concise and to the point                                                                                                                                                                                                                                                        | You are a calculator that adds two numbers and returns the result.                                                                                                                                                                                                                                                                                                                                           |
| `description`                                                                                                                                                                                                                                                                                                                                                                                                | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                           | Optional description of the function. This is used to describe the function to a user.                                                                                                                                                                                                                                                                                                                       | This function is used to add two numbers and return the result.                                                                                                                                                                                                                                                                                                                                              |
| `input_schema`                                                                                                                                                                                                                                                                                                                                                                                               | Dict[str, *Any*]                                                                                                                                                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                           | Optional input schema for the function. Can preferably include field descriptions to allow the model to reason about the input variables. Schema is validated against the input data and issues an error if it does not match. With the Opper SDKs you can define these schemas through libraries like Pydantic and Zod. For schemas with definitions, prefer using '$defs' and '#/$defs/...' references.    | {<br/>"properties": {<br/>"x": {<br/>"title": "X",<br/>"type": "integer"<br/>},<br/>"y": {<br/>"title": "Y",<br/>"type": "integer"<br/>}<br/>},<br/>"required": [<br/>"x",<br/>"y"<br/>],<br/>"title": "OpperInputExample",<br/>"type": "object"<br/>}                                                                                                                                                       |
| `output_schema`                                                                                                                                                                                                                                                                                                                                                                                              | Dict[str, *Any*]                                                                                                                                                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                           | Optional output schema for the function. Can preferably include field descriptions to allow the model to reason about the output variables. Schema is validated against the output data and issues an error if it does not match. With the Opper SDKs you can define these schemas through libraries like Pydantic and Zod. For schemas with definitions, prefer using '$defs' and '#/$defs/...' references. | {<br/>"properties": {<br/>"sum": {<br/>"title": "Sum",<br/>"type": "integer"<br/>}<br/>},<br/>"required": [<br/>"sum"<br/>],<br/>"title": "OpperOutputExample",<br/>"type": "object"<br/>}                                                                                                                                                                                                                   |
| `model`                                                                                                                                                                                                                                                                                                                                                                                                      | [Optional[models.TModel]](../../models/tmodel.md)                                                                                                                                                                                                                                                                                                                                                            | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                           | N/A                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                                              |
| `configuration`                                                                                                                                                                                                                                                                                                                                                                                              | [OptionalNullable[models.FunctionCallConfiguration]](../../models/functioncallconfiguration.md)                                                                                                                                                                                                                                                                                                              | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                           | Optional configuration for the function.Configuration is a dictionary of key-value pairs that can be used to override the default configuration for the function.                                                                                                                                                                                                                                            | {<br/>"beta.evaluation.enabled": true,<br/>"invocation.cache.ttl": 0,<br/>"invocation.few_shot.count": 0,<br/>"invocation.structured_generation.max_attempts": 5<br/>}                                                                                                                                                                                                                                       |
| `retries`                                                                                                                                                                                                                                                                                                                                                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                           | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                                              |

### Response

**[models.CreateFunctionResponse](../../models/createfunctionresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.ConflictError          | 409                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## list

List existing functions with the most recent revision in the current project

### Example Usage

<!-- UsageSnippet language="python" operationID="list_functions_functions_get" method="get" path="/functions" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.list(name="my-function", sort="name")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   | Example                                                                       |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `name`                                                                        | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | Filter functions by name                                                      | my-function                                                                   |
| `sort`                                                                        | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | Sort the functions by name or created_at, use '-' to sort in descending order | name                                                                          |
| `offset`                                                                      | *OptionalNullable[int]*                                                       | :heavy_minus_sign:                                                            | The offset of the page of functions to return when paginating                 |                                                                               |
| `limit`                                                                       | *OptionalNullable[int]*                                                       | :heavy_minus_sign:                                                            | The number of functions to return per page when paginating                    |                                                                               |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |                                                                               |

### Response

**[models.PaginatedResponseListFunctionsResponseItem](../../models/paginatedresponselistfunctionsresponseitem.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get

Get the latest revision of a function by ID

### Example Usage

<!-- UsageSnippet language="python" operationID="get_function_functions__function_id__get" method="get" path="/functions/{function_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.get(function_id="42016421-16e8-4b50-a2d1-30fc3894763b")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `function_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | The id of the function to retrieve                                  |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetFunctionResponse](../../models/getfunctionresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## update

Update a function, this will create a new revision of the function

### Example Usage

<!-- UsageSnippet language="python" operationID="update_function_functions__function_id__patch" method="patch" path="/functions/{function_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.update(function_id="b0f067f3-9aa2-4ce2-aad5-c9832fbf4fa4", name="my-function", description="This function is used to add two numbers and return the result.", instructions="You are a calculator that adds two numbers and returns the result.", input_schema={
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
    }, configuration={
        "beta.evaluation.enabled": True,
        "invocation.cache.ttl": 0,
        "invocation.few_shot.count": 0,
        "invocation.structured_generation.max_attempts": 5,
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Required                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Example                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `function_id`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | *str*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Unique identifier of the function given as a UUID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `name`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | The name of the function. Must be unique within the project and can only contain letters, numbers, underscores and hyphens.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | my-function                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `description`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Optional description of the function. This is used to describe the function to a user.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | This function is used to add two numbers and return the result.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `instructions`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | The instructions for the function, this is the prompt that will be sent to the model to complete the task. Recommended to be concise and to the point                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | You are a calculator that adds two numbers and returns the result.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `input_schema`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Dict[str, *Any*]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Optional input schema for the function. Can preferably include field descriptions to allow the model to reason about the input variables. Schema is validated against the input data and issues an error if it does not match. With the Opper SDKs you can define these schemas through libraries like Pydantic and Zod. For schemas with definitions, prefer using '$defs' and '#/$defs/...' references.                                                                                                                                                                                                                                                                                                                                                                                                                                | {<br/>"properties": {<br/>"x": {<br/>"title": "X",<br/>"type": "integer"<br/>},<br/>"y": {<br/>"title": "Y",<br/>"type": "integer"<br/>}<br/>},<br/>"required": [<br/>"x",<br/>"y"<br/>],<br/>"title": "OpperInputExample",<br/>"type": "object"<br/>}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `output_schema`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Dict[str, *Any*]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Optional output schema for the function. Can preferably include field descriptions to allow the model to reason about the output variables. Schema is validated against the output data and issues an error if it does not match. With the Opper SDKs you can define these schemas through libraries like Pydantic and Zod. For schemas with definitions, prefer using '$defs' and '#/$defs/...' references.                                                                                                                                                                                                                                                                                                                                                                                                                             | {<br/>"properties": {<br/>"sum": {<br/>"title": "Sum",<br/>"type": "integer"<br/>}<br/>},<br/>"required": [<br/>"sum"<br/>],<br/>"title": "OpperOutputExample",<br/>"type": "object"<br/>}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `model`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | [OptionalNullable[models.TModel]](../../models/tmodel.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Optionally provide a model to use for completing the task.<br/>If not provided, a default model will be used. Currently the default model is `azure/gpt-4o-eu`<br/>        <br/>To specify options for the model, use a dictionary of key-value pairs. The options are passed to the model on invocation.<br/>An example of passing temperature to `gpt-4o-mini` hosted on OpenAI is shown below.<br/>        <br/>```json<br/>{<br/>    "model": "openai/gpt-4o-mini", # the model name<br/>    "options": {<br/>        "temperature": 0.5 # the options for the model<br/>    }<br/>}<br/>```<br/><br/>To specify a fallback model, use a list of models. The models will then be tried in order.<br/>The second model will be used if the first model is not available, and so on.<br/><br/>```json<br/>[<br/>    "openai/gpt-4o-mini", # first model to try<br/>    "openai/gpt-4.1-nano", # second model to try<br/>]<br/>```<br/> |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `configuration`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Dict[str, *Any*]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Optional configuration for the function.Configuration is a dictionary of key-value pairs that can be used to override the default configuration for the function.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | {<br/>"beta.evaluation.enabled": true,<br/>"invocation.cache.ttl": 0,<br/>"invocation.few_shot.count": 0,<br/>"invocation.structured_generation.max_attempts": 5<br/>}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `retries`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

### Response

**[models.UpdateFunctionResponse](../../models/updatefunctionresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## delete

Delete a function by ID

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_function_functions__function_id__delete" method="delete" path="/functions/{function_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    opper.functions.delete(function_id="0a7a3f2e-ed2e-4c65-9f21-3d4ef7b6b17b")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `function_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | Unique identifier of the function given as a UUID                   |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_by_name

Get the latest revision of a function by name

### Example Usage

<!-- UsageSnippet language="python" operationID="get_function_by_name_functions_by_name__name__get" method="get" path="/functions/by-name/{name}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.get_by_name(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | The name of the function to retrieve                                |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetFunctionResponse](../../models/getfunctionresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_by_revision

Get a function by ID with a specific revision

### Example Usage

<!-- UsageSnippet language="python" operationID="get_function_by_revision_functions__function_id__revisions__revision_id__get" method="get" path="/functions/{function_id}/revisions/{revision_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.get_by_revision(function_id="5265325e-3604-40a9-a29d-2cc303395dab", revision_id="e60c7090-8545-4e1f-84d5-0d9e4be6c0d1")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `function_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | The id of the function to retrieve                                  |
| `revision_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | The id of the revision to retrieve                                  |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetFunctionResponse](../../models/getfunctionresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## call

Call a function

### Example Usage

<!-- UsageSnippet language="python" operationID="call_function_functions__function_id__call_post" method="post" path="/functions/{function_id}/call" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.call(function_id="864c5880-3d87-4091-828c-33cc2c7219a9", input={
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
    ], tags={
        "tag": "value",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                  | Type                                                                                       | Required                                                                                   | Description                                                                                | Example                                                                                    |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `function_id`                                                                              | *str*                                                                                      | :heavy_check_mark:                                                                         | The id of the function to call                                                             |                                                                                            |
| `input`                                                                                    | *OptionalNullable[Any]*                                                                    | :heavy_minus_sign:                                                                         | Input to the function                                                                      | {<br/>"x": 4,<br/>"y": 5<br/>}                                                             |
| `parent_span_id`                                                                           | *OptionalNullable[str]*                                                                    | :heavy_minus_sign:                                                                         | N/A                                                                                        |                                                                                            |
| `examples`                                                                                 | List[[models.ExampleIn](../../models/examplein.md)]                                        | :heavy_minus_sign:                                                                         | N/A                                                                                        | [<br/>{<br/>"comment": "Adds two numbers",<br/>"input": {<br/>"x": 1,<br/>"y": 3<br/>},<br/>"output": {<br/>"sum": 4<br/>}<br/>}<br/>] |
| `tags`                                                                                     | Dict[str, *str*]                                                                           | :heavy_minus_sign:                                                                         | Tags to add to the call event                                                              | {<br/>"tag": "value"<br/>}                                                                 |
| `retries`                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                           | :heavy_minus_sign:                                                                         | Configuration to override the default retry behavior of the client.                        |                                                                                            |

### Response

**[models.AppAPIPublicV2FunctionsCallFunctionResponse](../../models/appapipublicv2functionscallfunctionresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## stream

Stream a function call execution in real-time using Server-Sent Events (SSE).

This endpoint returns a continuous stream of Server-Sent Event objects as the function executes,
allowing for real-time streaming of responses. The response follows the Server-Sent Events
specification with proper event structure for SDK compatibility.

Each Server-Sent Event contains:
- `id`: Optional event identifier
- `event`: Optional event type
- `data`: JSON payload with streaming chunk information
- `retry`: Optional retry interval

The data payload includes:
- `delta`: Incremental text content (if any)
- `span_id`: Unique identifier for the execution span (when available)

### Example Usage

<!-- UsageSnippet language="python" operationID="stream_function_functions__function_id__call_stream_post" method="post" path="/functions/{function_id}/call/stream" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.stream(function_id="e35c595b-59f2-40b8-bc8a-d6f71ebd3c63", input={
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
    ], tags={
        "tag": "value",
    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                  | Type                                                                                       | Required                                                                                   | Description                                                                                | Example                                                                                    |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `function_id`                                                                              | *str*                                                                                      | :heavy_check_mark:                                                                         | The id of the function to call                                                             |                                                                                            |
| `input`                                                                                    | *OptionalNullable[Any]*                                                                    | :heavy_minus_sign:                                                                         | Input to the function                                                                      | {<br/>"x": 4,<br/>"y": 5<br/>}                                                             |
| `parent_span_id`                                                                           | *OptionalNullable[str]*                                                                    | :heavy_minus_sign:                                                                         | N/A                                                                                        |                                                                                            |
| `examples`                                                                                 | List[[models.ExampleIn](../../models/examplein.md)]                                        | :heavy_minus_sign:                                                                         | N/A                                                                                        | [<br/>{<br/>"comment": "Adds two numbers",<br/>"input": {<br/>"x": 1,<br/>"y": 3<br/>},<br/>"output": {<br/>"sum": 4<br/>}<br/>}<br/>] |
| `tags`                                                                                     | Dict[str, *str*]                                                                           | :heavy_minus_sign:                                                                         | Tags to add to the call event                                                              | {<br/>"tag": "value"<br/>}                                                                 |
| `retries`                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                           | :heavy_minus_sign:                                                                         | Configuration to override the default retry behavior of the client.                        |                                                                                            |

### Response

**[models.StreamFunctionFunctionsFunctionIDCallStreamPostResponse](../../models/streamfunctionfunctionsfunctionidcallstreampostresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## call_revision

Call a function

### Example Usage

<!-- UsageSnippet language="python" operationID="call_function_revision_functions__function_id__call__revision_id__post" method="post" path="/functions/{function_id}/call/{revision_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.call_revision(function_id="b7391b0d-f115-4145-ae29-a136ae2d6a7a", revision_id="de9b5cac-c926-4aa1-a5ab-dc3aa3cd539c", input={
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
    ], tags={
        "tag": "value",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                  | Type                                                                                       | Required                                                                                   | Description                                                                                | Example                                                                                    |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `function_id`                                                                              | *str*                                                                                      | :heavy_check_mark:                                                                         | The id of the function to call                                                             |                                                                                            |
| `revision_id`                                                                              | *str*                                                                                      | :heavy_check_mark:                                                                         | The id of the revision to call                                                             |                                                                                            |
| `input`                                                                                    | *OptionalNullable[Any]*                                                                    | :heavy_minus_sign:                                                                         | Input to the function                                                                      | {<br/>"x": 4,<br/>"y": 5<br/>}                                                             |
| `parent_span_id`                                                                           | *OptionalNullable[str]*                                                                    | :heavy_minus_sign:                                                                         | N/A                                                                                        |                                                                                            |
| `examples`                                                                                 | List[[models.ExampleIn](../../models/examplein.md)]                                        | :heavy_minus_sign:                                                                         | N/A                                                                                        | [<br/>{<br/>"comment": "Adds two numbers",<br/>"input": {<br/>"x": 1,<br/>"y": 3<br/>},<br/>"output": {<br/>"sum": 4<br/>}<br/>}<br/>] |
| `tags`                                                                                     | Dict[str, *str*]                                                                           | :heavy_minus_sign:                                                                         | Tags to add to the call event                                                              | {<br/>"tag": "value"<br/>}                                                                 |
| `retries`                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                           | :heavy_minus_sign:                                                                         | Configuration to override the default retry behavior of the client.                        |                                                                                            |

### Response

**[models.AppAPIPublicV2FunctionsCallFunctionResponse](../../models/appapipublicv2functionscallfunctionresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## stream_revision

Stream a function revision call execution in real-time using Server-Sent Events (SSE).

This endpoint returns a continuous stream of Server-Sent Event objects as the function executes,
allowing for real-time streaming of responses. The response follows the Server-Sent Events
specification with proper event structure for SDK compatibility.

Each Server-Sent Event contains:
- `id`: Optional event identifier
- `event`: Optional event type
- `data`: JSON payload with streaming chunk information
- `retry`: Optional retry interval

The data payload includes:
- `delta`: Incremental text content (if any)
- `span_id`: Unique identifier for the execution span (when available)

### Example Usage

<!-- UsageSnippet language="python" operationID="stream_function_revision_functions__function_id__call_stream__revision_id__post" method="post" path="/functions/{function_id}/call/stream/{revision_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.stream_revision(function_id="d69e8466-7dba-4eaf-983c-ee6573398ae7", revision_id="c5701ae3-acaf-40b6-95f8-5c1192d84640", input={
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
    ], tags={
        "tag": "value",
    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                  | Type                                                                                       | Required                                                                                   | Description                                                                                | Example                                                                                    |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `function_id`                                                                              | *str*                                                                                      | :heavy_check_mark:                                                                         | The id of the function to call                                                             |                                                                                            |
| `revision_id`                                                                              | *str*                                                                                      | :heavy_check_mark:                                                                         | The id of the revision to call                                                             |                                                                                            |
| `input`                                                                                    | *OptionalNullable[Any]*                                                                    | :heavy_minus_sign:                                                                         | Input to the function                                                                      | {<br/>"x": 4,<br/>"y": 5<br/>}                                                             |
| `parent_span_id`                                                                           | *OptionalNullable[str]*                                                                    | :heavy_minus_sign:                                                                         | N/A                                                                                        |                                                                                            |
| `examples`                                                                                 | List[[models.ExampleIn](../../models/examplein.md)]                                        | :heavy_minus_sign:                                                                         | N/A                                                                                        | [<br/>{<br/>"comment": "Adds two numbers",<br/>"input": {<br/>"x": 1,<br/>"y": 3<br/>},<br/>"output": {<br/>"sum": 4<br/>}<br/>}<br/>] |
| `tags`                                                                                     | Dict[str, *str*]                                                                           | :heavy_minus_sign:                                                                         | Tags to add to the call event                                                              | {<br/>"tag": "value"<br/>}                                                                 |
| `retries`                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                           | :heavy_minus_sign:                                                                         | Configuration to override the default retry behavior of the client.                        |                                                                                            |

### Response

**[models.StreamFunctionRevisionFunctionsFunctionIDCallStreamRevisionIDPostResponse](../../models/streamfunctionrevisionfunctionsfunctionidcallstreamrevisionidpostresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |