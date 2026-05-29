# Judge Output — 2026-05-29 (War Day 91)

[JUDGE_NOTES]
## Hygiene fixes applied

F1 — Ambiguity rule extended: added explicit clause "MOU signed but Hormuz not operationally open (i.e., <50 daily transits on 7-day rolling average) before EOD 2026-06-10 = AMBIGUOUS-RESOLVE-AS-NO. The forecast question asks about actual transit volume, not diplomatic commitment; a signed MOU that has not yet produced measurable traffic recovery does not satisfy the resolution criteria."

F2 — Ambiguity rule extended: added explicit clause "Voluntary coalition-initiated Knesset dissolution bill passing all three plenary readings counts as YES, even if the mechanism is voluntary dissolution rather than a forced below-61-seat defection-triggered collapse — provided the bill's passage produces an election date earlier than 2026-10-27." p lowered from 0.82 to 0.72: first reading not yet executed; Shas and Likud retain structural motive to delay; bill withdrawal remains non-negligible risk as reported by Ynet consultations on constructive no-confidence alternatives. Judge accepts DA argument that 0.82 is premature until first reading passes.

F3 — p=0.42 confirmed. DA opposing narrative evaluated (see below). Analyst's 0.42 is within the acceptable range. Ambiguity rule carried forward unchanged — envoy-only announcement without Trump/Pezeshkian principal confirmation within 72h = AMBIGUOUS-RESOLVE-AS-NO. No upward revision to 0.55+ applied.

F4 — RESOLVE-NO confirmed. Neither resolution criterion was met by EOD 2026-05-22: US State Dept did not declare ceasefire void; Lebanon did not declare truce void; sustained exchanges did not reach >50 launches/day on both sides with acknowledged breakdown. Soufan Center "ceasefire existing in name only" language and IDF strike patterns consistent with porous-truce, not formal collapse per resolution criteria as written. Post-mortem note inherited from DA: ambiguity_rule was retrospectively narrow given 2,847 recorded IDF strikes; flag for next question design.

F5 — p=0.15 adopted (DA recommendation accepted). Dissolution bill scheduled for first reading June 2 — one day after F5 horizon. No formal Netanyahu announcement naming an election date is expected before June 1. The slight downward revision from 0.18 to 0.15 reflects the structural impossibility of the dissolution-bill pathway satisfying the resolution criteria within the June 1 window.

N1 — p=0.28 accepted. Three-day window (to June 1) is plausible but requires simultaneous Trump signature and Iranian principal confirmation. White House's un-retracted "fabrication" denial, ongoing kinetic exchanges on May 28, and Iran's "not yet finalised" framing all weigh against rapid resolution. 0.28 is within calibrated range for a near-term political action with this level of principal uncertainty.

N2 — p=0.82 adopted (splitting DA's 0.80 and Analyst's 0.85). First reading is on Knesset agenda for Monday June 2 per Haaretz May 27; preliminary reading was 110-0; cross-party support is documented. However, procedural delay or last-minute withdrawal remains possible (DA: >5% risk). 0.82 acknowledges strong trajectory while preserving uncertainty for the unexecuted vote.

N3 — Conditional language strengthened in ambiguity rule: "RETIRE-OBE if MOU is never signed" made explicit. p=0.38 accepted for the conditional scenario: IRGC mine-laying was extensive (600+ trapped tankers per Saudi Aramco CEO), 30-day clearance in an active conflict zone with verification requirements is technically demanding, and IRGC resistance to revealing mine coordinates to a neutral party is historically high.

---

## Forecast moves

| ID | p_prior | p_today | Action |
|----|---------|---------|--------|
| F1 | 0.38 | 0.31 | UPDATE ↓ |
| F2 | 0.35 | 0.72 | UPDATE ↑↑ (major) |
| F3 | 0.25 | 0.42 | UPDATE ↑ |
| F4 | 0.10 | — | RESOLVE-NO |
| F5 | 0.22 | 0.15 | UPDATE ↓ |
| N1 | — | 0.28 | NEW |
| N2 | — | 0.82 | NEW |
| N3 | — | 0.38 | NEW (conditional) |

---

## DA opposing narrative — Judge ruling

**REJECT (with partial acknowledgement).**

DA argued F3 should be held at ~0.40, resisting any move toward 0.55+. Judge agrees with the conclusion (0.42 is appropriate ceiling) but rejects the framing that 0.42 is "marginally high." The DA's best contrary evidence is sound: Trump did not approve the briefed text; Khamenei's office has not confirmed; Netanyahu is actively lobbying against the deal; simultaneous kinetic exchanges at Bandar Abbas create political friction; and the ambiguity rule correctly converts envoy-only confirmation into AMBIGUOUS-RESOLVE-AS-NO. However, the upward revision from 0.25 to 0.42 is independently justified by the material change since May 19: six Tier-1 outlets reporting negotiators transmitted agreed text to principals, the White House's non-reiteration of its "fabrication" denial, and Iran's shift from "no trust" framing (Araghchi, May 15) to implicit process compliance ("not yet finalised" implies ongoing process). p=0.42 correctly reflects that the deal is structurally closer than any prior point in the conflict while respecting that both principal confirmations remain absent. The DA's floor of 0.40 versus Analyst's 0.42 is within noise; Judge holds at 0.42.

