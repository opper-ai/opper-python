# ListFilesResponse


## Fields

| Field                                     | Type                                      | Required                                  | Description                               | Example                                   |
| ----------------------------------------- | ----------------------------------------- | ----------------------------------------- | ----------------------------------------- | ----------------------------------------- |
| `id`                                      | *str*                                     | :heavy_check_mark:                        | The id of the file                        |                                           |
| `original_filename`                       | *str*                                     | :heavy_check_mark:                        | The original filename                     |                                           |
| `size`                                    | *int*                                     | :heavy_check_mark:                        | The size of the file in bytes             |                                           |
| `status`                                  | *str*                                     | :heavy_check_mark:                        | The indexing status of the file           |                                           |
| `document_id`                             | *int*                                     | :heavy_check_mark:                        | The id of the associated document         |                                           |
| `metadata`                                | Dict[str, *Any*]                          | :heavy_minus_sign:                        | The metadata attached to the file         | {<br/>"category": "legal",<br/>"client": "acme"<br/>} |