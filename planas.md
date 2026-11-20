# Motociklų nuomos IS – darbo planas žingsniais

Kursinis projektas dalykui „Informacinės ir grupinio darbo sistemos“ (VU MIF, ISI, I kursas).
Užduotis: motociklų nuomos IS analizė ir projektavimas bei ataskaitos šablono užpildymas.
Laboratorinio darbo ER diagramos (`saltiniai/lab-ER-diagrama.drawio`) – idėjų šaltinis, o ne pagrindas: modelį kuriame pagal savo reikalavimus, ir jis bus sudėtingesnis nei laboratoriniame darbe.
Dėstytojo sąlyga: senas diagramas naudoti galima, bet darbo lygis turi būti aukštesnis nei laboratoriniame darbe.

Šis planas rašomas tik lietuvių kalba (nuo 2026-11-20).

## Terminas ir grafikas

Ataskaitą dėstytojui pateikti: **pirmadienį, 2026-11-23**. Po to – gynimas auditorijoje.

| Diena | Žingsniai |
|---|---|
| Tr 2026-11-18 | 1–3: dalykinė sritis, naudotojai, analogai |
| Kt 2026-11-19 | 4–7: visi reikalavimai, panaudos atvejų diagrama |
| Pn 2026-11-20 | 8–9: loginė ER, DSD, 1 kontrolinis taškas (atlikta 2026-11-18–19) |
| Š 2026-11-21 | 10–12: fizinė ER ir lentelės, struktūrinė schema, funkcijos (10–11 žingsniai atlikti 2026-11-19) |
| Sk 2026-11-22 | 13–15: dizainas, testai, Ganto diagrama; 2 kontrolinis taškas; 16 žingsnis (surinkimas) (13–14 žingsniai atlikti 2026-11-19, 15 žingsnis, 2 kontrolinis taškas ir 16 žingsnis – 2026-11-20) |
| Pr 2026-11-23 | Galutinis teksto patikrinimas ir pateikimas |

Jei vėluojame, pirmiausia supaprastiname dizaino maketus (13 žingsnis), o DSD paliekame viename lygyje.

## Kurso skaidrės pagal žingsnius (aplankas `saltiniai/paskaitu_skaidres/`)

| Žingsnis | Paskaita |
|---|---|
| 1, 15 (gyvavimo ciklas, 6 etapai) | 2 |
| 7 (panaudos atvejų diagrama) | 3 |
| 8, 10 (ER, normalizavimas) | 5 |
| 9 (DSD) | 2 |
| 11 (struktūrinė schema) | 2 (20 skaidrė), 9 (24 skaidrė – WBS, tik kaip išdėstymo pavyzdys) |
| 4–6 (reikalavimai) | 10 |
| 14 (testavimas) | 11 |
| 15 (Ganto diagrama) | 9 |
| Literatūra (neprivaloma) | `LiteraturosSarasas_IGDS_2026_GNavickas.pdf` |

## Aplanko struktūra

- `planas.md`: šis planas.
- `sprendimai.md`: sprendimų žurnalas.
- `artefaktai/`: tekstai pagal žingsnius (`01-sritis-ir-tikslai.md`, `02-vartotojai.md`, …), prie jų – `.drawio` šaltiniai ir ataskaitos PNG tuo pačiu žingsnio numeriu; `13-dizainas/` – maketai (HTML, CSS, PNG).
- `saltiniai/`: ataskaitos šablonas, laboratorinio darbo diagramos ir paskaitų skaidrės aplanke `paskaitu_skaidres/` (nekeičiame).
- `darbas/`: darbinė medžiaga (rinkos tyrimas `moto rentals LT.md`, konkurentų ekrano nuotraukos ir pan.).
- `ataskaita/`: galutinis `.docx`.

## Kaip dirbame

- Einame žingsniais iš eilės. Kiekviename žingsnyje pirmiausia aptariame, paskui rezultatą įrašome į šio projekto artefaktą.
- Visus sprendimus rašome į `sprendimai.md` (sprendimų žurnalas, rašomas tik lietuvių kalba), kad kituose žingsniuose nereikėtų ginčytis iš naujo.
- Artefaktus ir šį planą rašome lietuvių kalba, aptarimas vyksta rusų kalba.
- Reikalavimų numerius (FR 1.2.1, NFR 1.3.1.1 ir t. t.) suteikiame vieną kartą ir toliau nurodome tik juos: pagal juos susiejamos diagramos, funkcijos ir testai.
- Pabaigoje (16 žingsnis) viską surenkame į šabloną.
- Visi dokumentai suderinti tarpusavyje: bet kokio pakeitimo atveju iš karto atnaujiname visus failus, kuriuose minimas tas pats faktas (artefaktus, `planas.md`, `sprendimai.md`, `README.md`). Neatitikimų būti neturi.
- Pakeitimus į saugyklą įrašome (commit) tik Dmitrijui juos patikrinus.

## Žingsniai

### A etapas. Analizės pagrindas

**1 žingsnis. Dalykinė sritis ir sistemos ribos** → 1.1.1, 1.1.2 skyriai
- Sugalvoti užsakovo įmonę: pavadinimas, kiek filialų, kiek motociklų, kaip dabar priimamos rezervacijos (telefonu, „Excel“, popierinės sutartys) ir kokios dėl to kyla problemos.
- Suformuluoti, ką sistema daro ir ko nedaro (ko nedaro → kandidatai į 1.6).
- Suformuluoti 3–4 IS tikslus su išmatuojama nauda (mažiau rankinio darbo, nėra dvigubų rezervacijų ir pan.).
- Artefaktai: `artefaktai/01-sritis-ir-tikslai.md`, pirmieji įrašai `sprendimai.md`.

**2 žingsnis. Naudotojai** → 1.1.3
- 3 kategorijos: klientas, filialo darbuotojas, administratorius.
- Kiekvienai: uždaviniai, patirtis dalykinėje srityje, IT patirtis, papildomos savybės.
- Artefaktas: `artefaktai/02-vartotojai.md`.

**3 žingsnis. Esami sprendimai** → 1.1.4 (ir medžiaga 2.3.1)
- Analogai: gamintojas, kaina, funkcijos, privalumai ir trūkumai. Šablonas prašo 1–2, nuspręsta aprašyti 4 (žr. `sprendimai.md`).
- **Nepamiršti: surinkti konkurentų svetainių ekrano nuotraukas** į `darbas/ekrano-nuotraukos/`. Svetainių sąrašas: `darbas/moto rentals LT.md` + pasirinktas SaaS analogas. Fotografuoti: motociklų sąrašą, motociklo puslapį, paiešką ir filtrus, rezervacijos formą, asmeninę paskyrą (kur ji yra). Failo pavadinimas: `<sait>-<ekranas>.png` ir nuotraukos data, kad vėliau būtų galima pasirašyti paveikslą.
- Suformuluoti, ką darome kitaip.
- Artefaktai: `artefaktai/03-analogai.md`, `darbas/ekrano-nuotraukos/`.

### B etapas. Reikalavimai

**4 žingsnis. Funkciniai reikalavimai** → 1.2
- 4–5 reikalavimai po 1–3 sakinius, kiekvienas su numeriu FR 1.2.N (FR 1.2.1–FR 1.2.5); jei reikalavimas netelpa į 3 sakinius, skaidome jį į kelis.
- Atlikta 2026-11-18: FR 1.2.1–FR 1.2.5 faile `artefaktai/04-reikalavimai.md`.
- Patikra: kiekvienas reikalavimas turi būti matomas bent vienam vaidmeniui ir patikrinamas testu.

