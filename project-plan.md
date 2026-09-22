# Banking Complaints Intelligence Platform - Production Plan

## 1. Goal

Build a production-grade backend that ingests public social media complaints about banking services, detects issue patterns using AI, ranks complaints based on a configurable business metric, and exposes monetizable APIs for enterprise clients.

## 2. Scope

This project focuses on the backend intelligence layer and operational foundation. The frontend is intentionally separate and should be built as a standalone microservice.

## 3. Architecture

### Core services

- Ingestion service
- Normalization and enrichment service
- AI classification and clustering service
- Ranking and metrics service
- Insight API service
- Alerting and reporting service
- Persistence layer

### Data flow

1. Collect public posts from X, Reddit, reviews, forums, and public complaint sources.
2. Normalize fields and detect duplicates.
3. Run complaint classification and semantic clustering.
4. Aggregate complaint topic metrics.
5. Use configurable metric weights to rank issues.
6. Serve insights through a secure REST API.
7. Store results for historical trend analysis and analyst review.

## 4. Stack

### Primary stack

- Python
- FastAPI
- MariaDB / MySQL
- Kafka or Azure Event Hubs
- OpenSearch or Elasticsearch
- Azure OpenAI or OpenAI
- LangChain
- sentence-transformers
- scikit-learn
- BERTopic
- Docker
- Kubernetes
- Terraform
- Prometheus + Grafana
- OAuth2 / JWT / Entra ID

## 5. Components to implement next

### A. Data model and migrations

- banks / tenants
- sources
- social_posts
- complaint_topics
- complaint_clusters
- complaint_issues
- alerts
- reports
- metric_configurations

### B. Ingestion layer

- polling adapters for X, Reddit, and review APIs
- message queue publisher
- retry and backoff strategy
- payload validation

### C. AI layer

- complaint vs non-complaint classifier
- sentiment scoring
- topic extraction
- cluster detection
- custom metric ranking engine

### D. Insight API

- GET /health
- POST /insights/rank
- GET /insights/trends
- GET /insights/issue-clusters
- GET /insights/alerts
- GET /insights/summary
- GET /insights/benchmark

### E. Production concerns

- tenant isolation
- rate limiting
- audit logs
- PII scrubbing
- privacy controls
- caching
- background workers
- alerting
- observability

## 6. Implementation order

1. Set up database schema and repository layer
2. Add ingestion service skeleton with message queue integration
3. Add complaint classification and topic detection service
4. Add clustering and trend aggregation service
5. Add configurable ranking service with custom metric support
6. Add insight API and authentication
7. Add alerting and operational monitoring
8. Add documentation and deployment pipeline

## 7. Key architectural principles

- Separate ingestion, processing, AI, and API layers
- Keep the frontend decoupled from backend implementation details
- Store raw data and normalized data separately
- Treat the metric engine as a configurable business rule layer
- Design for multi-tenant bank clients from day one
- Assume public social data may be noisy and incomplete

## 8. Success metrics

- Complaint detection accuracy above business threshold
- Fast ranking response time under target SLA
- Top complaint clusters identified within near-real-time windows
- Client-specific metrics can be changed without backend redeploy
- Alerts are actionable and correctly grouped by issue family

## 9. Frontend microservice contract

The frontend service must consume the backend via explicit API contracts only and should not share business logic with the backend. It will display dashboards, trend charts, rankings, and alert views for client teams.
