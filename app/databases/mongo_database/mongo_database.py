import logging
import os

from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional, Any, List, Dict, TypeVar
from typing import Type as TypingType
from dotenv import load_dotenv

T = TypeVar('T', bound=BaseModel)


class MongoDBDatabase:
    client: MongoClient
    db: Any

    def __init__(self):
        load_dotenv()
        url = os.getenv("URL")
        self.client = MongoClient(f"mongodb://root:example@{url}:27017/")
        self.db = self.client["kg_llm_db"]

    def add_entry(
            self,
            entity: BaseModel,
            collection_name: Optional[str] = None,
            metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        collection_name = entity.__class__.__name__ if collection_name is None else collection_name
        collection = self.db[collection_name]
        entry = entity.model_dump()
        if metadata:
            entry.update(metadata)

        collection.insert_one(entry)
        return True

    def get_entries(
            self,
            class_type: TypingType[T],
            doc_filter: Dict[str, Any] = None,
            collection_name: Optional[str] = None,
    ) -> List[T]:
        collection_name = class_type.__name__ if collection_name is None else collection_name
        collection = self.db[collection_name]
        documents = collection.find(doc_filter or {})
        class_fields = class_type.model_fields.keys()

        results = []
        for doc in documents:
            metadata = {}
            filtered_doc = {}
            for key, value in doc.items():
                if key in class_fields:
                    filtered_doc[key] = value
                else:
                    metadata[key] = value

            instance = class_type(**filtered_doc)
            results.append(instance)

        return results

    def get_ids(
            self,
            class_type: TypingType[BaseModel],
            collection_name: Optional[str] = None,
            doc_filter: Dict[str, Any] = None,
    ) -> List[str]:
        collection_name = class_type.__name__ if collection_name is None else collection_name
        collection = self.db[collection_name]

        ids_cursor = collection.find(doc_filter or {}, {"id": 1})

        return [str(doc["id"]) for doc in ids_cursor if "id" in doc]

    def get_entity(
            self,
            id: str,
            class_type: TypingType[T],
            collection_name: Optional[str] = None,
    ) -> Optional[T]:
        collection_name = class_type.__name__ if collection_name is None else collection_name
        collection = self.db[collection_name]

        document = collection.find_one({"id": id})
        if document:
            class_fields = class_type.model_fields.keys()
            filtered_doc = {key: value for key, value in document.items() if key in class_fields}

            instance = class_type(**filtered_doc)
            return instance

        return None

    def update_entity(
            self,
            entity: BaseModel,
            collection_name: Optional[str] = None,
            update: Optional[Dict[str, Any]] = None
    ) -> bool:
        collection_name = entity.__class__.__name__ if collection_name is None else collection_name
        collection = self.db[collection_name]

        entity_id = entity.id if hasattr(entity, "id") else None
        if not entity_id:
            raise ValueError("The entity must have an 'id' field to update.")

        entity_dict = entity.model_dump()

        if update:
            entity_dict.update(update)

        result = collection.update_one(
            {"id": entity_id},
            {"$set": entity_dict}
        )

        return result.modified_count > 0

    def delete_collection(self, collection_name: str) -> bool:
        if collection_name not in self.db.list_collection_names():
            logging.info(f"Collection '{collection_name}' does not exist.")

        self.db[collection_name].drop()
        return True

    def delete_entity(
            self,
            entity: BaseModel,
            collection_name: Optional[str] = None
    ) -> bool:
        collection_name = entity.__class__.__name__ if collection_name is None else collection_name
        collection = self.db[collection_name]

        entity_id = entity.id if hasattr(entity, "id") else None
        if not entity_id:
            raise ValueError("The entity must have an 'id' field to delete.")

        result = collection.delete_one({"id": entity_id})

        return result.deleted_count > 0

