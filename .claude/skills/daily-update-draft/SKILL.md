---
name: daily-update-draft
description: Automatiserad draft-fas av Mellanöstern-rapporten (forecast-board v45). Kör trippel-blind validering (Analyst forecast updater + DA forecast auditor + Judge calibration editor) mot persistent `forecasts/active.json`, genererar utkast till `drafts/YYYY-MM-DD/` enligt 8-sektions v45-skelett, kör lint-gate (banned verbs, forecast cite, schema, max 7), skriver judge-noter och machine-readable `status.json`. Rör ALDRIG `index.html`. Pushar ALDRIG till `main`. Designad för cloud routine 09:00 Stockholm. Triggas av "/daily-update-draft" eller schedule.
---

# Daily Update — Draft Phase (v45 forecast-board architecture)

## Designprincip

Två jobb separeras helt:

- **"What happened?"** — deskriptivt, källat, verb-disciplinerat
- **"Where is it going?"** — prediktivt, tidsbundet, schemavaliderat, scoreable

Forecasts persisterar över dagar i `forecasts/active.json`. Agenten ärver gårdagens forecasts och gör targeted updates (med Codex-justeringar: cold-start audit, OBE-retirement, ambiguity rules, conditional DA opposing narrative). HTML-rapporten regenereras däremot from scratch varje dag.

## Output-kontrakt

```
drafts/YYYY-MM-DD/
├── index.html.new            ← v45-skelett ifyllt, redo att svepas
├── forecasts-updated.json    ← uppdaterad active.json som ersätter main:s vid publicering
├── status.json               ← {"status": "draft_ready" | "human_review_required" | "failed", ...}
├── meta.json                 ← version, war-day, commit-mall
└── opposing-narrative.md     ← (om triggad) DA:s strongest opposing narrative
archive/judge-notes/YYYY-MM-DD.md  ← divergens/konvergens/flagga-rapport
```

`status.json` exempel:

```json
{
  "date": "2026-05-12",
  "version": "v45.0",
  "war_day": 74,
  "status": "draft_ready",
  "size_kb": 78,
  "structure_ok": true,
  "lint": {"fails": 0, "warns": 1, "passed": true},
  "forecasts_active": 7,
  "forecasts_resolved_today": 0,
  "forecasts_retired_today": 0,
  "forecasts_added_today": 1,
  "judge_flags": [],
  "scenario_probabilities": {"escalation": 25, "protracted": 40, "deescalation": 35},
  "direction_of_travel": "Diplomatic track holding; F2 (memo by May 18) firmed +5pp on Iranian response.",
  "draft_branch": "claude/daily-draft-2026-05-12"
}
```

## Förutsättningar

- CWD = `mellanostern-analys`-repot (cloud routine klonar via GitHub-app)
- Filer som måste finnas på `main`:
  - `forecasts/active.json` (persistent forecast state)
  - `schemas/forecast.schema.json` (validation reference)
  - `templates/v45-skeleton.html` (HTML template med FILL-markörer)
  - `scripts/lint-draft.py` (lint gate)
- `python3` >= 3.7 tillgängligt

Om någon fil saknas: avbryt med `status: "failed"`, beskriv vad som fattas.

## Flöde

### Steg 1: Skapa draft-branch

```bash
cd ~/projects/mellanostern-analys  # eller cloud-routine clone-dir
DATE=$(date +%Y-%m-%d)
BRANCH="claude/daily-draft-${DATE}"
git fetch origin
git checkout main && git pull --ff-only origin main
git checkout -b "$BRANCH" || git checkout "$BRANCH"
mkdir -p "drafts/${DATE}" archive/judge-notes
```

### Steg 2: Ladda state

Läs:
- `forecasts/active.json` → inherited_forecasts (förra dagens, med deras p_prior, status, etc.)
- `templates/v45-skeleton.html` → html_template
- `schemas/forecast.schema.json` → schema (för referens)
- Senaste 3 dagars commits på `main` för version-bump:
  ```bash
  LAST_VERSION=$(git log main --format=%s -1 | grep -oE 'v[0-9]+\.[0-9]+' | head -1)
  ```
- `archive/2026-XX-XX.html` (gårdagens publicerade — för att veta vad senaste war-day var)

Beräkna:
- `WAR_DAY` = senaste publicerade + (dagar sedan dess)
- `VERSION` = LAST_VERSION + (.0 för ny dag) eller (.1 för rerun samma dag)

### Steg 3: Trippel-blind triplet

Tre subagents. Ingen ser någon annans output förrän Judge.

#### Steg 3a: Agent A — Analyst (blind)

Spawna `general-purpose`. Mandat:

> Du är dagens **Analyst**: base-rate forecaster + evidence collector + delta-narrator.
>
> Du får följande inputs:
> - Gårdagens `forecasts/active.json` (inherited_forecasts nedan)
> - Aktuell DATE och WAR_DAY
> - Direktiv om dagens cadence (var fjärde söndag = "cold-start day"; läs WEEKDAY)
>
> **Använd WebSearch/WebFetch aggressivt** för senaste 24-48h evidens. Targetera senaste namngivna källor (Reuters/AP/AFP/Axios/Bloomberg, Iran International, Times of Israel, Al Jazeera). Verifiera oberoende; en single-source claim räcker inte för forecast-update.
>
> **Per inherited forecast, besluta exakt en åtgärd:**
> - **KEEP** (status oförändrad, p oförändrad, delta_reason = "No material movement")
> - **UPDATE** (p ändras, kräver delta_reason ≥1 mening med specifika events från senaste 48h)
> - **RESOLVE-YES / RESOLVE-NO / RESOLVE-AMBIGUOUS** (horizon passerat eller events utlöser resolution_criteria; sätt graveyard_reason="resolved")
> - **RETIRE-OBE** (events superseded the question; sätt graveyard_reason="superseded" eller "no_longer_relevant" eller "bad_question"; status="OBE")
> - **MERGE** (forecast subsumeras av annan; sätt graveyard_reason="merged" + merged_into=<id>)
>
> **Sedan: föreslå nya forecasts** (max så total ACTIVE landar ≤7). Varje ny forecast måste passera hygieneporten:
> 1. Binär eller resolvbar?
> 2. Har deadline (horizon_date)?
> 3. Probability 0.05-0.95?
> 4. Resolution criteria + ambiguity rule + resolution source rule specificerade?
> 5. ≥1 leading indicator strukturerad enl. schema?
> 6. owner_category från enumlistan?
>
> **Targetera horisontfördelning** (target, inte hard fill):
> - ≥1 i 24-72h
> - ≥1-2 i 7-14d
> - 0-1 i 30-90d
> - 0-1 i 6-12mo
> - Tomma slots OK; force inte fram skräpforecasts.
>
> **Söndagscadens (om WEEKDAY==Sun):** kör **cold-start audit**. För varje ACTIVE forecast: gör en fristående base-rate-bedömning IGNORERANDES inherited p, skriv resultatet som `p_cold` bredvid `p_inherited`. Om |p_cold − p_inherited| > 7pp: flagga för Judge-beslut (Judge avgör vilken som publishas, motivering loggas).
>
> **Output-format (strukturerad text, INTE HTML):**
>
> ```
> [DATE]: 2026-05-12
> [WAR_DAY]: 74
> [WEEKDAY]: Monday
>
> [FORECAST_UPDATES]
> F1 = 2026-05-11-iran-public-response-by-may-13
>   action: UPDATE
>   p: 0.65 (was 0.55)
>   delta_reason: "Baghaei (FM spokesperson) named the 14-point framework on Press TV May 11; Tasnim ran translated commentary. Two sources, named official — partial resolution signal."
>   indicators:
>     - "Tasnim publishes named Foreign Ministry comment on MOU" → state: OBSERVED, observed_at: 2026-05-11
>     - "Mojtaba Khamenei live televised address" → state: NOT_OBSERVED (unchanged)
>   status: ACTIVE
>
> F2 = 2026-05-11-us-iran-memo-signed-by-may-18
>   action: KEEP
>   delta_reason: "No material movement."
>   ...
>
> [NEW_FORECASTS]
> N1 = 2026-05-12-hezbollah-radwan-retaliation-by-may-20
>   ...full schema-compliant forecast object...
>
> [RETIREMENTS]
> F7 (Netanyahu coalition collapse) — KEEP, but flagged for Sunday weekly review (not modified today; weekly cadence per spec).
>
> [COLD_START_AUDIT]
> (only if Sunday)
> F1: p_inherited=0.55, p_cold=0.60, gap=5pp — within tolerance.
> F2: p_inherited=0.35, p_cold=0.50, gap=15pp — FLAG FOR JUDGE.
>
> [DESCRIPTIVE_DELTA]
> Three to five paragraphs of "what happened in the last 24-48h." Pure description.
> BANNED VERBS in this section: signals, indicates, points to, suggests, underscores, reflects,
> reveals, marks, prepares ground for, positions for, sets up, paves the way, foreshadows,
> opens the door to, hints at, raises the prospect of, increases/lowers the odds of,
> makes X more/less likely, pressure is building, momentum is shifting.
> Each paragraph MUST end with one of:
>   → moved F#  (cites forecast IDs that this evidence moved)
>   → supports F# without move  (evidence is real but probability didn't change)
>   → context only  (factual but doesn't bear on any open forecast)
>
> [INSIDE_IRAN]
> ~200 words on state-media framing. Same verb-ban applies. Same → cite rule.
>
> [SOURCES]
> Up to 15 sources from last 7 days. Each tagged [TIER1] (Reuters/AP/AFP/Bloomberg/major dailies),
> [OSINT] (Telegram channels, X analysts), [STATE_MEDIA] (IRNA, Press TV, Tasnim, Kayhan, RIA),
> or [EXPERT] (named analyst commentary, think-tank papers).
>
> [EXPERT_QUOTES]
> Optional. Named expert direct quotes from the last 7 days, only if cited in [DESCRIPTIVE_DELTA].
> Each: name, affiliation, quote, source URL.
> ```

