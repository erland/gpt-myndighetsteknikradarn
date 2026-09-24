# Status – Myndighetsteknikradarn

**Produktversion:** 1.0.2  
**Migration:** GPT Byggaren 1.5.0  
**Tillstånd:** Maintenance

Den ursprungliga 15-stegs utvecklingsplanen är slutförd och lämnas oförändrad som projekthistorik. Den nya 1.5-migreringen är en separat behavior-preserving modernisering av projekt- och runtime-modellen.

## Migrationssteg

- [x] Steg 1 – Stateful 1.5-projektmodell och plattformsneutrala kontrakt
- [x] Steg 2 – Anpassa test/eval-kontrakt till GPT Byggaren 1.5
- [x] Steg 3 – OpenCode peer-runtime
- [x] Steg 4 – Runtime parity och modern releaseleverans
- [x] Steg 5 – Slutregression, hygiene och reproducerbar release

## Runtime-bedömning

- ChatGPT Chat: ready / active
- Custom GPT: ready / active, med reducerad exekveringsdeterminism
- OpenCode: ready / active
- Claude Projects: reduced / inactive
- OpenAI Plugin: reduced / inactive

## Stateful grund

- `ResearchRun` är auktoritativt research-state.
- `ResearchCheckpoint` är atomisk validerbar snapshot för pause/resume.
- `resume-flow.yaml` härleder räknare och nästa arbete från state i stället för att lita på stale cursors.
- färdiga myndigheter öppnas inte igen utan explicit revisit-orsak.

## Verifiering av steg 1

CI passerade den nya stateful GPT Builder 1.5-linten tillsammans med project hygiene, hela regressionssviten, de realistiska evalsen, Chat ZIP, Custom GPT, distributionsvalidering och checksumkontroll. Researchbeteendet är oförändrat.

## Verifiering av steg 2

CI passerade GPT Builder 1.5-testmanifestet och kontraktsvalidatorn tillsammans med hela den befintliga sviten: 18 realistiska evalfall, varav 14 automatiska och 4 manuella runtime-evals. Den befintliga hårdare policyn är bevarad: alla automatiska evalfel blockerar CI/release, medan manuella runtime-evals hålls separat och bedöms enligt RUBRIC.md när runtime-release kräver det.

## Verifiering av steg 3

OpenCode-distributionen bygger och validerar i CI tillsammans med hela regressions- och evalkedjan. Runtimefiler ligger under `.opencode/myndighetsteknikradarn/`, auktoritativ ResearchRun/checkpoint-state under `.myndighetsteknikradarn-state/` och exporter under `myndighetsteknikradarn-output/`. Dessa ytor får inte användas som research-evidens. Färsk kartläggning kräver webbåtkomst; utan den får OpenCode endast analysera tillhandahållet material och måste redovisa begränsningen.

## Verifiering av steg 4

CI passerade fem-runtime parity-modellen. Aktiva peer-runtimes är ChatGPT Chat, Custom GPT och OpenCode; Claude Projects och OpenAI Plugin är explicit reducerade/inaktiva. Releaseleveransen bygger nu Project ZIP, Chat ZIP, Custom GPT ZIP och OpenCode ZIP samt gemensamma SHA-256-checksummor och delivery manifest. Release readiness verifierar hela leveransmängden.

## Verifiering av steg 5

Slutkörningen passerade full regression, 18 realistiska evals, alla tre aktiva runtimes, Project ZIP, runtime parity, release readiness, final project hygiene, workflow parity och reproducerbarhetskontroll. Reproducerbarhetsgrinden byggde hela releaseleveransen två gånger och verifierade identiska SHA-256-hashar.

## Aktuellt läge

Migreringen till GPT Byggaren 1.5.0 är klar. Projektet är i **maintenance-läge** och PR:n är redo att mergeas.

## Blockerare

Inga.
