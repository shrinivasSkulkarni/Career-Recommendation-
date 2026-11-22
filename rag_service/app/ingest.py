import hashlib

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from . import config


def get_embeddings(model_name=None):
    return HuggingFaceEmbeddings(model_name=model_name or config.EMBED_MODEL)


def get_vectorstore():
    return Chroma(
        collection_name="careerpath",
        embedding_function=get_embeddings(),
        persist_directory=config.CHROMA_DIR,
    )


def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    return splitter.split_documents(docs)


def add_chunks(chunks):
    # Same text -> same ID, so re-uploading overwrites instead of duplicating
    ids = [hashlib.md5(c.page_content.encode()).hexdigest() for c in chunks]
    get_vectorstore().add_documents(chunks, ids=ids)
    return len(chunks)


def ingest_pdf(path, doc_type="resume"):
    docs = PyPDFLoader(path).load()
    for d in docs:
        d.metadata["doc_type"] = doc_type
    return add_chunks(split_docs(docs))


def ingest_text(text, doc_type="resume", source="careerpath"):
    doc = Document(page_content=text, metadata={"doc_type": doc_type, "source": source})
    return add_chunks(split_docs([doc]))