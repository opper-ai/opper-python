# RerankResult

A single reranking result.


## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `index`                                                                | *int*                                                                  | :heavy_check_mark:                                                     | Original index of the document                                         |
| `relevance_score`                                                      | *float*                                                                | :heavy_check_mark:                                                     | Relevance score between 0 and 1                                        |
| `document`                                                             | [OptionalNullable[models.RerankDocument]](../models/rerankdocument.md) | :heavy_minus_sign:                                                     | The document content (if return_documents=True)                        |