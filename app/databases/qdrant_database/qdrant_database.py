import uuid
from typing import List, Dict, Any, Optional, TypeVar
from qdrant_client import QdrantClient, models
from app.llms.generic.openai_embedding import embedd_content
from pydantic import BaseModel
from qdrant_client.conversions import common_types as types


class SearchOutput(BaseModel):
    score: float
    value_type: str


T = TypeVar('T')


class QdrantDatabase:
    client: QdrantClient

    def __init__(self):
        self.client = QdrantClient(url="http://localhost:6333")

    def collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name)

    def create_collection(
            self,
            collection_name: str
    ):
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=3072, distance=models.Distance.COSINE),
        )

    def embedd_and_upsert_record(
            self,
            value: str,
            collection_name: str,
            unique_id: str = None,
            metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        if not self.collection_exists(collection_name):
            self.create_collection(collection_name)

        metadata = {} if metadata is None else metadata
        metadata["value"] = value

        vector = embedd_content(value)
        record_id = str(uuid.uuid4()) if unique_id is None else unique_id

        self.client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=record_id,
                    payload=metadata,
                    vector=vector,
                ),
            ],
        )

    def delete_all_collections(self):
        collections = self.client.get_collections().collections
        for collection in collections:
            self.client.delete_collection(collection_name=collection.name)

    def retrieve_point(
            self,
            collection_name: str,
            point_id: str
    ) -> types.Record:
        points = self.client.retrieve(
            collection_name=collection_name,
            ids=[point_id],
            with_vectors=True,
        )
        return points[0]

    def search_embeddings(
            self,
            query_vector: List[float],
            collection_name: str,
            score_threshold: float,
            top_k: int,
            filter: Optional[Dict[str, Any]] = None
    ) -> List[types.ScoredPoint]:
        file_condition=None
        if filter:
            file_condition = models.Filter(must=[
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value),
                )
                for key, value in filter.items()])

        return self.client.search(
            query_vector=query_vector,
            score_threshold=score_threshold,
            collection_name=collection_name,
            limit=top_k,
            query_filter=file_condition
        )
