from app.llms.openai.chat import chat_with_openai
from app.templates.summarize_template import summarize_template


def summarization_chain(
        text: str
) -> str:
    template = summarize_template(text=text)
    response = chat_with_openai(message=template)
    return response