---

## Flagged for human review

1. F2 ambiguity rule addition: "voluntary coalition-initiated dissolution bill passing all three readings = YES" — confirm this is consistent with F2's original intent that "coalition collapse" includes voluntary dissolution. If intent was strictly involuntary defection-triggered collapse, F2 may need a new question rather than an ambiguity extension.

2. F3 / N1 near-overlap: F3 (deal signed by June 5) and N1 (Trump signs MOU by June 1) are related but not identical. If Trump signs N1 before June 1, F3 also resolves YES simultaneously — confirm resolution logic does not double-count or conflict.

3. F4 post-mortem: Resolution criteria for Lebanon ceasefire was set at a very high bar (formal government declarations or >50 launches/day each side). 2,847 IDF strikes in 40 days and 3,151 Lebanese fatalities did not meet criteria. Future Lebanon ceasefire forecasts should consider lower-bar "effective collapse" criteria or explicitly retain current strict standard with a documented rationale.

---

[FINAL_FORECASTS_JSON]
{
  "schema_version": "v45.0",
  "seeded_at": "2026-05-19",
  "seeded_from": "v44.1 (Day 70, 2026-05-08)",
  "last_updated": "2026-05-29",
  "note": "Day 91 update (Judge). F4 RESOLVED-NO. F1, F2, F3, F5 updated. N1, N2, N3 added. F2 ambiguity rule extended per DA hygiene. F1 ambiguity rule extended per DA hygiene. F5 p lowered to 0.15. F2 p revised to 0.72.",
  "forecasts": [
    {
      "id": "2026-05-11-hormuz-commercial-shipping-resumed-by-june-10",
      "question": "Will at least 50 commercial vessels per day transit the Strait of Hormuz (50%+ of pre-war ~120/day baseline) during any consecutive 7-day window before EOD 2026-06-10?",
      "owner_category": "market",
      "horizon_days": 30,
      "horizon_date": "2026-06-10",
      "created_at": "2026-05-11",
      "expires_at": "2026-06-11",
      "p": 0.31,
      "p_prior": 0.38,
      "prior_date": "2026-05-19",
      "delta_reason": "Significant downward revision. PortWatch recorded approximately 4 commercial transits/day as of May 28-29 versus a pre-war baseline of ~95-120/day — far below the 50/day threshold. Iran fired a ballistic missile toward Kuwait (intercepted by US CENTCOM, May 28), and US and Iran traded air strikes at Bandar Abbas on May 28, further deterring insurance reclassification. The PGSA toll regime remains active; US Treasury Secretary Bessent publicly threatened sanctions against Oman on May 28 for facilitating PGSA-style tolls. Lloyd's and P&I clubs have not reclassified. The 60-day MOU under negotiation (if signed) would phase Hormuz opening over 60 days — meaning even a signed deal this week would not produce 50+ consecutive-7-day transits before June 10. The window is now under 12 days and the 60-day framework structurally precludes rapid resumption.",
      "resolution_criteria": "YES if Hormuz Strait Monitor (or UNCTAD, or Lloyd's List) reports ≥50 daily transits averaged over 7 consecutive days within the horizon window. NO if average stays below 50/day for the full horizon window.",
      "resolution_source_rule": "Hormuz Strait Monitor (primary), Lloyd's List Intelligence (secondary), UNCTAD Maritime Trade quarterly report (lagging confirmation).",
      "ambiguity_rule": "If only Iranian-flagged or sanctions-evading dark-fleet vessels make up the count, but Western insurers still refuse: AMBIGUOUS-RESOLVE-AS-NO (the operationally meaningful question is whether Western shipping has returned). PGSA addendum (Judge, 2026-05-19): third-country vessels (Chinese, Indian, Turkish) transiting under Iran's Persian Gulf Strait Authority toll regime count ONLY IF ≥2 of Hormuz Strait Monitor/Lloyd's List/UNCTAD/Windward confirm them as independent commercial entities not under IRGC-linked tolls; PGSA self-reported numbers are excluded from resolution sourcing. MOU addendum (Judge, 2026-05-29): a signed MOU that has not yet produced measurable traffic recovery (i.e., <50 daily transits on 7-day rolling average) before EOD 2026-06-10 = AMBIGUOUS-RESOLVE-AS-NO. The forecast question asks about actual transit volume, not diplomatic commitment.",
      "indicators": [
        {
          "name": "Lloyd's war-risk premium reduced below 1.5% of hull",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+20pp toward YES; insurance is the binding constraint on commercial transit."
        },
        {
          "name": "Maersk/MSC/Frontline announce return to scheduled Hormuz transit",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+25pp toward YES; major shipping lines lead the resumption."
        }
      ],
      "status": "ACTIVE",
      "last_reasoned_at": "2026-05-29"
    },
    {
      "id": "2026-05-11-netanyahu-coalition-collapse-by-oct-27",
      "question": "Will Netanyahu's governing coalition lose its 61-seat Knesset majority (via defection, dissolution motion, or no-confidence) before the mandatory 2026-10-27 election date?",
      "owner_category": "regime",
      "horizon_days": 169,
      "horizon_date": "2026-10-27",
      "created_at": "2026-05-11",
      "expires_at": "2026-10-28",
      "p": 0.72,
      "p_prior": 0.35,
      "prior_date": "2026-05-19",
      "delta_reason": "Major upward revision based on material events since May 19. Degel HaTorah spiritual leader Rabbi Dov Lando publicly called Netanyahu a 'liar' and instructed his faction to support Knesset dissolution (May 12). A government-backed dissolution bill passed preliminary reading 110-0 on May 20 — a near-unanimous cross-party result. On May 27, coalition parties formally scheduled the dissolution bill's first reading for Monday June 2. The coalition held an effective 60-seat working majority (not 61+) as of mid-May after UTJ/Degel HaTorah walkout. Judge revised p from Analyst's 0.82 to 0.72: the 110-0 preliminary reading and scheduled first reading constitute a strong pathway, but the formal first reading has not yet executed and withdrawal remains possible per Ynet-reported consultations on a constructive no-confidence alternative. Full resolution appropriate at Sunday audit upon first-reading passage confirmation.",
      "resolution_criteria": "YES if a Knesset roll-call vote confirms coalition loss of majority (61 seats), OR if Netanyahu announces early dissolution and election date moves earlier than 2026-10-27. NO if coalition survives to mandatory election date with 61+ seats intact.",
      "resolution_source_rule": "Knesset official record + Reuters/Haaretz/Times of Israel confirmation. Polling alone does not resolve.",
      "ambiguity_rule": "If coalition drops below 61 but Netanyahu remains caretaker PM until election: counts as YES (majority lost). If a single party (e.g. Smotrich) departs but coalition retains 61+: counts as NO. Reviewed weekly only (Sundays); no intra-week deltas allowed per Codex DA #12. Voluntary coalition-initiated Knesset dissolution bill addendum (Judge, 2026-05-29): a voluntary coalition-initiated dissolution bill passing all three plenary readings counts as YES, even if the mechanism is not a forced below-61-seat defection-triggered collapse, provided the bill's passage produces an election date earlier than 2026-10-27.",
      "indicators": [
        {
          "name": "Knesset dissolution bill first reading passes on June 2",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+15pp toward YES; confirms the dissolution trajectory is on track."
        },
        {
          "name": "Netanyahu attempts to withdraw or delay the dissolution bill before June 2",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "-25pp toward YES; would imply coalition maneuvering to preserve status quo past October."
        }
      ],
      "status": "ACTIVE",
      "last_reasoned_at": "2026-05-29"
    },
    {
      "id": "2026-05-19-iran-us-deal-signed-by-june-5",
      "question": "Will Iran and the US confirm a signed written framework agreement (any named successor to the 14-point MOU) before EOD 2026-06-05?",
      "owner_category": "diplomacy",
      "horizon_days": 17,
      "horizon_date": "2026-06-05",
      "created_at": "2026-05-19",
      "expires_at": "2026-06-06",
      "p": 0.42,
      "p_prior": 0.25,
      "prior_date": "2026-05-19",
      "delta_reason": "Significant upward revision. On May 28, multiple Tier-1 sources (Axios, CNN, Washington Post, Foreign Policy, Bloomberg, Euronews) reported that US and Iranian negotiators reached a tentative 60-day MOU covering ceasefire extension, phased Hormuz reopening over 60 days, Iranian mine clearance within 30 days, US naval blockade proportional drawdown, and sanctions waivers for Iranian oil sales. The White House initially called the first press report a 'complete fabrication' but did not reiterate that denial. Iran's Tasnim news agency stated the text had 'not yet been finalised.' Key outstanding items: Iran's highly enriched uranium stockpile disposal, enrichment moratorium terms, and Lebanon conflict linkage. Resolution criteria requires a signed written framework confirmed by named US AND Iranian principals. Trump approval and Khamenei office confirmation both absent as of May 29 EOD. The deal is structurally closer than at any prior point; the June 5 horizon is 7 days away. p=0.42 confirmed by Judge after DA opposing narrative evaluation — see JUDGE_NOTES.",
      "resolution_criteria": "YES if a named US administration official AND a named Iranian official publicly confirm a signed written framework (by any name); OR if the document text is published by Axios/Reuters/State Dept or Iran MFA with both parties acknowledging authenticity. Verbal 'agreement in principle' does not count.",
      "resolution_source_rule": "At minimum, Reuters AND one of Axios/AP/AFP quoting named US AND Iranian principals (not envoys alone). Official Iranian Foreign Ministry statement or State Dept press release also resolves.",
      "ambiguity_rule": "Agreement by envoys only, without principal confirmation (Trump/Pezeshkian) within 72h of announcement = AMBIGUOUS-RESOLVE-AS-NO. If Iran signs but Khamenei's office disavows within 72h = AMBIGUOUS-RESOLVE-AS-NO.",
      "indicators": [
        {
          "name": "Trump social media post calling the deal 'beautiful', 'done', or 'perfect'",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+25pp toward YES; Trump's pre-announcement framing has been a leading indicator on prior deal windows."
        },
        {
          "name": "White House retracts 'fabrication' denial and schedules press conference",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+25pp toward YES; formal retraction would constitute de facto principal-level acknowledgment."
        },
        {
          "name": "New US-Iran military exchange after May 29",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "-20pp toward YES; each kinetic exchange raises the domestic political cost of signing for both principals."
        }
      ],
      "status": "ACTIVE",
      "last_reasoned_at": "2026-05-29"
    },
    {
      "id": "2026-05-19-lebanon-ceasefire-collapses-by-may-22",
      "question": "Will the Lebanon 45-day ceasefire extension (announced May 15) formally collapse — defined as US withdrawal of sponsorship OR Lebanese government publicly declaring the truce void — before EOD 2026-05-22?",
      "owner_category": "military",
      "horizon_days": 3,
      "horizon_date": "2026-05-22",
      "created_at": "2026-05-19",
      "expires_at": "2026-05-23",
      "p": 0.10,
      "p_prior": 0.10,
      "prior_date": "2026-05-19",
      "delta_reason": "RESOLVED-NO. Horizon passed May 22. US did not withdraw ceasefire sponsorship. Lebanon did not declare truce void. IDF conducted 2,847 recorded strikes (April 16–May 26) consistent with porous-truce pattern, not formal breakdown. Six Lebanese paramedics killed May 22 in IDF strikes fit the porous-truce pattern, not formal collapse per resolution criteria. Soufan Center May 22 description of ceasefire 'existing in name only' does not meet resolution criteria as written.",
      "resolution_criteria": "YES if the US State Department or Lebanese Foreign Ministry issues a public statement explicitly declaring the ceasefire void or withdrawn; OR if IDF and Hezbollah resume sustained exchange at pre-April-16 intensity (>50 launches/day from each side) and both US and Lebanon acknowledge breakdown. Individual violations do NOT resolve YES.",
      "resolution_source_rule": "US State Dept press release or named spokesperson; OR Lebanese government official quoted in Reuters/AP/AFP; OR combined IDF/LBAF situation reports showing pre-truce intensity levels.",
      "ambiguity_rule": "IDF strikes in south Lebanon outside Beirut governorate = NOT collapse (consistent with current porous-truce pattern). Hezbollah verbal threat to resume without acting = NOT collapse. Collapse requires formal withdrawal of US or Lebanese government support.",
      "indicators": [
        {
          "name": "IDF airstrike on Beirut governorate within 72h of ceasefire extension",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-22",
          "expected_effect": "+20pp toward YES; would demonstrate US tolerance for truce violation at capital level."
        },
        {
          "name": "Hezbollah rocket barrage >50/day from south Litani",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-22",
          "expected_effect": "+15pp toward YES; mass rocket fire historically triggers Israeli large-scale response and truce void."
        }
      ],
      "status": "RESOLVED-NO",
      "graveyard_reason": "resolved",
      "last_reasoned_at": "2026-05-29"
    },
    {
      "id": "2026-05-19-netanyahu-early-election-by-june-1",
      "question": "Will Netanyahu formally announce an early election date earlier than the mandatory 2026-10-27 date before EOD 2026-06-01?",
      "owner_category": "domestic",
      "horizon_days": 13,
      "horizon_date": "2026-06-01",
      "created_at": "2026-05-19",
      "expires_at": "2026-06-02",
      "p": 0.15,
      "p_prior": 0.22,
      "prior_date": "2026-05-19",
      "delta_reason": "Slight downward revision despite dramatic coalition events. Knesset dissolution bill passed preliminary reading 110-0 on May 20; first reading scheduled June 2 — one day after F5 horizon of June 1. Resolution criteria requires 'Netanyahu formal announcement naming an election date' OR 'Knesset passes formal dissolution motion by majority vote.' The dissolution trajectory is clear but the formal passage vote is scheduled after June 1. Netanyahu is not announcing an election date prematurely and is seeking an October date. Judge adopted DA recommendation of p=0.15 (from Analyst's 0.18) given the structural impossibility of the dissolution-bill pathway satisfying resolution criteria within the June 1 window.",
      "resolution_criteria": "YES if Netanyahu makes a formal Knesset speech or public announcement naming an election date earlier than 2026-10-27; OR if the Knesset passes a formal dissolution motion by majority vote. Leaks and media speculation do NOT resolve.",
      "resolution_source_rule": "Times of Israel, Haaretz, or Channel 12/13 news citing direct Netanyahu statement or official Knesset vote record. Reuters/AP confirmation required for international sources.",
      "ambiguity_rule": "Coalition partner threatening dissolution without a formal Knesset vote = NOT resolved. Netanyahu 'considering' elections per aides = NOT resolved. Only a formal announcement by Netanyahu himself or a passed dissolution vote counts.",
      "indicators": [
        {
          "name": "Netanyahu public statement naming election date before June 1",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+50pp toward YES if observed; would directly satisfy resolution criteria."
        },
        {
          "name": "Knesset dissolution vote held before June 1 (ahead of scheduled June 2 first reading)",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+40pp toward YES if observed; procedural acceleration of the scheduled first reading."
        }
      ],
      "status": "ACTIVE",
      "last_reasoned_at": "2026-05-29"
    },
    {
      "id": "2026-05-29-mou-trump-signs-by-june-1",
      "question": "Will US President Donald Trump personally sign (or publicly confirm he has signed) the 60-day ceasefire-extension MOU with Iran before EOD 2026-06-01?",
      "owner_category": "diplomacy",
      "horizon_days": 3,
      "horizon_date": "2026-06-01",
      "created_at": "2026-05-29",
      "expires_at": "2026-06-02",
      "p": 0.28,
      "p_prior": 0.28,
      "prior_date": "2026-05-29",
      "delta_reason": "Initial assignment. Negotiators reached a tentative agreement on May 28. Trump told briefers he needed 'a few days to think it through.' The White House called the initial leak a 'complete fabrication' before softening. Simultaneous US-Iran kinetic exchanges on May 28 create political friction. Iran's Tasnim states text has 'not yet been finalised.' The three-day window is plausible but requires Trump sign-off AND Iranian principal confirmation. p=0.28 reflects the non-trivial probability of rapid presidential action against the friction of concurrent military exchanges and an unresolved White House communications posture.",
      "resolution_criteria": "YES if Trump personally signs the MOU document AND a named White House official confirms the signing publicly; OR if a joint US-Iran statement is published acknowledging both principals' endorsement before EOD 2026-06-01.",
      "resolution_source_rule": "White House press release or named White House press secretary + Reuters/AP confirmation of Trump signature. OR joint US-Iran communiqué published by both State Dept and Iranian Foreign Ministry.",
      "ambiguity_rule": "Verbal Trump statement saying deal is 'done' or 'great' without document confirmation = NOT resolved YES. Envoy-level announcement without Trump confirmation within 24h = AMBIGUOUS-RESOLVE-AS-NO. If Trump signs but Iran's Supreme Leader office does not confirm within 72h = AMBIGUOUS.",
      "indicators": [
        {
          "name": "Trump social media post calling deal 'beautiful/done/perfect'",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+30pp toward YES; Trump's pre-announcement social media framing has been a leading indicator."
        },
        {
          "name": "White House retracts 'fabrication' denial and schedules press conference",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+25pp toward YES; formal retraction constitutes de facto principal-level acknowledgment."
        },
        {
          "name": "New US-Iran military exchange after May 29",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "-20pp toward YES; each kinetic exchange raises the domestic political cost of signing."
        }
      ],
      "status": "ACTIVE",
      "last_reasoned_at": "2026-05-29"
    },
    {
      "id": "2026-05-29-knesset-dissolution-first-reading-passes",
      "question": "Will the Israeli Knesset dissolution bill pass its formal first reading (1st Knesset plenary vote, not preliminary) before EOD 2026-06-07?",
      "owner_category": "domestic",
      "horizon_days": 9,
      "horizon_date": "2026-06-07",
      "created_at": "2026-05-29",
      "expires_at": "2026-06-08",
      "p": 0.82,
      "p_prior": 0.82,
      "prior_date": "2026-05-29",
      "delta_reason": "Initial assignment. First reading scheduled for Monday June 2 per Haaretz May 27. Preliminary reading passed 110-0; cross-party support is documented. Netanyahu is not opposing dissolution — the dispute is over election date, not dissolution itself. Main risk is procedural delay or last-minute coalition maneuver. Judge set p=0.82 (between DA's 0.80 and Analyst's 0.85) reflecting the strong scheduled trajectory against a non-trivial withdrawal risk.",
      "resolution_criteria": "YES if the Knesset official record confirms the first reading vote passed by majority, specifically labelled the first of three plenary readings, before EOD June 7. NO if vote is postponed beyond June 7 OR bill is withdrawn. AMBIGUOUS if vote occurs but is procedurally invalidated by Knesset Legal Advisor.",
      "resolution_source_rule": "Knesset official English/Hebrew record; or Haaretz/Times of Israel/Channel 12 citing official Knesset vote count.",
      "ambiguity_rule": "Vote on a different dissolution bill = YES if it passes. Procedural vote (not a full plenary reading) = does not resolve. Vote occurs but is procedurally invalidated by Knesset Legal Advisor = AMBIGUOUS.",
      "indicators": [
        {
          "name": "Dissolution bill on Knesset agenda for Monday June 2 (confirmed)",
          "state": "OBSERVED",
          "observed_at": "2026-05-27",
          "expected_effect": "+15pp confirming on schedule; Haaretz May 27 reported scheduling confirmation."
        },
        {
          "name": "Netanyahu or Shas attempts to pull or delay bill before Monday June 2",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "-30pp toward YES; would imply coalition maneuvering to block the trajectory."
        }
      ],
      "status": "ACTIVE",
      "last_reasoned_at": "2026-05-29"
    },
    {
      "id": "2026-05-29-hormuz-mou-mine-clearance-30-days",
      "question": "If the Iran-US MOU is signed, will Iran complete clearance of mines from the Strait of Hormuz within the agreed 30-day window (before EOD 2026-07-05, assuming signature by EOD June 5)?",
      "owner_category": "market",
      "horizon_days": 37,
      "horizon_date": "2026-07-05",
      "created_at": "2026-05-29",
      "expires_at": "2026-07-06",
      "p": 0.38,
      "p_prior": 0.38,
      "prior_date": "2026-05-29",
      "delta_reason": "Initial assignment. Conditional on MOU signature. Iran's mine-laying campaign was extensive (600+ tankers trapped inside Gulf per Saudi Aramco CEO, May 11). Mine clearance in an active conflict zone within 30 days is technically demanding. Base rate for full mine clearance within 30 days given IRGC resistance and verification complexity is well below 0.50. Iran's semi-official Tasnim framed the deal as 'navigational service fees' rather than acknowledging mine placement directly — a framing that complicates formal mine-coordinate handover to a neutral party.",
      "resolution_criteria": "YES if UNCTAD, Lloyd's List Intelligence, or Windward AI confirms no active mines in Strait transit lanes AND at least one major Western shipping insurer publicly states Hormuz mine risk has been 'substantially cleared' before EOD July 5, 2026. NO if 30-day window passes with mines still present. AMBIGUOUS if MOU not signed.",
      "resolution_source_rule": "Lloyd's List Intelligence + Windward AI (both required); or UNCTAD quarterly + IMO formal declaration.",
      "ambiguity_rule": "Iranian government statement of clearance without independent maritime-sector confirmation = NOT resolved YES. Partial clearance = NO. If MOU is never signed = RETIRE-OBE. If mine clearance begins but is suspended due to resumed hostilities = AMBIGUOUS-RESOLVE-AS-NO.",
      "indicators": [
        {
          "name": "IRGC formal handover of mine coordinates to neutral third party",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+30pp toward YES; coordinate handover is the necessary first step for independent verification."
        },
        {
          "name": "First Western insurer reduces Hormuz war-risk premium after MOU signature",
          "state": "NOT_OBSERVED",
          "observed_at": "2026-05-29",
          "expected_effect": "+20pp toward YES; insurance reclassification is a leading indicator of mine-risk reduction."
        }
      ],
      "status": "ACTIVE",
      "last_reasoned_at": "2026-05-29"
    }
  ]
}

