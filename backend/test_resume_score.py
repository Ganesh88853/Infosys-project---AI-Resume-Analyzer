import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.resume_scorer import score_resume

sample_resume = """
Email: test@gmail.com
Education: B.Tech Computer Science
Skills: Python, SQL, AI, Streamlit
Experience: Built AI resume analyzer project
Improved accuracy by 30%
"""

result = score_resume(sample_resume)

print("FINAL SCORE:", result["final_score"])
print("GRADE:", result["grade"])
print("BREAKDOWN:")
for k, v in result["breakdown"].items():
    print(k, "->", v)
