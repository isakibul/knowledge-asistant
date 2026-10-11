from pathlib import Path

from docLoader import load_pdf
from chunker import chunk_pages
from embedder import generate_embeddings
from db import insert_chunks

project_root = Path(__file__).resolve().parent
documents_dir = project_root / "documents"

pdf_files = sorted(documents_dir.glob("*.pdf"))

all_chunks = []

# PDF → Pages → Chunks
for pdf_path in pdf_files:
    print(f"Processing: {pdf_path.name}")

    pages = load_pdf(str(pdf_path))

    for page in pages:
        page["filename"] = pdf_path.name

    chunks = chunk_pages(
        pages,
        chunk_size=500,
        overlap=100,
    )

    all_chunks.extend(chunks)


# Chunks → Embeddings
embedded_chunks = generate_embeddings(all_chunks)


# Save → PostgreSQL
insert_chunks(embedded_chunks)


print("\nIngestion complete!")
print("Total PDFs:", len(pdf_files))
print("Total chunks:", len(embedded_chunks))
