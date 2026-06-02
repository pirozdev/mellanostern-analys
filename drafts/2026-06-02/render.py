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
DATE_STRING = "June 2, 2026"
WAR_DAY = "Day 95"
PUBLISH_TS = "2026-06-02T07:00:00Z"
VERSION = "v46.0"
GEN_DATE = "2026-06-02"
NEXT_RUN = "2026-06-03"
BOARD_META = "7 active &middot; last reasoned 2026-06-02"

# ---- buckets by days-to-horizon from 2026-06-02 ----
from datetime import date
TODAY = date(2026, 6, 2)
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
    new = f["created_at"] == "2026-06-02"
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

# ---- text sections (from Judge, raw HTML) ----
DIRECTION = ('The diplomatic track ruptured rather than closed &mdash; Iran\'s 1 June suspension of '
            'mediator channels and its threat to fully shut Hormuz push both the signed-framework and '
            'shipping-recovery nodes lower while raising near-term closure-action risk, citing '
            '<span class="cite">F1</span>, <span class="cite">F2</span> and <span class="cite">F3</span>.')

DELTA = """      <p>Iran-US diplomacy moved from near-breakthrough to rupture. Negotiators reached a tentative 60-day framework MOU on 28 May &mdash; a 60-day ceasefire extension, Hormuz reopening, a lift of the US port blockade, and 60-day nuclear talks on HEU and frozen assets &mdash; but Trump declined final approval, with Vance citing &ldquo;a couple of language points&rdquo; and the 29 May meeting ending without a &ldquo;final determination.&rdquo; On 1 June Iran suspended all mediator-channel communications, Araghchi stating a violation &ldquo;on one front is a violation of the ceasefire on all fronts&rdquo; and tying re-engagement to an Israeli halt in Lebanon. &rarr; moved <span class="cite">F2</span></p>
      <p>The Strait of Hormuz stayed effectively closed. IMF PortWatch&rsquo;s last published day, 24 May, recorded ~4 transits against a pre-crisis baseline near 95/day; Maersk, MSC, CMA CGM and Hapag-Lloyd remained suspended and P&amp;I cover withdrawn. Bloomberg on 29 May described more vessels leaving under US escorts but recorded no daily count near 50, resting on the deal Iran suspended 1 June; Tehran then said via Tasnim it would &ldquo;completely&rdquo; block the strait. &rarr; moved <span class="cite">F3</span></p>
      <p>Israeli coalition politics advanced toward dissolution without locking a date. A dissolution bill passed preliminary reading 110-0 on 20 May and first reading 106-0 on 2 June, and the House Committee advanced it the same day but postponed an election date; Netanyahu pushed for October while UTJ and Shas pressed for ~15 September amid the unresolved Haredi conscription bill. No earlier date was set by the 1 June horizon, leaving the question of final passage open. &rarr; moved <span class="cite">F6</span></p>
      <p>The Lebanon track ran on two clocks. The 16 April truce was extended 45 days on 15 May, with a security track set for 29 May and Washington talks for 2-3 June. Through 22 May Israeli strikes continued daily, with about six Lebanese medics killed in a 24-hour span around that date, yet neither US sponsorship withdrawal nor a Lebanese void declaration occurred by the horizon. &rarr; <span class="context-only">context only</span></p>
      <p>Oil tracked the diplomacy. Brent fell roughly 19% over May, its worst month since the pandemic, to near $92.56 on ceasefire optimism, then rose about 5% above $95 on 1 June after Iran suspended talks and threatened full Hormuz closure, having spiked above 7% intraday. &rarr; supports <span class="cite">F1</span> without move</p>"""

