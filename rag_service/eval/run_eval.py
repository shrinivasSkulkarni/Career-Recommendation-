import json, os, time, uuid, itertools
import mlflow
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.rag_chain import PROMPT, format_docs
from app import config

DOC = "eval/sample_resume.pdf"
CACHE_PATH = "eval/.answers_cache.json"
USE_LLM = os.getenv("EVAL_LLM", "0") == "1"

questions = json.load(open("eval/questions.json"))
if USE_LLM:
    questions = questions[:int(os.getenv("EVAL_MAX_Q", 15))]
embeddings = HuggingFaceEmbeddings(model_name=config.EMBED_MODEL)
mlflow.set_experiment("careerpath-rag")


def norm(s):
    return " ".join(s.lower().split())


class QuotaExhausted(Exception):
    pass


if USE_LLM:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.output_parsers import StrOutputParser
    cache = json.load(open(CACHE_PATH)) if os.path.exists(CACHE_PATH) else {}
    llm = ChatGoogleGenerativeAI(
        model=config.LLM_MODEL, temperature=0, timeout=60, max_retries=0
    )
    chain = PROMPT | llm | StrOutputParser()

    def ask(inputs):
        for attempt in (1, 2):
            try:
                return chain.invoke(inputs)
            except Exception as e:
                print(f"    attempt {attempt}/2 failed: {type(e).__name__}: {str(e)[:200]}")
                if attempt == 1:
                    time.sleep(65)
        raise QuotaExhausted()


def run(chunk_size, top_k):
    overlap = chunk_size // 6
    docs = PyPDFLoader(DOC).load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    ).split_documents(docs)
    vs = Chroma.from_documents(
        chunks, embeddings, collection_name=f"eval_{uuid.uuid4().hex}"
    )
    retriever = vs.as_retriever(search_kwargs={"k": top_k})

    n = len(questions)
    retr_hits, retr_lat, llm_hits = 0, [], 0
    for q in questions:
        t0 = time.time()
        found = retriever.invoke(q["question"])
        retr_lat.append(time.time() - t0)
        text = norm(" ".join(d.page_content for d in found))
        if all(norm(k) in text for k in q["expected_keywords"]):
            retr_hits += 1

        if USE_LLM:
            key = f"{config.LLM_MODEL}|{chunk_size}|{top_k}|{q['question']}"
            if key not in cache:
                cache[key] = ask({"context": format_docs(found),
                                  "question": q["question"]})
                json.dump(cache, open(CACHE_PATH, "w"))
                time.sleep(13)  # stay under 5 requests per minute
            if all(norm(k) in norm(cache[key]) for k in q["expected_keywords"]):
                llm_hits += 1

    metrics = {
        "retrieval_hit_rate": retr_hits / n,
        "avg_retrieval_latency_s": sum(retr_lat) / n,
        "num_chunks": len(chunks),
    }
    if USE_LLM:
        metrics["answer_accuracy"] = llm_hits / n

    with mlflow.start_run():
        mlflow.log_params({
            "chunk_size": chunk_size, "chunk_overlap": overlap, "top_k": top_k,
            "embed_model": config.EMBED_MODEL, "n_questions": n,
            "llm_eval": USE_LLM,
            "llm": config.LLM_MODEL if USE_LLM else "none",
        })
        mlflow.log_metrics(metrics)
        mlflow.log_text(PROMPT.messages[0].prompt.template, "prompt.txt")
    print(f"chunk={chunk_size} k={top_k} {metrics}")


if USE_LLM:
    # LLM mode: only the one config you name, to save quota
    grid = [(int(os.getenv("BEST_CHUNK", 600)), int(os.getenv("BEST_K", 4)))]
else:
    grid = list(itertools.product([300, 500, 800, 1200], [1, 2, 4, 6]))

for cs, k in grid:
    try:
        run(cs, k)
    except QuotaExhausted:
        print("Stopped: the API kept failing (see the error above). Progress is saved; rerun later.")
        break