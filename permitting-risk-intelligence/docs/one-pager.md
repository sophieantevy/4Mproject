# Permitting & Risk Intelligence Engine — One-Pager

## The Problem

California infrastructure projects — water mains, storm drains, underground utilities — routinely face 6–18 month permitting delays because project engineers discover permit requirements too late. Early-stage scoping rarely includes a permitting expert, and agencies don't proactively communicate what they require. The result: missed environmental windows, undisclosed utility conflicts, CEQA surprises, and schedule compression that drives cost overruns.

## What This Tool Does

PRIE takes a plain-English description of a California utility or civil infrastructure project and returns a structured, prioritized analysis of:

- **Required permits** — encroachment, NPDES, CEQA exemptions, Section 404/401, Streambed Alteration
- **Agencies involved** — specific California agencies by name and district (not generic labels)
- **Multi-agency coordination risks** — sequencing dependencies, concurrent review windows, joint application opportunities
- **Environmental triggers** — CEQA pathway, biological survey windows, tribal consultation (AB 52 / Section 106)
- **Utility conflicts** — subsurface crowding risk, Dig Alert obligations, specific utility operators
- **Schedule risks** — moratorium streets, nesting bird windows, wet-season grading restrictions, permit critical path
- **Missing information** — what gaps would change the analysis if filled

## Who Uses It

- **Project engineers** — during pre-design and 30% design to scope permit-related work
- **Project managers** — for schedule risk identification and agency coordination planning
- **Public agency staff** — for capital program risk triage across a portfolio of projects
- **Owners' representatives and program managers** — to flag issues before they become change orders

## Why AI

Permitting knowledge in California is hyper-local, regulation-dense, and constantly evolving. An expert who knows Caltrans District 7 encroachment requirements, LA RWQCB Waste Discharge Requirements, and LADWP pipe material standards simultaneously is rare and expensive. A well-prompted LLM with California-specific system prompt can surface 80% of the relevant issues in seconds, giving the human expert something to validate rather than something to generate from scratch.

## Prototype Scope

This prototype demonstrates the core analysis loop: input → structured JSON → validated schema → formatted output. It is not a production system. It does not connect to live permit databases, CEQA portals, or agency GIS layers — those integrations are the next phase.

## Limitations

- Analysis quality depends on description quality. Thin descriptions produce thin analysis.
- The tool does not know current agency processing times (it uses expert-informed estimates).
- It does not search real-time databases (CNDDB, CEQA portals, Caltrans encroachment permit tracker).
- Outputs must be reviewed by a qualified permitting professional before acting on them.
