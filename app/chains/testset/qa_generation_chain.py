from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.templates.testset.qa_generation_template import qa_generation_template
from pydantic import BaseModel


class QAGenerationOutput(BaseModel):
    answer: str
    question: str


def qa_generation_chain(
        context: str
):
    template = qa_generation_template(context=context)
    json_data = generic_chat_chain_json(template)
    return QAGenerationOutput(**json_data)
