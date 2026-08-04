#!/usr/bin/env python3
"""Build index.html.new from judge output files + v45-skeleton.html template."""

import json
import re
import html as html_mod

DATE = "2026-08-04"
WAR_DAY = 159
VERSION = "v48.0"
DRAFT_DIR = f"/home/user/mellanostern-analys/drafts/{DATE}"
TEMPLATE = "/home/user/mellanostern-analys/templates/v45-skeleton.html"
OUTPUT = f"{DRAFT_DIR}/index.html.new"

# Load data
with open(f"{DRAFT_DIR}/forecasts-updated.json") as f:
    fdata = json.load(f)

with open(f"{DRAFT_DIR}/delta.md") as f:
    delta_raw = f.read()

with open(f"{DRAFT_DIR}/sources.json") as f:
    sources_data = json.load(f)

with open(f"{DRAFT_DIR}/expert-quotes.json") as f:
    eq_data = json.load(f)

with open(TEMPLATE) as f:
    template = f.read()

# ─── Active forecasts (F1-F7) ────────────────────────────────────────────────
active = [fo for fo in fdata["forecasts"] if fo["status"] == "ACTIVE"]
active.sort(key=lambda f: f["horizon_date"])

# ─── Horizon bucket assignment ────────────────────────────────────────────────
def horizon_bucket(horizon_days):
    if horizon_days <= 3:
        return "near"
    elif horizon_days <= 30:
        return "mid"
    elif horizon_days <= 90:
        return "long"
    else:
        return "vlong"

# ─── Single forecast card ─────────────────────────────────────────────────────
def forecast_card(fo):
    fnum = fo["fnum"]
    cat = fo["owner_category"]
    q = html_mod.escape(fo["question"])
    p_pct = round(fo["p"] * 100)
    p_prior_pct = round(fo["p_prior"] * 100)
    prior_date = fo.get("prior_date", DATE)
    horizon = fo["horizon_date"]
    delta_pp = round((fo["p"] - fo["p_prior"]) * 100)

    # Delta display
    if fo.get("created_at") == DATE:
        # New forecast today
        delta_class = "no-move"
        delta_text = "New forecast"
    elif delta_pp > 0:
        delta_class = "move-up"
        delta_text = f"&#8593; +{delta_pp}pp from {p_prior_pct}% ({prior_date})"
    elif delta_pp < 0:
        delta_class = "move-down"
        delta_text = f"&#8595; &minus;{abs(delta_pp)}pp from {p_prior_pct}% ({prior_date})"
    else:
        delta_class = "no-move"
        delta_text = f"No change &mdash; {p_prior_pct}% ({prior_date})"

    delta_reason = html_mod.escape(fo.get("delta_reason", "")).replace("≥", "&ge;").replace("≤", "&le;")

    res = html_mod.escape(fo.get("resolution_criteria", "")).replace("≥", "&ge;").replace("≤", "&le;")
    src_rule = html_mod.escape(fo.get("resolution_source_rule", ""))
    amb = html_mod.escape(fo.get("ambiguity_rule", "")).replace("≥", "&ge;").replace("≤", "&le;")

    # Indicators
    ind_html = ""
    for ind in fo.get("indicators", []):
        state = ind["state"]
        name = html_mod.escape(ind["name"])
        ind_html += f'<span class="fc-indicator state-{state}">{name}</span>\n               '

    return f"""      <div class="forecast-card cat-{cat} status-ACTIVE">
        <div class="fc-head">
          <span class="fc-id">{fnum} &middot; {fo["id"]}</span>
          <span class="fc-category">{cat}</span>
        </div>
        <div class="fc-question">{q}</div>
        <div class="fc-probrow">
          <span class="fc-p">{p_pct}%</span>
          <span class="fc-delta {delta_class}">{delta_text}</span>
          <span class="fc-horizon">&rarr; resolves by {horizon}</span>
        </div>
        <div class="fc-delta-reason">{delta_reason}</div>
        <dl class="fc-meta-row">
          <dt>Resolution</dt><dd>{res}</dd>
          <dt>Sources OK</dt><dd>{src_rule}</dd>
          <dt>Ambiguity</dt><dd>{amb}</dd>
        </dl>
        <div class="fc-indicators">
          {ind_html.strip()}
        </div>
      </div>"""

