from typing import Dict
class SEORiskScorer:
    def score(self, page: Dict) -> int:
        is_high_traffic = page.get("is_high_traffic", False)
        meta_issue = page.get("meta_issue")

        if is_high_traffic and meta_issue == "missing":
            return 90

        if is_high_traffic and meta_issue == "duplicate":
            return 80

        if not is_high_traffic and meta_issue == "missing":
            return 60

        return 30
