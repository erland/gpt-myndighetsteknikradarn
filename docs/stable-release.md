# Stabil release 1.0.0

## Status

Myndighetsteknikradarn 1.0.0 är den första stabila releasen efter `1.0.0-rc.1`. RC-versionen har provats i faktisk användning utan blockerande problem och projektet går efter denna release över i maintenance mode.

## Release gates

Före stabil release ska följande passera:

- full regressionstestsvit,
- automatiska realistiska evals utan kritiska fel,
- distributionsvalidering för Chat ZIP och Custom GPT,
- lint utan blockerande fel,
- final project hygiene utan blockerande fynd,
- GPT Byggarens stable-release-validator,
- release-readiness-bedömning,
- checksum- och ZIP-integritetskontroll.

## Runtimeprovning

`1.0.0-rc.1` har provats i faktisk användning och användaren har bekräftat att den fungerar. Detta används som stabiliserande runtime-smoke-test inför 1.0.0.

## Kända begränsningar

Custom GPT har hög metodparitet med Chat ZIP men lägre determinism för scriptstödd scoring, coverage och checkpointing. PDF-export i Custom GPT förutsätter att dataanalys/kodexekvering finns tillgänglig.

## Efter release

Projektet är i maintenance mode. Buggrättningar bör göras som patchversioner och nya funktioner som lämplig minor-/majorversion.

## GitHub Actions från 1.0.1

Projektet innehåller två workflows under `.github/workflows/`:

- `ci.yml` kör regressionstester, realistiska evals, lint, hygiene, bygger båda distributionerna, validerar dem och verifierar checksummor vid pull request, push och manuell körning.
- `release.yml` kör samma kvalitetsgates när en GitHub Release publiceras och bygger Chat ZIP samt Custom GPT ZIP med **versionsnumret från release-taggen**. Paketen och deras SHA-256-filer laddas upp som assets till GitHub Release.

Release-taggar kan vara exempelvis `v1.0.1` eller `1.0.1`; ett inledande `v` tas bort i distributionsfilernas versionsnummer. Projektets `gpt-project.yaml` behöver därför inte redigeras enbart för att distributionsfilerna ska få release-taggen som versionsnummer.
