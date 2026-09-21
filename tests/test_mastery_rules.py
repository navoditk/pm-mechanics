"""Tests for the depth-ladder bookkeeping.

The ladder's assessment half needs a human. This half does not: status
derivation, rung transitions, and the level ladder are pure functions, and
they are where a silent arithmetic bug would sit unnoticed — the level table
shipped once with a gap where 85 confirmed mapped to no level at all.

The last two tests are the ones that earn their keep: they assert the prose
tables in `skills/pmexpert/SKILL.md` still match this module. The
skill is the copy a human edits, so that is where drift starts.
"""

import re
import sys
from itertools import product
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from mastery_rules import (
    LEVEL_BANDS,
    MASTER_LEVEL,
    NOT_CLEARED,
    RUNGS,
    UNTOUCHED,
    XP_AWARDS,
    clear_rung,
    format_rungs,
    level_for,
    next_rung,
    parse_rungs,
    reset_from,
    status_for,
)

SKILL = (ROOT / "skills" / "pmexpert" / "SKILL.md").read_text()


# --- status derivation -------------------------------------------------------


def test_status_is_derived_for_every_possible_rung_combination():
    """All 16 combinations, not a sampled few — the whole domain is small."""
    for flags in product([False, True], repeat=len(RUNGS)):
        rungs = format_rungs(flags)
        expected = "untested" if not any(flags) else "confirmed" if all(flags) else "weak"
        assert status_for(rungs) == expected, rungs


def test_a_single_cleared_rung_is_weak_not_confirmed():
    """The bug this whole mechanism exists to prevent."""
    for rung in RUNGS:
        assert status_for(clear_rung(UNTOUCHED, rung)) == "weak"


def test_only_all_four_confirms():
    rungs = UNTOUCHED
    for rung in RUNGS[:-1]:
        rungs = clear_rung(rungs, rung)
        assert status_for(rungs) == "weak"
    assert status_for(clear_rung(rungs, RUNGS[-1])) == "confirmed"


# --- parsing and formatting --------------------------------------------------


@pytest.mark.parametrize("bad", ["", "DAB", "DABEE", "DA·", "XABE", "dabe", "D-B-"])
def test_malformed_rung_strings_raise(bad):
    with pytest.raises(ValueError):
        parse_rungs(bad)


def test_a_letter_in_the_wrong_column_raises():
    """Order is fixed: `AD··` is not a reordering of `DA··`, it is malformed."""
    with pytest.raises(ValueError, match="position 1"):
        parse_rungs("AD··")


def test_parse_and_format_round_trip():
    for flags in product([False, True], repeat=len(RUNGS)):
        assert parse_rungs(format_rungs(flags)) == flags


# --- transitions -------------------------------------------------------------


def test_clearing_is_idempotent_so_repeating_a_rung_earns_nothing():
    once = clear_rung(UNTOUCHED, "B")
    assert clear_rung(once, "B") == once


def test_rungs_can_be_cleared_out_of_order():
    """`D·B·` is legal: derived and broken, never applied or explained."""
    rungs = clear_rung(clear_rung(UNTOUCHED, "D"), "B")
    assert rungs == "D·B·"
    assert status_for(rungs) == "weak"


def test_reset_from_clears_that_rung_and_every_later_one():
    """A gap found under application discredits what came after it."""
    assert reset_from("DABE", "A") == "D···"
    assert reset_from("DABE", "D") == UNTOUCHED
    assert reset_from("DABE", "E") == "DAB·"


def test_reset_leaves_earlier_rungs_alone():
    assert reset_from("DABE", "B") == "DA··"


def test_next_rung_resumes_at_the_gap_rather_than_restarting():
    assert next_rung(UNTOUCHED) == "D"
    assert next_rung("DA··") == "B"
    assert next_rung("D·B·") == "A"
    assert next_rung("DABE") is None


# --- level ladder ------------------------------------------------------------


def test_level_bands_are_contiguous_with_no_unreachable_count():
    """The shipped bug: a banding that left 85 confirmed mapping to no level.

    Every count from 0 to total must resolve, so walking them must never
    raise and must never skip.
    """
    total = 86
    seen = [level_for(n, total) for n in range(total + 1)]
    assert len(seen) == total + 1
    assert seen[0] == LEVEL_BANDS[0][1]
    assert seen[-1] == MASTER_LEVEL
    assert seen[-2] == LEVEL_BANDS[-1][1], "the count just below total must sit in the last band"


def test_level_changes_exactly_at_each_band_boundary():
    total = 86
    for minimum, name in LEVEL_BANDS[1:]:
        assert level_for(minimum, total) == name
        assert level_for(minimum - 1, total) != name


def test_master_requires_every_concept_not_just_the_top_band():
    total = 86
    assert level_for(total, total) == MASTER_LEVEL
    assert level_for(total - 1, total) != MASTER_LEVEL


def test_nonsensical_counts_raise():
    for confirmed, total in [(-1, 86), (87, 86), (5, -1)]:
        with pytest.raises(ValueError):
            level_for(confirmed, total)


# --- anti-drift: the skill's prose must match this module --------------------


def test_skill_xp_table_matches_the_module():
    """If someone edits the skill's XP table and not this module, fail here."""
    table = re.search(r"\| Earned by \| XP \|\n\s*\|[-|]+\|\n((?:\s*\|.*\|\n)+)", SKILL)
    assert table, "could not find the XP table in the skill — did its format change?"
    stated = {
        int(m.group(2)) for m in re.finditer(r"\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|", table.group(1))
    }
    assert stated == set(XP_AWARDS.values()), (
        f"skill XP values {sorted(stated)} != module {sorted(set(XP_AWARDS.values()))}"
    )


def test_skill_level_table_matches_the_module():
    """Same for the level ladder, including the master row's total."""
    table = re.search(r"\| Confirmed \| Level \|\n\s*\|[-|]+\|\n((?:\s*\|.*\|\n)+)", SKILL)
    assert table, "could not find the level table in the skill"
    rows = re.findall(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|", table.group(1))

    banded = [(r, name) for r, name in rows if "–" in r]
    assert len(banded) == len(LEVEL_BANDS), (
        f"skill lists {len(banded)} bands, module defines {len(LEVEL_BANDS)}"
    )
    for (rng, name), (minimum, expected) in zip(banded, LEVEL_BANDS, strict=True):
        assert name == expected, f"band name drift: skill {name!r} vs module {expected!r}"
        assert int(rng.split("–")[0]) == minimum, f"band start drift for {name}"

    master = [(r, name) for r, name in rows if "all" in r]
    assert len(master) == 1 and master[0][1] == MASTER_LEVEL


def test_skill_documents_the_rung_letters_this_module_uses():
    for letter, name in zip(RUNGS, ("Derive", "Apply", "Break", "Explain"), strict=True):
        assert f"`{letter}`" in SKILL, f"skill never mentions rung letter {letter}"
        assert name in SKILL, f"skill never mentions rung name {name}"
    assert NOT_CLEARED in SKILL, "skill never shows the not-cleared character"
