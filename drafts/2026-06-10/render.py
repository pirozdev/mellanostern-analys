#!/usr/bin/env python3
"""Deterministic renderer: v45 skeleton + forecasts-updated.json + Judge text -> index.html.new (Day 103 / v47.0)"""
import json, re, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[2]
DRAFT = Path(__file__).resolve().parent
skeleton = (ROOT / "templates/v45-skeleton.html").read_text(encoding="utf-8")
active = json.loads((DRAFT / "forecasts-updated.json").read_text(encoding="utf-8"))

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

DATE_STRING = "June 10, 2026"
WAR_DAY = "Day 103"
PUBLISH_TS = "2026-06-10T07:00:00Z"
VERSION = "v47.0"
GEN_DATE = "2026-06-10"
NEXT_RUN = "2026-06-11"
BOARD_META = "7 active &middot; last reasoned 2026-06-10"

TODAY = date(2026, 6, 10)
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
    new = f["created_at"] == "2026-06-10"
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

DIRECTION = ('With the ceasefire actively faltering, a formal Iranian suspension of talks, June 7-8 strikes '
            'described as the worst in months, and Hormuz frozen near 2-10 transits per day, the trajectory is '
            'escalation over resumption, holding <span class="cite">F1</span> low, keeping '
            '<span class="cite">F4</span> depressed, and pricing a renewed direct Israel-Iran exchange at '
            '<span class="cite">F3</span> above even.')

DELTA = """      <p>The diplomatic track ruptured at the window start: on 2026-06-01 Iranian state media announced Tehran suspended mediated negotiations with the US over Israel&rsquo;s expanding operations in Lebanon and Gaza, tying resumption to a halt; Araghchi on 2026-06-03 stated there is no formal negotiation process underway, only written messages, and the one-page 60-day MOU remained unsigned with Trump&rsquo;s HEU and Hormuz amendments unresolved. &rarr; moved <span class="cite">F1</span></p>
      <p>The framework track produced no signed document by 2026-06-05 and no convened session followed, leaving a successor question on whether any mediator-hosted round occurs by 2026-06-24. &rarr; moved <span class="cite">F2</span></p>
      <p>Military activity escalated sharply: Iranian forces struck Kuwait&rsquo;s airport and Bahrain targets on June 2-3, the US struck Qeshm and Jask, and CNN on June 7-8 reported the worst Israel-Iran strikes in months, establishing an active two-way tempo. &rarr; moved <span class="cite">F3</span></p>
      <p>The strait stayed effectively closed at roughly 2-10 transits per day against a pre-war norm near 94, with Rubio describing mines across large segments and US clearance projected over months and not begun at scale, while Brent held near 95 dollars on June 8-9. &rarr; moved <span class="cite">F4</span></p>
      <p>Israeli politics advanced the coalition&rsquo;s own dissolution bill through a 106-0 first reading on 2026-06-02 after a 9-0 committee vote, with a Sept 8 to Oct 20 band floated but no fixed date set and two readings remaining. &rarr; moved <span class="cite">F6</span></p>"""

INSIDE_IRAN = """      <p>State framing this window combined defiance with conditionality. The 2026-06-01 suspension of mediated talks was presented as a principled stand, with Araghchi casting any acceptable US ceasefire as necessarily comprehensive across all fronts, including Lebanon, and framing the halt as a response to Israeli aggression; Ghalibaf accused Washington of violating the ceasefire&rsquo;s spirit through its support for Israel. &rarr; supports <span class="cite">F1</span> without move</p>
      <p>On 2026-06-04, at the Khomeini death-anniversary, a written statement attributed to Mojtaba Khamenei declared the enemy had suffered a decisive blow and a profound humiliation, while Rubio on 2026-06-02 described him as alive and increasingly engaging through written channels and intermediaries. State outlets amplified the reported IRGC seizure of the US-affiliated &lsquo;Arista&rsquo; as enforcement of transit laws, though that account rests on Fars/state-media sourcing without TIER1 corroboration. &rarr; <span class="context-only">context only</span></p>"""

SCN = {"esc": 55, "prot": 35, "desc": 10}
ESC_S = ('Escalation rises to the dominant weight on the June 7-8 worst-in-months Israel-Iran strikes, the '
         'June 2-3 attacks on Kuwait/Bahrain and US strikes on Qeshm/Jask, and the suspended talks, with a '
         'direct two-way exchange priced above even (F3 0.55).')
PROT_S = ('A protracted stalemate stays substantial as Hormuz holds near 2-10 transits/day with demining not '
          'begun at scale and no signed MOU, keeping any 50/day recovery remote (F4 0.20) and resumption gated '
          'on a held session (F1 0.30).')
