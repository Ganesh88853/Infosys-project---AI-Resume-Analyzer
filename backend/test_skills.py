import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from backend.llm_analyzer import extract_skills

sample_text = """
Skills: Python, SQL, Streamlit
Certified in IBM AI Fundamentals
Strong problem solving and communication skills
"""

result = extract_skills(sample_text)

print("\n--- TECHNICAL SKILLS ---")
print(json.dumps(result["technical_skills"], indent=2))

print("\n--- SOFT SKILLS ---")
print(result["soft_skills"])

print("\n--- CERTIFICATIONS ---")
print(result["certifications"])
