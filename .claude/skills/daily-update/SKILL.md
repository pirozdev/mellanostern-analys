---
name: daily-update
description: Manuellt fullt flöde av Mellanöstern-rapporten — research + triplet + publicering i ett enda steg. För automatiserad daglig körning, använd istället /daily-update-draft (cloud, schemalagd) + /daily-update-publish (laptop, manuell granskning). Denna kvarvarande full-flow-skill är för felsökning, helger eller när cloud-routinen inte kört. Triggas av "daily update full", "kör hela rapporten manuellt", "/daily-update".
---

# Daily Update — Manuellt full flow (legacy)

> **Notera:** Detta är det ursprungliga ett-steg-flödet som körs lokalt på din laptop. För daglig schemaläggning är det uppdelat i två faser:
>
> - **`/daily-update-draft`** — schemaläggs via cloud routine (kör 09:00 dagligen), producerar draft i `drafts/YYYY-MM-DD/` + judge notes, pushar till draft-branch
> - **`/daily-update-publish`** — du kör manuellt på laptop ~10:00, granskar judge-flaggor, sveper draft till `index.html` och pushar `main`
>
> Använd denna `/daily-update`-skill om:
> - Cloud-routinen kraschade och du vill köra om hela flödet manuellt
> - Du är inte vid datorn på morgonen och vill köra hela på en söndag
> - Du felsöker triplet- eller HTML-genereringssteget

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

### Steg 3: Trippel-blind analys

Tre subagents körs i sekvens: två producerar parallella analyser blindt, en tredje dömer mellan dem. Ingen agent får se de andras output.

#### Steg 3a: Agent A (Analyst) — blind

Spawna subagent (`general-purpose` med web-access). Ge standardbriefing.

> Du är dagens Analyst. Producera strukturerad analys för {DATUM}. Använd WebSearch/WebFetch aggressivt. Fokus: senaste 24-48h händelser. Inkludera historiska ankare ENDAST om de refereras direkt i dagens scenarier. Format: strukturerad textdata med taggade sektioner (`[HERO]`, `[DAILY_BRIEFING]`, `[SCENARIO_PROBS]`, `[REGIME_CHANGE]`, `[WATCH_NEXT_48H]`, `[EXECUTIVE_SUMMARY]`, `[TWITTER_OSINT]`, `[EXPERTS_3]`, `[SCENARIOS_3]`, `[EARLY_WARNING_10]`, `[SOURCES_15]`, `[INSIDE_IRAN]`) — INTE HTML. Producera ditt bästa konsensus-bedömning med sannolikheter och källcitat.

Spara som `analyst_output`.

#### Steg 3b: Agent B (Devil's Advocate) — blind

Spawna SEPARAT subagent (samma typ + web-access). Får INTE se `analyst_output`. Får samma datum och samma output-format.

> Du är dagens Devil's Advocate. Producera strukturerad analys för {DATUM} med ADVERSARIELL framing. Använd WebSearch/WebFetch aggressivt. Samma format som standardanalysen (taggade sektioner, INTE HTML).
>
> **Adversariell uppgift:**
> 1. Där konsensus skulle säga X% upptrappning — fråga: vad om det egentligen är X+20% eller X-20%? Argumentera för det mer extrema värdet.
> 2. Identifiera scenarier som default-analys missar (svart svan, dolda eskalationsvektorer, plötsliga fredsutbrott).
> 3. Vilka källor överviktas av konsensus? Vilka namngivna experter under-citeras eftersom de avviker från huvudbilden?
> 4. Vilka deadlines/förväntningar har passerat utan att materialiseras (motsäger headline-narrativet)?
> 5. Var är consensus probabilities anchored på gårdagens siffror snarare än ny data?
>
> Producera fullständig analys, inte bara invändningar. Probabilities ska vara DINA — argumentera för dem som om du var huvudanalytikern. Hitta minst två sannolikheter där du landar >10 procentenheter ifrån vad konsensus förmodligen skulle säga.

Spara som `devils_output`.

**Steg 3a och 3b spawnas i parallell** (samma user-message, två Agent-anrop) för att minska total körtid och garantera att de inte ser varandras output.

#### Steg 3c: Agent C (Judge) — blind till identitet

Spawna tredje subagent. Ge båda analyserna **utan att avslöja vilken som är vilken** (märk dem `Lista 1` och `Lista 2`, randomisera ordningen — t.ex. flippa baserat på t.ex. dagens datum-paritet).