Spara som `analyst_output`.

#### Steg 3b: Agent B — Devil's Advocate (blind)

Spawna SEPARAT general-purpose. Får INTE se `analyst_output`. Får samma inputs (inherited_forecasts, datum, WebSearch). **Får också den uppdaterade listan av candidate forecasts från Analyst** — men *inte* Analyst:s delta_reasons eller narrativ; bara forecast-objekten själva.

Mandat:

> Du är dagens **Devil's Advocate / forecast auditor**. Du är INTE en parallell pundit. Du är hygien.
>
> Du får candidate forecasts (post-Analyst). Granska varje för:
>
> 1. **Resolution-criteria-test:** Skulle två kompetenta analytiker oberoende komma fram till samma YES/NO/AMBIGUOUS-beslut givet criteria? Om nej, criteria är vag.
> 2. **Ambiguity-rule-test:** Förutser den kontrafaktiska resolutionsvägar realistiskt? Iran "rejects" via counter-proposal = AMBIGUOUS-NO är en sådan rule. Om ambiguity_rule = "any other outcome", den är värdelös.
> 3. **Source-rule-test:** Är resolution_source_rule specifik nog att förhindra propaganda-källor från att resolva forecasts vid horizon? "Reuters/AP/AFP" = OK. "Major media" = för vagt.
> 4. **Indicator-test:** Är indicators observerbara via OSINT inom resolution-fönstret? "IRGC internal deliberations" = inte observerbart. "KC-46 tracks resume on ADS-B" = observerbart.
> 5. **Status-test:** Forecasts orörda i >10 dagar (last_reasoned_at lookback) — argumentera för OBE-retirement OM den underliggande frågan har superseded av events.
> 6. **Verb-disciplin:** Granska Analyst:s `[DESCRIPTIVE_DELTA]` och `[INSIDE_IRAN]` för banned verbs OCH för avsaknad av required cite-markörer. Lista varje violation.
>
> **Mandatory opposing narrative — CONDITIONAL.** Skriv en 150-ord strongest-opposing-narrative ENDAST om någon av:
> - Direction-of-Travel kommer att ändras (Judge:s sak att avgöra; flagga om du tror det)
> - Något forecast rör sig ≥5pp
> - Nytt forecast läggs till
> - Något forecast orört >10 dagar
> - Söndags-cold-start-gap >7pp på något forecast
>
> Format:
> ```
> Claim being opposed: <one line>
> Best contrary evidence: <2-3 sentences with named sources>
> What would prove the report wrong within 7 days: <observable falsifier>
> DA recommendation: <hold | reduce | increase | retire forecast F#>
> ```
>
> Om inga triggers gäller: skriv "No opposing narrative required today; no qualifying triggers."
>
> **Output-format:**
>
> ```
> [HYGIENE_FINDINGS]
> F1: resolution_criteria OK / ambiguity_rule TOO_VAGUE — "any other outcome" doesn't cover the counter-proposal pathway.
> F2: OK across all dimensions.
> N1 (new): indicator "IRGC internal deliberations" not OSINT-observable; reject or replace.
> ...
>
> [VERB_VIOLATIONS]
> [DESCRIPTIVE_DELTA] para 2: "Saudi airspace closure signals a structural ceiling" — banned verb 'signals'.
> ...
>
> [CITE_VIOLATIONS]
> [INSIDE_IRAN] para 1: ends without → marker.
> ...
>
> [STALE_FORECAST_FLAGS]
> F7 (Netanyahu coalition): last_reasoned_at 2026-04-29; underlying drivers (Beyachad polling, Smotrich pressure) have moved without forecast update. Recommend Sunday cold-start audit OR retire to weekly cadence.
>
> [OPPOSING_NARRATIVE]
> (Either the structured 4-line block, OR the literal "No opposing narrative required today; no qualifying triggers.")
>
> [RECOMMENDATION_SUMMARY]
> One paragraph: what should Judge change in Analyst's output before publish.
> ```

