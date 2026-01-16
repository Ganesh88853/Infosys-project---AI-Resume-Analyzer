import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from llm_analyzer import extract_skills
from skills_gap import analyze_skill_gap

sample_resume = """
I have good knowledge in Python, SQL, AI.
Worked with Streamlit.
"""

skills = extract_skills(sample_resume)

result = analyze_skill_gap(skills, target_role="ai_intern")

print("\n--- SKILL GAP ANALYSIS ---")
print(result)