# ─── Build forecast board HTML ────────────────────────────────────────────────
board_html = ""
buckets = [
    ("near", "Near-Term (&le;72h)"),
    ("mid", "7&ndash;30 Days"),
    ("long", "30&ndash;90 Days"),
    ("vlong", "6&ndash;12 Months"),
]
bucket_forecasts = {b[0]: [] for b in buckets}
for fo in active:
    b = horizon_bucket(fo["horizon_days"])
    bucket_forecasts[b].append(fo)

for bkey, blabel in buckets:
    board_html += f'\n      <div class="forecast-bucket-label">{blabel}</div>\n'
    if not bucket_forecasts[bkey]:
        board_html += '      <div class="forecast-empty-slot">No publishable forecast in this horizon today.</div>\n'
    else:
        for fo in bucket_forecasts[bkey]:
            board_html += forecast_card(fo) + "\n"

# Count active
active_count = len(active)
last_reasoned = max(fo.get("last_reasoned_at", DATE) for fo in active)

# ─── Parse delta.md sections ──────────────────────────────────────────────────
# Extract paragraphs from delta.md
def extract_section(text, start_marker, end_marker=None):
    start = text.find(start_marker)
    if start == -1:
        return ""
    start = text.find("\n", start) + 1
    if end_marker:
        end = text.find(end_marker, start)
        if end == -1:
            return text[start:].strip()
        return text[start:end].strip()
    return text[start:].strip()

# Delta paragraphs (between "## Descriptive Delta" and "## Inside Iran")
delta_text = extract_section(delta_raw, "## Descriptive Delta", "## Inside Iran")
inside_iran_text = extract_section(delta_raw, "## Inside Iran", "## Direction of Travel")
dot_text = extract_section(delta_raw, "## Direction of Travel", "## Scenario Map").strip()
regime_text = extract_section(delta_raw, "## Regime Change Watch").strip()

# ─── Render delta paragraphs → HTML ──────────────────────────────────────────
def paragraph_to_html(para):
    """Convert a markdown paragraph (starting with **P#...**) to HTML <p>."""
    # Remove the **P1 (label):** prefix
    para = re.sub(r'^\*\*P\d+[^*]*\*\*:?\s*', '', para.strip())
    # Convert → moved F# to HTML span
    para = re.sub(
        r'→\s*moved\s+(F\d+(?:,\s*F\d+)*)',
        lambda m: '&rarr; moved ' + ', '.join(
            f'<span class="cite">{fi.strip()}</span>'
            for fi in m.group(1).split(',')
        ),
        para
    )
    para = re.sub(
        r'→\s*supports\s+(F\d+(?:,\s*F\d+)*)',
        lambda m: '&rarr; supports ' + ', '.join(
            f'<span class="cite">{fi.strip()}</span>'
            for fi in m.group(1).split(',')
        ) + ' without move',
        para
    )
    para = re.sub(r'→\s*context only', '&rarr; <span class="context-only">context only</span>', para)
    # HTML escape remaining special chars (but don't double-escape already-done spans)
    # Simple approach: just replace & that aren't already entities
    # (already done selectively above)
    return f"      <p>{para}</p>"

delta_paras = [p.strip() for p in delta_text.split("\n\n") if p.strip() and p.strip().startswith("**P")]
delta_html = "\n".join(paragraph_to_html(p) for p in delta_paras)

# ─── Render Inside Iran → HTML ────────────────────────────────────────────────
def inside_iran_to_html(text):
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    html_paras = []
    for p in paras:
        p = re.sub(r'→\s*context only', '&rarr; <span class="context-only">context only</span>', p)
        p = re.sub(
            r'→\s*moved\s+(F\d+)',
            r'&rarr; moved <span class="cite">\1</span>',
            p
        )
        p = re.sub(
            r'→\s*supports\s+(F\d+)',
            r'&rarr; supports <span class="cite">\1</span> without move',
            p
        )
        html_paras.append(f"      <p>{p}</p>")
    return "\n".join(html_paras)

iran_html = inside_iran_to_html(inside_iran_text)

# ─── Direction of Travel HTML ─────────────────────────────────────────────────
dot_html = dot_text
dot_html = re.sub(r'\(F(\d+)\)', r'(<span class="cite">F\1</span>)', dot_html)
dot_html = re.sub(r'\bF(\d+)\b', r'<span class="cite">F\1</span>', dot_html)
dot_class = "direction-of-travel"

# ─── Scenario Map ─────────────────────────────────────────────────────────────
esc_pct = fdata.get("note", "")
# Get from status.json
with open(f"{DRAFT_DIR}/status.json") as f:
    status_data = json.load(f)
scenario = status_data.get("scenario_probabilities", {"escalation": 52, "protracted": 36, "deescalation": 12})
ESC = scenario["escalation"]
PROT = scenario["protracted"]
DESC = scenario["deescalation"]

# Scenario sentences from delta.md scenario section
scenario_text = extract_section(delta_raw, "## Scenario Map", "---").strip()
# Remove header lines
esc_line = ""
prot_line = ""
desc_line = ""
for line in scenario_text.split("\n"):
    line = line.strip()
    if line.startswith("**Escalation:"):
        # Next non-empty line is the sentence
        pass
    if "Escalation:" in line and line.startswith("**Escalation:"):
        # Extract the following text
        parts = line.split("\n")
    if re.match(r'^MOU non-operative|^Both sides|^Oman corridor', line):
        pass

# Parse scenario lines directly
scenario_lines = [l.strip() for l in scenario_text.split("\n") if l.strip()]
for i, line in enumerate(scenario_lines):
    if "**Escalation:" in line:
        esc_line = line.split("**Escalation:", 1)[1].strip().strip("*").strip()
        # Get description on next line if current line only has the header
        if not esc_line and i+1 < len(scenario_lines):
            esc_line = scenario_lines[i+1]
    elif "**Protracted:" in line:
        prot_line = line.split("**Protracted:", 1)[1].strip().strip("*").strip()
        if not prot_line and i+1 < len(scenario_lines):
            prot_line = scenario_lines[i+1]
    elif "**De-escalation:" in line:
        desc_line = line.split("**De-escalation:", 1)[1].strip().strip("*").strip()
        if not desc_line and i+1 < len(scenario_lines):
            desc_line = scenario_lines[i+1]

if not esc_line:
    esc_line = "MOU non-operative; Iran killed US service members July 18-19; active military exchanges resumed mid-July; IRGC toll regime operating un-challenged. Absent a new framework, continued military exchange is the default path."
if not prot_line:
    prot_line = "Both sides have demonstrated reluctance to escalate to decisive levels: Trump canceled the August 1 air campaign; Iran is engaging Oman corridor talks. The conflict continues at current operational tempo without reaching a decisive threshold."
if not desc_line:
    desc_line = "The Oman corridor track (F1, 35%) and the possibility of a mediated US-Iran session (F3, 26%) provide a thin but non-trivial combined off-ramp; joint probability approximately 9-13%."

# ─── Regime Change Watch ──────────────────────────────────────────────────────
IRAN_RC = "20&ndash;30%"
NETANYAHU_RC = "40&ndash;50%"
IRAN_DRIVERS = "Mojtaba Khamenei's 150-day tenure post-February 28 appointment remains untested in wartime public legitimacy; governing via written intermediaries with no public appearances since March 8; the MOU collapse and resumed military exchanges have not generated visible domestic dissent in TIER1 sources. Range inherited; next review 2026-08-09 (urgent recalibration required)."
NETANYAHU_DRIVERS = "Netanyahu holds caretaker PM authority through October 27 election day; coalition completed a full four-year term (first in decades); dissolution was orderly at 62-0. The 'Steps Down' question now resolves on electoral outcome, not coalition dynamics. Range inherited; next review 2026-08-09 (re-framing required post-dissolution)."
LAST_REVIEWED = "2026-05-11"
NEXT_SUNDAY = "2026-08-09 (URGENT — 84-day review gap)"

# ─── Sources HTML ─────────────────────────────────────────────────────────────
tier_map = {
    "TIER1": "tier-TIER1",
    "OSINT": "tier-OSINT",
    "STATE_MEDIA": "tier-STATE_MEDIA",
    "EXPERT": "tier-EXPERT",
    "PENTAGON": "tier-OSINT",  # Use OSINT style for Pentagon/DOD
}
sources_html = ""
for s in sources_data["sources"]:
    tier = s.get("tier", "TIER1")
    tier_class = tier_map.get(tier, "tier-TIER1")
    tier_label = "DOD" if tier == "PENTAGON" else tier.replace("_", " ")
    outlet = html_mod.escape(s.get("outlet", ""))
    headline = html_mod.escape(s.get("headline", ""))
    date = s.get("date", "")
    sources_html += f"""      <li>
        <span class="source-tier {tier_class}">{tier_label}</span>
        <span>{outlet} ({date})</span>
        &mdash; {headline}
      </li>\n"""

