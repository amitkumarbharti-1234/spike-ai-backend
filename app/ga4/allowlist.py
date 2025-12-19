from typing import List, Tuple

ALLOWED_METRICS = {
    "users",
    "activeUsers",
    "newUsers",
    "sessions",
    "screenPageViews",
    "engagedSessions",
    "engagementRate",
    "averageSessionDuration",
    "bounceRate"
}

ALLOWED_DIMENSIONS = {
    "date",
    "pagePath",
    "pageTitle",
    "country",
    "city",
    "deviceCategory",
    "browser",
    "source",
    "medium"
}

METRIC_SYNONYMS = {
    "page views": "screenPageViews",
    "pageviews": "screenPageViews",
    "views": "screenPageViews",
    "visits": "sessions",
    "visitors": "users",
    "avg session duration": "averageSessionDuration"
}

DIMENSION_SYNONYMS = {
    "page": "pagePath",
    "url": "pagePath",
    "path": "pagePath",
    "device": "deviceCategory",
    "traffic source": "source"
}

def normalize_metrics(metrics: List[str]) -> List[str]:
    normalized = []
    for metric in metrics:
        key = metric.lower()
        if key in METRIC_SYNONYMS:
            normalized.append(METRIC_SYNONYMS[key])
        else:
            normalized.append(metric)
    return normalized


def normalize_dimensions(dimensions: List[str]) -> List[str]:
    normalized = []
    for dim in dimensions:
        key = dim.lower()
        if key in DIMENSION_SYNONYMS:
            normalized.append(DIMENSION_SYNONYMS[key])
        else:
            normalized.append(dim)
    return normalized

def validate_metrics_and_dimensions(
    metrics: List[str],
    dimensions: List[str]
) -> Tuple[List[str], List[str]]:
    valid_metrics = [m for m in metrics if m in ALLOWED_METRICS]
    valid_dimensions = [d for d in dimensions if d in ALLOWED_DIMENSIONS]

    if not valid_metrics:
        raise ValueError("No valid GA4 metrics provided")

    return valid_metrics, valid_dimensions
