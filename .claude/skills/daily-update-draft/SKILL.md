---
name: daily-update-draft
description: Automatiserad draft-fas av Mellanöstern-rapporten. Kör trippel-blind validering (Analyst + Devil's Advocate + Judge), genererar utkast till `drafts/YYYY-MM-DD/`, skriver judge-noter och en machine-readable `status.json`. Rör ALDRIG `index.html`. Pushar ALDRIG till `main`. Designad för att schemaläggas via remote routine (cloud) varje morgon. Triggas av "/daily-update-draft" eller schedule.
---

# Daily Update — Draft Phase

## Uppdrag

Producera dagens utkast utan att publicera något. Splittringen från `daily-update` (full flow) finns för att möjliggöra säker schemaläggning: en cloud routine kan köra detta varje morgon medan publicering förblir manuell när människan granskat judge-flaggor.

**Aldrig** rör `index.html`. **Aldrig** push:a `main`. **Aldrig** vänta interaktivt på människa.

## Output-kontrakt

Detta är en machine-readable status som `daily-update-publish` (och eventuellt monitoring) kan läsa.

```
drafts/YYYY-MM-DD/
├── index.html.new          ← regenererad rapport, redo att svepas till index.html
├── status.json             ← {"status": "draft_ready" | "human_review_required" | "failed", ...}
└── meta.json               ← versionsbump, war-day, commit-meddelande-template
archive/judge-notes/YYYY-MM-DD.md  ← divergens-/konvergens-rapport från Judge
```

`status.json` exempel:

```json
{
  "date": "2026-05-09",
  "version": "v45.0",
  "war_day": 71,
  "status": "human_review_required",
  "size_kb": 72,
  "structure_ok": true,
  "judge_flags": [
    {
      "field": "Escalation probability",
      "lista_1": 25,
      "lista_2": 45,
      "gap_pp": 20,
      "judge_decision": 35,
      "needs_human": true
    }
  ],
  "probabilities": {"escalation": 35, "protracted": 35, "deescalation": 30},
  "regime_change": {"iran": "15-25", "netanyahu": "30-42"},
  "headline": "DAY 71 — ...",
  "draft_branch": "claude/daily-draft-2026-05-09"
}
```

## Förutsättningar

- CWD = `mellanostern-analys`-repot (cloud routine klonar via GitHub-app)
- `index.html` existerar och följer v36-mallen
- Skillen körs antingen lokalt (manuellt) eller i cloud routine med GitHub-write-access

Om `index.html` saknas: avbryt med `status: "failed"`.

## Flöde

### Steg 1: Skapa draft-branch

Cloud routine ska aldrig push:a `main`. All output går till en daterad draft-branch.

```bash
DATE=$(date +%Y-%m-%d)
BRANCH="claude/daily-draft-${DATE}"

cd ~/projects/mellanostern-analys
git fetch origin
git checkout main
git pull --ff-only origin main
git checkout -b "$BRANCH" || git checkout "$BRANCH"
```

### Steg 2: Extrahera mallen (samma som daily-update)

Läs `index.html`, identifiera statisk template (CSS, head, nav-tabs, sektions-containrar, script-block). Behåll oförändrat. Allt annat regenereras.

### Steg 3: Trippel-blind analys

Tre subagents körs blint, identiskt med `daily-update`:

#### Steg 3a: Analyst (blind)

Spawna subagent (`general-purpose` med web-access). Standardbriefing:

> Du är dagens Analyst. Producera strukturerad analys för {DATUM}. Använd WebSearch/WebFetch aggressivt. Fokus: senaste 24-48h händelser. Format: taggade sektioner ([HERO], [DAILY_BRIEFING], [SCENARIO_PROBS], [REGIME_CHANGE], [WATCH_NEXT_48H], [EXECUTIVE_SUMMARY], [TWITTER_OSINT], [EXPERTS_3], [SCENARIOS_3], [EARLY_WARNING_10], [SOURCES_15], [INSIDE_IRAN]). INTE HTML.

Spara som `analyst_output`.

#### Steg 3b: Devil's Advocate (blind, parallellt med 3a)

Spawna SEPARAT subagent. Får INTE se `analyst_output`.

> Du är dagens Devil's Advocate. Producera strukturerad analys för {DATUM} med ADVERSARIELL framing. Argumentera för >10pp avvikelse på minst två probabilities. Hitta missade scenarier, under-citerade experter, deadlines som passerat utan att materialiseras.

Spara som `devils_output`.

**3a och 3b spawnas i parallell** (samma user-message, två Agent-anrop) för minimal körtid + garanterad blindhet.

#### Steg 3c: Judge (blind till identitet)

Spawna tredje subagent med båda outputs märkta `Lista 1` / `Lista 2` (randomisera ordningen baserat på datumparitet).

> Du är dagens Judge. Du får två oberoende analyser. Producera **konsoliderad slutanalys** + **Judge-not** som dokumenterar divergenser.
>
> Beslutsregler per fält:
> - Verifierbar fakta: värde med fler källor; vid lika, mer konservativ
> - Probabilities: gap <10pp → snitt avrundat till 5%; gap >10pp → välj listan med fler 48h-events i motivering, **flagga divergensen**
> - Scenarier/expert: behåll båda om ej direkt motsägande
> - Sources: union, max 15
> - Vid tvivel: konservativ + flagga för human review

Spara som `judge_output`. Extrahera `[FINAL_ANALYSIS]` som `analysis_today`.

### Steg 4: Generera draft-filer

Skapa katalogstrukturen:

```bash
mkdir -p drafts/${DATE}
mkdir -p archive/judge-notes
```

Bygg `drafts/${DATE}/index.html.new` från template + `analysis_today`. Samma sektionsstruktur som `daily-update` Step 4.

Bumpa version och war-day från senaste commit på `main`:

```bash
LAST_VERSION=$(git log main --format=%s -1 | grep -oE 'v[0-9]+\.[0-9]+' | head -1)
# t.ex. v44.1 → v45.0 (major bump för ny dag)
```

Skriv `drafts/${DATE}/meta.json`:

```json
{
  "date": "...",
  "version": "v45.0",
  "war_day": 71,
  "commit_message_template": "v45.0: Day 71 — {dagens headline}",
  "previous": "v44.1"
}
```

### Steg 5: Storleks-gate

```bash
SIZE=$(wc -c < drafts/${DATE}/index.html.new)
if [ "$SIZE" -gt 153600 ]; then
  echo "FEL: > 150 kb"
  # status.json: failed
  exit 1
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

### Steg 7: Skriv judge-noter

`archive/judge-notes/${DATE}.md` — full divergens-/konvergens-/flagga-rapport från Judge:s output. Format identisk med `daily-update` skill.

### Steg 8: Skriv status.json

```bash
cat > drafts/${DATE}/status.json <<EOF
{
  "date": "${DATE}",
  "version": "v45.0",
  "war_day": 71,
  "status": "${STATUS}",
  "size_kb": $((SIZE / 1024)),
  "structure_ok": true,
  "judge_flags": [...],
  "probabilities": {"escalation": ..., "protracted": ..., "deescalation": ...},
  "regime_change": {"iran": "...", "netanyahu": "..."},
  "headline": "...",
  "draft_branch": "${BRANCH}"
}
EOF
```

`status` är ett av:
- `"draft_ready"` — Judge gjorde inga human-review-flaggor; säkert att publish:a auto eller efter snabbgranskning
- `"human_review_required"` — Judge flaggade ≥1 fält där människa måste välja innan publicering
- `"failed"` — något gick fel (storlek, struktur, agent crash); ingen `index.html.new` på branchen

### Steg 9: Commit till draft-branch + push

```bash
git add drafts/${DATE}/ archive/judge-notes/${DATE}.md
git commit -m "draft v45.0: Day 71 [${STATUS}] — automated triplet run

Status: ${STATUS}
Probabilities: Esc ${E}% / Prot ${P}% / De-esc ${D}%
Judge flags: ${FLAG_COUNT}
Run by: daily-update-draft (cloud routine)

Granska och kör /daily-update-publish lokalt för att svepa till index.html + push main."

git push origin "$BRANCH"
```

### Steg 10: Slutrapport

Skriv ut till stdout (för cloud-routine-loggen):

```
DAILY-UPDATE-DRAFT KLAR
date=${DATE}
version=v45.0
status=${STATUS}
branch=${BRANCH}
flags=${FLAG_COUNT}
size=${SIZE_KB}kb

Nästa steg: kör /daily-update-publish lokalt på laptop när du är redo.
```

## Säkerhetsregler

1. **Aldrig push:a `main` från denna skill.** Bara draft-branch.
2. **Aldrig rör `index.html` på `main`.**
3. **Aldrig vänta interaktivt** på människa. Om Judge flaggar → status.json: `human_review_required`, fortsätt utan att blockera.
4. **Om någon agent crashar** → status.json: `failed`, ingen index.html.new produceras.
5. **Cloud routine får inte radera** äldre `drafts/`-kataloger.

## Debugging

Om draft-jobbet konsekvent ger `human_review_required`:
1. Läs `archive/judge-notes/${DATE}.md` — vilka fält flaggas?
2. Är det samma fält dag efter dag (probabilities som kontinuerligt avviker >10pp)? Då är kalibrering fel — antingen Analyst eller Devil's Advocate är systematiskt off.
3. Justera viktningen i Steg 3c (Judge:s beslutsregler) eller framingen i 3a/3b.

## Schemaläggning

Designad för cloud routine via `/schedule`. Recommenderad cron: `0 9 * * *` (varje dag 09:00 lokalt). Det ger publishen 1h marginal innan användaren sätter sig kl 10.

För att köra manuellt på laptop: `claude code -p '/daily-update-draft'`. Samma utgång (skriver till draft-branch lokalt + pushar till origin).
