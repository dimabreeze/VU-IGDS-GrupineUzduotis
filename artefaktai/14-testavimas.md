# 14. Testavimo planas ir programa

Medžiaga ataskaitos skyriams 3.1 „Testavimo apžvalga“ ir 3.2 „Testavimo atvejai“.

**Būsena:** baigta 2026-11-19. Per 2 kontrolinį tašką (2026-11-20) 3.1.2 skyriaus lentelėje prie FR 1.2.1 pridėtas TA2 1 žingsnis. 2026-11-24 pradiniai duomenys pateikti sąrašais, nurodyta, kas atlieka žingsnius; pradiniai duomenys nebesiejami su bandomosios duomenų bazės būsena; bandomieji duomenys apibrėžti 2.2.1 skyriuje, pastaba apie tuščius stulpelius perkelta į 3.2 skyrių; sąlygos po pateiktos sąrašais ir ataskaitoje perkeltos į TA lentelės paskutinę eilutę. 2026-11-25 sąlygose po nurodytos lentelės ir stulpeliai, kuriuos tikrina testuotojas (pilkoji dėžė); TA1 papildytas 9 žingsniu (paieška techninės priežiūros metu), TA sandara (aprašymas, pradiniai duomenys, žingsniai, sąlygos po) aprašyta 3.2 skyriuje sąrašu, įžangoje liko tik testavimo būdas. Papildyta 2026-11-28: TA2 papildytas 6 žingsniu (pažymėjimo tikrinimas išduodant).

Testavimas planuojamas sistemos lygiu, testavimo atvejai (TA) sudaryti pagal panaudos atvejus. Sistema tikrinama juodosios dėžės principu per sąsają, o duomenų bazėje papildomai patikrinama, kas įrašyta, – tai pilkosios dėžės testavimas. Duomenys parinkti ekvivalenčių klasių ir ribinių reikšmių metodais, ir kiekvienas TA apima ne tik tinkamus, bet ir netinkamus duomenis.

## 3.1. Testavimo apžvalga

### 3.1.1. Testavimo tikslai

1. Patikrinti, ar sistema atitinka funkcinius reikalavimus FR 1.2.1–FR 1.2.5, ypač taisykles, kurių duomenų bazės apribojimai neužtikrina: motociklo užimtumą ir buvimo vietą, vairuotojo pažymėjimo kategoriją ir jos galiojimą, galutinės kainos ir baudos skaičiavimą (2.2.1 skyriaus funkcijos).
2. Surasti defektus įvedant netinkamus ir ribinius duomenis (sutampantys ir besiliečiantys laikotarpiai, kategorija, kuri baigia galioti nuomos pabaigos dieną, vėlavimas lygiai ties baudos pakopos riba) ir patikrinti, ar sistema tokių veiksmų neleidžia ir nurodo aiškią priežastį (NFR 1.3.2.4).
3. Patikrinti nefunkcinius reikalavimus, kurių negalima patikrinti atskiromis funkcijomis: vienalaikes rezervacijas, atsako laiką ir pasiekiamumą esant 300 vartotojų, prieigą pagal vaidmenis.

### 3.1.2. Testuojamų sistemos funkcinių ir nefunkcinių reikalavimų sąrašas

Stulpelyje „Kaip tikrinama“ nurodytas testavimo atvejis (3.2 skyrius) arba testavimo rūšis, todėl kiekvienas reikalavimas susietas su jo patikrinimu.

