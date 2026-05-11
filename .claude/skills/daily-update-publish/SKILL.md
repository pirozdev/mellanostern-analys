---
name: daily-update-publish
description: Manuell publish-fas av Mellanöstern-rapporten. Läser senaste utkast från `drafts/YYYY-MM-DD/`, visar judge-flaggor för granskning, sveper draft till `index.html`, arkiverar gårdagens, commit:ar till `main` och pushar. Designad att triggas av användaren från laptop på morgonen efter att `daily-update-draft` redan kört i molnet. Triggas av "/daily-update-publish", "publicera dagens rapport".
---

# Daily Update — Publish Phase

## Uppdrag

Sveper en redan-genererad draft till live. Detta är den enda skillen som rör `index.html` och pushar `main`. Den ska:

1. Hitta dagens (eller senaste tillgängliga) draft
2. Visa Judge-flaggor och `status.json` för granskning
3. Få explicit godkännande från användaren om `human_review_required`
4. Arkivera gårdagens `index.html`, sveper draft → `index.html`
5. Commit:a till `main`, push:a

**Kör ALDRIG triplet, agenter eller WebSearch.** Allt analytiskt arbete är redan gjort av `daily-update-draft`.

## Förutsättningar

- CWD = `mellanostern-analys`-repot
- `drafts/YYYY-MM-DD/` finns för dagen (eller senaste 3 dagar)
- `main` är ren
- Git har push-rättigheter via SSH

Om dagens draft saknas: lista senaste 3 dagars drafts och fråga användaren vilken som ska publiceras (eller säg att inget finns).

## Flöde

### Steg 1: Hitta senaste draft

```bash
cd ~/projects/mellanostern-analys
git fetch origin

# Lista alla draft-branches på origin
DRAFT_BRANCHES=$(git branch -r | grep "origin/claude/daily-draft-" | sed 's|origin/||' | sort -r | head -5)

# Plocka senaste; fallback: kolla lokala drafts/-katalog
TODAY=$(date +%Y-%m-%d)
LATEST_BRANCH="claude/daily-draft-${TODAY}"

if ! git show-ref --verify --quiet "refs/remotes/origin/${LATEST_BRANCH}"; then
  # Försök gårdagen
  YESTERDAY=$(date -v-1d +%Y-%m-%d)
  LATEST_BRANCH="claude/daily-draft-${YESTERDAY}"
fi

echo "Plockar draft från: $LATEST_BRANCH"
```

Om ingen draft hittas senaste 3 dagar: avbryt och säg "Ingen färsk draft. Kör `/daily-update-draft` först eller `/daily-update` för fullt manuellt flöde."

### Steg 2: Hämta draft-branchen

```bash
git checkout "$LATEST_BRANCH"
git pull origin "$LATEST_BRANCH"

DATE=$(echo "$LATEST_BRANCH" | sed 's|claude/daily-draft-||')
DRAFT_DIR="drafts/${DATE}"

# Verifiera att alla förväntade filer finns
test -f "${DRAFT_DIR}/index.html.new" || { echo "FEL: ${DRAFT_DIR}/index.html.new saknas"; exit 1; }
test -f "${DRAFT_DIR}/status.json"     || { echo "FEL: ${DRAFT_DIR}/status.json saknas"; exit 1; }
test -f "${DRAFT_DIR}/meta.json"       || { echo "FEL: ${DRAFT_DIR}/meta.json saknas"; exit 1; }
test -f "archive/judge-notes/${DATE}.md" || { echo "VARNING: judge-notes saknas"; }
```

### Steg 3: Läs och presentera status

```bash
cat "${DRAFT_DIR}/status.json"
```

Visa för användaren:

```
📋 DRAFT-STATUS — ${DATE}
Version: ${VERSION}
War-day: ${WAR_DAY}
Storlek: ${SIZE_KB} kb
Strukturgate: ${STRUCTURE_OK}
Status: ${STATUS}

Probabilities:
  Escalation:     ${ESC}%
  Protracted:     ${PROT}%
  De-escalation:  ${DEESC}%

Regime change:
  Iran:       ${IRAN_RC}
  Netanyahu:  ${NETANYAHU_RC}

Headline: ${HEADLINE}
```

### Steg 4: Hantera judge-flaggor

**Om `status === "draft_ready"`:** ingen mänsklig granskning krävs. Hoppa till Steg 5.

**Om `status === "human_review_required"`:** visa varje flaggad post:

```
⚠ JUDGE FLAGGADE ${N} ITEMS — kräver beslut innan publicering:

Flagga 1: ${FIELD}
  Lista 1: ${VALUE_1}
  Lista 2: ${VALUE_2}
  Gap: ${GAP_PP}pp
  Judge:s kompromiss: ${JUDGE_VALUE}
  
  → Acceptera Judge:s värde, eller välj manuellt:
    [J] Judge:s ${JUDGE_VALUE} (default)
    [1] Lista 1 ${VALUE_1}
    [2] Lista 2 ${VALUE_2}
    [O] Annat värde (skriv in)
    [A] Avbryt publicering
```

Använd AskUserQuestion (eller motsvarande) för varje flagga. Om något manuellt val skiljer sig från Judge:s kompromiss → uppdatera `index.html.new` på det specifika fältet (probability-tabellen, hero-banner, scenario-bar). Detta kräver targeted Edit-anrop på de delar av filen som påverkas.

**Om `status === "failed"`:** avbryt och visa felet från status.json. Be användaren köra `/daily-update-draft` igen eller `/daily-update` manuellt.

### Steg 5: Arkivera nuvarande index.html

```bash
git checkout main
git pull --ff-only origin main

mkdir -p archive
PREV_DATE=$(date -v-1d +%Y-%m-%d)
cp index.html "archive/${PREV_DATE}.html"
```

### Steg 6: Sveper draft → main (HTML + persistent forecasts)

```bash
# Hämta draft-filen från draft-branchen
git checkout "$LATEST_BRANCH" -- "${DRAFT_DIR}/index.html.new"
mv "${DRAFT_DIR}/index.html.new" index.html

# v45+: hämta också uppdaterad forecasts/active.json (persistent state)
# Detta är kritiskt — utan det cyklar daglig forecast-uppdatering aldrig till main,
# och cloud-routinen nästa dag ärver stale state.
if git show "$LATEST_BRANCH:${DRAFT_DIR}/forecasts-updated.json" >/dev/null 2>&1; then
  git checkout "$LATEST_BRANCH" -- "${DRAFT_DIR}/forecasts-updated.json"
  # Validera schema innan vi skriver över main:s active.json
  python3 scripts/lint-draft.py /dev/null "${DRAFT_DIR}/forecasts-updated.json" || {
    echo "FEL: forecasts-updated.json validerar inte"; exit 1;
  }
  # Resolved/OBE forecasts arkiveras separat
  python3 -c "
import json
data = json.load(open('${DRAFT_DIR}/forecasts-updated.json'))
resolved = [f for f in data['forecasts'] if f['status'] != 'ACTIVE' and f['status'] != 'OPEN-AMBIGUOUS']
if resolved:
    from pathlib import Path
    Path('forecasts/resolved').mkdir(parents=True, exist_ok=True)
    with open('forecasts/resolved/${DATE}.jsonl', 'a') as out:
        for f in resolved:
            out.write(json.dumps(f) + chr(10))
    print(f'Arkiverade {len(resolved)} resolved/OBE till forecasts/resolved/${DATE}.jsonl')
# Behåll bara ACTIVE och OPEN-AMBIGUOUS i active.json
data['forecasts'] = [f for f in data['forecasts'] if f['status'] in ('ACTIVE', 'OPEN-AMBIGUOUS')]
json.dump(data, open('forecasts/active.json', 'w'), indent=2)
"
fi

# Hämta också judge-notes (de hör hemma på main)
git checkout "$LATEST_BRANCH" -- "archive/judge-notes/${DATE}.md"

# Hämta opposing-narrative om den finns
if git show "$LATEST_BRANCH:${DRAFT_DIR}/opposing-narrative.md" >/dev/null 2>&1; then
  mkdir -p archive/opposing-narratives
  git show "$LATEST_BRANCH:${DRAFT_DIR}/opposing-narrative.md" > "archive/opposing-narratives/${DATE}.md"
fi
```

### Steg 7: Sista validering

