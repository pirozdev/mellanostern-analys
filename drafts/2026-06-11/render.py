#!/usr/bin/env python3
"""Deterministic renderer: v45 skeleton + forecasts-updated.json + Judge text -> index.html.new (Day 104 / v48.0)"""
import json, re, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[2]
DRAFT = Path(__file__).resolve().parent
skeleton = (ROOT / "templates/v45-skeleton.html").read_text(encoding="utf-8")
active = json.loads((DRAFT / "forecasts-updated.json").read_text(encoding="utf-8"))

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

DATE_STRING = "June 11, 2026"
WAR_DAY = "Day 104"
PUBLISH_TS = "2026-06-11T07:00:00Z (auto-draft)"
VERSION = "v48.0"
GEN_DATE = "2026-06-11"
NEXT_RUN = "2026-06-12"
BOARD_META = "7 active &middot; F3 resolved YES &middot; last reasoned 2026-06-11"

TODAY = date(2026, 6, 11)
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
    new = f["created_at"] == "2026-06-11"
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

DIRECTION = ('The June 10&ndash;11 escalation cycle drove <span class="cite">F1</span> and '
             '<span class="cite">F2</span> to their lowest probabilities since the conflict&rsquo;s '
             'onset, <span class="cite">F4</span> to 5% as the Strait&rsquo;s near-complete shipping '
             'shutdown became formalized under IRGC hostile-fire declaration, and '
             '<span class="cite">F3</span> to YES resolution as the within-window Iran&ndash;Israel '
             'bilateral exchange threshold was met &mdash; collectively placing the conflict in its most '
             'acute military-dominant phase of the war&rsquo;s first 104 days.')

DELTA = """      <p>The June 10&ndash;11 window produced a sharp escalation cycle that materially worsened both the diplomatic and maritime tracks. On June 10, the US launched strikes on Iranian radar and drone sites in and around the Strait of Hormuz; Iran responded within hours with drone and missile fire on US military bases at Bahrain&rsquo;s Sheikh Isa airbase and Kuwait&rsquo;s Ali Al Salem and Ahmad Al-Jaber airbases, with all incoming ordnance intercepted and no reported US casualties. By June 11, the IRGC formally declared the Strait &ldquo;closed to all vessels, including oil tankers and commercial ships,&rdquo; with an explicit warning that any transiting vessel will be treated as a military target, and fired 12 ballistic missiles at Al-Azraq Air Base. &rarr; moved <span class="cite">F4</span>, <span class="cite">F5</span>, <span class="cite">F8</span></p>
      <p>On the diplomatic channel, Qatar dispatched a delegation to Tehran on June 10; Iranian and Qatari readouts described the contact only as &ldquo;bilateral discussions and exchange of views on regional developments&rdquo; &mdash; language that, per the ambiguity rules governing <span class="cite">F1</span> and <span class="cite">F2</span>, does not constitute a convened negotiating session. Written draft proposals continued to move through Qatar and Pakistan channels, but Araghchi&rsquo;s June 3 statement &mdash; that &ldquo;no formal negotiation process is underway&rdquo; &mdash; has not been rescinded by any Iranian official as of this reporting window. The June 1 suspension of mediated talks remains formally intact, with F1&rsquo;s five-day horizon and active military tempo making resumption before EOD June 16 a remote prospect. &rarr; moved <span class="cite">F1</span>, <span class="cite">F2</span></p>
      <p>The Israel&ndash;Iran bilateral exchange track crossed the resolution threshold within the June 10&ndash;24 window. June 7&ndash;8 saw IDF-confirmed strikes on Iranian &ldquo;strategic defence systems&rdquo; in western and central Iran with IRGC-confirmed reciprocal fire on Israeli-claimed targets, as reported by CNN, CBS News, and Al Jazeera. On June 11, the IRGC fired 12 ballistic missiles toward Israel and IDF confirmed active engagement with Iranian fire, with defensive intercept operations operational. Both named IDF and IRGC statements with TIER1 confirmation establish the within-window bilateral exchange; <span class="cite">F3</span> resolves YES. &rarr; moved <span class="cite">F3</span></p>
      <p>The maritime track reached near-complete shutdown. PortWatch recorded 2 vessel transits on June 7 against a pre-crisis baseline of 94/day; the June 10&ndash;11 IRGC closure re-declaration, war-risk insurance at 8&times; pre-crisis with six P&amp;I clubs withdrawn, and the hostile-fire warning for any transiting vessel eliminate any realistic path to the 50-transit/day threshold by July 2. CENTCOM&rsquo;s April MCM commencement established prior activity, but no CENTCOM statement confirms active operations in the June 10&ndash;11 hostile-fire environment. &rarr; moved <span class="cite">F4</span>; supports <span class="cite">F5</span> without move</p>
      <p>No second or third Knesset reading of the dissolution bill occurred in the June 10&ndash;11 window. Informal coalition consensus around October 20 as the target election date has been reported but not formally inserted into the bill text; two plenum readings remain unscheduled. Haredi parties continue to favor September, with intra-coalition friction capable of delaying final passage past the July 15 <span class="cite">F6</span> horizon. The June 2 first-reading vote (106-0, with opposition participation) confirms the dissolution process remains on a consensual track rather than a confidence-crisis trajectory. &rarr; supports <span class="cite">F6</span> without move; supports <span class="cite">F7</span> weekly cadence</p>"""

