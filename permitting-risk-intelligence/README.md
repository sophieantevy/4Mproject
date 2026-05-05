# Permitting & Risk Intelligence Engine (PRIE)

A Python CLI prototype that takes a plain-English description of a California utility or civil infrastructure project and returns a structured JSON analysis of required permits, agencies involved, coordination risks, environmental triggers, utility conflicts, and schedule risks — validated by Pydantic and rendered in a formatted terminal table.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key (or skip to run in mock mode)
cp .env.example .env
# edit .env and add your ANTHROPIC_API_KEY

# 3. Run with a sample project (index 0 = LA water main)
cd src
python main.py --sample 0

# 4. Run with a custom description
python main.py "Replace 500 LF of 8-inch water main on Main Street in Oakland, CA"

# 5. Force mock mode (no API key required)
python main.py --sample 1 --mock

# 6. List all available sample projects
python main.py --list-samples
```

## Sample Projects

| Index | Project |
|-------|---------|
| 0 | Urban water main replacement — Los Angeles (Venice Blvd) |
| 1 | Stormwater drainage improvement near Arcade Creek — Sacramento |
| 2 | Underground electric distribution line relocation — San Jose (Stevens Creek Blvd) |

## Output

Each run prints a formatted table in the terminal and saves a timestamped JSON file to `outputs/`.

### Output Schema

```json
{
  "project_summary": "string",
  "overall_risk_level": "High | Medium | Low",
  "insights": [
    {
      "category": "Permit | Agency | Coordination | Environmental | Utility Conflict | Schedule",
      "insight": "string",
      "risk_level": "High | Medium | Low",
      "why_it_matters": "string",
      "recommended_next_step": "string",
      "confidence": "High | Medium | Low",
      "assumptions": ["string"]
    }
  ],
  "missing_information": ["string"],
  "disclaimer": "This is a planning-support analysis, not legal or permitting advice."
}
```

## Architecture

```
main.py          CLI entrypoint — arg parsing, orchestration, output saving
llm_client.py    Abstract LLMClient + MockLLMClient + AnthropicLLMClient
schemas.py       Pydantic models for validated output
prompts.py       System prompt (CA permitting expert) + user prompt builder
formatter.py     Rich terminal table renderer
```

**Auto-mock mode:** If `ANTHROPIC_API_KEY` is not set, the tool automatically falls back to `MockLLMClient`, which returns realistic hardcoded output for the LA water main scenario. This lets you demo the full UI/output pipeline without an API key.

## Tech Stack

- Python 3.10+
- [anthropic](https://github.com/anthropics/anthropic-sdk-python) — Claude claude-opus-4-5
- [pydantic](https://docs.pydantic.dev/) v2 — schema validation
- [python-dotenv](https://github.com/theskumar/python-dotenv) — env var loading
- [rich](https://github.com/Textualize/rich) — terminal formatting

## Disclaimer

This tool is a planning-support prototype. It does not constitute legal or permitting advice. All outputs should be verified with the relevant agencies and qualified permitting professionals.
