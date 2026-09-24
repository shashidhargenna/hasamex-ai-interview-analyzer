from dataclasses import dataclass, field
from typing import List


@dataclass
class TranscriptSegment:
    """
    Represents one timestamped segment from an expert interview.
    """

    segment_id: str
    call_id: str
    expert: str
    role: str
    market: str
    speaker: str
    start_time: str
    end_time: str
    text: str

    metadata: dict = field(default_factory=dict)


@dataclass
class RetrievedSegment:
    """
    Represents a transcript segment returned by retrieval.
    """

    segment: TranscriptSegment
    score: float


@dataclass
class Evidence:
    """
    Evidence used to support an AI-generated answer.
    """

    expert: str
    market: str
    timestamp: str
    quote: str
    segment_id: str
    score: float


@dataclass
class AnalysisResult:
    """
    Structured result returned by the analysis layer.
    """

    answer: str
    evidence: List[Evidence]