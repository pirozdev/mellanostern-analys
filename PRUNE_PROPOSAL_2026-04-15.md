# Prune Proposal — 2026-04-15

**Rapport-status:** index.html, 212 kb, 1451 rader, Day 47, v42
**Analys-period:** senaste 14 dagars git-diff (24 commits på index.html)
**Modell:** dubbelblind (Pruner + Preserver + Judge, alla tre oberoende subagenter)

## Sammanfattning (efter manuell verifiering 2026-04-15)

| | |
|---|---|
| Pruner föreslog | 7 borttagningar |
| Preserver skyddade | 19 sektioner |
| Judge godkände helt | 1 |
| Judge godkände delvis | 1 |
| Judge avslog | 4 |
| Judge flaggade oklart (nu avgjort) | 1 → ✅ trygg |
| Bonus upptäckt vid verifiering | 1 |
| **Faktisk rekommenderad reduktion** | **~165 rader / ~18-24 kb (8-11% av filen)** |

**Judge's övergripande bedömning:** Bevarande-linjen vann initialt dominant, men manuell verifiering visade att Judge missbedömde P3 (trodde den överlappade med B16 — den gjorde den inte). Efter verifiering + bonus-upptäckt ändras utfallet från "nästan ingen vinst" till "meningsfull reduktion".

## Applicera detta manuellt

Innan du applicerar något:

```bash
cd ~/projects/mellanostern-analys
git checkout -b prune/2026-04-15
```

Öppna index.html och klipp ut radintervallen nedan. Commit:a varje prune som egen commit (lättare att rulla tillbaka enskilda).

---

## Godkända borttagningar

### ✅ P6 — Historical Day 13-15 Updates (rad 1351-1373 + 1407-1411)
**Vad:** Arkiv från Mars 12-14 (Day 13-15 uppdateringar + tillhörande källor).
**Motivering:** Övergivna arkivtrådar från krigets början, 33+ dagar gamla. Inga senaste commits refererar dem. Ingen överlapp med bevarande-listan.
**Uppskattad reduktion:** ~45 rader / ~6 kb.

### ✅ P7 (delvis) — Gammal Kharazi-framing (rad 1140-1142)
**Vad:** ENDAST raderna 1140-1142 — inte hela P7-intervallet. Judge noterade att 1024-1070 hör till B16 (nuvarande regime-assessment) och måste bevaras.
**Motivering:** Pre-April Kharazi-framing ej refererad i senaste commits.
**Uppskattad reduktion:** ~3 rader / <1 kb.
**OBS:** Verifiera själv att 1140-1142 faktiskt är den gamla framingen och inte del av det nya assessmentet — Judge var osäker på den exakta gränsen.

---

## Oklart fall efter verifiering → ✅ TRYGG BORTTAGNING

### ✅ P3 — Post-regime change scenarios (rad 1065-1142)
**Efter manuell läsning av rad 1020-1150:** Judge missbedömde. B16 och P3 handlar om olika frågor:
- **B16 (rad 1023-1063):** "Regime Change in Iran" — sannolikheten ATT regimen faller
- **P3-blocket (rad 1065-1142):** "Post-Regime Change — Does It Lead to Stable Government?" — vad händer OM regimen faller

Det är två separata assessments. Judge såg närheten i radintervall och antog överlapp. Ingen överlapp i innehåll.

P3-blocket innehåller en triple-blind-tabell daterad **March 25** med "Weighted Assessment (March 27)". Noll av senaste 7 dagars commits refererar IRGC junta / civil war / post-regime-scenarier. Övergivet arkiv.

**Ta bort rad 1065-1142 i helhet.** ~78 rader / ~11 kb.

---

## 🆕 Bonus upptäckt vid P3-verifiering

### ⚠️ B16-blocket är också föråldrat (rad 1023-1063) — ditt val

När jag verifierade P3 upptäckte jag något som Preservern missat:

- B16 påstår **28-38% regime change probability** (rad 1028)
- Daterat **"Weighted Assessment (March 31 EVENING)"** (rad 1062)
- Hero-kortet högst upp (rad 400-405) har **22-32%** — den aktuella siffran per v42

Samma fråga, två olika siffror, det detaljerade blocket är 15 dagar stale. Texten refererar "DAY 34 Kharazi assassination", "Mossad uprising FAILED", "Trump 2-3 week exit" — allt från början av april.

**Tre val:**
- **(a)** Ta bort hela 1023-1063 också (~40 rader / ~6 kb). Hero-kortet vid rad 400-405 räcker för dagsbilden.
- **(b)** Behåll strukturen men byt ut siffran till 22-32% och skriv om Weighted Assessment till April 15-data. (Kräver ny analys — kanske bättre i dagliga flödet än i pruning-cykeln.)
- **(c)** Lämna kvar men märk blocket tydligt som "📜 Day 34 archived assessment" så läsaren förstår att det inte är aktuellt.

Rekommendation: **(a)** — hero-kortet har redan aktuell data, detaljblocket duplicerar utan att tillföra.

---

## Avslagna borttagningar (för transparens)

### ❌ P1 — Trump 8PM ET ultimatum, "EVERY BRIDGE DECIMATED" (rad 790)
Konflikt med B12 (Scenario 1 Escalation, prio **kritisk**). Judge: att ta bort skulle bryta Scenario 1:s narrativ av varför escalation bedömdes till 65%. **Bevarande vinner.**

