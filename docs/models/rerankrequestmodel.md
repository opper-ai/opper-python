# RerankRequestModel

Request model for reranking.


## Fields

| Field                                                         | Type                                                          | Required                                                      | Description                                                   |
| ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| `query`                                                       | *str*                                                         | :heavy_check_mark:                                            | The search query to rank documents against                    |
| `documents`                                                   | List[[models.RerankDocument](../models/rerankdocument.md)]    | :heavy_check_mark:                                            | List of documents to rerank                                   |
| `model`                                                       | *str*                                                         | :heavy_check_mark:                                            | The reranking model to use                                    |
| `top_k`                                                       | *OptionalNullable[int]*                                       | :heavy_minus_sign:                                            | Number of top documents to return. Defaults to all documents. |
| `return_documents`                                            | *Optional[bool]*                                              | :heavy_minus_sign:                                            | Whether to return document content in the response            |
| `max_chunks_per_doc`                                          | *OptionalNullable[int]*                                       | :heavy_minus_sign:                                            | Maximum number of chunks per document                         |