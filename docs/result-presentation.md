# Resultatpresentation

Steg 8 definierar ett gemensamt presentationskontrakt för teknik-/produktkartläggningar.

## Designmål

Presentationens första skärm/sida ska svara på tre frågor:

1. Hur stor del av myndighetsuniversumet analyserades?
2. Hur många myndigheter har starka respektive svaga belägg?
3. Vilka myndigheter är mest intressanta att titta vidare på?

Därefter ska användaren kunna granska varför varje myndighet rankats som den gjort.

## Lager

### Lager 1 – status och totalsiffror

Visar scope, faktisk täckning och huvudkategorier. Delresultat märks synligt.

### Lager 2 – rangordnad positiv lista

Visar `likely_or_confirmed` och `trace`, sorterat på score, evidensaktualitet och myndighetsnamn.

### Lager 3 – källor och metod

Visar konkreta evidensreferenser per positiv myndighet, sammanfattade källtyper, kort metod och relevanta begränsningar.

### Lager 4 – valbar full detalj

För stora analyser kan full evidensmatris, alla `no_trace_found` och fullständiga källistor visas eller exporteras separat. Huvudsvaret får kortas, men inte utan att märka att listan är trunkerad.

## Säkerhetsvärde

Score visas som exempelvis `78/100`. Det kallas **säkerhetsvärde** och ska aldrig presenteras som `78 % sannolikhet`.

## Delresultat

Delresultat visar både antal analyserade och antal kvarvarande nära toppen. Exempel:

> **Delresultat:** 120 av 259 myndigheter har analyserats. 139 återstår.

`no_trace_found` avser endast analyserade myndigheter.

## Fullständigt exempel

Se `examples/presentation-result.yaml`. Det kan renderas deterministiskt med `scripts/render_result.py` för att kontrollera rubrikordning, räknare och sortering.
