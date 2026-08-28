# Scoring och säkerhetsklassning

Steg 7 inför den reproducerbara `AgencyAssessment`-modellen och scoringpolicyn.

## Designprincip

Score 0–100 är avsedd för rangordning och transparens. Den är **inte** en statistiskt kalibrerad sannolikhet. Två myndigheter med score 78 och 72 ska därför förstås som att den första har starkare samlad evidens enligt modellen, inte att användningssannolikheten är exakt 78 respektive 72 procent.

## Pipeline

1. normalisera målteknik,
2. skapa Evidence,
3. deduplicera dokument och claims,
4. beräkna claim-styrka,
5. aggregera verkligt oberoende claims med avtagande bonus,
6. applicera negativ/motsägande evidens,
7. tillämpa hårda caps,
8. mappa score till evidensnivå och användarens två positiva huvudgrupper.

## Varför avtagande corroboration

Den starkaste observationen står för huvuddelen av bedömningen. Ytterligare oberoende källor stärker slutsatsen men får successivt mindre effekt. Därmed blir modellen mindre känslig för mängden publicerat material kring stora myndigheter.

## Viktiga skydd

- URL-kopior ger inte extra styrka.
- Leverantörskälla kan vara viktig men har inget automatiskt bonuspåslag.
- Underliggande teknik kan endast ge ett spår för en specifik produkt.
- RFI visar intresse, inte köp.
- Ny avveckling kan slå ut äldre användningsbelägg.
- `not_analyzed` hålls helt separat från score 0 / `no_trace_found`.
