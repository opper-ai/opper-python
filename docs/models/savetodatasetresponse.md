# SaveToDatasetResponse


## Fields

| Field                                    | Type                                     | Required                                 | Description                              |
| ---------------------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| `dataset_id`                             | *str*                                    | :heavy_check_mark:                       | The ID of the dataset                    |
| `dataset_entry_id`                       | *str*                                    | :heavy_check_mark:                       | The ID of the dataset entry              |
| `input`                                  | *OptionalNullable[str]*                  | :heavy_minus_sign:                       | The input of the dataset entry           |
| `output`                                 | *OptionalNullable[str]*                  | :heavy_minus_sign:                       | The output of the dataset entry          |
| `expected`                               | *OptionalNullable[str]*                  | :heavy_minus_sign:                       | The expected output of the dataset entry |
| `comment`                                | *OptionalNullable[str]*                  | :heavy_minus_sign:                       | The comment of the dataset entry         |