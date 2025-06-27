# Analytics
(*analytics*)

## Overview

### Available Operations

* [get_usage](#get_usage) - Usage

## get_usage

Usage

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.analytics.get_usage(fields=[
        "completion_tokens",
        "total_tokens",
    ], group_by=[
        "model",
        "project.name",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                   | Type                                                                                                        | Required                                                                                                    | Description                                                                                                 | Example                                                                                                     |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `from_date`                                                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                        | :heavy_minus_sign:                                                                                          | Start date for the time range (inclusive). If not provided, defaults to the first day of the current month. |                                                                                                             |
| `to_date`                                                                                                   | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                        | :heavy_minus_sign:                                                                                          | End date for the time range (exclusive). If not provided, defaults to the last day of the current month.    |                                                                                                             |
| `granularity`                                                                                               | [OptionalNullable[models.Granularity]](../../models/granularity.md)                                         | :heavy_minus_sign:                                                                                          | Time granularity for grouping (minute, hour, day, month, year)                                              |                                                                                                             |
| `fields`                                                                                                    | List[*str*]                                                                                                 | :heavy_minus_sign:                                                                                          | Fields from event_metadata to include and sum                                                               | [<br/>"completion_tokens",<br/>"total_tokens"<br/>]                                                         |
| `group_by`                                                                                                  | List[*str*]                                                                                                 | :heavy_minus_sign:                                                                                          | Fields from tags to group by                                                                                | [<br/>"model",<br/>"project.name"<br/>]                                                                     |
| `retries`                                                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                            | :heavy_minus_sign:                                                                                          | Configuration to override the default retry behavior of the client.                                         |                                                                                                             |

### Response

**[List[models.GetUsageResultItem]](../../models/.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |