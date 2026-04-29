from fastapi import FastAPI, UploadFile, File
from app.rag_pipeline import load_and_store, get_qa_chain
from fastapi.middleware.cors import CORSMiddleware
from app.config import UPLOAD_DIR
import os, shutil

app = FastAPI(title="AskMyDoc API")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
def upload(file: UploadFile = File()):
    pdf = 

@app.post("/ask")
def ask():
    query = st.text_input("How can i help you?")
    
    chain_output = get_qa_chain(query)

    st.write(chain_output)



    