**5 žingsnis. Nefunkciniai reikalavimai** → 1.3
- Išvaizda 2–3, naudojimo paprastumas 2–3, veikimo charakteristikos 2–3, priežiūra 1–2, saugumas 1–2.
- Formuluotės išmatuojamos („paieška grąžina rezultatą per ≤ 2 s“), o ne „sistema patogi“.
- Atlikta 2026-11-18: NFR 1.3.1.1–NFR 1.3.5.2 (14 reikalavimų: 3/4/3/3/2) faile `artefaktai/04-reikalavimai.md`.

**6 žingsnis. Perspektyviniai reikalavimai** → 1.6
- 2–3 reikalavimai iš 1 žingsnio sąrašo „ko nedarome“.
- 4–6 žingsnių artefaktas: `artefaktai/04-reikalavimai.md` (visi reikalavimai šablono lentelių formatu).
- Atlikta 2026-11-18: PR 1.6.1–PR 1.6.3 (visi funkciniai) faile `artefaktai/04-reikalavimai.md`. 12 žingsnyje (2026-11-19) pridėtas PR 1.6.4 Nuolaidos ir kompensacijos.

### C etapas. Analizės modeliai

**7 žingsnis. Panaudos atvejų diagrama** → 1.4
- Aktoriai = 2 žingsnio vaidmenys, panaudos atvejai = funkciniai reikalavimai (+ „include“ / „extend“, kur tinka).
- Artefaktas: `.drawio` + PNG.
- Atlikta 2026-11-18: `artefaktai/07-panaudos-atvejai.drawio` + PNG (21 panaudos atvejis, „include“ / „extend“), panaudos atvejų lentelė faile `artefaktai/07-panaudos-atvejai.md`. 8 žingsnyje pridėtas PA22 „Planuoti motociklų perkėlimą“ – dabar 22 panaudos atvejai.

**8 žingsnis. Loginė ER diagrama** → 1.5.2
- Modelį kuriame pagal reikalavimus FR 1.2.1–FR 1.2.5, laboratorinis darbas – tik idėjų šaltinis: Darbuotojas, vairuotojo pažymėjimo kategorijos, techninė priežiūra, nuomos būsena ir laukai (rida ir būklė išduodant ir grąžinant), kliento kontaktai ir pan.
- Iš nefunkcinių reikalavimų: motociklo nuotrauka (NFR 1.3.1.3). Nesėkmingų prisijungimų žurnalas (NFR 1.3.5.2) iš pradžių buvo modelyje, 9 žingsnyje pašalintas: prisijungimo prie sistemos į darbą neįtraukiame.
- Žymėjimą suderinti su 5 paskaita (laboratoriniame darbe – Cheno); laboratorinio darbo pavadinimų neatitikimų neperkelti.
- Artefaktas: naujas `.drawio` + PNG aplanke `artefaktai/`.
- Atlikta 2026-11-18: `artefaktai/08-loginis-er.drawio` + PNG (Cheno žymėjimas, 15 esybių, silpnos esybės ir ryšiai, M : N; 9 žingsnyje pašalinta Prisijungimo bandymas – liko 14; 10 žingsnyje pridėti žinynai Gamintojas ir Motociklo tipas – 16), aprašymas faile `artefaktai/08-loginis-er.md`. Kartu patikslinti FR 1.2.1, FR 1.2.2, FR 1.2.4, FR 1.2.5, NFR 1.3.2.4: motociklų perkėlimas, motociklo buvimo vietos taisyklė, kiekvienos pažymėjimo kategorijos galiojimo terminas.

