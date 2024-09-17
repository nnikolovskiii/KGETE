from app.llms.openai.chat import chat_with_openai
from app.templates.qa_generation_template import qa_generation_template
from pydantic import BaseModel

from app.utils.json_extraction import trim_and_load_json


class QAGenerationOutput(BaseModel):
    answer: str
    question: str


def qa_generation_chain(
        context: str
):
    template = qa_generation_template(context=context)

    is_finished = False
    json_data = ""
    while not is_finished:
        response = chat_with_openai(message=template)
        is_finished, json_data = trim_and_load_json(response)
    return QAGenerationOutput(**json_data)
