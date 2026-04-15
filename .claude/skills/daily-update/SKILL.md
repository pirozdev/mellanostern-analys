---
name: daily-update
description: Kör daglig Mellanöstern-analys och REGENERERAR index.html från grunden (appenderar aldrig). Hämtar ny data, bygger rapporten med v36-mallen, commit:ar och pushar. Triggas av "daily update", "uppdatera rapporten", "/daily-update".
---

# Daily Update — Regenerating Mideast Report

## Huvudregel

**Appendera aldrig. Regenerera alltid.**

Den här skillen bygger om hela `index.html` från grunden varje dag. Gamla händelser som inte längre är relevanta försvinner automatiskt eftersom de inte produceras om. Det är så rapporten hålls fräsch utan manuell pruning.

## Förutsättningar

- CWD = `mellanostern-analys`-repot
- `index.html` existerar och följer v36-mallen (sticky nav-tabs, daily briefing-format, scenario-adjustment-tabell)
- `main` är ren (inga uncommitted changes)
- Git har push-rättigheter

Om något av detta saknas: avbryt och säg varför.

## Flöde

### Steg 1: Baseline-check

```bash
cd ~/projects/mellanostern-analys
git checkout main && git pull
git status  # måste vara "clean"
wc -c index.html  # notera start-storlek
```

Om `index.html` är > 200 kb: varna användaren att grundfilen redan är uppsvälld (daglig regenerering borde hålla den under 150 kb). Fråga om engångs-städning innan du kör.

### Steg 2: Extrahera mallen (inte innehållet)

Läs `index.html`. Identifiera:
- **CSS och `<head>`** (rad 1-336 ungefär): återanvänds oförändrat
- **Nav-tab-strukturen** (`<nav class="nav-tabs">`): återanvänds oförändrat
- **Sektions-containrar** (rubriker, data-tab-attribut, wrapper-divs): återanvänds oförändrat
- **Script-blocket längst ner**: återanvänds oförändrat

Spara dessa som "template" i minnet. ALLT annat (faktiska händelser, citat, siffror, expertbedömningar, källor) ska kastas och regenereras.

### Steg 3: Kör analysen

Invoke `anthropic-skills:geopolitical-mideast-analyst` via Skill-verktyget.

Ge den följande direktiv som arg:
> Producera dagens analys för {DATUM}. Fokus: senaste 24-48h händelser. Inkludera historiska ankare ENDAST om de refereras direkt i dagens scenarier. Format: strukturerad data, inte HTML — jag gör HTML-genereringen separat.

Spara outputen som `analysis_today`.

### Steg 4: Regenerera index.html

Skapa ny `index.html` genom att:
1. Börja med template-mallen från steg 2
2. Fyll varje sektion med färskt innehåll från `analysis_today`:
   - Hero: dagens datum, war-day (förra +1), version (förra +1)
   - Daily Briefing: dagens headline + 5 numrerade punkter
   - Scenario Adjustment-tabellen: dagens tre sannolikheter vs igår
   - Regime Change-kort: nuvarande sannolikheter (Iran, Israel)
   - Executive Summary / Scenarios: dagens text
   - OSINT-flikarna: dagens narrative per sfär
   - Expert Validation: dagens tre-expert-perspektiv
   - Early Warning Dashboard: dagens 10 signaler
   - Sources: ENDAST länkar från dagens/gårdagens commits (äldre källor flyttas till `archive/`, se Steg 7)

3. **Historiska ankare** — inkludera ENDAST om:
   - Händelsen refereras explicit i dagens analys
   - OCH händelsen var tröskelpassage (första gången X hände)
   - Om båda sant: en kort rad i relevant sektion, inte ett eget block

### Steg 5: Storleks-gate

```bash
wc -c index.html.new
```

- **≤ 150 kb:** OK, fortsätt
- **150-200 kb:** varna, be analysen vara mer koncis, regenerera
- **> 200 kb:** FEL. Regenereringen använder för mycket text. Trimma och försök igen.

### Steg 6: Struktur-gate

Kör en snabb sanity-check:
```bash
python3 -c "
import re
c = open('index.html.new').read()
opens = len(re.findall(r'<div[\s>]', c))
closes = len(re.findall(r'</div>', c))
assert opens == closes or abs(opens-closes) <= 1, f'div mismatch: {opens}/{closes}'
print('structure OK')
"
```

Om strukturen är bruten: FEL. Regenereringen lämnade orphan tags. Kasta och försök igen.

### Steg 7: Arkivera gårdagens sources

Innan du skriver över `index.html`:
```bash
mkdir -p archive
cp index.html archive/$(date -v-1d +%Y-%m-%d).html  # gårdagens
```

Detta bevarar full historik utanför main-rapporten. Om någon vill se "vad sa rapporten för en vecka sen" → arkivet.

### Steg 8: Skriv + commit + push

```bash
mv index.html.new index.html
git add index.html archive/
git commit -m "v{N+1}: Day {X+1} — {dagens headline}"
git push origin main
```

Version och war-day inkrementeras från senaste commit:
```bash
LAST_VERSION=$(git log --format=%s -1 | grep -oE 'v[0-9]+' | head -1)
```

## Säkerhetsregler

1. **Aldrig force-push.**
2. **Aldrig ändra `archive/`-filer retroaktivt.**
3. **Om analysen misslyckas halvvägs:** lämna `index.html` orörd på main. Skriv till `index.html.new` under hela flödet, byt namn först i Steg 8.
4. **Om du är osäker på om en historisk händelse ska behållas:** ta bort den. Den finns i `archive/` om den behövs.
5. **Template-mallen får INTE regenereras av analys-agenten.** CSS, nav, script-blocket är statiskt. Om analys-agenten försöker ändra dem: ignorera det och använd ursprunglig template.

## Debugging

Om rapporten börjar svälla igen trots denna skill:
1. Kolla senaste commit — regenererades verkligen hela filen, eller appenderades det till existerande innehåll?
2. Kolla Steg 3 — fick `geopolitical-mideast-analyst` rätt direktiv om format?
3. Kolla Steg 4 — blandades gammal och ny text (partial regeneration är buggens källa)?

## Första körningen efter skill-installation

Kör en gång manuellt och granska diff:en innan du schemalägger. Förvänta dig:
- Filstorlek: ~80-120 kb (inte 200+)
- War-day: inkrementerat med 1
- Sources: endast dagens/gårdagens länkar
- Inga hänvisningar till händelser från 2+ veckor sen om de inte är verkliga ankare