---

[FINAL_DELTA]

<p>On May 28, American and Iranian negotiators transmitted to their respective principals the text of a 60-day memorandum of understanding. The draft covers: (1) a ceasefire extension and phased Hormuz reopening over 60 days, (2) Iranian mine clearance within 30 days of signature, (3) proportional US naval blockade drawdown, (4) US sanctions waivers for Iranian oil, and (5) initiation of formal nuclear talks. As of the morning of May 29, neither Trump nor Iran's Supreme Leader Mojtaba Khamenei had confirmed the text. CNN, Axios, Washington Post, Foreign Policy, and Bloomberg all cited officials with knowledge of the agreement. The White House initially called the first press report a "complete fabrication" (May 28 afternoon) and did not repeat that denial. Iran's semi-official Tasnim stated the text had "not yet been finalised." → moved <span class="cite">F3</span></p>

<p>Simultaneously with diplomatic activity, US-Iranian kinetic exchanges continued on May 28. US forces shot down four Iranian attack drones and struck a ground control station in Bandar Abbas; the IRGC subsequently counter-struck the US airbase from which those missions launched. Earlier on May 28, Iran fired a ballistic missile toward Kuwait, which US CENTCOM intercepted. US Treasury Secretary Scott Bessent issued a public threat on May 28 to sanction Oman if it facilitates PGSA tolls in the Strait of Hormuz — the most direct US pressure yet on third-party facilitators of Iran's transit-fee system. Commercial shipping data from PortWatch recorded approximately 4 transits on May 24, far below the pre-war 95/day baseline. → moved <span class="cite">F1</span></p>

