# GetUsageResultItem


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `time_bucket`                                                        | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | The start time of the time bucket                                    |
| `cost`                                                               | *str*                                                                | :heavy_check_mark:                                                   | The cost in USD for the time bucket                                  |
| `__pydantic_extra__`                                                 | Dict[str, *Any*]                                                     | :heavy_minus_sign:                                                   | N/A                                                                  |