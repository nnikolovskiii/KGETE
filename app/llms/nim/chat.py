import os
from dotenv import load_dotenv
from openai import OpenAI


def chat_with_llama70(
        message: str,
) -> str:
    load_dotenv()
    nim_api_key = os.getenv("NIM_API_KEY")

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=nim_api_key
    )

    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": message}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=10000,
        stream=False
    )

    if completion.choices[0].message.content is not None:
        return completion.choices[0].message.content
    else:
        raise Exception()
