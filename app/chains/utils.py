import uuid
from app.databases.postgres_database.postgres import PostgresDatabase, Group, Type
from pydantic import BaseModel
from charset_normalizer.md import List


class TypesOutput(BaseModel):
    node_types: List[str]
    rel_types: List[str]


def save_group_and_types(
        text: str,
        types_output: TypesOutput,
        level: int = 0
) -> bool:
    db = PostgresDatabase()

    unique_id = str(uuid.uuid4())
    group = Group(
        id=unique_id,
        context=text,
        level=level
    )

    db.add_entry(group, "groups")

    for node_type in types_output.node_types:
        unique_id = str(uuid.uuid4())
        db.add_entry(Type(
            id=unique_id,
            type="node_type",
            value=node_type,
            group_id=group.id
        ), table="types")

    for rel_type in types_output.rel_types:
        unique_id = str(uuid.uuid4())
        db.add_entry(Type(
            id=unique_id,
            type="rel_type",
            value=rel_type,
            group_id=group.id
        ), table="types")

    return True
