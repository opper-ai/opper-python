# Spans
(*spans*)

## Overview

### Available Operations

* [create](#create) - Create Span
* [get](#get) - Get Span
* [update](#update) - Update Span
* [delete](#delete) - Delete Span
* [save_examples](#save_examples) - Save To Dataset

## create

Create a new span

### Example Usage

```python
from opperai import Opper
from opperai.utils import parse_datetime
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.spans.create(name="my span", start_time=parse_datetime("2024-03-20T10:00:00+00:00"), id="123e4567-e89b-12d3-a456-426614174000", trace_id="123e4567-e89b-12d3-a456-426614174000", parent_id="123e4567-e89b-12d3-a456-426614174000", type="email_tool", end_time=parse_datetime("2024-03-20T10:00:10+00:00"), input="Hello, world!", output="Hello, world!", error="Exception: This is an error message", meta={
        "key": "value",
    }, score=10)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                 | Type                                                                                                      | Required                                                                                                  | Description                                                                                               | Example                                                                                                   |
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `name`                                                                                                    | *str*                                                                                                     | :heavy_check_mark:                                                                                        | The name of the span, something descriptive about the span that will be used to identify it when querying | my span                                                                                                   |
| `start_time`                                                                                              | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                      | :heavy_minus_sign:                                                                                        | The start time of the span in UTC                                                                         | 2024-03-20T10:00:00+00:00                                                                                 |
| `id`                                                                                                      | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | The id of the span                                                                                        | 123e4567-e89b-12d3-a456-426614174000                                                                      |
| `trace_id`                                                                                                | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | The id of the trace                                                                                       | 123e4567-e89b-12d3-a456-426614174000                                                                      |
| `parent_id`                                                                                               | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | The id of the parent span                                                                                 | 123e4567-e89b-12d3-a456-426614174000                                                                      |
| `type`                                                                                                    | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | The type of the span                                                                                      | email_tool                                                                                                |
| `end_time`                                                                                                | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                      | :heavy_minus_sign:                                                                                        | The end time of the span in UTC                                                                           | 2024-03-20T10:00:10+00:00                                                                                 |
| `input`                                                                                                   | *OptionalNullable[Any]*                                                                                   | :heavy_minus_sign:                                                                                        | The input of the span                                                                                     | Hello, world!                                                                                             |
| `output`                                                                                                  | *OptionalNullable[Any]*                                                                                   | :heavy_minus_sign:                                                                                        | The output of the span                                                                                    | Hello, world!                                                                                             |
| `error`                                                                                                   | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | In case of an error, the error message                                                                    | Exception: This is an error message                                                                       |
| `meta`                                                                                                    | Dict[str, *Any*]                                                                                          | :heavy_minus_sign:                                                                                        | The metadata of the span                                                                                  | {<br/>"key": "value"<br/>}                                                                                |
| `score`                                                                                                   | *OptionalNullable[int]*                                                                                   | :heavy_minus_sign:                                                                                        | The score of the span                                                                                     | 10                                                                                                        |
| `retries`                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                          | :heavy_minus_sign:                                                                                        | Configuration to override the default retry behavior of the client.                                       |                                                                                                           |

### Response

**[models.CreateSpanResponse](../../models/createspanresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get

Get a span

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.spans.get(span_id="d4a69fe8-e8c8-444b-baeb-0f1eec05cc0b")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `span_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | The ID of the span to get                                           |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetSpanResponse](../../models/getspanresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## update

Update a span

### Example Usage

```python
from opperai import Opper
from opperai.utils import parse_datetime
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.spans.update(span_id="77b258a2-45c1-4b87-a50c-9116bc8ed1d6", name="my span", start_time=parse_datetime("2025-06-28T09:49:07.980658Z"), type="email_tool", end_time=parse_datetime("2025-06-28T09:49:07.980752Z"), input="Hello, world!", output="Hello, world!", error="Exception: This is an error message", meta={
        "key": "value",
    }, score=10)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                 | Type                                                                                                      | Required                                                                                                  | Description                                                                                               | Example                                                                                                   |
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `span_id`                                                                                                 | *str*                                                                                                     | :heavy_check_mark:                                                                                        | The ID of the span to update                                                                              |                                                                                                           |
| `name`                                                                                                    | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | The name of the span, something descriptive about the span that will be used to identify it when querying | my span                                                                                                   |
| `start_time`                                                                                              | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                      | :heavy_minus_sign:                                                                                        | The start time of the span in UTC                                                                         | 2025-06-28T09:49:07.980658Z                                                                               |
| `type`                                                                                                    | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | The type of the span                                                                                      | email_tool                                                                                                |
| `end_time`                                                                                                | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                      | :heavy_minus_sign:                                                                                        | The end time of the span in UTC                                                                           | 2025-06-28T09:49:07.980752Z                                                                               |
| `input`                                                                                                   | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | The input of the span                                                                                     | Hello, world!                                                                                             |
| `output`                                                                                                  | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | The output of the span                                                                                    | Hello, world!                                                                                             |
| `error`                                                                                                   | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | In case of an error, the error message                                                                    | Exception: This is an error message                                                                       |
| `meta`                                                                                                    | Dict[str, *Any*]                                                                                          | :heavy_minus_sign:                                                                                        | The meta data of the span                                                                                 | {<br/>"key": "value"<br/>}                                                                                |
| `score`                                                                                                   | *OptionalNullable[int]*                                                                                   | :heavy_minus_sign:                                                                                        | The score of the span                                                                                     | 10                                                                                                        |
| `retries`                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                          | :heavy_minus_sign:                                                                                        | Configuration to override the default retry behavior of the client.                                       |                                                                                                           |

### Response

**[models.UpdateSpanResponse](../../models/updatespanresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## delete

Delete a span by its id

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    opper.spans.delete(span_id="b18ef9c6-59d8-4040-afd8-0f7b26a5c501")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `span_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | The ID of the span to delete                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## save_examples

Save all generation spans to the dataset

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.spans.save_examples(span_id="347e319f-1453-4279-879f-b88d591d5dd3")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `span_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SaveToDatasetResponse](../../models/savetodatasetresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |