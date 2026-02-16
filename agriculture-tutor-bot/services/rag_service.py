from database.vector_store import search_knowledge

def get_context(query):
    docs = search_knowledge(query)
    context = "\n".join(docs)
    return context