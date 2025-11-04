# LanguageModels
(*language_models*)

## Overview

### Available Operations

* [list](#list) - List Models
* [register_custom](#register_custom) - Register Custom Model
* [list_custom](#list_custom) - List Custom Models
* [get_custom](#get_custom) - Get Custom Model
* [update_custom](#update_custom) - Update Custom Model
* [delete_custom](#delete_custom) - Delete Custom Model
* [get_custom_by_name](#get_custom_by_name) - Get Custom Model By Name
* [create_alias](#create_alias) - Create Model Alias
* [list_aliases](#list_aliases) - List Model Aliases
* [get_alias](#get_alias) - Get Model Alias
* [update_alias](#update_alias) - Update Model Alias
* [delete_alias](#delete_alias) - Delete Model Alias
* [get_alias_by_name](#get_alias_by_name) - Get Model Alias By Name

## list

List all language models available in the Opper platform

For more information on the models available, see the [Opper Models](https://docs.opper.ai/capabilities/models) documentation.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_models_models_get" method="get" path="/models" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.list(offset=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `offset`                                                            | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The offset of the models to return when paginating                  |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The number of models to return per page when paginating             |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PaginatedResponseListLanguageModelsResponse](../../models/paginatedresponselistlanguagemodelsresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## register_custom

Register a custom language model with the organization that owns the API key.

### Example Usage

<!-- UsageSnippet language="python" operationID="register_custom_model_models_custom_post" method="post" path="/models/custom" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.register_custom(name="<value>", identifier="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | The name of the custom language model                               |
| `identifier`                                                        | *str*                                                               | :heavy_check_mark:                                                  | The identifier of the custom language model                         |
| `extra`                                                             | Dict[str, *Any*]                                                    | :heavy_minus_sign:                                                  | Extra metadata about the custom language model                      |
| `api_key`                                                           | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The API key of the custom language model                            |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.RegisterCustomModelResponse](../../models/registercustommodelresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.ConflictError          | 409                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## list_custom

List all custom language models for the organization that owns the API key.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_custom_models_models_custom_get" method="get" path="/models/custom" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.list_custom(offset=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `offset`                                                            | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The offset of the first model to return                             |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The maximum number of models to return                              |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PaginatedResponseListCustomModelsResponseItem](../../models/paginatedresponselistcustommodelsresponseitem.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_custom

Get a custom language model by its ID.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_custom_model_models_custom__model_id__get" method="get" path="/models/custom/{model_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.get_custom(model_id="44f75e53-0d39-45a8-9fcc-e3f8b42e974f")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `model_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The ID of the custom language model to get                          |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetCustomModelResponse](../../models/getcustommodelresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## update_custom

Update a custom language model.

### Example Usage

<!-- UsageSnippet language="python" operationID="update_custom_model_models_custom__model_id__patch" method="patch" path="/models/custom/{model_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.update_custom(model_id="df4d7ee8-7295-4163-a08e-76f64619e364")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `model_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The ID of the custom language model to update                       |
| `name`                                                              | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The name of the custom language model                               |
| `identifier`                                                        | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The identifier of the custom language model                         |
| `extra`                                                             | Dict[str, *Any*]                                                    | :heavy_minus_sign:                                                  | Extra metadata about the custom language model                      |
| `api_key`                                                           | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The API key of the custom language model                            |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.UpdateCustomModelResponse](../../models/updatecustommodelresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## delete_custom

Delete a custom language model.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_custom_model_models_custom__model_id__delete" method="delete" path="/models/custom/{model_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    opper.language_models.delete_custom(model_id="0af9c852-1b3f-48d2-a14c-f58fcb425253")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `model_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The ID of the custom language model to delete                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_custom_by_name

Get a custom language model by its name.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_custom_model_by_name_models_custom_by_name__name__get" method="get" path="/models/custom/by-name/{name}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.get_custom_by_name(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetCustomModelResponse](../../models/getcustommodelresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## create_alias

Create a model alias with fallback models for the organization that owns the API key.

A model alias allows you to define a name that resolves to an ordered list of fallback models.
For example, you could create an alias called "sonnet-4" that falls back to
["anthropic/claude-3-5-sonnet-latest", "anthropic/claude-3-5-sonnet-20241022"].

### Example Usage

<!-- UsageSnippet language="python" operationID="create_model_alias_models_aliases_post" method="post" path="/models/aliases" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.create_alias(name="<value>", fallback_models=[
        "<value 1>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | The name of the model alias                                         |
| `fallback_models`                                                   | List[*str*]                                                         | :heavy_check_mark:                                                  | Ordered list of model names to try as fallbacks                     |
| `description`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Optional description of the model alias                             |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.CreateModelAliasResponse](../../models/createmodelaliasresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.ConflictError          | 409                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## list_aliases

List all model aliases for the organization that owns the API key.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_model_aliases_models_aliases_get" method="get" path="/models/aliases" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.list_aliases(offset=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `offset`                                                            | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The offset of the first alias to return                             |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The maximum number of aliases to return                             |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PaginatedResponseListModelAliasesResponseItem](../../models/paginatedresponselistmodelaliasesresponseitem.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_alias

Get a model alias by its ID.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_model_alias_models_aliases__alias_id__get" method="get" path="/models/aliases/{alias_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.get_alias(alias_id="1fb8ddb6-7ed4-4b09-ba67-90a8c5d1692e")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `alias_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The ID of the model alias to get                                    |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetModelAliasResponse](../../models/getmodelaliasresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## update_alias

Update a model alias.

### Example Usage

<!-- UsageSnippet language="python" operationID="update_model_alias_models_aliases__alias_id__patch" method="patch" path="/models/aliases/{alias_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.update_alias(alias_id="15f4454f-0437-4e37-8149-48504d2ca755")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `alias_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The ID of the model alias to update                                 |
| `name`                                                              | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The name of the model alias                                         |
| `fallback_models`                                                   | List[*str*]                                                         | :heavy_minus_sign:                                                  | Ordered list of model names to try as fallbacks                     |
| `description`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Optional description of the model alias                             |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.UpdateModelAliasResponse](../../models/updatemodelaliasresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## delete_alias

Delete a model alias.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_model_alias_models_aliases__alias_id__delete" method="delete" path="/models/aliases/{alias_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    opper.language_models.delete_alias(alias_id="69def0be-de07-4128-ac25-11c907d9c302")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `alias_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The ID of the model alias to delete                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_alias_by_name

Get a model alias by its name.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_model_alias_by_name_models_aliases_by_name__name__get" method="get" path="/models/aliases/by-name/{name}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.language_models.get_alias_by_name(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | The name of the model alias to get                                  |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetModelAliasResponse](../../models/getmodelaliasresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |