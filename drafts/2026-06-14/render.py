#!/usr/bin/env python3
"""Deterministic renderer: v45 skeleton + forecasts-updated.json + Judge text -> index.html.new (Day 107 / v48.0)"""
import json, re, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[2]
DRAFT = Path(__file__).resolve().parent
skeleton = (ROOT / "templates/v45-skeleton.html").read_text(encoding="utf-8")
active = json.loads((DRAFT / "forecasts-updated.json").read_text(encoding="utf-8"))

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

DATE_STRING = "June 14, 2026"
WAR_DAY = "Day 107"
PUBLISH_TS = "2026-06-14T07:00:00Z"
VERSION = "v48.0"
GEN_DATE = "2026-06-14"
NEXT_RUN = "2026-06-15"
BOARD_META = "6 active &middot; last reasoned 2026-06-14"

TODAY = date(2026, 6, 14)
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
    new = f["created_at"] == "2026-06-14"
    if new:
        delta_cls, delta_txt = "no-move", "New forecast"
    elif f["fnum"] in ("F7",) and f["owner_category"] == "regime":
        diff = p - pp
        if diff == 0:
            delta_cls, delta_txt = "no-move", "No change &mdash; weekly cadence only"
        elif diff > 0:
            delta_cls = "move-up"
            delta_txt = "&#8593; +%dpp from %d%% (%s) &mdash; Sunday review" % (diff, pp, f["prior_date"])
        else:
            delta_cls = "move-down"
            delta_txt = "&#8595; &minus;%dpp from %d%% (%s) &mdash; Sunday review" % (abs(diff), pp, f["prior_date"])
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

fs = [f for f in active["forecasts"] if f.get("status") == "ACTIVE"]
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

DIRECTION = (
    'The forecast board on Day 107 is dominated by the Islamabad Declaration text finalization: '
    '<span class="cite">N1</span> at p=72%% (formal signing by June 21) and '
    '<span class="cite">F2</span> at p=75%% (structured round by June 24) together drive a '
    'de-escalation trajectory, partially offset by <span class="cite">F3</span> at p=48%% '
    '(bilateral Israel-Iran exchange by June 24) and <span class="cite">F4</span> at p=5%% '
    '(Hormuz recovery near-floor), with diplomatic closure and military escalation risk '
    'simultaneously elevated through the next ten days.'
)

DELTA = """\
      <p>Pakistan Prime Minister Shehbaz Sharif on June 12, 2026, publicly confirmed that the United States and Iran had reached &ldquo;final, agreed upon text&rdquo; of the Islamabad Declaration &mdash; a Memorandum of Understanding brokered through Pakistani shuttle diplomacy led by Sharif and Field Marshal Asim Munir. CNBC, NBC News, and Washington Post all carried the announcement in the same news cycle, with Sharif stating that Pakistan was preparing for electronic signing &ldquo;in the next 24 hours.&rdquo; &rarr; moved <span class="cite">F2</span>, <span class="cite">N1</span></p>
      <p>President Trump on June 13 told press the Iran deal was &ldquo;scheduled to get signed tomorrow&rdquo; (Sunday June 14), while Iranian Foreign Minister Araghchi confirmed the MOU had &ldquo;never been closer&rdquo; (NPR, CBS News live blog). Iran MFA spokesman Esmaeil Baghaei on June 13&ndash;14 explicitly stated no signing ceremony would take place on Sunday, describing Iran&rsquo;s position as still in &ldquo;final deliberations&rdquo; and attributing delay to &ldquo;hesitation from the other side&rdquo; (France 24, Athens Times). The Islamabad Declaration text includes a 440&nbsp;kg enriched-uranium stockpile retention clause and a 30-day Hormuz reopening provision (TechTimes June 13) &mdash; structural elements that give the Iranian leadership domestic political cover to proceed without triggering hardline accusations of capitulation. &rarr; moved <span class="cite">F2</span>, <span class="cite">N1</span></p>
      <p>Israel and Iran executed confirmed bilateral strikes on June 7&ndash;8 &mdash; Israeli strikes on targets in Tehran, Tabriz, and Isfahan; Iranian missile salvos into northern Israel (CNN, Time, Al Jazeera, Euronews) &mdash; but this exchange predates the <span class="cite">F3</span> tracking window opening June 10. Post-June 10, Al Jazeera&rsquo;s June 10 live blog documented US strikes on Iranian targets following a downed helicopter; bilateral Israel-Iran state-on-state exchange after June 10 has not been confirmed by two independent TIER1 sources within a 48h window, which is the threshold <span class="cite">F3</span> requires. &rarr; moved <span class="cite">F3</span></p>
      <p>Hormuz commercial transits remained in the 2&ndash;4 vessel/day range through June 13&ndash;14, confirmed by hormuztracking.com (4 vessels June 13), PortWatch (2 transits June 7 vs pre-war baseline of approximately 94/day), and NBC News UANI shipping update. The 30-day Hormuz reopening clause in the Islamabad Declaration text means even a June 14 signing would not achieve &ge;50-transit 7-day averages before the July 2 <span class="cite">F4</span> horizon. CENTCOM confirmed MCM operations commenced April 11 (centcom.mil, Naval News, DefenseScoop), a date that predates <span class="cite">F5</span>&rsquo;s tracking window and retires that forecast as OBE. &rarr; moved <span class="cite">F4</span></p>
      <p>In Israeli domestic politics, no second or third Knesset reading of the dissolution bill has been scheduled as of June 14, despite first reading passing 106&ndash;0 on June 2. UTJ (United Torah Judaism) formally quit Netanyahu&rsquo;s government over the unresolved haredi draft bill dispute (JNS, Jewish Chronicle, Times of Israel), reducing the effective working majority toward the 61-seat threshold. Coalition negotiations over the election date (Netanyahu pushing October, haredi parties pressing September) remain unresolved, with Shas&rsquo;s continued participation under active leverage pressure. &rarr; moved <span class="cite">F6</span>, <span class="cite">F7</span></p>"""

