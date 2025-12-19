import os
from typing import Dict, Optional

from app.ga4.executer import GA4Executor
from app.ga4.query_builder import GA4QueryBuilder
from app.ga4.interpreter import GA4Interpreter
from app.llm.litellm_client import LiteLLMClient


class GA4Agent:
    def __init__(self):
        api_key = os.getenv("LITELLM_API_KEY")

        # ----------------------------
        # SAFE MODE: LLM not configured
        # ----------------------------
        if not api_key:
            self.enabled = False
            self.error = "LITELLM_API_KEY is not configured"
            return

        self.enabled = True
        self.llm = LiteLLMClient(
            api_key=api_key,
            base_url="http://3.110.18.218"
        )
        self.query_builder = GA4QueryBuilder(self.llm)
        self.executor = GA4Executor()
        self.interpreter = GA4Interpreter()

    def run(self, query: str, property_id: Optional[str]) -> Dict:
        # ----------------------------
        # Agent disabled
        # ----------------------------
        if not self.enabled:
            return {
                "agent": "GA4",
                "status": "disabled",
                "reason": self.error
            }

        # ----------------------------
        # Missing propertyId
        # ----------------------------
        if not property_id:
            return {
                "agent": "GA4",
                "error": "propertyId is required for GA4 queries"
            }

        # ----------------------------
        # Build GA4 plan via LLM
        # ----------------------------
        plan = self.query_builder.build(query)

        # ----------------------------
        # LLM failure → STOP EARLY
        # ----------------------------
        if plan.get("status") in ("llm_error", "invalid_llm_output"):
            return {
                "agent": "GA4",
                "status": "llm_unavailable",
                "reason": plan
            }

        # ----------------------------
        # Execute GA4 safely
        # ----------------------------
        try:
            raw_result = self.executor.execute(property_id, plan)
            interpreted = self.interpreter.interpret(plan, raw_result)

            return {
                "agent": "GA4",
                "plan": plan,
                "analysis": interpreted
            }

        except Exception as e:
            return {
                "agent": "GA4",
                "status": "execution_error",
                "error": str(e)
            }
