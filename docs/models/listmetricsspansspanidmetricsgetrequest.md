# ListMetricsSpansSpanIDMetricsGetRequest


## Fields

| Field                                  | Type                                   | Required                               | Description                            |
| -------------------------------------- | -------------------------------------- | -------------------------------------- | -------------------------------------- |
| `span_id`                              | *str*                                  | :heavy_check_mark:                     | The id of the span to list metrics for |
| `offset`                               | *Optional[int]*                        | :heavy_minus_sign:                     | The offset to start the list from      |
| `limit`                                | *Optional[int]*                        | :heavy_minus_sign:                     | The number of metrics to return        |