# Myndighetsteknikradarn

## Mål

Bygga en GPT som evidensbaserat kan kartlägga vilka svenska myndigheter som sannolikt använder en viss produkt eller teknologi och därefter hjälpa användaren att hitta relevanta professionella kontaktpersoner.

## Primärt resultat

GPT:n ska redovisa:

- hur många myndigheter som ingick i analysunderlaget,
- hur många som faktiskt analyserades,
- hur många som har relativt trolig eller bekräftad användning,
- hur många där endast spår av möjlig användning hittades,
- hur många där inga relevanta spår hittades,
- en myndighetslista sorterad efter evidensstyrka,
- källtyper och konkreta källor bakom varje positiv bedömning,
- relevanta kontaktkandidater i en separat efterföljande analysfas.

## Distribution

Primär runtime är Chat ZIP. Custom GPT är sekundärt distributionsmål.

## Plan

Se `docs/development-plan.md`.

## Kärnflöde etablerat i steg 2

Projektets canonical runtimebeteende följer nu ett flerpassflöde: förberedelse → bred screening → evidensfördjupning → verifiering → negativ kontroll → sammanställning. Stora analyser får batchas inom samma ResearchRun och måste redovisa faktisk täckning. Detaljregler för normalisering, myndighetsuniversum, källor, evidens och scoring införs i efterföljande steg.


## Teknologinormalisering etablerad i steg 3

Varje researchuppdrag använder nu ett strukturerat `TechnologyTarget`. Exakta produktnamn, verifierade alias och versioner skiljs från produktfamilj, komponenter, underliggande teknik och andra relaterade termer. Sökexpansion får användas för att hitta källor men får inte automatiskt räknas som produktbelägg.


## Steg 4 – Myndighetsuniversum och täckning

SCB:s allmänna myndighetsregister är canonical universumkälla. Projektet har separata scope-profiler och räkneregler så att ej analyserade myndigheter aldrig blandas ihop med myndigheter där inga spår hittades.


### Steg 5: källstrategi

Projektet har canonical källtaxonomi och ett adaptivt sökflöde som prioriterar originalkällor, tolkar upphandlingsstadier och jobbannonsers formulering explicit samt tidsstämplar det svenska upphandlingslandskapets seed-källor.

### Steg 6: evidens och deduplicering

Projektet har nu en canonical `Evidence`-modell med proveniens, directness, usage semantics, färskhetsmetadata och två dedupliceringsnivåer: samma dokument/publicering samt samma underliggande claim. Återpubliceringar och derivat får inte blåsa upp antalet oberoende belägg. Motsägande evidens, exempelvis avveckling eller migrering, bevaras explicit.

## Steg 8: resultatpresentation

Projektet har nu ett canonical presentationskontrakt. Varje analys börjar med faktisk scope/täckning, följs av en rangordnad positiv myndighetslista med säkerhetsvärde och källtyper och ger därefter spårbar evidens, metodnot och aktuella begränsningar. Delresultat märks uttryckligen och får aldrig extrapoleras till ej analyserade myndigheter.

## Steg 9: kontaktpersonsanalys

Projektet har nu ett separat `ContactResearchRun` efter teknikbedömningen. Kandidater rangordnas efter aktuell verifierad roll, målteknik-/domänrelevans och källkvalitet. Chefsarkitekt, enterprise-/IT-arkitekt samt relevanta plattforms-/produktansvariga prioriteras. Direkt professionell e-post/telefon används endast när uppgiften uttryckligen är offentligt publicerad; kontaktuppgifter får aldrig gissas eller konstrueras. När direkt kontakt saknas används verifierad myndighetsväxel, kontaktformulär eller generell kontaktväg.


## Steg 10: exportformat

Projektet har nu ett gemensamt `ExportBundle` och en canonical exportpipeline för Markdown, PDF och Confluence Markup. Exporten renderar samma strukturerade `ResultPresentation` och valfri `ContactResearchRun` utan att göra ny research eller ändra scoring. Delresultat, källspårbarhet, kontaktpolicy och coverage-räknare bevaras mellan formaten.



## Steg 11 – flerpass och återupptagning

Projektet har nu canonical ResearchRun/ResearchCheckpoint, myndighetscentrerad passstatus, deterministisk nästa-batch-härledning och validerad checkpoint/resume. Se `docs/multipass-and-resume.md`.

## Steg 12 – evals och realistiska testfall

Projektet har nu en behavioral evalsvit med 18 syntetiska realistiska fall. 14 är
deterministiskt körbara och 4 är manuella runtime-evals. Sviten täcker bland annat
produktnormalisering, upphandlingsstadier, jobbannonssemantik, dubbletter, freshness,
avveckling/motsägelser, kontaktpersoner, exportparitet och flerpass-resume.

Evalsen identifierade och korrigerade ett tidigare semantiskt scoringfel: relevant stark
avveckling får inte resultera i `no_trace_found`; sådana starkt motsagda fall blir
`unresolved`.

Se `docs/evals-and-realistic-test-cases.md` och `evals/eval-manifest.yaml`.


## Steg 14 – Custom GPT-distribution

Custom GPT är sekundär runtime. Den kompilerade distributionen använder en instruktion under 8 000 tecken och 10 konsoliderade knowledge-filer. Kärnresearch och evidensmetodik har hög paritet med Chat ZIP, medan scriptstödd determinism, checkpointing och PDF-export är reducerad/villkorad. Se `docs/custom-gpt-parity.md`.


## Release candidate

Version `1.0.1` är den första stabila releasen efter slutförd utvecklingsplan steg 1–15 och godkänd RC-provning. Se `docs/stable-release.md` för releasegates och kända begränsningar.