INSIDE_IRAN = """      <p>Iranian state media on June 10&ndash;11 ran a unified framing across IRNA, Tasnim, and Fars. The IRGC&rsquo;s strikes on US bases in Bahrain, Kuwait, and Jordan were presented as a &ldquo;punitive operation&rdquo; in direct response to US &ldquo;violations&rdquo; of the April ceasefire, with Tasnim publishing the IRGC&rsquo;s full statement naming each targeted facility. Press TV framed the June 11 ballistic missile salvo at Al-Azraq as a demonstration of Iran&rsquo;s capacity to reach deep into the region, with IRGC commanders quoted warning that &ldquo;any vessel cooperating with the enemy&rdquo; in the Strait will be treated as a military target. The near-identical language across all three outlets is consistent with a coordinated top-level messaging decision, not a field-commander statement. &rarr; <span class="context-only">context only</span></p>
      <p>The Hormuz closure re-declaration received the same coordinated amplification pattern observed in the March 2 original. Euronews noted in April that the IRGC &ldquo;appears to now shape Iran&rsquo;s decisions&rdquo; on the strait; the June 10&ndash;11 communications pattern &mdash; with the Foreign Ministry absent from the closure narrative and the IRGC carrying the communication autonomously &mdash; is consistent with that structural observation. Araghchi and the MFA issued no statement on the closure, and no MFA language appeared on the IRGC&rsquo;s targeting of Al-Azraq or the vessel-attack warning. &rarr; supports <span class="cite">F5</span> without move; <span class="context-only">context only</span> for <span class="cite">F8</span></p>
      <p>On the diplomatic side, Tasnim published no language rescinding the June 1 suspension of mediated talks and no readout of a Witkoff&ndash;Araghchi contact. The Qatari delegation visit on June 10 received minimal IRNA coverage &mdash; &ldquo;bilateral discussions&rdquo; &mdash; with no indication that ceasefire or nuclear negotiation topics were formally tabled as a convened session. State media framing of the broader conflict remains built around &ldquo;resistance&rdquo; language and the precondition that Israeli operations in Lebanon and Gaza cease before any diplomatic re-engagement, a precondition Israel has publicly rejected. &rarr; supports <span class="cite">F1</span>, <span class="cite">F2</span> without move</p>"""

SCN = {"esc": 62, "prot": 28, "desc": 10}
ESC_S = ('Active bilateral exchange confirmed (<span class="cite">F3</span> YES); Hormuz formally closed at near-zero transits '
         '(<span class="cite">F4</span> 5%); diplomacy suspended with five days to <span class="cite">F1</span> horizon; '
         'IRGC autonomous messaging without MFA moderation. Military tempo shows no deceleration within current indicators.')
PROT_S = ('Neither side has achieved decisive military objectives; US and Iranian strike exchanges remain within '
          'a calibrated threshold (bases, not capitals); backchannel Qatar/Pakistan contacts continue, preserving '
          'a latent de-escalation architecture. MCM operations partially established '
          '(<span class="cite">F5</span> PARTIAL) and could resume under a freeze.')
DESC_S = ('Requires a ceasefire offer accepted by both sides, IRGC closure lifted '
          '(<span class="cite">F8</span> 22% within 14 days), and Iran rescinding June 1 suspension '
          '(<span class="cite">F1</span> 10%). All three conditions in conjunction sit well below 10%; '
          '10% reflects tail probability of a surprise backchannel breakthrough not captured in current indicators.')

REGIME = {
    "last": "2026-05-11", "next": "2026-06-14",
    "iran_range": "20&ndash;30%",
    "iran_drivers": ("Mojtaba Khamenei consolidated as supreme leader post-28-Feb, governing via written "
        "intermediaries; Rubio on 2026-06-02 described him as alive and increasingly engaging, with a "
        "2026-06-04 written statement asserting control, showing continuity rather than imminent rupture "
        "despite sustained US/Israeli strikes. IRGC autonomous communications pattern on June 10-11 "
        "consistent with IRGC-dominant governance, not a regime-change signal. Range held; next review 2026-06-14."),
    "net_range": "40&ndash;50%",
    "net_drivers": ("Dissolution bill on consensual track: June 2 first reading 106-0 including opposition, "
        "informal Oct 20 target consensus. June 10-11 military escalation may consolidate war-cabinet support "
        "short-term. UTJ formal-status question to be assessed at Sunday 2026-06-14 review. Range held."),
}

