from pydantic import BaseModel
from typing import Optional


class Group(BaseModel):
    id: str
    context: str
    summed_group_id: Optional[str] = None
    level: Optional[int] = 0


class Type(BaseModel):
    id: Optional[str] = None
    type: str
    value: str
    description: str
    parent_type: Optional[str] = None

    def __str__(self):
        return f"{self.value}: {self.description}"


class Document(BaseModel):
    id: str
    name: Optional[str] = None
    context: str


class Chunk(BaseModel):
    id: str
    doc_id: str
    context: str