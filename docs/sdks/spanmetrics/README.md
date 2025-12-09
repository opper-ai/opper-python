# SpanMetrics

## Overview

### Available Operations

* [create_metric](#create_metric) - Create Metric
* [list](#list) - List Metrics
* [get](#get) - Get Metric
* [update_metric](#update_metric) - Update Metric
* [delete](#delete) - Delete Metric

## create_metric

Create a new metric for a span

### Example Usage

<!-- UsageSnippet language="python" operationID="create_metric_spans__span_id__metrics_post" method="post" path="/spans/{span_id}/metrics" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.span_metrics.create_metric(span_id="e2dedc7f-a1a2-4eb9-990c-c81f34373ed2", dimension="<value>", value=6022.87)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `span_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | The id of the span                                                  |
| `dimension`                                                         | *str*                                                               | :heavy_check_mark:                                                  | The dimension of the metric                                         |
| `value`                                                             | *float*                                                             | :heavy_check_mark:                                                  | The value of the metric                                             |
| `comment`                                                           | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | A comment about the metric, e.g. a description of the metric        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.CreateSpanMetricResponse](../../models/createspanmetricresponse.md)**

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

List metrics for a span

### Example Usage

<!-- UsageSnippet language="python" operationID="list_metrics_spans__span_id__metrics_get" method="get" path="/spans/{span_id}/metrics" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.span_metrics.list(span_id="65689346-76c0-45f7-a40b-63556c71b1c7", offset=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `span_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | The id of the span to list metrics for                              |
| `offset`                                                            | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The offset to start the list from                                   |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The number of metrics to return                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PaginatedResponseListSpanMetricsResponse](../../models/paginatedresponselistspanmetricsresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get

Get a metric for a span

### Example Usage

<!-- UsageSnippet language="python" operationID="get_metric_spans__span_id__metrics__metric_id__get" method="get" path="/spans/{span_id}/metrics/{metric_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.span_metrics.get(span_id="79eccc0e-04d4-4c88-9b48-e9c1fba622be", metric_id="f6486ef2-ef7b-4221-8f8f-e12202849ee1")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `span_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | The id of the span                                                  |
| `metric_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | The id of the metric to get                                         |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetSpanMetricResponse](../../models/getspanmetricresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## update_metric

Update a metric for a span

### Example Usage

<!-- UsageSnippet language="python" operationID="update_metric_spans__span_id__metrics__metric_id__patch" method="patch" path="/spans/{span_id}/metrics/{metric_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.span_metrics.update_metric(span_id="a6608e7f-16ba-44c7-944b-d024a416ad8b", metric_id="e5a732b2-6b58-43f9-ab70-e75a98267516")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `span_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | The id of the span                                                  |
| `metric_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | The id of the metric to update                                      |
| `dimension`                                                         | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The dimension of the metric                                         |
| `value`                                                             | *OptionalNullable[float]*                                           | :heavy_minus_sign:                                                  | The value of the metric                                             |
| `comment`                                                           | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | A comment about the metric, e.g. a description of the metric        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.UpdateSpanMetricResponse](../../models/updatespanmetricresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## delete

Delete a metric for a span

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_metric_spans__span_id__metrics__metric_id__delete" method="delete" path="/spans/{span_id}/metrics/{metric_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    opper.span_metrics.delete(span_id="ad9bed87-edf2-4286-9e82-4fe46d9550e2", metric_id="418572fc-adf1-4a8d-82f0-3ec1e7d7d2cb")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `span_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `metric_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |