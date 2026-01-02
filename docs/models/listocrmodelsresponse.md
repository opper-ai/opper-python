# ListOCRModelsResponse

Response model for listing OCR models.


## Fields

| Field                              | Type                               | Required                           | Description                        | Example                            |
| ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- |
| `hosting_provider`                 | *str*                              | :heavy_check_mark:                 | The hosting provider of the model  | Mistral                            |
| `name`                             | *str*                              | :heavy_check_mark:                 | The name of the model              | mistral/ocr-latest                 |
| `location`                         | *str*                              | :heavy_check_mark:                 | The location of the model          | EU                                 |
| `cost_per_page`                    | *OptionalNullable[float]*          | :heavy_minus_sign:                 | The cost in USD per page processed | 0.001                              |