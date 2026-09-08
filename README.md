# Banking Complaints Intelligence Platform

This starter project contains a working foundation for a system that tracks social media complaints about banking platforms and ranks them using a user-defined priority metric.

## Included pieces

- Complaint scoring engine
- API endpoint for ranked insights
- Demo endpoint for sample data
- Basic tests covering the ranking logic
- MySQL/MariaDB-oriented architecture guidance for the production system

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.api:app --reload
```

## Example API call

```bash
curl -X POST http://localhost:8000/insights/rank \
  -H "Content-Type: application/json" \
  -d '{
    "complaints": [
      {"topic": "card_declined", "severity": 5, "sentiment": -0.9, "volume": 120, "trend": 0.28, "regulatory_risk": 0.9, "business_impact": 0.8},
      {"topic": "app_crash", "severity": 4, "sentiment": -0.7, "volume": 90, "trend": 0.19, "regulatory_risk": 0.4, "business_impact": 0.7}
    ]
  }'
```

## Next steps

- Add real data ingestion from Twitter/Reddit/other channels
- Add complaint detection and clustering with AI
- Add storage, dashboards, and user auth
- Add delayed jobs for recurring analysis
