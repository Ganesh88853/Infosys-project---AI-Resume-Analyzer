import os
import logging
from typing import Tuple

from PyPDF2 import PdfReader
from docx import Document

from utils.database import (
    save_resume_for_user,
    get_latest_resume_for_user,
    delete_latest_resume_for_user,
)

# ------------ Logging Setup ------------

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "resume_parser.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


# ------------ Helpers for Cleaning ------------

def _clean_text(text: str) -> str:
    """
    Clean extracted text:
    - Normalize line breaks
    - Strip extra spaces
    """
    if not text:
        return ""

    # Replace Windows line endings and normalize
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove extra blank lines
    lines = [ln.strip() for ln in text.split("\n")]
    lines = [ln for ln in lines if ln]  # remove empty lines
    return "\n".join(lines)


# ------------ Extraction for PDF ------------

def extract_text_from_pdf(file_obj) -> Tuple[bool, str]:
    """
    Extract text from PDF using PyPDF2.
    Returns (success, text_or_error_message)
    """
    try:
        # ensure pointer at start
        file_obj.seek(0)
        reader = PdfReader(file_obj)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

        if not text.strip():
            msg = "No extractable text found in PDF. It might be image-based (scanned)."
            logging.warning(msg)
            return False, msg

        cleaned = _clean_text(text)
        logging.info("PDF text extraction successful.")
        return True, cleaned

    except Exception as e:
        msg = f"Error while extracting PDF text: {e}"
        logging.exception(msg)
        return False, msg


# ------------ Extraction for DOCX ------------

def extract_text_from_docx(file_obj) -> Tuple[bool, str]:
    """
    Extract text from DOCX using python-docx.
    Returns (success, text_or_error_message)
    """
    try:
        file_obj.seek(0)
        doc = Document(file_obj)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        text = "\n".join(paragraphs)

        if not text.strip():
            msg = "No text found in DOCX file."
            logging.warning(msg)
            return False, msg

        cleaned = _clean_text(text)
        logging.info("DOCX text extraction successful.")
        return True, cleaned

    except Exception as e:
        msg = f"Error while extracting DOCX text: {e}"
        logging.exception(msg)
        return False, msg


# ------------ Unified Extraction ------------

def extract_resume_text(uploaded_file) -> Tuple[bool, str]:
    """
    Detect file type and extract text accordingly.
    uploaded_file is Streamlit's UploadedFile (or similar file-like object).

    Returns (success, text_or_error_message)
    """
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    else:
        msg = "Unsupported file type. Please upload a PDF or DOCX file."
        logging.warning(msg)
        return False, msg


# ------------ Extract + Save to DB ------------

def extract_and_save_resume(user_id: int, uploaded_file) -> Tuple[bool, str]:
    """
    High-level function for dashboard:
    - Detect file type
    - Extract text
    - Clean it
    - Save in DB linked with user_id

    Returns (success, message_for_ui)
    """
    ok, result = extract_resume_text(uploaded_file)
    if not ok:
        # result is an error message
        return False, result

    extracted_text = result  # already cleaned
    file_name = uploaded_file.name

    db_ok, db_msg = save_resume_for_user(
        user_id=user_id,
        file_name=file_name,
        extracted_text=extracted_text,
    )

    if db_ok:
        logging.info(f"Resume saved to DB for user_id={user_id}, file={file_name}")
        return True, "Resume uploaded and text extracted successfully."
    else:
        logging.error(f"Failed saving resume for user_id={user_id}: {db_msg}")
        return False, db_msg


# Re-export these DB helpers so frontend can import from resume_parser if desired
__all__ = [
    "extract_and_save_resume",
    "extract_resume_text",
    "extract_text_from_pdf",
    "extract_text_from_docx",
    "get_latest_resume_for_user",
    "delete_latest_resume_for_user",
]
