from typing import Dict, List

from langchain_openai import ChatOpenAI

from .qa import answer_question


def analyze_themes_and_disagreements() -> Dict[str, List[str]]:
    """
    Analyze the three expert interviews to identify:
    1. Common themes
    2. Differences/disagreements between experts

    Uses the existing QA/retrieval pipeline to gather
    evidence before asking the LLM to synthesize it.
    """

    questions = [
        "What are the main barriers to robotic surgery adoption?",
        "How important are hospital budgets and ROI when purchasing robotic surgery systems?",
        "How important are surgeon training and clinical outcomes?",
        "What is your expectation for robotic surgery adoption over the next 3–5 years?",
        "What is the typical decision-making timeline for purchasing a robotic surgery system?",
    ]

    all_evidence = []

    for question in questions:
        answer, evidence = answer_question(
            question=question,
            k=6
        )

        all_evidence.append(
            {
                "question": question,
                "answer": answer,
                "evidence": evidence,
            }
        )

    evidence_text = []

    for item in all_evidence:

        evidence_text.append(
            f"""
INTERVIEW GUIDE QUESTION:
{item["question"]}

ANSWER:
{item["answer"]}

SUPPORTING EVIDENCE:
"""
        )

        for evidence in item["evidence"]:

            evidence_text.append(
                f"""
Expert: {evidence.expert}
Market: {evidence.market}
Timestamp: {evidence.timestamp}

Quote:
{evidence.quote}
"""
            )

    combined_evidence = "\n".join(evidence_text)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = f"""
You are analyzing three expert interviews about the
European robotic surgery market.

The interviews are from:
- France
- Germany
- United Kingdom

Using ONLY the evidence provided below, identify:

1. COMMON THEMES

Identify the major themes that appear across multiple
expert interviews.

For each theme:
- Give the theme a short title.
- Explain the theme briefly.
- Mention which markets/experts support it.

2. DIFFERENCES / DISAGREEMENTS

Identify meaningful differences between the experts.

For each difference:
- Explain what differs.
- Identify the relevant markets/experts.
- Do not call something a disagreement unless the
  evidence actually shows different views.

Important rules:

- Use ONLY the provided transcript evidence.
- Do not use outside knowledge.
- Do not invent expert opinions.
- Do not invent quotes.
- Do not invent timestamps.
- Preserve the meaning of the expert statements.
- If there is no clear disagreement, say that the
  transcripts do not show a clear disagreement.
- Distinguish differences in emphasis or expectations
  from direct contradictions.

Return the result in this structure:

COMMON THEMES

1. Theme:
   Explanation:
   Experts/Markets:

2. Theme:
   Explanation:
   Experts/Markets:

DIFFERENCES / DISAGREEMENTS

1. Difference:
   Explanation:
   Experts/Markets:

2. Difference:
   Explanation:
   Experts/Markets:

SOURCE EVIDENCE:
For each important theme or difference, include the
relevant expert, market, timestamp, and exact quote.

TRANSCRIPT EVIDENCE:
{combined_evidence}
"""

    response = llm.invoke(prompt)

    return {
        "analysis": response.content,
    }