| Reikalavimo pavadinimas | Reikalavimo Nr. | Kaip tikrinama |
|---|---|---|
| Motociklų paieška | FR 1.2.1 | Testavimas pagal panaudos atvejį PA1; paieškos rezultatai tikrinami TA1 (9 žingsnis), TA2 (1 žingsnis) ir TA4 (2 žingsnis) |
| Rezervacija ir jos valdymas | FR 1.2.2 | TA1, TA2, TA4 |
| Išdavimas ir grąžinimas | FR 1.2.3 | TA2 (6 žingsnis), TA3 |
| Techninė priežiūra | FR 1.2.4 | TA1 (7–9 žingsniai) |
| Parko administravimas ir ataskaitos | FR 1.2.5 | Testavimas pagal panaudos atvejus PA16–PA22 |
| Prisitaikanti sąsaja | NFR 1.3.1.1 | Sąsajos peržiūra 360 ir 1280 px pločio ekranuose: siaurame ekrane elementai nepersidengia ir nėra horizontalios slinkties juostos, plačiame turinys neišsitempia per visą plotį |
| Vieningas stilius | NFR 1.3.1.2 | Visų puslapių palyginimas su 2.3.2 skyriuje apibrėžta spalvų palete, šriftu ir mygtukų išdėstymu |
| Motociklo kortelė | NFR 1.3.1.3 | Paieškos rezultatų peržiūra: kiekvienam tinkamam modeliui – viena kortelė su nuotrauka, pavadinimu, tipu, variklio tūriu, galia, kategorija ir paros kaina |
| Kalbos | NFR 1.3.2.1 | Kiekviename puslapyje kalba perjungiama LT ↔ EN; įvesti formos duomenys išlieka |
| Darbuotojo mokymas | NFR 1.3.2.2 | Priėmimo bandymai: naujas darbuotojas po ne ilgesnio kaip 3 val. mokymo savarankiškai atlieka rezervaciją kliento vardu, išdavimą, grąžinimą ir techninės priežiūros planavimą |
| Trumpas rezervacijos kelias | NFR 1.3.2.3 | TA2 (4 žingsnis): nuo motociklo pasirinkimo iki patvirtinimo – 3 ekranai |
| Aiški atsisakymo priežastis | NFR 1.3.2.4 | TA1–TA4 |
| Atsako laikas | NFR 1.3.3.1 | Našumo ir apkrovos testavimas: imituojant 300 vienu metu dirbančių vartotojų, paieškos rezultatai ir rezervacijos patvirtinimas parodomi ne vėliau kaip per 2 s, kiti puslapiai – per 3 s |
| Pasiekiamumas | NFR 1.3.3.2 | Patikimumo testavimas sintetiniais testais: testavimo etape kiekvieną naktį 6 valandas kas minutę automatiškai vykdomi paieškos ir rezervacijos scenarijai, kartu imituojant 300 vienu metu prisijungusių vartotojų apkrovą; per kiekvieną naktį sėkmingų vykdymų turi būti ne mažiau kaip 99 % (iš 360 – ne daugiau kaip 3 nesėkmingi). Naktį testuojama tam, kad apkrova netrukdytų dienos testams. Metinis pasiekiamumas matuojamas tais pačiais testais sistemos veikimo ir priežiūros etape (sintetinė stebėsena) |
| Vienalaikės rezervacijos | NFR 1.3.3.3 | TA4 |
| Duomenų dubliavimas ir atsarginės kopijos | NFR 1.3.4.1 | Atkūrimo bandymas: pagrindinėje duomenų bazėje įrašyta rezervacija iš karto yra ir atsarginėje; sistema atkuriama iš paskutinės atsarginės kopijos ne ilgiau kaip per 4 val.; saugomos ne mažiau kaip 30 dienų kopijos |
| Istoriniai duomenys | NFR 1.3.4.2 | Bandoma ištrinti užbaigtą nuomą kiekvieno vaidmens paskyra – sistema neleidžia |
| Prieiga pagal vaidmenis | NFR 1.3.5.1 | TA1 (1 žingsnis): klientas mato tik savo rezervacijas |
| Duomenų apsauga | NFR 1.3.5.2 | Kreipiantis HTTP adresu naršyklė nukreipiama į HTTPS; duomenų bazėje saugoma tik slaptažodžio maiša, o ne pats slaptažodis |

**Netestuojamas reikalavimas – NFR 1.3.4.3 „Klaidų taisymas ir atnaujinimai“.** Reikalavimas nustato ne programos savybę, o priežiūros darbų tvarką: per kiek laiko ištaisomos kritinės klaidos ir kada diegiami atnaujinimai. Todėl programos testavimu jo patikrinti negalima. Jo laikymasis vertinamas sistemos veikimo ir priežiūros etape.

