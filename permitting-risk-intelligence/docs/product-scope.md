# Product Scope — Permitting & Risk Intelligence Engine

## Vision

A SaaS-ready AI tool that gives infrastructure project teams a permitting risk briefing in under 60 seconds, reducing the cost of "permitting surprise" in California utility and civil projects.

## Prototype (Current)

### In Scope
- CLI Python tool
- Plain-English project description input
- Structured JSON output validated by Pydantic
- Rich terminal table display
- JSON output saved to disk with timestamp
- MockLLMClient for offline/demo use
- 3 sample California projects (LA, Sacramento, San Jose)
- California-specific expert system prompt

### Out of Scope (Prototype)
- Web UI
- User accounts or multi-tenant access
- Real-time agency database queries
- Geospatial analysis or parcel lookup
- PDF report generation
- Historical permit data or case law

---

## V1 Product (Next Phase)

### Core Features
1. **Web interface** — project description input form, formatted results page
2. **Project library** — save, name, and retrieve past analyses
3. **GIS integration** — auto-detect jurisdiction, proximity to waterways, Caltrans ROW from project location
4. **Agency database** — maintain current processing time estimates per agency, updated quarterly
5. **PDF export** — formatted permitting memo suitable for owner/stakeholder distribution

### Integrations to Explore
| Integration | Value |
|-------------|-------|
| California CEQA database (CEQA portals) | Confirm exemption precedents for similar projects |
| CNDDB (CA Natural Diversity Database) | Auto-check listed species presence in project footprint |
| Caltrans Encroachment Permit portal | Status lookups for active permits |
| Underground Service Alert (Dig Alert) | Trigger automated 811 notifications |
| ArcGIS / county parcel APIs | Confirm jurisdiction and ROW ownership |

### Pricing Hypothesis
- Per-analysis: $25–50 for one-off users
- Subscription: $300–500/month for project teams (unlimited analyses)
- Enterprise: $2,000–5,000/month for program managers running 20+ projects

---

## V2 Product (12-Month Horizon)

### Portfolio Intelligence
- Ingest a project list (CSV or API) and generate risk heatmap across a capital program
- Flag projects with overlapping permit windows or shared agency bottlenecks
- Auto-generate permitting Gantt chart for a project portfolio

### Feedback Loop
- Allow permitting professionals to rate and correct outputs
- Use corrections to fine-tune prompts (or fine-tune model)
- Track accuracy metrics: % of predicted permits confirmed vs. missed

### Expansion Opportunities
- Other western states (Oregon, Washington, Arizona) with similar CEQA-analogues
- Federal lands / BLM / Forest Service overlay
- Stormwater-specific module (MS4 permit compliance, green infrastructure)
- Transmission line / substation module (CPUC jurisdiction, NEPA/CEQA hybrid)

---

## Key Risks

| Risk | Mitigation |
|------|-----------|
| LLM hallucination of agency names or requirements | Expert review layer; confidence scoring; user-visible assumptions |
| Regulatory changes not reflected in model | System prompt versioning; periodic prompt audits; user-reported corrections |
| Liability for incorrect permitting advice | Clear disclaimer on all outputs; positioning as planning support, not legal advice |
| California-only limits TAM | Design for extensibility from day one; state-specific prompt modules |
| Competitors (established permitting consultants) | Focus on speed and early-stage value; not replacing the expert, augmenting them |
