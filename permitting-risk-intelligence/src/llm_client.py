from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod

from prompts import SYSTEM_PROMPT, build_user_prompt


class LLMClient(ABC):
    @abstractmethod
    def analyze(self, project_description: str) -> dict:
        """Return a parsed dict matching the PermitAnalysis schema."""


class MockLLMClient(LLMClient):
    """Returns realistic hardcoded output for an urban water main project.
    Used when ANTHROPIC_API_KEY is absent or --mock flag is set.
    """

    def analyze(self, project_description: str) -> dict:
        return {
            "project_summary": (
                "Replace approximately 1,800 LF of 12-inch cast-iron water main in a Los Angeles "
                "city street right-of-way, including service lateral reconnections and temporary "
                "traffic control."
            ),
            "overall_risk_level": "Medium",
            "insights": [
                {
                    "category": "Permit",
                    "insight": (
                        "An Encroachment Permit from the City of Los Angeles Bureau of Engineering "
                        "(BOE) will likely be required for all work within the public right-of-way, "
                        "including open-cut trenching and restoration."
                    ),
                    "risk_level": "High",
                    "why_it_matters": (
                        "Without the encroachment permit, no work can begin in the ROW. BOE review "
                        "can take 4–8 weeks and may require Traffic Management Plan (TMP) approval "
                        "from LADOT concurrently."
                    ),
                    "recommended_next_step": (
                        "Submit encroachment permit application to LA BOE early in design; coordinate "
                        "with LADOT for TMP requirements simultaneously."
                    ),
                    "confidence": "High",
                    "assumptions": [
                        "Project is located within City of Los Angeles jurisdiction, not an unincorporated LA County area.",
                        "Work will require lane closures or full street closure.",
                    ],
                },
                {
                    "category": "Permit",
                    "insight": (
                        "An NPDES Construction General Permit (CGP) from the State Water Resources "
                        "Control Board will likely be required if disturbed area meets or exceeds "
                        "1 acre, requiring a Stormwater Pollution Prevention Plan (SWPPP) and "
                        "enrollment via SMARTS."
                    ),
                    "risk_level": "Medium",
                    "why_it_matters": (
                        "Non-enrollment prior to ground disturbance is a violation enforceable by "
                        "the Los Angeles RWQCB. SWPPP preparation and QSD/QSP designation add "
                        "cost and lead time."
                    ),
                    "recommended_next_step": (
                        "Calculate total disturbed area across all work zones. If ≥1 acre, initiate "
                        "SWPPP preparation and SMARTS enrollment 30+ days before construction start."
                    ),
                    "confidence": "Medium",
                    "assumptions": [
                        "Total ground disturbance area has not yet been calculated.",
                        "Project is phased along a single corridor; staging areas may push total acreage over threshold.",
                    ],
                },
                {
                    "category": "Agency",
                    "insight": (
                        "LADWP (Los Angeles Department of Water and Power) must be notified as the "
                        "water system owner and must approve connection details, pressure zone "
                        "compliance, and service lateral specifications."
                    ),
                    "risk_level": "High",
                    "why_it_matters": (
                        "LADWP review and approval is on the critical path. Unapproved designs or "
                        "materials can result in rejection at inspection, causing costly rework."
                    ),
                    "recommended_next_step": (
                        "Schedule pre-design meeting with LADWP Distribution Engineering to confirm "
                        "pipe material standards, allowable connection methods, and as-built record "
                        "availability."
                    ),
                    "confidence": "High",
                    "assumptions": [
                        "The existing main is LADWP-owned infrastructure.",
                        "Project is funded by LADWP capital program or a developer reimbursement agreement.",
                    ],
                },
                {
                    "category": "Coordination",
                    "insight": (
                        "Concurrent coordination between LA BOE, LADOT, and LADWP is required. "
                        "These agencies operate on independent review timelines and do not share "
                        "a joint application portal, creating potential sequencing delays."
                    ),
                    "risk_level": "Medium",
                    "why_it_matters": (
                        "If BOE encroachment permit is conditioned on LADOT TMP approval, and LADOT "
                        "has a separate 4–6 week review, the combined lead time may exceed 12 weeks "
                        "before a notice to proceed can be issued."
                    ),
                    "recommended_next_step": (
                        "Prepare a permitting matrix with submission dates and expected approval dates "
                        "for each agency. Identify the critical-path permit and initiate that application first."
                    ),
                    "confidence": "Medium",
                    "assumptions": [
                        "No Caltrans right-of-way is involved; project is entirely within city streets.",
                        "Project does not cross a Metro Rail or Bus Rapid Transit corridor requiring separate MTA approval.",
                    ],
                },
                {
                    "category": "Environmental",
                    "insight": (
                        "The project will likely qualify for a CEQA Categorical Exemption under "
                        "Class 1 (Existing Facilities) or Class 2 (Replacement/Reconstruction), "
                        "but this must be confirmed by the lead agency and documented in a Notice "
                        "of Exemption (NOE)."
                    ),
                    "risk_level": "Low",
                    "why_it_matters": (
                        "If the exemption is challenged or an unusual circumstance applies (e.g., "
                        "adjacent to a historic district, proximity to a creek), CEQA review could "
                        "trigger an Initial Study and delay the project 3–6 months."
                    ),
                    "recommended_next_step": (
                        "Have the lead agency (likely LA BOE or LADWP) confirm applicability of "
                        "the categorical exemption in writing and file the NOE with the State "
                        "Clearinghouse promptly."
                    ),
                    "confidence": "Medium",
                    "assumptions": [
                        "Project replaces existing infrastructure in kind with no increase in capacity.",
                        "No sensitive biological, cultural, or archaeological resources are known in the corridor.",
                        "Project is not located in a Hillside Area or within a Specific Plan with enhanced CEQA triggers.",
                    ],
                },
                {
                    "category": "Utility Conflict",
                    "insight": (
                        "Urban LA corridors typically contain dense subsurface infrastructure from "
                        "SoCalGas, Southern California Edison (SCE), AT&T, Spectrum, and LADWP "
                        "electrical conduit in addition to the water main being replaced. Potholing "
                        "will likely be required to verify depths and horizontal clearances."
                    ),
                    "risk_level": "High",
                    "why_it_matters": (
                        "Undisclosed conflicts discovered during construction are a leading cause of "
                        "change orders, schedule delays, and utility damage claims. California "
                        "Government Code §4216 (Dig Alert) requires notification but record accuracy "
                        "varies significantly by utility owner."
                    ),
                    "recommended_next_step": (
                        "Submit Dig Alert (811) notification and request as-built records from all "
                        "utility owners. Budget for soft-dig potholing at all major intersections "
                        "and utility crossings during design."
                    ),
                    "confidence": "High",
                    "assumptions": [
                        "No utility atlas or SUE (Subsurface Utility Engineering) study has been completed yet.",
                        "Existing LADWP water main records may be incomplete for laterals installed prior to 1980.",
                    ],
                },
                {
                    "category": "Schedule",
                    "insight": (
                        "If the project corridor is classified as a 'Moratorium Street' by LA BOE "
                        "(recently repaved within 5 years), open-cut trenching may be restricted "
                        "or require additional pavement restoration standards, potentially adding "
                        "cost and requiring a variance."
                    ),
                    "risk_level": "Medium",
                    "why_it_matters": (
                        "Moratorium streets require full-width pavement restoration or may prohibit "
                        "open-cut entirely, forcing a trenchless alternative (e.g., pipe bursting, "
                        "CIPP) that significantly changes the project scope and cost."
                    ),
                    "recommended_next_step": (
                        "Check LA BOE's online Moratorium Street viewer for each block in the "
                        "project corridor before finalizing the construction method."
                    ),
                    "confidence": "Medium",
                    "assumptions": [
                        "The specific street segments have not yet been checked against the LA BOE moratorium database.",
                    ],
                },
            ],
            "missing_information": [
                "Exact street address(es) or APN(s) to confirm jurisdiction and moratorium street status.",
                "Whether any portion of the alignment crosses a Caltrans right-of-way or state highway.",
                "Total project area of ground disturbance (for NPDES CGP threshold determination).",
                "Proximity to any waterways, flood control channels, or LA County DPW-maintained infrastructure.",
                "Whether existing mains are known to contain asbestos cement pipe (ACP), triggering Cal/OSHA and air district requirements.",
                "Project funding source (federal funds trigger additional environmental review under NEPA).",
                "Whether a City-issued franchise agreement or license agreement exists for the water main corridor.",
            ],
            "disclaimer": "This is a planning-support analysis, not legal or permitting advice.",
        }


class AnthropicLLMClient(LLMClient):
    def __init__(self, model: str = "claude-opus-4-5") -> None:
        import anthropic

        self._client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self._model = model

    def analyze(self, project_description: str) -> dict:
        message = self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": build_user_prompt(project_description),
                }
            ],
        )
        raw = message.content[0].text.strip()
        return json.loads(raw)


def get_client(force_mock: bool = False) -> LLMClient:
    if force_mock or not os.environ.get("ANTHROPIC_API_KEY"):
        return MockLLMClient()
    return AnthropicLLMClient()