Spara som `da_output`.

**Steg 3a och 3b ska spawnas i parallell** (samma user-message med två Agent-anrop) för minimal körtid + garanterad blindhet.

#### Steg 3c: Agent C — Judge (blind till identitet... fast nästan)

I detta flöde är Analyst och DA INTE symmetriska. Analyst producerar primärt innehåll; DA är en hygienlager. Märk dem ändå `Källa A` / `Källa B` (randomiserat på datumparitet) för Judge, för att förhindra anchor på persona.

Spawna `general-purpose`. Mandat:

> Du är dagens **Judge / calibration editor**. Du tar in:
> - `Källa A` — antingen Analyst:s output eller DA:s hygienrapport (du vet inte vilken)
> - `Källa B` — den andra
>
> Du producerar:
> 1. En **konsoliderad förslag-set forecasts** för dagen — den exakta `forecasts-updated.json` som ska skrivas
> 2. En **rendrad version** av varje text-sektion (descriptive delta, inside iran) med alla verb-violations + cite-violations fixade
> 3. **Direction-of-Travel one-liner** — SKRIVS SIST, efter forecasts är låsta. Måste citera ≥2 forecast IDs som `F#`. Om inget forecast rörde >2pp idag: skriv literally `"No material movement — see Inside Iran for context."`
> 4. **Sönds-cold-start-beslut** — om Källa A/B flaggade cold-start-gap >7pp: avgör vilken (cold eller inherited) som ska publiceras; logga motivering.
> 5. **Veckosvar på DA:s opposing narrative** — minst en gång per vecka måste du explicit accept/reject DA:s strongest objection och skriva varför. Inte citera (Codex: citation = theater). Decide.
>
> **Beslutsregler:**
> - DA-flaggade hygiene-issues på forecasts → Källa A:s forecast måste fixas innan publish ELLER forecasten droppas helt.
> - Verb-violations → Källa A:s text måste fixas innan publish (Judge editar direkt).
> - Cite-violations → samma.
> - DA:s opposing narrative → Judge beslutar publish/internal-only och accept/reject; ALDRIG bara "cite for theater".
> - Probability-konflikter (om DA inte gav alternativ-p men flaggade Analyst:s motivering svag) → Judge sänker probability mot p_prior tills motivering bär.
> - Cold-start-gap >7pp på söndag → Judge måste välja och motivera.
>
> **Output-format:**
>
> ```
> [JUDGE_NOTES]
> ## Hygiene fixes applied
> - F1 ambiguity_rule strengthened: ...
> - [DESCRIPTIVE_DELTA] para 2: "signals" → replaced with descriptive verb
>
> ## Forecast moves
> - F1: 0.55 → 0.65 (Analyst proposal accepted; DA had no hygiene issue)
> - F2: 0.35 → 0.35 (kept; Analyst proposed UPDATE but evidence was single-source per DA)
>
> ## Cold-start decisions (Sundays only)
> - F2: p_inherited=0.35, p_cold=0.50; Judge selects 0.40 — partial cold-start credit because cold-derivation used same sources as inherited.
>
> ## DA opposing narrative — Judge ruling
> (Only if DA produced one)
> ACCEPT: <DA's claim+rec, marked accepted, applied to forecast updates>
> REJECT: <DA's claim+rec, marked rejected, reasoning>
>
> ## Flagged for human review
> - (or "(inga)")
>
> [FINAL_FORECASTS_JSON]
> {full forecasts-updated.json content — ready to write to drafts/.../forecasts-updated.json}
>
> [FINAL_DELTA]
> {edited descriptive delta — verb-clean, every <p> ends with → marker}
>
> [FINAL_INSIDE_IRAN]
> {edited inside iran — verb-clean, → markers}
>
> [FINAL_DIRECTION_OF_TRAVEL]
> {one sentence with ≥2 F# cites, OR the canned no-move sentence}
>
> [FINAL_SCENARIO_MAP]
> {Esc% / Prot% / De-esc% — computed by aggregating relevant forecasts, NOT hand-set}
> {1 sentence per scenario}
>
> [FINAL_REGIME_CHANGE]
> {Iran range, Netanyahu range — only updated on Sundays; otherwise inherited from main}
>
> [FINAL_SOURCES]
> {up to 15 sources, with tier badges}
>
> [FINAL_EXPERT_QUOTES]
> {optional, only quotes cited in FINAL_DELTA}
>
> [PUBLISH_DECISION]
> status: draft_ready | human_review_required | failed
> reason: <one sentence>
> ```

Spara som `judge_output`.

### Steg 4: Skriv draft-filer

Från `judge_output`:

1. Skriv `drafts/${DATE}/forecasts-updated.json` från `[FINAL_FORECASTS_JSON]`. Validera mot schema:
   ```bash
   python3 -c "
   import json
   schema = json.load(open('schemas/forecast.schema.json'))
   data = json.load(open('drafts/${DATE}/forecasts-updated.json'))
   # hand-check required fields via lint-draft.py:
   "
   python3 scripts/lint-draft.py /dev/null drafts/${DATE}/forecasts-updated.json
   # bara forecast-schemavalidering körs eftersom HTML är /dev/null — exit code måste vara 0 eller 2
   ```

2. Bygg `drafts/${DATE}/index.html.new`:
   - Läs `templates/v45-skeleton.html`
   - Ersätt alla `<!-- FILL: ... -->`-markörer med Judge:s `[FINAL_*]`-sektioner
   - Rendera Forecast Board-kort från `[FINAL_FORECASTS_JSON]` (gruppera per horisont-bucket: NEAR-TERM ≤72h / 7-30 DAYS / 30-90 DAYS / 6-12 MONTHS; tomma buckets få visuell `forecast-empty-slot`-placeholder)
   - Rendera Sources med tier-badges
   - Rendera Expert Appendix (collapsible details/summary; om inga quotes: `<p class="expert-empty">No expert citations in today's Delta.</p>`)
   - Säkerställ alla `<p>` i delta och inside-iran slutar med `→ moved F#` / `→ supports F#` / `→ context only`-markörer (Judge har redan editat texten; här bara rendering)

