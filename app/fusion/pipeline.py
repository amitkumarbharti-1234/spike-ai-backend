from typing import Dict, List
import pandas as pd
from app.fusion.traffic_analyzer import TrafficAnalyzer
from app.fusion.seo_meta_analyzer import SEOMetaAnalyzer
from app.fusion.risk_engine import SEORiskEngine
from app.fusion.risk_scorer import SEORiskScorer
class Tier3PlusPipeline:
    def run(
        self,
        ga4_rows: List[Dict],
        seo_df: pd.DataFrame
    ) -> Dict:
       

       
        traffic_analyzer = TrafficAnalyzer()
        traffic_data = traffic_analyzer.analyze(ga4_rows)

      
        meta_analyzer = SEOMetaAnalyzer()
        meta_map = meta_analyzer.analyze(seo_df)

     
        risk_engine = SEORiskEngine()
        high_risk_pages = risk_engine.detect(traffic_data, meta_map)

    
        scorer = SEORiskScorer()

        final_pages = []
        for page in high_risk_pages:
            score = scorer.score(page)
            page["seo_risk_score"] = score
            final_pages.append(page)
        final_pages.sort(
            key=lambda x: x.get("seo_risk_score", 0),
            reverse=True
        )

        return {
            "analysis_type": "HIGH_TRAFFIC_HIGH_SEO_RISK",
            "summary": {
                "total_pages_analyzed": len(traffic_data),
                "high_risk_pages": len(final_pages)
            },
            "data": final_pages
        }
