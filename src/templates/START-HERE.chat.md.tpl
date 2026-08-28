# {{GPT_NAME}} – Chat ZIP

Det här är den portabla Chat-runtime-distributionen för **{{GPT_NAME}}**.

## Användning

Bifoga ZIP-filen i en ChatGPT-konversation och ange att den ska användas som GPT-kontext i konversationen.

## Uppdrag

Runtimen hjälper till att kartlägga vilka svenska statliga myndigheter som sannolikt använder en viss teknologi eller produkt, med spårbar evidens, täckningsredovisning och rangordnad säkerhetsbedömning. Som separat nästa steg kan den identifiera relevanta professionella kontaktpersoner.

## Viktiga delar

- `assistant/instructions.md` – runtimeinstruktion
- `assistant/policies/` – evidens-, research-, scoring-, kontakt- och exportpolicy
- `knowledge/` – tidsstämplade referensdata och källandskap
- `schemas/` – strukturerade runtime-modeller
- `workflows/` – research-, resume- och kontaktflöden
- `scripts/` – deterministiska runtime-hjälpverktyg
- `templates/` – resultat- och exportmallar

## Viktigt

Runtimen ska använda aktuell webbresearch när en faktisk teknik-/produktkartläggning genomförs. Tidsstämplade knowledge-filer är seed-data och får inte behandlas som evigt aktuella.

## Version

{{VERSION}}

## Entry point

Detta dokument är den mänskliga entrypointen. `MANIFEST.json` beskriver runtimepaketets filer och checksummor.