```bash
# Storleksgate (igen, post-edit)
SIZE=$(wc -c < index.html)
[ "$SIZE" -gt 153600 ] && { echo "FEL: > 150 kb efter manuella edits"; exit 1; }

# Strukturgate
python3 -c "
import re
c = open('index.html').read()
opens = len(re.findall(r'<div[\s>]', c))
closes = len(re.findall(r'</div>', c))
assert abs(opens-closes) <= 1, f'div mismatch: {opens}/{closes}'
print('structure OK')
"
```

### Steg 8: Commit + push main

```bash
COMMIT_MSG=$(jq -r '.commit_message_template' "${DRAFT_DIR}/meta.json")
# Eller bygg från status.json:
# COMMIT_MSG="${VERSION}: Day ${WAR_DAY} — ${HEADLINE}"

git add index.html "archive/${PREV_DATE}.html" "archive/judge-notes/${DATE}.md"
git commit -m "$COMMIT_MSG

Publicerad från draft-branch: ${LATEST_BRANCH}
Judge-flaggor: ${FLAG_COUNT} (${FLAGS_ACCEPTED_AS_JUDGE_DEFAULT} accepterade som default, ${FLAGS_OVERRIDDEN} manuellt overridade)

Probabilities: Esc ${E}% / Prot ${P}% / De-esc ${D}%
Iran regime change: ${IRAN_RC}
Netanyahu step-down: ${NETANYAHU_RC}"

git push origin main
```

### Steg 9: Städa draft-branchen (valfritt)

```bash
# Behåll draftning för historik 7 dagar, ta bort äldre
git branch -r | grep "origin/claude/daily-draft-" | while read branch; do
  branch_date=$(echo "$branch" | sed 's|.*claude/daily-draft-||')
  age_days=$(( ( $(date +%s) - $(date -j -f "%Y-%m-%d" "$branch_date" +%s) ) / 86400 ))
  if [ "$age_days" -gt 7 ]; then
    git push origin --delete "${branch#origin/}" 2>/dev/null || true
  fi
done
```

(Skip om denna komplexitet inte behövs — branches kostar inget.)

### Steg 10: Verifiera live

Vänta 60s, hämta `https://pirozdev.github.io/mellanostern-analys/`, verifiera att build-version och datum matchar dagens commit.

```bash
sleep 60
curl -s https://pirozdev.github.io/mellanostern-analys/ | grep -E '(date-badge|build-id)' | head -2
```

Rapport till användaren:

```
✅ PUBLICERAT
Version: ${VERSION}
Live på: https://pirozdev.github.io/mellanostern-analys/
Commit: $(git rev-parse --short HEAD)
```

## Säkerhetsregler

1. **Aldrig publicera utan att ha visat Judge-flaggor** för användaren först.
2. **Aldrig push:a om strukturgate eller storleksgate misslyckas.**
3. **Aldrig ta bort äldre `archive/`-filer.**
4. **Om publicering avbryts** → lämna `main` orörd. Draft-branchen påverkas inte.
5. **Om användaren overridar en flagga**: uppdatera ENDAST det specifika fältet i `index.html`, rör inte andra sektioner.

## Debugging

Om dagens draft saknar förväntade filer:
1. Kolla `git log origin/claude/daily-draft-${TODAY}` — kördes draft-jobbet alls?
2. Kolla cloud routine-loggen via Anthropic-konsol
3. Om `status: failed` i status.json — läs orsaken; oftast WebSearch-kvot eller agent-crash

Om publicering misslyckas mitt i (efter swap men före push):
1. `index.html` är redan uppdaterad lokalt → safe, inga skador
2. `git status` → committa manuellt om commit:en gjordes men push:en hängde
3. Om commit:en saknas → bara `git push origin main` borde göra det

## Sammanhang

Detta är fas 2 av två. Fas 1 är `daily-update-draft` (cloud, automatisk, 09:00). Fas 2 är denna skill (laptop, manuell, ~10:00). Fas 1 + Fas 2 = vad `daily-update` (legacy) gör i ett enda flöde.

Använd `daily-update` (legacy single-pass) om du:
- Inte har en draft (cloud-routinen kraschade)
- Vill köra hela flödet manuellt på din laptop (t.ex. på en söndag)
- Felsöker flödet