**9 žingsnis. Duomenų srautų diagrama (DSD)** → 1.5.1
- Žymėjimas ir lygis (nuspręsta 2026-11-18): viena „0 lygio“ diagrama su procesais, kaip dėstytojo priimtame pavyzdyje `saltiniai/lab-DSD-diagrama.png`; žymenys – pagal 2 paskaitos 22 skaidrę (stačiakampis, suapvalintas stačiakampis, cilindras), E/P/DS numeracija ir legenda – kaip pavyzdyje.
- Procesai ↔ funkciniai reikalavimai, duomenų saugyklos ↔ 8 žingsnio esybės.
- Artefaktas: `.drawio` + PNG.
- Atlikta 2026-11-19: `artefaktai/09-dsd.drawio` + PNG (3 išorinės esybės, 7 procesai, 8 duomenų saugyklos, 47 srautai; po 1 kontrolinio taško – 49), aprašymas faile `artefaktai/09-dsd.md`. Užimtumą tikrina tik P1, kiti procesai kreipiasi į jį.

**1 kontrolinis taškas.** Suderinti reikalavimus ↔ panaudos atvejus ↔ DSD ↔ ER (šablonas tiesiogiai prašo patikrinti, ar nepraleista reikalavimų). Jei reikia, grįžti prie 4–9 žingsnių.
- Atlikta 2026-11-19: ryšys Tarifas 1 : N Nuoma „įkainojama“ (tarifas pagal rezervacijos datą, panaudotas tarifas nekeičiamas; iš Nuoma pašalinti „Paros kaina“ ir „Užstatas“); išdavimo ir grąžinimo filialai pasirenkami rezervuojant (FR 1.2.2); motociklo buvimo vietos taisyklė perkėlimui (FR 1.2.5); srautai DS2 → P3 ir DS4 → P3 DSD diagramoje; Kategorija – žinynas; užimtumo tikrinimo funkcija – `tikrintiUzimtuma`. Išsamiai – `sprendimai.md`, 2026-11-19 įrašas.

### D etapas. Projektavimas

**10 žingsnis. Fizinė ER diagrama ir lentelių aprašymas** → 2.1.2, 2.2.2
- Lentelės, tipai, PK/FK/UK, NOT NULL, CHECK.
- Kiekvienos lentelės aprašymas pagal šabloną: pavadinimas ir paskirtis, atributai (pavadinimas, tipas, apribojimai).
- Savikontrolei: SQL DDL skriptas, kuris iš tikrųjų sukuria schemą (ataskaitoje neprivalomas).
- Artefaktai: `.drawio` + PNG, `artefaktai/10-lenteles.md`, `darbas/schema.sql`.
- Atlikta 2026-11-19: `artefaktai/10-fizinis-er.drawio` + PNG (varnos pėdos žymėjimas, kaip 5 paskaitos 17–20 skaidrėse; 18 lentelių, 29 ryšiai; diagramoje tik raktas PK/FK, pavadinimas ir tipas), lentelių aprašymas su apribojimais faile `artefaktai/10-lenteles.md`, `darbas/schema.sql` patikrintas su PostgreSQL 18. DBVS nepasirinkta: tik standartiniai SQL tipai. Į loginę ER pridėti žinynai Gamintojas ir Motociklo tipas, TP ir perkėlimo atributai pervadinti į „Pradžia“ / „Pabaiga“ (TIMESTAMP).
- Atlikta 2026-11-19 (po 10 žingsnio): bandomoji PostgreSQL duomenų bazė su išgalvotais duomenimis – `darbas/duomenys.sql` (generatorius `darbas/generuoti_duomenis.py`), taisyklių patikros `darbas/patikra.sql` (14 patikrų, visos 0; 12 žingsnyje – 15), `darbas/docker-compose.yml`; paleidimas aprašytas `README.md`. Naudojama 12 ir 14 žingsniuose.

