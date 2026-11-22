import shutil
import tempfile
from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel
from .ingest import ingest_pdf, ingest_text
from .rag_chain import answer

app = FastAPI(title="CareerPath RAG Service")


class AskRequest(BaseModel):
    question: str
    top_k: int | None = None


class TextIn(BaseModel):
    text: str
    doc_type: str = "resume"
    source: str = "careerpath"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile = File(...), doc_type: str = Form("resume")):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
    return {"chunks_added": ingest_pdf(tmp.name, doc_type)}


@app.post("/ingest-text")
def ingest_text_endpoint(body: TextIn):
    return {"chunks_added": ingest_text(body.text, body.doc_type, body.source)}


@app.post("/ask")
def ask(req: AskRequest):
    return answer(req.question, req.top_k)