SOURCES = [
    ("TIER1", "CNN", "2026-06-07", "https://www.cnn.com/2026/06/07/world/live-news/iran-war-trump-israel-lebanon", "June 7-8 worst Israel-Iran direct strikes in months"),
    ("TIER1", "Al Jazeera", "2026-06-10", "https://www.aljazeera.com/news/2026/6/10/iran-strikes-bahrain-and-jordan-in-retaliation-for-us-attacks-in-hormuz", "Iran attacks Bahrain, Kuwait, Jordan in retaliation for US strikes"),
    ("TIER1", "Al Jazeera", "2026-06-10", "https://www.aljazeera.com/news/2026/6/10/us-bombs-iran-after-trump-threat-tehran-closes-hormuz-strait-to-all-ships", "Tehran closes Hormuz Strait to all ships after US strikes"),
    ("TIER1", "Times of Israel", "2026-06-11", "https://www.timesofisrael.com/liveblog-june-11-2026/", "US launches new self-defense strikes in Iran; Hegseth: Key facilities will be bombed"),
    ("TIER1", "CBS News", "2026-06-08", "https://www.cbsnews.com/live-updates/iran-us-war-israel-hezbollah-fighting-ceasefire-efforts/", "Israel and Iran trade strikes on war's 100th day"),
    ("TIER1", "CNBC", "2026-06-01", "https://www.cnbc.com/2026/06/01/iran-us-negotiations-strait-of-hormuz.html", "Iran stops negotiations with US, vows to completely block Strait of Hormuz"),
    ("TIER1", "CNN", "2026-06-01", "https://www.cnn.com/2026/06/01/world/live-news/iran-trump-lebanon-war-news", "Trump insists talks continue after Iran suspended negotiations"),
    ("TIER1", "Al Jazeera", "2026-06-03", "https://www.aljazeera.com/news/liveblog/2026/6/3/iran-war-live-us-strikes-irans-qeshm-says-tehran-attacks-kuwait-bahrain", "Araghchi: no progress on negotiations with the US"),
    ("TIER1", "Euronews", "2026-06-08", "https://www.euronews.com/2026/06/08/irgc-threatens-regional-energy-assets-as-iran-trades-strikes-with-israel", "IRGC threatens regional energy assets as Iran trades strikes with Israel"),
    ("TIER1", "ABC News", "2026-06-10", "https://abcnews.com/International/live-updates/iran-live-updates/?id=133674243", "CENTCOM: latest round of US strikes on Iran completed"),
    ("STATE_MEDIA", "IRNA/Euronews", "2026-06-01", "https://www.euronews.com/2026/06/01/tehran-suspended-negotiations-via-mediators-with-us-iranian-media-says", "Iran suspended negotiations via mediators with US"),
    ("TIER1", "Tribune India/IRGC", "2026-06-10", "https://www.tribuneindia.com/news/bandar-abbas/strait-of-hormuz-closed-to-all-vessels-says-irans-irgc-amid-escalating-tensions", "Strait of Hormuz closed to all vessels, says Iran's IRGC"),
    ("TIER1", "Jerusalem Post", "2026-06-02", "https://www.jpost.com/israel-news/politics-and-diplomacy/article-898048", "Knesset dissolution bill passes first reading 106-0"),
    ("OSINT", "Statista/PortWatch", "2026-06-07", "https://www.statista.com/chart/35984/ship-traffic-in-the-strait-of-hormuz/", "Ship traffic in Strait of Hormuz has virtually stopped: 2 transits vs 94 pre-war"),
    ("TIER1", "CENTCOM", "2026-04-11", "https://www.centcom.mil/MEDIA/PRESS-RELEASES/Press-Release-View/Article/4457220/us-forces-start-mine-clearance-mission-in-strait-of-hormuz/", "U.S. Forces Start Mine Clearance Mission in Strait of Hormuz"),
]
src_html = "\n".join(
    '      <li>\n        <span class="source-tier tier-%s">%s</span>\n        <a href="%s" target="_blank">%s (%s)</a>\n        &mdash; %s\n      </li>' % (t, t, url, esc(outlet), d, esc(title))
    for (t, outlet, d, url, title) in SOURCES
)

EXPERT_SUMMARY = "no quotes today"
expert_html = '<p class="expert-empty">No expert citations in today\'s Delta.</p>'

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