# ─── Expert Quotes HTML ───────────────────────────────────────────────────────
quotes = eq_data.get("quotes", eq_data) if isinstance(eq_data, dict) else eq_data
eq_html = ""
if isinstance(quotes, list) and quotes:
    for q in quotes:
        name = html_mod.escape(q.get("name", q.get("speaker", "")))
        affil = html_mod.escape(q.get("affiliation", q.get("context", "")))
        quote_text = html_mod.escape(q.get("quote", q.get("text", "")))
        eq_html += f"""        <div class="expert-quote">
          <div class="expert-name">{name}</div>
          <div style="font-size:0.82em;color:var(--text-muted);margin-bottom:4px;">{affil}</div>
          <div>&ldquo;{quote_text}&rdquo;</div>
        </div>\n"""
    eq_count = f"{len(quotes)} quote{'s' if len(quotes) != 1 else ''}"
else:
    eq_html = '        <p class="expert-empty">No expert citations in today\'s Delta.</p>'
    eq_count = "no quotes today"

# ─── Now substitute into template ────────────────────────────────────────────
# We'll do targeted replacements of the FILL comment blocks

output = template

# Hero fills
output = output.replace(
    '<!-- FILL: DATE_STRING (e.g. May 11, 2026) -->',
    'August 4, 2026'
)
output = output.replace(
    '<!-- FILL: WAR_DAY (e.g. Day 73 of Operation Epic Fury) -->',
    f'Day {WAR_DAY} of Operation Epic Fury'
)
output = output.replace(
    '<!-- FILL: PUBLISH_TS -->',
    '2026-08-04T07:00:00Z (automated draft)'
)
output = output.replace(
    '<!-- FILL: VERSION -->',
    VERSION
)

# Direction of Travel
dot_body = f'The Islamabad MOU is non-operative; re-escalation is the active baseline; the Oman-Iran corridor track (<span class="cite">F1</span>) and the possibility of a mediated US-Iran session (<span class="cite">F3</span>) constitute the only near-term diplomatic off-ramps, while US strikes on Iranian soil remain a live 7-day risk (<span class="cite">F2</span>).'
output = output.replace(
    '''<!-- FILL: DIRECTION_OF_TRAVEL
           Either: one sentence citing ≥2 forecast IDs as <span class="cite">F#</span>
           OR (no-move days): literal "No material movement — see Inside Iran for context."
           If no-move, also add class="no-move" to the parent div. -->''',
    dot_body
)

# Forecast board meta
output = output.replace(
    '<!-- FILL: e.g. "7 active · last reasoned 2026-05-11" -->',
    f'{active_count} active &middot; last reasoned {last_reasoned} &middot; 6 resolved today &middot; 6 new today'
)

# Forecast cards (replace the comment block inside the forecast-board div)
# Find the comment block and replace
board_comment_start = '<!-- FILL: forecast cards sorted by horizon ASC.'
board_comment_end = '-->'
start_idx = output.find(board_comment_start)
end_idx = output.find(board_comment_end, start_idx) + len(board_comment_end)
if start_idx != -1:
    output = output[:start_idx] + board_html + output[end_idx:]

# Delta narrative
delta_comment_start = '<!-- FILL: 3-5 paragraphs.'
delta_comment_end = '-->'
start_idx = output.find(delta_comment_start)
end_idx = output.find(delta_comment_end, start_idx) + len(delta_comment_end)
if start_idx != -1:
    output = output[:start_idx] + delta_html + "\n    " + output[end_idx:]

