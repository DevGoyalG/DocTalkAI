# =========================
# Import Libraries
# =========================

from pathlib import Path

from langchain_core.documents import Document
from pypdf import PdfReader


# =========================
# Read Single PDF File
# =========================

def read_pdf_text(pdf_path: str | Path) -> str:
    """Read and return the text content of a PDF file."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF Not Found: {path}")

    reader = PdfReader(str(path))

    text_parts = [page.extract_text() or "" for page in reader.pages]

    return "\n".join(text_parts)


# =========================
# Read Multiple PDF Files
# =========================

def read_multiple_pdfs(pdf_paths: list[str | Path]) -> list[Document]:
    """Read multiple PDFs and return a list of LangChain Documents."""

    docs: list[Document] = []

    for path in pdf_paths:
        path_obj = Path(path)

        text = read_pdf_text(path_obj)

        docs.append(
            Document(
                page_content=text,
                metadata={"source": str(path_obj)}
            )
        )

    return docs


# =========================
# Define PDF File Paths
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOC_PATHS = [
    PROJECT_ROOT / "pdfs" / "climate_change.pdf",
    PROJECT_ROOT / "pdfs" / "global_warming.pdf"
]


# =========================
# Main Execution
# =========================

if __name__ == "__main__":
    documents = read_multiple_pdfs(DOC_PATHS)

    print(f"Successfully loaded {len(documents)} PDF documents.")

    for document in documents:
        print(f"\nSource: {document.metadata['source']}")
        print(document.page_content[:500])