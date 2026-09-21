"""The published artifact, tested as the surface for readers who cannot clone.

The Claude Artifact preview is the fallback when GitHub Pages is unreachable,
which makes it the only way into this material in some environments. A
reference it cannot open is a dead end there, not a cosmetic flaw -- so these
assert that every link resolves to something, by one of the three routes the
builder is allowed to take.
"""

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

markdown = pytest.importorskip("markdown", reason="artifact preview needs the docs extra")

from build_artifact_preview import (
    REPOSITORY_URL,
    build_pages,
    rewrite_xrefs,
)

# --- the three outcomes a link may have --------------------------------------


def test_a_link_to_a_page_in_the_artifact_becomes_an_in_page_xref():
    out = rewrite_xrefs('<a href="./duration.md">Duration</a>', "fixed_income/dv01.md")
    assert 'class="xref"' in out
    assert 'href="#ref-fixed_income-duration"' in out


def test_a_link_to_a_real_file_not_in_the_artifact_becomes_a_github_link():
    """Previously unwrapped to plain text. A link that opens the notebook is
    better than prose, and better than a dead relative path."""
    out = rewrite_xrefs(
        '<a href="../../notebooks/fixed_income/08_bond_math.ipynb">Notebook</a>',
        "fixed_income/duration.md",
    )
    assert f"{REPOSITORY_URL}/blob/main/notebooks/fixed_income/08_bond_math.ipynb" in out


def test_a_link_to_nothing_is_unwrapped_rather_than_pointed_at_a_404():
    out = rewrite_xrefs(
        '<a href="../../notebooks/does_not_exist.ipynb">Gone</a>',
        "fixed_income/duration.md",
    )
    assert "<a" not in out
    assert "Gone" in out


def test_an_absolute_url_is_left_alone():
    original = '<a href="https://example.com/x">x</a>'
    assert rewrite_xrefs(original, "fixed_income/duration.md") == original


def test_a_fragment_on_a_github_link_is_preserved():
    out = rewrite_xrefs(
        '<a href="../../README.md#start-here">Start</a>', "fixed_income/duration.md"
    )
    assert "/blob/main/README.md#start-here" in out


def test_links_resolve_from_pages_outside_reference():
    """The three page types built without link handling were where every dead
    link lived: the overview, the curriculum, and the use cases."""
    out = rewrite_xrefs(
        '<a href="../../reference/glossary.md">Glossary</a>',
        "README.md",
        "curriculum/bootcamp_01_foundations",
    )
    assert 'class="xref"' in out


# --- the built artifact as a whole -------------------------------------------


def _links(pages):
    for page in pages:
        for match in re.finditer(r'<a ([^>]*)href="([^"]+)"([^>]*)>', page["html"]):
            yield page["id"], match.group(1) + match.group(3), match.group(2)


def test_the_artifact_has_no_dead_relative_links():
    pages = build_pages()
    ids = {p["id"] for p in pages}
    dead = []
    for page_id, attrs, href in _links(pages):
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        if "xref" in attrs and href.startswith("#") and href[1:] in ids:
            continue
        dead.append((page_id, href))
    assert not dead, f"dead links in the artifact: {sorted(set(dead))[:10]}"


def test_every_github_link_points_at_a_file_that_exists():
    prefix = f"{REPOSITORY_URL}/blob/main/"
    missing = []
    for _, _, href in _links(build_pages()):
        if href.startswith(prefix):
            target = href[len(prefix) :].split("#")[0]
            if not (ROOT / target).exists():
                missing.append(target)
    assert not missing, f"artifact links to missing files: {sorted(set(missing))}"


def test_every_xref_targets_a_page_the_artifact_contains():
    pages = build_pages()
    ids = {p["id"] for p in pages}
    broken = [
        (pid, href)
        for pid, attrs, href in _links(pages)
        if "xref" in attrs and href.startswith("#") and href[1:] not in ids
    ]
    assert not broken, f"xrefs to absent pages: {broken}"


def test_the_artifact_covers_every_reference_page_the_readme_claims():
    from reference_taxonomy import TITLES

    ids = {p["id"] for p in build_pages()}
    missing = [
        key for key in TITLES if "ref-" + key.replace(".md", "").replace("/", "-") not in ids
    ]
    assert not missing, f"reference pages absent from the artifact: {missing}"
