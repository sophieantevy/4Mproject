from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from schemas import PermitAnalysis, RiskLevel

console = Console()

_RISK_COLORS = {
    RiskLevel.high: "bold red",
    RiskLevel.medium: "bold yellow",
    RiskLevel.low: "bold green",
}

_CONFIDENCE_COLORS = {
    "High": "green",
    "Medium": "yellow",
    "Low": "red",
}


def _risk_badge(level: RiskLevel) -> Text:
    return Text(level.value, style=_RISK_COLORS[level])


def print_analysis(analysis: PermitAnalysis, source_label: str = "") -> None:
    header_text = "[bold cyan]Permitting & Risk Intelligence Engine[/bold cyan]"
    if source_label:
        header_text += f"  [dim]({source_label})[/dim]"
    console.print(Panel(header_text, expand=False))

    console.print()
    console.print(
        Panel(
            f"[bold]{analysis.project_summary}[/bold]\n\n"
            f"Overall Risk: {_risk_badge(analysis.overall_risk_level)}",
            title="Project Summary",
            border_style="cyan",
        )
    )

    console.print()

    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold white on dark_blue",
        expand=True,
        title="[bold]Insights[/bold]",
        title_style="bold cyan",
    )
    table.add_column("Category", style="bold", min_width=14, no_wrap=True)
    table.add_column("Insight", min_width=30)
    table.add_column("Risk", justify="center", min_width=8, no_wrap=True)
    table.add_column("Confidence", justify="center", min_width=10, no_wrap=True)
    table.add_column("Why It Matters", min_width=28)
    table.add_column("Next Step", min_width=28)

    for insight in analysis.insights:
        confidence_style = _CONFIDENCE_COLORS.get(insight.confidence.value, "white")
        assumptions_note = ""
        if insight.assumptions:
            assumptions_note = "\n[dim]Assumes: " + "; ".join(insight.assumptions) + "[/dim]"

        table.add_row(
            insight.category.value,
            insight.insight + assumptions_note,
            _risk_badge(insight.risk_level),
            Text(insight.confidence.value, style=confidence_style),
            insight.why_it_matters,
            insight.recommended_next_step,
        )

    console.print(table)

    if analysis.missing_information:
        console.print()
        missing_table = Table(
            box=box.SIMPLE,
            show_header=True,
            header_style="bold white on dark_red",
            title="[bold]Missing Information Needed for Full Analysis[/bold]",
            title_style="bold red",
            expand=True,
        )
        missing_table.add_column("#", justify="right", style="dim", no_wrap=True, min_width=3)
        missing_table.add_column("Item")
        for i, item in enumerate(analysis.missing_information, 1):
            missing_table.add_row(str(i), item)
        console.print(missing_table)

    console.print()
    console.print(
        Panel(
            f"[dim italic]{analysis.disclaimer}[/dim italic]",
            border_style="dim",
            expand=False,
        )
    )
