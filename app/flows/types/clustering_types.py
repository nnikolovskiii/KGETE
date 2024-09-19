from typing import List, Tuple, Dict
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from tqdm import tqdm


def recursive_clustering(
        vectors: np.ndarray,
        vector_ids_dict: Dict[Tuple[float], int],
        max_size: int = 20,
) -> List[int]:
    clusters = []
    cluster_model = AgglomerativeClustering(metric="cosine", linkage="average")
    cluster_labels = cluster_model.fit_predict(vectors)

    label_to_vectors = {}
    for i, label in enumerate(cluster_labels):
        if label not in label_to_vectors:
            label_to_vectors[label] = []
        label_to_vectors[label].append(vectors[i])

    for label, grouped_vectors in label_to_vectors.items():
        cluster_size = len(grouped_vectors)
        if cluster_size <= max_size:
            clusters.append([vector_ids_dict[tuple(vector)] for vector in grouped_vectors])
        elif cluster_size > max_size:
            sub_clusters = recursive_clustering(np.array(grouped_vectors), vector_ids_dict, max_size)
            clusters.extend(sub_clusters)

    return clusters


def cluster_vectors(
        vector_ids: List[int],
        qdb: QdrantDatabase
) -> List[List[int]]:
    vector_ids_dict: Dict[Tuple[float], int] = {}

    for type_id in tqdm(vector_ids):
        point = qdb.retrieve_point(collection_name="kg_llm_fusion", point_id=type_id)
        vector_ids_dict[tuple(point.vector)] = type_id

    vectors = np.array([key for key, value in vector_ids_dict.items()])
    clusters = recursive_clustering(vectors, vector_ids_dict)

    return clusters
