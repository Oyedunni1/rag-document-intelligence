import os
from pathlib import Path

def load_document(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    elif ext == ".txt" or ext == ".md":
        return load_txt(file_path)
    elif ext == ".csv":
        return load_csv(file_path)
    elif ext == ".html":
        return load_html(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def load_pdf(path):
    import pdfplumber
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if page_text:
                text += page_text + "\n"
    return text


def load_docx(file_path: str) -> str:
    from docx import Document
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def load_csv(file_path: str) -> str:
    import pandas as pd
    df = pd.read_csv(file_path)
    return df.to_string(index=False)


def load_html(file_path: str) -> str:
    from bs4 import BeautifulSoup
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    return soup.get_text(separator="\n").strip()