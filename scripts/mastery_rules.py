"""Single source of truth for the /pmexpert depth ladder's bookkeeping.

`skills/pmexpert/SKILL.md` states these rules in prose for the agent
running a session, and `scripts/check_repo.py` enforces them against
`docs/mastery.md`. Without this module those are two independent copies of
the same rules, and `tests/test_mastery_rules.py` would be a third.

So the rules live here once, `check_repo.py` imports them, and the tests
assert that the skill's own tables still match — which is the check that
actually matters, since the skill is the copy a human edits.
"""

# Rung letters in their fixed column order. A cleared rung shows its letter;
# an outstanding one shows NOT_CLEARED.
RUNGS = ("D", "A", "B", "E")
RUNG_NAMES = ("Derive", "Apply", "Break", "Explain")
NOT_CLEARED = "·"  # MIDDLE DOT
UNTOUCHED = NOT_CLEARED * len(RUNGS)

# Mode that clears each rung, for routing and for error messages.
RUNG_MODES = {
    "D": "lesson",
    "A": "scenario",
    "B": "failure lab",
    "E": "teach-back",
}

# XP awarded once per item per concept. Mirrors the skill's table.
XP_AWARDS = {
    "lesson": 20,
    "quiz_correct": 10,
    "scenario": 25,
    "failure_lab": 25,
    "teachback": 30,
    "concept_confirmed": 50,
    "final_exam": 150,
}

# (minimum confirmed count, level). The final level requires *every* concept,
# so it is not expressible as a lower bound and is handled separately.
LEVEL_BANDS = (
    (0, "Trainee"),
    (14, "Analyst"),
    (28, "Associate PM"),
    (42, "Portfolio Manager"),
    (57, "Senior PM"),
    (71, "Desk Head"),
)
MASTER_LEVEL = "PM Mechanics Master"


def parse_rungs(rungs):
    """Return a tuple of booleans, one per rung. Raises on a malformed string."""
    if len(rungs) != len(RUNGS):
        raise ValueError(f"rungs must be {len(RUNGS)} characters, got {rungs!r}")
    cleared = []
    for position, (got, letter) in enumerate(zip(rungs, RUNGS, strict=True), start=1):
        if got == letter:
            cleared.append(True)
        elif got == NOT_CLEARED:
            cleared.append(False)
        else:
            raise ValueError(
                f"position {position} must be {letter!r} or {NOT_CLEARED!r}, got {got!r}"
            )
    return tuple(cleared)


def format_rungs(cleared):
    """Inverse of parse_rungs."""
    if len(cleared) != len(RUNGS):
        raise ValueError(f"expected {len(RUNGS)} flags, got {len(cleared)}")
    return "".join(
        letter if done else NOT_CLEARED for letter, done in zip(RUNGS, cleared, strict=True)
    )


def status_for(rungs):
    """Status is derived from the rungs, never set independently.

    This is the rule that duration's row violated before it was enforced:
    `confirmed` with nothing demonstrated.
    """
    cleared = parse_rungs(rungs)
    if not any(cleared):
        return "untested"
    if all(cleared):
        return "confirmed"
    return "weak"


def clear_rung(rungs, rung):
    """Mark one rung cleared. Idempotent — re-clearing earns nothing."""
    if rung not in RUNGS:
        raise ValueError(f"unknown rung {rung!r}; expected one of {RUNGS}")
    cleared = list(parse_rungs(rungs))
    cleared[RUNGS.index(rung)] = True
    return format_rungs(cleared)


def reset_from(rungs, rung):
    """Clear this rung and every later one.

    A gap surfacing under application is evidence an earlier rung was granted
    too easily, so the later ones stop being credible too.
    """
    if rung not in RUNGS:
        raise ValueError(f"unknown rung {rung!r}; expected one of {RUNGS}")
    cleared = list(parse_rungs(rungs))
    for index in range(RUNGS.index(rung), len(RUNGS)):
        cleared[index] = False
    return format_rungs(cleared)


def next_rung(rungs):
    """The first outstanding rung, or None when the concept is confirmed.

    Returning to a partly-done concept resumes here rather than restarting.
    """
    for letter, done in zip(RUNGS, parse_rungs(rungs), strict=True):
        if not done:
            return letter
    return None


def level_for(confirmed, total):
    """Level from the confirmed count. `total` matters only for the top band."""
    if confirmed < 0 or total < 0 or confirmed > total:
        raise ValueError(f"nonsensical counts: {confirmed}/{total}")
    if total and confirmed == total:
        return MASTER_LEVEL
    level = LEVEL_BANDS[0][1]
    for minimum, name in LEVEL_BANDS:
        if confirmed >= minimum:
            level = name
    return level