**11 žingsnis. Funkcijų struktūrinė schema** → 2.1.1
- Sistemos funkcijų hierarchija (struktūrinė schema / WBS), šakos pagal posistemes.
- Suderinti su 2 paskaitos skaidrėmis.
- Artefaktas: `.drawio` + PNG.
- Atlikta 2026-11-19: `artefaktai/11-strukturine-schema.drawio` + PNG, aprašymas faile `artefaktai/11-strukturine-schema.md`. Kaip 2 paskaitos 20 skaidrėje: 0 – sistema, 1 – DSD procesai P1–P7 (su funkcinio reikalavimo numeriu), 2 – operacijos (PA, kuriuos paleidžia aktorius), 3 – kviečiamos funkcijos (PA iš „include“ / „extend“); visi 22 PA – funkcijos tais pačiais pavadinimais. Bendros funkcijos (Tikrinti motociklo užimtumą, Tikrinti vairuotojo pažymėjimą, Užfiksuoti ridą ir būklę) pakartotos prie kiekvienos jas kviečiančios operacijos ir pažymėtos dvigubomis šoninėmis linijomis; „extend“ sąlygos – laužtiniuose skliaustuose; 12 žingsnio funkcijų antroje eilutėje kursyvu – funkcijos vardas.

**12 žingsnis. Išsamus funkcijų aprašymas** → 2.2.1
- Algoritmus tikrinti užklausomis bandomojoje duomenų bazėje (`darbas/duomenys.sql`); `darbas/patikra.sql` jau turi užimtumo, motociklo buvimo vietos taisyklės, tarifo, kategorijų ir kainos skaičiavimo patikras. Kainos formulė galutinė: Galutinė kaina = planinio laikotarpio parų skaičius (suapvalintas į viršų, ≥ 1) × paros kaina + bauda (bauda – pagal pakopą).
- 2–3 funkcijos: tikrintiUzimtuma, skaiciuotiKaina, tikrintiKlientoTeise (galutinis pasirinkimas – šiame žingsnyje). tikrintiUzimtuma (pavadinimas kaip PA6 ir P1) tikrina sutapimus su nuomomis, TP ir perkėlimais bei motociklo buvimo vietos taisyklę (žr. `artefaktai/08-loginis-er.md`); tikrintiKlientoTeise – ar klientas turi modelio reikalaujamą kategoriją ir ar ji galioja visą nuomos laikotarpį (kategorijų lygių nėra); skaiciuotiKaina – bauda pagal pakopą su didžiausiu „Vėlavimas nuo (val.)“ ≤ vėlavimui (nesumuojama; iki pirmos pakopos ir be pakopų – 0).
- Kiekvienai: paskirtis, įėjimai (vardas, tipas), algoritmas (pseudokodas arba blokinė schema), išėjimas.
- Artefaktas: `artefaktai/12-funkcijos.md` (+ blokinės schemos, jei nuspręsime jas braižyti).
- Vardai `tikrintiUzimtuma`, `tikrintiKlientoTeise`, `skaiciuotiKaina` jau yra struktūrinėje schemoje (11 žingsnis); jei pasirinksime tik 2 funkcijas, trečios vardą pašalinti iš schemos ir iš `11-strukturine-schema.md`.
- Atlikta 2026-11-19: `artefaktai/12-funkcijos.md` – visos trys funkcijos (paskirtis, įėjimai, algoritmas sunumeruotais žingsniais, išėjimas, pavyzdžiai), be blokinių schemų. Patikros grąžina `uzimtas` / `turiTeise` ir priežastį (NFR 1.3.2.4); transakciją ir užraktą valdo kviečianti operacija (NFR 1.3.3.3); nuomos laikotarpis: pradžia planinė, pabaiga – grąžinimas, vykstančios nuomos – ne ankstesnė už dabartinį laiką; pavėluotas grąžinimas: išdavimas tik po grąžinimo (PA9), žymė tvarkaraštyje (PA8), rezervacijos perkėlimas, atšaukimas arba laiko keitimas (PA4, PA5). Savikontrolė: `darbas/funkcijos.sql`, `darbas/funkciju_testai.sql` (24 atvejai), `darbas/lygiagreti_rezervacija.sh`; `patikra.sql` – 15-a patikra, generatoriuje – laukusio kliento atvejis. Pridėtas perspektyvinis reikalavimas PR 1.6.4 Nuolaidos ir kompensacijos.

