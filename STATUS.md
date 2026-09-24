# Status – Myndighetsteknikradarn

**Produktversion:** 1.0.2  
**Migration:** GPT Byggaren 1.5.0  
**Tillstånd:** Migration pågår

Den ursprungliga 15-stegs utvecklingsplanen är slutförd och lämnas oförändrad som projekthistorik. Den nya 1.5-migreringen är en separat behavior-preserving modernisering av projekt- och runtime-modellen.

## Migrationssteg

- [x] Steg 1 – Stateful 1.5-projektmodell och plattformsneutrala kontrakt
- [x] Steg 2 – Anpassa test/eval-kontrakt till GPT Byggaren 1.5
- [ ] Steg 3 – OpenCode peer-runtime
- [ ] Steg 4 – Runtime parity och modern releaseleverans
- [ ] Steg 5 – Slutregression, hygiene och reproducerbar release

## Runtime-bedömning

- ChatGPT Chat: ready / active
- Custom GPT: ready / active, med reducerad exekveringsdeterminism
- OpenCode: ready / planned
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

## Aktuellt steg

**Steg 3 – OpenCode peer-runtime.**
