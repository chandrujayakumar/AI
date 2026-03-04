import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import uuid

index_name = "clauseai-index"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Pinecone
pc = Pinecone(api_key=os.environ.get("pcsk_2JkNvF_G2ybVJfn3tkXZXGUPbWAnvfUyVaHoZcH2a1PKjpw93eDjkjg2AWCxa2nKVbMWvV"))

index_name = "clauseai-index"

# Create index safely
existing_indexes = [i.name for i in pc.list_indexes().indexes]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)


def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def store_contract(text):
    chunks = chunk_text(text)

    vectors = []
    for chunk in chunks:
        embedding = model.encode(chunk).tolist()
        vectors.append({
            "id": str(uuid.uuid4()),
            "values": embedding,
            "metadata": {"text": chunk}
        })

    index.upsert(vectors)


def query_relevant_chunks(query, top_k=3):
    query_embedding = model.encode(query).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return [match["metadata"]["text"] for match in results["matches"]]