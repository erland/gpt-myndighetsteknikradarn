# Migreringsplan – GPT Byggaren 1.5.0

**Projekt:** Myndighetsteknikradarn  
**Migrationstyp:** existing-project, behavior-preserving  
**Modellrobusthet:** `stateful`

Den ursprungliga utvecklingsplanen med steg 1–15 är fortsatt historik i `docs/development-plan.md`. Den här planen gäller endast migreringen till GPT Byggaren 1.5.0.

## Steg 1 – Stateful 1.5-projektmodell och plattformsneutrala kontrakt

Behåll befintlig canonical researchmetod, ResearchRun/checkpoint/resume, evals och Chat/Custom-distributioner.

Inför eller komplettera:

- `model_robustness.level: stateful`,
- explicit bedömning av alla fem peer-runtimes,
- capability contract,
- artifact contract,
- workspace/state contract,
- tool contract,
- CI-lint som verifierar ResearchRun, ResearchCheckpoint och resume-flödet.

**Klart när:** den nya projektmodellen passerar befintlig CI utan att researchbeteendet ändras.

## Steg 2 – Anpassa test/eval-kontrakt till GPT Byggaren 1.5

Registrera befintliga regressionstester och 18 realistiska evals i 1.5:s testmodell. Säkerställ att kritiska automated evals blockerar release och att manuella runtime-evals är tydligt separerade.

## Steg 3 – OpenCode peer-runtime

Bygg OpenCode från samma canonical instruktion, policies, modeller, workflows och relevanta scripts.

Research-state ska ligga separat från runtimefiler. OpenCode ska använda workspace-baserad ResearchRun/checkpoint, deterministic scoring/coverage och export.

## Steg 4 – Runtime parity och modern releaseleverans

Aktiva peers:

- ChatGPT Chat,
- Custom GPT,
- OpenCode.

Reducerade/inaktiva:

- Claude Projects,
- OpenAI Plugin.

Inför runtime contracts, runtime parity, Project ZIP, gemensamma checksummor, delivery manifest och release readiness.

## Steg 5 – Slutregression, hygiene och reproducerbar release

Verifiera:

- full regression,
- behavioral evals,
- project hygiene,
- workflow parity,
- runtime parity,
- reproducerbar leverans,
- slutlig dokumentationssynk.

## Aktuellt steg

Alla migrationssteg 1–5 är klara och verifierade. Projektet är i maintenance-läge efter migreringen till GPT Byggaren 1.5.0.