**Pasiekiamumas ir planiniai atnaujinimai.** NFR 1.3.3.2 neišskiria planinių atnaujinimų, kurie sezono metu diegiami 0–6 val. (NFR 1.3.4.3), todėl sintetinė stebėsena veikimo etape jų metu sistemą laiko nepasiekiama ir šios prastovos turi tilpti į leistiną 1 %. Testavimo etape atnaujinimai nediegiami, todėl naktiniams testams tai įtakos neturi.

## 3.2. Testavimo atvejai

Testavimo atvejai sudaryti ten, kur klaidos rizika didžiausia: taisyklėms, kurių duomenų bazės apribojimai neužtikrina (2.2.1 skyriaus funkcijos, TA1–TA3), ir vienalaikėms rezervacijoms (NFR 1.3.3.3, TA4), kurių rankiniu būdu patikrinti negalima. Kiekvienas TA susietas su 2.2.1 skyriaus funkcija, panaudos atvejais ir reikalavimais:

| TA | Pavadinimas | Funkcija | Panaudos atvejai | Reikalavimai |
|---|---|---|---|---|
| 1 | Rezervacijos keitimas ir techninės priežiūros planavimas | `tikrintiUzimtuma` | PA1, PA3, PA4, PA6, PA11 | FR 1.2.1, FR 1.2.2, FR 1.2.4, NFR 1.3.2.4, NFR 1.3.5.1 |
| 2 | Vairuotojo pažymėjimo tikrinimas rezervuojant ir išduodant | `tikrintiKlientoTeise` | PA1, PA2, PA4, PA7, PA9 | FR 1.2.1, FR 1.2.2, FR 1.2.3, NFR 1.3.2.3, NFR 1.3.2.4 |
| 3 | Pavėluotas grąžinimas ir galutinė kaina | `skaiciuotiKaina` | PA4, PA8, PA9, PA10, PA12, PA13, PA14 | FR 1.2.3, NFR 1.3.2.4 |
| 4 | Vienalaikės rezervacijos | `tikrintiUzimtuma` | PA1, PA2, PA6 | FR 1.2.1, FR 1.2.2, NFR 1.3.2.4, NFR 1.3.3.3 |

Kiekvienas TA pateikiamas viena lentele, kurią sudaro šios dalys:

- **„Aprašymas“** – kas tikrinama, kurios 2.2.1 skyriaus funkcijos ir reikalavimai, kokios ekvivalenčių klasės ir ribinės reikšmės.
- **„Pradiniai duomenys (sąlygos prieš)“** – kokia turi būti sistemos būsena prieš vykdant TA: dabartinis laikas, kas ir kokiu vaidmeniu atlieka žingsnius, motociklai, darbuotojai, klientai ir jų nuomos. Nurodyti tik TA svarbūs duomenys; kiti privalomi 2.2.2 skyriaus lentelių stulpeliai (pvz., VIN, telefonas, pažymėjimo numeris) užpildomi bet kokiomis tinkamomis reikšmėmis. Testuotojas prieš kiekvieną TA paruošia duomenų bazę šioje būsenoje, todėl TA galima pakartoti tomis pačiomis sąlygomis.
- **Žingsniai** – kiekvienas žingsnis yra vartotojo veiksmas sąsajoje, o po jo trumpai aprašomas laukiamas rezultatas. Laukiami pranešimai – 2.2.1 skyriaus funkcijų grąžinamos priežastys, parodomos taip, kaip 2.3.2 skyriaus maketuose. Stulpeliai „Pavyko gauti laukiamą rezultatą?“ ir „Klaidos, pastabos“ pildomi vykdant TA; sistema dar nesukurta (darbe atliekama tik analizė ir projektavimas), todėl jie palikti tušti.
- **„Sąlygos po“** (paskutinė lentelės eilutė) – kurių lentelių (2.2.2 skyrius) eilutės po TA vykdymo turi būti įrašytos ar pakeistos ir kurių neturi būti. Motociklai, klientai, darbuotojai, tarifai ir filialai nurodomi taip pat kaip pradiniuose duomenyse: motociklai – valstybiniu numeriu, klientai ir darbuotojai – numeriu, tarifai – modeliu ir paros kaina, filialai – miestu. Duomenų bazėje jie tikrinami per išorinius raktus; lentelės, į kurias šie raktai nurodo, pateikiamos skliaustuose po lentelės pavadinimo, pvz., „Nuoma“ (susijusios lentelės: „Klientas“, „Motociklas“, „Tarifas“).

