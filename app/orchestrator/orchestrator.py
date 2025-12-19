from typing import Dict, Optional

from app.agents.ga4_agent import GA4Agent
from app.agents.seo_agent import SEOAgent
from app.fusion.pipeline import Tier3PlusPipeline


class Orchestrator:
    def route(self, query: str, property_id: Optional[str]) -> Dict:
        q = query.lower()

        ga4_keywords = ["user", "users", "session", "traffic", "ga4"]
        seo_keywords = ["seo", "meta", "index", "duplicate", "missing"]
        tier3_keywords = ["high traffic", "risk", "top", "priority"]

        is_ga4 = any(k in q for k in ga4_keywords)
        is_seo = any(k in q for k in seo_keywords)
        is_tier3 = is_ga4 and is_seo and any(k in q for k in tier3_keywords)

        # -------------------------
        # TIER-3+ SAFE FLOW
        # -------------------------
        if is_tier3:
            ga4_agent = GA4Agent()
            seo_agent = SEOAgent()

            # 🛑 SAFETY CHECK
            if not getattr(ga4_agent, "enabled", True):
                return {
                    "agent": "MULTI",
                    "status": "disabled",
                    "reason": "GA4 agent is not configured"
                }

            if not getattr(seo_agent, "enabled", True):
                return {
                    "agent": "MULTI",
                    "status": "disabled",
                    "reason": "SEO agent is not configured"
                }

            pipeline = Tier3PlusPipeline()

            ga4_result = ga4_agent.run(query, property_id)
            ga4_rows = ga4_result.get("analysis", {}).get("data", [])

            seo_df = seo_agent.get_dataframe()

            return pipeline.run(ga4_rows, seo_df)

        # -------------------------
        # SEO ONLY
        # -------------------------
        if is_seo and not is_ga4:
            return SEOAgent().run(query)

        # -------------------------
        # GA4 ONLY
        # -------------------------
        return GA4Agent().run(query, property_id)
