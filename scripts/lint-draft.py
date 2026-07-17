#!/usr/bin/env python3
"""
Lint gate for daily-update-draft + daily-update-publish pipelines.

Three modes:

  Full      (draft Step 8):
    python3 scripts/lint-draft.py <html> <forecasts.json>
      Runs schema check on forecasts + verb-ban + cite-closure on HTML sections.

  Forecasts-only (publish Step 6 — schema sanity on forecasts-updated.json):
    python3 scripts/lint-draft.py --forecasts-only <forecasts.json>
      Skips HTML extraction entirely. Use when validating just the persistent
      state file with no HTML context (e.g. mid-publish sweep).

  HTML-only   (debugging / template smoke-test):
    python3 scripts/lint-draft.py --html-only <html>
      Skips forecast schema. Useful for verifying template structure + verb
      discipline without a full forecasts JSON in hand.

Checks performed:

  Forecast schema (full / forecasts-only):
    - Max 7 ACTIVE forecasts (cap)
    - Horizon coverage warnings (no near-term / no 7-30d)
    - Required fields per object (id, question, owner_category, p, p_prior,
      resolution_criteria, ambiguity_rule, indicators, status, ...)
    - owner_category in {diplomacy, military, domestic, regime, market, humanitarian}
    - status in {ACTIVE, RESOLVED-YES, RESOLVED-NO, RESOLVED-AMBIGUOUS,
      OPEN-AMBIGUOUS, OBE}
    - p in [0.05, 0.95] (Codex 5-95% rule)
    - resolution_criteria ≥30 chars; ambiguity_rule ≥20 chars
    - ≥1 indicator per forecast
    - graveyard_reason present when status is non-ACTIVE

  HTML lints (full / html-only):
    - Banned-verb scan in <div class="section" id="delta"> and "inside-iran"
    - Every <p> in those sections ends with → moved F# / → supports F# /
      → context only

Exit codes:
  0 = pass (publishable)
  1 = fail (one or more checks blocked)
  2 = warn (passes but flagged)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional


# Banned verbs that smuggle prediction into descriptive sections.
# Patterns are case-insensitive whole-word/phrase matches.
BANNED_PATTERNS = [
    r"\bsignals\b",
    r"\bsignaling\b",
    r"\bpositions for\b",
    r"\bpositioning for\b",
    r"\bprepares ground for\b",
    r"\bsets up\b",
    r"\bpaves the way\b",
    r"\bforeshadows\b",
    r"\bhints at\b",
    r"\bopens the door to\b",
    r"\braises the prospect of\b",
    r"\bincreases the odds of\b",
    r"\blowers the odds of\b",
    r"\bmakes \w+ more likely\b",
    r"\bmakes \w+ less likely\b",
    r"\bpressure is building\b",
    r"\bmomentum is shifting\b",
    r"\bsuggests\b",
    r"\bindicates\b",
    r"\bpoints to\b",
    r"\bunderscores\b",
    r"\breflects\b",
    r"\breveals\b",
    # "marks" is too common; require "marks the" / "marks a" pattern
    r"\bmarks (?:a|the) \w+ (?:shift|turn|moment|inflection)\b",
]

BANNED_RE = re.compile("|".join(BANNED_PATTERNS), re.IGNORECASE)

# Required closure: every <p> in linted sections must end with one of these markers.
# Markers are HTML-rendered spans; we look for them as text patterns near the </p>.
REQUIRED_CLOSURE_PATTERNS = [
    r"→\s*moved\s+<span[^>]*class=[\"']cite[\"'][^>]*>[A-Z]\d+",
    r"→\s*moved\s+[A-Z]\d+",
    r"→\s*supports\s+<span[^>]*class=[\"']cite[\"'][^>]*>[A-Z]\d+",
    r"→\s*supports\s+[A-Z]\d+",
    r"→\s*<span[^>]*class=[\"']context-only[\"'][^>]*>context only",
    r"→\s*context only",
]
CLOSURE_RE = re.compile("|".join(REQUIRED_CLOSURE_PATTERNS), re.IGNORECASE)


def load_forecasts(path: Path) -> dict:
    """Parse active.json; return the wrapper dict."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        die(f"FAIL: could not parse {path}: {exc}")