INSIDE_IRAN = """      <p>Iranian state and state-affiliated media drove the 1 June rupture. Tasnim reported that Tehran would stop exchanging messages with Washington through intermediaries and move to &ldquo;completely&rdquo; block the Strait of Hormuz, framing it as a response to Israel&rsquo;s expanding Lebanon offensive and to US strikes. Araghchi&rsquo;s MFA channel was the headline vehicle: his statement that &ldquo;the ceasefire between Iran and the US is unequivocally a ceasefire on all fronts, including in Lebanon,&rdquo; and that &ldquo;its violation on one front is a violation of the ceasefire on all fronts,&rdquo; was carried as the official position, conditioning any re-engagement on an Israeli halt in Lebanon. Coverage referenced the appointed Mojtaba Khamenei as a required approver of any framework while noting he has not appeared publicly since his installation. All of this is verifiable only through Western TIER1 aggregation &mdash; WaPo, NPR, CNBC, and Euronews citing Tasnim and IRNA &mdash; rather than direct outlet fetches, so the granular wording should be treated as secondhand and the closure threat read against an already de facto shut strait. &rarr; <span class="context-only">context only</span></p>"""

SCN = {"esc": 40, "prot": 50, "desc": 10}
ESC_S = ('Iran&rsquo;s suspension of talks and its Tasnim threat to &ldquo;completely&rdquo; close Hormuz '
         'keep a fresh closure action a live near-term risk (F1 0.40).')
PROT_S = ('With the signed framework unlikely by 5 June (F2 0.10) and Hormuz transits stuck near 4/day '
          '(F3 0.15, F5 0.30) while resumption odds sit only moderate (F4 0.45) and Israeli dissolution '
          'stays unresolved (F6 0.50, F7 0.35), the war most likely grinds on without resolution.')
DESC_S = ('A genuine de-escalation requires both a signed framework and a verified shipping recovery, '
          'neither of which the board prices as probable inside the window.')

REGIME = {
    "last": "2026-05-11", "next": "2026-06-07",
    "iran_range": "20&ndash;30%",
    "iran_drivers": ("Mojtaba Khamenei installed 9 March remains unseen in public and is cited as a required "
        "approver of any US framework; the 1 June suspension of talks and the Hormuz-closure threat show a "
        "leadership leaning on confrontation, but no fracture in the security apparatus is evident. "
        "(Carried unchanged from 2026-05-11; next review 2026-06-07.)"),
    "net_range": "40&ndash;50%",
    "net_drivers": ("A dissolution bill passed first reading 106-0 on 2 June with preliminary passage 110-0 "
        "on 20 May, but no election date is set and the coalition has not lost its majority; UTJ/Shas pressure "
        "over the Haredi conscription bill keeps early-exit risk elevated without yet forcing it. "
        "(Range carried unchanged; next review 2026-06-07.)"),
}

