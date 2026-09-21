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


def rewrite_xrefs(html_text, from_ref_key):
    """Turn relative .md links between reference pages into in-page
    anchors (#ref-...), since the artifact is one document rather than a
    directory tree. Links that don't resolve to a known reference page
    (notebooks, src/, resources/) are unwrapped to plain text - they'd
    be dead inside a standalone file, and a dead link is worse than none.
    """
    from_dir = Path(from_ref_key).parent

    def repl(m):
        href, label = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        parts = []
        for seg in (from_dir / href).as_posix().split("/"):
            if seg == "..":
                if parts:
                    parts.pop()
            elif seg not in (".", ""):
                parts.append(seg)
        target = "/".join(parts)
        if target in TITLES:
            return f'<a href="#{page_id(target)}" class="xref">{label}</a>'
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
            "html": md_to_html(strip_h1(overview)),
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
            "html": md_to_html(strip_h1(curriculum)),
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
                "html": md_to_html(strip_h1(raw)),
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