def validate_forecast_schema(active: dict) -> list[str]:
    """Schema validation without jsonschema dependency — hand-rolled checks."""
    errors: list[str] = []
    forecasts = active.get("forecasts", [])

    active_forecasts = [f for f in forecasts if f.get("status") == "ACTIVE"]
    if len(active_forecasts) > 7:
        errors.append(f"FAIL: {len(active_forecasts)} ACTIVE forecasts; cap is 7.")

    if not active_forecasts:
        errors.append("FAIL: zero ACTIVE forecasts; board cannot be empty.")

    # Horizon distribution: hard requirement ≥1 near-term, ≥1 in 7-30d
    near = [f for f in active_forecasts if f.get("horizon_days", 999) <= 3]
    mid = [f for f in active_forecasts if 7 <= f.get("horizon_days", 0) <= 30]
    if not near:
        errors.append("WARN: no near-term (≤72h) forecast on active board.")
    if not mid:
        errors.append("WARN: no 7-30d forecast on active board.")

    required_keys = [
        "id", "question", "owner_category", "horizon_days", "horizon_date",
        "created_at", "expires_at", "p", "p_prior", "prior_date",
        "delta_reason", "resolution_criteria", "resolution_source_rule",
        "ambiguity_rule", "indicators", "status",
    ]
    valid_categories = {"diplomacy", "military", "domestic", "regime", "market", "humanitarian"}
    valid_statuses = {"ACTIVE", "RESOLVED-YES", "RESOLVED-NO", "RESOLVED-AMBIGUOUS",
                      "OPEN-AMBIGUOUS", "OBE"}

    for i, f in enumerate(forecasts):
        fid = f.get("id", f"<idx {i}>")
        for k in required_keys:
            if k not in f:
                errors.append(f"FAIL [{fid}]: missing required field '{k}'.")

        if f.get("owner_category") not in valid_categories:
            errors.append(f"FAIL [{fid}]: owner_category '{f.get('owner_category')}' not in {valid_categories}.")
        if f.get("status") not in valid_statuses:
            errors.append(f"FAIL [{fid}]: status '{f.get('status')}' not in {valid_statuses}.")

        p = f.get("p")
        if p is not None and not (0.05 <= p <= 0.95):
            errors.append(f"FAIL [{fid}]: p={p} outside [0.05, 0.95] (Codex 5-95% rule).")

        if not f.get("resolution_criteria") or len(f["resolution_criteria"]) < 30:
            errors.append(f"FAIL [{fid}]: resolution_criteria missing or <30 chars.")
        if not f.get("ambiguity_rule") or len(f["ambiguity_rule"]) < 20:
            errors.append(f"FAIL [{fid}]: ambiguity_rule missing or <20 chars.")
        if not f.get("indicators") or len(f["indicators"]) < 1:
            errors.append(f"FAIL [{fid}]: zero indicators; need ≥1.")
        if not f.get("delta_reason"):
            errors.append(f"FAIL [{fid}]: empty delta_reason (use 'No material movement' for zero-move).")

        # Status that requires graveyard_reason
        if f.get("status") in {"RESOLVED-YES", "RESOLVED-NO", "RESOLVED-AMBIGUOUS", "OBE"}:
            if not f.get("graveyard_reason"):
                errors.append(f"FAIL [{fid}]: status={f['status']} requires graveyard_reason.")

    return errors


def extract_section(html: str, section_id: str) -> Optional[str]:
    """Pull out a section by id using div-depth counting.

    Lookahead-based regex was unreliable because nested divs and HTML
    comments between sections broke the boundary detection. Counts <div...>
    vs </div> from the section start until depth returns to zero.
    """
    start_re = re.compile(
        rf'<div\s+class="section"\s+id="{re.escape(section_id)}"[^>]*>'
    )
    m = start_re.search(html)
    if not m:
        return None
    content_start = m.end()
    depth = 1
    pos = content_start
    open_re = re.compile(r"<div\b", re.IGNORECASE)
    close_re = re.compile(r"</div>", re.IGNORECASE)
    while depth > 0 and pos < len(html):
        next_open = open_re.search(html, pos)
        next_close = close_re.search(html, pos)
        if not next_close:
            return None
        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            if depth == 0:
                return html[content_start:next_close.start()]
            pos = next_close.end()
    return None


