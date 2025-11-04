# RerankResponseModel

Response model for reranking.


## Fields

| Field                                                          | Type                                                           | Required                                                       | Description                                                    |
| -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| `id`                                                           | *str*                                                          | :heavy_check_mark:                                             | Unique identifier for this rerank request                      |
| `results`                                                      | List[[models.RerankResult](../models/rerankresult.md)]         | :heavy_check_mark:                                             | Ranked results                                                 |
| `model`                                                        | *str*                                                          | :heavy_check_mark:                                             | The model used for reranking                                   |
| `usage`                                                        | Dict[str, *Any*]                                               | :heavy_check_mark:                                             | Usage information                                              |
| `cost`                                                         | [OptionalNullable[models.RerankCost]](../models/rerankcost.md) | :heavy_minus_sign:                                             | Cost information for this rerank request                       |