### Testavimo atvejo Nr. 1

**Rezervacijos keitimas ir techninės priežiūros planavimas: motociklo užimtumas ir buvimo vieta**

**Aprašymas:** tikrinama, ar keičiant rezervaciją (PA4) ir planuojant techninę priežiūrą (PA11) sistema neleidžia laikotarpio, kuris sutampa su kitu motociklo užimtumo laikotarpiu arba pažeidžia motociklo buvimo vietos taisyklę, ir nurodo priežastį (funkcija `tikrintiUzimtuma`, PA6). Ribinės reikšmės: laikotarpis, kuris baigiasi tą pačią minutę, kai prasideda kitas, leidžiamas, o 1 min. ilgesnis – ne. Taip pat tikrinama, ar klientas mato tik savo rezervacijas ir ar techninės priežiūros metu motociklas nerodomas paieškoje (PA1). Testuojami reikalavimai FR 1.2.1, FR 1.2.2, FR 1.2.4, NFR 1.3.2.4, NFR 1.3.5.1.

**Pradiniai duomenys (sąlygos prieš):**

- Dabartinis laikas: 2026-11-19 12:00.
- Žingsnius atlieka:
  - 1–6 – Klientas 8, prisijungęs prie savo paskyros;
  - 7–9 – Klaipėdos filialo darbuotojas (Darbuotojas 6).
- Klientas 8: kategorijos A1, A2 ir A galioja iki 2033-10-13.
- Motociklas: Honda CB500 Hornet, valst. nr. 52 UVE, dabar Vilniuje.
- Kliento 8 rezervacija Nr. 655:
  - laikotarpis: 2027-05-12 10:00 – 2027-05-15 10:00 (3 paros);
  - išdavimas Vilniuje, grąžinimas Klaipėdoje;
  - tarifas: 64,00 €/para, užstatas 400,00 €.
- Kita šio motociklo nuoma – Kliento 12 rezervacija Nr. 661:
  - laikotarpis: 2027-05-24 10:00 – 2027-05-26 10:00 (2 paros);
  - išdavimas ir grąžinimas Klaipėdoje.
- Kitų šio motociklo užimtumo laikotarpių po 2027-05-12 nėra.
- Kitų Honda CB500 Hornet motociklų Klaipėdoje nėra.

| Nr. | Testavimo atvejo (scenarijaus) žingsnis | Laukiamas rezultatas | Pavyko gauti laukiamą rezultatą? (Taip/Ne) | Klaidos, pastabos |
|---|---|---|---|---|
| 1. | Klientas 8 atidaro „Mano rezervacijos“. | Rodomos tik Kliento 8 rezervacijos, tarp jų Nr. 655; Nr. 661 nėra. | | |
| 2. | Rezervacijoje Nr. 655 spaudžia „Keisti rezervaciją“, pabaigą pakeičia į 2027-05-25 10:00 ir išsaugo. | Atmesta: „Motociklas užimtas 2027-05-24 10:00 – 2027-05-26 10:00 (nuoma)“. | | |
| 3. | Pabaigą grąžina į 2027-05-15 10:00, grąžinimo filialą pakeičia į Vilnių ir išsaugo. | Atmesta: „Motociklą reikia grąžinti į filialą Klaipėda, nes 2027-05-24 10:00 ten prasideda kita jo nuoma“. | | |
| 4. | Grąžinimo filialą grąžina į Klaipėdą, išdavimo filialą pakeičia į Kauną ir išsaugo. | Atmesta: „Laikotarpio pradžioje motociklas bus filiale Vilnius“. | | |
| 5. | Išdavimo filialą grąžina į Vilnių, pabaigą pakeičia į 2027-05-24 10:01 ir išsaugo. | Atmesta: „Motociklas užimtas 2027-05-24 10:00 – 2027-05-26 10:00 (nuoma)“. | | |
| 6. | Pabaigą pakeičia į 2027-05-24 10:00 ir išsaugo. | Išsaugota; nauja kaina 12 parų × 64,00 € = 768,00 €. | | |
| 7. | Darbuotojas 6 planuoja motociklo 52 UVE techninę priežiūrą 2027-05-14 08:00 – 17:00. | Atmesta: „Motociklas užimtas 2027-05-12 10:00 – 2027-05-24 10:00 (nuoma)“. | | |
| 8. | Darbuotojas 6 planuoja priežiūrą 2027-05-27 08:00 – 17:00. | Priežiūra įrašyta. | | |
| 9. | Darbuotojas 6 ieško motociklų Klaipėdoje 2027-05-27 10:00 – 2027-05-28 10:00. | Honda CB500 Hornet kortelė nerodoma. | | |

