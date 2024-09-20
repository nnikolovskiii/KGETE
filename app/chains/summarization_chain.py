from app.llms.generic.generic_chat import generic_chat
from app.templates.summarize_template import summarize_template


def summarization_chain(
        text: str
) -> str:
    template = summarize_template(text=text)
    response = generic_chat(message=template)
    return response