> Du är dagens Judge. Du får två oberoende analyser av samma situation. Båda har samma format. Din uppgift är att producera en **konsoliderad slutanalys** + en kort **Judge-not** som dokumenterar var och varför listorna avvek.
>
> **Beslutsregler per fält:**
> - **Verifierbar fakta** (datum, namn, casualty-siffror, oljepriser): välj värdet med fler/bättre källcitat. Vid lika: välj det mer konservativa.
> - **Probabilities**: om listorna ligger inom 10 procentenheter — ta medelvärdet, runda till närmsta 5%. Om de ligger >10 procentenheter ifrån varandra — välj den lista vars motivering är mest direkt kopplad till verifierbara händelser senaste 48h. Notera divergensen i Judge-noten.
> - **Scenarier/expertbedömningar**: behåll båda om de inte direkt motsäger varandra. Vid motsägelse: välj listan vars argumentation refererar mer specifika källor.
> - **Sources**: union (alla unika URLs från båda listorna, dedupliceras), max 15 — prioritera de som är från senaste 7 dagarna.
> - **Vid tvivel**: notera i Judge-not för mänsklig granskning, fortsätt med den mer konservativa varianten.
>
> **Output-format:**
> ```
> [JUDGE_NOTES]
> ## Divergenser mellan Lista 1 och Lista 2
> ### D1: [fält, t.ex. "Escalation probability"]
> Lista 1: [värde + 1-rads motivering]
> Lista 2: [värde + 1-rads motivering]
> Beslut: [valt värde + varför]
> Konfidens: [hög / medel / låg]
> ### D2: ...
>
> ## Konvergenser (där båda var överens)
> - [kort lista, en rad per item — t.ex. "Brent $113.54 (5 sources both)"]
>
> ## Flaggade för mänsklig granskning
> - [item där judge inte kunde avgöra, kräver beslut innan publicering]
>
> [FINAL_ANALYSIS]
> [Hela den konsoliderade analysen i samma taggade format som agenterna fick — denna används av Step 4 för HTML-generering]
> ```

Spara som `judge_output`. Extrahera `[FINAL_ANALYSIS]`-sektionen som `analysis_today` (används i Step 4).

**Om Judge flaggar item för mänsklig granskning:** stoppa flödet, visa flaggorna för användaren, vänta på beslut innan Step 4.

### Steg 4: Regenerera index.html

Skapa ny `index.html` genom att:
1. Börja med template-mallen från steg 2
2. Fyll varje sektion med färskt innehåll från `analysis_today` (= Judge:s `[FINAL_ANALYSIS]`):
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

### Steg 7: Arkivera gårdagens rapport + dagens judge-not

Innan du skriver över `index.html`:
```bash
mkdir -p archive archive/judge-notes
cp index.html archive/$(date -v-1d +%Y-%m-%d).html  # gårdagens rapport
```

Skriv Judge-noten från Steg 3c till `archive/judge-notes/YYYY-MM-DD.md`. Format:

```markdown
# Judge Notes — YYYY-MM-DD (v{N+1})

**Modell:** trippel-blind (Analyst + Devil's Advocate + Judge)
**Lista 1 = [Analyst|Devil's Advocate]** (avslöjas EFTER beslut, för transparens)
**Lista 2 = [Analyst|Devil's Advocate]**

## Divergenser
[från Judge-output]

## Konvergenser
[från Judge-output]

## Flaggade för mänsklig granskning
[om några — annars "(inga)"]
```

Detta gör att man kan jämföra över tid: blev Devil's Advocate konsekvent övertrumfad av Analyst? Drev Devil's Advocate scenarier som senare materialiserades? Det är hur trippel-modellen kalibreras över veckor.

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
2. Kolla Steg 3a/3b — fick Analyst och Devil's Advocate rätt direktiv om format?
3. Kolla Steg 3c — extraherades `[FINAL_ANALYSIS]` korrekt eller blandades den med `[JUDGE_NOTES]`?
4. Kolla Steg 4 — blandades gammal och ny text (partial regeneration är buggens källa)?

Om probabilities ser rycktiga ut dag till dag:
1. Läs senaste 7 `archive/judge-notes/*.md`. Fanns mönster där Devil's Advocate konsekvent föreslog +20% upptrappning som senare visade sig korrekt?
2. Om ja — höj viktningen av Devil's Advocate i Step 3c (ändra "vid lika: välj mer konservativ" → "vid lika: välj Devil's Advocate-värde").
3. Om Devil's Advocate aldrig får rätt — överväg att förenkla flödet tillbaka till bara Analyst (men spara judge-noterna som kalibreringsdata).

## Första körningen efter skill-installation

Kör en gång manuellt och granska diff:en innan du schemalägger. Förvänta dig:
- Filstorlek: ~80-120 kb (inte 200+)
- War-day: inkrementerat med 1
- Sources: endast dagens/gårdagens länkar
- Inga hänvisningar till händelser från 2+ veckor sen om de inte är verkliga ankare
- En judge-not i `archive/judge-notes/` som dokumenterar var Analyst och Devil's Advocate avvek
