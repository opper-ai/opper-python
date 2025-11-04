# RerankCost

Cost information for reranking.


## Fields

| Field                                               | Type                                                | Required                                            | Description                                         |
| --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- |
| `generation`                                        | *float*                                             | :heavy_check_mark:                                  | Cost of the reranking request in USD                |
| `platform`                                          | *float*                                             | :heavy_check_mark:                                  | Platform fee in USD (percentage of generation cost) |
| `total`                                             | *float*                                             | :heavy_check_mark:                                  | Total cost in USD (generation + platform)           |