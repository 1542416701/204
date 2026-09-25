# agentic_se — Requirements Engineering project

Course: Special Course in Software Engineering '26 — Project: Requirements Engineering

## Files

| File | Purpose |
|---|---|
| `brief.txt` | The human-language brief (robot navigation). |
| `brief_to_req.py` | Asks Qwen to read the brief and produce software requirements; saves the output to `robot_requirements.txt`. Run several times to check consistency. |
| `analyst_agent.py` | The Analyst Agent: `run_analyst()` + `validate_requirements()`. Converts the brief into validated JSON requirements. |
| `run_analyst.py` | Runner: reads `brief.txt`, calls `run_analyst()`, writes `artifacts/requirements.json`. |
| `artifacts/requirements.json` | Final validated software requirements (JSON). |

## Setup (one time)

1. Get a DashScope (Qwen) API key: <https://bailian.console.aliyun.com/> → API-KEY management.
2. Set the key in the terminal where you run the scripts:
   - PowerShell: `$env:DASHSCOPE_API_KEY = "sk-..."`
   - CMD: `set DASHSCOPE_API_KEY=sk-...`
3. Optional: default model is `qwen-plus`; you can override with the environment
   variable `QWEN_MODEL` (e.g. `qwen-turbo` for a cheaper/faster model).
4. Python 3.8+ is required. No third-party packages are needed (standard library only).

## Run

```text
python brief_to_req.py --times 3   # run 3 times, examine consistency; output in robot_requirements.txt
python run_analyst.py              # writes artifacts/requirements.json
```

## Notes

- The final output MUST come from Qwen — run the scripts with your own API key.
- Actions are restricted to exactly: FORWARD, LEFT, RIGHT, STOP.
- Submission: create a GitHub repository named `scse_agentic_se_<groupname>`
  (replace `<groupname>` with your actual group name), push all files, and
  submit the repository link on Moodle.