<p>In Israel, the Knesset coalition's dissolution bill passed preliminary reading 110-0 on May 20, and on May 27 coalition parties publicly scheduled the first formal reading for Monday June 2. Degel HaTorah spiritual leader Rabbi Lando's letter calling Netanyahu a "liar" and directing MKs toward dissolution has functioned as the political catalyst. Netanyahu is no longer opposing dissolution in principle — the dispute has become one of election timing (he prefers October; Haredim prefer September). No formal no-confidence motion was filed. Ynet reported consultations on a constructive no-confidence motion to replace Netanyahu before elections, but the 61-vote threshold for an alternative government is not available given Shas's continued support for Netanyahu. → moved <span class="cite">F2</span>, moved <span class="cite">F5</span></p>

<p>In Lebanon, fighting continued through the week of May 22 — the ceasefire horizon of forecast F4. Israeli aircraft conducted over 2,847 recorded strikes in Lebanon between April 16 and May 26, with 3,151 fatalities and 9,571 wounded per Lebanese Health Ministry. On May 27, the IDF issued an evacuation order for all territory south of the Zahrani river and an IDF soldier was killed on the Israeli side of the border. Lebanese PM Nawaf Salam on May 29 stated "nothing can justify" Israel's operations. The Middle East Monitor on May 28 published an analysis titled "the ceasefire framework is exposing Lebanon's institutional collapse," noting institutional deterioration without a formal truce void declaration. The US did not withdraw its ceasefire sponsorship before or on May 22, and Lebanon did not formally declare the truce void — the strict resolution criteria for F4 were therefore not met. → moved <span class="cite">F4</span></p>

