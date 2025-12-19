import json
from typing import Any, Dict

from app.llm.prompts import GA4_EXTRACTION_PROMPT
from app.llm.litellm_client import LiteLLMClient
from app.ga4.allowlist import (
    normalize_metrics,
    normalize_dimensions,
    validate_metrics_and_dimensions
)


class GA4QueryBuilder:
    """
    Converts natural language queries into validated GA4 reporting plans.
    """

    def __init__(self, llm_client: LiteLLMClient):
        self.llm = llm_client

    def build(self, query: str) -> Dict[str, Any]:
        prompt = GA4_EXTRACTION_PROMPT + query

        raw_response = self.llm.chat(prompt)

        # ----------------------------
        # CASE 1: LLM returned error dict
        # ----------------------------
        if isinstance(raw_response, dict):
            return {
                "status": "llm_error",
                "details": raw_response
            }

        # ----------------------------
        # CASE 2: LLM returned string
        # ----------------------------
        try:
            plan = json.loads(raw_response)
        except json.JSONDecodeError as e:
            return {
                "status": "invalid_llm_output",
                "raw_output": raw_response,
                "error": str(e)
            }

        # ----------------------------
        # Normalize
        # ----------------------------
        metrics = normalize_metrics(plan.get("metrics", []))
        dimensions = normalize_dimensions(plan.get("dimensions", []))

        # ----------------------------
        # Validate
        # ----------------------------
        valid_metrics, valid_dimensions = validate_metrics_and_dimensions(
            metrics, dimensions
        )

        # ----------------------------
        # GA4 requires at least one metric
        # ----------------------------
        if not valid_metrics:
            valid_metrics = ["activeUsers"]

        plan["metrics"] = valid_metrics
        plan["dimensions"] = valid_dimensions

        return plan
