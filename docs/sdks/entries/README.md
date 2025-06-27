# Entries
(*datasets.entries*)

## Overview

### Available Operations

* [update](#update) - Update Dataset Entry

## update

Update Dataset Entry

### Example Usage

```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.datasets.entries.update(dataset_id="df57581c-3364-4ee6-a9f8-7de20cb937ff", entry_id="2789b25b-1a98-4360-96ee-67e9af98c53f", input_="Given this input, what is the output?", output="This is the output to the dataset entry", expected="This `was` the output to the dataset entry", comment="This is an example of how one can edit the output")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                    | Type                                                                                         | Required                                                                                     | Description                                                                                  | Example                                                                                      |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `dataset_id`                                                                                 | *str*                                                                                        | :heavy_check_mark:                                                                           | The id of the dataset                                                                        |                                                                                              |
| `entry_id`                                                                                   | *str*                                                                                        | :heavy_check_mark:                                                                           | The id of the entry to update                                                                |                                                                                              |
| `input`                                                                                      | *OptionalNullable[Any]*                                                                      | :heavy_minus_sign:                                                                           | The input to the dataset entry                                                               | Given this input, what is the output?                                                        |
| `output`                                                                                     | *OptionalNullable[Any]*                                                                      | :heavy_minus_sign:                                                                           | The output to the dataset entry                                                              | This is the output to the dataset entry                                                      |
| `expected`                                                                                   | *OptionalNullable[Any]*                                                                      | :heavy_minus_sign:                                                                           | The expected output to the dataset entry, this is an optionally edited version of the output | This `was` the output to the dataset entry                                                   |
| `comment`                                                                                    | *OptionalNullable[str]*                                                                      | :heavy_minus_sign:                                                                           | The comment to the dataset entry                                                             | This is an example of how one can edit the output                                            |
| `retries`                                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                             | :heavy_minus_sign:                                                                           | Configuration to override the default retry behavior of the client.                          |                                                                                              |

### Response

**[models.UpdateDatasetEntryResponse](../../models/updatedatasetentryresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |