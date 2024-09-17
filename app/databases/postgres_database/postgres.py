from pydantic import BaseModel, Field
import psycopg2
import uuid
from typing import Optional, Any, TypeVar, List, Tuple
from typing import Type as TypingType
from psycopg2 import extensions

T = TypeVar('T')


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


class PostgresDatabase:
    conn: psycopg2.extensions.connection
    cur: psycopg2.extensions.cursor

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="kg_llm_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def get_id_for_value(self, value: str) -> uuid.UUID:
        self.cur.execute("SELECT id FROM key_value_pairs WHERE value = %s", (value,))
        existing_row = self.cur.fetchone()

        if existing_row is not None:
            return existing_row[0]

        unique_id = uuid.uuid4()
        self.cur.execute("INSERT INTO key_value_pairs (id, value) VALUES (%s, %s)", (str(unique_id), value))

        self.conn.commit()

        return unique_id

    def add_entry(self, entity: Any, table: str) -> bool:
        columns = [attr for attr in vars(entity)]
        values = [getattr(entity, attr) for attr in vars(entity)]

        query = f"""
            INSERT INTO {table} ({', '.join(columns)}) 
            VALUES ({', '.join(['%s'] * len(values))})
        """

        self.cur.execute(query, values)
        self.conn.commit()

        return True

    def get_all_entries(self, class_type: TypingType[T], table: str) -> List[T]:
        query = f"SELECT * FROM {table}"
        self.cur.execute(query)
        rows = self.cur.fetchall()

        columns = [desc[0] for desc in self.cur.description]

        entries = []
        for row in rows:
            entry_data = {columns[i]: row[i] for i in range(len(columns))}
            entry = class_type(**entry_data)
            entries.append(entry)

        return entries

    def get_types(self, group_id: str, value_type: str) -> List[str]:
        query = """
            SELECT value FROM types
            WHERE group_id = %s AND type = %s
        """
        self.cur.execute(query, (group_id, value_type))
        rows = self.cur.fetchall()

        return [row[0] for row in rows]

    def get_groups_by_level(self, level: int) -> List[Group]:
        query = """
                    SELECT * FROM groups
                    WHERE level = %s
                """
        self.cur.execute(query, (level,))
        rows = self.cur.fetchall()

        columns = [desc[0] for desc in self.cur.description]

        groups = []
        for row in rows:
            group_data = {columns[i]: row[i] for i in range(len(columns))}
            group = Group(**group_data)
            groups.append(group)

        return groups

    def get_deepest_types(self) -> Tuple[List[str], List[str]]:
        node_types: List[str] = []
        rel_types: List[str] = []
        self.cur.execute("SELECT MAX(level) AS highest_level FROM groups")
        highest_level = self.cur.fetchone()[0]

        query = """
            SELECT t.value
            FROM types t
            JOIN groups g ON t.group_id = g.id
            WHERE g.level = %s AND t.type = %s
        """
        self.cur.execute(query, (highest_level, 'rel_type'))
        rows = self.cur.fetchall()

        rel_types = [row[0] for row in rows]

        query = """
                    SELECT t.value
                    FROM types t
                    JOIN groups g ON t.group_id = g.id
                    WHERE g.level = %s AND t.type = %s
                """
        self.cur.execute(query, (highest_level, 'node_type'))
        rows = self.cur.fetchall()

        node_types = [row[0] for row in rows]

        return node_types, rel_types
