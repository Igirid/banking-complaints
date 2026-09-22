from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func

from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(120), unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SourceChannel(Base):
    __tablename__ = "source_channels"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=False, default=0)
    name = Column(String(160), nullable=False)
    platform = Column(String(160), nullable=False)
    config_json = Column(Text, nullable=True)
    is_enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ComplaintIssue(Base):
    __tablename__ = "complaint_issues"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), nullable=False)
    severity = Column(Integer, nullable=False, default=0)
    sentiment = Column(Float, nullable=False, default=0.0)
    volume = Column(Integer, nullable=False, default=0)
    trend = Column(Float, nullable=False, default=0.0)
    regulatory_risk = Column(Float, nullable=False, default=0.0)
    business_impact = Column(Float, nullable=False, default=0.0)
    priority_score = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())


class SocialPost(Base):
    __tablename__ = "social_posts"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(120), nullable=False)
    source_url = Column(String(500), nullable=True)
    platform = Column(String(120), nullable=False)
    text = Column(Text, nullable=False)
    language = Column(String(30), nullable=True)
    sentiment_score = Column(Float, nullable=False, default=0.0)
    is_complaint = Column(Integer, nullable=False, default=0)
    complaint_topic = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ComplaintCluster(Base):
    __tablename__ = "complaint_clusters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    size = Column(Integer, nullable=False, default=0)
    growth_rate = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AlertRecord(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=False, default=0)
    title = Column(String(255), nullable=False)
    severity = Column(String(60), nullable=False, default="medium")
    issue_topic = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
