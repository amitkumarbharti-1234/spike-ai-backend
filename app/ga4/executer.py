from typing import Dict, List
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
)

from app.ga4.client import get_ga4_client


class GA4Executor:
    def execute(self, property_id: str, plan: Dict) -> Dict:
        client = get_ga4_client()

        # ----------------------------
        # SAFETY: GA4 requires at least one metric
        # ----------------------------
        metric_names = plan.get("metrics") or []
        if not metric_names:
            metric_names = ["activeUsers"]

        dimension_names = plan.get("dimensions") or []

        # Build metrics
        metrics: List[Metric] = [
            Metric(name=m) for m in metric_names
        ]

        # Build dimensions
        dimensions: List[Dimension] = [
            Dimension(name=d) for d in dimension_names
        ]

        # Build date range (default last 7 days)
        date_range_cfg = plan.get("date_range", {})
        days = date_range_cfg.get("value", 7)

        date_ranges = [
            DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )
        ]

        request = RunReportRequest(
            property=f"properties/{property_id}",
            metrics=metrics,
            dimensions=dimensions,
            date_ranges=date_ranges
        )

        response = client.run_report(request)

        return self._parse_response(response)

    def _parse_response(self, response) -> Dict:
        results = []

        for row in response.rows:
            entry = {}

            for idx, dim in enumerate(response.dimension_headers):
                entry[dim.name] = row.dimension_values[idx].value

            for idx, met in enumerate(response.metric_headers):
                entry[met.name] = row.metric_values[idx].value

            results.append(entry)

        return {
            "row_count": response.row_count,
            "data": results
        }
