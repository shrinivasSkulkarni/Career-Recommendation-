from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from . import config
from .ingest import get_vectorstore

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a career assistant. Answer ONLY using the context below. "
     "If the answer is not in the context, say you don't know.\n\n"
     "Context:\n{context}"),
    ("human", "{question}"),
])


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


def answer(question, top_k=None):
    retriever = get_vectorstore().as_retriever(
        search_kwargs={"k": top_k or config.TOP_K}
    )
    docs = retriever.invoke(question)

    llm = ChatGoogleGenerativeAI(model=config.LLM_MODEL, temperature=0)
    chain = PROMPT | llm | StrOutputParser()
    text = chain.invoke({"context": format_docs(docs), "question": question})

    return {
        "answer": text,
        "sources": [
            {"text": d.page_content[:200], "metadata": d.metadata} for d in docs
        ],
    }