3. Skriv `drafts/${DATE}/meta.json`:
   ```json
   {
     "date": "${DATE}",
     "version": "${NEW_VERSION}",
     "war_day": ${WAR_DAY},
     "commit_message_template": "${NEW_VERSION}: Day ${WAR_DAY} — ${DIRECTION_OF_TRAVEL_FIRST_30_WORDS}",
     "previous_version": "${LAST_VERSION}"
   }
   ```

4. Om DA:s opposing narrative triggades: skriv `drafts/${DATE}/opposing-narrative.md` med strukturen från DA + Judge:s accept/reject-ruling.

5. Skriv `archive/judge-notes/${DATE}.md` från `[JUDGE_NOTES]`.

### Steg 5: Storleks-gate

```bash
SIZE=$(wc -c < drafts/${DATE}/index.html.new)
if [ "$SIZE" -gt 153600 ]; then
  echo "FAIL: index.html.new ${SIZE} bytes > 150 kb"
  STATUS="failed"
fi
```

### Steg 6: Struktur-gate

```bash
python3 -c "
import re
c = open('drafts/${DATE}/index.html.new').read()
opens = len(re.findall(r'<div[\s>]', c))
closes = len(re.findall(r'</div>', c))
assert abs(opens-closes) <= 1, f'div mismatch: {opens}/{closes}'
print('structure OK')
"
```

### Steg 7: Lint-gate (NY i v45)

```bash
python3 scripts/lint-draft.py drafts/${DATE}/index.html.new drafts/${DATE}/forecasts-updated.json
LINT_RC=$?
```

- `0` = pass
- `1` = FAIL, blocka publicering, `status: "failed"` i status.json med lint-output
- `2` = warn, fortsätt med `status: "draft_ready"` men logga warns

Om Judge har redan editat texten i Steg 3c korrekt, lint ska gå igenom. Om lint failar här, är det Judge-pipeline-bug — logga som `failed` och be om human review.

### Steg 8: Skriv status.json

```json
{
  "date": "...",
  "version": "...",
  "war_day": ...,
  "status": "...",
  "size_kb": ...,
  "structure_ok": true,
  "lint": {
    "fails": 0,
    "warns": N,
    "passed": true
  },
  "forecasts_active": 7,
  "forecasts_resolved_today": 0,
  "forecasts_retired_today": 0,
  "forecasts_added_today": 1,
  "judge_flags": [...],
  "opposing_narrative_triggered": false,
  "cold_start_audit_run": false,
  "scenario_probabilities": {"escalation": ..., "protracted": ..., "deescalation": ...},
  "direction_of_travel": "...",
  "draft_branch": "..."
}
```

`status` är:
- `"draft_ready"` — Judge har inga human-review-flaggor, lint pass, struktur OK
- `"human_review_required"` — Judge flaggade ≥1 fält, eller lint warn-nivå behöver mänsklig kalibrering
- `"failed"` — storlek, struktur, lint fail, eller agent crash

### Steg 9: Commit + push till draft-branch

```bash
git add drafts/${DATE}/ archive/judge-notes/${DATE}.md
git commit -m "draft ${NEW_VERSION}: Day ${WAR_DAY} [${STATUS}] — forecast-board v45 automated run

Status: ${STATUS}
Active forecasts: ${ACTIVE_COUNT}
Resolved today: ${RESOLVED_COUNT}
Retired (OBE) today: ${OBE_COUNT}
Added today: ${ADDED_COUNT}
Scenario: Esc ${E}% / Prot ${P}% / De-esc ${D}%
Opposing narrative triggered: ${OPPNARR_BOOL}
Judge flags: ${FLAG_COUNT}

Run by: daily-update-draft v45 (cloud routine)
Lint: ${LINT_PASS_FAIL}
Granska + kör /daily-update-publish lokalt för att svepa till index.html + push main."

git push origin "$BRANCH"
```

### Steg 10: Slutrapport till stdout

```
DAILY-UPDATE-DRAFT v45 KLAR
date=${DATE}
version=${NEW_VERSION}
status=${STATUS}
branch=${BRANCH}
forecasts={active:N, resolved:N, retired:N, added:N}
lint={fails:N, warns:N}
size=${SIZE_KB}kb

Nästa steg: kör /daily-update-publish lokalt på laptop när du är redo.
```

## Säkerhetsregler

1. **Aldrig push:a `main`** från denna skill. Bara draft-branch.
2. **Aldrig rör `index.html`** eller `forecasts/active.json` på main.
3. **Aldrig vänta interaktivt** på människa. Flagga via status.json istället.
4. **Aldrig publicera** om lint fails (exit 1).
5. **Aldrig retro-editera** äldre `archive/`-filer.
6. **Aldrig hand-set scenario probabilities** — de måste härledas från Forecast Board (Judge regel).
7. **Empty horizon buckets stannar tomma.** Visa `forecast-empty-slot` placeholder. Force INTE fram skräpforecasts.

## Debugging

Om lint konsekvent failar på Judge:s output:
1. Kolla `archive/judge-notes/YYYY-MM-DD.md` — vilka edits gjorde Judge?
2. Verifiera att Judge:s `[FINAL_DELTA]`-output har `→` markörer på varje paragraf.
3. Kolla om banned-verb-listan i `scripts/lint-draft.py` har en synonym som Analyst använder och Judge inte fångade — uppdatera listan.

Om forecasts börjar driva (autocorrelated ±2pp över veckor utan resolution):
1. Kolla att söndagscold-start kör (`cold_start_audit_run: true` i status.json varje söndag)
2. Kolla `forecasts/cold_start/YYYY-WW.json` (om Fas 2 implementerat) — vilka forecasts driver vs. cold-derivation?
3. Om >50% av forecasts har |p_cold − p_inherited| < 2pp: cold-start är teater, behöver separat modell-run.

Om OBE-rate > 30% (>30% av forecasts retireras innan resolution):
1. Frågorna formuleras för smalt — events superseder dem snabbare än de hinner resolva
2. Bredda question-formulation i Analyst-prompten

## Schemaläggning

Designad för cloud routine via `/schedule`, redan satt upp som `mideast-daily-draft` (id `trig_01FjEGmoeQeejD4smr9EciQ4`). Cron: `0 7 * * *` UTC = 09:00 Stockholm.

För manuell körning lokalt: `claude code -p '/daily-update-draft'`.

## Versionshistorik

- **v45.0** (2026-05-11): forecast-board architecture. Triplet redesignade (Analyst forecast updater + DA forecast auditor + Judge calibration editor). Persistent `forecasts/active.json`. Lint gate. 8-sektions HTML-template. Banned-verb-discipline + cite-markörer.
- **v44.1** (2026-05-08): single-pass triplet, scenario cards, all sections regenerated daily. Replaced by v45.