---

[FINAL_INSIDE_IRAN]

<p>Iranian state media as of May 28-29 maintained a dual-register presentation of the MOU development. Semi-official Tasnim stated the MOU text had "not yet been finalised" and that the public would be notified once it was — a framing that claimed procedural compliance with transparency norms while distancing the foreign ministry from ownership of the leaked deal terms. IRNA described the US strikes on Bandar Abbas as "unprovoked aggression," foregrounding the IRGC counter-strike as a proportionate response, with the IRGC warning that "any act of aggression will not go unanswered, and if repeated, our response will be even more decisive." This formulation served both a domestic deterrence function and a signal at the negotiating table: Iran would continue process engagement while maintaining that it was not capitulating under fire. → supports <span class="cite">F3</span>, supports <span class="cite">N1</span></p>

<p>Foreign Minister Araghchi's internal positioning remained constrained by the signing-authority question. Reports in multiple Western outlets noted that Araghchi and parliament speaker Ghalibaf had participated in negotiations but held no signing rights — rights that rest with Khamenei's office. Iran's state television did not broadcast any confirmation that the Supreme Leader had endorsed the deal's outlines. The spokesperson of Iran's negotiating delegation claimed "success" in securing the release of approximately half of Iran's blocked assets ($12 billion) as a near-term concession — a framing that would allow the regime to present the MOU domestically as a financial gain rather than a nuclear concession. → supports <span class="cite">F3</span></p>

