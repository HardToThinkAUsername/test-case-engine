"""测试用例生成引擎 CLI。"""

from __future__ import annotations

import json
from pathlib import Path

import typer

from test_case_engine.services.session_service import SessionService
from test_case_engine.utils.excel_exporter import export_to_excel

app = typer.Typer(
    no_args_is_help=True,
    help="AI-powered test case generation from requirement documents.",
)


def _get_session(project_dir: str) -> SessionService:
    return SessionService(project_dir)


@app.command()
def init(
    project_name: str = typer.Option(..., help="Project name"),
    project_dir: str = typer.Option(".test-case", help="Project directory"),
) -> None:
    """Initialize test case generation project."""
    session = _get_session(project_dir)
    session.ensure_project_dir()

    # 读取constitution模板并适配
    constitution_path = Path(__file__).parent.parent.parent / "prompts" / "constitution.md"
    if constitution_path.exists():
        content = constitution_path.read_text(encoding="utf-8")
        session.save_constitution(content)
        typer.echo(f"Project initialized: {project_name}")
        typer.echo(f"Constitution saved to: {project_dir}/constitution.md")
    else:
        typer.echo("Warning: constitution template not found")


@app.command()
def status(
    project_dir: str = typer.Option(".test-case", help="Project directory"),
) -> None:
    """Show current project status."""
    session = _get_session(project_dir)
    status = session.get_status()

    typer.echo("## Project Status\n")
    for key, exists in status.items():
        label = key.replace("has_", "").replace("_", " ").title()
        icon = "✅" if exists else "❌"
        typer.echo(f"  {icon} {label}")


@app.command()
def model(
    document: Path = typer.Option(..., exists=True, readable=True, help="Requirement document path"),
    project_dir: str = typer.Option(".test-case", help="Project directory"),
) -> None:
    """Business modeling from requirement document.

    This command reads the requirement document and builds a business tree.
    The actual modeling is done by the AI agent following the extraction guide.
    """
    session = _get_session(project_dir)

    typer.echo(f"## Business Modeling")
    typer.echo(f"Document: {document}")
    typer.echo(f"Project dir: {project_dir}")
    typer.echo("")
    typer.echo("The AI agent should now:")
    typer.echo("1. Parse the requirement document")
    typer.echo("2. Identify entry points")
    typer.echo("3. Trace business flows")
    typer.echo("4. Identify branch points")
    typer.echo("5. Build business tree")
    typer.echo("6. Generate L1-L4 scenarios")
    typer.echo("7. Run breadth inquiry until convergence")
    typer.echo("")
    typer.echo("Save result to: .test-case/business_tree.json")


@app.command()
def review(
    adjustment: str = typer.Option(None, help="User adjustment description"),
    project_dir: str = typer.Option(".test-case", help="Project directory"),
) -> None:
    """Review requirements based on business tree."""
    session = _get_session(project_dir)
    tree = session.load_business_tree()

    if tree is None:
        typer.echo("Error: business tree not found. Run 'model' first.")
        raise typer.Exit(code=1)

    typer.echo("## Requirement Review")
    if adjustment:
        typer.echo(f"Adjustment: {adjustment}")
    typer.echo("")
    typer.echo("The AI agent should now:")
    typer.echo("1. Load business tree")
    typer.echo("2. Run 5-dimension review")
    typer.echo("3. Output review result")
    typer.echo("")
    typer.echo("Save result to: .test-case/review_result.json")


@app.command()
def outline(
    project_dir: str = typer.Option(".test-case", help="Project directory"),
) -> None:
    """Build test outline from confirmed business tree."""
    session = _get_session(project_dir)
    tree = session.load_business_tree()

    if tree is None:
        typer.echo("Error: business tree not found. Run 'model' first.")
        raise typer.Exit(code=1)

    typer.echo("## Build Test Outline")
    typer.echo("")
    typer.echo("The AI agent should now:")
    typer.echo("1. Load business tree and review result")
    typer.echo("2. Organize test points by module")
    typer.echo("3. Annotate priority and source layer")
    typer.echo("")
    typer.echo("Save result to: .test-case/outline.json")


@app.command()
def generate(
    module: str = typer.Option(None, help="Only generate cases for specified module"),
    project_dir: str = typer.Option(".test-case", help="Project directory"),
) -> None:
    """Generate test cases from outline."""
    session = _get_session(project_dir)
    outline = session.load_outline()

    if outline is None:
        typer.echo("Error: outline not found. Run 'outline' first.")
        raise typer.Exit(code=1)

    typer.echo("## Generate Test Cases")
    if module:
        typer.echo(f"Module: {module}")
    typer.echo("")
    typer.echo("The AI agent should now:")
    typer.echo("1. Load outline and business tree")
    typer.echo("2. Generate test cases for each test point")
    typer.echo("3. Run breadth inquiry")
    typer.echo("4. Deduplicate and validate")
    typer.echo("")
    typer.echo("Save result to: .test-case/test_cases.json")


@app.command()
def export(
    output: Path = typer.Option(Path(".test-case/test_cases.xlsx"), help="Output Excel path"),
    project_dir: str = typer.Option(".test-case", help="Project directory"),
) -> None:
    """Export test cases to Excel."""
    session = _get_session(project_dir)
    cases_data = session.load_test_cases()

    if cases_data is None:
        typer.echo("Error: test cases not found. Run 'generate' first.")
        raise typer.Exit(code=1)

    test_cases = cases_data.get("test_cases", [])
    if not test_cases:
        typer.echo("Error: no test cases found.")
        raise typer.Exit(code=1)

    output_path = export_to_excel(test_cases, output)
    typer.echo(f"## Excel Exported")
    typer.echo(f"File: {output_path}")
    typer.echo(f"Cases: {len(test_cases)}")


@app.command()
def explain(
    topic: str = typer.Argument(None, help="Topic: constitution, model, review, outline, generate, export"),
) -> None:
    """Explain the test case generation skill."""
    prompts_dir = Path(__file__).parent.parent.parent / "prompts"
    commands_dir = prompts_dir / "commands"

    if topic is None:
        typer.echo("""
# Test Case Generation Skill

## Core Goal

**Perfect** — Zero omissions, zero redundancy, zero false positives.

## Flow

1. **Init** — Create project constitution
2. **Model** — Business modeling from requirement document
3. **Review** — Requirement review (loop with user)
4. **Outline** — Build test outline
5. **Generate** — Generate test cases
6. **Export** — Export to Excel

## Commands

  test-case-engine init --project-name <name>
  test-case-engine model --document <path>
  test-case-engine review [--adjustment <text>]
  test-case-engine outline
  test-case-engine generate [--module <name>]
  test-case-engine export [--output <path>]
  test-case-engine status
""")
        return

    file_map = {
        "constitution": prompts_dir / "constitution.md",
        "model": commands_dir / "model.md",
        "review": commands_dir / "review.md",
        "outline": commands_dir / "outline.md",
        "generate": commands_dir / "generate.md",
        "export": commands_dir / "export.md",
    }

    if topic not in file_map:
        typer.echo(f"Unknown topic: {topic}")
        typer.echo("Available: constitution, model, review, outline, generate, export")
        raise typer.Exit(code=1)

    file_path = file_map[topic]
    if not file_path.exists():
        typer.echo(f"File not found: {file_path}")
        raise typer.Exit(code=1)

    content = file_path.read_text(encoding="utf-8")
    typer.echo(content)


if __name__ == "__main__":
    app()