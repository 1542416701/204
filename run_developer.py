"""
run_developer.py

Runner for the Developer Agent.  Its responsibilities:
    1. read the validated navigation plan from plan.json (the artifact
       produced by the Planner Agent; preferred location is artifacts/,
       falling back to the project root),
    2. call run_developer(plan),
    3. receive the validated Python code,
    4. store the generated code in generated/navigation_logic.py.

Usage:
    python run_developer.py
"""

import json
import os

from developer_agent import run_developer

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN_PATH = os.path.join(HERE, "artifacts", "plan.json")
if not os.path.exists(PLAN_PATH):
    PLAN_PATH = os.path.join(HERE, "plan.json")
GENERATED_DIR = os.path.join(HERE, "generated")
OUT_PATH = os.path.join(GENERATED_DIR, "navigation_logic.py")


def main():
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        plan = json.load(f)

    print("Validated plan (input to the Developer Agent):")
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    print()

    code = run_developer(plan)

    os.makedirs(GENERATED_DIR, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(code)
        if not code.endswith("\n"):
            f.write("\n")

    print("Validated navigation code:")
    print(code)
    print()
    print("Saved to: {}".format(OUT_PATH))


if __name__ == "__main__":
    main()
