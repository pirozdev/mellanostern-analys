#!/usr/bin/env python3
"""Deterministic renderer: v45 skeleton + forecasts-updated.json + Judge text -> index.html.new"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFT = Path(__file__).resolve().parent
skeleton = (ROOT / "templates/v45-skeleton.html").read_text(encoding="utf-8")
active = json.loads((DRAFT / "forecasts-updated.json").read_text(encoding="utf-8"))

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---- meta ----
DATE_STRING = "June 3, 2026"
WAR_DAY = "Day 96"
PUBLISH_TS = "2026-06-03T07:00:00Z"
VERSION = "v46.1"
GEN_DATE = "2026-06-03"
NEXT_RUN = "2026-06-04"
BOARD_META = "7 active &middot; last reasoned 2026-06-03"

# ---- buckets by days-to-horizon from 2026-06-03 ----
from datetime import date
TODAY = date(2026, 6, 3)
def days_to(d):
    y, m, dd = map(int, d.split("-"))
    return (date(y, m, dd) - TODAY).days

BUCKETS = [
    ("Near-Term (&le;72h)", lambda n: n <= 3),
    ("7&ndash;30 Days", lambda n: 3 < n <= 30),
    ("30&ndash;90 Days", lambda n: 30 < n <= 90),
    ("6&ndash;12 Months", lambda n: n > 90),
]

def card(f):
    p = int(round(f["p"] * 100))
    pp = int(round(f["p_prior"] * 100))
    new = f["created_at"] == "2026-06-03"
    if new:
        delta_cls, delta_txt = "no-move", "New forecast"
    elif f["p"] == f["p_prior"] and f["owner_category"] == "regime":
        delta_cls, delta_txt = "no-move", "No change &mdash; weekly cadence only"
    elif f["p"] == f["p_prior"]:
        delta_cls, delta_txt = "no-move", "No change"
    else:
        diff = p - pp
        if diff < 0:
            delta_cls = "move-down"
            delta_txt = "&#8595; &minus;%dpp from %d%% (%s)" % (abs(diff), pp, f["prior_date"])
        else:
            delta_cls = "move-up"
            delta_txt = "&#8593; +%dpp from %d%% (%s)" % (diff, pp, f["prior_date"])
    inds = "\n          ".join(
        '<span class="fc-indicator state-%s">%s</span>' % (i["state"], esc(i["name"]))
        for i in f["indicators"]
    )
    return """      <div class="forecast-card cat-{cat} status-ACTIVE">
        <div class="fc-head">
          <span class="fc-id">{fnum} &middot; {fid}</span>
          <span class="fc-category">{cat}</span>
        </div>
        <div class="fc-question">{q}</div>
        <div class="fc-probrow">
          <span class="fc-p">{p}%</span>
          <span class="fc-delta {dcls}">{dtxt}</span>
          <span class="fc-horizon">&rarr; resolves by {hd}</span>
        </div>
        <div class="fc-delta-reason">{dr}</div>
        <dl class="fc-meta-row">
          <dt>Resolution</dt><dd>{rc}</dd>
          <dt>Sources OK</dt><dd>{rsr}</dd>
          <dt>Ambiguity</dt><dd>{amb}</dd>
        </dl>
        <div class="fc-indicators">
          {inds}
        </div>
      </div>""".format(
        cat=f["owner_category"], fnum=f.get("fnum", ""), fid=esc(f["id"]),
        q=esc(f["question"]), p=p, dcls=delta_cls, dtxt=delta_txt, hd=f["horizon_date"],
        dr=esc(f["delta_reason"]), rc=esc(f["resolution_criteria"]),
        rsr=esc(f["resolution_source_rule"]), amb=esc(f["ambiguity_rule"]), inds=inds,
    )

fs = active["forecasts"]
board_parts = []
for label, pred in BUCKETS:
    bucket_cards = [f for f in fs if pred(days_to(f["horizon_date"]))]
    bucket_cards.sort(key=lambda f: f["horizon_date"])
    board_parts.append('      <div class="forecast-bucket-label">%s</div>' % label)
    if bucket_cards:
        board_parts.extend(card(f) for f in bucket_cards)
    else:
        board_parts.append('      <div class="forecast-empty-slot">No publishable forecast in this horizon today.</div>')
BOARD_HTML = "\n\n".join(board_parts)

# ---- DIRECTION OF TRAVEL (written last; cites F1, F4, F2) ----
DIRECTION = ('Iran&rsquo;s massing of 201 IRGCN small craft at the strait and its formal 1&nbsp;June '
             'suspension of mediator channels lifts <span class="cite">F1</span> to 45% while '
             're-engagement probability (<span class="cite">F4</span>) falls to 35% with no observed '
             'indicators of renewed contact; the signed-framework node '
             '(<span class="cite">F2</span>) expires in 48h at the 5% floor.')

# ---- DELTA (5 paragraphs; verb-clean; all end with cite marker) ----
DELTA = """      <p>On 1&nbsp;June Iranian Foreign Minister Araghchi stated publicly that the Iran&ndash;US ceasefire framework covers &ldquo;all fronts, including Lebanon,&rdquo; and that a violation on one front constitutes a violation across all; the same day Tasnim reported that Tehran had halted all mediator-channel message exchanges with Washington, citing Israel&rsquo;s Lebanon operations as the proximate cause. IRNA on 2&nbsp;June reported there was &ldquo;no clear prospect of fruitful negotiations&rdquo; and attributed the stall to US &ldquo;unreasonable and unrealistic demands.&rdquo; &rarr; moved <span class="cite">F4</span></p>
      <p>On 30&nbsp;May Windward electro-optical imagery documented approximately 201 IRGCN small craft massed across the northern Strait of Hormuz at Larak Island &mdash; the largest single-day small-craft footprint recorded in that corridor since Operation Epic Fury began. CNN&rsquo;s 2&nbsp;June account placed commercial transit at approximately 4 vessels per day against a pre-crisis baseline near 95 per day, with Lloyd&rsquo;s war-risk insurance at 8.0&times; pre-crisis levels, six Maersk vessels still in the Gulf, and an IMO tally of 39 vessel strikes and 11 deaths since 28&nbsp;February. An unknown projectile struck a cargo vessel in the northern Persian Gulf per the IMO tally; UKMTO had not issued a specific advisory confirming a new IRGC closure action as of EOD 2&nbsp;June. &rarr; moved <span class="cite">F1</span></p>
      <p>Secretary of State Rubio testified before the Senate Foreign Relations Committee on 2&nbsp;June, confirming the US remained in negotiations and stating Iran had for the first time acknowledged the nuclear program as a negotiating subject; he described Hormuz reopening as a US deal requirement. Trump told ABC News a deal was achievable &ldquo;over the next week,&rdquo; and CNN cited a single unnamed regional source claiming talks had returned &ldquo;back on track&rdquo; within hours of Iran&rsquo;s suspension announcement. Neither claim was corroborated by a named Iranian official or a named mediator readout by the close of 2&nbsp;June. &rarr; supports <span class="cite">F4</span> without move</p>
      <p>The 60-day framework MOU tentatively reached by negotiators on 28&nbsp;May per Axios remained unsigned and unacknowledged by principals as of 3&nbsp;June. Tasnim cited a source close to Iran&rsquo;s negotiating team characterizing the MOU as &ldquo;neither finalized nor confirmed.&rdquo; All three confirmation indicators &mdash; a confirmed Witkoff&ndash;Araghchi direct meeting, a Trump public acknowledgment of a deal, and a reopened mediator channel &mdash; remained at NOT_OBSERVED as the 48-hour window before the 5&nbsp;June horizon opened. &rarr; moved <span class="cite">F2</span></p>
      <p>The Knesset passed the dissolution bill&rsquo;s first reading 106&ndash;0 on 2&nbsp;June; the House Committee advanced it the same day without inserting an election date. Coalition whip Ofir Katz stated the date would be determined before the second and third readings. Shas and UTJ publicly favoured a September date ahead of the High Holy Days; Netanyahu&rsquo;s office preferred October. No schedule for further readings was announced as of 3&nbsp;June. &rarr; supports <span class="cite">F6</span> without move</p>"""

# ---- INSIDE IRAN (~200 words; verb-clean; one paragraph with cite) ----
INSIDE_IRAN = """      <p>Iranian state media on 1&ndash;2&nbsp;June operated with disciplined consistency across Tasnim, IRNA, and Fars. Tasnim led the coverage of Iran&rsquo;s suspension of mediator-channel exchanges, framing the step as a principled response to ceasefire violations in Lebanon rather than a negotiating collapse; the Hormuz closure posture was presented as a sovereign prerogative and a legitimate instrument of leverage, not a tactical concession. No state-media outlet described the Hormuz blockade as a bargaining chip to be lifted for concessions. IRNA&rsquo;s diplomatic desk attributed the stall to Washington&rsquo;s &ldquo;unreasonable and unrealistic demands,&rdquo; a formulation placing the burden of concession on the US side. Fars cited unnamed sources &ldquo;close to the negotiating team&rdquo; characterizing the MOU as unfinalized, distancing the leadership from being seen as having accepted terms that Iranian hardliners might reject. The CNN unnamed-source claim that talks had returned &ldquo;on track&rdquo; within hours of the suspension was absent from Persian-language state-media output as visible through English-language feeds on 2&nbsp;June, as was any acknowledgment of the Windward IRGCN small-craft massing report. Araghchi&rsquo;s Lebanon ceasefire statement appeared across all three outlets as Iran&rsquo;s current red line. Mojtaba Khamenei, installed as Supreme Leader on 9&nbsp;March, has not appeared publicly; his required role as deal approver was not addressed in open state-media output. &rarr; supports <span class="cite">F1</span> without move</p>"""

# ---- SCENARIO MAP ----
# Escalation: P(F1 new closure action AND talks fail) = 0.45 * 0.65 ≈ 0.29 → 30%
# De-esc: P(F5 Hormuz recovery by Jul 2) anchored at 0.25 → ~20%
# Protracted: residual 50%
SCN = {"esc": 30, "prot": 50, "desc": 20}
ESC_S = ('Iran&rsquo;s 201-craft IRGCN build-up at the strait and its declarative suspension of mediator '
         'channels keep a concrete new closure action the live near-term risk (<span class="cite" style="color:var(--red)">F1</span>&nbsp;45%); '
         'absent a re-engagement signal this week, escalation is the default trajectory.')
PROT_S = ('With the signed framework at the 5%&nbsp;floor (<span class="cite" style="color:var(--orange)">F2</span>), '
          're-engagement probability at 35% (<span class="cite" style="color:var(--orange)">F4</span>), '
          'and Hormuz commercial transit at ~4/day far below the recovery bar '
          '(<span class="cite" style="color:var(--orange)">F5</span>&nbsp;25%), the war most likely '
          'grinds on without resolution through the near-term window.')
DESC_S = ('A genuine de-escalation requires Iran to re-engage (<span class="cite" style="color:var(--green)">F4</span>), '
          'a principals-confirmed framework, and verified shipping recovery &mdash; '
          'none of which the board prices as better-than-even within 30&nbsp;days.')

# ---- REGIME CHANGE WATCH (non-Sunday: inherit from last review 2026-05-11) ----
REGIME = {
    "last": "2026-05-11", "next": "2026-06-07",
    "iran_range": "20&ndash;30%",
    "iran_drivers": ("Mojtaba Khamenei installed 9&nbsp;March has not appeared publicly and is cited as "
        "a required approver of any US framework; the 1&nbsp;June suspension of talks and the Hormuz-closure "
        "posture show a leadership leaning on confrontation, but no fracture in the security apparatus is "
        "evident from open sources. (Range carried unchanged from 2026-05-11; next review 2026-06-07.)"),
    "net_range": "40&ndash;50%",
    "net_drivers": ("The dissolution bill passed first reading 106&ndash;0 on 2&nbsp;June and the House "
        "Committee advanced it the same day without inserting an election date; the coalition retains its "
        "majority and no party has formally departed. UTJ/Shas pressure over the Haredi conscription bill "
        "keeps early-exit risk elevated without yet forcing it. (Range carried unchanged; next review 2026-06-07.)"),
}

# ---- SOURCES (up to 15, last 7 days, typed) ----
SOURCES = [
    ("TIER1", "CNBC", "2026-06-01", "https://www.cnbc.com/2026/06/01/iran-us-negotiations-strait-of-hormuz.html",
     "Iran stops negotiations, vows to 'completely' block Hormuz"),
    ("TIER1", "CNBC", "2026-06-02", "https://www.cnbc.com/amp/2026/06/02/rubio-iran-nuclear-talks-trump-war-strategy-hormuz.html",
     "Rubio: US in talks with Iran; Iran acknowledges nuclear program as subject"),
    ("TIER1", "CNN", "2026-06-01", "https://www.cnn.com/2026/06/01/world/live-news/iran-trump-lebanon-war-news",
     "Trump insists talks continue after Iran suspended negotiations"),
    ("TIER1", "CNN", "2026-06-02", "https://www.cnn.com/2026/06/02/business/strait-of-hormuz-ship-traffic",
     "94 days of paralysis: The Strait of Hormuz remains choked off"),
    ("TIER1", "Al Jazeera", "2026-06-01", "https://www.aljazeera.com/news/2026/6/1/us-iran-trade-new-attacks-amid-talks-heres-what-we-know",
     "US, Iran trade attacks amid talks — here is what we know"),
    ("TIER1", "Iran International", "2026-06-01", "https://www.iranintl.com/en/202606012472",
     "Araghchi: Iran-US ceasefire covers Lebanon; violations on one front void all"),
    ("TIER1", "Democracy Now!", "2026-06-02", "https://www.democracynow.org/2026/6/2/lebanon_israel_iran",
     "Iran suspends US talks as Israel expands Lebanon offensive"),
    ("TIER1", "Axios", "2026-05-28", "https://www.axios.com/2026/05/28/iran-peace-deal-trump-approval",
     "Scoop: US and Iran reach deal but need Trump's final approval"),
    ("TIER1", "Times of Israel", "2026-06-02", "https://www.timesofisrael.com/mks-advance-bill-to-dissolve-knesset-and-potentially-move-up-elections-to-september/",
     "MKs advance Knesset dissolution bill 106-0; no election date set"),
    ("TIER1", "Haaretz", "2026-06-02", "https://www.haaretz.com/israel-news/elections/2026-06-02/",
     "Knesset first reading of dissolution bill passes 106-0"),
    ("TIER1", "Fortune", "2026-06-01", "https://fortune.com/2026/06/01/strait-of-hormuz-us-iranian-lanes-ship-traffic-airstrikes-missile-attacks-drones/",
     "Hormuz splitting into US and Iranian lanes; IRGCN small-craft density rises"),
    ("STATE_MEDIA", "Tasnim (via ABC7/multiple)", "2026-06-01", "https://abc7news.com/live-updates/iran-war-news-trump-peace-deal-strait-of-hormuz-oil-gas-prices/19168718/",
     "Iran walks away from talks; Tasnim confirms suspension"),
    ("STATE_MEDIA", "IRNA (cited in multiple outlets)", "2026-06-02", "https://www.cnbc.com/amp/2026/06/02/rubio-iran-nuclear-talks-trump-war-strategy-hormuz.html",
     "IRNA: 'no clear prospect of fruitful negotiations'; US demands 'unreasonable'"),
    ("OSINT", "Windward AI", "2026-06-01", "https://windward.ai/blog/hormuz-dark-fleet-stalls-as-enforcement-widens/",
     "EO imagery: ~201 IRGCN small craft massed at Larak Island, 30 May (largest single-day footprint)"),
    ("OSINT", "Windward AI (vessel strikes tracker)", "2026-06-02", "https://windward.ai/blog/iran-war-vessel-attacks-and-maritime-infrastructure-strikes/",
     "IMO tally: 39 vessel strikes, 11 deaths since 28 Feb; unknown projectile 2 Jun"),
]
src_html = "\n".join(
    '      <li>\n        <span class="source-tier tier-%s">%s</span>\n        <a href="%s" target="_blank">%s (%s)</a>\n        &mdash; %s\n      </li>' % (t, t, url, esc(outlet), d, esc(title))
    for (t, outlet, d, url, title) in SOURCES
)

# ---- EXPERT QUOTES (Rubio + Araghchi; both cited in DELTA) ----
EXPERT_HTML = """        <div class="expert-quote">
          <div class="expert-name">Marco Rubio &mdash; US Secretary of State</div>
          <p>Senate Foreign Relations Committee testimony, 2026-06-02 (CNBC): &ldquo;There is the prospect that [Iran] could negotiate aspects of their nuclear program &mdash; something that just a month ago they were refusing to even mention.&rdquo;</p>
        </div>
        <div class="expert-quote">
          <div class="expert-name">Abbas Araghchi &mdash; Iranian Foreign Minister</div>
          <p>Public statement, 2026-06-01 (Iran International / Tasnim): &ldquo;The ceasefire between Iran and the US is unequivocally a ceasefire on all fronts, including in Lebanon. Its violation on one front is a violation of the ceasefire on all fronts.&rdquo;</p>
        </div>"""

# ---- fill skeleton ----
h = skeleton
repl = [
    (r'<span class="date-badge"><!-- FILL: DATE_STRING.*?--></span>', '<span class="date-badge">%s</span>' % DATE_STRING),
    (r'<span class="war-day"><!-- FILL: WAR_DAY.*?--></span>', '<span class="war-day">%s</span>' % WAR_DAY),
    (r'<span id="pub-ts"><!-- FILL: PUBLISH_TS --></span>', '<span id="pub-ts">%s</span>' % PUBLISH_TS),
    (r'<span id="build-id"([^>]*)><!-- FILL: VERSION --></span>', r'<span id="build-id"\1>%s</span>' % VERSION),
]
for pat, rep in repl:
    h = re.sub(pat, rep, h, count=1, flags=re.DOTALL)

# direction of travel
h = re.sub(r'<!-- FILL: DIRECTION_OF_TRAVEL.*?-->', DIRECTION, h, count=1, flags=re.DOTALL)
# board meta
h = re.sub(r'<span class="meta"><!-- FILL: e\.g\. "7 active.*?--></span>', '<span class="meta">%s</span>' % BOARD_META, h, count=1, flags=re.DOTALL)
# board cards
h = re.sub(r'<!-- FILL: forecast cards sorted.*?-->', BOARD_HTML, h, count=1, flags=re.DOTALL)
# delta
h = re.sub(r'<!-- FILL: 3-5 paragraphs.*?-->', DELTA, h, count=1, flags=re.DOTALL)
# scenario bar widths + labels
h = h.replace('style="width:<!-- FILL: ESCALATION_PCT -->%;"><!-- FILL: e.g. "Escalation 25%" -->',
              'style="width:%d%%;">Escalation %d%%' % (SCN["esc"], SCN["esc"]))
h = h.replace('style="width:<!-- FILL: PROTRACTED_PCT -->%;"><!-- FILL: e.g. "Protracted 40%" -->',
              'style="width:%d%%;">Protracted %d%%' % (SCN["prot"], SCN["prot"]))
h = h.replace('style="width:<!-- FILL: DEESCALATION_PCT -->%;"><!-- FILL: e.g. "De-esc 35%" -->',
              'style="width:%d%%;">De-esc %d%%' % (SCN["desc"], SCN["desc"]))
h = re.sub(r'<!-- FILL: 1 sentence on what drives or blocks escalation -->', ESC_S, h, count=1)
h = re.sub(r'<strong class="label-prot">Protracted path:</strong> <!-- FILL: 1 sentence -->',
           '<strong class="label-prot">Protracted path:</strong> ' + PROT_S, h, count=1)
h = re.sub(r'<strong class="label-desc">De-escalation path:</strong> <!-- FILL: 1 sentence -->',
           '<strong class="label-desc">De-escalation path:</strong> ' + DESC_S, h, count=1)
# inside iran
h = re.sub(r'<!-- FILL: ~200 word state-media decode.*?-->', INSIDE_IRAN, h, count=1, flags=re.DOTALL)
# regime change
h = re.sub(r'<!-- FILL: LAST_REVIEWED_DATE -->', REGIME["last"], h, count=1)
h = re.sub(r'<!-- FILL: NEXT_SUNDAY -->', REGIME["next"], h, count=1)
h = re.sub(r'<!-- FILL: IRAN_RC_RANGE e\.g\. "15-25%" -->', REGIME["iran_range"], h, count=1)
h = re.sub(r'<!-- FILL: 1-2 sentence driver summary, ban same verbs -->', REGIME["iran_drivers"], h, count=1)
h = re.sub(r'<!-- FILL: NETANYAHU_RANGE -->', REGIME["net_range"], h, count=1)
h = re.sub(r'<!-- FILL: driver summary -->', REGIME["net_drivers"], h, count=1)
# sources
h = re.sub(r'<!-- FILL: source items.*?-->', src_html, h, count=1, flags=re.DOTALL)
# expert appendix
h = re.sub(r'<!-- FILL: e\.g\. "3 quotes" or "no quotes today" -->', "2 expert quotes", h, count=1)
h = re.sub(r'<!-- FILL: One <div class="expert-quote">.*?-->', EXPERT_HTML, h, count=1, flags=re.DOTALL)
# footer
h = re.sub(r'Generated <!-- FILL: GENERATION_DATE --> \(<!-- FILL: VERSION -->\)',
           'Generated %s (%s)' % (GEN_DATE, VERSION), h, count=1)
h = re.sub(r'Next automatic update: <!-- FILL: NEXT_RUN_DATE -->', 'Next automatic update: %s' % NEXT_RUN, h, count=1)

# convert &rarr; to literal → so lint closure-regex matches
h = h.replace('&rarr;', '→')

# sanity: no FILL markers left
leftover = re.findall(r'<!-- FILL:.*?-->', h, flags=re.DOTALL)
if leftover:
    sys.stderr.write("UNFILLED MARKERS:\n" + "\n".join(m[:80] for m in leftover) + "\n")
    sys.exit(3)

out = DRAFT / "index.html.new"
out.write_text(h, encoding="utf-8")
print("wrote", out, len(h), "bytes")
