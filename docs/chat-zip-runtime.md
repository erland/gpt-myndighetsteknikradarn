# Chat ZIP runtime

Steg 13 etablerar `chat_zip` som primär runtime.

## Runtimeinnehåll

- `assistant/instructions.md` – kompilerad canonical instruktion
- `assistant/policies/` – runtimepolicies
- `knowledge/` – seed-data och källandskap
- `schemas/` – strukturerade modeller
- `workflows/` – research-, kontakt- och resumeflöden
- `scripts/` – deterministiska runtimehjälpverktyg
- `templates/` – resultat- och exportmallar

Utvecklingsmaterial som tests, evals, reports och docs följer inte med Chat ZIP.

## Kompilering

Canonical instruktion behåller projektvägar under `src/`. Vid build översätts dessa till runtimevägar, exempelvis `src/models/` → `schemas/` och `src/policies/` → `assistant/policies/`.

## Validering

Manifestet innehåller SHA-256 och storlek för varje runtimefil. ZIP byggs deterministiskt med fasta timestamps. Manuella språk-/resonemangsevals kräver en faktiskt laddad runtimekonversation och kvarstår därför som releasevalidering.