**13 žingsnis. Dizainas** → 2.3.1, 2.3.2
- Analogų dizaino apžvalga pagal 3 žingsnio ekrano nuotraukas (`darbas/ekrano-nuotraukos/`): kas veikia gerai, ką keisti. Jei nuotraukos 3 žingsnyje nesurinktos, pirmiausia surinkti jas čia.
- Mūsų dizaino principai: tipas, spalvų paletė, šriftai, tinklelis.
- 3–4 pagrindinių ekranų maketai (paieška ir rezervavimas klientui, išdavimas ir grąžinimas darbuotojui, parko valdymas administratoriui).
- Artefaktai: `artefaktai/13-dizainas.md`, ekranų maketai.

### E etapas. Testavimas ir terminai

**14 žingsnis. Testavimo planas** → 3.1, 3.2
- Scenarijų „Pradiniai duomenys“ imti iš bandomosios duomenų bazės (konkretūs motociklai, klientai, rezervacijos).
- 2–3 testavimo tikslai.
- Testuojamų reikalavimų lentelė (pavadinimas + numeris), įskaitant nefunkcinius (šablono 3.1.2 skyrius prašo ir tų, ir kitų).
- 3 testavimo scenarijai šablono formatu, susieti su 12 žingsnio funkcijomis (datų sutapimas, pavėluotas grąžinimas, netinkama pažymėjimo kategorija arba kategorija nustoja galioti iki nuomos pabaigos, grąžinimas į kitą filialą prieš kitą rezervaciją pradiniame filiale). Paruošti duomenys ir laukiami rezultatai – `darbas/funkciju_testai.sql` (U, K, S atvejai), dvi vienalaikės rezervacijos (NFR 1.3.3.3) – `darbas/lygiagreti_rezervacija.sh`, pavėluotas grąžinimas su laukusiu klientu – nuomos 631 ir 632.
- Artefaktas: `artefaktai/14-testavimas.md`.
- Atlikta 2026-11-19: `artefaktai/14-testavimas.md` – 3 tikslai; 3.1.2 lentelė su trečiu stulpeliu „Kaip tikrinama“ (visi funkciniai ir 13 iš 14 nefunkcinių; NFR 1.3.4.3 netestuojamas – tai priežiūros darbų tvarka, priežastis aprašyta; NFR 1.3.3.2 – naktiniai sintetiniai testai po 6 val., ≥ 99 % sėkmingų); 4 testavimo atvejai vietoj 3: TA1 rezervacijos keitimas ir TP (`tikrintiUzimtuma`, rezervacija 655), TA2 pažymėjimo kategorija (`tikrintiKlientoTeise`, klientai 26, 33, 35), TA3 pavėluotas grąžinimas ir kaina (`skaiciuotiKaina`, nuomos 631, 632), TA4 vienalaikės rezervacijos (NFR 1.3.3.3, automatizuotai). Stulpeliai „Pavyko?“ ir „Klaidos, pastabos“ tušti – sistemos nėra. Visi duomenys ir pranešimai suderinti su funkcijomis bandomojoje duomenų bazėje.

**15 žingsnis. Ganto diagrama** → 1.1.5
- Visi 6 IS gyvavimo ciklo etapai su terminais, nors aprašome tik analizę ir projektavimą.
- Darome pabaigoje, kai aiški darbų apimtis.
- Artefaktas: Ganto diagrama (PNG).
- Atlikta 2026-11-19–20: `artefaktai/15-ganto-diagrama.xlsx` (pagal pavyzdį `saltiniai/lab-GANTT-diagrama.xlsx`: sąlyginis formatavimas, ryšiai datų formulėse, kontroliniai taškai ◆ pirmą savaitę po etapo), `.png` ir aprašymas `15-ganto-diagrama.md`. Pradžia 2026-09-21 – kad 2.5 „Techninio projekto suderinimas“ sutaptų su ataskaitos pateikimo savaite 2026-11-23; programavimas iki 2027-01-31; UAT 2027-03-29 – 04-18, OAT 04-19 – 05-02; diegimas: infrastruktūra → įdiegimas su duomenų perkėlimu iš „Excel“ → mokymai (dokumentacija nuo savaitės prieš mokymus iki jų pabaigos) → paleidimas 2027-05-31 – 06-06 → priežiūra; pabaiga 2028-06-11 (90 savaičių); 6 etapai, 35 darbai, 6 kontroliniai taškai. Savos antraštės grafikas neturi: paveikslo pavadinimas – ataskaitoje.

