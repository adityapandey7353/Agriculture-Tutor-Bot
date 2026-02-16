from database.chroma_setup import get_collection

collection = get_collection()

def load_knowledge(file_path="data/farming_tips.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        docs = [line.strip() for line in f.readlines() if line.strip()]

    ids = [str(i) for i in range(len(docs))]

    collection.add(documents=docs, ids=ids)
    print("✅ Knowledge loaded into ChromaDB")


def search_knowledge(query, n_results=2):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results["documents"][0]