SOURCES = [
    ("TIER1", "Axios", "2026-05-28", "https://www.axios.com/2026/05/28/iran-peace-deal-trump-approval", "US and Iran reach deal but need Trump's final approval"),
    ("TIER1", "CNN", "2026-05-28", "https://www.cnn.com/2026/05/28/world/live-news/iran-war-us-news", "US and Iran reach tentative agreement, Trump hasn't signed off"),
    ("TIER1", "PBS NewsHour", "2026-05-28", "https://www.pbs.org/newshour/world/u-s-and-iranian-negotiators-reach-tentative-deal-to-extend-ceasefire-and-start-new-nuclear-talks", "Tentative deal to extend ceasefire and start nuclear talks"),
    ("TIER1", "CNBC", "2026-05-29", "https://www.cnbc.com/2026/05/29/trump-iran-deal-hormuz-nuclear-war.html", "Trump ends Iran meeting without 'final determination'"),
    ("TIER1", "CNBC", "2026-05-29", "https://www.cnbc.com/2026/05/29/oil-prices-iran-ceasefire-us-trump-strait-hormuz-energy-costs.html", "Oil drops 20% from 2026 peak on ceasefire optimism"),
    ("TIER1", "Washington Post", "2026-06-01", "https://www.washingtonpost.com/world/2026/06/01/iran-us-trade-strikes-deal-end-war-remains-elusive/", "Iran breaks off US ceasefire talks over Israeli attacks on Lebanon"),
    ("TIER1", "NPR", "2026-06-01", "https://www.npr.org/2026/06/01/g-s1-125285/iran-israel-us-lebanon-gaza", "Iran halts talks with US over Israeli actions"),
    ("TIER1", "CNBC", "2026-06-01", "https://www.cnbc.com/2026/06/01/iran-us-negotiations-strait-of-hormuz.html", "Iran stops negotiations, vows to 'completely' block Hormuz"),
    ("TIER1", "CNBC", "2026-05-15", "https://www.cnbc.com/2026/05/15/israel-lebanon-agree-to-extend-ceasefire-by-45-days-us-state-dept.html", "Israel-Lebanon agree to extend ceasefire by 45 days"),
    ("TIER1", "Bloomberg", "2026-05-15", "https://www.bloomberg.com/news/articles/2026-05-15/israel-lebanon-extend-ceasefire-45-days-after-washington-talks", "Israel, Lebanon extend ceasefire 45 days"),
    ("TIER1", "The National", "2026-05-15", "https://www.thenationalnews.com/news/us/2026/05/15/israel-lebanon-ceasefire-extended-by-45-days/", "Ceasefire extended 45 days but deadly strikes continue"),
    ("OSINT", "USNI News", "2026-05-01", "https://news.usni.org/2026/05/01/strait-of-hormuz-commercial-transits-at-lowest-level-since-operation-epic-fury-start-shipping-data-shows", "Hormuz commercial transits at lowest level"),
    ("OSINT", "CNN", "2026-06-02", "https://www.cnn.com/2026/06/02/business/strait-of-hormuz-ship-traffic", "Hormuz ship traffic near standstill (day 94)"),
    ("TIER1", "Times of Israel", "2026-06-02", "https://www.timesofisrael.com/mks-advance-bill-to-dissolve-knesset-and-potentially-move-up-elections-to-september/", "MKs advance Knesset dissolution bill, no date set"),
    ("STATE_MEDIA", "Euronews citing Tasnim/IRNA", "2026-06-01", "https://www.euronews.com/2026/06/01/tehran-suspended-negotiations-via-mediators-with-us-iranian-media-says", "Tehran suspended negotiations via mediators"),
]
src_html = "\n".join(
    '      <li>\n        <span class="source-tier tier-%s">%s</span>\n        <a href="%s" target="_blank">%s (%s)</a>\n        &mdash; %s\n      </li>' % (t, t, url, esc(outlet), d, esc(title))
    for (t, outlet, d, url, title) in SOURCES
)

# ---- fill skeleton ----
def fill(html, marker_substr, replacement):
    pat = re.compile(r"<!--\s*FILL:.*?-->", re.DOTALL)
    # we replace by sequential marker matching instead; handled below
    return html

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
h = re.sub(r'<!-- FILL: e\.g\. "3 quotes" or "no quotes today" -->', "no quotes today", h, count=1)
h = re.sub(r'<!-- FILL: One <div class="expert-quote">.*?-->', '<p class="expert-empty">No expert citations in today&rsquo;s Delta.</p>', h, count=1, flags=re.DOTALL)
# footer
h = re.sub(r'Generated <!-- FILL: GENERATION_DATE --> \(<!-- FILL: VERSION -->\)',
           'Generated %s (%s)' % (GEN_DATE, VERSION), h, count=1)
h = re.sub(r'Next automatic update: <!-- FILL: NEXT_RUN_DATE -->', 'Next automatic update: %s' % NEXT_RUN, h, count=1)

# literal arrow char required by lint closure regex + matches house style
h = h.replace('&rarr;', '→')

# sanity: no FILL markers left
leftover = re.findall(r'<!-- FILL:.*?-->', h, flags=re.DOTALL)
if leftover:
    sys.stderr.write("UNFILLED MARKERS:\n" + "\n".join(m[:80] for m in leftover) + "\n")
    sys.exit(3)

out = DRAFT / "index.html.new"
out.write_text(h, encoding="utf-8")
print("wrote", out, len(h), "bytes")
