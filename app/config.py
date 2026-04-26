import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DB_PATH = "./chroma_db"
UPLOAD_DIR = "./uploads"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200