from pathlib import Path

from docLoader import load_pdf
from chunker import chunk_pages
from embedder import generate_embeddings
from retriever import retrieve, retrieve_from_db
from db import insert_chunks

project_root = Path(__file__).resolve().parent
documents_dir = project_root / "documents"

pdf_files = sorted(documents_dir.glob("*.pdf"))

all_chunks = []


# ==========================================
# 1. PDF → Pages → Chunks
# ==========================================

for pdf_path in pdf_files:
    pages = load_pdf(str(pdf_path))

    for page in pages:
        page["filename"] = pdf_path.name

    chunks = chunk_pages(
        pages,
        chunk_size=500,
        overlap=100,
    )

    all_chunks.extend(chunks)


# ==========================================
# 2. Chunks → Embeddings
# ==========================================

embedded_chunks = generate_embeddings(all_chunks)


# ==========================================
# 3. Verify
# ==========================================

print("Total PDFs:", len(pdf_files))
print("Total chunks:", len(embedded_chunks))

if embedded_chunks:
    print("Embedding dimension:", len(embedded_chunks[0]["embedding"]))


# ==========================================
# 4. Save chunks → PostgreSQL
# ==========================================

# insert_chunks(embedded_chunks)

# print("Chunks inserted into database!")


# ==========================================
# 5. Test Retrieval
# ==========================================

query = "How many annual leave days do full-time employees get?"

results = retrieve_from_db(
    query=query,
    top_k=3,
)


print("\n" + "=" * 60)
print("QUERY")
print("=" * 60)
print(query)


print("\n" + "=" * 60)
print("TOP 3 RESULTS")
print("=" * 60)


for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print(f"Score: {result['score']:.4f}")
    print(f"File: {result['filename']}")
    print(f"Page: {result['page']}")
    print(f"Chunk: {result['chunk_index']}")
    print("Text:")
    print(result["text"])
