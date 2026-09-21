import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_committed_tool_schema_is_up_to_date():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_tool_schema.py")],
        capture_output=True,
        text=True,
        check=True,
        cwd=ROOT,
    )
    generated = json.loads(result.stdout)
    committed = json.loads((ROOT / "docs" / "tool_schema.json").read_text())
    assert generated == committed, (
        "docs/tool_schema.json is stale - regenerate with "
        "`python scripts/generate_tool_schema.py > docs/tool_schema.json`"
    )


def test_tool_schema_covers_every_public_pm_module():
    schema = json.loads((ROOT / "docs" / "tool_schema.json").read_text())
    modules = {tool["module"] for tool in schema["tools"]}
    for expected in ["pm.returns", "pm.risk", "pm.fixed_income.bond", "pm.fx", "pm.robust"]:
        assert expected in modules
