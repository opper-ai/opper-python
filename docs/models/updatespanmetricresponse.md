# UpdateSpanMetricResponse


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `dimension`                                                          | *str*                                                                | :heavy_check_mark:                                                   | The dimension of the metric                                          |
| `value`                                                              | *float*                                                              | :heavy_check_mark:                                                   | The value of the metric                                              |
| `comment`                                                            | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | A comment about the metric, e.g. a description of the metric         |
| `id`                                                                 | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `span_id`                                                            | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `created_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | N/A                                                                  |