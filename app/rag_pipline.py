from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

def load_and_store(pdf_path: str):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)

    print("Total chunks created:", len(chunks))
    print("Sample chunk:", chunks[0].page_content[:200])  # Print the first 200 characters of the first chunk
    print("Metadata of the first chunk:", chunks[0].metadata)

    return chunks

chunks = load_and_store(r"C:\D_\projects\AskMyDoc\eyetalk conference paper (1).pdf")