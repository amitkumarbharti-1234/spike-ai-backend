from typing import Dict, List
class GA4SEOFusion:
    def fuse(self, ga4_result: Dict, seo_df) -> List[Dict]:
        fused = []
        ga4_rows = ga4_result.get("analysis", {}).get("data", [])
        if not ga4_rows or seo_df is None:
            return []
        seo_lookup = {}
        for _, row in seo_df.iterrows():
            url = str(row.get("Address") or row.get("URL") or "").strip()
            if url:
                seo_lookup[url.rstrip("/")] = row
        for row in ga4_rows:
            page_path = row.get("pagePath") or row.get("page_path")
            if not page_path:
                continue
            seo_row = seo_lookup.get(page_path.rstrip("/"))
            fused.append({
                "url": page_path,
                "views": int(row.get("screenPageViews", 0)),
                "title": seo_row.get("Title 1") if seo_row is not None else None,
                "indexable": (
                    seo_row.get("Indexability") == "Indexable"
                    if seo_row is not None else None
                )
            })

        return fused
