# Evidens- och dedupliceringspolicy

## Syfte

Varje positiv, negativ eller motsägande tekniksignal ska representeras som en strukturerad `Evidence`-post. Målet är spårbarhet och korrekt viktning, inte maximalt antal träffar.

## 1. En evidenspost beskriver vad källan faktiskt visar

Skriv en kort `evidence_summary` som skiljer observation från slutsats.

Bra:

> Jobbannonsen beskriver OpenShift som en del av myndighetens befintliga containerplattform.

Sämre:

> Myndigheten använder säkert OpenShift.

Den senare formuleringen är en bedömning och hör hemma i `AgencyAssessment`.

## 2. Proveniens före antal

Två URL:er är inte automatiskt två oberoende belägg. För varje relevant träff ska GPT:n försöka avgöra:

1. Är detta originalkällan?
2. Är detta samma dokument på annan URL eller i annat format?
3. Är detta en sekundär källa som bygger på en identifierbar originalkälla?
4. Återger flera källor samma underliggande påstående utan självständig verifiering?
5. Är det faktiskt en separat, oberoende observation?

## 3. Två dedupliceringsnivåer

### A. Dokumentdeduplicering

Använd `document_duplicate_group` när flera evidensposter avser samma dokument eller materiellt samma publicering, till exempel:

- samma jobbannons på myndighetens webbplats och en jobbaggregator,
- samma pressmeddelande med trackingparametrar,
- HTML- och PDF-version av samma upphandlingsdokument,
- samma dokument speglat på flera webbplatser.

Relationer:

- `exact_document_duplicate`
- `same_document_variant`

Dessa ska normalt räknas som **ett** självständigt belägg.

### B. Påståendededuplicering

Använd `claim_duplicate_group` när olika dokument återger samma underliggande uppgift.

Exempel:

- leverantörens pressmeddelande citeras ordagrant av branschpress,
- en nyhetssajt återpublicerar myndighetens pressmeddelande,
- flera aggregatorer bygger på samma jobbannons,
- ett blogginlägg refererar samma tilldelningsbeslut utan egen verifiering.

Relationen blir `derivative_same_claim` när källan kan spåras till samma ursprung. Den får då ge kontext eller verifiera att uppgiften cirkulerat, men ska **inte** behandlas som ett nytt oberoende belägg.

## 4. Oberoende corroboration

`independent_corroboration` får användas när två källor har separat proveniens och ger självständigt stöd för samma användningshypotes.

Exempel:

- en myndighetsjobbannons beskriver befintlig OpenShift-miljö,
- ett separat avrop flera månader senare gäller support/licenser för OpenShift,
- en myndighetsanställd presenterar den egna OpenShift-plattformen på en konferens.

Det krävs inte att källorna är oense om detaljer; det avgörande är att de inte bara återger samma ursprungsuppgift.

## 5. URL-normalisering

`canonical_source_url` får normaliseras deterministiskt när det är säkert:

- ta bort fragment (`#...`),
- ta bort typiska trackingparametrar (`utm_*`, `gclid`, `fbclid`),
- normalisera host till gemener,
- sortera kvarvarande query-parametrar.

Ta **inte** bort parametrar som kan identifiera ett faktiskt dokument eller en upphandling.

URL-normalisering är en signal, inte slutligt bevis för dokumentidentitet.

## 6. Fingerprints

När scripts används får följande fingerprints skapas:

- `document_fingerprint`: hash av canonical URL och/eller stabil dokumentidentitet,
- `claim_fingerprint`: hash av normaliserad kärnuppgift (myndighet + målteknik + användningssemantik + ursprung).

Fingerprinting får aldrig ersätta semantisk kontroll när två olika dokument råkar vara lika.

## 7. Originalkälla

När en sekundär källa pekar på originalet ska GPT:n i första hand öppna och registrera originalet som egen Evidence-post. Den sekundära källan kan behållas om den tillför självständig kontext, men proveniensrelationen ska framgå.

Söksnippets och aggregatorsidor är normalt `discovery_only` och bör inte finnas kvar som bärande evidens om originalet har verifierats.

## 8. Motsägande evidens

Deduplicering får aldrig radera semantiskt motsägande signaler.

Exempel:

- äldre källa: “vi använder VMware”
- nyare källa: “migreringen bort från VMware är slutförd”

De är inte dubbletter även om de handlar om samma produkt och myndighet. `decommission_or_replacement` ska bevaras och senare påverka bedömningen.

## 9. Färskhet

Steg 6 lagrar källdatum, hämtat datum och freshness-band. Den exakta numeriska effekten på score definieras först i steg 7.

Standardband för metadata:

- `very_recent`: <= 365 dagar,
- `recent`: 366–1095 dagar,
- `aging`: 1096–1825 dagar,
- `old`: > 1825 dagar,
- `unknown`: källdatum saknas.

Dessa gränser är default och kan senare justeras per källtyp i scoringmodellen.

## 10. Minimikrav för positiv evidens

Varje evidenspost som ska användas i AgencyAssessment ska minst ha:

- rätt myndighet verifierad,
- målteknikens `match_class`,
- `source_type`,
- URL och hämtat datum,
- sammanfattning,
- directness,
- usage_semantics,
- proveniensstatus,
- dedupliceringsstatus.

Om centrala fält inte kan avgöras ska posten markeras med caveat eller `unresolved` snarare än att antaganden fyller luckan.
