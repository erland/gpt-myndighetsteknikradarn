# Myndighetsuniversum och täckningsmodell

## Varför universumet måste vara explicit

En teknikradar kan annars ge två typer av missvisande resultat:

1. ett okänt eller godtyckligt antal myndigheter analyseras men resultatet ser nationellt heltäckande ut,
2. organisatoriska registerposter räknas som separata teknikmiljöer trots att det inte är en rimlig analysenhet för frågan.

Projektet separerar därför **registeruniversum**, **analys-scope** och **faktiskt analyserade myndigheter**.

## Canonical registerkälla

SCB:s allmänna myndighetsregister är huvudkälla. Registret bygger på förordning (2007:755), omfattar statliga myndigheter inklusive domstolar, affärsverk och utlandsmyndigheter och uppdateras veckovis.

Utvecklingssnapshot 2026-08-27:

| Grupp | Antal |
|---|---:|
| Statliga förvaltningsmyndigheter | 244 |
| Myndigheter under riksdagen | 5 |
| Statliga affärsverk | 3 |
| AP-fonder | 6 |
| Sveriges domstolar samt Domstolsverket | 83 |
| Svenska utlandsmyndigheter | 108 |
| **Totalt** | **449** |

Källa: `https://myndighetsregistret.scb.se/`. Snapshotet är referensdata och ska inte behandlas som evigt aktuellt.

## Scope-profiler

### technology_research_default

Standardprofil för teknikresearch. Med snapshotet ovan motsvarar den 259 analysenheter: grupperna förvaltningsmyndigheter, riksdagsmyndigheter, affärsverk och AP-fonder samt Domstolsverket.

Enskilda domstolar och utlandsmyndigheter exkluderas som standard men kan inkluderas på begäran.

### scb_full_registry

Alla aktiva registerposter. Referensantal: 449.

### state_bodies_without_foreign_missions

Alla grupper utom utlandsmyndigheter. Referensantal: 341.

### custom

Explicit användarvalt urval.

## Tre olika antal

Ett ResearchRun ska alltid kunna skilja:

- **universum** – registerbasen som scope byggdes från,
- **scope** – myndigheterna uppdraget omfattar,
- **analyserade** – myndigheterna där minsta screening verkligen genomförts.

Exempel:

> SCB-universum: 449 · Scope: 259 · Analyserade: 120 · Återstår: 139

Det är då fel att säga att 139 myndigheter saknar produkten eller att inga spår hittats där.

## Slutlig reconciliation

För en färdig körning ska varje analyserad myndighet ligga i exakt en huvudkategori:

- relativt trolig/bekräftad,
- endast spår,
- inga relevanta spår hittades,
- unresolved.

Ej analyserade hålls utanför dessa evidensutfall.

## Designkonsekvens

Denna modell gör att en användare kan jämföra resultat mellan olika tekniker utan att täckningsgraden döljs. Den gör också batchad research säkrare: ett delresultat kan vara värdefullt utan att framstå som en nationell slutmätning.
