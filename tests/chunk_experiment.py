from pathlib import Path

from docLoader import load_pdf
from chunker import chunk_pages

CHUNK_SIZES = [200, 500, 1000, 1500]
OVERLAPS = [0, 50, 100, 200]


def main():
    project_root = Path(__file__).resolve().parent
    documents_dir = project_root / "documents"

    pdf_files = sorted(documents_dir.glob("*.pdf"))

    for chunk_size in CHUNK_SIZES:
        for overlap in OVERLAPS:

            # Invalid combination
            if overlap >= chunk_size:
                continue

            total_chunks = 0

            print("\n" + "=" * 60)
            print(f"Chunk size: {chunk_size} | Overlap: {overlap}")
            print("=" * 60)

            for pdf_path in pdf_files:
                # Load PDF pages
                pages = load_pdf(str(pdf_path))

                # Add filename metadata
                for page in pages:
                    page["filename"] = pdf_path.name

                # Create chunks
                chunks = chunk_pages(
                    pages,
                    chunk_size=chunk_size,
                    overlap=overlap,
                )

                total_chunks += len(chunks)

                print(f"{pdf_path.name}: {len(chunks)} chunks")

                # Inspect Leave Policy page 2
                if pdf_path.name == "leave_policy.pdf":
                    print("\nLeave Policy - Page 2:")

                    for chunk in chunks:
                        if chunk["page"] == 2:
                            print("\n---")
                            print(
                                f"Chunk {chunk['chunk_index']} | "
                                f"{len(chunk['text'])} chars"
                            )
                            print(chunk["text"])

            print(f"\nTOTAL: {total_chunks} chunks")


if __name__ == "__main__":
    main()
