from enum import Enum


class Database(Enum):
    QDRANT: str = 'qdrant'
    NEO4j: str = 'neo4j'
    MONGO: str = 'mongo'
