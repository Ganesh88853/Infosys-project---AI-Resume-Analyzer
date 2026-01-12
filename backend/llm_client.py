import os
import time
from dotenv import load_dotenv
from google import genai

# -------------------------------------------------
# LOAD ENV
# -------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY missing in .env")

# -------------------------------------------------
# CLIENT
# -------------------------------------------------
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash"  # ✅ CORRECT for new SDK

# -------------------------------------------------
# SAFE LLM CALL
# -------------------------------------------------
def call_llm(prompt: str, retries: int = 2, delay: int = 3) -> str:
    for attempt in range(retries + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if response and response.text:
                return response.text.strip()

            raise RuntimeError("Empty LLM response")

        except Exception as e:
            print(f"⚠️ LLM Error (attempt {attempt+1}):", e)
            time.sleep(delay)

    print("❌ LLM failed after retries")
    return ""
