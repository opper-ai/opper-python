import os
from typing import List, Union
from opperai import Opper
from opperai.models import CreateKnowledgeBaseResponse, QueryKnowledgeBaseResponse
from pydantic import BaseModel

opper = Opper(os.getenv("OPPER_API_KEY"))


class Answer(BaseModel):
    answer: str
    steps: List[str]


class QuestionAndContext(BaseModel):
    question: str
    context: Union[List[str], str]


def answer_question(index: CreateKnowledgeBaseResponse, question: str) -> Answer:
    results: QueryKnowledgeBaseResponse = opper.knowledge.query(
        index_id=index.id, top_k=1, query=question
    )

    response = opper.call(
        name="answer_question",
        instructions="Answer the question and provide the steps to do so",
        input=QuestionAndContext(question=question, context=results[0].content),
        output_schema=Answer.model_json_schema(),
    )
    opper.span_metrics.create_metric(
        span_id=response.span_id, dimension="artificial_score", value=5
    )

    return response.json_payload


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


def index_qna(qnas: list[dict]):
    try:
        index = opper.knowledge.get_by_name(index_name="qna")
    except Exception:
        index = opper.knowledge.create_base(name="qna")

    for qna in qnas:
        opper.knowledge.add_data(
            index_id=index.id,
            key=qna["id"],
            content=f"question: {qna['question']}\nanswer: {qna['answer']}",
            metadata={
                "id": qna["id"],
            },
        )

    return index


def run_sync():
    index = index_qna(qna)

    question = "How can I see my invoices?"
    answer = answer_question(index, question)
    print(answer)


run_sync()
