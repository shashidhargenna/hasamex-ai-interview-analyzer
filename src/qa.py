from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

from .models import Evidence
from .retrieval import retrieve_documents


def build_context(documents: List[Document]) -> str:
    """
    Convert retrieved transcript documents into a context
    that can be provided to the LLM.
    """

    context_parts = []

    for document in documents:
        metadata = document.metadata

        context_parts.append(
            f"""
Expert: {metadata['expert']}
Market: {metadata['market']}
Speaker: {metadata['speaker']}
Timestamp: {metadata['start_time']} - {metadata['end_time']}

Transcript:
{document.page_content}
"""
        )

    return "\n---\n".join(context_parts)


def build_evidence(documents: List[Document]) -> List[Evidence]:
    """
    Convert retrieved transcript documents into structured evidence.
    """

    evidence = []

    for document in documents:
        metadata = document.metadata

        evidence.append(
            Evidence(
                expert=metadata["expert"],
                market=metadata["market"],
                timestamp=(
                    f"{metadata['start_time']} - "
                    f"{metadata['end_time']}"
                ),
                quote=document.page_content,
                segment_id=metadata["segment_id"],
                score=0.0,
            )
        )

    return evidence


def answer_question(
    question: str,
    k: int = 6
):
    """
    Answer a question using retrieved transcript evidence.

    Returns:
        answer: LLM-generated answer
        evidence: Structured evidence from the original transcripts
    """

    # Step 1: Retrieve relevant expert transcript segments
    documents = retrieve_documents(
        query=question,
        k=k
    )

    # Step 2: Build context for the LLM
    context = build_context(documents)

    # Step 3: Create the LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # Step 4: Create the grounded prompt
    prompt = f"""
You are analyzing expert interviews about the European
robotic surgery market.

Answer the user's question using ONLY the transcript
evidence provided below.

Do not use outside knowledge.

If the evidence does not contain enough information to
answer the question, say that the transcripts do not
provide enough information.

Synthesize the views across experts when appropriate.

Do not invent:
- facts
- expert opinions
- quotes
- timestamps
- numbers

USER QUESTION:
{question}

TRANSCRIPT EVIDENCE:
{context}

Provide a concise, factual answer.
"""

    # Step 5: Generate the answer
    response = llm.invoke(prompt)

    # Step 6: Convert retrieved documents into structured evidence
    evidence = build_evidence(documents)

    # Step 7: Return answer + evidence
    return response.content, evidence