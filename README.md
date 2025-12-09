# Opper Python SDK

This is the Opper Python SDK. See below for getting started, and the [docs](https://docs.opper.ai) for more information. The SDK has builtin documentation and examples in function docstrings, which should be visible in your code editor as you are using the functions.

## Install

```bash
pip install opperai
```

## Configuration

### Environment variable

- `OPPER_API_KEY` environment variable is read by the SDK if no `api_key` is provided to the `Client` object. 

## Using opper

```python
from typing import List

from opperai import Index, Opper, trace
from opperai.types import DocumentIn
from opperai.types.indexes import DocumentIn, RetrievalResponse
from pydantic import BaseModel


class Answer(BaseModel):
    steps: List[str]


class QuestionAndContext(BaseModel):
    question: str
    context: List[RetrievalResponse]


@trace
def answer_question(index: Index, question: str) -> Answer:
    results = index.query(question, 1, None)

    result, response = opper.call(
        name="answer_question",
        instructions="Answer the question and provide the steps to do so",
        input=QuestionAndContext(question=question, context=results),
        output_type=Answer,
    )
    response.span.save_metric("artificial_score", 5)

    return result


@trace
def translate(answer: Answer, language: str) -> str:
    result, _ = opper.call(
        name="translate",
        instructions="Translate the answer to the given language",
        input=answer,
        output_type=Answer,
    )
    return result


qna = [
    {
        "question": "I cannot log in to my account",
        "answer": "Use the reset password feature by clicking on 'Forgot password?' and then follow the instructions from email",
        "id": "1",
    },
    {
        "question": "How can I see my invoices?",
        "answer": "Go to the billing section and click on 'Invoices'",
        "id": "2",
    },
    {
        "question": "How can I add a new user to my account?",
        "answer": "Upgrade account and add the user to your account",
        "id": "3",
    },
]

opper = Opper()


def index_qna(qnas: list[dict]):
    index = opper.indexes.create("qna")

    for qna in qnas:
        index.add(
            DocumentIn(
                key=qna["id"],
                content=f"question: {qna['question']}\nanswer: {qna['answer']}",
                metadata={
                    "id": qna["id"],
                },
            )
        )

    return index


def run():
    index = index_qna(qna)

    question = "How can I see my invoices?"

    with opper.traces.start("answer_question") as trace:
        answer = answer_question(index, question)
        print(answer)


run()
```

# More examples

See examples in our [documentation](https://docs.opper.ai)
and [examples](https://github.com/opper-ai/opper-python/tree/main/examples) folder.
