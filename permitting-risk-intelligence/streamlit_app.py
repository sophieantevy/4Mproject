import json
import os
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent / "src"))

from llm_client import get_client, MockLLMClient
from schemas import PermitAnalysis, RiskLevel

DATA_FILE = Path(__file__).parent / "data" / "sample_projects.json"

RISK_COLORS = {
    "High": "#ef4444",
    "Medium": "#f59e0b",
    "Low": "#22c55e",
}

RISK_BG = {
    "High": "#fef2f2",
    "Medium": "#fffbeb",
    "Low": "#f0fdf4",
}

CATEGORY_ICONS = {
    "Permit": "📋",
    "Agency": "🏛️",
    "Coordination": "🔗",
    "Environmental": "🌿",
    "Utility Conflict": "⚡",
    "Schedule": "📅",
}


def load_samples():
    if DATA_FILE.exists():
        with DATA_FILE.open() as f:
            return json.load(f)
    return []


def risk_badge(level: str) -> str:
    color = RISK_COLORS.get(level, "#6b7280")
    bg = RISK_BG.get(level, "#f9fafb")
    return (
        f'<span style="background:{bg};color:{color};border:1px solid {color};'
        f'padding:2px 10px;border-radius:999px;font-size:0.78rem;font-weight:600;">'
        f'{level}</span>'
    )


def render_insight_card(insight, index: int):
    icon = CATEGORY_ICONS.get(insight.category.value, "•")
    risk_color = RISK_COLORS.get(insight.risk_level.value, "#6b7280")
    risk_bg = RISK_BG.get(insight.risk_level.value, "#f9fafb")
    conf_color = RISK_COLORS.get(insight.confidence.value, "#6b7280")

    assumptions_html = ""
    if insight.assumptions:
        items = "".join(f"<li>{a}</li>" for a in insight.assumptions)
        assumptions_html = f"""
        <div style="margin-top:10px;padding:8px 12px;background:#f8f7ff;border-radius:6px;
                    border-left:3px solid #c7d2fe;">
          <div style="font-size:0.72rem;font-weight:600;color:#6366f1;margin-bottom:4px;
                      text-transform:uppercase;letter-spacing:0.05em;">Assumes</div>
          <ul style="margin:0;padding-left:16px;color:#4b5563;font-size:0.82rem;">
            {items}
          </ul>
        </div>
        """

    st.markdown(
        f"""
        <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;
                    padding:18px 20px;margin-bottom:12px;
                    border-left:4px solid {risk_color};">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;
                      flex-wrap:wrap;gap:8px;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="font-size:1.1rem;">{icon}</span>
              <span style="font-weight:600;color:#1e1b4b;font-size:0.95rem;">
                {insight.category.value}
              </span>
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
              <span style="background:{risk_bg};color:{risk_color};border:1px solid {risk_color};
                           padding:2px 10px;border-radius:999px;font-size:0.75rem;font-weight:600;">
                {insight.risk_level.value} Risk
              </span>
              <span style="background:#f9fafb;color:{conf_color};border:1px solid {conf_color};
                           padding:2px 10px;border-radius:999px;font-size:0.75rem;font-weight:600;">
                {insight.confidence.value} Confidence
              </span>
            </div>
          </div>
          <p style="color:#111827;font-size:0.93rem;line-height:1.6;margin:0 0 10px 0;">
            {insight.insight}
          </p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px;">
            <div style="background:#fafafa;border-radius:8px;padding:10px 12px;">
              <div style="font-size:0.72rem;font-weight:600;color:#6b7280;margin-bottom:4px;
                          text-transform:uppercase;letter-spacing:0.05em;">Why it matters</div>
              <div style="color:#374151;font-size:0.85rem;line-height:1.5;">{insight.why_it_matters}</div>
            </div>
            <div style="background:#f0f9ff;border-radius:8px;padding:10px 12px;">
              <div style="font-size:0.72rem;font-weight:600;color:#0369a1;margin-bottom:4px;
                          text-transform:uppercase;letter-spacing:0.05em;">Next step</div>
              <div style="color:#0c4a6e;font-size:0.85rem;line-height:1.5;">
                {insight.recommended_next_step}
              </div>
            </div>
          </div>
          {assumptions_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_results(analysis: PermitAnalysis):
    risk_color = RISK_COLORS.get(analysis.overall_risk_level.value, "#6b7280")
    risk_bg = RISK_BG.get(analysis.overall_risk_level.value, "#f9fafb")

    st.markdown(
        f"""
        <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:14px;
                    padding:20px 24px;margin-bottom:24px;">
          <div style="font-size:0.75rem;font-weight:600;color:#6366f1;text-transform:uppercase;
                      letter-spacing:0.08em;margin-bottom:8px;">Project Summary</div>
          <p style="font-size:1.05rem;color:#1e1b4b;line-height:1.6;margin:0 0 14px 0;">
            {analysis.project_summary}
          </p>
          <span style="background:{risk_bg};color:{risk_color};border:1.5px solid {risk_color};
                       padding:4px 14px;border-radius:999px;font-size:0.85rem;font-weight:700;">
            Overall Risk: {analysis.overall_risk_level.value}
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    high = [i for i in analysis.insights if i.risk_level == RiskLevel.high]
    medium = [i for i in analysis.insights if i.risk_level == RiskLevel.medium]
    low = [i for i in analysis.insights if i.risk_level == RiskLevel.low]

    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 High Risk", len(high))
    col2.metric("🟡 Medium Risk", len(medium))
    col3.metric("🟢 Low Risk", len(low))

    st.markdown("---")
    st.markdown("### Insights")

    if high:
        with st.expander(f"🔴 High Risk ({len(high)})", expanded=True):
            for i, insight in enumerate(high):
                render_insight_card(insight, i)

    if medium:
        with st.expander(f"🟡 Medium Risk ({len(medium)})", expanded=True):
            for i, insight in enumerate(medium):
                render_insight_card(insight, i)

    if low:
        with st.expander(f"🟢 Low Risk ({len(low)})", expanded=False):
            for i, insight in enumerate(low):
                render_insight_card(insight, i)

    if analysis.missing_information:
        st.markdown("---")
        st.markdown("### 📌 Missing Information")
        st.caption("Providing these details would sharpen the analysis.")
        for item in analysis.missing_information:
            st.markdown(f"- {item}")

    st.markdown("---")
    st.caption(f"_{analysis.disclaimer}_")

    output = json.dumps(analysis.model_dump(), indent=2)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="⬇️ Download JSON",
        data=output,
        file_name=f"prie_analysis_{timestamp}.json",
        mime="application/json",
    )


