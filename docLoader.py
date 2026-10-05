from pathlib import Path
from pypdf import PdfReader


def load_pdf(path: str) -> list[dict]:
    reader = PdfReader(path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(
            {
                "page": page_number,
                "text": text.strip(),
            }
        )

    return pages


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    documents_dir = project_root / "documents"

    pdf_files = sorted(documents_dir.glob("*.pdf"))
    all_pages = []

    for pdf_path in pdf_files:
        print(f"\n=== Document: {pdf_path.name} ===")

        extracted_pages = load_pdf(str(pdf_path))

        for page in extracted_pages:
            page["filename"] = pdf_path.name
            all_pages.append(page)

            print(f"\n--- Page {page['page']} ---")
            print(page["text"])

        print(f"\nDocument pages: {len(extracted_pages)}")

    print(f"\nTotal PDFs: {len(pdf_files)}")
    print(f"Total pages: {len(all_pages)}")
