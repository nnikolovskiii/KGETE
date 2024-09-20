import uuid
from typing import List
import re
import wikipedia
from pathlib import Path
from tqdm import tqdm

from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Document, Chunk
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.databases.qdrant_database.qdrant_database import QdrantDatabase


def insert_wikipedia_chunks(
        file_path_str: str,
        qdrant: bool,
        chunk_size: int = 2000,
        chunk_overlap: int = 300,
) -> None:
    qdrant_db = QdrantDatabase() if qdrant else None
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
                "file_path": file_path_str,
            }
        )

        chunks: List[str] = text_splitter.split_text(page_content)

        for chunk in tqdm(chunks, desc="Processing Chunks", leave=False):
            unique_id = str(uuid.uuid4())
            if qdrant:
                qdrant_db.embedd_and_upsert_record(
                    value=chunk,
                    collection_name="chunks",
                    unique_id=unique_id,
                    metadata={"file_path": file_path_str},
                )

            mongo_db.add_entry(
                entity=Chunk(id=unique_id, doc_id=document.id, context=chunk),
                metadata={
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "file_path": file_path_str,
                }
            )
