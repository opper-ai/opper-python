# Datasets
(*datasets*)

## Overview

### Available Operations

* [create_entry](#create_entry) - Create Dataset Entry
* [list_entries](#list_entries) - List Dataset Entries
* [get_entry](#get_entry) - Get Dataset Entry
* [delete_entry](#delete_entry) - Delete Dataset Entry
* [query_entries](#query_entries) - Query Dataset Entries

## create_entry

Create Dataset Entry

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.datasets.create_entry(dataset_id="50c15d18-6e79-449b-9e59-30324da6de5f", input_={
        "x": 4,
        "y": 5,
    }, output={
        "sum": 9,
    }, expected="This `was` the output to the dataset entry", comment="This is an example of how one can edit the output")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                    | Type                                                                                         | Required                                                                                     | Description                                                                                  | Example                                                                                      |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `dataset_id`                                                                                 | *str*                                                                                        | :heavy_check_mark:                                                                           | The id of the dataset                                                                        |                                                                                              |
| `input`                                                                                      | *Any*                                                                                        | :heavy_check_mark:                                                                           | The input to the dataset entry                                                               | {<br/>"x": 4,<br/>"y": 5<br/>}                                                               |
| `output`                                                                                     | *Any*                                                                                        | :heavy_check_mark:                                                                           | The output to the dataset entry                                                              | {<br/>"sum": 9<br/>}                                                                         |
| `expected`                                                                                   | *OptionalNullable[Any]*                                                                      | :heavy_minus_sign:                                                                           | The expected output to the dataset entry, this is an optionally edited version of the output | This `was` the output to the dataset entry                                                   |
| `comment`                                                                                    | *OptionalNullable[str]*                                                                      | :heavy_minus_sign:                                                                           | The comment to the dataset entry                                                             | This is an example of how one can edit the output                                            |
| `retries`                                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                             | :heavy_minus_sign:                                                                           | Configuration to override the default retry behavior of the client.                          |                                                                                              |

### Response

**[models.CreateDatasetEntryResponse](../../models/createdatasetentryresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## list_entries

List Dataset Entries

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.datasets.list_entries(dataset_id="984b502b-adc1-4c0f-a69a-4733598fbb25", offset=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | The id of the dataset                                               |
| `offset`                                                            | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The offset of the entries to get                                    |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The limit of the entries to get                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PaginatedResponseGetDatasetEntriesResponse](../../models/paginatedresponsegetdatasetentriesresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_entry

Get Dataset Entry

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.datasets.get_entry(dataset_id="9e9ec381-de20-405d-80e0-5a53e2facfd9", entry_id="fdfd96d0-b56a-45dd-9a48-a4225b217177")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | The id of the dataset                                               |
| `entry_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The id of the entry to get                                          |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetDatasetEntryResponse](../../models/getdatasetentryresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## delete_entry

Delete Dataset Entry

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    opper.datasets.delete_entry(dataset_id="28392d52-9541-4ea9-93f0-596438b9d0c1", entry_id="de374b46-6700-466c-9f46-64f32a3b0c80")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | The id of the dataset                                               |
| `entry_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The id of the entry to delete                                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## query_entries

Query Dataset Entries

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.datasets.query_entries(dataset_id="67f85e63-b416-44da-aab0-fea4bb316c72", query="<value>", limit=5)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `dataset_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | The id of the dataset                                               |
| `query`                                                             | *str*                                                               | :heavy_check_mark:                                                  | The query to search for                                             |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The limit of the entries to get                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.QueryDatasetEntriesResponse]](../../models/.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |