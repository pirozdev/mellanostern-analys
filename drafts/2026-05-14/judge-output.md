# Judge Output — 2026-05-14 (War Day 76, Thursday)

```
[JUDGE_NOTES]

## Hygiene fixes applied

1. F1: RESOLVED-AMBIGUOUS-AS-NO. Horizon passed (EOD May 13). Unanimous between Source A and Source B. No named Iranian official addressed the US-authored 14-point MOU by name in the qualifying window. Araghchi's May 12 PressTV statement addressed negotiating conduct broadly; no named-framework citation confirmed in dual sources. Ambiguity rule invoked. Status set to RESOLVED-AMBIGUOUS, graveyard_reason = resolved.

2. F2 — Indicator state corrected: "Witkoff/Kushner return to Islamabad" changed from NOT_OBSERVED to CONTRADICTED. The trip was cancelled in late April and has not been rescheduled — this is a confirmed negation, not an absence of observation. p reduced from 0.35 to 0.07 (see Forecast Moves).

3. F2 — Ambiguity rule expanded: added explicit clause "Trump-unilateral announcement without Iranian FM confirmation within 24 hours = NO" to close the scenario gap flagged by Source B.

4. F3 — Resolution criteria expanded: disambiguation note about Iran's own 14-point counter-proposal vs. the US-authored framework is now embedded directly in resolution_criteria JSON, not only in narrative text. Indicator language updated to specify "US framework" throughout.

5. F4 — Indicator state updated: "Hezbollah rocket fire >20/day" changed from NOT_OBSERVED to OBSERVED (IDF reporting >40/day confirmed). Smotrich indicator retained through May 15 resolution window but annotated as less relevant given coalition dissolution bill dynamics.

6. F5 — Indicator state corrected: "MBS-Trump phone call or in-person summit" changed from NOT_OBSERVED to OBSERVED (second call confirmed ~May 7-8, WSJ/Iran International/Defense News). p adjusted to 0.28 (see Forecast Moves and F5 Divergence Resolution).

7. F6 — Baseline mismatch corrected: removed parenthetical reference to "50%+ of pre-war ~120/day" from delta_reason context; retained the 50/day absolute threshold as specified in resolution_criteria. The parenthetical is internally inconsistent (50% of 120 = 60, not 50). p reduced from 0.45 to 0.18 (see Forecast Moves).

8. F7 — Ambiguity rule expanded: added clause covering the dissolution bill scenario — "If dissolution bill passes with 61+ votes and elections are scheduled before Oct 27: AMBIGUOUS — requires adjudication at Sunday review re: whether scheduled dissolution constitutes majority loss." Flagged for mandatory Sunday 2026-05-17 review.

9. N1 (new forecast) — Accepted as written with minor edit: "indicator" renamed to "All four coalition factions present and voting for first reading" for precision. Added to ACTIVE board.

10. N2 (new forecast) — Dropped to OBE. Cap enforcement: analytical content merged into F6's delta_reason. China's named Hormuz commitment is now an explicit pathway note within F6 rather than a standalone 4-day forecast that would push ACTIVE to 8.

11. N3 (new forecast) — Dropped to OBE per both Source A and Source B recommendation. Analytically subsumed by F2; reopen as standalone after F2 resolves.

---

## Forecast moves

F1: p=0.55 → RESOLVED-AMBIGUOUS (AMBIGUOUS-RESOLVE-AS-NO). Horizon passed EOD May 13. Unanimous verdict.

F2: p=0.35 → p=0.07. Diplomatic collapse confirmed across multiple evidence streams (May 10-13). Witkoff/Kushner trip CONTRADICTED. Araghchi at BRICS. Iran 5-conditions posture set. No operational signing mechanism within 5 days.

F3: p=0.20 → p=0.18. Slight downward move consistent with Iran's counter-proposal posture (tactical engagement) rather than formal walk-away. DA hygiene fix applied to resolution_criteria.

F4: p=0.30 → p=0.40. Hezbollah rocket threshold OBSERVED (>40/day). Jiyeh highway strikes (Mount Lebanon governorate) not qualifying, but northward geographic creep raises conditional probability of Beirut governorate strike before EOD May 15. Horizon is tomorrow.

F5: p=0.40 → p=0.28. MBS-Trump call OBSERVED; operational restoration reported. Source-rule structural gap (no named DoD source, no Saudi MOFA statement) remains active and historically persistent. Judge splits between Source A (0.20, over-penalizes operational reality) and Source B (0.55, under-weights source-rule constraint). See F5 divergence section.

F6: p=0.45 → p=0.18. Current transits at 6-12/day vs 50/day threshold. Lloyd's at ~2.5% (above 1.5% indicator). No major shipping line announcement. Xi summit pathway noted in delta_reason but does not immediately move vessel counts. Baseline mismatch corrected.

F7: p=0.35 → p=0.35 (no move; weekly cadence, Thursday). Flagged for mandatory Sunday review given coalition dissolution bill filing.

N1: Created at p=0.72 (ACTIVE). Knesset dissolution bill filed May 13; all factions co-sponsored; first reading expected ~May 20.

N2: OBE at creation. Content merged into F6. See cap note.

N3: OBE at creation. Subsumed by F2. See cap note.

---

## F4 verification result

**VERDICT: NOT CONFIRMED. F4 remains ACTIVE.**

The web research conducted for this calibration session finds the following:

- The UN News article cited by Source B ("Fresh strike on Beirut suburbs — a very alarming development," DS6) dates to **May 7, 2026**, not May 12. It reports the UN's reaction to the **May 6 Haret Hreik strike** (IDF killing of Radwan commander Malek Balout), confirmed by Euronews, Haaretz, CBC, Al Jazeera, and multiple other tier-1 sources as the first Beirut strike since April 8. This is the first ceasefire-period Dahieh strike, occurring before the seed date of this forecast board (May 11).

- The **May 12-13 strikes** are confirmed as targeting the **Jiyeh coastal highway** (~20 km south of Beirut) in Mount Lebanon governorate, killing 8-15 people including two children. Sources: Times of Israel, Al Jazeera, PressTV, Antiwar.com, Daily Sabah, RTÉ, 1News NZ — all consistently describe location as "highway south of Beirut" / Jiyeh / Sidon corridor. None place the strikes within Beirut governorate.

- There is **no confirmed IDF strike on Beirut governorate (Dahieh, Bourj el-Barajneh, Haret Hreik, Hadath, Chiyah) between May 11-14, 2026** in any searched source. The IDF evacuation notices for Bourj el-Barajneh/Hadath/Haret Hreik/Chiyah cited in search results originate from March 2026 and the early May 2026 period around the May 6 strike.

**Source B's F4 critical flag was a false positive**: it conflated the May 7 UN News article (reporting on the May 6 Dahieh strike, which predates F4's creation) with a hypothetical new May 12 strike. Source B's claim that "Source A appears to have analyzed the HIGHWAY STRIKE only and missed a SEPARATE Dahieh-area strike on approximately May 12" is not supported by any sourced evidence.

**Resolution: F4 remains ACTIVE at p=0.40.** The genuine operational escalation (Hezbollah >40 rockets/day OBSERVED, IDF northward geographic creep from south Lebanon through Jiyeh toward Beirut) justifies an upward move from 0.30, but not resolution.

---

## F5 divergence resolution

Source A: p=0.20. Source B: p=0.55 (revised down from 0.72). Judge sets p=**0.28**.

**Reasoning:** The operational evidence is clear — Saudi Arabia and Kuwait restored US access per WSJ, Iran International, and Defense News (May 7-8). The MBS-Trump indicator is OBSERVED. The question for F5 resolution is not whether access was restored operationally but whether a qualifying public confirmation will be issued.

Source A's 0.20 under-weights the operational reality: access was restored 17 days before the horizon, giving multiple opportunities for a public statement to emerge. Source B's 0.55 under-weights Saudi Arabia's documented and historically consistent practice of not publicly confirming US basing arrangements — the same practice was observed for pre-2026 Prince Sultan access periods.

The resolution path requires either (a) Saudi MOFA statement or (b) named DoD source in Reuters/Bloomberg/Times of Israel. The Pentagon's response ("referred questions to White House") is below the threshold for (b). No MOFA statement has been issued in 17 days. Saudi Arabia is structurally averse to on-record confirmation of US military basing — this reflects a domestic political constraint that has persisted across the MBS era. However, the restoration is real and some probability remains that a formal statement is issued in the remaining 11 days. Judge sets 0.28: meaningfully above Source A's 0.20 to acknowledge operational reality and MBS-Trump call, meaningfully below Source B's 0.55 to acknowledge the genuine structural barrier.

---

## DA opposing narrative — Judge ruling per block

**BLOCK 1 (F2, reduce to ~0.06-0.08): ACCEPT**
Judge sets F2 at 0.07, within DA's recommended range. The contrary evidence cited by Source B is real but insufficient to reverse the finding of no operational signing mechanism. Trump's documented pattern of sudden announcements does not overcome the absence of any confirmed channel, Iranian engagement, or bridging mechanism. The Xi summit creates a theoretical pathway but the conditional chain (Xi commitment → Iran engagement → Witkoff contact → written MOU in 5 days) is too long to justify p above 0.10. 0.07 is the Judge's calibration, splitting Source A's 0.08 and DA's 0.06.

**BLOCK 2 (F4, possibly already YES — Source A missed it): REJECT**
Source B's claim is not supported by evidence. The May 12-13 strikes are confirmed as Jiyeh/Mount Lebanon governorate, not Beirut governorate. The UN News article Source B cited as evidence of a May 12 Dahieh strike dates to May 7 and concerns the May 6 strike, which predates this forecast. Source A correctly analyzed the available evidence. F4 is not resolved YES; it remains ACTIVE. Judge notes that Source B performed a useful function by flagging the UN News citation for verification, but the underlying claim was incorrect. The DA's opposing narrative here was wrong on facts, not wrong on method.

**BLOCK 3 (F5, Source A too low at 0.20): PARTIAL ACCEPT**
Source B is correct that 0.20 under-weights operational reality and that the MBS-Trump indicator must be marked OBSERVED. Judge accepts the direction of the correction but not the magnitude: Source B's 0.55 over-corrects by treating operational restoration as nearly equivalent to the formal public confirmation required for YES resolution. Judge sets 0.28 as a calibrated midpoint. The structural public-confirmation gap is real and historically persistent.

**BLOCK 4 (F6, Source A's KEEP at 0.45 is wrong): ACCEPT**
Source A's KEEP at 0.45 is indefensible given current transit data (6-12/day vs 50/day threshold). Source B's 0.18 is the correct order of magnitude. Judge sets 0.18, matching Source B, because: (a) the baseline mismatch was real; (b) current transits are at 10-24% of threshold with no major shipping line announcement; (c) Lloyd's at 2.5% provides no near-term insurance signal; (d) while the Xi summit creates a pathway, a complete YES resolution by June 10 requires a near-linear chain of events from Chinese commitment through Iranian compliance through Lloyd's re-rating through major-carrier announcement — each conditional step reduces probability multiplicatively.

---

## New forecasts — trim decision

**N1 (Knesset dissolution vote by May 28): ACCEPTED at p=0.72**
Fills a genuine gap on the board. F7 tracks coalition majority loss; N1 tracks the specific procedural vote. These are distinct questions that can resolve differently (N1 YES + F7 ambiguous is a live scenario). 14-day horizon is appropriate.

**N2 (China-Iran Hormuz commitment by May 18): DROPPED → OBE**
Cap enforcement. Analytical content merged into F6 delta_reason. The question is a 4-day sub-question of F6's most important near-term pathway and does not justify a standalone board slot. Reopen after cap clears if summit produces an unexpected named commitment.

**N3 (US-Iran talks resume channel by May 21): DROPPED → OBE**
Both sources agreed this was the lowest-priority new forecast. Partially subsumed by F2. Reopen as standalone if F2 resolves NO and the diplomatic track requires a dedicated channel-formation tracker for the period May 18-21.

**Cap status after trim: 7 ACTIVE forecasts.** Exactly at limit.
F2 (diplomacy) + F3 (diplomacy) + F4 (military) + F5 (diplomacy) + F6 (market) + F7 (regime) + N1 (regime)

---

## Flagged for human review

1. **F4 horizon EOD May 15**: Judge must verify tomorrow whether any IDF strike hits Beirut governorate before EOD May 15. The horizon expires tomorrow; resolution or continued ACTIVE status requires same-day check on May 15.

2. **F7 Sunday review (2026-05-17)**: Coalition dissolution bill dynamics have materially changed the question structure. The specific adjudication required: if N1 (dissolution bill preliminary vote) passes before Oct 27, does that resolve F7 YES (election moved earlier) or NO (scheduled dissolution ≠ majority loss)? This requires careful reading of F7 resolution_criteria — current text says YES if "Netanyahu announces early dissolution and election date moves earlier than 2026-10-27," which would cover this scenario as YES. But the ambiguity rule addition flagged for Sunday review notes this needs adjudication.

3. **F2/F3 logical coherence**: With F2 at 0.07 and F3 at 0.18, the implied P(limbo — neither memo signed nor formal rejection) = 0.75. This is now coherent with the deadlock reality (DA's original tension flag applied to the old p=0.35 seed).

4. **N2 and N3 for rapid reinstatement**: If Trump-Xi summit produces an unexpected named Hormuz commitment on May 14-15, N2 should be reinstated immediately at p=0.75+ and F6 moved sharply upward. Monitor summit conclusion statement.

[FINAL_FORECASTS_JSON]

See /home/user/mellanostern-analys/drafts/2026-05-14/forecasts-updated.json

Active forecast summary (7 ACTIVE):
- F2: 2026-05-11-us-iran-memo-signed-by-may-18 → p=0.07
- F3: 2026-05-11-iran-formally-rejects-by-may-18 → p=0.18
- F4: 2026-05-11-second-beirut-strike-by-may-15 → p=0.40
- F5: 2026-05-11-saudi-airspace-restored-by-may-25 → p=0.28
- F6: 2026-05-11-hormuz-commercial-shipping-resumed-by-june-10 → p=0.18
- F7: 2026-05-11-netanyahu-coalition-collapse-by-oct-27 → p=0.35
- N1: 2026-05-14-knesset-dissolution-vote-passes-by-may-28 → p=0.72

[FINAL_DELTA]

<p>The US-Iran negotiating track entered acute collapse between May 10 and May 13 as Trump characterised Iran's counter-proposal as "a piece of garbage" and declared the ceasefire "on life support." Iran responded through two distinct registers: Pezeshkian's "we will never bow" defiance framing on May 11 and Araghchi's procedural "US approach is the main obstacle" formulation delivered in a bilateral session with Norway's Deputy FM on May 12. Neither statement named the US-authored 14-point framework by title or addressed its specific terms, keeping Iran inside a posture of principled non-engagement rather than explicit rejection. → supports <span class="cite">F3</span> without move</p>

<p>Iran's foreign minister travelled to the BRICS foreign ministers' meeting in New Delhi on May 13-14, demonstrating Tehran's refusal to treat the collapsed Pakistan channel as the only available diplomatic arena. Araghchi's presence at the BRICS format — where he engaged with Jaishankar and other multilateral counterparts — signals diplomatic bandwidth redirected to frameworks where Iran holds a stronger structural position than in bilateral US-mediated channels. The Witkoff-Kushner Islamabad trip has been cancelled with no confirmed reschedule; the IRGC Quds Force has issued no statement endorsing the diplomatic track. No operational pathway exists for a signed written memorandum by May 18. → moved <span class="cite">F2</span> (0.35 → 0.07)</p>

<p>The May 12-13 Jiyeh coastal highway strikes — three IDF drone attacks targeting vehicles approximately 20 kilometres south of Beirut — killed eight to fifteen people including two children. All tier-1 sourcing places the strikes within the Jiyeh area of Mount Lebanon governorate rather than Beirut governorate; IDF attributed the attacks to Hezbollah infrastructure interdiction without naming Beirut as a target. Hezbollah rocket fire stands confirmed above 40 per day, crossing the >20/day indicator threshold. The geographic northward creep of IDF operations from southern Lebanon through the Jiyeh corridor raises the conditional probability of a strike within Beirut governorate boundaries before EOD May 15. The forecast's horizon expires tomorrow. → moved <span class="cite">F4</span> (0.30 → 0.40)</p>

<p>Saudi Arabia and Kuwait restored US basing and overflight access to Prince Sultan Air Base following a second Trump-MBS phone call, per WSJ, Iran International, and Defense News reporting around May 7-8. The operational restoration is real; the MBS-Trump indicator is observed. However, the public-confirmation pathway — requiring Saudi MOFA or a named Pentagon spokesperson statement — faces a structural barrier that Saudi Arabia has historically sustained: the Pentagon referred press questions to the White House, and no MOFA statement has been issued in seventeen days since restoration. The YES-resolution path for F5 by May 25 requires an unusual departure from Saudi Arabia's documented basing communication practice. → moved <span class="cite">F5</span> (0.40 → 0.28)</p>

<p>Trump arrived in Beijing on May 13-14 for a summit with Xi Jinping on May 14-15, with Iran's Hormuz closure on the central agenda. China purchases over 80% of Iranian crude and holds the relationship that most directly conditions Iranian economic sustainability, giving Xi leverage he did not anticipate entering 2026. Even if the summit produces Chinese engagement on the Hormuz file, a YES resolution for F6 by June 10 requires a near-linear chain — Chinese commitment, Iranian operational compliance, Lloyd's re-rating below 1.5%, and major shipping line announcements — at a moment when daily transits stand at 6-12 vessels against a 50-vessel threshold. A named Chinese Hormuz commitment would materially shift this probability; no such commitment had been issued as of this report's compilation. → moved <span class="cite">F6</span> (0.45 → 0.18)</p>

<p>The Israeli coalition reached a structural inflection on May 12-13. Degel Hatorah announced departure from the coalition on May 12; the coalition then pulled all Knesset legislation citing lack of majority; Netanyahu's full coalition co-submitted a Knesset dissolution bill on May 13, framing a managed path to September elections. Per Codex DA #12, F7 carries weekly cadence and receives no intra-week probability delta today. The dissolution process creates conditions for an ambiguous interaction between F7 and N1: if the dissolution bill passes preliminary reading before May 28 (p=0.72), elections would occur via scheduled vote rather than coalition collapse, potentially resolving F7 as YES on the amended ambiguity rule (election date moved earlier than Oct 27) or requiring Sunday adjudication. → supports <span class="cite">F7</span> without move | → created <span class="cite">N1</span> (p=0.72)</p>

[FINAL_INSIDE_IRAN]

Iranian state media operated in a tightly coordinated register across May 12-13. PressTV led with Araghchi's Norwegian FM bilateral as the primary diplomatic framing vehicle: the "US approach is the main obstacle" formulation was carried without elaboration of which specific US demands constitute the obstacle, keeping the statement maximally vague while attributing blame to Washington. PressTV simultaneously ran Araghchi's BRICS travel to India as evidence of Iranian diplomatic normality — the foreign minister directing bandwidth toward a multilateral forum rather than sitting in Islamabad waiting for Witkoff signals Tehran's refusal to treat the Pakistan channel as the primary arena of engagement. → supports <span class="cite">F2</span> without move

IRNA and Tasnim amplified Pezeshkian's "never bow" formulation from May 11 through May 13 without pairing it with any named reference to the US 14-point MOU or to Trump's "piece of garbage" characterisation of Iran's counter-proposal. The deliberate omission of Trump's rejection language prevents a frame in which Iran is seen as responding reactively to US escalation; the narrative preferred by state media positions Iran as aggrieved peace initiator versus US as maximalist saboteur. The 30-day gap since Araghchi's April 13 X post — the last instance in which a named Iranian official addressed the specific framework by name — is consistent with a deliberate Iranian policy of maintaining deniability about whether the framework under discussion is identical to the one the US claims to have proposed. → supports <span class="cite">F3</span> without move

Mojtaba Khamenei has not appeared publicly since the war began. State broadcaster reports of "new and decisive directives" for military operations carry deliberate opacity: the absence of a named Mojtaba statement explicitly addressing the 14-point MOU is a calculated choice, not silence of ignorance, serving to preserve IRGC operational freedom while denying adversaries a quotable rejection. → context only

[FINAL_DIRECTION_OF_TRAVEL]

The board's centre of gravity has shifted decisively toward prolonged stalemate: the collapse of the US-Iran diplomatic channel (<span class="cite">F2</span> 0.07) combined with Hormuz transits at 10-24% of threshold (<span class="cite">F6</span> 0.18) suggests the highest-probability near-term path is continued deadlock rather than either rapid de-escalation or escalation to a new military threshold, with the Trump-Xi summit outcome the single variable most capable of altering that trajectory within the current forecast horizon.

[FINAL_SCENARIO_MAP]

Escalation (Esc%): ~24%
Derived from F4 (0.40 strike on Beirut governorate by tomorrow) as the primary near-term military trigger; F6 failure (0.82) sustaining economic-pressure pathway; F3 (0.18) formal Iranian rejection as signal of hardliner ascendancy. Escalation scenario requires at least one of: Beirut governorate strike triggering Hezbollah full-spectrum response, Iranian formal rejection accompanied by IRGC operational shift, or Hormuz complete closure reinforced by IRGC declaration.

Protection/Stalemate (Prot%): ~62%
Dominant scenario. F2 near-zero (0.07), F6 low (0.18), F3 low (0.18) — none of the principal resolution pathways is likely to move within current horizons. Iran remains in counter-proposal posture rather than formal engagement or rejection; Saudi access remains operationally restored but publicly unconfirmed; Hormuz transits at a fraction of threshold. Israeli coalition dissolution (N1 at 0.72) creates internal Israeli political uncertainty that reduces the probability of a major new Israeli military initiative while also reducing Netanyahu's ability to cut a deal.

De-escalation (De-esc%): ~14%
Requires a successful Trump-Xi summit outcome that produces Chinese named pressure on Iran, a subsequent Iranian decision to allow Hormuz partial reopening, and Lloyd's re-rating — a conditional chain each step of which carries its own probability below 0.20. F5 Saudi airspace public confirmation (0.28) is a necessary but insufficient signal of the bilateral alignment that would support this pathway.

[FINAL_REGIME_CHANGE]

Iran political stability range: 15–25% (significant but not dominant probability of meaningful leadership fracture or succession pressure within 12-month horizon; Mojtaba's continued opacity and Pezeshkian's "never bow" framing reflect coordination, not cohesion). Last reviewed: 2026-05-08. Next review: 2026-05-17 (Sunday).

Netanyahu coalition collapse range: 30–45% — see F7. Last reviewed: 2026-05-08. Next Sunday review: 2026-05-17, at which point the dissolution bill procedural status and F7 ambiguity adjudication must be addressed.

[FINAL_SOURCES]

S1: [TIER1] Washington Post — "Trump says Iran ceasefire is on 'life support,' calls latest proposal 'garbage'" May 10, 2026
S2: [STATE_MEDIA] PressTV — "Iran FM: US approach main obstacle to ending war" May 12, 2026
S3: [STATE_MEDIA] PressTV — "Iran demands end to war before nuclear talks as FM Araghchi set to attend India BRICS meeting" May 12, 2026
S4: [TIER1] Times of Israel — "Israeli strikes on highway south of Beirut kill 8, including 2 children" May 13, 2026
S5: [TIER1] Al Jazeera — "At least 15 people killed in Israeli attacks on Lebanon" May 13, 2026
S6: [TIER1] Iran International / WSJ — "Saudi Arabia and Kuwait lift restrictions on US military access to bases, airspace" May 7-8, 2026
S7: [TIER1] Defense News — "Saudi Arabia and Kuwait Lift Restrictions on U.S. Military Access to Bases and Airspace" May 8, 2026
S8: [TIER1] CNBC — "Trump-Xi summit: China's help in Iran may require US concessions" May 12, 2026
S9: [TIER1] Al Jazeera — "Trump-Xi summit live: US, China leaders holding talks on trade, tech, Iran" May 14, 2026
S10: [TIER1] Haaretz — "Top Haredi Leader Orders Coalition Collapse After Netanyahu Freezes Key Bill" May 12, 2026
S11: [TIER1] Times of Israel — "Coalition files bill to dissolve Knesset, doesn't set an election date" May 13, 2026
S12: [TIER1] Newsmax — "Companies Paying Iran Extortion Tolls for Transit Again" May 12, 2026
S13: [TIER1] CNBC — "Iran says it will 'never bow' as Trump rejects peace counteroffer" May 11, 2026
S14: [TIER1] Tribune India — "Iran FM Abbas Araghchi arrives in New Delhi for BRICS Foreign Ministers' Meeting" May 13, 2026
S15: [TIER1] UN News / European Express — "Lebanon: Fresh strike on Beirut suburbs 'a very alarming development'" May 7, 2026 [NOTE: dates to May 6 Haret Hreik strike, not May 12 — verified by Judge during F4 audit]

[FINAL_EXPERT_QUOTES]

"We are deeply worried also about reports of civilians also being killed in the attack, and that also includes children." — UN Spokesperson Stéphane Dujarric, May 7, 2026, on the May 6 Beirut Dahieh strike (UN News / European Express, S15)

[PUBLISH_DECISION]
status: draft_ready
reason: All seven mandatory hygiene fixes applied, F4 verified via targeted web research (false positive from Source B corrected), F1 resolved, cap enforced at 7 ACTIVE, all probability moves grounded in evidence with delta_reasons.
judge_flags:
  - F4 horizon expires EOD May 15 — same-day resolution check required tomorrow
  - F7 Sunday 2026-05-17 mandatory review: dissolution bill vs. majority-loss adjudication
  - N2 and N3 held in OBE state pending cap clearance; reinstate N2 immediately if Xi summit names Hormuz
  - F5 at 0.28 is a Judge judgment call between two conflicting source assessments — human reviewer should confirm comfort with this split
```
