# Utvecklingsplan – Myndighetsteknikradarn

## 1. Målbild

Skapa en GPT som hjälper användaren att bedöma vilka svenska myndigheter som sannolikt använder en viss teknologi eller produkt, med spårbar evidens, tydlig osäkerhet och möjlighet att därefter identifiera lämpliga professionella kontaktpersoner.

GPT:n ska vara research-orienterad och kunna arbeta i flera analysomgångar när antalet myndigheter eller källor är stort.

Primär runtime: **Chat ZIP**.  
Sekundärt distributionsmål: **Custom GPT**, i den mån funktionaliteten kan bibehållas utan missvisande begränsningar.

---

## 2. Huvudsakliga användningsfall

### A. Teknologi-/produktkartläggning

Användaren anger exempelvis:

- Kubernetes
- Red Hat OpenShift
- Oracle Database
- Microsoft Power BI
- IBM MQ
- ServiceNow
- Splunk
- GitLab
- VMware
- PostgreSQL

GPT:n ska:

1. identifiera relevanta namn, produktvarianter, tidigare namn och tekniska alias,
2. fastställa vilka svenska myndigheter som ska ingå i analysen,
3. söka systematiskt i flera källtyper,
4. registrera evidens myndighet för myndighet,
5. väga evidensen,
6. presentera sammanställning och sorterad myndighetslista,
7. redovisa vilka källtyper som gav underlag,
8. redovisa hur många myndigheter som faktiskt analyserades,
9. skilja mellan stark evidens och svaga spår,
10. erbjuda fördjupning av osäkra myndigheter.

### B. Kontaktpersonsanalys

Som nästa steg ska användaren kunna be GPT:n att hitta lämpliga personer att kontakta för en vald myndighet eller för alla relevanta myndigheter.

Prioriterade roller:

1. chefsarkitekt / Chief Architect,
2. enterprise architect,
3. IT-arkitekt,
4. lösningsarkitekt,
5. plattformsansvarig,
6. produktansvarig / product owner för relevant teknikområde,
7. IT-chef / CIO / digitaliseringschef,
8. annan tekniskt relevant ansvarig.

För varje kandidat ska GPT:n visa:

- namn,
- myndighet,
- roll,
- varför personen bedöms relevant,
- direkt e-post eller telefon **endast när den är offentligt publicerad i professionellt sammanhang**,
- annars myndighetens växel eller generell kontaktväg,
- källa,
- säkerhet i att rollen fortfarande är aktuell.

GPT:n ska aldrig gissa e-postadresser eller privata telefonnummer.

---

## 3. Resultatmodell

### 3.1 Översikt

Varje kartläggning ska inledas med exempelvis:

| Mått | Antal |
|---|---:|
| Myndigheter i analysunderlaget | 220 |
| Myndigheter faktiskt analyserade | 220 |
| Relativt trolig eller bekräftad användning | 31 |
| Spår/indikationer på möjlig användning | 18 |
| Inga relevanta spår hittades | 171 |

GPT:n ska tydligt skilja mellan **inga spår hittades** och **produkten används inte**.

### 3.2 Sorterad myndighetslista

Föreslagen standardtabell:

| Myndighet | Bedömning | Säkerhet | Evidenssammanfattning | Källtyper | Senaste relevanta belägg |
|---|---|---:|---|---|---|
| Myndighet A | Bekräftad / mycket trolig | 94/100 | ... | Avtal, jobbannons, officiell tekniksida | 2026-05 |
| Myndighet B | Trolig | 78/100 | ... | Jobbannons, konferenspresentation | 2025-11 |
| Myndighet C | Spår finns | 42/100 | ... | LinkedIn-profil, sökträff | 2024-09 |

Listan sorteras efter evidensstyrka, säkrast först.

---

## 4. Evidensmodell

GPT:n bör internt använda en rikare skala än vad som visas i sammanfattningen.

### Nivå 5 – Direkt bekräftat

Exempel:

- myndigheten beskriver själv produkten som en del av sin miljö,
- aktuellt avtal eller tilldelningsbeslut visar produkten,
- teknisk dokumentation eller publikt repo visar faktisk drift/användning,
- myndighetens egen presentation anger att tekniken används.

