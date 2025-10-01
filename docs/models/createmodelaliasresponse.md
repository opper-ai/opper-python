# CreateModelAliasResponse


## Fields

| Field                                           | Type                                            | Required                                        | Description                                     |
| ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- |
| `id`                                            | *str*                                           | :heavy_check_mark:                              | The ID of the model alias                       |
| `name`                                          | *str*                                           | :heavy_check_mark:                              | The name of the model alias                     |
| `fallback_models`                               | List[*str*]                                     | :heavy_check_mark:                              | Ordered list of model names to try as fallbacks |
| `description`                                   | *OptionalNullable[str]*                         | :heavy_minus_sign:                              | Optional description of the model alias         |