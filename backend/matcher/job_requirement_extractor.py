import json
import google.generativeai as genai

def extract_job_requirements(job_description: str) -> dict:
    """
    Uses LLM to extract structured job requirements
    """

    prompt = f"""
You are an ATS job parser.

Extract job requirements from the description below.

Return ONLY valid JSON.

FORMAT:
{{
  "must_have_skills": [],
  "nice_to_have_skills": [],
  "required_experience_years": null,
  "required_education": "",
  "responsibilities": [],
  "seniority_level": "junior | mid | senior | lead"
}}

JOB DESCRIPTION:
{job_description}
"""

    try:
        response = genai.GenerativeModel("models/gemini-1.0-pro").generate_content(prompt)
        data = json.loads(response.text)
        return data

    except Exception as e:
        print(f"Job requirement extraction failed: {e}")

        # 🔁 Safe fallback
        return {
            "must_have_skills": [],
            "nice_to_have_skills": [],
            "required_experience_years": None,
            "required_education": "",
            "responsibilities": [],
            "seniority_level": "unknown"
        }
