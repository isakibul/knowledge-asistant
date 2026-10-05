from pathlib import Path

from docLoader import load_pdf


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[dict]:
    all_chunks = []

    for page in pages:
        text_chunks = chunk_text(
            page["text"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk_index, text_chunk in enumerate(text_chunks):
            all_chunks.append(
                {
                    "text": text_chunk.strip(),
                    "page": page["page"],
                    "chunk_index": chunk_index,
                    "filename": page["filename"],
                }
            )

    return all_chunks


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    documents_dir = project_root / "documents"

    pdf_files = sorted(documents_dir.glob("*.pdf"))

    all_chunks = []

    for pdf_path in pdf_files:
        print(f"\n{'=' * 60}")
        print(f"Document: {pdf_path.name}")
        print("=" * 60)

        # Extract PDF pages
        pages = load_pdf(str(pdf_path))

        # Add filename metadata
        for page in pages:
            page["filename"] = pdf_path.name

        # Chunk extracted pages
        chunks = chunk_pages(
            pages,
            chunk_size=500,
            overlap=100,
        )

        all_chunks.extend(chunks)

        # Print first 5 chunks from this PDF
        for chunk in chunks[:5]:
            print("\n------------------------------")
            print(f"File: {chunk['filename']}")
            print(f"Page: {chunk['page']}")
            print(f"Chunk: {chunk['chunk_index']}")
            print("------------------------------")
            print(chunk["text"])

        print(f"\nDocument pages: {len(pages)}")
        print(f"Document chunks: {len(chunks)}")

    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    print(f"Total PDFs: {len(pdf_files)}")
    print(f"Total chunks: {len(all_chunks)}")
