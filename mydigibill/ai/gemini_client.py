import json  # Standard IDE sync complete
import time
import re as _re
import google.generativeai as genai  # type: ignore
from ai.prompts import RECEIPT_EXTRACTION_PROMPT, DATA_ANALYSIS_PROMPT, CHAT_WITH_DATA_PROMPT  # type: ignore


_PREFERRED_MODELS = [
    "models/gemini-2.5-flash",
    "models/gemini-1.5-pro",
    "models/gemini-pro",
]

def _parse_retry_seconds(error_str: str) -> int:
    """Extract retry delay from a 429 error string if present."""
    match = _re.search(r"retry[_ ](?:in|after)[^\d]*(\d+)", error_str, _re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = _re.search(r"(\d+)\.?\d*\s*s", error_str)
    if match:
        return int(match.group(1))
    return 60  # safe default

def _friendly_error(e: Exception) -> str:
    """Convert API exceptions to user-friendly strings."""
    err = str(e)
    if "429" in err or "quota" in err.lower() or "RESOURCE_EXHAUSTED" in err:
        wait = _parse_retry_seconds(err)
        mins = wait // 60
        secs = wait % 60
        time_str = f"{mins}m {secs}s" if mins else f"{secs}s"
        return (
            f"⚠️ **Gemini API free-tier quota reached.**\n\n"
            f"You've hit the daily limit for AI requests (20/day on the free plan). "
            f"Please retry in **{time_str}**, or upgrade your Gemini API plan at "
            f"[ai.google.dev](https://ai.google.dev)."
        )
    if "401" in err or "API_KEY" in err or "invalid" in err.lower():
        return "❌ **Invalid Gemini API Key.** Please check the key in the sidebar."
    if "404" in err or "not found" in err.lower():
        return "❌ **Gemini model not available.** The selected model is unavailable for your API key."
    return f"❌ **AI Error:** {err}"

class GeminiClient:
    """
    Client for interacting with Google Gemini for receipt analysis.
    Uses gemini-1.5-flash by default (best free-tier quota).
    """
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API Key is required")

        genai.configure(api_key=api_key)  # type: ignore

        self.model = None
        try:
            available_models = [
                m.name for m in genai.list_models()  # type: ignore
                if 'generateContent' in m.supported_generation_methods
                # Explicitly exclude 2.x models to stay on free-tier-friendly 1.5
                and "2." not in m.name
            ]

            for preferred in _PREFERRED_MODELS:
                if preferred in available_models:
                    self.model = genai.GenerativeModel(preferred)  # type: ignore
                    break

            # Partial match fallback — pick first 1.5-flash available
            if not self.model:
                for m in available_models:
                    if "1.5" in m and "flash" in m:
                        self.model = genai.GenerativeModel(m)  # type: ignore
                        break

            if not self.model and available_models:
                self.model = genai.GenerativeModel(available_models[0])  # type: ignore

        except Exception as e:
            print(f"Error listing models: {e}. Falling back to default.")

        # Hard fallback
        if not self.model:
            self.model = genai.GenerativeModel("gemini-1.5-flash")  # type: ignore

    def _generate_content_safe(self, prompt_parts):
        if not self.model:
            raise RuntimeError("Gemini model not initialized")
        try:
            return self.model.generate_content(prompt_parts)
        except Exception as e:
            err = str(e)
            # On quota error, raise immediately with friendly message
            if "429" in err or "RESOURCE_EXHAUSTED" in err or "quota" in err.lower():
                raise RuntimeError(_friendly_error(e))
            # On model-not-found, try legacy gemini-pro once
            if "404" in err or "not found" in err.lower():
                print("Current model failed, trying gemini-pro")
                try:
                    return genai.GenerativeModel("gemini-pro").generate_content(prompt_parts)  # type: ignore
                except Exception as e2:
                    raise RuntimeError(_friendly_error(e2))
            raise e


    def extract_receipt(self, image):
        """
        Sends the receipt image to Gemini 1.5 Flash for structured extraction.
        Returns a dict matching the schema or None on failure.
        """
        try:
            response = self._generate_content_safe([RECEIPT_EXTRACTION_PROMPT, image])
            text = response.text.strip()
            
            # Use regex to find the JSON block
            import re
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                json_str = match.group()
                data = json.loads(json_str)
                
                # Ensure all required keys exist with defaults
                defaults = {
                    "bill_id": "UNKNOWN",
                    "vendor": "Unknown Vendor",
                    "category": "Uncategorized",
                    "date": "2024-01-01",
                    "amount": 0.0,
                    "tax": 0.0,
                    "subtotal": 0.0,
                    "items": []
                }
                
                for key, default in defaults.items():
                    if key not in data:
                        data[key] = default
                    elif data[key] is None:
                        data[key] = default
                        
                # Type safety for amount/tax
                try:
                    data["amount"] = float(data["amount"])
                except:
                    data["amount"] = 0.0
                    
                try:
                    data["tax"] = float(data["tax"])
                except:
                    data["tax"] = 0.0
                    
                try:
                    data["subtotal"] = float(data["subtotal"])
                except:
                    data["subtotal"] = 0.0

                return data
            return None
        except Exception as e:
            print(f"Error extracting receipt: {e}")
            return None

    def generate_insights(self, data_summary):
        """
        Generates spending insights based on the dataframe summary string.
        """
        try:
            prompt = f"{DATA_ANALYSIS_PROMPT}\n\nData:\n{data_summary}"
            response = self._generate_content_safe(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insights: {e}"

    def chat_with_data(self, query, context_str):
        """
        Answers user questions based on the provided data context.
        """
        try:
            prompt = CHAT_WITH_DATA_PROMPT.format(context=context_str, question=query)
            response = self._generate_content_safe(prompt)
            return response.text
        except Exception as e:
            return "Sorry, I encountered an error analyzing the data."
