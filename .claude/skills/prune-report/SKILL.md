---
name: prune-report
description: Dubbelblind-analys som föreslår vad som kan tas bort ur index.html för att rapporten inte ska svälla. Producerar en PRUNE_PROPOSAL_YYYY-MM-DD.md — redigerar ALDRIG index.html själv. Triggas av "prune report", "rensa rapporten", "/prune-report".
---

# Prune Report — Dubbelblind pruning-förslag

## Uppdrag

Rapporten (`index.html`) växer varje dag när daily-flödet kör. Utan pruning sväller den med stale claims, passerade deadlines och döda trådar. Denna skill producerar ett **förslag** på vad som kan tas bort — aldrig en direkt ändring.

**Output:** `PRUNE_PROPOSAL_YYYY-MM-DD.md` i repo-roten. Människan applicerar manuellt efter granskning.

## Förutsättningar

- CWD = `mellanostern-analys`-repot
- `index.html` finns
- Minst 3 dagars git-historik på `index.html` (annars finns inget att prune:a)

## Flöde

### Steg 1: Samla kontext

Läs:
- `index.html` (hela filen, markera radnummer på varje sektion för senare referens)
- `git log --oneline -14 -- index.html` (senaste 14 dagars commits)
- `git diff HEAD~7 -- index.html` (vad som ändrats senaste 7 dagarna)

Notera:
- Dagens datum (från system)
- Rapportens "war-day" och build-version (hero-sektionen)
- Varje sektion med förekomst + radintervall: hero, daily briefing, regime change-tabell, watch next 24-72h, highlight-strip, narrative analysis (per sfär), Twitter-sentiment, expert-bedömningar, sources

### Steg 2: Agent A (Pruner) — blind

Spawna subagent via Agent-verktyget med följande uppdrag. Agenten får INTE veta att det finns en Preserver.

> Du är en Pruner. Du får `index.html` (med radnummer) och senaste 14 dagars git-diff. Ditt ENDA jobb är att identifiera innehåll som kan tas bort. Var aggressiv men motiverad.
>
> **Borttagningsregler:**
> 1. Händelser/påståenden äldre än 14 dagar som INTE refereras i dagens eller gårdagens commit
> 2. Hotbilder/deadlines som passerat utan att materialiseras (ex: "Iran svarar inom 48h" där >72h gått utan händelse)
> 3. Scenarier/sannolikheter som legat under 10% i 2+ dagar i rad
> 4. Källor/tweets som raderats eller inte går att verifiera (kolla URL-status om möjligt, annars flagga som osäker)
> 5. Regime change-rader där indikator inte rört sig på 7+ dagar
> 6. Duplicerat innehåll mellan sektioner (samma claim i briefing OCH expert-bedömning)
> 7. Övergivna trådar: sektioner som uppdaterades ofta för 2+ veckor sen men inte alls senaste 7 dagarna
>
> **Output** (strukturerad markdown):
> ```
> ## Pruner-förslag
>
> ### P1 (rad X-Y): [kort beskrivning]
> **Varför ta bort:** [regel 1-7 + motivering]
> **Hur säkert:** [hög / medel / låg]
>
> ### P2 (rad X-Y): ...
> ```
>
> Lista MINST 5 förslag om rapporten är större än 100kb. Varje förslag MÅSTE ha radintervall och regelreferens.

Spara outputen i minnet som `pruner_output`.

### Steg 3: Agent B (Preserver) — blind

Spawna separat subagent. Ge SAMMA input som Pruner men motsatt uppdrag. Agenten får INTE se pruner_output.

> Du är en Preserver. Du får `index.html` (med radnummer) och senaste 14 dagars git-diff. Ditt ENDA jobb är att identifiera innehåll som MÅSTE behållas oavsett ålder. Var kritisk — lista bara det som har verkligt kvarvarande värde.
>
> **Bevarande-kriterier:**
> 1. Historiska ankare: första gången en viktig tröskel passerades (ex: "first CENTCOM blockade 10 apr") — även om den är gammal, den är referenspunkt
> 2. Pågående trådar: händelser där senaste uppdateringen ligger inom 5 dagar OCH ingen resolution nåtts
> 3. Referenspunkter för nuvarande scenarier: om ett scenario bygger på en händelse måste händelsen stå kvar
> 4. Recurring patterns: data som visar mönster (ex: veckovis missiluppskjutningsfrekvens)
> 5. Motbilder: claims som motsäger huvudnarrativet (viktiga för balans)
> 6. Citerade expertuttalanden som ofta återanvänds
>
> **Output** (strukturerad markdown):
> ```
> ## Preserver-krav
>
> ### B1 (rad X-Y): [kort beskrivning]
> **Varför behålla:** [kriterium 1-6 + motivering]
> **Prioritet:** [kritisk / hög / medel]
>
> ### B2 (rad X-Y): ...
> ```
>
> Lista ENDAST innehåll som verkligen måste behållas. Om något är trivialt att återskapa från källor, lista det inte.

