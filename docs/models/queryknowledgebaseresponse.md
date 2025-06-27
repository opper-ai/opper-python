# QueryKnowledgeBaseResponse


## Fields

| Field                                   | Type                                    | Required                                | Description                             | Example                                 |
| --------------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- |
| `id`                                    | *str*                                   | :heavy_check_mark:                      | The id of the document                  |                                         |
| `key`                                   | *str*                                   | :heavy_check_mark:                      | The key of the document                 | paris_123                               |
| `content`                               | *str*                                   | :heavy_check_mark:                      | The content of the document             | The capital of France is Paris          |
| `metadata`                              | Dict[str, *Any*]                        | :heavy_check_mark:                      | The metadata of the document            | {<br/>"category": "product",<br/>"price": 100<br/>} |
| `score`                                 | *float*                                 | :heavy_check_mark:                      | The score of the document               | 0.95                                    |