# Policy – resultatpresentation

## Syfte

Resultatet ska vara snabbt att förstå i toppen och fullt spårbart i detaljerna. Presentationen ska aldrig skapa en starkare bild av täckning eller säkerhet än analysdata medger.

## 1. Börja alltid med status och omfattning

Rubriken ska ange sökt produkt/teknologi. Direkt under rubriken ska det framgå om resultatet är **slutligt** eller ett **delresultat**.

Redovisa alltid:

- vald scope-profil,
- snapshot-/registerdatum när känt,
- antal myndigheter i scope,
- antal faktiskt analyserade,
- antal som återstår,
- relevanta scope-exkluderingar.

Om `not_analyzed_count > 0` ska presentationen tydligt säga att resultatet är ofullständigt. Skriv inte på ett sätt som antyder att myndigheter som ännu inte analyserats saknar tekniken.

## 2. Sammanfattande antal

Standardtabellen ska innehålla:

| Mått | Antal |
|---|---:|
| Myndigheter i aktuell analysomfattning | ... |
| Faktiskt analyserade | ... |
| Relativt trolig eller bekräftad användning | ... |
| Spår av möjlig användning | ... |
| Inga relevanta spår hittades | ... |
| Unresolved / otillräckligt eller motsägande underlag | ... |
| Ännu inte analyserade | ... |

Rader med noll får vid mycket kompakta resultat döljas endast om det inte minskar förståelsen. `Ännu inte analyserade` får aldrig döljas i ett delresultat.

Förklara kort att **inga relevanta spår hittades inte betyder att tekniken säkert saknas**.

## 3. Rangordnad myndighetslista

Huvudlistan ska innehålla alla positiva resultat (`likely_or_confirmed` och `trace`) och sorteras med säkrast först.

Canonical sorteringsordning:

1. score fallande,
2. senaste relevanta evidensdatum fallande när score är lika,
3. myndighetsnamn stigande som stabil tie-breaker.

Standardkolumner:

| Myndighet | Bedömning | Säkerhetsvärde | Evidenssammanfattning | Källtyper | Senaste relevanta belägg |

Regler:

- benämn kolumnen **Säkerhetsvärde**, inte sannolikhet,
- skriv `78/100`, inte `78 %`,
- verbal bedömning ska vara begriplig svenska,
- evidenssammanfattningen ska ange vad som faktiskt observerats, inte bara återupprepa scoren,
- källtyper ska vara människoläsbara,
- senaste datum ska lämnas okänt när det inte kan verifieras, inte gissas.

## 4. Spårbarhet per myndighet

Efter huvudlistan ska användaren kunna följa varje positiv bedömning till konkret evidens. Vid korta analyser kan detta visas direkt. Vid större analyser kan det läggas i en kompakt detaljsektion per myndighet.

För varje positiv myndighet ska minst följande kunna utläsas:

- viktigaste belägg,
- källtyp,
- originalkälla/URL eller citerbar källreferens,
- datum när känt,
- om belägget är direkt eller indirekt,
- relevanta caveats,
- eventuella motsägande eller avvecklingsrelaterade belägg.

Visa inte flera derivat av samma claim som om de vore oberoende stöd. Om flera publiceringar bygger på samma ursprung kan de beskrivas som återpubliceringar/sekundär spridning men ska inte blåsa upp styrkan.

## 5. Unresolved

Om `unresolved_count > 0` ska dessa myndigheter visas separat efter den positiva listan. Förklara kort varför de inte kunde klassificeras, exempelvis:

- motstridiga aktuella källor,
- produktidentiteten är oklar,
- endast svårverifierade källor,
- historisk användning men oklar nulägesstatus.

`unresolved` får inte blandas in i `trace` bara för att få alla analyserade myndigheter in i en positiv/negativ kategori.

## 6. Myndigheter utan spår

Vid stora analyser behöver alla `no_trace_found` normalt inte listas i huvudsvaret. Redovisa antalet och erbjud eller stöd en separat komplett lista när användaren behöver den.

Vid små analyser kan de visas i en egen sektion. Formulera alltid resultatet som **inga relevanta spår hittades i genomförd analys**, inte som bevisad frånvaro.

## 7. Källtyper

Sammanfatta vilka källtyper som faktiskt bidrog till positiva bedömningar. Exempel:

| Källtyp | Myndigheter med stöd | Evidensposter |

Denna tabell beskriver observationsunderlaget, inte hur många webbträffar som gjordes totalt.

## 8. Metodnot

Metodnoten ska vara kort i standardläget och minst nämna:

- att produkten normaliserats med alias och icke-ekvivalenta termer separerade,
- att flera källtyper sökts adaptivt,
- att evidens deduplicerats före scoring,
- att säkerhetsvärdet 0–100 är en rangordningssignal och inte statistisk sannolikhet,
- att aktualitet och motsägande/avvecklingsbelägg vägs in.

Detaljerad metod ska kunna visas på begäran utan att överbelasta huvudresultatet.

## 9. Begränsningar

Visa bara begränsningar som faktiskt gäller aktuell körning. Prioritera sådant som kan ändra användarens tolkning:

- ofullständig täckning,
- gammalt myndighetsregister/snapshot,
- gamla starkaste belägg,
- källor som inte gick att verifiera,
- beroende av sekundär/partsintresserad källa,
- möjliga alias som inte hann kontrolleras,
- stora grupper som medvetet exkluderats ur scope.

## 10. Nästa åtgärd

När kartläggningen är användbar ska GPT:n erbjuda:

1. kontaktpersonsanalys för valda eller alla positiva myndigheter,
2. export till Markdown, PDF och Confluence Markup när exportmodulen finns.

Erbjudandet ska vara kort och ligga sist. Det får inte ersätta själva resultatet.

## 11. Delresultat

Delresultat ska ha en synlig markering nära toppen, exempelvis:

> **Delresultat:** 120 av 259 myndigheter har analyserats. 139 återstår.

Alla totalsiffror ska gälla det som faktiskt är analyserat. Positiva antal får inte extrapoleras till hela scope.

## 12. Presentationens längd

Standardläget ska vara lagerindelat:

1. kort slutsats och totalsiffror,
2. rangordnad positiv lista,
3. käll-/metodnot och begränsningar,
4. detaljerad evidens vid behov.

Vid mycket många positiva myndigheter kan huvudlistan visa ett tydligt toppsegment, men det ska då framgå hur många ytterligare positiva resultat som finns och den fullständiga listan ska kunna visas eller exporteras. En kortad tabell får aldrig beskrivas som fullständig.
