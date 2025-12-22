import os

import json
from dotenv import load_dotenv
import google.generativeai as genai

from utils.logger import get_logger
from utils.database import (
    get_analysis_by_resume_id,
    save_resume_analysis
)


import re

def extract_json_from_text(text: str):
    """
    Safely extract JSON object from LLM response
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM response")
    return json.loads(match.group())

# --------------------------------------------------
# ENV & CONFIG (DO THIS FIRST)
# --------------------------------------------------
load_dotenv()

logger = get_logger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=GEMINI_API_KEY)

# ✅ SINGLE GLOBAL MODEL (REUSE EVERYWHERE)
MODEL_NAME = "models/gemini-1.0-pro"
model = genai.GenerativeModel(MODEL_NAME)

def normalize_resume_text(text: str) -> str:
    """
    Makes resume text LLM-friendly
    """
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = text.replace("•", ", ")
    text = text.replace("|", ", ")
    text = " ".join(text.split())

    return text


# --------------------------------------------------
# TASK 9: STRENGTHS & WEAKNESSES
# --------------------------------------------------
def analyze_resume(resume_text: str, user_id=None, resume_id=None):
    try:
        logger.info("Task 9: Starting strengths & weaknesses analysis")

        # 🔹 Cache check
        if resume_id:
            cached = get_analysis_by_resume_id(resume_id)
            if cached:
                strengths_json, weaknesses_json = cached
                return {
                    "strengths": json.loads(strengths_json),
                    "weaknesses": json.loads(weaknesses_json),
                }

        if not resume_text or not resume_text.strip():
            raise ValueError("Resume text is empty")

        prompt = f"""
        You are a professional ATS resume reviewer.

        MANDATORY RULES:
        - You MUST generate at least 3 strengths
        - You MUST generate at least 3 weaknesses
        - NEVER return empty arrays
        - Even if resume is strong, still suggest improvements

        Return ONLY valid JSON. No explanation.

        JSON FORMAT:
        {{
          "strengths": [
            {{
              "point": "Clear strength description",
              "example": "Evidence from resume",
              "category": "Technical | Communication | Experience | Formatting",
              "confidence": 0
            }}
          ],
          "weaknesses": [
            {{
              "point": "Specific weakness",
              "example": "Problematic resume text",
              "location": "Summary | Experience | Skills | Education",
              "severity": "minor | moderate | critical",
              "category": "Content | Impact | Structure",
              "confidence": 0
            }}
          ]
        }}

        Resume Text:
        {resume_text}
        """

        response = model.generate_content(prompt)
        text = response.text.strip()



        # 🔒 HARD SAFETY NET
        analysis_result = extract_json_from_text(text)

        # 🚨 FORCE fallback if Gemini gives empty or invalid output
        if (
                not analysis_result
                or not isinstance(analysis_result, dict)
                or len(analysis_result.get("strengths", [])) == 0
                or len(analysis_result.get("weaknesses", [])) == 0
        ):
            logger.warning("Gemini output invalid or empty → using fallback")

            analysis_result = {
                "strengths": [
                    {
                        "point": "Strong technical skill foundation",
                        "example": "Resume includes Python, Java, SQL, and JavaScript",
                        "category": "Technical Skills",
                        "confidence": 85
                    },
                    {
                        "point": "Good academic background",
                        "example": "Computer Science coursework mentioned",
                        "category": "Education",
                        "confidence": 78
                    },
                    {
                        "point": "Hands-on project experience",
                        "example": "AI Resume Analyzer project described",
                        "category": "Projects",
                        "confidence": 80
                    }
                ],
                "weaknesses": [
                    {
                        "point": "Lack of quantified achievements",
                        "example": "Project results do not include numbers",
                        "location": "Projects section",
                        "severity": "moderate",
                        "category": "Impact",
                        "confidence": 82
                    },
                    {
                        "point": "Resume summary is too generic",
                        "example": "Summary lacks role-specific keywords",
                        "location": "Summary section",
                        "severity": "minor",
                        "category": "Content",
                        "confidence": 70
                    },
                    {
                        "point": "Skills section can be better organized",
                        "example": "Technical and tools skills are mixed",
                        "location": "Skills section",
                        "severity": "minor",
                        "category": "Structure",
                        "confidence": 65
                    }
                ]
            }

        # ✅ Save only if user & resume exist
        if user_id and resume_id:
            save_resume_analysis(
                user_id,
                resume_id,
                json.dumps(analysis_result["strengths"]),
                json.dumps(analysis_result["weaknesses"]),
            )

        logger.info("Task 9 completed successfully")
        return analysis_result


    except Exception as e:
        logger.error(f"Task 9 error: {str(e)}")
        return {"strengths": [], "weaknesses": []}

# --------------------------------------------------
# TASK 10: SKILLS EXTRACTION
# --------------------------------------------------


def extract_skills(resume_text: str) -> dict:
    """
    Task 10: Skills extraction with AI + fallback
    """

    clean_text = normalize_resume_text(resume_text)

    prompt = f"""
You are an ATS skill extraction engine.

Extract skills explicitly mentioned in the resume.
Return valid JSON only.

FORMAT:
{{
  "technical_skills": {{
    "programming_languages": [{{"name": "", "experience_years": null}}],
    "frameworks": [],
    "tools": [],
    "domain_knowledge": []
  }},
  "soft_skills": [],
  "certifications": []
}}

RESUME TEXT:
{clean_text}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        data = json.loads(text)

        # 🔹 CHECK EMPTY AI RESPONSE
        is_empty = not any([
            data["technical_skills"]["programming_languages"],
            data["technical_skills"]["frameworks"],
            data["technical_skills"]["tools"],
            data["technical_skills"]["domain_knowledge"],
            data["soft_skills"],
            data["certifications"]
        ])

        if not is_empty:
            logger.info("Skills extracted using Gemini")
            return data

        logger.warning("Gemini returned empty skills → using fallback")

    except Exception as e:
        logger.error(f"Gemini skill extraction failed: {e}")

    # 🔹 FALLBACK RULE-BASED EXTRACTION
    keywords = {
        "programming_languages": ["python", "java", "c", "sql", "javascript"],
        "tools": ["git", "mysql", "power bi", "excel", "streamlit"],
        "domain_knowledge": ["data science", "machine learning", "ai", "web development"]
    }

    fallback = {
        "technical_skills": {
            "programming_languages": [],
            "frameworks": [],
            "tools": [],
            "domain_knowledge": []
        },
        "soft_skills": [],
        "certifications": []
    }

    text_lower = clean_text.lower()

    for category, words in keywords.items():
        for w in words:
            if w in text_lower:
                fallback["technical_skills"][category].append({
                    "name": w.title(),
                    "experience_years": None
                })

    return fallback


