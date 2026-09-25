"""
developer_agent.py

The Developer Agent - the third agent of the system.

Following the multi-agent principle, its input is ONLY the validated
navigation plan produced by the Planner Agent (context isolation: it never
sees the Analyst conversation or the raw requirements, just the plan
artifact).  It turns the plan into actual Python code that makes the robot
navigate.

Like the other agents, the code MUST come from the Qwen model (served through
Ollama), not from this Python program.  This module only:
    1. builds the prompt (role, task, constraints, output format),
    2. sends the plan to Qwen via the Ollama client,
    3. extracts the Python code from the model's response,
    4. validates the code (validate_code),
    5. returns the validated code as a string.

Public API:
    run_developer(plan) -> str
    validate_code(code) -> str
"""

import json
import os

from ollama import chat

# Qwen model served by the local Ollama installation.
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:1.5b")

ALLOWED_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}

SYSTEM_PROMPT = """You are a senior robot software engineer. You receive a
validated navigation plan (a JSON object) and you write the actual Python code
that makes the robot navigate according to that plan.

Requirements for the code you produce:
1. It must be plain, valid Python 3 code that can be executed as-is.
2. It MUST define and fully implement the navigation decision function below.
   You may rename the function, add helper functions and docstrings, but the
   core if/elif/else logic MUST be kept exactly as shown (matching the plan's
   "decisions" rules):

   def decide_next_action(blocked_ahead, blocked_left, blocked_right,
                          goal_reached):
       if goal_reached:
           return "STOP"
       if not blocked_ahead:
           return "FORWARD"
       if not blocked_left:
           return "LEFT"
       if not blocked_right:
           return "RIGHT"
       return "STOP"

3. You MAY add small helper functions (e.g. a navigate() loop that calls
   decide_next_action), but EVERY function must contain real working logic.
   NEVER use "pass" and NEVER write placeholder comments like
   "Replace with actual logic".
4. The code may ONLY use the actions listed in the plan's "allowed_actions"
   (FORWARD, LEFT, RIGHT, STOP) - nothing else.
5. Use only the Python standard library. Do not import any external library.
6. Do not read files, do not open network connections, do not call eval/exec,
   do not ask for user input. Keep it a pure, deterministic logic module.
7. Output ONLY the Python code - no explanations, no markdown code fences, no
   extra text before or after.

You will receive the plan as the user message. Write the code now."""


def call_qwen(plan):
    """Send the system prompt + the validated plan to Qwen through Ollama and
    return the raw response text (which should be Python code)."""
    user_content = json.dumps(plan, indent=2, ensure_ascii=False)

    response = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        options={"temperature": 0.2},
    )

    # ollama returns a ChatResponse object (pydantic model).
    if hasattr(response, "message"):
        message = response.message
        if hasattr(message, "content"):
            return message.content
    # Fallback for dict-style responses.
    if isinstance(response, dict):
        try:
            return response["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                "Unexpected response from Qwen: {}".format(response)
            ) from exc
    raise RuntimeError("Unexpected response from Qwen: {}".format(response))


def _strip_code_fence(text):
    """Remove a wrapping markdown code fence, if Qwen adds one."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def validate_code(code):
    """Validate the Python code produced by Qwen.

    Checks that:
    - the code is a string,
    - it compiles as valid Python 3 (compile with mode='exec'),
    - it defines at least one function (contains a top-level "def"),
    - it does not contain obviously dangerous constructs.

    Returns the validated (cleaned) code string on success, otherwise raises
    ValueError with a clear message.
    """
    if not isinstance(code, str):
        raise ValueError(
            "Generated code must be a string, got {}.".format(type(code).__name__)
        )

    if not code.strip():
        raise ValueError("Generated code is empty.")

    # The plan's actions must be the only ones the code may use.  Any string
    # literal that looks like an action must be one of the allowed actions.
    # (Simple sanity check: no obviously forbidden constructs.)
    forbidden = ["eval(", "exec(", "__import__", "subprocess", "socket", "open("]
    lowered = code.lower()
    for token in forbidden:
        if token.lower() in lowered:
            raise ValueError(
                "Generated code contains forbidden construct {!r}.".format(token)
            )

    # Must compile as valid Python 3.
    try:
        compile(code, "<generated>", "exec")
    except SyntaxError as exc:
        snippet = code[:300]
        raise ValueError(
            "Generated code is not valid Python ({}). Code starts with: {!r}".format(
                exc, snippet
            )
        ) from exc

    # Must define at least one function meaningful for navigation.
    if "def " not in code:
        raise ValueError(
            "Generated code must define at least one function (e.g. "
            "decide_next_action)."
        )

    return code


def run_developer(plan):
    """Accept the validated plan artifact as a parameter, send it to the
    Developer Agent (Qwen via Ollama), accept Qwen's response, extract the
    Python code, validate it, and return the validated code as a string."""
    response_text = call_qwen(plan)

    cleaned = _strip_code_fence(response_text)
    return validate_code(cleaned)


if __name__ == "__main__":
    # Small self-test against a known-good plan artifact.
    sample_plan = {
        "goal": "Navigate the robot toward its goal while avoiding blocked paths.",
        "allowed_actions": ["FORWARD", "LEFT", "RIGHT", "STOP"],
        "safe_stop": True,
        "avoid.obstacles": True,
        "strategy": (
            "Move FORWARD whenever the path ahead is clear; if an obstacle "
            "blocks the path ahead, try LEFT then RIGHT; stop when the goal "
            "is reached or when no direction is safe."
        ),
        "decisions": [
            "If the path ahead is clear, go FORWARD.",
            "If an obstacle blocks the path ahead and the left is clear, go LEFT.",
            "If the left is blocked too, try RIGHT.",
            "If every direction is blocked, STOP.",
        ],
        "stop_condition": "Stop when the goal is reached, or when no direction "
        "is safe to move into.",
    }
    print("Running the Developer Agent on the sample plan...")
    code = run_developer(sample_plan)
    print(code)
