# Custom GPT – distribution och paritybedömning

## Syfte

Custom GPT är sekundär runtime för Myndighetsteknikradarn. Chat ZIP är fortsatt referensruntime eftersom den kan bära komplett runtimefilstruktur, scripts, schemas och checkpointartefakter i samma paket.

## Krävda Custom GPT-funktioner

För avsedd funktion ska Custom GPT konfigureras med:

- webbsökning/browsing aktiverad för aktuell research,
- fil-/dataanalys eller motsvarande kodexekvering aktiverad för robust filgenerering, särskilt PDF,
- knowledge-filerna i distributionen uppladdade,
- `instructions.md` som GPT-instruktion,
- konversationsstarterna från `conversation-starters.md`.

## Paritet

| Funktion | Chat ZIP | Custom GPT | Bedömning |
|---|---|---|---|
| Teknologinormalisering | Full | Full metodik | Likvärdig |
| Myndighetsuniversum/scope | Full | Full metodik, färsk data kräver webb | Likvärdig med webbsökning |
| Adaptiv flerpassresearch | Full | Full metodik | Likvärdig inom konversation |
| Källtolkning | Full | Full | Likvärdig |
| Evidens/deduplicering | Policy + scripts | Policy, modellutförd | Metodlikvärdig, lägre determinism |
| Scoring | Policy + deterministiskt script | Policy, modellutförd | Samma modell, reducerad reproducerbarhet |
| Coverage reconciliation | Script + modell | Modellutförd | Samma regler, lägre determinism |
| Kontaktpersonsanalys | Full | Full med webb | Likvärdig med webbsökning |
| Markdown-export | Full | Full | Likvärdig |
| Confluence Markup | Full | Full | Likvärdig |
| PDF-export | Deterministisk pipeline | Kräver fil-/dataanalysverktyg | Villkorad paritet |
| Checkpointfil + fingerprint | Full, scriptstöd | Kan sammanfatta tillstånd i chat; filcheckpoint beror på verktyg | Reducerad |
| Exakt resume från extern checkpoint | Full | Möjlig om checkpoint laddas som knowledge/fil och kan läsas | Villkorad |
| Automatiska evals/scripts | Ingår i projekt, ej runtime | Ingår inte | Ej runtimefunktion |

## Viktiga skillnader

### 1. Deterministiska scripts

Chat ZIP kan leverera hjälpscript för scoring, deduplicering, coverage, resume och export. En Custom GPT kör inte knowledge-filer som programkod bara för att de laddats upp. Därför kompileras metoden till instruktion + knowledge och modellen förväntas följa samma regler. Det ger metodparitet men inte identisk determinism.

### 2. Flerpass och återupptagning

Inom samma Custom GPT-konversation kan researchstatus hållas och återges. Robust återupptagning över konversationer är svagare än Chat ZIP:s explicita ResearchCheckpoint med fingerprint, om inte användaren sparar/laddar en checkpointfil.

### 3. Export

Markdown och Confluence är textbaserade och har full metodparitet. PDF kräver att den aktuella Custom GPT-konfigurationen har filskapande/kodexekvering. Om verktyget saknas ska GPT:n inte låtsas att PDF skapats.

### 4. Webbresearch

Knowledge-filerna är metod- och seedmaterial, inte en statisk sanning om dagens myndigheter, personer eller upphandlingar. Färska breda analyser kräver webbsökning och verifiering av aktuella originalkällor.

## Distributionsinnehåll

Custom GPT ZIP ska innehålla:

- `instructions.md` – kompilerad instruktion, högst 8 000 tecken,
- `conversation-starters.md`,
- `CONFIGURATION.md` – installations- och capabilitykrav,
- `knowledge/` – högst 20 kompilerade knowledge-filer,
- `MANIFEST.json`, `RUNTIME.json`, `VERSION`.

Knowledge-filerna grupperar metod och schema efter ansvar för att hålla filantalet lågt och göra retrieval tydligare.

## Slutsats

Custom GPT är fullt användbar för kärnuppgiften: research, evidensbedömning, rangordning, kontaktpersoner och textbaserad export. Chat ZIP är starkare för reproducerbarhet, deterministisk scoring/coverage, checkpointing och garanterad exportpipeline. Därför ska Custom GPT beskrivas som **metodmässigt nära paritet, men med villkorad exekveringsparitet**.
