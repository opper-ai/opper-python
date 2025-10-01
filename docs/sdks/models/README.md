# Models
(*models*)

## Overview

### Available Operations

* [create_model_alias_models_aliases_post](#create_model_alias_models_aliases_post) - Create Model Alias
* [list_model_aliases_models_aliases_get](#list_model_aliases_models_aliases_get) - List Model Aliases
* [get_model_alias_models_aliases_alias_id_get](#get_model_alias_models_aliases_alias_id_get) - Get Model Alias
* [update_model_alias_models_aliases_alias_id_patch](#update_model_alias_models_aliases_alias_id_patch) - Update Model Alias
* [delete_model_alias_models_aliases_alias_id_delete](#delete_model_alias_models_aliases_alias_id_delete) - Delete Model Alias
* [get_model_alias_by_name_models_aliases_by_name_name_get](#get_model_alias_by_name_models_aliases_by_name_name_get) - Get Model Alias By Name

## create_model_alias_models_aliases_post

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

    res = opper.models.create_model_alias_models_aliases_post(name="<value>", fallback_models=[
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

## list_model_aliases_models_aliases_get

List all model aliases for the organization that owns the API key.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_model_aliases_models_aliases_get" method="get" path="/models/aliases" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.models.list_model_aliases_models_aliases_get(offset=0, limit=100)

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

## get_model_alias_models_aliases_alias_id_get

Get a model alias by its ID.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_model_alias_models_aliases__alias_id__get" method="get" path="/models/aliases/{alias_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.models.get_model_alias_models_aliases_alias_id_get(alias_id="1fb8ddb6-7ed4-4b09-ba67-90a8c5d1692e")

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

## update_model_alias_models_aliases_alias_id_patch

Update a model alias.

### Example Usage

<!-- UsageSnippet language="python" operationID="update_model_alias_models_aliases__alias_id__patch" method="patch" path="/models/aliases/{alias_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.models.update_model_alias_models_aliases_alias_id_patch(alias_id="15f4454f-0437-4e37-8149-48504d2ca755")

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

## delete_model_alias_models_aliases_alias_id_delete

Delete a model alias.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_model_alias_models_aliases__alias_id__delete" method="delete" path="/models/aliases/{alias_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    opper.models.delete_model_alias_models_aliases_alias_id_delete(alias_id="69def0be-de07-4128-ac25-11c907d9c302")

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

## get_model_alias_by_name_models_aliases_by_name_name_get

Get a model alias by its name.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_model_alias_by_name_models_aliases_by_name__name__get" method="get" path="/models/aliases/by-name/{name}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.models.get_model_alias_by_name_models_aliases_by_name_name_get(name="<value>")

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