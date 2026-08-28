# Research workflow policy

Denna policy operationaliserar steg 2 i utvecklingsplanen.

## Obligatorisk ordning

En fullständig teknik-/produktkartläggning följer normalt:

1. `prepare`
2. `screen`
3. `deepen`
4. `verify`
5. `negative_control`
6. `synthesize`

Ordningen får iterera. Exempel: verifiering kan upptäcka ett nytt alias som motiverar ny screening.

## Pass får inte förväxlas med bedömning

Researchpass beskriver vad GPT:n har gjort. Evidensnivå beskriver vad källorna stödjer. En myndighet kan vara fullständigt analyserad men ändå bara ha ett svagt spår.

## Minimikrav för `analyzed`

En myndighet får räknas som analyserad när minst bred screening är genomförd och resultatet har registrerats. Om projektets senare källpolicy ställer högre krav gäller den striktare regeln.

## Minimikrav för `no_trace_found`

- myndigheten har screenats,
- inga relevanta spår hittades,
- statusen är inte `not_analyzed` eller `ambiguous`.

Negativ kontroll ökar kvaliteten men frånvaro får aldrig uttryckas som bevisad icke-användning.

## Batchning

Vid batchning ska ResearchRun vara stabil över batcherna. Varje myndighet har egen processstatus. Totalsiffror ska alltid baseras på dessa statusar, inte uppskattningar.

## Iteration

Ny information får återöppna en tidigare myndighetsbedömning. Registrera orsaken och bevara tidigare evidens i stället för att skriva över historiken utan spår.

## Slutresultat

Slutresultatet måste kunna skilja:

- scope,
- analyserat,
- ej analyserat,
- sannolik/belagd användning,
- endast spår,
- inga relevanta spår hittades.