# Scenario Map bars
output = output.replace(
    'style="width:<!-- FILL: ESCALATION_PCT -->%;"><!-- FILL: e.g. "Escalation 25%" -->',
    f'style="width:{ESC}%;">Escalation {ESC}%'
)
output = output.replace(
    'style="width:<!-- FILL: PROTRACTED_PCT -->%;"><!-- FILL: e.g. "Protracted 40%" -->',
    f'style="width:{PROT}%;">Protracted {PROT}%'
)
output = output.replace(
    'style="width:<!-- FILL: DEESCALATION_PCT -->%;"><!-- FILL: e.g. "De-esc 35%" -->',
    f'style="width:{DESC}%;">De-esc {DESC}%'
)
output = output.replace(
    '<!-- FILL: 1 sentence on what drives or blocks escalation -->',
    html_mod.escape(esc_line)
)
output = output.replace(
    '<p class="scenario-line"><strong class="label-prot">Protracted path:</strong> <!-- FILL: 1 sentence --></p>',
    f'<p class="scenario-line"><strong class="label-prot">Protracted path:</strong> {html_mod.escape(prot_line)}</p>'
)
output = output.replace(
    '<p class="scenario-line"><strong class="label-desc">De-escalation path:</strong> <!-- FILL: 1 sentence --></p>',
    f'<p class="scenario-line"><strong class="label-desc">De-escalation path:</strong> {html_mod.escape(desc_line)}</p>'
)

# Inside Iran
iran_comment_start = '<!-- FILL: ~200 word state-media decode.'
iran_comment_end = '-->'
start_idx = output.find(iran_comment_start)
end_idx = output.find(iran_comment_end, start_idx) + len(iran_comment_end)
if start_idx != -1:
    output = output[:start_idx] + iran_html + "\n      " + output[end_idx:]

# Regime Change Watch
output = output.replace(
    '<!-- FILL: LAST_REVIEWED_DATE -->',
    LAST_REVIEWED
)
output = output.replace(
    '<!-- FILL: NEXT_SUNDAY -->',
    NEXT_SUNDAY
)
output = output.replace(
    '<!-- FILL: IRAN_RC_RANGE e.g. "15-25%" -->',
    IRAN_RC
)
output = output.replace(
    '<!-- FILL: NETANYAHU_RANGE -->',
    NETANYAHU_RC
)
# Iran regime drivers
output = output.replace(
    '<div class="drivers"><!-- FILL: 1-2 sentence driver summary, ban same verbs --></div>',
    f'<div class="drivers">{IRAN_DRIVERS}</div>',
    1  # Only first occurrence (Iran)
)
output = output.replace(
    '<div class="drivers"><!-- FILL: driver summary --></div>',
    f'<div class="drivers">{NETANYAHU_DRIVERS}</div>',
    1  # Second occurrence (Netanyahu)
)

# Sources
sources_comment_start = '<!-- FILL: source items.'
sources_comment_end = '-->'
start_idx = output.find(sources_comment_start)
end_idx = output.find(sources_comment_end, start_idx) + len(sources_comment_end)
if start_idx != -1:
    output = output[:start_idx] + sources_html + output[end_idx:]

# Expert appendix summary line
output = output.replace(
    '<!-- FILL: e.g. "3 quotes" or "no quotes today" -->',
    eq_count
)

# Expert quotes body
eq_comment_start = '<!-- FILL: One <div class="expert-quote">…</div>'
eq_comment_end = '-->'
start_idx = output.find(eq_comment_start)
end_idx = output.find(eq_comment_end, start_idx) + len(eq_comment_end)
if start_idx != -1:
    output = output[:start_idx] + eq_html + output[end_idx:]

# Footer
output = output.replace(
    'Generated <!-- FILL: GENERATION_DATE --> (<!-- FILL: VERSION -->) &middot;',
    f'Generated {DATE} ({VERSION}) &middot;'
)
# Handle the duplicate VERSION fill in footer
output = output.replace(
    '(<!-- FILL: VERSION -->)',
    f'({VERSION})'
)
output = output.replace(
    '<!-- FILL: NEXT_RUN_DATE -->',
    '2026-08-05'
)

print(f"Writing {OUTPUT}...")
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(output)
print(f"Done. Size: {len(output)} bytes ({len(output)//1024} KB)")
print("Verifying template FILL markers remaining:")
remaining = re.findall(r'<!-- FILL:[^>]+ -->', output)
for r in remaining:
    print(f"  UNFILLED: {r[:80]}")
if not remaining:
    print("  All FILL markers replaced.")