### Nivå 4 – Mycket stark indikation

Exempel:

- aktuell jobbannons kräver erfarenhet av produkten och beskriver myndighetens befintliga miljö,
- flera oberoende starka källor pekar på aktuell användning,
- leverantörens kundcase beskriver konkret implementation och kan kopplas till myndigheten.

### Nivå 3 – Trolig

Exempel:

- en eller flera relativt starka indirekta källor,
- upphandling eller avrop som starkt antyder användning men där faktisk implementation inte kan säkerställas,
- återkommande aktuella jobbannonser för samma teknik.

### Nivå 2 – Spår/indikation

Exempel:

- offentlig yrkesprofil där en person kopplar tekniken till arbete vid myndigheten,
- äldre jobbannons,
- tidningsartikel,
- konferensprogram,
- tekniskt dokument där användningsstatusen är oklar.

### Nivå 1 – Svagt spår

Exempel:

- enstaka sökträff,
- aggregator,
- svårtolkad snippet,
- indirekt leverantörsreferens.

### Nivå 0 – Inga relevanta belägg hittades

Detta betyder inte att tekniken saknas.

---

## 5. Poängmodell

Poängen ska inte vara en enkel summering av antal träffar. Föreslagen modell:

**Grundstyrka per evidenspost**

- Officiell direkt källa: 35–50
- Avtal/tilldelning med tydlig produktkoppling: 30–45
- Officiell jobbannons: 20–35
- Leverantörens namngivna kundcase: 20–35
- Professionell profil / konferensprofil: 10–25
- Etablerad branschpress: 10–20
- Övrig webbindikation: 3–10

**Modifierare**

- + aktualitet,
- + flera oberoende källtyper,
- + uttrycklig formulering att produkten används,
- + samma produkt i flera år eller sammanhang,
- – gammal källa,
- – formulering av typen “meriterande kunskap” utan koppling till befintlig miljö,
- – upphandling som bara visar avsikt,
- – sekundär eller återpublicerad källa,
- – träff som kan avse konsultens tidigare arbetsgivare.

Poängen begränsas till 0–100.

Poängen ska alltid kompletteras med en verbal bedömning.

---

## 6. Sammanfattningskategorier

För användarens huvudresultat används:

### Relativt trolig eller bekräftad användning

Omfattar evidensnivå 3–5.

### Spår av möjlig användning

Omfattar evidensnivå 1–2.

### Inga relevanta spår hittades

Evidensnivå 0.

Detta ger de två positiva grupper som efterfrågats, samtidigt som GPT:n kan visa mer nyanserad säkerhet i detaljlistan.

---

## 7. Källstrategi

### Prioritet 1 – Myndighetens egna källor

- myndighetens webbplats,
- tekniska rapporter,
- arkitekturdokument,
- årsredovisningar,
- regeringsuppdrag och redovisningar,
- öppna data,
- publika GitHub/GitLab-repon,
- pressmeddelanden,
- presentationer,
- jobbannonser,
- kontakt- och organisationssidor.

### Prioritet 2 – Offentlig upphandling och avtal

- TED,
- Mercell,
- e-Avrop,
- KommersAnnons,
- Clira,
- avropa.se / Statens inköpscentral,
- myndigheters avtals- och diariedokument,
- tilldelningsbeslut,
- RFI,
- RFP/upphandlingsunderlag,
- förfrågningsunderlag,
- avropsunderlag.

Viktigt: en upphandling visar inte automatiskt faktisk användning. GPT:n ska skilja på planerad anskaffning, genomförd tilldelning och belagd drift.

### Prioritet 3 – Rekryteringskällor

- myndighetens egen karriärsida,
- Arbetsgivarverket / statliga jobbkällor,
- LinkedIn Jobs,
- andra jobbaggregatorer som sökindex.

Jobbannonser är ofta starka tekniksignaler, men GPT:n ska analysera formuleringarna:
“vi använder X” är starkare än “erfarenhet av X är meriterande”.

### Prioritet 4 – Professionella profiler och presentationer

- offentligt synliga LinkedIn-profiler,
- konferenstalare,
- seminarier,
- meetups,
- webinarier,
- publika presentationer,
- branschorganisationer.

