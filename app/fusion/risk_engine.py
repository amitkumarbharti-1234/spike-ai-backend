from typing import List, Dict
class SEORiskEngine:
    def detect(self, traffic_data: List[Dict], meta_map: Dict) -> List[Dict]:
        high_risk_pages = []
        for page in traffic_data:
            url = page.get("url")
            is_high_traffic = page.get("is_high_traffic", False)
            meta_info = meta_map.get(url, {})
            meta_issue = meta_info.get("meta_issue", "ok")
            if is_high_traffic and meta_issue in ["missing", "duplicate"]:
                high_risk_pages.append({
                    "url": url,
                    "views": page.get("views"),
                    "traffic_percentile": page.get("traffic_percentile"),
                    "meta_issue": meta_issue,
                    "seo_risk_level": "high"
                })

        return high_risk_pages
