# Knowledge
(*knowledge*)

## Overview

### Available Operations

* [create](#create) - Create Knowledge Base
* [list](#list) - List Knowledge Bases
* [get](#get) - Get Knowledge Base
* [delete](#delete) - Delete Knowledge Base
* [get_by_name](#get_by_name) - Get Knowledge Base By Name
* [get_upload_url](#get_upload_url) - Get Upload Url
* [register_file_upload](#register_file_upload) - Register File Upload
* [delete_file](#delete_file) - Delete File From Knowledge Base
* [get_file_download_url](#get_file_download_url) - Get File Download Url
* [list_files](#list_files) - List Files
* [query](#query) - Query Knowledge Base
* [delete_documents](#delete_documents) - Delete Documents
* [add](#add) - Add

## create

Create a knowledge base

### Example Usage

<!-- UsageSnippet language="python" operationID="create_knowledge_base_knowledge_post" method="post" path="/knowledge" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.create(name="<value>", embedding_model="azure/text-embedding-3-large")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |                                                                     |
| `embedding_model`                                                   | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | The embedding model to use for the knowledge base                   | azure/text-embedding-3-large                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.CreateKnowledgeBaseResponse](../../models/createknowledgebaseresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## list

List all knowledge bases for the current project

### Example Usage

<!-- UsageSnippet language="python" operationID="list_knowledge_bases_knowledge_get" method="get" path="/knowledge" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.list(offset=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `offset`                                                            | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The offset to start the list from                                   |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The number of knowledge bases to return                             |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PaginatedResponseListKnowledgeBasesResponse](../../models/paginatedresponselistknowledgebasesresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get

Get a knowledge base by its id

### Example Usage

<!-- UsageSnippet language="python" operationID="get_knowledge_base_knowledge__knowledge_base_id__get" method="get" path="/knowledge/{knowledge_base_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.get(knowledge_base_id="be4b1ab3-e801-401e-ac5f-bf91dbf857c6")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `knowledge_base_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | The id of the knowledge base to get                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetKnowledgeBaseResponse](../../models/getknowledgebaseresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## delete

Delete a knowledge base

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_knowledge_base_knowledge__knowledge_base_id__delete" method="delete" path="/knowledge/{knowledge_base_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    opper.knowledge.delete(knowledge_base_id="2964306e-df22-4249-9106-5bd153bbbf99")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `knowledge_base_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | The id of the knowledge base to delete or delete documents from     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_by_name

Get a knowledge base by its name

### Example Usage

<!-- UsageSnippet language="python" operationID="get_knowledge_base_by_name_knowledge_by_name__knowledge_base_name__get" method="get" path="/knowledge/by-name/{knowledge_base_name}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.get_by_name(knowledge_base_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `knowledge_base_name`                                               | *str*                                                               | :heavy_check_mark:                                                  | The name of the knowledge base to get                               |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetKnowledgeBaseResponse](../../models/getknowledgebaseresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_upload_url

Get upload URL for a knowledge base by its id

Uploading files is a three step process:
1. Get upload URL (GET /v2/knowledge/{knowledge_base_id}/upload_url)
2. Upload file to the URL
3. Register file (POST /v2/knowledge/{knowledge_base_id}/register_file)

### Example Usage

<!-- UsageSnippet language="python" operationID="get_upload_url_knowledge__knowledge_base_id__upload_url_get" method="get" path="/knowledge/{knowledge_base_id}/upload_url" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.get_upload_url(knowledge_base_id="70e60583-3f45-4ab8-9a7f-cce7ab08546e", filename="example.pdf")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `knowledge_base_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | The id of the knowledge base to get the upload URL for              |                                                                     |
| `filename`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The filename of the file to upload                                  | example.pdf                                                         |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.GetUploadURLResponse](../../models/getuploadurlresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## register_file_upload

Register a file upload for a knowledge base by its id

Registering a file upload is a three step process:
1. Get upload URL (GET /v2/knowledge/{knowledge_base_id}/upload_url)
2. Upload file to the URL
3. Register file (POST /v2/knowledge/{knowledge_base_id}/register_file)

### Example Usage

<!-- UsageSnippet language="python" operationID="register_file_upload_knowledge__knowledge_base_id__register_file_post" method="post" path="/knowledge/{knowledge_base_id}/register_file" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.register_file_upload(knowledge_base_id="3c6931ec-d324-46b6-bec6-bf31a5f0623f", filename="example.pdf", file_id="0dff5851-c155-4a46-8450-5b96eb017ae5", content_type="application/pdf", metadata={
        "category": "legal",
        "client": "acme",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                           | Type                                                                                                | Required                                                                                            | Description                                                                                         | Example                                                                                             |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `knowledge_base_id`                                                                                 | *str*                                                                                               | :heavy_check_mark:                                                                                  | The id of the knowledge base to register the file for                                               |                                                                                                     |
| `filename`                                                                                          | *str*                                                                                               | :heavy_check_mark:                                                                                  | The filename of the file to register                                                                | example.pdf                                                                                         |
| `file_id`                                                                                           | *str*                                                                                               | :heavy_check_mark:                                                                                  | The id of the file to register                                                                      |                                                                                                     |
| `content_type`                                                                                      | *str*                                                                                               | :heavy_check_mark:                                                                                  | The content type of the file to register                                                            | application/pdf                                                                                     |
| `configuration`                                                                                     | [OptionalNullable[models.TextProcessingConfiguration]](../../models/textprocessingconfiguration.md) | :heavy_minus_sign:                                                                                  | The configuration for the file to register                                                          |                                                                                                     |
| `metadata`                                                                                          | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | Optional metadata to attach to the file                                                             | {<br/>"category": "legal",<br/>"client": "acme"<br/>}                                               |
| `retries`                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                    | :heavy_minus_sign:                                                                                  | Configuration to override the default retry behavior of the client.                                 |                                                                                                     |

### Response

**[models.RegisterFileUploadResponse](../../models/registerfileuploadresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## delete_file

Delete a file from a knowledge base by its id

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_file_from_knowledge_base_knowledge__knowledge_base_id__files__file_id__delete" method="delete" path="/knowledge/{knowledge_base_id}/files/{file_id}" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    opper.knowledge.delete_file(knowledge_base_id="17be92df-8b1d-4801-96cf-02fc837c4214", file_id="0ceef03f-4e06-464c-b5e7-be55bcc94e9f")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `knowledge_base_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | The id of the knowledge base                                        |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | The id of the file to delete                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## get_file_download_url

Get a presigned URL to download a file from a knowledge base

### Example Usage

<!-- UsageSnippet language="python" operationID="get_file_download_url_knowledge__knowledge_base_id__files__file_id__download_url_get" method="get" path="/knowledge/{knowledge_base_id}/files/{file_id}/download_url" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.get_file_download_url(knowledge_base_id="3d6f9cb0-cbf2-4c9a-8995-331034439b8d", file_id="d917ff5b-acf0-4e5c-943a-7d584204a9f3")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `knowledge_base_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | The id of the knowledge base                                        |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | The id of the file                                                  |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.FileDownloadURLResponse](../../models/filedownloadurlresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## list_files

List all files in a knowledge base

### Example Usage

<!-- UsageSnippet language="python" operationID="list_files_knowledge__knowledge_base_id__files_get" method="get" path="/knowledge/{knowledge_base_id}/files" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.list_files(knowledge_base_id="53b2ef93-22ff-4826-aac5-a53c7fa8e075", offset=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `knowledge_base_id`                                                 | *str*                                                               | :heavy_check_mark:                                                  | The id of the knowledge base to list files from                     |
| `offset`                                                            | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The offset to start the list from                                   |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | The number of files to return                                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PaginatedResponseListFilesResponse](../../models/paginatedresponselistfilesresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## query

Query a knowledge base by its id

### Example Usage

<!-- UsageSnippet language="python" operationID="query_knowledge_base_knowledge__knowledge_base_id__query_post" method="post" path="/knowledge/{knowledge_base_id}/query" -->
```python
from opperai import Opper, models
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.query(knowledge_base_id="1944d10d-ea53-4b17-ad7e-d92d98c8620e", query="What is the capital of France?", prefilter_limit=10, top_k=3, filters=[
        {
            "field": "price",
            "operation": models.Op.GREATER_THAN_,
            "value": 100,
        },
        {
            "field": "category",
            "operation": models.Op.IN,
            "value": [
                "product",
                "service",
            ],
        },
    ], rerank=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                    | Type                                                                                                                                         | Required                                                                                                                                     | Description                                                                                                                                  | Example                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `knowledge_base_id`                                                                                                                          | *str*                                                                                                                                        | :heavy_check_mark:                                                                                                                           | The id of the knowledge base to query                                                                                                        |                                                                                                                                              |
| `query`                                                                                                                                      | *str*                                                                                                                                        | :heavy_check_mark:                                                                                                                           | Query string                                                                                                                                 | What is the capital of France?                                                                                                               |
| `prefilter_limit`                                                                                                                            | *Optional[int]*                                                                                                                              | :heavy_minus_sign:                                                                                                                           | Number of documents to retrieve from the knowledge base before filtering                                                                     | 10                                                                                                                                           |
| `top_k`                                                                                                                                      | *Optional[int]*                                                                                                                              | :heavy_minus_sign:                                                                                                                           | Number of documents to return                                                                                                                | 3                                                                                                                                            |
| `filters`                                                                                                                                    | List[[models.Filter](../../models/filter_.md)]                                                                                               | :heavy_minus_sign:                                                                                                                           | Per-field filters to apply to the query combined with AND                                                                                    | [<br/>{<br/>"field": "price",<br/>"operation": "\u003e",<br/>"value": 100<br/>},<br/>{<br/>"field": "category",<br/>"operation": "in",<br/>"value": [<br/>"product",<br/>"service"<br/>]<br/>}<br/>] |
| `rerank`                                                                                                                                     | *Optional[bool]*                                                                                                                             | :heavy_minus_sign:                                                                                                                           | Whether to rerank the results                                                                                                                |                                                                                                                                              |
| `parent_span_id`                                                                                                                             | *OptionalNullable[str]*                                                                                                                      | :heavy_minus_sign:                                                                                                                           | Parent span id                                                                                                                               |                                                                                                                                              |
| `retries`                                                                                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                             | :heavy_minus_sign:                                                                                                                           | Configuration to override the default retry behavior of the client.                                                                          |                                                                                                                                              |

### Response

**[List[models.QueryKnowledgeBaseResponse]](../../models/.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## delete_documents

Delete documents from a knowledge base based on filters

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_documents_knowledge__knowledge_base_id__query_delete" method="delete" path="/knowledge/{knowledge_base_id}/query" -->
```python
from opperai import Opper, models
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.delete_documents(knowledge_base_id="7418a0c9-d40d-4761-8b00-e8948f7d8426", filters=[
        {
            "field": "category",
            "operation": models.Op.EQUAL_,
            "value": "outdated",
        },
        {
            "field": "version",
            "operation": models.Op.LESS_THAN_,
            "value": 2,
        },
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                     | Type                                                                                                                          | Required                                                                                                                      | Description                                                                                                                   | Example                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `knowledge_base_id`                                                                                                           | *str*                                                                                                                         | :heavy_check_mark:                                                                                                            | The id of the knowledge base to delete or delete documents from                                                               |                                                                                                                               |
| `filters`                                                                                                                     | List[[models.Filter](../../models/filter_.md)]                                                                                | :heavy_minus_sign:                                                                                                            | Filters to apply for deletion. If no filters are provided, the entire knowledge base will be deleted.                         | [<br/>{<br/>"field": "category",<br/>"operation": "=",<br/>"value": "outdated"<br/>},<br/>{<br/>"field": "version",<br/>"operation": "\u003c",<br/>"value": 2<br/>}<br/>] |
| `retries`                                                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                              | :heavy_minus_sign:                                                                                                            | Configuration to override the default retry behavior of the client.                                                           |                                                                                                                               |

### Response

**[models.DeleteKnowledgeBaseResponse](../../models/deleteknowledgebaseresponse.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |

## add

Add data to a knowledge base

### Example Usage

<!-- UsageSnippet language="python" operationID="add_knowledge__knowledge_base_id__add_post" method="post" path="/knowledge/{knowledge_base_id}/add" -->
```python
from opperai import Opper
import os


with Opper(
    http_bearer=os.getenv("OPPER_HTTP_BEARER", ""),
) as opper:

    res = opper.knowledge.add(knowledge_base_id="c441b497-32db-4e24-8f41-ab160e1329fc", content="The capital of France is Paris", key="paris_123", metadata={
        "category": "product",
        "price": 100,
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                           | Type                                                                                                | Required                                                                                            | Description                                                                                         | Example                                                                                             |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `knowledge_base_id`                                                                                 | *str*                                                                                               | :heavy_check_mark:                                                                                  | The id of the knowledge base to add the data to                                                     |                                                                                                     |
| `content`                                                                                           | *str*                                                                                               | :heavy_check_mark:                                                                                  | N/A                                                                                                 | The capital of France is Paris                                                                      |
| `key`                                                                                               | *OptionalNullable[str]*                                                                             | :heavy_minus_sign:                                                                                  | The key of the document                                                                             | paris_123                                                                                           |
| `metadata`                                                                                          | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | The metadata of the document                                                                        | {<br/>"category": "product",<br/>"price": 100<br/>}                                                 |
| `configuration`                                                                                     | [OptionalNullable[models.TextProcessingConfiguration]](../../models/textprocessingconfiguration.md) | :heavy_minus_sign:                                                                                  | The configuration for the document                                                                  |                                                                                                     |
| `retries`                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                    | :heavy_minus_sign:                                                                                  | Configuration to override the default retry behavior of the client.                                 |                                                                                                     |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                    | Status Code                   | Content Type                  |
| ----------------------------- | ----------------------------- | ----------------------------- |
| errors.BadRequestError        | 400                           | application/json              |
| errors.UnauthorizedError      | 401                           | application/json              |
| errors.NotFoundError          | 404                           | application/json              |
| errors.RequestValidationError | 422                           | application/json              |
| errors.APIError               | 4XX, 5XX                      | \*/\*                         |