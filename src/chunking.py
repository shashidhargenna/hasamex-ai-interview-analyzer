from typing import List

from langchain_core.documents import Document

from .models import TranscriptSegment


def create_documents(
    segments: List[TranscriptSegment],
) -> List[Document]:
    """
    Convert transcript segments into LangChain Documents
    while preserving all source metadata.
    """

    documents = []

    for segment in segments:

        metadata = {
            "segment_id": segment.segment_id,
            "call_id": segment.call_id,
            "expert": segment.expert,
            "role": segment.role,
            "market": segment.market,
            "speaker": segment.speaker,
            "start_time": segment.start_time,
            "end_time": segment.end_time,
        }

        document = Document(
            page_content=segment.text,
            metadata=metadata,
        )

        documents.append(document)

    return documents