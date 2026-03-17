#!/usr/bin/env python3
"""Generate repo-hosted SVG badges for local skills.

This script prefers direct parsing of public skill pages for weekly installs.
If a skill page does not expose data, it falls back to a search API lookup to
determine whether the skill is listed. Missing data is rendered explicitly as
neutral unknown/unlisted badges instead of guessed values.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any


DEFAULT_SOURCE_REPO = "NaNomicon/skills"
DEFAULT_BASE_URL = "https://skills.sh"
SKILL_FILE_NAME = "SKILL.md"
UNKNOWN = "unknown"
UNLISTED = "unlisted"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        cleaned = data.strip()
        if cleaned:
            self.parts.append(cleaned)

    def text_items(self) -> list[str]:
        return self.parts


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--output-dir", type=pathlib.Path, default=None)
    parser.add_argument("--source-repo", default=DEFAULT_SOURCE_REPO)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--fixtures", type=pathlib.Path, default=None)
    return parser.parse_args(argv)


def load_fixtures(path: pathlib.Path | None) -> dict[str, str]:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def discover_skills(repo_root: pathlib.Path) -> list[str]:
    skills: list[str] = []
    for child in sorted(repo_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if child.name in {"scripts", "tests", "badges"}:
            continue
        if (child / SKILL_FILE_NAME).exists():
            skills.append(child.name)
    return skills


def fetch_text(url: str, fixtures: dict[str, str]) -> str | None:
    if url in fixtures:
        return fixtures[url]
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "skill-badge-generator/1.0 (+https://github.com/NaNomicon/skills)",
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError):
        return None


def page_url(base_url: str, source_repo: str, skill_name: str) -> str:
    safe_skill = urllib.parse.quote(skill_name)
    return f"{base_url.rstrip('/')}/{source_repo}/{safe_skill}"


def search_url(base_url: str, skill_name: str) -> str:
    encoded = urllib.parse.urlencode({"q": skill_name})
    return f"{base_url.rstrip('/')}/api/search?{encoded}"


def parse_text_items(page: str) -> list[str]:
    parser = TextExtractor()
    parser.feed(page)
    return parser.text_items()


def find_value_after_label(items: list[str], label: str) -> str | None:
    lowered = label.lower()
    for index, item in enumerate(items):
        if item.lower() == lowered:
            for candidate in items[index + 1 :]:
                if candidate:
                    return candidate
    return None


def parse_weekly_installs(page: str | None) -> str:
    if not page:
        return UNKNOWN
    items = parse_text_items(page)
    value = find_value_after_label(items, "Weekly Installs")
    if not value:
        return UNKNOWN
    match = re.search(r"\d[\d,\.KkMm]*", value)
    return match.group(0) if match else UNKNOWN


def page_indicates_listing(page: str | None) -> bool | None:
    if not page:
        return None
    lowered = page.lower()
    if "skill not found" in lowered or "404" in lowered:
        return False
    return True


def normalize_audit_value(raw: str) -> str:
    value = raw.strip().lower()
    if value == "pass":
        return "pass"
    if value == "fail":
        return "fail"
    if "risk" in value:
        return value
    if "alert" in value:
        return value
    return value or UNKNOWN


def parse_security_audit(page: str | None) -> str:
    if not page:
        return UNKNOWN
    items = parse_text_items(page)
    try:
        start = items.index("Security Audits") + 1
    except ValueError:
        return UNKNOWN

    relevant: list[str] = []
    for item in items[start:]:
        lowered = item.lower()
        if item in {
            "Installed on",
            "Repository",
            "GitHub Stars",
            "First Seen",
            "Skill",
            "Skills",
        }:
            break
        if lowered in {"gen agent trust hub", "socket", "snyk"}:
            continue
        relevant.append(normalize_audit_value(item))

    if not relevant:
        return UNKNOWN
    if any(value == "fail" or "high risk" in value for value in relevant):
        return "fail"
    if any("med risk" in value or "medium risk" in value for value in relevant):
        return "review"
    if any(value == "pass" or "low risk" in value for value in relevant):
        return "pass"
    return relevant[0]


def parse_search_json(payload: str | None) -> list[dict[str, Any]]:
    if not payload:
        return []
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return []
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        skills = data.get("skills")
        if isinstance(skills, list):
            return [item for item in skills if isinstance(item, dict)]
    return []


def exact_match_listing(
    search_results: list[dict[str, Any]], skill_name: str, source_repo: str
) -> bool:
    for item in search_results:
        if str(item.get("name", "")).strip() != skill_name:
            continue
        repo = str(item.get("repo", "")).strip()
        url = str(item.get("url", "")).strip()
        if repo == source_repo or url.endswith(f"/{source_repo}/{skill_name}"):
            return True
    return False


def badge_style_for_value(value: str) -> tuple[str, str]:
    lowered = value.lower()
    if lowered in {UNKNOWN, UNLISTED}:
        return value, "#9ca3af"
    if lowered == "pass":
        return value, "#16a34a"
    if lowered in {"fail", "review"}:
        return value, "#dc2626" if lowered == "fail" else "#d97706"
    return value, "#2563eb"


def make_badge(label: str, value: str) -> str:
    label_text = html.escape(label)
    rendered_value, color = badge_style_for_value(value)
    value_text = html.escape(rendered_value)

    label_width = max(80, 8 * len(label) + 16)
    value_width = max(72, 8 * len(rendered_value) + 16)
    total_width = label_width + value_width
    value_x = label_width + value_width / 2
    label_x = label_width / 2

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20" role="img" '
        f'aria-label="{label_text}: {value_text}">'
        f"<title>{label_text}: {value_text}</title>"
        f'<rect width="{label_width}" height="20" fill="#374151"/>'
        f'<rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>'
        f'<text x="{label_x}" y="14" fill="#ffffff" font-family="Verdana,Geneva,sans-serif" '
        f'font-size="11" text-anchor="middle">{label_text}</text>'
        f'<text x="{value_x}" y="14" fill="#ffffff" font-family="Verdana,Geneva,sans-serif" '
        f'font-size="11" text-anchor="middle">{value_text}</text>'
        "</svg>"
    )


def write_badge(path: pathlib.Path, label: str, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(make_badge(label, value), encoding="utf-8")


def generate(
    repo_root: pathlib.Path,
    output_dir: pathlib.Path,
    source_repo: str,
    base_url: str,
    fixtures: dict[str, str],
) -> dict[str, Any]:
    skills = discover_skills(repo_root)
    manifest: dict[str, Any] = {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "source_repo": source_repo,
        "skills": {},
    }

    for skill_name in skills:
        skill_page = fetch_text(page_url(base_url, source_repo, skill_name), fixtures)
        weekly_installs = parse_weekly_installs(skill_page)
        security_audit = parse_security_audit(skill_page)

        listed_from_page = page_indicates_listing(skill_page)
        if listed_from_page is None:
            search_results = parse_search_json(
                fetch_text(search_url(base_url, skill_name), fixtures)
            )
            listed = exact_match_listing(search_results, skill_name, source_repo)
        elif listed_from_page:
            listed = True
        else:
            search_results = parse_search_json(
                fetch_text(search_url(base_url, skill_name), fixtures)
            )
            listed = exact_match_listing(search_results, skill_name, source_repo)
        listing_status = "listed" if listed else UNLISTED

        skill_output_dir = output_dir / skill_name
        write_badge(
            skill_output_dir / "weekly-installs.svg", "weekly installs", weekly_installs
        )
        write_badge(
            skill_output_dir / "security-audit.svg", "security audit", security_audit
        )
        write_badge(skill_output_dir / "listing-status.svg", "listing", listing_status)

        manifest["skills"][skill_name] = {
            "weekly_installs": weekly_installs,
            "security_audit": security_audit,
            "listing_status": listing_status,
            "page_url": page_url(base_url, source_repo, skill_name),
        }

    return manifest


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    output_dir = (args.output_dir or (repo_root / "badges")).resolve()
    fixtures = load_fixtures(args.fixtures.resolve() if args.fixtures else None)

    manifest = generate(
        repo_root=repo_root,
        output_dir=output_dir,
        source_repo=args.source_repo,
        base_url=args.base_url,
        fixtures=fixtures,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    sys.stdout.write(
        json.dumps({"generated": sorted(manifest["skills"].keys())}, indent=2) + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
