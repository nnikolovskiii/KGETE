from app.wikipedia.insert_wikipedia_chunks import insert_wikipedia_chunks


insert_wikipedia_chunks(
        file_path_str="/home/nikola/dev/kg_llm_fusion/app/resources/astronomy_titles",
        qdrant=True,
        chunk_size=1000,
        chunk_overlap=150
)


