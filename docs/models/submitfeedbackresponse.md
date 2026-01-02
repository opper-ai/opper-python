# SubmitFeedbackResponse


## Fields

| Field                                        | Type                                         | Required                                     | Description                                  |
| -------------------------------------------- | -------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| `span_id`                                    | *str*                                        | :heavy_check_mark:                           | The ID of the span                           |
| `score`                                      | *float*                                      | :heavy_check_mark:                           | The feedback score that was submitted        |
| `comment`                                    | *OptionalNullable[str]*                      | :heavy_minus_sign:                           | The feedback comment that was submitted      |
| `example_saved`                              | *bool*                                       | :heavy_check_mark:                           | Whether the example was saved to the dataset |