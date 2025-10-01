# EvaluationConfig

Configuration for evaluation features stored under 'beta.evaluation'.

- enabled: master switch
- scorers: which evaluators to run. Accepts:
    - string: "base" | "rubrics"
    - dict: { "rubrics": RubricDefinition-like payload }
    - list[str | dict]
  "base" is the default scorer.


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `enabled`                                                        | *Optional[bool]*                                                 | :heavy_minus_sign:                                               | Enable evaluation features (base or rubrics).                    |
| `scorers`                                                        | [Optional[models.ScorersUnion2]](../models/scorersunion2.md)     | :heavy_minus_sign:                                               | Evaluation scorers to run: 'base', 'rubrics', or a list of them. |
| `__pydantic_extra__`                                             | Dict[str, *Any*]                                                 | :heavy_minus_sign:                                               | N/A                                                              |