**Sąlygos po:**

- „Nuoma“:
  - Nr. 655: „Planuojama pabaiga“ – 2027-05-24 10:00; „Planuojama pradžia“, išdavimo ir grąžinimo filialai ir tarifas nepakeisti;
  - naujų eilučių nėra.
- „Techninė priežiūra“ (susijusios lentelės: „Motociklas“, „Darbuotojas“): tik viena nauja eilutė – motociklas 52 UVE, 2027-05-27 08:00 – 17:00, suplanavo Darbuotojas 6.

### Testavimo atvejo Nr. 2

**Vairuotojo pažymėjimo tikrinimas rezervuojant ir išduodant**

**Aprašymas:** tikrinama, ar sistema leidžia rezervuoti (PA2), keisti rezervaciją (PA4) ir išduoti motociklą (PA9) tik tada, kai kliento pažymėjime yra motociklo modeliui reikalinga kategorija, galiojanti visą nuomos laikotarpį (funkcija `tikrintiKlientoTeise`, PA7), ir nurodo atsisakymo priežastį. Duomenys parinkti ekvivalenčių klasių metodu: reikiamos kategorijos nėra (turima tik žemesnė kategorija arba nėra jokios motociklų kategorijos); kategorija baigia galioti nuomos metu; kategorija galioja iki nuomos pabaigos dienos (ribinė reikšmė). Išduodant darbuotojas pataiso pažymėjimo duomenis, kurie nesutampa su kliento pateiktu pažymėjimu. Taip pat skaičiuojami ekranai nuo motociklo pasirinkimo iki patvirtinimo. Testuojami reikalavimai FR 1.2.1, FR 1.2.2, FR 1.2.3, NFR 1.3.2.3, NFR 1.3.2.4.

**Pradiniai duomenys (sąlygos prieš):**

- Dabartinis laikas: 2026-11-19 12:00 (6 žingsnio – 2027-05-09 10:00).
- Žingsnius atlieka:
  - 1 – Klientas 33, prisijungęs prie savo paskyros;
  - 2 – Vilniaus filialo darbuotojas (Darbuotojas 1);
  - 3–5 – Klientas 26, prisijungęs prie savo paskyros;
  - 6 – Vilniaus filialo darbuotojas (Darbuotojas 1).
- Motociklas: BMW F 900 R, valst. nr. 26 HUN – vienintelis šio modelio motociklas Vilniuje, laisvas 2027-05-09 10:00 – 2027-05-12 10:00.
- Modelis BMW F 900 R:
  - reikalinga kategorija: A;
  - tarifas: 100,00 €/para, užstatas 700,00 €;
  - baudų pakopos:
    - nuo 1 val. – 20,00 €;
    - nuo 3 val. – 50,00 €;
    - nuo 24 val. – 100,00 €.
- Klientas 26 (turi paskyrą):
  - kategorijos A1, A2 ir A galioja iki 2027-05-10;
  - rezervacija Nr. 642: kitas BMW F 900 R (valst. nr. 84 VZL), 2027-04-14 11:00 – 2027-04-18 11:00, išdavimas ir grąžinimas Kaune.
- Klientas 33 (turi paskyrą): tik A1 kategorija, galioja iki 2030-01-21.
- Klientas 35 (paskyros neturi): pažymėjime motociklų kategorijų nėra.

