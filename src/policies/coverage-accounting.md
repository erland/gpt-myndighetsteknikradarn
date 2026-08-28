# Policy för täckningsredovisning

## Syfte

Täckningsmåtten ska hindra falsk fullständighet. Researchstatus och evidensbedömning är två olika dimensioner och får inte blandas ihop.

## Processstatus per myndighet

Tillåtna processstatusar:

- `not_analyzed` – ingen fullgod första screening har genomförts,
- `positive_candidate` – relevant spår finns och behöver/har fått fördjupning,
- `no_trace_yet` – första screening klar men negativ kontroll/slutbedömning kan återstå,
- `ambiguous` – screening klar men träffen kan ännu inte tolkas säkert,
- `analysis_complete` – planerade pass för myndigheten är färdiga nog för slutlig klassning.

`not_analyzed` är aldrig ett evidensutfall.

## Slututfall per analyserad myndighet

När en myndighet summeras används exakt ett av:

- `likely_or_confirmed` – slutbedömningen ligger i den positiva huvudgruppen,
- `trace_only` – spår finns men stödet räcker inte för sannolik användning,
- `no_trace_found` – genomförd analys gav inga relevanta spår,
- `unresolved` – myndigheten har analyserats men slutbedömning kan inte göras på ett ansvarsfullt sätt.

`unresolved` ska visas när det är större än noll i stället för att pressas in i en annan kategori.

## Räknare

Varje `ResearchRun` ska minst bära:

- `agency_universe_count` – antal aktiva unika myndigheter i den källbas som scope härleddes från,
- `scoped_agency_count` – antal myndigheter som faktiskt omfattas av uppdraget,
- `analyzed_count` – antal myndigheter där minsta screeningkrav uppfyllts,
- `not_analyzed_count`,
- `likely_count`,
- `trace_count`,
- `no_trace_count`,
- `unresolved_count`.

## Matematiska invariants

Följande måste gälla:

`scoped_agency_count = analyzed_count + not_analyzed_count`

`analyzed_count = likely_count + trace_count + no_trace_count + unresolved_count`

Därmed gäller även:

`scoped_agency_count = likely_count + trace_count + no_trace_count + unresolved_count + not_analyzed_count`

Om räknarna inte går ihop får resultatet inte presenteras som slutligt.

## Analyserad

En myndighet räknas som analyserad när den åtminstone har genomgått den projektdefinierade minsta screeningen. Att namnet har förekommit i en batchlista eller att en sökning misslyckats räcker inte.

## Inga spår

`no_trace_found` kräver faktisk analys. Det betyder endast att relevanta spår inte hittades i de genomförda sökningarna. Det betyder inte att tekniken saknas.

## Ofullständiga körningar

Vid delresultat ska:

- `not_analyzed_count` alltid visas om det är större än noll,
- resultatet märkas som ofullständigt,
- positiva resultat få visas, men totalsiffror får inte beskrivas som slutliga för hela scope,
- återstående myndigheter bevaras i ResearchRun.

## Täckningsgrad

Om det hjälper användaren får GPT:n visa:

`coverage_percent = analyzed_count / scoped_agency_count * 100`

Avrunda för presentation, men behåll heltalsräknarna som källan till sanningen.
