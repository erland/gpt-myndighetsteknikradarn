# Manuell evalrubrik

De manuella fallen körs mot den faktiska Chat ZIP- eller Custom GPT-runtimen i steg 13–15.
De ska inte ersättas av bedömning av en statisk mall.

## Bedömning

För varje `required`-kriterium:

- 1 = tydligt uppfyllt,
- 0,5 = delvis uppfyllt,
- 0 = inte uppfyllt.

Om ett `forbidden`-kriterium förekommer är fallet underkänt oavsett medelvärde.
Godkänt kräver minst `scoring.pass_threshold`.

## Särskilt viktiga kvaliteter

- Osäkerhet ska vara proportionerlig mot evidensen.
- Faktiskt användande får inte härledas från anskaffningsintresse ensamt.
- Frånvaro av träffar får inte beskrivas som bevis för frånvaro av teknik.
- Leverantörskällor ska identifieras som partsintresse och helst verifieras oberoende.
- Motsägande evidens ska visas, inte döljas genom summering.
- Delresultat ska tydligt visa återstående analysmängd.
- Kontaktuppgifter får aldrig konstrueras.

## Testdata

Alla namn på myndigheter och personer i eval-fixtures är syntetiska. `.invalid` används för
exempel-URL:er/e-post där så är tillämpligt.
