# Policy – exportformat

## Syfte

Export är en ren presentationsfas ovanpå redan strukturerade och verifierade analysdata. Den får inte göra ny research, skapa nya evidenspåståenden eller ändra scoring.

## Gemensam källa

Markdown, PDF och Confluence Markup ska genereras från samma `ResultPresentation` och, när kontaktresearch genomförts, samma `ContactResearchRun`.

Följande måste vara identiskt mellan formaten:

- målprodukt/teknik,
- partial/complete-status,
- scope och täckningsräknare,
- bedömningsnivå och säkerhetsvärde per myndighet,
- evidenssammanfattningar,
- källtyper och källreferenser,
- begränsningar,
- kontaktkandidater och kontaktvägar.

## Markdown

Markdown är canonical text-export och ska vara läsbar som fristående rapport. Den ska innehålla:

1. titel och analystatus,
2. sammanfattande räknare,
3. rangordnad positiv myndighetslista,
4. unresolved-sektion när relevant,
5. evidens och källor,
6. källtypssammanställning,
7. metod och begränsningar,
8. kontaktpersoner när kontaktresearch finns,
9. exportmetadata.

## PDF

PDF ska vara en fristående läsrapport och innehålla samma sakdata som Markdown. PDF-exporten ska:

- använda inbäddad eller systemtillgänglig Unicode-font som klarar svenska tecken,
- radbryta långa texter och URL:er,
- använda tabeller som kan fortsätta över flera sidor,
- ha sidnummer,
- inte klippa tabellinnehåll utanför sidan,
- behålla klickbara källänkar när renderaren stöder det,
- visuellt markera delresultat.

PDF ska renderingsverifieras i utveckling/test när layout ändras.

## Confluence Markup

Confluence-export ska använda klassisk Confluence Wiki Markup så att innehållet kan klistras in/importeras där detta format stöds.

Använd:

- `h1.`, `h2.`, `h3.` för rubriker,
- `||` för tabellhuvud,
- `|` för tabellceller,
- `[text|URL]` för länkar,
- `{note}` eller `{info}` för status-/begränsningsnotiser när lämpligt.

Pipe-tecken i cellinnehåll ska neutraliseras så att tabeller inte bryts.

## Kontaktuppgifter

Exportlagret får aldrig fylla i saknade direktuppgifter. Om kontaktresearch endast har växel eller generell kontaktväg ska exakt den verifierade fallbacken exporteras.

## Delresultat

När `run_status = partial` ska alla format uttryckligen visa:

- att exporten är ett delresultat,
- analyserat antal,
- scope-antal,
- antal kvar att analysera.

## Filnamn

Rekommenderad canonical bas:

`myndighetsteknikradarn-<slug>-<YYYY-MM-DD>`

med suffix `.md`, `.pdf` respektive `.confluence.txt`.

## Felhantering

Export ska avbrytas hellre än att generera en missvisande rapport om:

- coverage-räknarna inte reconcilerar,
- complete används trots ej analyserade myndigheter,
- obligatoriska analysfält saknas,
- kontaktuppgift markerats som direkt men inte är verifierad offentlig professionell uppgift.
