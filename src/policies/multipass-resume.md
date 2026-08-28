# Policy – flerpassarbete, checkpoints och återupptagning

## Syfte

Stora myndighetskartläggningar får delas upp i flera batcher och flera kontextfönster. Samma `ResearchRun` ska kunna återupptas utan att redan genomförd research försvinner, räknas två gånger eller oavsiktligt görs om.

Canonical modeller är `src/models/research-run.yaml` och `src/models/research-checkpoint.yaml`.

## En ResearchRun är den sammanhållande identiteten

Ett nytt uppdrag får ett stabilt `run_id`. Följande fryses som snapshots inom körningen:

- TechnologyTarget-identitet och `target_fingerprint`,
- myndighetsurval och `scope_fingerprint`,
- registerdatum,
- stabil ordning (`ordinal`) för alla myndigheter i scope,
- vilka pass som är obligatoriska.

Mindre metadata kan kompletteras, men ett ändrat mål eller scope får inte tyst mutera en pågående körning. Om ändringen påverkar vilka belägg eller myndigheter som hör till körningen ska den migreras explicit eller forkas till en ny ResearchRun.

## Myndighetscentrerat tillstånd

Varje myndighet i scope ska ha exakt en `AgencyWorkState`. Det är denna post – inte en global radpekare – som avgör vad som redan är gjort.

För varje myndighet sparas minst:

- processstatus,
- status per researchpass,
- evidensreferenser,
- eventuell assessmentreferens och outcome,
- om återbesök krävs och varför,
- eventuellt fel/blockering.

En påbörjad men ofullständig myndighet får ligga kvar som `in_progress`; resume ska då fortsätta det ofullständiga passet i stället för att markera myndigheten som färdig eller starta om från noll.

## Deterministisk nästa batch

Nästa arbete ska härledas från `AgencyWorkState` i denna prioritet:

1. fortsätt avbrutna `in_progress`-pass,
2. hantera explicit `revisit.required=true`,
3. kör screening för `not_started`, i stigande `ordinal`,
4. fördjupa positiva/tvetydiga kandidater som saknar deepen,
5. verifiera bärande evidens som saknar verify,
6. kör negativ kontroll där den krävs,
7. syntetisera assessments som är researchmässigt redo.

En cachead `next_work` i checkpointen är hjälpdata. Om den inte stämmer med myndighetstillstånden ska den beräknas om.

## Checkpointregler

Skapa checkpoint minst:

- efter en färdig batch,
- innan ett delresultat presenteras,
- när användaren pausar arbetet,
- före en känd kontextgräns,
- före export eller kontaktresearch om analysen ska kunna återupptas efteråt.

Checkpointen ska vara atomisk: den representerar ett fullständigt validerat run-state, inte bara senaste diffen. `state_fingerprint` ska beräknas från canonical serialisering av `run_state`.

## Resume

Vid återupptagning ska GPT:n:

1. läsa senaste validerade checkpoint,
2. verifiera schema/fingerprint och coverage-invariants,
3. verifiera att run-id, target-fingerprint och scope-fingerprint är konsistenta,
4. härleda räknare från myndighetstillstånden,
5. räkna om `next_work`,
6. fortsätta ofullständigt arbete före nya myndigheter,
7. inte göra om completed myndigheter om ingen återbesöksorsak finns.

Om checkpointen är trasig ska GPT:n hellre återgå till föregående validerade checkpoint än gissa fram saknat tillstånd.

## Idempotens och dublettskydd

- Samma `evidence_id` får inte läggas in flera gånger i en myndighets `evidence_refs`.
- Ett completed pass ska inte köras om bara för att körningen återupptas.
- Ett completed assessment får inte skrivas över tyst. Om ny evidens kräver ny bedömning ska `revisit.required=true` registreras och den nya assessmenten spåras.
- Eventlogg är append-only; resume får inte duplicera tidigare event-id.

## Räknare

Räknare i `ResearchRun` är materialiserade vyer och ska kunna räknas om från `agency_states`.

Minst följande ska alltid reconcileras:

`scoped_agency_count = analyzed_count + not_analyzed_count`

`analyzed_count = likely_count + trace_count + no_trace_count + unresolved_count`

En myndighet som bara är `in_progress` och ännu inte uppnått screeningminimum räknas fortfarande som ej analyserad.

## Delresultat

Ett delresultat ska tas från samma checkpointade run-state som senare återupptas. Presentationen får inte bli en alternativ sanning. Innan delresultat visas skapas därför checkpoint med `reason: before_partial_result`.

## Återbesök

Completed myndigheter får återöppnas endast med registrerad orsak, exempelvis:

- nytt verifierat alias,
- korrigerad målidentitet,
- falsk ekvivalens upptäckt,
- motsägande evidens,
- gammal evidens som behöver aktualitetskontroll,
- uttrycklig användarbegäran.

Återbesök ska inte nollställa gammal evidens; ny och gammal evidens ska kunna jämföras spårbart.

## Persistens i olika runtimes

I Chat ZIP är ett strukturerat checkpointobjekt den canonical återupptagningsartefakten. Om runtime kan skapa filer bör checkpoint kunna lagras som YAML eller JSON och följa med arbetsresultatet. Om runtime endast kan hålla strukturen i kontext ska samma modell ändå användas internt och återges/exporteras vid behov.

Custom GPT-distributionen ska inte lova persistens över separata chattar om plattformen inte faktiskt kan garantera det. Runtime-parity bedöms i senare steg.
