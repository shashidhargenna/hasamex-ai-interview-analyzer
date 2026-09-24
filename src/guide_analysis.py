from typing import List, Dict

from .qa import answer_question


def get_interview_questions() -> List[str]:
    """
    Return the six questions from the Hasamex interview guide.
    """

    return [
        "How would you describe robotic surgery adoption in the market today?",
        "What are the main barriers to robotic surgery adoption?",
        "How important are hospital budgets and ROI when purchasing robotic surgery systems?",
        "How important are surgeon training and clinical outcomes?",
        "What is your expectation for robotic surgery adoption over the next 3–5 years?",
        "What is the typical decision-making timeline for purchasing a robotic surgery system?",
    ]


def analyze_interview_guide() -> List[Dict]:
    """
    Answer every question in the interview guide using
    the transcript RAG pipeline.
    """

    questions = get_interview_questions()

    results = []

    for question in questions:

        answer, evidence = answer_question(
            question=question,
            k=6
        )

        results.append(
            {
                "question": question,
                "answer": answer,
                "evidence": evidence,
            }
        )

    return results