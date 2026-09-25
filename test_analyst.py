"""
test_analyst.py

Level 1 - Agent / Pipeline smoke test for the Analyst Agent.

What it does:
    1. takes the original brief.txt file,
    2. sends it to the Analyst Agent (run_analyst) and lets the agent run as
       usual - the agent's own validation accepts or rejects its output,
    3. stores the agent output in the artifacts folder under
       artifacts/requirements.json,
    4. displays the artifact after the test ends.

Ensures the agent turns the brief text into a usable requirements artifact.

Usage:
    python test_analyst.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from analyst_agent import run_analyst  # noqa: E402

BRIEF_PATH = os.path.join(HERE, "brief.txt")
ARTIFACTS_DIR = os.path.join(HERE, "artifacts")
OUT_PATH = os.path.join(ARTIFACTS_DIR, "requirements.json")


def main():
    # 1. Read the original brief.
    with open(BRIEF_PATH, "r", encoding="utf-8") as f:
        brief_text = f.read()
    print("=== Analyst Agent smoke test ===")
    print("Brief text:\n{}".format(brief_text))
    print()

    # 2. Let the agent run as usual (its own validation accepts/rejects).
    requirements = run_analyst(brief_text)

    # 3. Store the artifact under artifacts/requirements.json.
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(requirements, f, indent=2, ensure_ascii=False)

    # 4. Display the artifact after the test.
    print("Validated requirements artifact:")
    print(json.dumps(requirements, indent=2, ensure_ascii=False))
    print()
    print("PASSED: brief text was turned into a usable requirements artifact.")
    print("Saved to: {}".format(OUT_PATH))


if __name__ == "__main__":
    main()