def lint_section_text(section_html: str, label: str) -> list[str]:
    """Banned-verb scan + closure check on each <p>."""
    errors: list[str] = []

    # Strip HTML comments to avoid false positives on the FILL hints
    stripped = re.sub(r"<!--.*?-->", "", section_html, flags=re.DOTALL)

    # Banned verbs
    for match in BANNED_RE.finditer(stripped):
        # Get a snippet around the match
        start = max(0, match.start() - 40)
        end = min(len(stripped), match.end() + 40)
        snippet = re.sub(r"\s+", " ", stripped[start:end]).strip()
        errors.append(f"FAIL [{label}]: banned verb '{match.group(0)}' in: ...{snippet}...")

    # Closure check: every <p> must end with → moved F# / → supports F# / → context only
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", stripped, flags=re.DOTALL)
    for i, para_inner in enumerate(paragraphs, 1):
        para_text = re.sub(r"\s+", " ", para_inner).strip()
        if not para_text:
            continue
        # Look only at the last ~200 chars where the marker should appear
        tail = para_text[-300:]
        if not CLOSURE_RE.search(tail):
            errors.append(
                f"FAIL [{label}]: paragraph {i} does not end with required forecast cite / context-only marker. "
                f"Tail: ...{tail[-150:]}"
            )

    return errors


def parse_args() -> argparse.Namespace:
    """Parse CLI; support positional (full mode) + flag-based modes.

    Backwards-compatible: `lint-draft.py <html> <forecasts>` still works.
    """
    parser = argparse.ArgumentParser(
        prog="lint-draft.py",
        description="Lint gate for daily-update-draft + publish pipelines.",
        epilog="See module docstring for full check list. Exit: 0=pass, 1=fail, 2=warn.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--forecasts-only",
        metavar="FORECASTS_JSON",
        help="Run only forecast schema checks (skip HTML extraction).",
    )
    mode.add_argument(
        "--html-only",
        metavar="HTML_FILE",
        help="Run only HTML lints (skip forecast schema).",
    )
    parser.add_argument(
        "positional",
        nargs="*",
        help="Full mode: <html> <forecasts>. Ignored if --forecasts-only or --html-only.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Determine mode + resolve file paths
    html_path: Optional[Path] = None
    forecasts_path: Optional[Path] = None

    if args.forecasts_only:
        forecasts_path = Path(args.forecasts_only)
    elif args.html_only:
        html_path = Path(args.html_only)
    else:
        # Full mode requires exactly two positional args
        if len(args.positional) != 2:
            print(__doc__, file=sys.stderr)
            return 2
        html_path = Path(args.positional[0])
        forecasts_path = Path(args.positional[1])

    # Validate file existence
    if html_path is not None and not html_path.exists():
        die(f"FAIL: HTML file not found: {html_path}")
    if forecasts_path is not None and not forecasts_path.exists():
        die(f"FAIL: forecasts file not found: {forecasts_path}")

    all_errors: list[str] = []

    # Forecast schema checks
    if forecasts_path is not None:
        active = load_forecasts(forecasts_path)
        all_errors.extend(validate_forecast_schema(active))

    # HTML section lints
    if html_path is not None:
        html = html_path.read_text(encoding="utf-8")
        for sid, label in [("delta", "DELTA"), ("inside-iran", "INSIDE_IRAN")]:
            section = extract_section(html, sid)
            if section is None:
                all_errors.append(f"FAIL: section '{sid}' not found in HTML; structure broken.")
                continue
            all_errors.extend(lint_section_text(section, label))

    # Categorize
    fails = [e for e in all_errors if e.startswith("FAIL")]
    warns = [e for e in all_errors if e.startswith("WARN")]

    if fails:
        print("=" * 70, file=sys.stderr)
        print("LINT FAILED", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        for e in fails:
            print(f"  {e}", file=sys.stderr)
    if warns:
        print("-" * 70, file=sys.stderr)
        print("LINT WARNINGS", file=sys.stderr)
        print("-" * 70, file=sys.stderr)
        for w in warns:
            print(f"  {w}", file=sys.stderr)

    if fails:
        return 1
    if warns:
        print("\nlint OK (with warnings) — publishable", file=sys.stderr)
        return 2
    print("lint OK — publishable", file=sys.stderr)
    return 0


def die(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