INSIDE_IRAN = """\
      <p>Iranian domestic messaging this week combined forward diplomatic language with institutional constraint management. Araghchi&rsquo;s June 12 characterization of the MOU as &ldquo;closer than ever&rdquo; was delivered in response to Pakistan&rsquo;s text confirmation, not as a freestanding initiative &mdash; a pattern consistent with Iran&rsquo;s diplomatic practice of allowing the Foreign Minister to convey flexibility while MFA spokesman Baghaei manages expectations and preserves deniability. Baghaei&rsquo;s explicit denial of Sunday signing on June 13&ndash;14, framed as &ldquo;hesitation from the other side,&rdquo; placed delay attribution on Washington without closing the door on an imminent agreement. &rarr; supports <span class="cite">F2</span> without move</p>
      <p>The 440&nbsp;kg enriched-uranium stockpile retention clause secured in the Islamabad Declaration text allows the leadership to frame the agreement domestically as a non-capitulation: nuclear material is not handed over or destroyed pre-signing, with nuclear issues deferred to 60-day follow-on talks. This structure gives the regime political cover to sign without triggering hardline accusations of surrender, and is consistent with the principle of maintaining nuclear ambiguity as a strategic asset. &rarr; <span class="context-only">context only</span></p>
      <p>The IRGC&rsquo;s pre-June 8 threat &mdash; energy-asset strikes against US and Israeli regional partners if Iranian energy facilities were attacked &mdash; and the subsequent pause after Israeli strikes halted on June 8, confirms the IRGC as a functional constraint on both the deal timeline and on autonomous military escalation. MCM operations proceeding without Iranian re-mining since April 11 represent a tacit acceptance of the operational demining track, and the absence of IRGC re-mining through Day 107 is consistent with a leadership calculation that Hormuz closure costs exceed its current leverage value. &rarr; supports <span class="cite">F4</span> without move</p>"""

SCN = {"esc": 20, "prot": 25, "desc": 55}
ESC_S = (
    'Escalation path (20%): Islamabad Declaration signing fails on HEU language or US-side delay, '
    'a bilateral Israel-Iran exchange recurs in the June 10&ndash;24 window (<span class="cite">F3</span> p=48%), '
    'and Hormuz closure extends past the July 2 horizon (<span class="cite">F4</span> p=5%).'
)
PROT_S = (
    'Protracted path (25%): Declaration signed (<span class="cite">N1</span>) but 30-day Hormuz '
    'reopening clause drags recovery past July 2 (<span class="cite">F4</span> confirmed at near-floor), '
    'and follow-on 60-day nuclear talks stall without resumed bilateral strikes.'
)
DESC_S = (
    'De-escalation path (55%): Islamabad Declaration formally signed within the week '
    '(<span class="cite">N1</span> p=72%), structured round convened by June 24 '
    '(<span class="cite">F2</span> p=75%), bilateral Israel-Iran exchange does not recur '
    'in the June 10&ndash;24 window, and MCM operations continue unimpeded.'
)

REGIME = {
    "last": "2026-06-14", "next": "2026-06-21",
    "iran_range": "18&ndash;25%",
    "iran_drivers": (
        "Supreme Leader Khamenei retains institutional control and the Islamabad Declaration&rsquo;s "
        "HEU retention clause was designed to preserve the nuclear legacy framing; no credible "
        "succession crisis or IRGC fracture has been reported through Day 107. Economic pressure "
        "from Hormuz closure and direct US/Israeli strikes on Qeshm/Jask add structural stress "
        "without producing observable elite defection. Range revised down from 20&ndash;30% "
        "on deal-track progress; next review 2026-06-21."
    ),
    "net_range": "40&ndash;52%",
    "net_drivers": (
        "UTJ formally quit Netanyahu&rsquo;s government (JNS, Jewish Chronicle, Times of Israel), "
        "reducing the effective working majority toward the 61-seat threshold; Shas (11 seats) "
        "remains under active leverage pressure. The dissolution bill advanced (106&ndash;0 first "
        "reading June 2) with no second reading scheduled; F6 (p=30%) and F7 (p=50%) both "
        "incorporate the controlled dissolution path plus involuntary collapse risk. "
        "Range revised up; next review 2026-06-21."
    ),
}