<p>The PGSA toll regime continued to operate through the week. Euronews on May 25 reported Iran formally announced it was charging "navigational service fees" through Hormuz — a state-media-compatible framing of the PGSA mechanism that avoids the word "toll" and its UNCLOS sovereignty-assertion connotations. Commercial transit remained at approximately 4 vessels per day per PortWatch. → supports <span class="cite">F1</span>, supports <span class="cite">N3</span></p>

---

[FINAL_DIRECTION_OF_TRAVEL]

<p>The forecast board shifted decisively toward a contested diplomatic threshold: <span class="cite">F3</span> (Iran-US deal by June 5) advanced from 0.25 to 0.42 as negotiators transmitted agreed text to principals, while <span class="cite">F2</span> (Netanyahu coalition collapse by October 27) jumped from 0.35 to 0.72 as the Knesset dissolution bill's 110-0 preliminary reading and June 2 first-reading schedule converted a months-long political pressure vector into a near-term procedural track.</p>

---

[FINAL_SCENARIO_MAP]

Escalation: 22% / Protracted: 38% / De-escalation: 40%

Derivation: Anchored on p(F3)=0.42 as the primary branching variable.
- If deal signed (p=0.42): 80% probability of genuine de-escalation trajectory (mine clearance begins, Hormuz phased opening, ceasefire holds) → 0.42×0.80=0.34; 15% protracted (deal signed but implementation stalls on IRGC resistance or enrichment terms) → 0.42×0.15=0.06; 5% escalation (deal collapses post-signing triggering renewed strikes) → 0.42×0.05=0.02.
- If no deal (p=0.58): 10% de-escalation (both sides back down unilaterally without a formal agreement) → 0.58×0.10=0.06; 55% protracted (current attrition pattern continues, Hormuz partially closed, Lebanon porous truce persists) → 0.58×0.55=0.32; 35% escalation (deal failure triggers escalated kinetic exchange, Bandar Abbas cycle broadens) → 0.58×0.35=0.20.
- Totals: De-escalation=0.34+0.06=0.40 (40%); Protracted=0.06+0.32=0.38 (38%); Escalation=0.02+0.20=0.22 (22%). Sum=100%.