### F etapas. Surinkimas

**2 kontrolinis taškas.** Atsekamumo matrica: reikalavimas → panaudos atvejis → DSD procesas → esybė → funkcija → testas. Patikrinti, kad niekas nekabo ore ir pavadinimai visur vienodi.
- Atlikta 2026-11-20: `artefaktai/16-atsekamumo-matrica.md` – A lentelė pagal PA1–PA22 (funkcinis reikalavimas, aktorius, procesas, duomenų saugyklos, esybės, schemos funkcija, maketas, testas), B lentelė pagal 14 nefunkcinių reikalavimų, C lentelė – atvirkštinės patikros; pavadinimai `.drawio` ir `.md` failuose ir visi skaičiai sutampa. Ištaisyta: būsena „baigta“ 13–15 žingsnių failuose, PA9 prie ekrano EKRANAS04, TA2 (1) prie FR 1.2.1 lentelėje 3.1.2. Ne visi PA tikrinami TA (šablonas prašo 3 TA) – taip ir sumanyta. A (be stulpelių „Aktoriai“ ir „Maketas“) ir B lentelės dedamos į ataskaitą kaip priedas.

**16 žingsnis. Perkėlimas į šabloną**
- Užpildyti skyrius šablono tvarka, įterpti diagramas su pavadinimais.
- Pašalinti visus kursyvu parašytus šablono nurodymus (gaires), atnaujinti turinį.
- Perskaityti ir pataisyti lietuvišką tekstą, patikrinti reikalavimų ir paveikslų numeraciją.
- Priedas „Atsekamumo matrica“: A ir B lentelės iš `artefaktai/16-atsekamumo-matrica.md`.
- Artefaktas: galutinis `.docx`.
- Atlikta 2026-11-20: ataskaita `ataskaita/MotoNuoma_IS_ataskaita.docx` ir `.pdf` (84 psl., 22 paveikslai, 72 lentelės), surenkama iš `ataskaita/ataskaita.md` (žr. `README.md`). Perskaitytas ir pataisytas lietuviškas tekstas; pataisos, liečiančios artefaktus, padarytos visuose dokumentuose. Liko: galutinė peržiūra ir pateikimas 2026-11-23.

## Priminimai

- [x] Surinkti konkurentų svetainių ekrano nuotraukas (3 žingsnis, reikia 1.1.4 ir 2.3.1 skyriams). Atlikta 2026-11-18: 10 nuotraukų aplanke `darbas/ekrano-nuotraukos/` (bikerent, kubamotors, riderent, RentSyst); 7 siauros (907 px) nufotografuotos iš naujo 2026-11-19 1512 px pločiu (13 žingsnis).

## Apipavidalinimo reikalavimai

Galioja visiems artefaktams ir galutinei ataskaitai (žr. `sprendimai.md`):
- datos lietuvišku formatu `yyyy-mm-dd`;
- diagramos simetriškos: elementai išlyginti horizontaliai ir vertikaliai;
- kiekviena diagrama ir kiekvienas paveikslas pasirašyti.

## Jei liks laiko

- Literatūros sąrašas (pagal `saltiniai/paskaitu_skaidres/LiteraturosSarasas_IGDS_2026_GNavickas.pdf`).
