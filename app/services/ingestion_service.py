from dataclasses import dataclass
from typing import Any

from app.repositories import ComplaintRepository


@dataclass
class SocialPostPayload:
    source: str
    platform: str
    text: str
    language: str = "en"
    source_url: str | None = None
    sentiment_score: float = 0.0
    is_complaint: bool = False
    complaint_topic: str | None = None


class IngestionService:
    """Ingestion service for social media complaint processing with repository support."""

    def __init__(self, repository: ComplaintRepository | None = None):
        self.repository = repository or ComplaintRepository.from_default_database()
        self._queue: list[dict[str, Any]] = []

    def ingest(self, payload: SocialPostPayload) -> dict[str, Any]:
        item = {
            "source": payload.source,
            "platform": payload.platform,
            "text": payload.text,
            "language": payload.language,
            "source_url": payload.source_url,
            "sentiment_score": payload.sentiment_score,
            "is_complaint": payload.is_complaint,
            "complaint_topic": payload.complaint_topic,
        }
        self._queue.append(item)

        stored_id = self.repository.add_social_post(
            source=payload.source,
            platform=payload.platform,
            text=payload.text,
            language=payload.language,
            source_url=payload.source_url,
            sentiment_score=payload.sentiment_score,
            is_complaint=payload.is_complaint,
            complaint_topic=payload.complaint_topic,
        )

        item["id"] = stored_id
        return {"accepted": True, "queued_items": len(self._queue), "payload": item}

    def get_queue(self) -> list[dict[str, Any]]:
        return list(self._queue)
