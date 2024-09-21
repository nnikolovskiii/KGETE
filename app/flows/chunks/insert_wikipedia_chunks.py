from app.chains.generic.models import Database
from app.wikipedia.insert_wikipedia_chunks import insert_wikipedia_chunks
import os

from dotenv import load_dotenv


def insert_chunks():
    load_dotenv()
    path = os.getenv("BASE_PATH")

    insert_wikipedia_chunks(
        file_path_str=path + "app/resources/astronomy_titles",
        chunk_size=1000,
        chunk_overlap=150,
        databases=[Database.MONGO, Database.QDRANT]
    )