| Nr. | Testavimo atvejo (scenarijaus) žingsnis | Laukiamas rezultatas | Pavyko gauti laukiamą rezultatą? (Taip/Ne) | Klaidos, pastabos |
|---|---|---|---|---|
| 1. | Klientas 33 ieško motociklų Vilniuje 2027-05-09 10:00 – 2027-05-12 10:00, BMW F 900 R kortelėje spaudžia „Rezervuoti“, tada „Patvirtinti rezervaciją“. | Paieškos rezultatuose rodoma BMW F 900 R kortelė. Atmesta: „Vairuotojo pažymėjime nėra A kategorijos“. | | |
| 2. | Darbuotojas 1 Kliento 35 vardu rezervuoja tą patį motociklą tam pačiam laikotarpiui. | Atmesta: „Vairuotojo pažymėjime nėra A kategorijos“. | | |
| 3. | Klientas 26 atlieka tą pačią paiešką, pasirenka BMW F 900 R ir spaudžia „Patvirtinti rezervaciją“. | Atmesta: „A kategorija galioja iki 2027-05-10, o nuoma baigiasi 2027-05-12“. | | |
| 4. | Klientas 26 spaudžia „Atgal“, paieškoje nurodo grąžinimą 2027-05-10 10:00 ir rezervuoja BMW F 900 R. | Rodomas patvirtinimas: 100,00 €, užstatas 700,00 €, baudų lentelė su pakopa „iki 1 val. – 0,00 €“. Nuo motociklo pasirinkimo – 3 ekranai. | | |
| 5. | Klientas 26 puslapyje „Mano rezervacijos“ keičia rezervacijos Nr. 642 pabaigą į 2027-05-12 11:00. | Atmesta: „A kategorija galioja iki 2027-05-10, o nuoma baigiasi 2027-05-12“. | | |
| 6. | Darbuotojas 1 įformina 4 žingsnyje sukurtos rezervacijos išdavimą. Kliento 26 pateiktame pažymėjime A kategorija galioja iki 2027-05-09, todėl darbuotojas pataiso jos galiojimo datą ir spaudžia „Įforminti išdavimą“. | Atmesta: „A kategorija galioja iki 2027-05-09, o nuoma baigiasi 2027-05-10“; motociklas neišduotas. | | |

**Sąlygos po:**

- „Nuoma“ (susijusios lentelės: „Klientas“, „Motociklas“, „Tarifas“):
  - tik viena nauja eilutė – Klientas 26, motociklas 26 HUN, 2027-05-09 10:00 – 2027-05-10 10:00, „Būsena“ – „rezervuota“, tarifas – BMW F 900 R (100,00 €/para), užregistravusio darbuotojo nėra;
  - Klientų 33 ir 35 eilučių nėra;
  - Nr. 642 nepakeista („Planuojama pabaiga“ – 2027-04-18 11:00).
- „Kliento kategorija“ (susijusi lentelė: „Klientas“): Kliento 26 A kategorijos „Galioja iki“ – 2027-05-09; A1 ir A2 nepakeistos.
- „Išdavimas“: 4 žingsnyje sukurtai nuomai eilutės nėra.

### Testavimo atvejo Nr. 3

**Pavėluotas grąžinimas ir galutinė kaina**

**Aprašymas:** tikrinama, kaip sistema elgiasi, kai motociklas grąžinamas pavėluotai, o po šios nuomos jau rezervuota kita. Tvarkaraštyje (PA8) vėlavimas pažymimas; motociklo neleidžiama išduoti, kol ankstesnė nuoma negrąžinta (PA9); neleidžiama įrašyti mažesnės ridos nei išduodant (PA12); grąžinant apskaičiuojama galutinė kaina ir bauda (PA13, PA14, funkcija `skaiciuotiKaina`). Ribinė reikšmė: vėlavimas lygiai 3 val. – baudos pakopos „nuo 3 val.“ pradžia. Laukusiam klientui pakeičiama nuomos pradžia (PA4). Testuojami reikalavimai FR 1.2.3, NFR 1.3.2.4.

**Pradiniai duomenys (sąlygos prieš):**

- Dabartinis laikas: 2026-11-12 11:00.
- Žingsnius atlieka: Vilniaus filialo darbuotojas (Darbuotojas 3).
- Motociklas: BMW G 310 R, valst. nr. 82 HNU.
- Kliento 19 nuoma Nr. 631:
  - laikotarpis: 2026-11-10 10:00 – 2026-11-12 10:00 (2 paros);
  - išdavimas ir grąžinimas Vilniuje;
  - išduota 2026-11-10 10:26, rida 23 642 km;
  - būsena „aktyvi“ (motociklas dar negrąžintas).
