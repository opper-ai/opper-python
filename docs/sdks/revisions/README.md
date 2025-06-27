# Revisions
(*functions.revisions*)

## Overview

### Available Operations

* [list](#list) - List Function Revisions

## list

Get all revisions for a function with pagination

Returns a list of revisions for the function with the given function id
revisions are sorted by created_at in descending order ergo the latest revision is the first one

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.functions.revisions.list(function_id="197f3203-7e7e-453d-b36a-b1f4e551ebf4")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `function_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | The id of the function to get revisions for                         |
| `offset`                                                            | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | The offset of the revisions to get                                  |
| `limit`                                                             | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | The limit of the revisions to get                                   |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PaginatedResponseListFunctionRevisionResponse](../../models/paginatedresponselistfunctionrevisionresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |