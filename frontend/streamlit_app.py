import streamlit as st
import requests
from pathlib import Path

# --- Page Config ---
st.set_page_config(
    page_title="AskMyDoc",
    page_icon="📄",
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    html, body, [class*="css"] {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }

    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem 0 1rem 0;
        animation: fadeInDown 1s ease;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .logo-title {
        font-family: 'Press Start 2P', monospace;
        font-size: 2rem;
        color: #00c9b1;
        margin-top: 1rem;
        letter-spacing: 4px;
        text-shadow: 0 0 20px #00c9b133;
    }

    .logo-subtitle {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.5rem;
        color: #4a9aba;
        margin-top: 0.5rem;
        letter-spacing: 3px;
    }

    .upload-box {
        background: #111827;
        border: 2px solid #00c9b133;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .answer-box {
        background: #0f2a45;
        border-left: 4px solid #00c9b1;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #e0f7f4;
    }

    .source-tag {
        display: inline-block;
        background: #00c9b122;
        border: 1px solid #00c9b155;
        color: #00c9b1;
        border-radius: 4px;
        padding: 2px 10px;
        font-size: 0.75rem;
        margin: 3px;
    }

    .stButton > button {
        background-color: #00c9b1;
        color: #0a0a0a;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        width: 100%;
        font-size: 1rem;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        background-color: #00a896;
        transform: scale(1.02);
    }

    .stTextInput > div > div > input {
        background-color: #111827;
        color: #e0e0e0;
        border: 1px solid #00c9b155;
        border-radius: 8px;
    }

    .success-msg {
        background: #00c9b122;
        border: 1px solid #00c9b1;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        color: #00c9b1;
        font-size: 0.9rem;
    }

    div[data-testid="stFileUploader"] {
        background: #111827;
        border: 2px dashed #00c9b155;
        border-radius: 12px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Logo & Header ---
logo_path = Path("assets/Logo.jpeg")
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
if logo_path.exists():
    st.image(str(logo_path), width=160)
st.markdown("""
    <div class="logo-title">ASKMYDOC</div>
    <div class="logo-subtitle">RAG · GEMINI · LANGCHAIN</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- Upload Section ---
st.markdown("### 📂 Upload your document")
uploaded_file = st.file_uploader("Drop your PDF here", type=["pdf"], label_visibility="collapsed")

if uploaded_file:
    if "uploaded_file_name" not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
        with st.spinner("🔄 Indexing your document..."):
            response = requests.post(
                "http://localhost:8000/upload",
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            )
        if response.status_code == 200:
            st.session_state.uploaded_file_name = uploaded_file.name
            data = response.json()
            st.markdown(f"""
                <div class="success-msg">
                    ✅ <b>{uploaded_file.name}</b> indexed successfully — 
                    <b>{data.get('chunks', '?')}</b> chunks stored in ChromaDB
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Upload failed. Is the FastAPI server running?")

    if st.session_state.get("uploaded_file_name"):
        st.divider()
        st.markdown("### 💬 Ask a question")
        question = st.text_input("", placeholder="What is this document about?", label_visibility="collapsed")

        if st.button("Ask") and question:
            with st.spinner("🤔 Thinking..."):
                ask_response = requests.post(
                    "http://localhost:8000/ask",
                    json={"question": question}
                )
            if ask_response.status_code == 200:
                result = ask_response.json()
                st.markdown("#### 🧠 Answer")
                st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)

                with st.expander("📄 Source chunks used"):
                    for i, source in enumerate(result["sources"]):
                        page = source.get("page", "?")
                        src = source.get("source", "unknown")
                        st.markdown(f"""
                            <span class="source-tag">Chunk {i+1}</span>
                            <span class="source-tag">Page {page}</span>
                            <span class="source-tag">{Path(src).name}</span>
                        """, unsafe_allow_html=True)
            else:
                st.error("Something went wrong with the question.")