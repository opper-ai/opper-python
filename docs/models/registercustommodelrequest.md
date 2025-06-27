# RegisterCustomModelRequest


## Fields

| Field                                          | Type                                           | Required                                       | Description                                    |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |
| `name`                                         | *str*                                          | :heavy_check_mark:                             | The name of the custom language model          |
| `identifier`                                   | *str*                                          | :heavy_check_mark:                             | The identifier of the custom language model    |
| `extra`                                        | Dict[str, *Any*]                               | :heavy_minus_sign:                             | Extra metadata about the custom language model |
| `api_key`                                      | *OptionalNullable[str]*                        | :heavy_minus_sign:                             | The API key of the custom language model       |