- Klientas 22: A2 kategorija galioja iki 2038-05-22 (BMW G 310 R reikia A2).
- Kliento 22 rezervacija Nr. 632 tam pačiam motociklui:
  - laikotarpis: 2026-11-12 11:00 – 2026-11-13 13:00;
  - išdavimas ir grąžinimas Vilniuje;
  - būsena „rezervuota“.
- Abiejų nuomų tarifas:
  - 60,00 €/para, užstatas 400,00 €;
  - baudų pakopos:
    - nuo 1 val. – 10,00 €;
    - nuo 3 val. – 25,00 €;
    - nuo 24 val. – 60,00 €.

| Nr. | Testavimo atvejo (scenarijaus) žingsnis | Laukiamas rezultatas | Pavyko gauti laukiamą rezultatą? (Taip/Ne) | Klaidos, pastabos |
|---|---|---|---|---|
| 1. | 11:00 darbuotojas atidaro 2026-11-12 išdavimų ir grąžinimų tvarkaraštį. | Nr. 631 pažymėta „Vėluoja 1 val.“ su nuoroda į kitą laikotarpį (Nr. 632 nuo 11:00), Nr. 632 – „Laukia grąžinimo“. | | |
| 2. | Bando išduoti nuomą Nr. 632. | Atmesta: „Išduoti negalima, kol negrąžinta nuoma Nr. 631“; siūlomi galimi veiksmai. | | |
| 3. | Klientas 22 sutinka palaukti. 13:00 darbuotojas nuomos Nr. 631 grąžinimo formoje įveda ridą 23 600 km, būklę „Be pastabų“ ir spaudžia „Įforminti grąžinimą“. | Atmesta: „Grąžinimo rida (23 600 km) negali būti mažesnė už išdavimo ridą (23 642 km)“. | | |
| 4. | Ridą pakeičia į 24 042 km ir spaudžia „Įforminti grąžinimą“. | Galutinė kaina 145,00 € = 2 paros × 60,00 € + bauda 25,00 € (pakopa „nuo 3 val.“); grąžinti užstatą 400,00 €. | | |
| 5. | Rezervacijos Nr. 632 pradžią pakeičia į 2026-11-12 13:20. | Išsaugota; nauja kaina 1 para × 60,00 € = 60,00 €. | | |
| 6. | 13:20 įformina nuomos Nr. 632 išdavimą: rida 24 042 km, būklė „Be pastabų“. | Motociklas išduotas, nuomos būsena „aktyvi“. | | |
| 7. | 2026-11-13 12:40 įformina nuomos Nr. 632 grąžinimą: rida 24 157 km, būklė „Be pastabų“. | Galutinė kaina 60,00 €, bauda 0,00 € (grąžinta anksčiau – kaina nemažinama). | | |

**Sąlygos po:**

- „Nuoma“:
  - Nr. 631: „Būsena“ – „užbaigta“;
  - Nr. 632: „Planuojama pradžia“ – 2026-11-12 13:20, „Būsena“ – „užbaigta“.
- „Išdavimas“: nauja eilutė nuomai Nr. 632 – 2026-11-12 13:20, rida 24 042 km.
- „Grąžinimas“:
  - Nr. 631: 2026-11-12 13:00, rida 24 042 km, „Galutinė kaina“ – 145,00 €, „Bauda“ – 25,00 €;
  - Nr. 632: 2026-11-13 12:40, rida 24 157 km, „Galutinė kaina“ – 60,00 €, „Bauda“ – 0,00 €;
  - eilutės su rida 23 600 km nėra.
- „Motociklas“ 82 HNU (susijusi lentelė: „Filialas“): „Rida“ – 24 157 km, filialas – Vilnius.

### Testavimo atvejo Nr. 4

**Vienalaikės rezervacijos**

