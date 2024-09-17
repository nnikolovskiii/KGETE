from beir import util, LoggingHandler
from beir.datasets.data_loader import GenericDataLoader
import pathlib, os

from app.databases.postgres_database.postgres import PostgresDatabase, Document

# Set the path to the BEIR dataset
dataset = "scifact"
data_path = util.download_and_unzip("https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scifact.zip",
                                    dataset)

# Load the dataset
corpus, queries, corpus_queries = GenericDataLoader(data_path).load(split="test")

db = PostgresDatabase()

all_corpus = ""

for item in corpus.items():
    corpus_id = item[0]
    corpus_text = item[1]['text']
    all_corpus += corpus_text
    #db.add_entry(entity=Document(id=corpus_id, context=corpus_text), table="docs")

for item in corpus_queries.items():
    if len(item[1])>1:
        print("lol")

print(len(all_corpus))

# # Print the length of each component
# print("Corpus length:", len(corpus))
# print("Queries length:", len(queries))
# print("Qrels length:", len(qrels))
#
# # Print the first entry of each
# print("\nFirst Corpus entry:", list(corpus.items())[0])
# print("\nFirst Query entry:", list(queries.items())[0])
# print("\nFirst Qrel entry:", list(qrels.items())[0])