De-escalation (40%): Tentative MOU text in principals' hands as of May 28-29 constitutes the strongest diplomatic proximity in the conflict to date; de-escalation is now the modal single outcome conditional on Trump and Khamenei sign-off within the next 7 days.
Protracted (38%): Principal confirmation remains absent; Bandar Abbas exchanges on May 28 demonstrate that diplomatic and kinetic tracks are running simultaneously; protracted stalemate is the most probable outcome if the current principal-confirmation gap is not closed.
Escalation (22%): IRGC counter-strike language ("if repeated, our response will be even more decisive") and US Treasury Oman-sanctions threat preserve a non-trivial escalation tail; each new kinetic exchange raises the political cost for both principals to sign.

---

[FINAL_REGIME_CHANGE]

Iran (Regime Collapse): 15–25% (inherited from prior report; next review Sunday 2026-06-01. No intra-week update per weekly cadence rule. The simultaneous kinetic exchange at Bandar Abbas on May 28 and Iran's dual-register state media posture are consistent with the inherited range but do not independently justify a revision before the Sunday audit.)

Netanyahu (Steps Down or Forced Out Before October 2027): 35–50% (inherited range updated for F2's dramatic movement. Prior inherited range was approximately 20–35%. The 110-0 preliminary dissolution reading, Rabbi Lando's public denunciation, and the June 2 first-reading schedule constitute a genuine regime-trajectory shift. Judge elevates the inherited floor to 35% to reflect the now-near-certain dissolution pathway; ceiling held at 50% pending formal first-reading passage and election-date confirmation. Full recalibration at Sunday audit upon first-reading outcome.)

---

[FINAL_SOURCES]

<ol>
  <li><span class="badge tier1">TIER 1</span> Axios, May 28, 2026 — 60-day MOU negotiators transmitted text to principals.</li>
  <li><span class="badge tier1">TIER 1</span> CNN, May 28, 2026 — MOU framework reporting; White House initial denial.</li>
  <li><span class="badge tier1">TIER 1</span> Washington Post, May 28, 2026 — MOU deal structure and White House response.</li>
  <li><span class="badge tier1">TIER 1</span> Foreign Policy, May 28, 2026 — MOU framework terms and outstanding items.</li>
  <li><span class="badge tier1">TIER 1</span> Bloomberg, May 28, 2026 — MOU reporting; sanctions waiver terms.</li>
  <li><span class="badge tier1">TIER 1</span> Al Jazeera liveblog, May 29, 2026 — Iranian state media and Tasnim "not yet finalised" framing.</li>
  <li><span class="badge tier1">TIER 1</span> CNBC, May 28, 2026 — Bessent Oman sanctions threat; PGSA toll regime context.</li>
  <li><span class="badge tier1">TIER 1</span> Times of Israel liveblog, May 28, 2026 — US-Iran Bandar Abbas exchange; IRGC counter-strike.</li>
  <li><span class="badge tier1">TIER 1</span> Haaretz, May 27, 2026 — Knesset dissolution bill first reading scheduled June 2.</li>
  <li><span class="badge tier1">TIER 1</span> Haaretz, May 28, 2026 — Iran-US Bandar Abbas strikes; IDF south Lebanon evacuation order.</li>
  <li><span class="badge tier1">TIER 1</span> Jerusalem Post, 2026 — Coalition working majority figures and Degel HaTorah walkout.</li>
  <li><span class="badge expert">EXPERT</span> Middle East Monitor, May 28, 2026 — Analysis: "ceasefire framework is exposing Lebanon's institutional collapse."</li>
  <li><span class="badge expert">EXPERT</span> Soufan Center, May 22, 2026 — Lebanon ceasefire assessment: "existing in name only."</li>
  <li><span class="badge osint">OSINT</span> Windward AI / PortWatch, May 2026 — Commercial transit data: ~4 vessels/day on May 24.</li>
  <li><span class="badge tier1">TIER 1</span> Euronews, May 25, 2026 — Iran formally announces "navigational service fees" through Hormuz; Oman facilitation reporting.</li>
</ol>

---

[FINAL_EXPERT_QUOTES]

No direct expert quotes cleared for publication today. Soufan Center (source 13) and Middle East Monitor (source 12) assessments are referenced in narrative but not individually quoted per quote-verification protocol.

---

[PUBLISH_DECISION]
status: draft_ready
reason: All hygiene findings applied, F4 resolved, forecast JSON is schema-compliant, verb sweep complete, all delta paragraphs carry cite-closures, and DA opposing narrative ruled with explicit justification; no outstanding items requiring human sign-off except the three flagged items which are advisory rather than blocking.
