from typing import Dict, List


class GA4Interpreter:
    """
    Converts raw GA4 API results into human-readable insights.
    """

    def interpret(self, plan: Dict, result: Dict) -> Dict:
        row_count = result.get("row_count", 0)
        data: List[Dict] = result.get("data", [])

        if row_count == 0 or not data:
            return {
                "summary": "No data was found for the given query and date range.",
                "rows": 0,
                "data": []
            }

        metrics = plan.get("metrics", [])
        dimensions = plan.get("dimensions", [])

        summary_parts = []
        summary_parts.append(
            f"Retrieved {row_count} rows of analytics data."
        )

        if "date" in dimensions:
            summary_parts.append("The data is reported as a time series.")

        if metrics:
            summary_parts.append(
                "Metrics analyzed: " + ", ".join(metrics)
            )

        return {
            "summary": " ".join(summary_parts),
            "rows": row_count,
            "data": data
        }
