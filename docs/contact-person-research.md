# Kontaktpersonsanalys

Steg 9 inför ett separat researchlager för att gå från en teknikbedömning till en praktisk kontaktväg vid en eller flera myndigheter.

## Varför separat flöde?

Teknikresearch svarar på **om en produkt sannolikt används**. Kontaktresearch svarar på **vem som sannolikt är rätt person att fråga**. Dessa är olika slutsatser och får inte blandas i samma score eller evidensmodell.

Kontaktresearch länkas därför till föregående `ResearchRun` men använder `ContactResearchRun` och `ContactCandidate`.

## Prioriteringsprincip

Första val är normalt chefsarkitekt eller enterprise-/IT-arkitekt. Men en verifierad plattforms- eller produktansvarig med uttrycklig koppling till måltekniken kan vara mer relevant än en generell arkitektchef.

Rangordningen bedömer fyra saker:

1. Är personen fortfarande vid rätt myndighet?
2. Är rollen verifierad och aktuell?
3. Är ansvarsområdet relevant för måltekniken?
4. Finns en säker offentlig professionell kontaktväg?

Punkt 4 är en sekundär faktor. En lättfunnen e-postadress gör inte en mindre relevant person till bättre kontakt.

## Kontaktuppgifter

Systemet använder endast kontaktuppgifter som uttryckligen publicerats i ett professionellt sammanhang. Det får aldrig konstruera e-postadresser från namn och domän eller härleda telefonnummer.

Om direkt kontakt saknas används myndighetens verifierade växel, kontaktformulär eller generella e-postadress.

## Standardutfall

Per myndighet visas normalt högst tre kandidater. Den bäst lämpade kan markeras som rekommenderad första kontakt. Om ingen person kan verifieras visas myndighetens officiella kontaktväg med ett förslag att fråga efter exempelvis chefsarkitekt, IT-arkitektur eller relevant plattformsansvarig.

## Aktualitet

Gamla konferens- och LinkedIn-profiler kan vara värdefulla för discovery men är inte tillräckliga för att påstå att personen fortfarande innehar samma roll. Nyare källor ska sökas, och tidigare anställda markeras `former` och rekommenderas inte som aktuell kontakt.
