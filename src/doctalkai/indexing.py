# =========================
# Import Libraries
# =========================

from pathlib import Path
from dotenv import load_dotenv

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from doctalkai.file_reader import read_multiple_pdfs


# =========================
# Load Environment Variables
# =========================

load_dotenv()


# =========================
# Initialize Embedding Model
# =========================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================
# Initialize Vector Store
# =========================

vector_store = InMemoryVectorStore(embeddings)


# =========================
# Define PDF File Paths
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOC_PATHS = [
    PROJECT_ROOT / "pdfs" / "climate_change.pdf",
    PROJECT_ROOT / "pdfs" / "global_warming.pdf"
]


# =========================
# Load PDF Documents
# =========================

docs = read_multiple_pdfs(DOC_PATHS)


# =========================
# Split Documents into Chunks
# =========================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

all_splits = text_splitter.split_documents(docs)

print(f"Split documentation into {len(all_splits)} chunks")


# =========================
# Index Documents into Vector Store
# =========================

vector_store.add_documents(documents=all_splits)

print(f"Indexed {len(all_splits)} chunks successfully")