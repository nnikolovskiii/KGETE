import random

from app.chains.testset.qa_generation_chain import qa_generation_chain
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from app.templates.qa_generation_template import qa_generation_template


def qa_generation(
        num_questions: int
):
    mdb = MongoDBDatabase()
    qdb = QdrantDatabase()
    chunk_ids = mdb.get_ids(class_type=Chunk)

    for _ in range(num_questions):
        random_chunk_id = random.choice(chunk_ids)
        random_point = qdb.retrieve_point(
            collection_name="kg_llm_fusion",
            point_id=random_chunk_id
        )

        records = qdb.search_embeddings(
            query_vector=random_point.vector,
            collection_name="kg_llm_fusion",
            score_threshold=0.5,
            top_k=5,
            filter_type="chunk"
        )

        chunks = [record.payload['value'] for record in records if "value" in record.payload.keys()]

        context = "\n".join(chunks)

        qa_output = qa_generation_chain(context=context)

        mdb.add_entry(
            entity=qa_output,
            metadata={
                "top_k": 5,
                "score_threshold": 0.5,
                "template": qa_generation_template(context=""),
            }
        )
