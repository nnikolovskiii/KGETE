from typing import List, Tuple, Optional
import uuid
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk
from app.databases.qdrant_database.qdrant_database import QdrantDatabase


def get_top_keywords(num: int) -> List[str]:
    mdb = MongoDBDatabase()
    chunks = mdb.get_entries(Chunk)

    text = " ".join([chunk.context for chunk in chunks])

    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')

    tokens = nltk.word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t.lower() not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(tokens)

    keyword_scores = vectorizer.transform([' '.join(tokens)]).toarray()[0]

    top_keywords = sorted(zip(vectorizer.get_feature_names_out(), keyword_scores), key=lambda x: x[1], reverse=True)[:num]

    return [word for word, freq in top_keywords]


def get_context_from_top_keywords(
        num_keywords: int = 20,
        top_k: int = 1,
) -> Tuple[str, List[str]]:
    top_keywords = get_top_keywords(num_keywords)

    context = ""
    qdb = QdrantDatabase()
    for keyword in top_keywords:
        unique_id = str(uuid.uuid4())
        qdb.embedd_and_upsert_record(
            value=keyword,
            collection_name="miscellaneous",
            unique_id=unique_id,
            metadata={
                "type":"keyword"
            }
        )
        point = qdb.retrieve_point(
            point_id=unique_id,
            collection_name="miscellaneous",
        )

        points = qdb.search_embeddings(
            query_vector=point.vector,
            collection_name="Chunks",
            score_threshold=0.2,
            top_k=top_k,
        )

        for point in points:
            context += "\n" + point.payload["value"]

    return context, top_keywords