**Aprašymas:** tikrinama, ar sistema, gavusi dvi tuo pačiu metu pateiktas to paties motociklo rezervacijas sutampančiam laikotarpiui, patvirtina tik vieną, o kitam klientui praneša, kad motociklas užimtas, ir ar užimtas motociklas nebėra paieškos rezultatuose. Testas vykdomas automatizuotai: abi rezervacijos pateikiamos dviem lygiagrečiomis užklausomis, nes rankiniu būdu to paties momento pasiekti negalima. Testuojami reikalavimai FR 1.2.1, FR 1.2.2, NFR 1.3.2.4, NFR 1.3.3.3.

**Pradiniai duomenys (sąlygos prieš):**

- Dabartinis laikas: 2026-11-19 12:00.
- Žingsnius atlieka: Klientai 2 ir 3, prisijungę skirtingose naršyklėse (rezervacijas pateikia automatizuotas testas).
- Motociklas: BMW F 900 R, valst. nr. 84 VZL – vienintelis šio modelio motociklas Kaune, laisvas 2027-05-05 11:00 – 2027-05-08 11:00.
- Klientai 2 ir 3:
  - A kategorija galioja: Kliento 2 – iki 2034-11-26, Kliento 3 – iki 2034-02-26;
  - abu ieškojo motociklų Kaune šiam laikotarpiui, pasirinko BMW F 900 R ir yra rezervacijos duomenų ekrane.

| Nr. | Testavimo atvejo (scenarijaus) žingsnis | Laukiamas rezultatas | Pavyko gauti laukiamą rezultatą? (Taip/Ne) | Klaidos, pastabos |
|---|---|---|---|---|
| 1. | Abiejų klientų rezervacijos patvirtinamos tuo pačiu metu (dvi lygiagrečios užklausos „Patvirtinti rezervaciją“). | Vienam klientui rodomas patvirtinimas, kitam – „Motociklas užimtas 2027-05-05 11:00 – 2027-05-08 11:00 (nuoma)“. | | |
| 2. | Klientas, kurio rezervacija atmesta, pakartoja paiešką Kaune tam pačiam laikotarpiui. | BMW F 900 R kortelė nerodoma. | | |

**Sąlygos po:**

- „Nuoma“ (susijusios lentelės: „Motociklas“, „Klientas“):
  - motociklui 84 VZL laikotarpiui 2027-05-05 11:00 – 2027-05-08 11:00 – lygiai viena nauja eilutė, to kliento, kuris gavo patvirtinimą, „Būsena“ – „rezervuota“;
  - atmestos rezervacijos eilutės nėra.

## Savikontrolė (ataskaitoje nepateikiama)

Laukiami pranešimai 2026-11-19 sutikrinti bandomojoje duomenų bazėje: funkcijos `tikrintiUzimtuma`, `tikrintiKlientoTeise` ir `skaiciuotiKaina` (`darbas/funkcijos.sql`) su TA įėjimais grąžina būtent tuos atsakymus ir priežastis, kurie nurodyti lentelėse. TA1 7 žingsnis patikrintas po 6 žingsnio pakeitimo (rezervacija Nr. 655 iki 2027-05-24 10:00). TA1 9 žingsnis: be priežiūros motociklas 22 Klaipėdoje 2027-05-27 10:00 – 2027-05-28 10:00 laisvas, įrašius 8 žingsnio priežiūrą – „Motociklas užimtas 2027-05-27 08:00 – 2027-05-27 17:00 (techninė priežiūra)“. Bandomojoje duomenų bazėje tą dieną Klaipėdoje yra ir kiti CB500 Hornet (71 UZR, 51 SKK), todėl TA1 pradiniuose duomenyse nurodyta, kad kitų šio modelio motociklų Klaipėdoje nėra. Tais pačiais įėjimais `darbas/funkciju_testai.sql` jau yra K2 (TA2 5 žingsnis), S1 ir S2 (TA3 4 ir 7 žingsniai); kiti žingsniai tikrina tas pačias taisykles kaip U1–U3, U5, U6, K4 ir K5, bet su kitais įėjimais. TA4 atitinka `darbas/lygiagreti_rezervacija.sh` (ten – kitas motociklas ir laikotarpis). Sąsajos elgesys (tvarkaraščio žymos, ekranų skaičius, ridos patikra) bus tikrinamas tik sukūrus sistemą.
