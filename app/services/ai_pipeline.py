from __future__ import annotations

from typing import Any


class ComplaintAIService:
    """Production-oriented AI service scaffold for complaint classification and clustering.

    This module is intentionally lightweight for the current prototype but structured so
    it can later integrate with OpenAI, LangChain, BERTopic, or a custom classifier.
    """

    def classify_complaint(self, text: str) -> dict[str, Any]:
        normalized = text.lower().strip()
        complaint_keywords = [
            "declined",
            "unable",
            "broken",
            "error",
            "fraud",
            "slow",
            "delay",
            "cannot",
            "blocked",
            "freeze",
            "charge",
            "lost",
            "wrong",
            "access",
            "balance",
            "transfer",
        ]

        is_complaint = any(keyword in normalized for keyword in complaint_keywords)

        if not is_complaint:
            return {
                "is_complaint": False,
                "confidence": 0.76,
                "label": "neutral",
                "topic": "neutral",
            }

        if "declined" in normalized or "card" in normalized:
            topic = "card_declined"
        elif "freeze" in normalized or "frozen" in normalized or "app" in normalized:
            topic = "app_freeze"
        elif "transfer" in normalized or "delay" in normalized:
            topic = "transfer_delay"
        elif "balance" in normalized or "wrong" in normalized:
            topic = "account_balance"
        else:
            topic = "service_issue"

        return {
            "is_complaint": True,
            "confidence": 0.92,
            "label": "complaint",
            "topic": topic,
        }

    def cluster_issues(self, complaints: list[dict[str, Any]]) -> list[dict[str, Any]]:
        topics = {}
        for complaint in complaints:
            topic = complaint.get("topic") or "uncategorized"
            topics.setdefault(topic, {"count": 0, "items": []})
            topics[topic]["count"] += 1
            topics[topic]["items"].append(complaint)

        return [
            {
                "topic": name,
                "size": data["count"],
                "sample_size": min(5, len(data["items"])),
            }
            for name, data in sorted(topics.items(), key=lambda kv: kv[1]["count"], reverse=True)
        ]

    def summarize_issue(self, complaint_group: list[dict[str, Any]]) -> dict[str, Any]:
        if not complaint_group:
            return {"summary": "No complaints found"}

        top_topic = max(complaint_group, key=lambda item: item.get("volume", 0))
        return {
            "summary": f"Most active complaint pattern: {top_topic.get('topic', 'unknown')}",
            "top_topic": top_topic.get("topic", "unknown"),
            "count": len(complaint_group),
        }
