import streamlit as st
import os
import tempfile
import shutil
import gc
import uuid
from loader import load_document
from chunker import chunk_text
from embedder import embed_and_store
from retriever import retrieve_and_answer

st.set_page_config(
    page_title="AskMyDocs",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0e1a;
    color: #e8eaf6;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1100px; }
            
.stApp { background: #0a0e1a; }

.hero {
    padding: 3rem 0 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 2.5rem;
}
.hero-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #06d6a0;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    margin-bottom: 0.8rem;
    background: linear-gradient(135deg, #e8eaf6 0%, #4f9fff 60%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    color: rgba(232,234,246,0.45);
    font-weight: 300;
}
            
.upload-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(232,234,246,0.4);
    margin-bottom: 0.5rem;
}
            
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px dashed rgba(79,159,255,0.25) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: all 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(79,159,255,0.5) !important;
    background: rgba(79,159,255,0.04) !important;
}
            
.msg-wrap { margin-bottom: 1.5rem; }
            
.msg-you {
    background: rgba(79,159,255,0.08);
    border: 1px solid rgba(79,159,255,0.15);
    border-radius: 12px 12px 4px 12px;
    padding: 1rem 1.25rem;
    margin-left: 3rem;
    font-size: 0.95rem;
    line-height: 1.65;
}
.msg-ai {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px 12px 12px 4px;
    padding: 1rem 1.25rem;
    margin-right: 3rem;
    font-size: 0.95rem;
    line-height: 1.75;
}
.msg-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    color: rgba(232,234,246,0.35);
}
.msg-label.ai-label { color: #4f9fff; }
            
.status-pill {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    background: rgba(6,214,160,0.1);
    border: 1px solid rgba(6,214,160,0.2);
    color: #06d6a0;
    margin-bottom: 1.5rem;
}
            
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8eaf6 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(79,159,255,0.4) !important;
    box-shadow: none !important;
}
            
.stButton button {
    background: linear-gradient(135deg, #4f9fff, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.8rem !important;
    transition: opacity 0.2s !important;
}
.stButton button:hover { opacity: 0.85 !important; }
            
.custom-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 2rem 0;
}
            
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: rgba(232,234,246,0.2);
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.08em;
}
.empty-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
}
</style>
""", unsafe_allow_html=True)


# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "doc_loaded" not in st.session_state:
    st.session_state.doc_loaded = False
if "doc_name" not in st.session_state:
    st.session_state.doc_name = ""
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "input_source" not in st.session_state:
    st.session_state.input_source = ""


# --- HERO ---
st.markdown("""
<div class="hero">
    <div class="hero-tag">&#x2B21; RAG Document Intelligence</div>
    <div class="hero-title">AskMyDocs</div>
    <div class="hero-sub">Upload any document. Ask anything. Get grounded answers.</div>
</div>
""", unsafe_allow_html=True)


# --- LAYOUT ---
col1, col2 = st.columns([1, 1.8], gap="large")


# --- LEFT COLUMN: UPLOAD ---
with col1:
    st.markdown('<div class="upload-label">01 &mdash; Load your document</div>',
                unsafe_allow_html=True)

    # URL input
    url_input = st.text_input(
        "Paste a URL",
        placeholder="https://example.com/article",
        label_visibility="collapsed"
    )

    st.markdown('<div style="text-align:center; color: rgba(232,234,246,0.3); font-family: DM Mono, monospace; font-size:0.72rem; margin: 0.5rem 0;">— or —</div>',
                unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "txt", "docx", "csv", "md", "html"],
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_key}"
    )

    # Handle URL input
    if url_input and url_input != st.session_state.input_source:
        with st.spinner("Fetching and embedding URL..."):
            try:
                from loader import load_url
                text = load_url(url_input)
                if not text.strip():
                    st.error("Could not extract text from that URL.")
                else:
                    chunks = chunk_text(text)
                    embed_and_store(chunks, collection_name=st.session_state.session_id)
                    st.session_state.doc_loaded = True
                    st.session_state.doc_name = url_input
                    st.session_state.input_source = url_input
                    st.session_state.messages = []
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to load URL: {str(e)}")

    # Handle file upload
    if uploaded_file:
        file_changed = uploaded_file.name != st.session_state.doc_name
        if file_changed:
            with st.spinner("Reading and embedding your document..."):
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                text = load_document(tmp_path)
                chunks = chunk_text(text)
                embed_and_store(chunks, collection_name=st.session_state.session_id)
                os.unlink(tmp_path)

                st.session_state.doc_loaded = True
                st.session_state.doc_name = uploaded_file.name
                st.session_state.input_source = uploaded_file.name
                st.session_state.messages = []
                st.rerun()


# --- RIGHT COLUMN: CHAT ---
with col2:
    st.markdown('<div class="upload-label">03 &mdash; Chat with your document</div>',
                unsafe_allow_html=True)

    if not st.session_state.doc_loaded:
        st.markdown("""
        <div class="empty-state">
            <span class="empty-icon">&#x2B21;</span>
            Upload a document on the left<br/>to start asking questions
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-wrap">
                    <div class="msg-label">You</div>
                    <div class="msg-you">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-wrap">
                    <div class="msg-label ai-label">AskMyDocs</div>
                    <div class="msg-ai">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

        if "pending_question" in st.session_state:
            question = st.session_state.pending_question
            del st.session_state.pending_question
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner("Thinking..."):
                answer = retrieve_and_answer(question, collection_name=st.session_state.session_id)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Your question",
                placeholder="Ask anything about your document...",
                label_visibility="collapsed"
            )
            submitted = st.form_submit_button("Ask")

        if submitted and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                answer = retrieve_and_answer(user_input, collection_name=st.session_state.session_id)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
