import os
from dotenv import load_dotenv
import requests
import json

from app.utils.json_extraction import trim_and_load_json


def chat_with_ollama(
        message: str,
) -> str:
    url = 'http://localhost:11434/api/generate'

    data = {
        'model': 'llama3.1',
        'prompt': message,
        'stream': False
    }

    response = requests.post(url, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        return response_data['response']
    else:
        response.raise_for_status()