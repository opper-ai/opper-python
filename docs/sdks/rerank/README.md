# Rerank

## Overview

### Available Operations

* [documents](#documents) - Rerank Documents
* [list_models](#list_models) - List Rerank Models

## documents

Rerank documents based on relevance to a query.

This endpoint allows you to rerank a list of documents based on their relevance
to a given query using state-of-the-art reranking models.

The documents will be returned in order of relevance, with the most relevant
documents first. Each result includes the original document index and a
relevance score.

### Example Usage

<!-- UsageSnippet language="python" operationID="rerank_documents_rerank_post" method="post" path="/rerank" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.rerank.documents(query="<value>", documents=[
        {
            "text": "<value>",
        },
    ], model="Mustang", return_documents=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `query`                                                             | *str*                                                               | :heavy_check_mark:                                                  | The search query to rank documents against                          |
| `documents`                                                         | List[[models.RerankDocument](../../models/rerankdocument.md)]       | :heavy_check_mark:                                                  | List of documents to rerank                                         |
| `model`                                                             | *str*                                                               | :heavy_check_mark:                                                  | The reranking model to use                                          |
| `top_k`                                                             | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | Number of top documents to return. Defaults to all documents.       |
| `return_documents`                                                  | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to return document content in the response                  |
| `max_chunks_per_doc`                                                | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | Maximum number of chunks per document                               |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.RerankResponseModel](../../models/rerankresponsemodel.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## list_models

List all available reranking models.

Returns a list of all reranking models available on the Opper platform,
including their hosting providers, locations, and pricing information.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_rerank_models_rerank_models_get" method="get" path="/rerank/models" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.rerank.list_models()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PaginatedResponseListRerankModelsResponse](../../models/paginatedresponselistrerankmodelsresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |