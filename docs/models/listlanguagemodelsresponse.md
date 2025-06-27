# ListLanguageModelsResponse


## Fields

| Field                                | Type                                 | Required                             | Description                          | Example                              |
| ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ |
| `hosting_provider`                   | *str*                                | :heavy_check_mark:                   | The hosting provider of the model    | azure                                |
| `name`                               | *str*                                | :heavy_check_mark:                   | The name of the model                | azure/gpt-4o-eu                      |
| `location`                           | *str*                                | :heavy_check_mark:                   | The location of the model            | us                                   |
| `input_cost_per_token`               | *OptionalNullable[float]*            | :heavy_minus_sign:                   | The cost in USD per token for input  | 0.00015                              |
| `output_cost_per_token`              | *OptionalNullable[float]*            | :heavy_minus_sign:                   | The cost in USD per token for output | 0.0006                               |