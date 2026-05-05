# Evaluation Framework — Permitting & Risk Intelligence Engine

## Goal

Measure whether the tool surfaces correct, complete, and useful permitting insights — and whether it does so without hallucinating agency names, requirements, or process steps.

---

## Evaluation Dimensions

### 1. Recall — Did it catch what matters?

**Definition:** Of all the permits and risks a qualified California permitting consultant would flag for a given project, what percentage did the tool identify?

**Method:**
- For each sample project, have 2–3 subject matter experts (SMEs) independently list the permits and risks they would flag.
- Score the tool's output against the SME union list.
- Compute: `Recall = (issues correctly flagged) / (total issues SMEs would flag)`

**Target:** >75% recall on well-described projects; >50% on thin descriptions.

---

### 2. Precision — Did it avoid hallucination?

**Definition:** Of the permits and risks the tool flagged, what percentage are real (not fabricated or wrong)?

**Method:**
- For each insight, SME rates: Correct / Plausible (real risk, uncertain applicability) / Incorrect (wrong agency, doesn't apply, made-up requirement).
- Compute: `Precision = (Correct + Plausible) / (total insights)`

**Target:** >90% precision (Correct + Plausible). Zero tolerance for clearly fabricated agency names or regulation citations.

---

### 3. Specificity — Is it California-specific?

**Definition:** Does the tool name actual California agencies and statutes, or does it give generic advice?

**Scoring rubric (per insight):**
| Score | Description |
|-------|-------------|
| 3 | Named specific agency + district/region + relevant statute or program |
| 2 | Named specific agency, no district or statute |
| 1 | Generic agency type (e.g., "the relevant water quality agency") |
| 0 | Wrong or fabricated agency |

**Target:** Mean score ≥ 2.0 across all agency-related insights.

---

### 4. Assumptions Transparency

**Definition:** Does the tool explicitly state its assumptions rather than presenting uncertain conclusions as facts?

**Method:** For each insight, check whether the assumptions array is populated and whether the stated assumptions are plausible (not trivially obvious, not fabricated).

**Target:** Every Medium/Low confidence insight has at least one explicit assumption. No High-confidence insight has a hidden assumption a SME would consider load-bearing.

---

### 5. Missing Information Quality

**Definition:** Is the missing_information list useful — does it name things that would actually change the analysis?

**Method:** SME rates each missing_information item: Critical / Useful / Obvious / Not relevant.

**Target:** >60% Critical or Useful; <10% Not relevant.

---

## Test Projects

| ID | Project | Complexity | Expected Risk Level |
|----|---------|-----------|-------------------|
| T1 | LA urban water main replacement (sample 0) | Medium | Medium |
| T2 | Sacramento stormwater near Arcade Creek (sample 1) | High | High |
| T3 | San Jose underground electric, Caltrans ROW + federal funds (sample 2) | High | High |
| T4 | Simple waterline repair in a cul-de-sac, no ROW crossing | Low | Low |
| T5 | New force main crossing a tidal slough in the Bay Area | Very High | High |

---

## Baseline

The primary baseline is **unstructured web search + experienced engineer.** A senior engineer spending 30 minutes researching a project should outperform the tool on recall and precision. The tool's value proposition is speed (seconds vs. 30 minutes) and consistency (no forgotten items when an engineer is busy).

A secondary baseline is **generic ChatGPT with no system prompt.** PRIE should substantially outperform on California specificity and assumptions transparency.

---

## Iteration Protocol

1. Run evaluation on all 5 test projects monthly.
2. Log recall/precision/specificity scores in a versioned evaluation sheet.
3. For every Incorrect rating: diagnose whether the error is a prompt issue, a knowledge cutoff issue, or a model hallucination.
4. Prompt changes require re-running the full evaluation before merging.
5. Track prompt version in output metadata for traceability.