SOURCES = [
    ("TIER1", "CNBC", "2026-06-12", "https://www.cnbc.com/2026/06/12/iran-deal-trump-pakistan-sharif.html", "Pakistan PM: US-Iran deal text finalized, signing 'in next 24 hours'"),
    ("TIER1", "NBC News", "2026-06-12", "https://www.nbcnews.com/world/iran/live-blog/live-updates-us-iran-drones-trump-deal-war-hormuz-tehran-rcna349750", "Islamabad Declaration text confirmed; electronic signing preparation announced"),
    ("TIER1", "Washington Post", "2026-06-12", "https://www.washingtonpost.com/world/2026/06/12/pakistan-prime-minister-says-us-iran-deal-text-finalized/", "Pakistan confirms Islamabad Declaration text finalization"),
    ("TIER1", "NPR", "2026-06-13", "https://www.npr.org/2026/06/13/nx-s1-5857149/trump-iran-war-peace-deal", "Trump declares Iran deal 'scheduled to get signed tomorrow'"),
    ("TIER1", "CBS News", "2026-06-13", "https://www.cbsnews.com/live-updates/iran-war-deal-signing-june-2026/", "Trump: 'immediately after signing, the Hormuz Strait will be OPEN TO ALL'"),
    ("TIER1", "CNN", "2026-06-13", "https://edition.cnn.com/2026/06/13/world/live-news/iran-war-trump-israel", "US, Iran near agreement; officials plan virtual signing"),
    ("TIER1", "France 24", "2026-06-13", "https://www.france24.com/en/middle-east/20260613-iran-baghaei-deal-not-sunday", "Baghaei denies Sunday signing; describes Iran in 'final deliberations'"),
    ("TIER1", "Athens Times", "2026-06-13", "https://athens-times.com/iranian-foreign-ministry-spokesperson-us-iran-islamabad-memorandum-not-to-be-signed-tomorrow/", "Iran attributes deal delay to 'hesitation from the other side'"),
    ("TIER1", "Al Jazeera", "2026-06-10", "https://www.aljazeera.com/news/liveblog/2026/6/10/iran-war-live", "US strikes Iranian targets following downed helicopter; Tehran vows response"),
    ("OSINT", "TechTimes", "2026-06-13", "https://www.techtimes.com/articles/318319/20260613/iran-peace-deal-text-agreed-440kg-enriched-uranium-stays-tehran-during-60-day-talks.htm", "MOU terms: 30-day Hormuz clause, 440 kg HEU retention, 60-day nuclear follow-on"),
    ("OSINT", "hormuztracking.com", "2026-06-13", "https://hormuztracking.com/", "Live tracker: 4 commercial vessels transiting Hormuz on June 13"),
    ("STATE_MEDIA", "Naval News / centcom.mil", "2026-04-11", "https://www.navalnews.com/naval-news/2026/04/u-s-forces-start-mine-clearance-mission-in-strait-of-hormuz/", "CENTCOM: US Forces Start Mine Clearance Mission in Strait of Hormuz"),
    ("TIER1", "CNN / Time / Al Jazeera", "2026-06-08", "https://www.aljazeera.com/news/2026/6/8/israel-and-iran-halt-attacks-but-sabre-rattling-continues", "June 7-8: IDF strikes Tehran/Tabriz/Isfahan; Iranian missile salvo into northern Israel confirmed"),
    ("OSINT", "NBC News / UANI", "2026-06-14", "https://www.nbcnews.com/world/iran/live-blog/live-updates-us-iran-drones-trump-deal-war-hormuz-tehran-rcna349750", "Hormuz shipping tracker: Strait effectively closed, &le;4 vessels/day"),
    ("TIER1", "Times of Israel", "2026-06-14", "https://www.timesofisrael.com/mks-unanimously-advance-bill-to-dissolve-knesset-and-trigger-elections-no-date-set/", "Knesset dissolution bill: first reading 106-0; no second reading scheduled; date debate ongoing"),
]
src_html = "\n".join(
    '      <li>\n        <span class="source-tier tier-%s">%s</span>\n        <a href="%s" target="_blank">%s (%s)</a>\n        &mdash; %s\n      </li>' % (t, t, url, esc(outlet), d, esc(title))
    for (t, outlet, d, url, title) in SOURCES
)

EXPERTS = []
expert_html = '<p class="expert-empty">No expert citations in today\'s Delta.</p>'
EXPERT_SUMMARY = "no quotes today"

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