### Prioritet 5 – Leverantörskällor

- kundcase,
- referenskunder,
- partnercase,
- pressmeddelanden,
- webinarier,
- konferenspresentationer.

Leverantörskällor ska markeras som partsintresse och helst verifieras med annan källa.

### Prioritet 6 – Branschpress

Exempel:

- Computer Sweden,
- Ny Teknik,
- Voister,
- IDG-relaterade publikationer,
- CIO Sweden,
- andra relevanta fackmedier.

### Prioritet 7 – Bred webbsökning

Google-/webbsökning används för att hitta källorna ovan och för kompletterande indikationer.

Sökresultat/snippets ska inte ensamma klassificeras som stark evidens när originalkällan kan granskas.

---

## 8. Sökstrategi per produkt

Innan myndigheter analyseras ska GPT:n skapa ett söklexikon.

Exempel för Red Hat OpenShift:

- "OpenShift"
- "Red Hat OpenShift"
- "OpenShift Container Platform"
- "OCP"
- relevanta versionsnamn
- eventuella tidigare produktnamn
- relaterade men **inte likvärdiga** begrepp som Kubernetes

GPT:n ska separera:

- exakt produktträff,
- produktfamilj,
- underliggande teknik,
- alternativ/konkurrent,
- allmän kompetens.

Det förhindrar att exempelvis “Kubernetes” felaktigt räknas som bevis för “OpenShift”.

---

## 9. Flerstegsanalys för stora mängder myndigheter

### Pass 1 – Inventering och bred screening

- skapa myndighetsuniversum,
- gör begränsad bred sökning per myndighet,
- samla positiva kandidater,
- registrera även att myndigheten screenats utan träff.

### Pass 2 – Evidensfördjupning

Fördjupa:

- alla positiva kandidater,
- större IT-intensiva myndigheter,
- myndigheter där endast svaga träffar hittats.

### Pass 3 – Verifiering

- kontrollera originalkällor,
- deduplicera samma uppgift som återpublicerats,
- kontrollera datum,
- skilj anskaffning från faktisk användning,
- identifiera motsägelser.

### Pass 4 – Negativ kontroll

För myndigheter där inga spår hittats:

- gör minst en alternativ sökning,
- använd produktalias,
- kontrollera minst en relevant myndighetsspecifik källa där det är rimligt.

### Pass 5 – Sammanställning

- beräkna bedömning,
- skapa listan,
- sortera efter säkerhet,
- redovisa täckningsgrad.

GPT:n ska kunna pausa presentationen mellan passen om analysmängden blir för stor, men behålla ett strukturerat arbetsunderlag så att nästa prompt kan fortsätta från föregående pass.

---

## 10. Myndighetsuniversum

Projektet ska innehålla en metod för att skapa och underhålla en baslista över svenska statliga myndigheter.

Varje körning ska redovisa:

- antal myndigheter i baslistan,
- antal som ingick i aktuell avgränsning,
- antal som faktiskt analyserades,
- eventuella myndigheter som utelämnades och varför.

Baslistan ska inte vara hårdkodad som evigt sann; den behöver kunna uppdateras.

---

## 11. Kontaktpersonsflöde

Kontaktpersonsanalysen körs som ett separat steg efter teknikbedömningen.

### Sökord för roller

Exempel:

- chefsarkitekt
- chief architect
- enterprise architect
- enterprise-arkitekt
- IT-arkitekt
- it arkitekt
- lösningsarkitekt
- solution architect
- infrastrukturarkitekt
- plattformsarkitekt
- CIO
- IT-chef
- digitaliseringschef
- produktägare
- produktansvarig

Kombinera med myndighet och aktuell produkt/teknik.

### Kontaktkällor

Prioritering:

1. myndighetens kontaktsida/personsida,
2. myndighetens press- eller organisationssida,
3. offentliga konferens-/talarsidor,
4. offentliga professionella profiler,
5. publika dokument,
6. branschpress.

### Standardresultat

| Person | Roll | Myndighet | Relevans | Kontakt | Kontaktform | Säkerhet | Källa |
|---|---|---|---|---|---|---|---|

Om direkt kontaktuppgift saknas:

