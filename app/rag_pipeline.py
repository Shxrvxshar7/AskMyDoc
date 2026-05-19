from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP, CHROMA_DB_PATH #, GOOGLE_API_KEY
from langchain_chroma import Chroma
from app.embeddings import get_embedding_function
#from langchain_google_genai import ChatGoogleGenerativeAI  
from langchain_groq import ChatGroq
import shutil, os
from langchain_classic.chains import RetrievalQA
import chromadb
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers.ensemble import EnsembleRetriever

from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain

# Global storage for BM25
stored_chunks = []
_qa_chain = None
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

def load_and_store(pdf_path: str):

    global stored_chunks, _qa_chain
    _qa_chain = None  # reset chain on new upload

    # Clear existing ChromaDB before re-indexing
    if os.path.exists(CHROMA_DB_PATH):
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        try:
            client.delete_collection("askmydoc")
        except:
            pass

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)

    global stored_chunks
    stored_chunks = chunks

    embeddings = get_embedding_function()
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
        collection_name="askmydoc"
    )

    return len(chunks)


def get_qa_chain():

    global _qa_chain
    if _qa_chain is not None:
        return _qa_chain
    # Step 1 - load embeddings

    embeddings = get_embedding_function()
    
    # Step 2 - load existing ChromaDB

    vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, 
                         embedding_function=embeddings,
                         collection_name="askmydoc"
                         )
    
    # Step 3 - Dense retriever
    dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Step 4 - BM25 retriever
    if stored_chunks:
        bm25_retriever = BM25Retriever.from_documents(stored_chunks)
        bm25_retriever.k = 5
        retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, dense_retriever],
            weights=[0.5, 0.5]
        )
    else:
        retriever = dense_retriever  # fallback to dense only

    # Step 5 - Combine with RRF
    '''retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, dense_retriever],
        weights=[0.5, 0.5]
    )'''

    # Step 6 - initialize Gemini LLM

    """llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3)"""
    
    

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

    # Step 7 - connect into a chain
    _qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        output_key = "answer"
    )
    return _qa_chain
