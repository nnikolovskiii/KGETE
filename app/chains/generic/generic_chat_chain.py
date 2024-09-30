import os
from typing import Any, Dict
import logging
from pydantic import BaseModel

from dotenv import load_dotenv

from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.llms.generic_chat import generic_chat
from app.utils.json_extraction import trim_and_load_json


class ChatResponse(BaseModel):
    message: str
    response: str
    llm_model: str


def generic_chat_chain_json(
        template: str,
        list_name: str = ""
) -> Dict[str, Any]:
    mdb = MongoDBDatabase()
    is_finished = False
    json_data = {}
    tries = 0
    response = ""
    while not is_finished:
        if tries > 0:
            logging.warning(f"Chat not returning as expected. it: {tries}")

        if tries > 3:
            if tries > 0:
                logging.warning("Chat not returning as expected.")
            raise Exception()

        response = generic_chat(message=template)

        is_finished, json_data = trim_and_load_json(input_string=response, list_name=list_name)
        tries += 1

    load_dotenv()
    chat_model = os.getenv("CHAT_MODEL")
    mdb.add_entry(entity=ChatResponse(message=template, response=response, llm_model=chat_model), metadata={"version": 1})

    return json_data
