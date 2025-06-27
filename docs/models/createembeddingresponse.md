# CreateEmbeddingResponse


## Fields

| Field                                           | Type                                            | Required                                        | Description                                     | Example                                         |
| ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- |
| `model`                                         | *str*                                           | :heavy_check_mark:                              | The model that was used to create the embedding | text-embedding-3-large                          |
| `data`                                          | List[Dict[str, *Any*]]                          | :heavy_check_mark:                              | The embedding data                              | {<br/>"embedding": [<br/>0.1,<br/>0.2,<br/>0.3<br/>],<br/>"index": 0<br/>} |
| `usage`                                         | Dict[str, *Any*]                                | :heavy_check_mark:                              | The usage information                           | {<br/>"prompt_tokens": 100,<br/>"total_tokens": 100<br/>} |