> Direkt professionell kontaktuppgift hittades inte. Kontakta myndighetens växel: XX-XXX XX XX.

---

## 12. Spårbarhetskrav

Varje positiv bedömning ska kunna härledas till minst en konkret källa.

För varje evidenspost lagras:

- myndighet,
- produkt/teknik,
- produktvariant,
- källa,
- URL,
- källtyp,
- publiceringsdatum om känt,
- åtkomstdatum,
- kort evidenssammanfattning,
- direkt/indirekt evidens,
- styrka,
- eventuell varning,
- vilka andra evidensposter den stöder eller duplicerar.

GPT:n ska undvika långa citat och primärt sammanfatta belägget.

---

## 13. Hantering av tid

Teknikmiljöer förändras.

GPT:n ska därför:

- visa datum för varje viktig källa,
- väga ned äldre belägg,
- markera när enda evidensen är gammal,
- kunna skilja “har använt” från “använder sannolikt nu”,
- söka efter tecken på avveckling/migrering när stark äldre evidens hittas.

---

## 14. Export

Efter presentationen ska GPT:n erbjuda:

- Markdown (`.md`)
- PDF (`.pdf`)
- Confluence Markup (`.txt` eller `.confluence`)

Exporten ska inkludera:

1. sökt produkt/teknik,
2. analystidpunkt,
3. analysomfattning,
4. sammanfattande antal,
5. metod,
6. evidensskala,
7. sorterad myndighetslista,
8. källor per myndighet,
9. kontaktpersoner om det steget genomförts,
10. begränsningar och osäkerheter.

PDF ska vara läsbar som fristående rapport.

---

## 15. Rekommenderad GPT-arkitektur

### Canonical project

Projekt-ZIP med:

- `gpt-project.yaml`
- `project-status.yaml`
- `PROJECT.md`
- `STATUS.md`
- `docs/development-plan.md`
- canonical instructions
- policies
- schemas
- templates
- scripts
- tests/evals

### Chat ZIP runtime

Bör innehålla:

- instruktioner,
- researchpolicy,
- evidenspolicy,
- kontaktpersonspolicy,
- källstrategi,
- myndighetsbas/uppdateringsmetod,
- schemas för analysdata,
- rapportmallar,
- exportmallar,
- eventuella scripts för sammanställning, scoring och export.

### Custom GPT

Byggs som separat distribution.

Om Custom GPT-runtime inte kan ge samma robusta flerpassanalys eller artefakthantering ska skillnaden dokumenteras tydligt.

---

## 16. Föreslagna strukturerade datamodeller

Projektet bör ha schemas för minst:

### TechnologyTarget

- canonical_name
- aliases
- vendor
- product_family
- related_but_not_equivalent_terms
- exclusions

### Agency

- name
- organization_number
- type
- website
- active

### Evidence

- agency
- technology
- source_type
- source_url
- source_date
- retrieved_date
- evidence_text
- directness
- strength
- freshness
- duplicate_group
- notes

### AgencyAssessment

- agency
- score
- evidence_level
- display_category
- rationale
- evidence_ids
- source_types
- latest_evidence
- caveats

### ContactCandidate

- name
- agency
- role
- relevance
- public_email
- public_phone
- switchboard
- source
- role_freshness
- confidence

### ResearchRun

- target
- started_at
- agency_universe_count
- scoped_agency_count
- analyzed_count
- likely_count
- trace_count
- no_trace_count
- incomplete_count
- passes_completed

---

## 17. Testfall som bör ingå

Minst följande evals:

1. etablerad produkt med många tydliga myndighetsspår,
2. nischad produkt med få träffar,
3. generisk teknik som Kubernetes,
4. produkt med många alias,
5. produkt där upphandling finns men användning inte är belagd,
6. produkt med endast gamla belägg,
7. produkt med leverantörscase men ingen myndighetskälla,
8. samma uppgift återpublicerad på många webbplatser,
9. jobbannons där tekniken endast är “meriterande”,
10. jobbannons som uttryckligen beskriver befintlig miljö,
11. myndighet med motstridiga uppgifter,
12. kontaktperson som bytt arbetsgivare,
13. ingen direkt kontaktperson hittas – korrekt fallback till växel,
14. export till Markdown,
15. export till PDF,
16. export till Confluence Markup,
17. avbruten flerpassanalys som återupptas korrekt,
18. redovisning av faktisk analycoverage.

