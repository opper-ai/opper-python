# ListRerankModelsResponse

Response model for listing rerank models.


## Fields

| Field                              | Type                               | Required                           | Description                        | Example                            |
| ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- |
| `hosting_provider`                 | *str*                              | :heavy_check_mark:                 | The hosting provider of the model  | Cohere                             |
| `name`                             | *str*                              | :heavy_check_mark:                 | The name of the model              | rerank-v3.5                        |
| `location`                         | *str*                              | :heavy_check_mark:                 | The location of the model          | US                                 |
| `cost_per_request`                 | *OptionalNullable[float]*          | :heavy_minus_sign:                 | The cost in USD per rerank request | 0.002                              |