DESC_S = ('De-escalation is thin and conditional on a mediator-hosted round or an Iranian rescinding of the '
          'June 1 suspension materializing inside the horizon (F2 0.40), against a rejected Lebanon ceasefire '
          'and unresolved MOU amendments.')

REGIME = {
    "last": "2026-05-11", "next": "2026-06-14",
    "iran_range": "20&ndash;30%",
    "iran_drivers": ("Mojtaba Khamenei consolidated as supreme leader post-28-Feb, governing via written "
        "intermediaries; Rubio on 2026-06-02 described him as alive and increasingly engaging, with a "
        "2026-06-04 written statement asserting control, showing continuity rather than imminent rupture "
        "despite sustained US/Israeli strikes on Qeshm/Jask. Range held; next review 2026-06-14."),
    "net_range": "40&ndash;50%",
    "net_drivers": ("The coalition advanced its own dissolution bill through a 106-0 first reading on "
        "2026-06-02 after a 9-0 committee vote, with a Sept 8&ndash;Oct 20 election band floated but no fixed "
        "date and haredi-draft/Basic Law Torah Study brinkmanship unresolved; the escalation adds wartime "
        "strain. Range held; next review 2026-06-14."),
}

SOURCES = [
    ("TIER1", "NPR", "2026-06-01", "https://www.npr.org/2026/06/01/g-s1-125285/iran-israel-us-lebanon-gaza", "Iran halts talks over Israeli actions"),
    ("STATE_MEDIA", "Euronews", "2026-06-01", "https://www.euronews.com/2026/06/01/tehran-suspended-negotiations-via-mediators-with-us-iranian-media-says", "Iran suspended negotiations via mediators"),
    ("TIER1", "Al Jazeera", "2026-06-03", "https://www.aljazeera.com/news/liveblog/2026/6/3/iran-war-live-us-strikes-irans-qeshm-says-tehran-attacks-kuwait-bahrain", "Araghchi: no formal process; US strikes Qeshm; Iran attacks Kuwait/Bahrain"),
    ("TIER1", "CNBC", "2026-06-02", "https://www.cnbc.com/2026/06/02/iran-war-strait-hormuz-marco-rubio-mine.html", "Rubio: Iran mined 'large segments' of Hormuz"),
    ("TIER1", "Al Jazeera", "2026-06-02", "https://www.aljazeera.com/news/2026/6/2/irans-supreme-leader-appears-more-active-as-talks-continue-uss-rubio", "Mojtaba alive, 'increasingly engaging'"),
    ("TIER1", "Al Jazeera", "2026-06-04", "https://www.aljazeera.com/news/2026/6/4/israel-and-lebanon-agree-to-conditional-ceasefire", "Israel-Lebanon conditional ceasefire"),
    ("TIER1", "Axios", "2026-06-03", "https://www.axios.com/2026/06/03/israel-lebanon-ceasefire-hezbollah-us", "Israel-Lebanon ceasefire; Hezbollah rejects"),
    ("TIER1", "NPR", "2026-06-04", "https://www.npr.org/2026/06/04/g-s1-125942/israel-lebanon-ceasefire", "Hezbollah rejects ceasefire"),
    ("TIER1", "Times of Israel", "2026-06-02", "https://www.timesofisrael.com/mks-advance-bill-to-dissolve-knesset-and-potentially-move-up-elections-to-september/", "Dissolution bill advances; date debate"),
    ("TIER1", "Jerusalem Post", "2026-06-02", "https://www.jpost.com/israel-news/politics-and-diplomacy/article-898048", "Dissolution bill passes first reading 106-0"),
    ("TIER1", "CNN", "2026-06-07", "https://www.cnn.com/2026/06/07/world/live-news/iran-war-trump-israel-lebanon", "Worst Israel-Iran strikes in months; talks not resumed"),
    ("TIER1", "Fortune", "2026-06-09", "https://fortune.com/article/price-of-oil-06-09-2026/", "Brent ~$95.06 June 9"),
    ("OSINT", "Critical Threats", "2026-06-06", "https://www.criticalthreats.org/analysis/iran-update-evening-special-report-june-6-2026", "June 5 IRGC fired on tankers; CENTCOM strikes Qeshm"),
    ("OSINT", "CNN", "2026-06-02", "https://www.cnn.com/2026/06/02/business/strait-of-hormuz-ship-traffic", "Hormuz ship traffic near standstill"),
    ("OSINT", "NPR", "2026-06-08", "https://www.npr.org/2026/06/08/nx-s1-5848001/the-strait-of-hormuzs-3-month-closure-could-set-a-dangerous-precedent-experts-worry", "3-month closure precedent"),
]
src_html = "\n".join(
    '      <li>\n        <span class="source-tier tier-%s">%s</span>\n        <a href="%s" target="_blank">%s (%s)</a>\n        &mdash; %s\n      </li>' % (t, t, url, esc(outlet), d, esc(title))
    for (t, outlet, d, url, title) in SOURCES
)

