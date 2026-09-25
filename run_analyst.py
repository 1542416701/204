"""
run_analyst.py

Runner for the Analyst Agent.  Its responsibilities:
    1. read the brief text (brief.txt),
    2. call run_analyst(brief_text),
    3. receive the final validated software requirements,
    4. save the requirements as requirements.json inside the artifacts/
       folder (json.dump).

Usage:
    python run_analyst.py
"""

import json
import os

from analyst_agent import run_analyst

HERE = os.path.dirname(os.path.abspath(__file__))
BRIEF_PATH = os.path.join(HERE, "brief.txt")
ARTIFACTS_DIR = os.path.join(HERE, "artifacts")
OUT_PATH = os.path.join(ARTIFACTS_DIR, "requirements.json")


def main():
    with open(BRIEF_PATH, "r", encoding="utf-8") as f:
        brief_text = f.read()

    requirements = run_analyst(brief_text)

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(requirements, f, indent=2, ensure_ascii=False)

    print("Validated requirements:")
    print(json.dumps(requirements, indent=2, ensure_ascii=False))
    print()
    print("Saved to: {}".format(OUT_PATH))


if __name__ == "__main__":
    main()
