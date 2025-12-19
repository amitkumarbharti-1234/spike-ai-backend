from typing import List, Dict
import math
class TrafficAnalyzer:
    def analyze(self, ga4_data: List[Dict]) -> List[Dict]:
        if not ga4_data:
            return []

        sorted_pages = sorted(
            ga4_data,
            key=lambda x: int(x.get("screenPageViews", 0)),
            reverse=True
        )
        total_pages = len(sorted_pages)
        top_20_cutoff = math.ceil(total_pages * 0.2)
        enriched = []
        for index, page in enumerate(sorted_pages):
            percentile = round(
                100 * (1 - (index / total_pages)),
                2
            )
            enriched.append({
                "url": page.get("pagePath"),
                "views": int(page.get("screenPageViews", 0)),
                "traffic_percentile": percentile,
                "is_high_traffic": index < top_20_cutoff
            })
        return enriched
