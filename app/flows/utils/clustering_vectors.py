from typing import List, Tuple, Dict
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from tqdm import tqdm

import numpy as np
from typing import List, Dict, Tuple
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_distances



def divisive_clustering(
        vectors: np.ndarray,
        vector_ids_dict: Dict[Tuple[float], str],
        max_size: int
) -> List[List[str]]:
    clusters = []
    queue = [vectors]  # Start with all vectors in one cluster

    while queue:
        current_vectors = queue.pop(0)  # Process the current cluster
        print(f"Processing cluster with {len(current_vectors)} vectors")

        if len(current_vectors) <= max_size:
            print(f"Cluster is small enough, adding to final clusters")
            clusters.append([vector_ids_dict[tuple(vector)] for vector in current_vectors])
        else:
            print(f"Cluster too large, splitting...")

            # Compute cosine distances for the cluster
            distances = cosine_distances(current_vectors)

            # Find the two most dissimilar points (maximum distance)
            farthest_points = np.unravel_index(np.argmax(distances), distances.shape)
            point1, point2 = current_vectors[farthest_points[0]], current_vectors[farthest_points[1]]

            # Split the cluster based on proximity to the farthest points
            group1, group2 = [], []
            for vector in current_vectors:
                dist_to_p1 = np.linalg.norm(vector - point1)
                dist_to_p2 = np.linalg.norm(vector - point2)
                if dist_to_p1 < dist_to_p2:
                    group1.append(vector)
                else:
                    group2.append(vector)

            # Add the new clusters to the queue for further processing
            queue.append(np.array(group1))
            queue.append(np.array(group2))

    return clusters

def pack_items(ind_elements, max_capacity):
    ind_elements.sort(key=lambda x: x[1], reverse=True)

    bags = []

    for ind, element in ind_elements:
        placed = False
        for bag in bags:
            if sum([elem for ind, elem in bag]) + element <= max_capacity:
                bag.append((ind, element))
                placed = True
                break

        if not placed:
            bags.append([(ind, element)])

    return bags

def cluster_vectors(
        vector_ids: List[str],
        qdb: QdrantDatabase,
        max_size: int = 20
) -> List[List[str]]:
    vector_ids_dict: Dict[Tuple[float], str] = {}

    for type_id in tqdm(vector_ids):
        point = qdb.retrieve_point(collection_name="nodes", point_id=type_id)
        vector_ids_dict[tuple(point.vector)] = type_id

    vectors = np.array([key for key, value in vector_ids_dict.items()])
    clusters = divisive_clustering(vectors, vector_ids_dict, max_size=max_size)

    cluster_sizes: List[Tuple[int, int]] = [(ind, len(cluster)) for ind, cluster in enumerate(clusters)]
    cluster_groups = pack_items(ind_elements=cluster_sizes, max_capacity=22)

    new_clusters: List[List[str]] = []

    for cluster_group in cluster_groups:
        new_clusters.append([x for ind, _ in cluster_group for x in clusters[ind]])

    return new_clusters
