# Evidensmodell och deduplicering

Steg 6 inför projektets canonical `Evidence`-modell och regler för att skilja antal träffar från antal oberoende belägg.

## Varför detta behövs

En teknik kan förekomma i samma jobbannons på myndighetens webbplats, LinkedIn och flera jobbaggregatorer. Utan deduplicering skulle fyra URL:er kunna se ut som fyra oberoende bevis trots att allt kommer från samma annons.

Samma problem finns när branschpress återger ett leverantörspressmeddelande eller när flera artiklar hänvisar till samma tilldelningsbeslut.

## Två grupper

- `document_duplicate_group` samlar samma dokument/publicering.
- `claim_duplicate_group` samlar samma underliggande uppgift även om den återges i olika dokument.

`relationship` anger om posten är unik, dokumentvariant, derivat av samma claim eller verkligt oberoende corroboration.

## Proveniens

Varje post anger om den är primär, sekundär eller tertiär och om den är originalkälla, länkar till originalet eller endast återger uppgiften.

## Motsägande belägg

Evidens om avveckling eller migrering ska bevaras även om den gäller samma produkt. Det är en ny semantisk observation, inte en dubblett av äldre användningsbelägg.

## Scriptstöd

`scripts/deduplicate_evidence.py` kan:

- normalisera URL:er utan trackingparametrar,
- skapa deterministiskt dokumentfingerprint,
- skapa claim-fingerprint när ursprungsnyckel finns.

Scriptet avgör medvetet inte semantisk oberoendegrad automatiskt. Den kräver proveniensbedömning.

## Koppling till nästa steg

Steg 7 använder Evidence-posterna och deras dedupliceringsstatus för scoring. Bara självständiga evidensenheter ska kunna ge full inkrementell styrka; derivat och dokumentdubbletter ska inte blåsa upp score.
