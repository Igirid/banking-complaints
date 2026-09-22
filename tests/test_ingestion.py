from fastapi.testclient import TestClient

from app.api import app
from app.repositories import ComplaintRepository
from app.services.ai_pipeline import ComplaintAIService
from app.services.ingestion_service import IngestionService, SocialPostPayload


def test_ingestion_service_accepts_payload_and_tracks_queue():
    service = IngestionService()
    payload = SocialPostPayload(
        source="x",
        platform="twitter",
        text="My card was declined and I cannot transfer money",
        language="en",
        source_url="https://x.com/example",
        sentiment_score=-0.9,
        is_complaint=True,
        complaint_topic="card_declined",
    )

    result = service.ingest(payload)

    assert result["accepted"] is True
    assert result["queued_items"] == 1
    assert service.get_queue()[0]["platform"] == "twitter"
    assert service.get_queue()[0]["complaint_topic"] == "card_declined"


def test_repository_persists_social_post_records():
    repo = ComplaintRepository.from_memory_database()
    source_id = repo.add_social_post(
        source="reddit",
        platform="reddit",
        text="My bank app froze after transfer",
        language="en",
        source_url="https://reddit.com/r/bankingscams",
        sentiment_score=-0.8,
        is_complaint=True,
        complaint_topic="app_freeze",
    )

    posts = repo.list_social_posts(limit=10)
    assert source_id is not None
    assert len(posts) == 1
    assert posts[0].platform == "reddit"
    assert posts[0].complaint_topic == "app_freeze"


def test_ai_service_detects_bank_complaint_topic():
    service = ComplaintAIService()
    result = service.classify_complaint(
        "My card was declined and the app froze after I tried to transfer money")

    assert result["is_complaint"] is True
    assert result["topic"] in {"card_declined", "transfer_delay", "app_freeze"}


def test_ingest_endpoint_accepts_social_post():
    client = TestClient(app)
    response = client.post(
        "/ingest/social-post",
        json={
            "source": "x",
            "platform": "twitter",
            "text": "My account balance is wrong and I cannot access my money",
            "language": "en",
            "source_url": "https://x.com/example",
            "sentiment_score": -0.9,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["accepted"] is True
    assert payload["payload"]["platform"] == "twitter"
    assert payload["payload"]["is_complaint"] is True


def test_repository_tracks_issue_summary_and_clusters():
    repo = ComplaintRepository.from_memory_database()
    repo.add_issue(
        topic="card_declined",
        severity=5,
        sentiment=-0.9,
        volume=25,
        trend=0.28,
        regulatory_risk=0.9,
        business_impact=0.8,
        priority_score=0.91,
    )
    repo.add_issue(
        topic="card_declined",
        severity=4,
        sentiment=-0.8,
        volume=18,
        trend=0.19,
        regulatory_risk=0.7,
        business_impact=0.7,
        priority_score=0.81,
    )

    issues = repo.list_issues(limit=20)
    summary = repo.summarize_issues()

    assert len(issues) == 2
    assert summary["top_topic"] == "card_declined"
    assert summary["total_volume"] == 43


def test_clustered_issue_endpoint_returns_topic_summary():
    client = TestClient(app)
    response = client.get("/insights/issue-clusters")

    assert response.status_code == 200
    payload = response.json()
    assert "items" in payload
    assert isinstance(payload["items"], list)


def test_repository_tracks_alerts_and_sources():
    repo = ComplaintRepository.from_memory_database()
    repo.add_alert(
        tenant_id=1,
        title="Card declines spike",
        severity="high",
        issue_topic="card_declined",
    )
    repo.add_alert(
        tenant_id=1,
        title="App freezes rising",
        severity="medium",
        issue_topic="app_freeze",
    )

    alerts = repo.list_alerts(limit=10)
    summary = repo.summarize_alerts()

    assert len(alerts) == 2
    assert summary["high_alert_count"] == 1
    assert summary["total_alerts"] == 2


def test_alerts_endpoint_uses_repository_data():
    client = TestClient(app)
    response = client.get("/insights/alerts")

    assert response.status_code == 200
    payload = response.json()
    assert "items" in payload
    assert isinstance(payload["items"], list)
