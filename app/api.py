from fastapi import FastAPI

from app.repositories import ComplaintRepository
from app.services.ai_pipeline import ComplaintAIService
from app.services.complaint_service import ComplaintInsightService
from app.services.ingestion_service import IngestionService, SocialPostPayload
from app.services.ranking import rank_complaints

app = FastAPI(title="Banking Complaints Insight API")
service = ComplaintInsightService()
issue_repository = ComplaintRepository.from_default_database()
ingestion_service = IngestionService(repository=issue_repository)
ai_service = ComplaintAIService()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest/social-post")
def ingest_social_post(payload: dict):
    complaint_text = payload.get("text", "")
    classification = ai_service.classify_complaint(complaint_text)
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
    return ingestion_service.ingest(item)


@app.post("/insights/rank")
def rank_complaints_api(payload: dict):
    complaints = payload.get("complaints", [])
    metric_weights = payload.get("metric_weights")
    return {"items": rank_complaints(complaints, metric_weights)}


@app.get("/insights/demo")
def demo_insights():
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


@app.get("/insights/summary")
def insight_summary():
    return service.get_summary()


@app.get("/insights/trends")
def trend_insights():
    return service.get_trends()


@app.get("/insights/issues")
def issue_insights():
    return service.get_top_issues()


@app.get("/insights/issue-clusters")
def issue_cluster_insights():
    summary = issue_repository.summarize_issues()
    return {"items": summary["items"]}


@app.get("/insights/alerts")
def alert_insights():
    summary = issue_repository.summarize_alerts()
    return {"items": summary["items"]}
