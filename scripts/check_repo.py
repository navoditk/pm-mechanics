import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]

required = [
    "README.md","ROADMAP.md","LEARNING_PATHS.md","AGENTS.md",
    "reference/index.md","use_cases/index.md","tutors/README.md"
]
for rel in required:
    p = root/rel
    assert p.exists(), f"Missing {rel}"

nbs = list((root/"notebooks").rglob("*.ipynb"))
assert len(nbs) >= 12
for p in nbs:
    json.loads(p.read_text())


def check_mastery():
    """Validate docs/mastery.md's rung/status/XP consistency.

    /pmexpert derives what to teach next from this table, so a malformed or
    self-contradicting row silently misroutes the curriculum rather than
    failing loudly. The specific case this exists to catch is real: the
    duration row sat at `confirmed` with `····` rungs -- claiming mastery
    while recording that nothing had been demonstrated.
    """
    path = root / "docs" / "mastery.md"
    # position -> the only letter legal there; "·" is always legal
    RUNGS = ("D", "A", "B", "E")
    errors = []
    rows = 0

    for n, line in enumerate(path.read_text().split("\n"), 1):
        if not line.startswith("| ") or "reference/" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            errors.append(f"line {n}: expected 6 cells, found {len(cells)}")
            continue
        rows += 1
        concept, pages, status, rungs, xp, _ = cells

        if len(rungs) != len(RUNGS):
            errors.append(f"{concept}: Rungs must be {len(RUNGS)} characters, found {rungs!r}")
            continue
        for i, (got, want) in enumerate(zip(rungs, RUNGS, strict=True), 1):
            if got not in (want, "·"):
                errors.append(
                    f"{concept}: Rungs position {i} must be {want!r} or '·', found {got!r}"
                )

        cleared = sum(1 for c in rungs if c != "·")
        expected = "untested" if cleared == 0 else "confirmed" if cleared == len(RUNGS) else "weak"
        if status != expected:
            errors.append(
                f"{concept}: Rungs {rungs!r} imply status {expected!r}, found {status!r}"
            )

        if not xp.isdigit():
            errors.append(f"{concept}: XP must be a non-negative integer, found {xp!r}")

        for rel in re.findall(r"`([a-z0-9_]+/[a-z0-9_]+\.md)`", pages):
            if not (root / "reference" / rel).exists():
                errors.append(f"{concept}: reference page not found: {rel}")

    assert rows, "docs/mastery.md has no concept rows -- did its format change?"
    assert not errors, "docs/mastery.md is inconsistent:\n  " + "\n  ".join(errors)
    return rows


concepts = check_mastery()

print(
    f"Repository structure OK. {len(nbs)} notebooks validated. "
    f"{concepts} mastery rows consistent."
)
