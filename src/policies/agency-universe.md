# Policy för myndighetsuniversum

## Canonical källa

Utgå från SCB:s **allmänna myndighetsregister** när ett svenskt statligt myndighetsuniversum ska skapas. Registret är den canonical källan för vilka myndighetsposter som finns och ska inte ersättas av en egen, permanent handskriven lista.

SCB anger att registret uppdateras veckovis. Därför är listan ett tidsstämplat snapshot, inte statisk kunskap.

## Standardprofil

Om användaren bara säger "svenska myndigheter" eller motsvarande används `technology_research_default`, om inte uppdraget tydligt kräver hela SCB-registret.

Standardprofilen omfattar:

- statliga förvaltningsmyndigheter,
- myndigheter under riksdagen,
- statliga affärsverk,
- AP-fonder,
- Domstolsverket som namngiven central analysenhet.

Enskilda domstolar och svenska utlandsmyndigheter ingår inte automatiskt i standardprofilen. Skälet är metodiskt: en teknikradar bör inte utan uttryckligt val behandla varje organisatoriskt registerobjekt som en oberoende teknikmiljö. Exkluderingen ska alltid redovisas, och användaren ska kunna välja full SCB-täckning.

## Full registerprofil

När användaren ber om "alla statliga myndigheter", "hela myndighetsregistret" eller motsvarande ska `scb_full_registry` användas eller erbjudas som den tydliga tolkningen.

## Anpassat urval

Om användaren anger en lista, myndighetstyp, departementsområde eller annan avgränsning används `custom`. Urvalet ska kunna reproduceras och dess storlek ska redovisas.

## Identitet och deduplicering

- Föredra organisationsnummer som stabil identitet när det finns.
- Slå inte ihop myndigheter enbart på namnlikhet.
- Namnändringar och omorganisationer ska hanteras som identitetsfrågor, inte som fria textmatchningar.
- Historiska myndigheter får finnas i evidens men ska inte räknas som aktiva i ett aktuellt universum utan stöd.

## Aktualitet

Inför en ny bred analys ska GPT:n försöka uppdatera universumet från SCB när:

- användaren uttryckligen efterfrågar aktuell eller full täckning,
- senaste snapshot är äldre än 30 dagar,
- registerantal eller struktur verkar ha ändrats,
- analysen annars skulle presenteras som heltäckande.

Om aktuell hämtning inte är möjlig ska GPT:n använda senaste kända snapshot, visa datumet och tydligt markera att universumet kan vara inaktuellt.

## Redovisningskrav

Varje analys ska visa:

- vilken scope-profil som användes,
- snapshot-/hämtningsdatum,
- antal myndigheter i scope,
- vad som uttryckligen exkluderats,
- antal faktiskt analyserade,
- antal ej analyserade.

Ett lägre scope än hela SCB-registret får aldrig beskrivas som "alla svenska myndigheter" utan kvalificering.
