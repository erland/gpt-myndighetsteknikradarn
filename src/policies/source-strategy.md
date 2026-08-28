# Källstrategi och källspecifik tolkningspolicy

Denna policy operationaliserar steg 5 i utvecklingsplanen. Källtypernas canonical namn finns i `src/models/source-type.yaml`.

## 1. Grundregel: sök för discovery, bedöm från källan

En sökmotor är en väg till underlaget, inte underlaget i sig. Öppna och granska originalkällan när det är möjligt. En söksnippet får endast bära ett svagt discovery-spår och ska inte ensam användas för en stark positiv slutbedömning.

## 2. Prioritetsordning

Prioritera i normalfallet:

1. myndighetens egna källor och publika kod,
2. offentlig upphandling, avtal, avrop och andra offentliga dokument,
3. myndighetens egna jobbannonser,
4. professionella profiler, konferenser och presentationer,
5. leverantörers kundcase och referenser,
6. branschpress och jobbaggregatorer,
7. övrig bred webbsökning.

Prioritet betyder inte automatisk evidensstyrka. En myndighetssida som bara listar en produkt som möjlig standard kan vara svagare än ett daterat leverantörscase som beskriver en faktisk implementation. Semantiken i källan styr.

## 3. Upphandlingskällor

Svenska annonspliktiga upphandlingar annonseras i registrerade annonsdatabaser och upphandlingar över relevanta tröskelvärden publiceras normalt även i TED. Research ska därför inte vara beroende av en enda kommersiell annonsdatabas.

Sökvägar bör kunna omfatta:

- Mercell Annonsdatabas,
- e-Avrop,
- KommersAnnons.se,
- Clira Annonsdatabas,
- andra vid analystidpunkten registrerade annonsdatabaser,
- TED,
- Upphandlingsmyndighetens statistik-/informationskällor,
- Avropa/Statens inköpscentrals ramavtal,
- myndighetens egna diarier, avtalslistor, tilldelningsbeslut och upphandlingsdokument när de är publikt åtkomliga.

Källandskapet är föränderligt. Namngivna databaser ska behandlas som ett tidsstämplat seed-set, inte som en evigt komplett lista.

### Upphandlingssemantik

- **RFI/marknadsdialog:** visar sondering eller behov. Inte köp, inte drift.
- **Förhandsannons/upphandlingsannons:** visar planerad eller pågående anskaffning. Inte drift.
- **Tilldelningsbeslut/efterannons:** visar resultat/tilldelning. Starkt anskaffningsspår, men inte automatiskt implementation.
- **Avtal/avrop/beställning:** visar myndighetsspecifik anskaffning eller rätt att köpa. Starkare än annons, men kontrollera faktisk användning och giltighet.
- **Ramavtal utan myndighetsspecifikt avrop:** visar endast möjlighet att köpa och får inte räknas som myndighetsspecifikt produktbelägg.
- **Drift-, förvaltnings-, support-, migrerings- eller implementationstext:** kan ge direktare stöd för faktisk användning om myndighet och produkt är entydiga.

## 4. Jobbannonser

Klassificera formuleringen, inte bara förekomsten av produktnamnet.

Från starkare till svagare signal:

1. “vi använder X”, “vår X-miljö”, “förvalta/drifta X”,
2. rollen ska arbeta med eller vidareutveckla X i myndighetens miljö,
3. X är ett uttryckligt krav för rollen men miljökopplingen är indirekt,
4. erfarenhet av X är meriterande/önskvärd,
5. X förekommer i en generell kompetenslista eller i konsultens bakgrund utan tydlig myndighetskoppling.

Spara datum. En gammal annons kan visa historisk användning men ska inte utan stöd beskrivas som aktuell.

## 5. Professionella profiler

En offentlig professionell profil kan ge ett användbart spår men ska granskas för:

- rätt person och rätt myndighet,
- om tekniken hör till anställningen eller en tidigare roll,
- anställningens datum,
- om personen varit konsult och tekniken kan avse annan kund,
- om påståendet är självrapporterat eller verifierat på annat sätt.

Profiler ska inte användas för att samla privata kontaktuppgifter.

## 6. Leverantörskällor

Kundcase, partnercase och leverantörspresentationer kan vara konkreta men har partsintresse. Registrera dem som sådan källtyp. När de är centrala för en stark slutbedömning ska GPT:n, om rimligt, söka en myndighetskälla eller annan oberoende källa som stöd.

## 7. Branschpress

Computer Sweden, Ny Teknik och andra relevanta fackmedier kan vara bra discovery- och kontextkällor. Skillnaden mellan reportertext, sponsrat innehåll och leverantörsmaterial ska beaktas när det går att avgöra.

## 8. Publik kod

Ett officiellt repository kan visa användning av bibliotek, SDK, images, operators, konfiguration eller produktnamn. Verifiera:

- att organisationen/repositoryt faktiskt tillhör myndigheten,
- att träffen gäller målprodukten och inte bara underliggande teknik,
- aktivitet/datum,
- om repot är exempel/prototyp eller del av en verklig lösning.

Kodspår är inte automatiskt bevis för produktion.

## 9. Originalkälla och återpublicering

När samma annons, pressmeddelande eller case återpubliceras på flera webbplatser ska de behandlas som samma ursprungsuppgift. Full dedupliceringsmodell implementeras i steg 6, men redan nu gäller att antal sökträffar inte är antal oberoende källor.

## 10. Aktualitet och migreringskontroll

När enda starka belägget är gammalt ska fördjupning inkludera sökningar efter exempelvis:

- migrering,
- ersättning/replacement,
- avveckling,
- uppgradering,
- nytt ramavtal eller ny plattform,
- “från X till Y”.

Gammal användning ska vid behov beskrivas som historisk i stället för aktuell.
