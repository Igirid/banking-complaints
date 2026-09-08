class ComplaintInsightService:
    def get_summary(self):
        return {
            "total_issues": 24,
            "critical_issues": 6,
            "avg_sentiment": -0.71,
            "alert_count": 4,
        }

    def get_trends(self):
        return {
            "period": "7d",
            "trend_points": [
                {"day": "Mon", "complaints": 32},
                {"day": "Tue", "complaints": 46},
                {"day": "Wed", "complaints": 50},
                {"day": "Thu", "complaints": 68},
                {"day": "Fri", "complaints": 72},
                {"day": "Sat", "complaints": 83},
                {"day": "Sun", "complaints": 77},
            ],
        }

    def get_top_issues(self):
        return {
            "items": [
                {"topic": "card_declined", "volume": 120, "priority_score": 0.81},
                {"topic": "app_crash", "volume": 90, "priority_score": 0.73},
                {"topic": "transfer_delay", "volume": 75, "priority_score": 0.68},
            ]
        }

    def get_alerts(self):
        return {
            "items": [
                {"id": "AL-101", "title": "Card declines spike", "severity": "high"},
                {"id": "AL-102", "title": "App crash complaints rising", "severity": "medium"},
            ]
        }
