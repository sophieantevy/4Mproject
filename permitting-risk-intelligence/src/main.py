#!/usr/bin/env python3
"""Permitting & Risk Intelligence Engine — CLI entrypoint."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError
from rich.console import Console

from formatter import print_analysis
from llm_client import get_client
from schemas import PermitAnalysis

load_dotenv()

console = Console(stderr=True)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "data" / "sample_projects.json"
OUTPUTS_DIR = REPO_ROOT / "outputs"


def load_sample_projects() -> list[dict]:
    if not DATA_FILE.exists():
        console.print(f"[red]Sample data file not found: {DATA_FILE}[/red]")
        sys.exit(1)
    with DATA_FILE.open() as f:
        return json.load(f)


def pick_sample(index: int | None) -> tuple[str, str]:
    projects = load_sample_projects()
    if not projects:
        console.print("[red]No sample projects found in data file.[/red]")
        sys.exit(1)
    if index is None:
        index = 0
    if index >= len(projects):
        console.print(
            f"[red]Sample index {index} out of range. {len(projects)} project(s) available (0-indexed).[/red]"
        )
        sys.exit(1)
    project = projects[index]
    return project["name"], project["description"]


def save_output(analysis: PermitAnalysis, project_name: str) -> Path:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in project_name)[:40]
    filename = OUTPUTS_DIR / f"{timestamp}_{safe_name}.json"
    with filename.open("w") as f:
        json.dump(analysis.model_dump(), f, indent=2)
    return filename


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prie",
        description="Permitting & Risk Intelligence Engine — analyze infrastructure projects for permitting risks.",
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "description",
        nargs="?",
        help="Plain-English project description (wrap in quotes).",
    )
    input_group.add_argument(
        "--sample",
        metavar="INDEX",
        nargs="?",
        const=0,
        type=int,
        help="Use a sample project from data/sample_projects.json. Optionally specify index (default 0).",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Force mock mode regardless of whether an API key is set.",
    )
    parser.add_argument(
        "--list-samples",
        action="store_true",
        help="List available sample projects and exit.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_samples:
        projects = load_sample_projects()
        console.print("[bold cyan]Available sample projects:[/bold cyan]")
        for i, p in enumerate(projects):
            console.print(f"  [bold]{i}[/bold] — {p['name']}")
        sys.exit(0)

    using_mock = args.mock or not os.environ.get("ANTHROPIC_API_KEY")
    if using_mock and not args.mock:
        console.print(
            "[yellow]ANTHROPIC_API_KEY not set — running in mock mode.[/yellow]"
        )

    if args.sample is not None:
        project_name, description = pick_sample(args.sample)
        source_label = f"Sample: {project_name}"
        if using_mock:
            console.print(
                f"[dim]Using sample project: {project_name}[/dim]"
            )
    elif args.description:
        description = args.description
        project_name = "custom_project"
        source_label = "Custom input"
    else:
        console.print(
            "[red]Provide a project description or use --sample. Run with --help for usage.[/red]"
        )
        sys.exit(1)

    client = get_client(force_mock=args.mock)
    mode_label = "mock" if isinstance(client, __import__("llm_client").MockLLMClient) else "Anthropic API"
    console.print(f"[dim]Analyzing project using {mode_label}...[/dim]")

    try:
        raw = client.analyze(description)
    except Exception as exc:
        console.print(f"[red]LLM call failed: {exc}[/red]")
        sys.exit(1)

    try:
        analysis = PermitAnalysis.model_validate(raw)
    except ValidationError as exc:
        console.print("[red]Response failed schema validation:[/red]")
        console.print(exc)
        console.print("[dim]Raw response:[/dim]")
        console.print(json.dumps(raw, indent=2))
        sys.exit(1)

    print_analysis(analysis, source_label=source_label)

    out_path = save_output(analysis, project_name)
    console.print(f"\n[green]Output saved:[/green] {out_path}")


if __name__ == "__main__":
    main()
