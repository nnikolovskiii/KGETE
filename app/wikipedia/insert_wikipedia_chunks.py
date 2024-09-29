import uuid
from typing import List, Optional
import re
import wikipedia
from pathlib import Path
from tqdm import tqdm

from app.chains.generic.models import Database
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from app.models.models import Chunk, Document


def insert_wikipedia_chunks(
        file_path_str: str,
        chunk_size: int = 2000,
        chunk_overlap: int = 300,
        databases: Optional[List[Database]] = None
) -> List[Chunk]:
    qdrant_db = QdrantDatabase()
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

    chunks: List[Chunk] = []
    documents: List[Document] = []

    for title in tqdm(titles, desc="Processing Titles"):
        page_content = wikipedia.page(title).content
        li = page_content.split("== See also ==")
        page_content = re.sub(r'\n+', '\n', li[0]).replace('\t', '')

        document_id = str(uuid.uuid4())
        documents.append(Document(id=document_id, name=title, context=page_content))

        chunk_contexts: List[str] = text_splitter.split_text(page_content)

        chunks.extend([Chunk(
            id=str(uuid.uuid4()),
            doc_id=document_id,
            context=chunk_context,
        ) for chunk_context in chunk_contexts])

    # databases
    if databases:
        if Database.MONGO in databases:
            [mongo_db.add_entry(
                entity=chunk,
                metadata={
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "file_path": file_path_str,
                }
            ) for chunk in chunks]

            [mongo_db.add_entry(
                entity=document,
                metadata={
                    "file_path": file_path_str,
                }
            )for document in documents]

        if Database.QDRANT in databases:
            [qdrant_db.embedd_and_upsert_record(
                value=chunk.context,
                collection_name="chunks",
                unique_id=chunk.id,
                metadata={"file_path": file_path_str},
            ) for chunk in tqdm(chunks, desc="Adding chunks to Qdrant")]