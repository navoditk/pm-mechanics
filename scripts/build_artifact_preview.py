"""Build a single-file, searchable HTML preview of the curriculum for
publishing as a Claude Artifact - a companion to the full MkDocs site
(docs/OVERVIEW.md explains why both exist) for readers who can't reach
GitHub Pages at all. Covers reference pages, curriculum, and use cases;
notebooks and code live in the full docs site and the repo itself.

Section/subsection nesting and titles come from reference_taxonomy.py,
the same source reference/index.md and mkdocs.yml's nav follow, so all
three surfaces stay organized identically. Relative markdown links
between reference pages are rewritten into in-page navigation so
cross-references stay clickable inside the single-file artifact.

Refresh manually when content changes meaningfully (see AGENTS.md rule 14):
  python scripts/build_artifact_preview.py
Output is a gitignored build artifact; publish it with the Artifact tool
to the existing URL already linked from README.md.
"""

import json
import re
from pathlib import Path

import markdown
from reference_taxonomy import SECTIONS, TITLES, USE_CASES

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site_src" / "_artifact_preview.html"
TEMPLATE = Path(__file__).with_name("_artifact_preview_template.html")

MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]


def page_id(ref_key):
    """Stable in-page id for a reference page, e.g. concepts/covariance.md
    -> ref-concepts-covariance."""
    return "ref-" + ref_key.replace(".md", "").replace("/", "-")


def md_to_html(text):
    return markdown.markdown(text, extensions=MD_EXTENSIONS)


def strip_h1(text):
    lines = text.lstrip().split("\n")
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).lstrip("\n")
    return text


REPOSITORY_URL = "https://github.com/navoditk/pm-mechanics"

# Pages the artifact embeds that are not section entries in the taxonomy.
# Keyed by their path relative to `reference/`, valued by their page id.
STANDALONE_PAGE_IDS = {
    "glossary.md": "start-glossary",
}


def rewrite_xrefs(html_text, from_ref_key, from_root=None):
    """Resolve every relative link so nothing in the artifact is a dead end.

    The artifact is one standalone document, so a relative path to another
    file in the tree resolves to nothing. Three outcomes, in order:

    1. **A page the artifact contains** becomes an in-page `#anchor`
       (`class="xref"`, which the page script intercepts to navigate).
    2. **A real repository file the artifact does not contain** -- notebooks,
       `src/`, `use_cases/` READMEs -- becomes a GitHub link. This is the
       case that changed: these were previously unwrapped to plain text on
       the reasoning that a dead link is worse than none. True, but a link
       that opens the notebook is better than either, and it is the whole
       point of a preview someone reads when they cannot clone the repo.
    3. **Anything that resolves to no real file** is still unwrapped to
       plain text, so a renamed target degrades to prose instead of becoming
       a confident 404.

    `from_root` is the directory the source document lives in, relative to
    the repository root, so a link can be resolved from any page rather than
    only from `reference/`.
    """
    from_dir = Path(from_root or "reference") / Path(from_ref_key).parent

    def repl(m):
        href, label = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)

        anchor = ""
        if "#" in href:
            href, _, anchor = href.partition("#")
            anchor = f"#{anchor}"
        if not href:
            return m.group(0)

        parts = []
        for seg in (from_dir / href).as_posix().split("/"):
            if seg == "..":
                if parts:
                    parts.pop()
            elif seg not in (".", ""):
                parts.append(seg)
        target = "/".join(parts)

        reference_key = target.removeprefix("reference/")
        if reference_key in TITLES:
            return f'<a href="#{page_id(reference_key)}" class="xref">{label}</a>'
        # Pages the artifact carries outside the section taxonomy. The
        # glossary is embedded as `start-glossary` but is not in TITLES, so
        # checking TITLES alone sent every link to it out to GitHub when it
        # could navigate in place.
        if reference_key in STANDALONE_PAGE_IDS:
            return f'<a href="#{STANDALONE_PAGE_IDS[reference_key]}" class="xref">{label}</a>'

        resolved = ROOT / target
        if resolved.exists():
            kind = "tree" if resolved.is_dir() else "blob"
            return (
                f'<a href="{REPOSITORY_URL}/{kind}/main/{target}{anchor}"'
                f' target="_blank" rel="noopener">{label}</a>'
            )
        return label

    return re.sub(r'<a href="([^"]+)">(.*?)</a>', repl, html_text, flags=re.DOTALL)


def build_pages():
    pages = []

    overview = (ROOT / "docs" / "OVERVIEW.md").read_text()
    pages.append(
        {
            "id": "start-overview",
            "section": "Start Here",
            "subsection": None,
            "title": "Repository Overview",
            "html": rewrite_xrefs(md_to_html(strip_h1(overview)), "OVERVIEW.md", "docs"),
        }
    )

    glossary = (ROOT / "reference" / "glossary.md").read_text()
    pages.append(
        {
            "id": "start-glossary",
            "section": "Start Here",
            "subsection": None,
            "title": "Glossary",
            "html": rewrite_xrefs(md_to_html(strip_h1(glossary)), "glossary.md"),
        }
    )

    curriculum = (ROOT / "curriculum" / "bootcamp_01_foundations" / "README.md").read_text()
    pages.append(
        {
            "id": "start-curriculum",
            "section": "Start Here",
            "subsection": None,
            "title": "Curriculum (14-Day Bootcamp)",
            "html": rewrite_xrefs(
                md_to_html(strip_h1(curriculum)),
                "README.md",
                "curriculum/bootcamp_01_foundations",
            ),
        }
    )

    for section, subsection, items in SECTIONS:
        for ref_key, title in items:
            raw = (ROOT / "reference" / ref_key).read_text()
            body = rewrite_xrefs(md_to_html(strip_h1(raw)), ref_key)
            pages.append(
                {
                    "id": page_id(ref_key),
                    "section": section,
                    "subsection": subsection,
                    "title": title,
                    "html": body,
                }
            )

    for slug, title in USE_CASES:
        raw = (ROOT / "use_cases" / slug / "README.md").read_text()
        pages.append(
            {
                "id": f"usecase-{slug}",
                "section": "Use Cases",
                "subsection": None,
                "title": title,
                "html": rewrite_xrefs(md_to_html(strip_h1(raw)), "README.md", f"use_cases/{slug}"),
            }
        )

    return pages


def render(pages):
    data_json = json.dumps(pages)
    # Neutralize "<" so the JSON can never contain a literal "</script>".
    # < is a valid JSON escape, decoded correctly by JSON.parse.
    safe_json = data_json.replace("<", "\\u003c")
    return TEMPLATE.read_text().replace("__PAGES_JSON__", safe_json)


def main():
    pages = build_pages()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(pages))
    print(f"Wrote {OUT} ({len(pages)} pages, {OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
