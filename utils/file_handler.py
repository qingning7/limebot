import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from utils.logger_handler import logger


def get_file_md5_hex(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"file not found: {filepath}")
        return None

    if not os.path.isfile(filepath):
        logger.error(f"path is not a file: {filepath}")
        return None

    md5_hash = hashlib.md5()

    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                md5_hash.update(chunk)

        return md5_hash.hexdigest()
    except Exception as exc:
        logger.error(f"failed to calc md5 for {filepath}: {exc}")
        return None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    files: list[str] = []

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]directory not found: {path}")
        return tuple(files)

    for filename in os.listdir(path):
        if filename.endswith(allowed_types):
            files.append(os.path.join(path, filename))

    return tuple(files)


def pdf_loader(filepath: str, password=None) -> list[Document]:
    return PyPDFLoader(filepath, password).load()


def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()
