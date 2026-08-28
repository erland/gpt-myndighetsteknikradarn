# Målarkitektur – Myndighetsteknikradarn

## Syfte

Projektet ska ge en spårbar researchkedja från en användares teknikfråga till en rangordnad myndighetslista och, i nästa analysfas, relevanta professionella kontaktpersoner.

## Logiskt flöde

1. **TechnologyTarget** – normalisera produktnamn, alias och falska ekvivalenser.
2. **Agency universe** – fastställ vilka svenska myndigheter som ingår och hur många som faktiskt analyseras.
3. **Source discovery** – sök i prioriterade källtyper och hitta originalkällor.
4. **Evidence register** – skapa daterade, deduplicerade evidensposter.
5. **Agency assessment** – väga direkthet, källstyrka, aktualitet och oberoende källor.
6. **Coverage summary** – redovisa analyserade myndigheter samt grupperna relativt trolig/bekräftad, spår och inga hittade spår.
7. **Ranked result** – sortera myndigheter efter evidensstyrka med säkrast först.
8. **Contact research** – som separat nästa fas identifiera professionellt relevanta personer och officiella kontaktvägar.
9. **Export** – generera Markdown, PDF och Confluence Markup med samma käll- och bedömningsmodell.

## Runtimeval

Chat ZIP är primär runtime eftersom arbetsflödet kan kräva flerpassresearch, strukturerat mellanresultat och artefaktexport. Custom GPT byggs separat och ska paritybedömas.

## Centrala designregler

- En sökträff är inte samma sak som evidens för faktisk användning.
- En upphandling kan visa avsikt eller anskaffning men inte automatiskt drift.
- Jobbannonser ska tolkas semantiskt: “vi använder X” väger mer än “X är meriterande”.
- Leverantörskällor är relevanta men ska märkas som partsintresse.
- Flera återpubliceringar av samma grunduppgift ska inte räknas som flera oberoende belägg.
- Äldre evidens ska vägas ned och, vid behov, följas av sökning efter migrering eller avveckling.
- Direkt e-post eller telefon till kontaktperson får bara användas om den är offentligt publicerad i professionellt sammanhang; annars används myndighetens officiella kontaktväg eller växel.
