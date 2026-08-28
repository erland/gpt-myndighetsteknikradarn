# Evals och realistiska testfall

## Syfte

Steg 12 kompletterar regressionssviten med scenarier som efterliknar de felsituationer som
är mest riskfyllda i verklig myndighetsteknikresearch. Testfallen använder syntetiska
myndighets- och personnamn och ska inte läsas som faktapåståenden om verkliga organisationer.

## Två testlager

### Deterministiska evals

14 fall kan köras automatiskt eftersom utfallet kan kontrolleras exakt. De täcker bland annat:

- OpenShift kontra endast Kubernetes-belägg,
- RFI kontra faktisk användning,
- tilldelning utan driftbevis,
- återpublicerad jobbannons,
- "meriterande" kontra uttrycklig befintlig miljö,
- gammal historisk evidens,
- nyare avveckling som motsäger äldre användning,
- kontaktperson som bytt arbetsgivare,
- overifierad direktkontakt,
- exportparitet,
- återupptagning av avbruten flerpassanalys.

Kör:

```bash
python scripts/run_evals.py
```

### Manuella runtime-evals

Fyra fall kräver bedömning av språk, transparens och försiktighet och ska därför köras mot
den faktiska distributionen när Chat ZIP byggts:

- `EVAL-010` – leverantörscase som enda källa,
- `EVAL-011` – inga träffar är inte bevis för frånvaro,
- `EVAL-012` – delresultat får inte extrapoleras,
- `EVAL-018` – motsägande aktuell/historisk evidens.

Rubriken finns i `evals/manual/RUBRIC.md`.

## Releaseprincip

Ett kritiskt automatiskt evalfel blockerar release. De manuella runtime-fallen ska vara
körda och godkända innan slutlig releasekandidat accepteras.

## Fynd i steg 12

Eval `EVAL-009` identifierade ett semantiskt fel i den tidigare scoringimplementationen:
score 0 efter en stark ny avvecklingskälla kunde mappas till `no_trace_found`, trots att
relevanta spår fanns. Scoringlogiken korrigerades så stark negativ/motsägande evidens ger
`unresolved` i stället. Därmed reserveras `no_trace_found` för analyser där inga relevanta
evidensposter hittats.
