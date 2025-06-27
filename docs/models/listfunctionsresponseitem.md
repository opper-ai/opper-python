# ListFunctionsResponseItem


## Fields

| Field                                                  | Type                                                   | Required                                               | Description                                            | Example                                                |
| ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ |
| `id`                                                   | *str*                                                  | :heavy_check_mark:                                     | The ID of the function                                 |                                                        |
| `name`                                                 | *str*                                                  | :heavy_check_mark:                                     | The name of the function                               | my-function                                            |
| `description`                                          | *OptionalNullable[str]*                                | :heavy_minus_sign:                                     | The description of the function                        |                                                        |
| `instructions`                                         | *OptionalNullable[str]*                                | :heavy_minus_sign:                                     | The instructions of the function                       |                                                        |
| `model`                                                | [OptionalNullable[models.TModel]](../models/tmodel.md) | :heavy_minus_sign:                                     | The model of the function                              |                                                        |
| `revision_id`                                          | *str*                                                  | :heavy_check_mark:                                     | The ID of the latest revision of the function          |                                                        |