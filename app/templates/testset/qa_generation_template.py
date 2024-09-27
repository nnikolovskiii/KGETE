def qa_generation_template(
        context: str
):
    return f"""Given the context generate an answer and question pair, that can be entirely answered using the context. 
Do not provide any knowledge outside the context when creating the answer question pair.
Make the question short and precise.

Context:
{context}

Important: Make the question short, precise and simple.

Return a JSON with keys "answer" and "question". First generate the answer and after that provide the question."""