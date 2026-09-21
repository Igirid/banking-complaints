from masonite.controllers import Controller
from masonite.request import Request

from app.services.ranking import rank_complaints
from app.services.ai_pipeline import ComplaintAIService
from app.services.ingestion_service import IngestionService, SocialPostPayload
from app.services.complaint_service import ComplaintInsightService
from app.repositories import ComplaintRepository


class InsightController(Controller):
    def __init__(self):
        self.ai_service = ComplaintAIService()
        self.repo = ComplaintRepository.from_default_database()
        self.ingestion = IngestionService(repository=self.repo)
        self.service = ComplaintInsightService()

    def health(self, request: Request):
        return {"status": "ok"}

    def ingest_social_post(self, request: Request):
        payload = request.json or {}
        complaint_text = payload.get("text", "")
        classification = self.ai_service.classify_complaint(complaint_text)
        normalized = {
            "source": payload.get("source", "unknown"),
            "platform": payload.get("platform", "unknown"),
            "text": complaint_text,
            "language": payload.get("language", "en"),
            "source_url": payload.get("source_url"),
            "sentiment_score": float(payload.get("sentiment_score", 0.0)),
            "is_complaint": bool(classification.get("is_complaint", False)),
            "complaint_topic": payload.get("complaint_topic") or classification.get("topic"),
        }
        item = SocialPostPayload(**normalized)
        return self.ingestion.ingest(item)

    def rank_complaints(self, request: Request):
        payload = request.json or {}
        complaints = payload.get("complaints", [])
        metric_weights = payload.get("metric_weights")
        return {"items": rank_complaints(complaints, metric_weights)}

    def demo_insights(self, request: Request):
        complaints = [
            {
                "topic": "card_declined",
                "severity": 5,
                "sentiment": -0.9,
                "volume": 120,
                "trend": 0.28,
                "regulatory_risk": 0.9,
                "business_impact": 0.8,
            },
            {
                "topic": "app_crash",
                "severity": 4,
                "sentiment": -0.7,
                "volume": 90,
                "trend": 0.19,
                "regulatory_risk": 0.4,
                "business_impact": 0.7,
            },
        ]
        return {"items": rank_complaints(complaints)}

    def summary(self, request: Request):
        return self.service.get_summary()

    def trends(self, request: Request):
        return self.service.get_trends()

    def issues(self, request: Request):
        return self.service.get_top_issues()

    def issue_clusters(self, request: Request):
        return {"items": self.repo.summarize_issues()["items"]}

    def alerts(self, request: Request):
        return {"items": self.repo.summarize_alerts()["items"]}