Spara som `preserver_output`.

### Steg 4: Agent C (Judge) — blind

Spawna tredje subagent. Ge den båda listorna **utan att avslöja vilken som är vilken** (märk dem "Lista 1" och "Lista 2", randomisera ordningen).

> Du är en Judge. Du får två listor med förslag om innehåll i ett dokument. Lista 1 föreslår handlingar, Lista 2 föreslår handlingar. Din uppgift: identifiera konflikter och avgöra vilka förslag från den borttagande listan som FAKTISKT ska genomföras.
>
> **Beslutsregel:**
> - Förslag från borttagande listan godkänns ENDAST om INGEN post från bevarande listan överlappar samma radintervall
> - Vid överlapp: bevarande-posten vinner om den är prio "kritisk" eller "hög", annars detaljerad motivering krävs
> - Vid tvivel: behåll (fel mot falskt-behålla, inte falskt-borttag)
>
> **Output:**
> ```
> ## Judge-beslut
>
> ### Godkända borttagningar (N st)
> - [rad X-Y]: [beskrivning] — motivering: [varför ingen konflikt]
>
> ### Avslagna borttagningar (N st)
> - [rad X-Y]: [beskrivning] — konflikt med: [bevarande-post] — anledning: [...]
>
> ### Oklara fall (N st, för mänsklig granskning)
> - [rad X-Y]: [beskrivning] — båda listorna har argument, människa måste välja
> ```

### Steg 5: Sammanställ `PRUNE_PROPOSAL_YYYY-MM-DD.md`

Skriv till repo-roten. Struktur:

```markdown
# Prune Proposal — YYYY-MM-DD

**Rapport-status:** index.html, {KB} kb, {rader} rader, war-day {N}, version {vXX}
**Analys-period:** senaste {N} dagars git-diff
**Modell:** dubbelblind (Pruner + Preserver + Judge)

## Sammanfattning
- Pruner föreslog {X} borttagningar
- Preserver skyddade {Y} sektioner
- Judge godkände {Z} borttagningar, avslog {W}, flaggade {V} för mänsklig granskning

## Applicera detta manuellt
För varje godkänd borttagning: öppna index.html, gå till radintervall, klipp ut.
**Innan du applicerar: kör `git checkout -b prune/YYYY-MM-DD` först.**

## Godkända borttagningar
[från Judge-output]

## Oklara fall — DU behöver avgöra
[från Judge-output — det här är det viktiga, läs noga]

## Avslagna borttagningar (för transparens)
[från Judge-output]

## Rå agent-output (för debugging)
<details>
<summary>Pruner-förslag (alla, även ej godkända)</summary>
...
</details>

<details>
<summary>Preserver-krav</summary>
...
</details>
```

## Regler

1. **Rör ALDRIG `index.html`.** Bara producera markdown-förslaget.
2. **Alla agenter MÅSTE vara blinda.** Använd Agent-verktyget med subagent_type=general-purpose, skicka bara det de behöver, inte de andras output.
3. **Om git-historik < 3 dagar:** avbryt, säg "för tidigt att prune:a, kom tillbaka efter några dagars flöde".
4. **Om samma prune-förslag stått i 3 dagar utan att applicerats:** notera det överst i rapporten — antingen är förslaget fel eller människan har missat det.
5. **Aldrig föreslå borttagning av hero-sektionen, daily briefing-rubriken eller sources-sektionens grundstruktur.** Bara innehåll inom dem.

## Storleks-forcing function

Om `index.html` > 250kb: markera rapporten som `## ⚠️ URGENT` överst. Pruner-agenten får instruktionen "var mer aggressiv — målet är att krympa till 150kb".

Om `index.html` > 400kb: rekommendera att arkivera hela innehåll äldre än 30 dagar till `archive/YYYY-MM.html` oavsett judge-beslut.
