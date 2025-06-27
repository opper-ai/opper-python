# Choice


## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `finish_reason`                                                        | [models.FinishReason](../models/finishreason.md)                       | :heavy_check_mark:                                                     | N/A                                                                    |
| `index`                                                                | *int*                                                                  | :heavy_check_mark:                                                     | N/A                                                                    |
| `logprobs`                                                             | [OptionalNullable[models.ChoiceLogprobs]](../models/choicelogprobs.md) | :heavy_minus_sign:                                                     | N/A                                                                    |
| `message`                                                              | [models.ChatCompletionMessage](../models/chatcompletionmessage.md)     | :heavy_check_mark:                                                     | N/A                                                                    |
| `__pydantic_extra__`                                                   | Dict[str, *Any*]                                                       | :heavy_minus_sign:                                                     | N/A                                                                    |