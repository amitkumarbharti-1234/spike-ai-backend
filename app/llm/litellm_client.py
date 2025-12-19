import time
from typing import Any, Dict

from openai import OpenAI
from openai import APIError, APITimeoutError, APIConnectionError, RateLimitError


class LiteLLMClient:
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def chat(self, prompt: str, max_retries: int = 5) -> Any:
        base_delay = 1

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    timeout=30
                )

                return response.choices[0].message.content

            except (RateLimitError, APITimeoutError, APIConnectionError) as e:
                wait_time = base_delay * (2 ** attempt)
                time.sleep(wait_time)
                continue

            
            except APIError as e:
                return {
                    "error_type": e.__class__.__name__,
                    "error_message": str(e)
                }

           
            except Exception as e:
                return {
                    "error_type": e.__class__.__name__,
                    "error_message": str(e)
                }

        return {
            "error_type": "RetryLimitExceeded",
            "error_message": "LLM request failed after multiple retries"
        }
