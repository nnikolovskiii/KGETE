from app.wikipedia.insert_wikipedia_chunks import insert_wikipedia_chunks, DatabaseType


insert_wikipedia_chunks(
        file_path_str="/home/nikola/dev/kg_llm_fusion/app/resources/astronomy_titles",
        database_type=DatabaseType.qdrant,
        chunk_size=1000,
        chunk_overlap=150
)


