# Scoring- och säkerhetsklassningspolicy

## Syfte

Scoring ska ge en transparent och reproducerbar rangordning av myndigheter. `score` är ett **evidensbaserat säkerhetsvärde 0–100**, inte en statistiskt kalibrerad sannolikhet.

Scoring sker först efter teknologinormalisering, källklassificering och deduplicering.

## 1. Bedömningsenhet

Räkna självständiga **claim-grupper**, inte URL:er eller antal sökträffar. Samma dokumentvariant och `derivative_same_claim` ska normalt bara påverka score genom sin canonical claim. `independent_corroboration` får däremot ge begränsad extra styrka.

## 2. Positiv grundstyrka per användningssemantik

Utgå från den starkaste verifierade evidensposten i varje självständig claim-grupp:

| usage_semantics | Grundpoäng |
|---|---:|
| `current_use_explicit` | 52 |
| `current_environment_explicit` | 48 |
| `implementation_or_migration` | 40 |
| `procurement_contract_or_calloff` | 34 |
| `procurement_award` | 28 |
| `competence_requirement` | 22 |
| `historical_use` | 18 |
| `procurement_intent` | 13 |
| `competence_merit` | 8 |
| `capability_or_interest_only` | 5 |
| `unknown` | 3 |

`decommission_or_replacement` är negativ evidens och hanteras separat.

## 3. Directness

Modifiera den positiva grundstyrkan:

- `direct`: +10
- `near_direct`: +5
- `indirect`: +0
- `discovery_only`: +0 och hela slutbedömningen begränsas enligt discovery-cap nedan.

## 4. Källmodifierare

Källtypen är en modifierare, inte ett automatiskt bevis:

- `agency_official`: +8
- `agency_public_code`: +6
- `government_or_public_document`: +5
- `procurement_contract_or_calloff`: +4
- `procurement_award`: +3
- `job_ad_official`: +3
- `conference_or_presentation`: +2
- `vendor_customer_case`: +0
- `professional_profile`: -3
- `industry_press`: -3
- `job_ad_aggregator`: -5
- `procurement_notice`: +0
- `procurement_rfi`: -2
- `framework_agreement`: -6
- `search_result_snippet`: -8
- `other_web`: -5

Källmodifieraren ska aldrig göra ett svagt semantiskt påstående starkare än vad texten faktiskt stödjer.

## 5. Teknologimatch och caps

För en specifik produkt:

- `exact_target`, `verified_alias`, `target_version_or_edition`: ingen match-cap.
- `family_only`: max 34.
- `component_only`: max 30.
- `underlying_technology_only`: max 24.
- `related_not_equivalent`: max 18.
- `ambiguous_term`: max 12.
- `excluded_false_match`: 0 och exkluderas från positiv scoring.

Om målobjektet i sig är en produktfamilj eller generell teknologi kan motsvarande relation bedömas annorlunda, men ändringen måste motiveras i `TechnologyTarget` och vara explicit.

## 6. Freshness

Applicera freshness på varje claim innan aggregation:

- `very_recent`: +6
- `recent`: +2
- `aging`: -5
- `old`: -12
- `unknown`: -4

Gamla belägg kan fortfarande vara starka historiska belägg men ska inte utan stöd beskrivas som aktuell användning.

## 7. Verifieringsjustering

För bärande evidens:

- originalkälla öppnad + rätt myndighet verifierad + teknikmatch verifierad: +4,
- delvis verifierad: +0,
- central identitet eller teknikmatch osäker: -8 och normalt `unresolved` om osäkerheten är avgörande.

## 8. Aggregation av positiva claim-grupper

1. Beräkna poäng för varje självständig positiv claim-grupp.
2. Välj den starkaste som `strongest_positive`.
3. Lägg endast en reducerad bonus från ytterligare **oberoende** claim-grupper:
   - näst starkaste: 30 % av dess claim-score,
   - tredje: 20 %,
   - fjärde och senare: 10 % vardera.
4. Total positiv corroboration-bonus är max +25.
5. Dubbletter och derivat ger 0 oberoende bonus.

Detta gör att tio kopior av samma jobbannons inte slår två genuint oberoende källor.

## 9. Negativ/motsägande evidens

`decommission_or_replacement` påverkar bedömningen av **aktuell** användning.

Beräkna negativ claim-styrka med bas 50 plus directness/källmodifierare/freshness/verifiering enligt samma princip, cap 0–70. Applicera sedan:

- negativt belägg nyare än starkaste positiva och `direct`/`near_direct`: dra av 35–70 beroende på styrka,
- negativt belägg ungefär samtida men motsägande: dra av 20–45 och markera `unresolved` om konflikten inte kan lösas,
- äldre negativt belägg än tydlig senare aktuell användning: dra normalt av 0–15.

En explicit ny myndighetskälla som säger att produkten är avvecklad ska kunna väga tyngre än flera äldre positiva belägg.

## 10. Slutscore och nivåer

Klipp slutscore till 0–100.

| Score | Evidence level | Visad huvudkategori |
|---:|---|---|
| 85–100 | Nivå 5 – direkt bekräftat | Relativt trolig eller bekräftad användning |
| 70–84 | Nivå 4 – mycket stark indikation | Relativt trolig eller bekräftad användning |
| 55–69 | Nivå 3 – trolig | Relativt trolig eller bekräftad användning |
| 30–54 | Nivå 2 – spår/indikation | Spår av möjlig användning |
| 1–29 | Nivå 1 – svagt spår | Spår av möjlig användning |
| 0 | Nivå 0 – inga relevanta belägg | Inga relevanta spår hittades |

`unresolved` används i stället för en normal nivå när det finns avgörande identitetsproblem eller olöst stark konflikt.

## 11. Hårda säkerhetsregler

Oavsett råpoäng gäller:

- Endast `discovery_only`: max score 19 och nivå 1.
- Endast indirekta produktfamilj/komponent/underliggande/relaterade träffar: följ match-cap och kan inte nå huvudkategorin `likely_or_confirmed` för specifik produkt.
- Endast ramavtal utan myndighetsspecifikt avrop: ska normalt inte ge positiv produktbedömning; max 9 om det finns ett konkret myndighetsrelaterat discovery-spår, annars 0.
- Endast RFI/marknadsdialog: max 29.
- Endast `competence_merit`: max 29.
- En analyserad myndighet utan relevanta evidensposter får score 0 och `no_trace_found`.
- En ej analyserad myndighet får aldrig score 0/no_trace; den är `not_analyzed`.

## 12. Presentation

Visa normalt score och verbal nivå men skriv tydligt att score är **säkerhetsvärde**, inte sannolikhetsprocent. Sortera myndigheter fallande på score, därefter på senaste starka evidens och antal oberoende bärande källtyper.

Varje rad ska kunna förklaras med de viktigaste evidensposterna och eventuella caveats.

## Evalförtydligande: negativ evidens och score 0

Score 0 betyder inte automatiskt `no_trace_found`. Om relevanta evidensposter finns men de
primärt visar avveckling, ersättning eller en stark olöst konflikt ska utfallet vara
`unresolved` (eller annan uttrycklig negativ/konfliktstatus i en framtida modell), aldrig
`no_trace_found`. `no_trace_found` är reserverat för en faktiskt analyserad myndighet där
inga relevanta evidensposter hittades efter föreskriven sökning.
