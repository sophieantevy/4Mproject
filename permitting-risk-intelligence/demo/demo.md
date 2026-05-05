# Demo Guide — Permitting & Risk Intelligence Engine

## Setup (2 minutes)

```bash
git clone <repo>
cd permitting-risk-intelligence
pip install -r requirements.txt
cp .env.example .env
# Optional: add ANTHROPIC_API_KEY to .env
# If omitted, the tool runs in mock mode automatically
```

---

## Demo Script

### Act 1: The Problem (30 seconds)

> "A project engineer in Los Angeles is asked to replace an aging water main. She needs to know what permits are required before she can scope the project. Normally she'd spend a day or two emailing agencies and searching the web. Let's see what PRIE can do in a few seconds."

---

### Act 2: Run the Tool (live)

**Step 1 — List available samples:**
```bash
cd src
python main.py --list-samples
```

Expected output:
```
Available sample projects:
  0 — LA Urban Water Main Replacement
  1 — Sacramento Stormwater Drainage Improvement Near Creek
  2 — San Jose Underground Electric Line Relocation
```

---

**Step 2 — Run sample 0 (LA water main) in mock mode:**
```bash
python main.py --sample 0 --mock
```

Point out:
- **Project Summary** panel at the top — clean restatement of the project
- **Overall Risk Level** — Medium (visible in the summary panel)
- **Insights table** — 7 rows covering Permit, Agency, Coordination, Environmental, Utility Conflict, Schedule
- **Risk** and **Confidence** columns — color-coded (red/yellow/green)
- **Assumptions** shown inline in gray under each insight
- **Missing Information** table — 7 items that would sharpen the analysis
- **Disclaimer** footer

---

**Step 3 — Run a live custom description (if API key set):**
```bash
python main.py "Install a new 500-foot 16-inch recycled water main alongside Coyote Creek in San Jose, CA, connecting to an existing recycled water system. The alignment crosses under the creek in one location using horizontal directional drilling (HDD). The project is within Santa Clara Valley Water District easement and partially in Caltrans right-of-way on Capitol Expressway."
```

This description is intentionally information-rich to show the tool's full depth:
- Recycled water = Title 22 / CDPH involvement
- Creek crossing = Section 404/401 + Fish & Game 1602
- HDD = trenchless-specific permit considerations
- SCVWD easement = district approval layer
- Caltrans ROW = encroachment permit from District 4
- Capitol Expressway = may be expressway-classified (special Caltrans rules)

---

**Step 4 — Show the saved output:**
```bash
ls ../outputs/
cat ../outputs/<most_recent>.json | python -m json.tool | head -80
```

---

### Act 3: The Output Structure (2 minutes)

Walk through the JSON schema:

```json
{
  "project_summary": "...",
  "overall_risk_level": "Medium",
  "insights": [
    {
      "category": "Permit",
      "insight": "...",
      "risk_level": "High",
      "why_it_matters": "...",
      "recommended_next_step": "...",
      "confidence": "High",
      "assumptions": ["..."]
    }
  ],
  "missing_information": ["..."],
  "disclaimer": "..."
}
```

Key points:
- **Structured and machine-readable** — can be consumed by downstream tools (scheduling, cost estimation, GIS)
- **Pydantic-validated** — schema errors are caught and surfaced clearly
- **Every insight has a recommended next step** — actionable, not just a list of risks
- **Assumptions are explicit** — the tool tells you what it doesn't know

---

### Act 4: Why This Matters

> "This analysis would normally take a permitting consultant half a day. PRIE does it in seconds. It won't replace the expert — but it gives them a validated checklist rather than a blank page. And it catches the things that get forgotten when engineers are heads-down."

---

## Suggested Q&A Responses

**Q: What if the AI gets something wrong?**
> "Every insight includes an explicit confidence rating and assumptions list. The tool is designed to flag uncertainty rather than hide it. High-confidence items are things every expert would agree on; low-confidence items are 'worth checking.' A permitting professional reviews the output — the tool augments them, it doesn't replace them."

**Q: How do you keep it current as regulations change?**
> "The system prompt is versioned and can be updated as regulations change. Longer term, we'd connect to real-time databases (CEQA portals, CNDDB, Caltrans permit tracker) to verify against live data."

**Q: Can it handle projects outside California?**
> "The current system prompt is tuned specifically for California — CEQA, Porter-Cologne, Fish & Game Code Section 1602, Caltrans district-specific requirements. Expanding to other states is a prompt engineering exercise, with Oregon and Washington as natural next targets."

**Q: What's the business model?**
> "Per-analysis pricing for occasional users ($25–50), subscriptions for project teams ($300–500/month), and enterprise licensing for program managers overseeing 20+ projects. The enterprise play is portfolio intelligence — flagging which projects in a capital program have the highest permitting risk."
