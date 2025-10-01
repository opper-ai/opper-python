# UpdateModelAliasRequest


## Fields

| Field                                           | Type                                            | Required                                        | Description                                     |
| ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- |
| `name`                                          | *OptionalNullable[str]*                         | :heavy_minus_sign:                              | The name of the model alias                     |
| `fallback_models`                               | List[*str*]                                     | :heavy_minus_sign:                              | Ordered list of model names to try as fallbacks |
| `description`                                   | *OptionalNullable[str]*                         | :heavy_minus_sign:                              | Optional description of the model alias         |