### ❌ P2 — Triple-Blind Validation April 6 (rad 939-995)
Konflikt med B10 (Triple Expert Validation, prio **kritisk**). Judge: de gamla siffrorna (52/25/27) utgör historisk referens för att förstå nuvarande (55/30/15). Utan dem saknas kontext. **Bevarande vinner.**

### ❌ P4 — Scenario 1 med power plant strikes + Bushehr (rad 802-843)
Radintervallet är i princip identiskt med B12 (prio **kritisk**). Även om Trumps power-plant-strikes inte materialiserades, bevaras scenariot som eskalationspath om valet hade gjorts. **Bevarande vinner.**

### ❌ P5 — OSINT/Twitter Expert table med March-assessments (rad 552-639)
Judge såg potentiell överlapp med B10 och B11 (hög prio). Även om datan är från Mars är det then-vs-now-material för att visa expert-utveckling. Gränsfall men bevarande vann. **Bevarande vinner.**

---

## Varningar och kalibrerings-noter (för dig som skill-ägare)

Saker jag fångade när jag sammanställde denna rapport, som skillen bör förbättras på:

1. **Judge förväxlade etiketterna i sin slutsats.** Den skrev "LISTA B (bevARANDE) vinner" men LISTA B var i själva verket Pruner-listan i dispatchen. Analysen i sig är korrekt — Judge identifierade rätt typ per lista från innehållet — men slutsatsen är mislabeled. Vid nästa skill-iteration: lägg till en sanity-check där Judge måste upprepa vilken lista som är vilken innan den kör beslut.

2. **Preserver's B12 innehåller daterad siffra.** B12 beskriver Scenario 1 som "65%" men v42 har 55%. Preserver läste en gammal version. Vid nästa iteration: kräv att Preserver verifierar numeriska claims mot senaste commit-diff.

3. **Mycket konservativ första körning — confirmed (b).** Bara 1 hel + 1 delvis godkänd av 7 förslag var lågt utfall. Manuell verifiering bekräftade att Pruner hade rätt om P3 också, men Judge missade det eftersom Preservern märkt B16 som "hög" och B12 som "kritisk" för generöst. Vid nästa iteration: kräv att Preserver bara får sätta max 3 poster som "kritisk" och max 5 som "hög".

4. **Preservern skyddar föråldrad data som om den vore aktuell.** Det allvarligaste fyndet från denna körning. Preservern listade B16 med siffran "28-38%" som "hög prio" utan att märka att siffran är 15 dagar gammal och motsägs av hero-kortet. Preservern kopierade bara från rapporten utan att korsvalidera mot senaste commits. **Högsta prioritet för nästa iteration:** kräv explicit att Preservern jämför varje numeriskt claim mot git-log senaste 7 dagar och flaggar föråldrade siffror som "NOT preservation-worthy".

5. **Judge gör ytliga överlapp-bedömningar baserat på radintervall-närhet.** Judge antog att P3 (1079-1142) överlappade B16 (1024+) för att de ligger nära varandra. Men blocken handlar om olika frågor (probability that vs scenarios if). Vid nästa iteration: kräv att Judge läser båda blockens rubriker/innehåll innan den utlöser konflikt-regel baserat på rad-närhet.

---

## Rå agent-output (för debugging)

<details>
<summary>Pruner-förslag (alla, även ej godkända)</summary>

P1 (rad 790): Trump 8PM ET ultimatum — hög säkerhet
P2 (rad 939-995): Triple-Blind Validation April 6 — hög säkerhet
P3 (rad 1079-1142): Triple-blind post-regime change March 25 — medel säkerhet
P4 (rad 802-843): Scenario 1 Escalation med power plant strikes — hög säkerhet
P5 (rad 552-639): OSINT/Twitter Expert table March — medel säkerhet
P6 (rad 1351-1373, 1407-1411): Historical Day 13-15 Updates — medel-låg säkerhet
P7 (rad 1029-1075): Regime Change från March 27 Kharazi-framing — medel säkerhet

Totalt Pruner-estimat: ~295-320 rader / ~45-50 kb potential
</details>

<details>
<summary>Preserver-krav (alla 19)</summary>

B1 (350-351): CENTCOM Hormuz blockad Day 3 — kritisk
B2 (351): Trump "war close to over" + Pakistan Round 2 — kritisk
B3 (352): Iran avvisar 20-årigt anrikningsstopp — hög
B4 (356-357): Knesset FY26 budget — hög
B5 (357-358): Houthis Bab el-Mandeb aktivering — kritisk
B6 (350-351): Brent $96 — medel
B7 (362-389): Scenario Adjustment-tabell Day 46→47 — medel
B8 (400-405): Iran Regime Collapse 22-32% — hög
B9 (407-410): Netanyahu Stepping Down 45-55% — hög
B10 (715-763): Triple Expert Validation — kritisk
B11 (768-779): Where Experts Agree & Diverge — hög
B12 (799-842): Scenario 1 Escalation — kritisk
B13 (846-889): Scenario 2 Protracted — hög
B14 (892-936): Scenario 3 De-escalation — hög
B15 (1180-1217): Early Warning Dashboard — kritisk
B16 (1024+): Regime Change Iran Assessment — hög
B17 (1190-1200): Early Warning Table — medel
B18 (350): CENTCOM Day 3 0 vessels/6 turned back — medel
B19 (401-404): Day 43 legacy note Ghalibaf — hög
</details>
