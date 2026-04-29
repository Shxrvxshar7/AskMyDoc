from fastapi import FastAPI, UploadFile, File
from app.rag_pipeline import load_and_store, get_qa_chain
from fastapi.middleware.cors import CORSMiddleware
from app.config import UPLOAD_DIR
import os, shutil
from pydantic import BaseModel



app = FastAPI(title="AskMyDoc API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb")as f:
        shutil.copyfileobj(file.file, f)
    chunk_count = load_and_store(path)
    return {"message": f"{file.filename} indexed sucessfully", "chunks": chunk_count}

class AskRequest(BaseModel):
    question: str
    
@app.post("/ask")
async def ask(request: AskRequest):
    question = request.question
    chain = get_qa_chain()
    result = chain.invoke({"query": question})
    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result["source_documents"]]
    }



    



