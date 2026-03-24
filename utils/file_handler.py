import hashlib
import os
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def get_file_md5_hex(filepath: str):
    
    if not os.path.exists(filepath):
        logger.error(f"文件不存在: {filepath}")
        return None
    
    if not os.path.isfile(filepath):
        logger.error(f"路径不是一个文件: {filepath}")
        return None
    
    md5_hash = hashlib.md5()

    chunk_size = 4096
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_hash.update(chunk)

        return md5_hash.hexdigest()
    
    except Exception as e:
        logger.error(f"计算文件{filepath}的MD5失败: {e}")
        return None

def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    files = []

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_types
    
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f))

    return tuple(files)

def pdf_loader(filepath: str,password=None) -> list[Document]:
    return PyPDFLoader(filepath, password).load()

def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath).load()