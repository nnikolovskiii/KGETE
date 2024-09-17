import uuid
from enum import Enum
from typing import List
import re
import wikipedia
from pathlib import Path
from tqdm import tqdm

from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Document, Chunk
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.databases.qdrant_database.qdrant_database import QdrantDatabase


class DatabaseType(str, Enum):
    postgres = 'mongodb'
    qdrant = 'qdrant'


def insert_wikipedia_chunks(
        file_path_str: str,
        database_type: DatabaseType,
        chunk_size: int = 2000,
        chunk_overlap: int = 300,
) -> None:
    qdrant_db = QdrantDatabase() if database_type == DatabaseType.qdrant else None
    mongo_db = MongoDBDatabase()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
        ]
    )

    file_path = Path(file_path_str)

    titles = file_path.read_text().splitlines()

    for title in tqdm(titles, desc="Processing Titles"):
        page_content = wikipedia.page(title).content
        li = page_content.split("== See also ==")
        page_content = re.sub(r'\n+', '\n', li[0]).replace('\t', '')
        document = Document(id=str(uuid.uuid4()), name=title, context=page_content)
        mongo_db.add_entry(
            entity=document,
            metadata={
                "file_path":file_path_str,
            }
        )

        chunks: List[str] = text_splitter.split_text(page_content)

        for chunk in tqdm(chunks, desc="Processing Chunks", leave=False):
            unique_id = str(uuid.uuid4())
            if database_type == DatabaseType.qdrant:
                qdrant_db.embedd_and_upsert_record(
                    value=chunk,
                    value_type="chunk",
                    collection_name="kg_llm_fusion",
                    unique_id=unique_id,
                )

            mongo_db.add_entry(
                entity=Chunk(id=unique_id, doc_id=document.id, context=chunk),
                metadata={
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "file_path": file_path_str,
                }
            )
