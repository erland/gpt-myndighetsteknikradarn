# Policy för teknologinormalisering

## Syfte

Normalisering ska hindra att sökresultat för närliggande teknik felaktigt behandlas som belägg för exakt den produkt eller teknologi användaren frågat efter.

## 1. Skapa ett TechnologyTarget före klassificering

Före bred screening ska GPT:n skapa eller uppdatera ett `TechnologyTarget`. Det ska minst innehålla:

- `canonical_name`,
- `target_kind`,
- kända verifierade `aliases`,
- eventuell `vendor`,
- produktfamilj när relevant,
- relaterade men inte likvärdiga termer,
- kända exkluderingar,
- söktermer uppdelade i exact, expansion, disambiguation och negative.

Om identiteten är osäker får normaliseringen vara preliminär, men osäkerheten måste följa med tills den verifierats.

## 2. Klassificera relationen för varje teknikträff

En träff ska tilldelas exakt en primär `match_class`:

1. `exact_target`
2. `verified_alias`
3. `target_version_or_edition`
4. `family_only`
5. `component_only`
6. `underlying_technology_only`
7. `related_not_equivalent`
8. `ambiguous_term`
9. `excluded_false_match`

Endast `exact_target`, `verified_alias` och `target_version_or_edition` får räknas som direkt träff på målprodukten utan ytterligare produktidentitetsbevis.

## 3. Produktfamilj är inte specifik produkt

Om användaren frågar efter en specifik produkt får en träff på familjen inte automatiskt räknas som träff på produkten.

Exempel:

- mål: `Red Hat OpenShift Container Platform`
- träff: `Red Hat Hybrid Cloud` → inte exakt produktbelägg
- mål: `Microsoft SQL Server`
- träff: `Microsoft Data Platform` → inte exakt produktbelägg

Om användaren uttryckligen frågar efter en produktfamilj kan familjen däremot vara själva canonical target.

## 4. Underliggande teknik är inte produktbelägg

Att en produkt bygger på en teknik innebär inte att användning av tekniken bevisar produkten.

Exempel:

- Kubernetes → bevisar inte OpenShift
- Java → bevisar inte JBoss EAP
- PostgreSQL → bevisar inte EDB Postgres Advanced Server
- Elasticsearch → bevisar inte Elastic Cloud

Underliggande teknik får användas som expansionsspår för att hitta fler källor men ska märkas `underlying_technology_only` tills en explicit målproduktkoppling hittas.

## 5. Komponent är inte alltid helheten

En namngiven komponent kan vara relevant men ska inte utan vidare styrka hela sviten/plattformen.

Exempel: träff på en enskild modul i en produktfamilj ska klassas utifrån den faktiska relationen och användarens target.

## 6. Förkortningar måste disambigueras

En förkortning får klassas `verified_alias` endast när den är entydig i källans kontext.

Exempel: `OCP` kan i rätt Red Hat-/containerkontext vara OpenShift Container Platform, men en fristående OCP-träff får inte automatiskt räknas som sådan.

Kontrollera vid behov leverantör, närliggande ord, dokumentets ämne och myndighetskontext.

## 7. Tidigare namn och namnbyten

Ett tidigare officiellt produktnamn kan räknas som alias om relationen är verifierad. Datum ska bevaras när det spelar roll. Ett gammalt alias kan styrka historisk användning men säger inte ensamt att nuvarande efterföljare används idag.

Efterföljare och föregångare som inte är ren namnändring ska normalt klassas `predecessor_uncertain` eller `successor_uncertain` tills en migrations- eller kontinuitetsrelation verifierats.

## 8. Generiska kategorier

Om måltermen är generisk, exempelvis `Kubernetes`, `PostgreSQL` eller `Java`, ska GPT:n inte snäva in den till en specifik leverantörsprodukt. Om användaren däremot anger `Red Hat OpenShift`, får generiska Kubernetes-träffar bara vara expansionsspår.

## 9. Leverantör + produkt

När ett produktnamn är generiskt eller delas av flera aktörer ska leverantör användas för disambiguering när relevant. En träff på leverantören utan produkten är inte produktbelägg.

## 10. Search expansion får aldrig ändra target

GPT:n får använda produktfamiljer, underliggande teknik, komponenter och ekosystemtermer för att hitta kandidatkällor. Men en expanderad sökterm får inte i sig ändra vad som räknas som målträff.

Formellt:

> sökbar relation ≠ evidensmässig ekvivalens

## 11. Nytt alias under research

Om ett trovärdigt nytt alias upptäcks:

1. verifiera relationen,
2. lägg till det i `TechnologyTarget`,
3. registrera varför det accepterades,
4. avgör om tidigare screenade myndigheter behöver återbesökas,
5. återöppna bara de delar av ResearchRun där det nya aliaset rimligen kan ändra resultatet.

## 12. Tvivel ska ge lägre matchklass, inte starkare språk

Om en träff inte säkert kan skiljas mellan exakt target och relaterad teknik ska den klassas `ambiguous_term` och verifieras i ett senare pass. GPT:n ska inte välja den starkare tolkningen för att få fler positiva träffar.
