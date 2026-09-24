import re
from pathlib import Path
from typing import List

from .models import TranscriptSegment


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def parse_timestamp(timestamp: str) -> int:
    """
    Convert MM:SS into total seconds.
    """

    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + int(seconds)


def format_timestamp(total_seconds: int) -> str:
    """
    Convert total seconds back to MM:SS.
    """

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes:02d}:{seconds:02d}"


def get_transcript_metadata(file_path: Path):
    """
    Extract expert, role and market from transcript header.
    """

    text = file_path.read_text(encoding="utf-8")

    expert_match = re.search(
        r"Expert\s+\d+\s+[–-]\s*(.+)",
        text
    )

    role_match = re.search(
        r"Role:\s*(.+)",
        text
    )

    market_match = re.search(
        r"Market:\s*(.+)",
        text
    )

    expert = expert_match.group(1).strip() if expert_match else "Unknown"
    role = role_match.group(1).strip() if role_match else "Unknown"
    market = market_match.group(1).strip() if market_match else "Unknown"

    return expert, role, market, text


def parse_transcript(file_path: Path) -> List[TranscriptSegment]:
    """
    Parse one transcript into timestamped speaker segments.
    """

    expert, role, market, text = get_transcript_metadata(file_path)

    call_id = file_path.stem

    # Find timestamp positions.
    timestamp_pattern = re.compile(
        r"(?m)^(\d{2}:\d{2})\s*$"
    )

    matches = list(timestamp_pattern.finditer(text))

    segments = []

    for index, match in enumerate(matches):

        start_time = match.group(1)

        content_start = match.end()

        if index + 1 < len(matches):
            content_end = matches[index + 1].start()
        else:
            content_end = len(text)

        block = text[content_start:content_end].strip()

        if not block:
            continue

        # Extract speaker.
        speaker_match = re.match(
            r"([^:]+):\s*(.*)",
            block,
            re.DOTALL
        )

        if speaker_match:
            speaker = speaker_match.group(1).strip()
            segment_text = speaker_match.group(2).strip()
        else:
            speaker = "Unknown"
            segment_text = block

        # End time is the next timestamp.
        if index + 1 < len(matches):
            end_time = matches[index + 1].group(1)
        else:
            end_time = start_time

        segment_id = f"{call_id}_{index:03d}"

        segment = TranscriptSegment(
            segment_id=segment_id,
            call_id=call_id,
            expert=expert,
            role=role,
            market=market,
            speaker=speaker,
            start_time=start_time,
            end_time=end_time,
            text=segment_text,
        )

        segments.append(segment)

    return segments


def load_all_transcripts() -> List[TranscriptSegment]:
    """
    Load all transcript files from the data directory.
    """

    transcript_files = sorted(
        DATA_DIR.glob("Transcript_*.txt")
    )

    all_segments = []

    for file_path in transcript_files:
        segments = parse_transcript(file_path)
        all_segments.extend(segments)

    return all_segments