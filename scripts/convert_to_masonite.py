#!/usr/bin/env python3
"""
Simple converter that scaffolds a Masonite-compatible controller and routes
which import the existing business logic from the `app` package.

This script does not require Masonite to be installed to create the files.
Run it from the repository root. After Masonite is installed and a project
is created (e.g. `craft new masonite_project`), copy the generated files
into the Masonite project's `app/` and `routes/` locations.

This is an automated assist to speed migration; manual adjustments may be needed.
"""
import os
from textwrap import dedent

ROOT = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(ROOT, "masonite_project_stub")


def ensure(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def write(path: str, content: str):
    print("Writing", path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(dedent(content))


def main():
    ensure(OUT_DIR)
    controllers_dir = os.path.join(OUT_DIR, "app", "controllers")
    routes_dir = os.path.join(OUT_DIR, "routes")
    ensure(controllers_dir)
    ensure(routes_dir)

    # Controller that mirrors the FastAPI endpoints and reuses business logic
    controller_path = os.path.join(controllers_dir, "InsightController.py")
    write(
        controller_path,
        """
        from masonite.controllers import Controller
        from masonite.request import Request

        # Import existing business logic from the original FastAPI app
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
        """,
    )

    # routes/web.py mapping
    routes_path = os.path.join(routes_dir, "web.py")
    write(
        routes_path,
        """
        from masonite.routes import Route
        from app.controllers.InsightController import InsightController

        # Health
        Route.get("/health", "InsightController@health")

        # Ingestion
        Route.post("/ingest/social-post", "InsightController@ingest_social_post")

        # Insights
        Route.post("/insights/rank", "InsightController@rank_complaints")
        Route.get("/insights/demo", "InsightController@demo_insights")
        Route.get("/insights/summary", "InsightController@summary")
        Route.get("/insights/trends", "InsightController@trends")
        Route.get("/insights/issues", "InsightController@issues")
        Route.get("/insights/issue-clusters", "InsightController@issue_clusters")
        Route.get("/insights/alerts", "InsightController@alerts")
        """,
    )

    print("Masonite project stub created at:", OUT_DIR)


if __name__ == "__main__":
    main()