EXPERTS = [
    ("Abbas Araghchi, Iranian Foreign Minister", "There is no formal negotiation process underway between Iran and the United States. However, messages continue to be exchanged.", "Al Jazeera liveblog, 2026-06-03"),
    ("Marco Rubio, US Secretary of State", "increasingly engaging at some level, although all of his communications have been in writing and through intermediaries.", "Al Jazeera, 2026-06-02"),
]
expert_html = "\n        ".join(
    '<div class="expert-quote"><div class="expert-name">%s</div>&ldquo;%s&rdquo; &mdash; %s</div>' % (esc(name), esc(q), esc(src))
    for (name, q, src) in EXPERTS
)
EXPERT_SUMMARY = "2 quotes"

# ---- fill skeleton ----
h = skeleton
for pat, rep in [
    (r'<span class="date-badge"><!-- FILL: DATE_STRING.*?--></span>', '<span class="date-badge">%s</span>' % DATE_STRING),
    (r'<span class="war-day"><!-- FILL: WAR_DAY.*?--></span>', '<span class="war-day">%s</span>' % WAR_DAY),
    (r'<span id="pub-ts"><!-- FILL: PUBLISH_TS --></span>', '<span id="pub-ts">%s</span>' % PUBLISH_TS),
    (r'<span id="build-id"([^>]*)><!-- FILL: VERSION --></span>', r'<span id="build-id"\1>%s</span>' % VERSION),
]:
    h = re.sub(pat, rep, h, count=1, flags=re.DOTALL)

h = re.sub(r'<!-- FILL: DIRECTION_OF_TRAVEL.*?-->', DIRECTION, h, count=1, flags=re.DOTALL)
h = re.sub(r'<span class="meta"><!-- FILL: e\.g\. "7 active.*?--></span>', '<span class="meta">%s</span>' % BOARD_META, h, count=1, flags=re.DOTALL)
h = re.sub(r'<!-- FILL: forecast cards sorted.*?-->', BOARD_HTML, h, count=1, flags=re.DOTALL)
h = re.sub(r'<!-- FILL: 3-5 paragraphs.*?-->', DELTA, h, count=1, flags=re.DOTALL)
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
h = re.sub(r'<!-- FILL: ~200 word state-media decode.*?-->', INSIDE_IRAN, h, count=1, flags=re.DOTALL)
h = re.sub(r'<!-- FILL: LAST_REVIEWED_DATE -->', REGIME["last"], h, count=1)
h = re.sub(r'<!-- FILL: NEXT_SUNDAY -->', REGIME["next"], h, count=1)
h = re.sub(r'<!-- FILL: IRAN_RC_RANGE e\.g\. "15-25%" -->', REGIME["iran_range"], h, count=1)
h = re.sub(r'<!-- FILL: 1-2 sentence driver summary, ban same verbs -->', REGIME["iran_drivers"], h, count=1)
h = re.sub(r'<!-- FILL: NETANYAHU_RANGE -->', REGIME["net_range"], h, count=1)
h = re.sub(r'<!-- FILL: driver summary -->', REGIME["net_drivers"], h, count=1)
h = re.sub(r'<!-- FILL: source items.*?-->', src_html, h, count=1, flags=re.DOTALL)
h = re.sub(r'<!-- FILL: e\.g\. "3 quotes" or "no quotes today" -->', EXPERT_SUMMARY, h, count=1)
h = re.sub(r'<!-- FILL: One <div class="expert-quote">.*?-->', expert_html, h, count=1, flags=re.DOTALL)
h = re.sub(r'Generated <!-- FILL: GENERATION_DATE --> \(<!-- FILL: VERSION -->\)',
           'Generated %s (%s)' % (GEN_DATE, VERSION), h, count=1)
h = re.sub(r'Next automatic update: <!-- FILL: NEXT_RUN_DATE -->', 'Next automatic update: %s' % NEXT_RUN, h, count=1)

h = h.replace('&rarr;', '→')

leftover = re.findall(r'<!-- FILL:.*?-->', h, flags=re.DOTALL)
if leftover:
    sys.stderr.write("UNFILLED MARKERS:\n" + "\n".join(m[:80] for m in leftover) + "\n")
    sys.exit(3)

out = DRAFT / "index.html.new"
out.write_text(h, encoding="utf-8")
print("wrote", out, len(h), "bytes")