def main():
    st.set_page_config(
        page_title="Permitting & Risk Intelligence Engine",
        page_icon="🏗️",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        .block-container { padding-top: 2rem; max-width: 960px; }
        h1 { color: #1e1b4b; }
        .stTextArea textarea { font-size: 0.95rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🏗️ Permitting & Risk Intelligence Engine")
    st.caption(
        "Describe a California utility or civil infrastructure project "
        "and get an instant structured permitting risk analysis."
    )

    samples = load_samples()

    with st.sidebar:
        st.markdown("### ⚙️ Settings")

        api_key_input = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-... (leave blank for demo mode)",
            help="If left blank, the tool runs in demo mode with realistic sample output.",
        )
        if api_key_input:
            os.environ["ANTHROPIC_API_KEY"] = api_key_input

        using_mock = not os.environ.get("ANTHROPIC_API_KEY")
        if using_mock:
            st.info("Running in **demo mode** — no API key needed.", icon="🤖")
        else:
            st.success("API key set — using Claude.", icon="✅")

        st.markdown("---")
        st.markdown("### 📂 Sample Projects")
        st.caption("Click to load a sample into the description box.")
        for i, s in enumerate(samples):
            if st.button(s["name"], key=f"sample_{i}", use_container_width=True):
                st.session_state["desc_text"] = s["description"]
                st.session_state["sample_name"] = s["name"]
                st.rerun()

        st.markdown("---")
        st.markdown(
            "<div style='font-size:0.75rem;color:#9ca3af;'>"
            "Not legal or permitting advice. For planning support only."
            "</div>",
            unsafe_allow_html=True,
        )

    if "desc_text" not in st.session_state:
        st.session_state["desc_text"] = ""

    description = st.text_area(
        "Project Description",
        key="desc_text",
        height=180,
        placeholder=(
            "e.g. Replace 1,800 LF of 12-inch cast-iron water main along Venice Blvd "
            "in Los Angeles, CA. Open-cut trenching in city ROW, reconnect 40 service "
            "laterals, full pavement restoration. Funded by LADWP capital program."
        ),
    )

    analyze_clicked = st.button("Analyze Project →", type="primary", use_container_width=False)

    if analyze_clicked:
        if not description.strip():
            st.warning("Please enter a project description or load a sample from the sidebar.")
            return

        with st.spinner("Analyzing permitting risks..."):
            try:
                client = get_client(force_mock=using_mock)
                raw = client.analyze(description)
                analysis = PermitAnalysis.model_validate(raw)
                st.session_state["last_analysis"] = analysis
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                return

    if "last_analysis" in st.session_state:
        render_results(st.session_state["last_analysis"])


if __name__ == "__main__":
    main()