---

# Steg-för-steg-plan

## Steg 1 – Projektgrund och målmodell

Skapa canonical projektstruktur, `gpt-project.yaml`, projektstatus, projektbeskrivning och denna utvecklingsplan.

**Klart när:** projektet kan valideras strukturellt och nästa steg kan härledas från projektstatus.

## Steg 2 – Kärninstruktion och researchflöde

Implementera huvudbeteendet för teknik-/produktkartläggning och flerpassanalys.

**Klart när:** GPT:n kan beskriva och följa ett konsekvent end-to-end-flöde.

## Steg 3 – Teknologinormalisering

Implementera modell och instruktioner för produktnamn, alias, produktfamiljer och falska ekvivalenser.

**Klart när:** GPT:n kan skilja exakta produktbelägg från relaterad teknik.

## Steg 4 – Myndighetsuniversum och täckningsmodell

Implementera basmodell för svenska myndigheter och regler för hur analysomfattning och faktisk täckning redovisas.

**Klart när:** varje analys kan säga exakt hur många myndigheter som ingick och analyserades.

## Steg 5 – Källstrategi och sökplaner

Implementera källhierarki, sökmönster och källspecifika tolkningsregler.

**Klart när:** GPT:n systematiskt kan söka flera källtyper och prioritera originalkällor.

## Steg 6 – Evidensschema och deduplicering

Skapa schemas och regler för evidensposter, källdeduplicering, direkthet och aktualitet.

**Klart när:** samma underliggande belägg inte felaktigt räknas som flera oberoende källor.

## Steg 7 – Scoring och säkerhetsklassning

Implementera poängmodell, evidensnivåer och roll-up till “relativt trolig” respektive “spår”.

**Klart när:** sorteringsordningen blir reproducerbar och motiverad.

## Steg 8 – Resultatpresentation

Skapa standardmallar för sammanfattning, myndighetslista, metodnot och källredovisning.

**Klart när:** resultatet är kortfattat i toppen men fullt spårbart i detaljerna.

## Steg 9 – Kontaktpersonsanalys

Implementera separat researchflöde för ansvariga arkitekter och andra relevanta IT-roller, inklusive fallback till växel.

**Klart när:** GPT:n kan rangordna kontaktkandidater utan att gissa kontaktuppgifter.

## Steg 10 – Exportformat

Implementera Markdown-, PDF- och Confluence Markup-export.

**Klart när:** samma analys kan exporteras konsekvent till alla tre formaten.

## Steg 11 – Flerpass- och återupptagningsstöd

Implementera strukturerat arbetsläge för stora analyser som kräver flera researchomgångar.

**Klart när:** ett avbrutet arbete kan fortsätta utan att redan analyserade myndigheter tappas eller räknas om felaktigt.

## Steg 12 – Evals och realistiska testfall

Skapa automatiska och manuella evals för evidensklassning, källtolkning, scoring, kontaktpersoner och export.

**Klart när:** centrala felscenarier fångas.

## Steg 13 – Chat ZIP runtime

Bygg den fullständiga runtime-distributionen för användning direkt i ChatGPT-konversation.

**Klart när:** Chat ZIP innehåller endast runtime-relevanta filer och passerar validering.

## Steg 14 – Custom GPT-distribution och paritybedömning

Bygg Custom GPT-varianten och dokumentera eventuella skillnader mot Chat ZIP.

**Klart när:** användaren vet vilka funktioner som är identiska, reducerade eller olämpliga i Custom GPT.

## Steg 15 – Slutvalidering, hygiene och release candidate

Kör lint, evals, distributionsvalidering, project hygiene och release-readiness.

**Klart när:** inga blockerande fel återstår och en komplett RC-projekt-ZIP kan levereras.

---

## Rekommenderat nästa steg

Genomför **Steg 1 – Projektgrund och målmodell** och leverera den första kompletta projekt-ZIP:en.

Föreslaget arbetsnamn: **Myndighetsteknikradarn**.
