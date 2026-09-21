from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.models import ComplaintIssue, SocialPost, AlertRecord, Base, engine


@dataclass
class RepositoryResult:
    success: bool
    item_id: int | None = None
    error: str | None = None


class ComplaintRepository:
    def __init__(self, session: Session | None = None):
        self.session = session

    @classmethod
    def from_default_database(cls):
        Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        return cls(session=session)

    @classmethod
    def from_memory_database(cls):
        test_engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            future=True,
        )
        Base.metadata.create_all(bind=test_engine)
        return cls(session=Session(bind=test_engine))

    def add_social_post(self, *, source, platform, text, language='en', source_url=None, sentiment_score=0.0, is_complaint=False, complaint_topic=None):
        post = SocialPost(
            source=source,
            platform=platform,
            text=text,
            language=language,
            source_url=source_url,
            sentiment_score=sentiment_score,
            is_complaint=1 if is_complaint else 0,
            complaint_topic=complaint_topic,
        )
        if self.session is None:
            return None
        self.session.add(post)
        self.session.commit()
        return post.id

    def list_social_posts(self, *, limit=100):
        if self.session is None:
            return []
        return self.session.query(SocialPost).order_by(SocialPost.id.desc()).limit(limit).all()

    def add_issue(self, * , topic, severity, sentiment, volume, trend, regulatory_risk, business_impact, priority_score):
        if self.session is None:
            return RepositoryResult(success=False, error='No database session configured')
        issue = ComplaintIssue(
            topic=topic,
            severity=severity,
            sentiment=sentiment,
            volume=volume,
            trend=trend,
            regulatory_risk=regulatory_risk,
            business_impact=business_impact,
            priority_score=priority_score,
        )
        self.session.add(issue)
        self.session.commit()
        return RepositoryResult(success=True, item_id=issue.id)

    def list_issues(self, *, limit=100):
        if self.session is None:
            return []
        return self.session.query(ComplaintIssue).order_by(ComplaintIssue.priority_score.desc()).limit(limit).all()

    def summarize_issues(self):
        issues = self.list_issues(limit=500)
        if not issues:
            return {"top_topic": None, "total_volume": 0, "issue_count": 0, "items": []}
        topics = {}
        for issue in issues:
            bucket = topics.setdefault(issue.topic, {"topic": issue.topic, "volume": 0, "priority_score": 0.0, "count": 0})
            bucket["volume"] += int(issue.volume)
            bucket["priority_score"] = max(bucket["priority_score"], float(issue.priority_score))
            bucket["count"] += 1
        ordered = sorted(topics.values(), key=lambda item: (item["volume"], item["priority_score"]), reverse=True)
        top_topic = ordered[0]["topic"] if ordered else None
        total_volume = sum(item["volume"] for item in ordered)
        return {"top_topic": top_topic, "total_volume": total_volume, "issue_count": len(ordered), "items": ordered}

    def add_alert(self, *, tenant_id, title, severity, issue_topic=None):
        if self.session is None:
            return RepositoryResult(success=False, error='No database session configured')
        alert = AlertRecord(
            tenant_id=tenant_id,
            title=title,
            severity=severity.lower(),
            issue_topic=issue_topic,
            is_active=True,
        )
        self.session.add(alert)
        self.session.commit()
        return RepositoryResult(success=True, item_id=alert.id)

    def list_alerts(self, *, limit=100):
        if self.session is None:
            return []
        return self.session.query(AlertRecord).order_by(AlertRecord.created_at.desc()).limit(limit).all()

    def summarize_alerts(self):
        alerts = self.list_alerts(limit=500)
        high_alert_count = sum(1 for alert in alerts if alert.severity.lower() == 'high')
        return {"total_alerts": len(alerts), "high_alert_count": high_alert_count, "items": [{"id": alert.id, "title": alert.title, "severity": alert.severity, "issue_topic": alert.issue_topic, "tenant_id": alert.tenant_id} for alert in alerts]}
