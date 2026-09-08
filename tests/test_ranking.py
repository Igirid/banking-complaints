from app.services.ranking import rank_complaints, score_complaint


def test_score_complaint_prioritizes_critical_issue():
    complaint = {
        "topic": "card_declined",
        "severity": 5,
        "sentiment": -0.9,
        "volume": 120,
        "trend": 0.28,
        "regulatory_risk": 0.9,
        "business_impact": 0.8,
    }

    score = score_complaint(complaint)

    assert score > 0.8


def test_ranked_list_is_sorted_by_priority():
    complaints = [
        {
            "topic": "low_balance_alerts",
            "severity": 2,
            "sentiment": -0.4,
            "volume": 10,
            "trend": 0.05,
            "regulatory_risk": 0.2,
            "business_impact": 0.3,
        },
        {
            "topic": "card_declined",
            "severity": 5,
            "sentiment": -0.9,
            "volume": 120,
            "trend": 0.28,
            "regulatory_risk": 0.9,
            "business_impact": 0.8,
        },
    ]

    ranked = rank_complaints(complaints)

    assert ranked[0]["topic"] == "card_declined"
    assert ranked[0]["priority_score"] >= ranked[1]["priority_score"]
