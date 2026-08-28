# Flerpass- och återupptagningsstöd

## Problem som löses

En bred teknikresearch kan omfatta hundratals myndigheter och flera pass per myndighet. En enkel global cursor som “vi är på myndighet 87” är inte tillräcklig: positiva kandidater kan behöva fördjupas senare, ett verifieringspass kan avbrytas mitt i arbetet och ett nytt alias kan kräva återbesök av redan färdiga myndigheter.

Steg 11 inför därför två canonical objekt:

- **ResearchRun** – den samlade körningen och ett myndighetscentrerat arbetsläge.
- **ResearchCheckpoint** – ett atomiskt snapshot av hela körningen vid en bestämd tidpunkt.

## Varför myndighetscentrerat state

Varje myndighet har passstatus för screening, fördjupning, verifiering, negativ kontroll och syntes. Det går därför att återuppta en halvfärdig myndighet utan att göra om en redan slutförd myndighet.

Nästa batch härleds i första hand från tillståndet, inte från en sparad cursor. Prioriteten är:

1. påbörjat men avbrutet arbete,
2. explicit återbesök,
3. ännu inte screenade myndigheter,
4. fördjupning,
5. verifiering,
6. negativ kontroll,
7. syntes.

## Frysta snapshots

Target och scope fingerprints fryses inom ett `run_id`. Det förhindrar att ett arbete som startade som “OpenShift hos 259 myndigheter” tyst blir ett annat uppdrag efter halva analysen.

Nytt verifierat alias kan läggas till som en kontrollerad återbesökshändelse. En faktisk ändring av produktidentiteten eller myndighetsmängden kräver däremot explicit migration eller en ny körning.

## Checkpoints

Checkpoint skapas efter varje batch och alltid innan ett delresultat. Den innehåller hela validerade run-state och en SHA-256-fingerprint. En cachead rekommendation om nästa arbete följer med, men kan alltid räknas om.

Om senaste checkpointen skadats används föregående validerade checkpoint hellre än att GPT:n gissar.

## Idempotens

Resume får inte:

- duplicera evidence refs,
- köra om completed pass utan orsak,
- öppna completed myndigheter utan `revisit.required`,
- ändra gamla assessments tyst,
- räkna en avbruten myndighet som analyserad innan screeningminimum uppnåtts.

## Exempel

`examples/research-run-resume.yaml` visar fyra myndigheter:

- A är färdig och ska hoppas över,
- B avbröts mitt i deepen och ska fortsättas först,
- C väntar på negativ kontroll,
- D är ännu inte screenad.

Det deterministiska hjälpscriptet `scripts/research_state.py` väljer därför B/deepen som nästa arbete efter resume.
