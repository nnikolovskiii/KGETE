from app.wikipedia.insert_wikipedia_chunks import insert_wikipedia_chunks
import os

from dotenv import load_dotenv

load_dotenv()
path = os.getenv("PATH")

insert_wikipedia_chunks(
        file_path_str=path+"app/resources/astronomy_titles",
        qdrant=True,
        chunk_size=1000,
        chunk_overlap=150
)


