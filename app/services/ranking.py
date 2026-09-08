DEFAULT_WEIGHTS = {
    "severity": 0.30,
    "sentiment": 0.25,
    "volume": 0.15,
    "trend": 0.10,
    "regulatory_risk": 0.10,
    "business_impact": 0.10,
}


def _normalize(value, lower=0.0, upper=1.0):
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value


def _resolve_weights(metric_weights: dict | None = None) -> dict:
    weights = dict(DEFAULT_WEIGHTS)
    if metric_weights:
        for key, value in metric_weights.items():
            if key in weights:
                weights[key] = value
    return weights


def score_complaint(complaint: dict, metric_weights: dict | None = None) -> float:
    """Score a complaint according to a configurable metric.

    The default metric strongly favors severe, negative, high-volume and
    business-sensitive issues. A caller can override the weights to reflect a
    custom business priority model.
    """
    weights = _resolve_weights(metric_weights)

    severity = _normalize(complaint.get("severity", 0) / 5)
    sentiment = _normalize(abs(complaint.get("sentiment", 0)))
    volume = _normalize(complaint.get("volume", 0) / 200)
    trend = _normalize(complaint.get("trend", 0))
    regulatory = _normalize(complaint.get("regulatory_risk", 0))
    business = _normalize(complaint.get("business_impact", 0))

    score = (
        weights["severity"] * severity
        + weights["sentiment"] * sentiment
        + weights["volume"] * volume
        + weights["trend"] * trend
        + weights["regulatory_risk"] * regulatory
        + weights["business_impact"] * business
    )

    return round(score, 4)


def rank_complaints(complaints: list[dict], metric_weights: dict | None = None) -> list[dict]:
    ranked = []
    for complaint in complaints:
        item = dict(complaint)
        item["priority_score"] = score_complaint(item, metric_weights)
        ranked.append(item)

    ranked.sort(key=lambda item: item["priority_score"], reverse=True)
    return ranked
