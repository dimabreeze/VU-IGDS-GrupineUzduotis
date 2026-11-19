# 16. Atsekamumo matrica (2 kontrolinis taškas)

Medžiaga ataskaitos priedui „Atsekamumo matrica“ (šablone tokio skyriaus nėra; sutrumpinta lentelė pridedama surenkant ataskaitą, žr. skyrių „Kas perkeliama į ataskaitą“).

**Būsena:** baigta 2026-11-20.

Matrica rodo, kaip kiekvienas reikalavimas (`04-reikalavimai.md`) susijęs su panaudos atvejais (`07-panaudos-atvejai.md`), duomenų srautų diagramos procesais ir saugyklomis (`09-dsd.md`), ER esybėmis ir lentelėmis (`08-loginis-er.md`, `10-lenteles.md`), struktūrinės schemos funkcijomis (`11-strukturine-schema.md`, `12-funkcijos.md`), sąsajos maketais (`13-dizainas.md`) ir testavimu (`14-testavimas.md`). Ja patikrinta, ar kiekvienas elementas susietas su kitais ir ar pavadinimai visur vienodi.

## A. Funkciniai reikalavimai ir panaudos atvejai

Aktoriai: K – klientas, D – filialo darbuotojas, A – administratorius. Saugyklose: R – skaito, W – rašo; „per P1“ – duomenis procesas gauna iš P1 (užimtumo tikrinimas, PA6). Schemos funkcija: lygis (2 – operacija, 3 – iškviečiama funkcija), rodyklė – kviečiamos funkcijos, pasviru šriftu – 2.2.1 skyriaus funkcija. Testavimas: TA ir žingsniai (3.2 skyrius) arba „pagal PA“ – testavimas pagal panaudos atvejį be atskiro TA (3.1.2 skyrius).

| PA | Panaudos atvejis | Akt. | Procesas | Saugyklos | ER esybės | Schemos funkcija | Maketas | Testavimas |
|---|---|---|---|---|---|---|---|---|
| | **1.2.1 Motociklų paieška** | | | | | | | |
| PA1 | Ieškoti laisvų motociklų | K, D | P1 | DS1, DS2, DS3 R; DS5–DS7 R (PA6) | Filialas, Motociklas, Motociklo modelis, Motociklo tipas, Kategorija, Tarifas | 2 → PA6 | E1 | TA2 (1), TA4 (2) |
| | **1.2.2 Rezervacija ir jos valdymas** | | | | | | | |
| PA2 | Rezervuoti motociklą | K, D | P2 | DS4 R/W, DS5 W; DS3 per P1 | Klientas, Kategorija („turi teisę“), Nuoma, Tarifas, Baudos pakopa, Filialas, Darbuotojas | 2 → PA6, PA7 | E2, E3 | TA2 (4), TA4 (1) |
| PA3 | Peržiūrėti savo rezervacijas | K | P2 | DS5 R | Nuoma | 2 | – | TA1 (1) |
| PA4 | Keisti rezervaciją | K, D | P2 | DS4 R, DS5 R/W | Nuoma, Klientas, Kategorija („turi teisę“) | 2 → PA6, PA7 | – | TA1 (2–6), TA2 (5), TA3 (5) |
| PA5 | Atšaukti rezervaciją | K, D | P2 | DS5 W | Nuoma | 2 | – | pagal PA |
| PA6 | Tikrinti motociklo užimtumą | – | P1 | DS2, DS5, DS6, DS7 R | Motociklas, Filialas, Nuoma, Techninė priežiūra, Perkėlimas | 3, *tikrintiUzimtuma* | E2 (atmetimas) | TA1 (2–8), TA4 (1) |
| PA7 | Tikrinti vairuotojo pažymėjimą | – | P2 | DS4 R; reikiama kategorija per P1 | Klientas, Kategorija („turi teisę“), Motociklo modelis | 3, *tikrintiKlientoTeise* | E2 (atmetimas) | TA2 (1–5) |
| | **1.2.3 Išdavimas ir grąžinimas** | | | | | | | |
| PA8 | Peržiūrėti išdavimų ir grąžinimų tvarkaraštį | D | P3 | DS2, DS4, DS5 R | Nuoma, Motociklas, Klientas | 2 | E4 | TA3 (1) |
| PA9 | Įforminti išdavimą | D | P3 | DS5 R/W | Išdavimas, Nuoma, Darbuotojas | 2 → PA12 | E4 | TA3 (2, 6) |
| PA10 | Įforminti grąžinimą | D | P3 | DS3 R, DS5 W, DS2 W | Grąžinimas, Nuoma, Darbuotojas | 2 → PA12, PA13, PA14 [grąžinta pavėluotai], PA15 [kitas filialas] | E4 | TA3 (3, 4, 7) |
| PA12 | Užfiksuoti ridą ir būklę | – | P3 | DS5 W, DS2 W | Išdavimas, Grąžinimas, Motociklas (Rida) | 3 | E4 | TA3 (3, 4, 6, 7) |
| PA13 | Apskaičiuoti galutinę nuomos kainą | – | P3 | DS3 R, DS5 W | Tarifas, Nuoma, Grąžinimas (Galutinė kaina) | 3, *skaiciuotiKaina* | E4 | TA3 (4, 7) |
| PA14 | Apskaičiuoti baudą už pavėluotą grąžinimą | – | P3 | DS3 R, DS5 W | Baudos pakopa, Grąžinimas (Bauda) | 3 [grąžinta pavėluotai] | E4 | TA3 (4) |
| PA15 | Grąžinti į kitą filialą | – | P3 | DS2 W | Motociklas, Filialas (ryšys „yra“) | 3 [kitas filialas] | – | pagal PA |
| | **1.2.4 Techninė priežiūra** | | | | | | | |
| PA11 | Planuoti techninę priežiūrą | D | P4 | DS6 W | Techninė priežiūra, Motociklas, Darbuotojas | 2 → PA6 | – | TA1 (7–8) |
| | **1.2.5 Parko administravimas ir ataskaitos** | | | | | | | |
| PA16 | Tvarkyti filialus | A | P5 | DS1 W | Filialas | 2 | – | pagal PA |
| PA17 | Tvarkyti motociklų modelius ir motociklus | A | P5 | DS2 W | Motociklo modelis, Motociklas, Gamintojas, Motociklo tipas | 2 | – | pagal PA |
| PA18 | Tvarkyti tarifus | A | P5 | DS3 W | Tarifas, Baudos pakopa | 2 | – | pagal PA |
| PA19 | Tvarkyti darbuotojų paskyras | A | P5 | DS8 R/W | Darbuotojas, Paskyra | 2 | – | pagal PA |
| PA20 | Peržiūrėti parko užimtumą | A | P7 | per P1 (DS5–DS7) | Nuoma, Techninė priežiūra, Perkėlimas, Motociklas | 2 | E5 | pagal PA |
| PA21 | Formuoti statistines ataskaitas | A | P7 | per P1 (DS5) | Nuoma, Grąžinimas | 2 | – (turinys nenustatytas) | pagal PA |
| PA22 | Planuoti motociklų perkėlimą | A | P6 | DS7 W, DS2 W | Perkėlimas (ryšys „perkeliamas“), Motociklas, Filialas, Darbuotojas | 2 → PA6 | – | pagal PA |

Ne kiekvienam panaudos atvejui sudarytas atskiras testavimo atvejis: šablonas prašo 3 testavimo atvejų, todėl jie parinkti svarbiausioms taisyklėms (2.2.1 skyriaus funkcijoms) ir vienam nefunkciniam reikalavimui (1.3.3.3). Kiti panaudos atvejai tikrinami testavimu pagal panaudos atvejus (3.1.2 skyrius).

## B. Nefunkciniai reikalavimai

| Reikalavimas | Kur atsispindi projekte | Kaip tikrinama (3.1.2) |
|---|---|---|
| 1.3.1.1 Prisitaikanti sąsaja | 2.3.2 „Tinklelis ir išdėstymas“; E1 360 ir 1280 px | Peržiūra 360 ir 1280 px pločio ekranuose |
| 1.3.1.2 Vieningas stilius | 2.3.2: paletė, šriftas, mygtukai; vienas stiliaus failas | Puslapių palyginimas su 2.3.2 |
| 1.3.1.3 Motociklo kortelė | Motociklo modelis (Nuotrauka, charakteristikos), Motociklo tipas, Kategorija, Tarifas (Paros kaina); E1 | Paieškos rezultatų peržiūra |
| 1.3.2.1 Kalbos | Perjungiklis LT \| EN visuose ekranuose | Kalbos perjungimas kiekviename puslapyje |
| 1.3.2.2 Darbuotojo apmokymas | Darbuotojo operacijos PA2, PA9, PA10, PA11; E4; mokymai (Ganto diagrama, 5.4) | Priėmimo bandymai |
| 1.3.2.3 Trumpas rezervacijos kelias | E1 → E2 → E3 | TA2 (4) |
| 1.3.2.4 Aiški atsisakymo priežastis | *tikrintiUzimtuma* ir *tikrintiKlientoTeise* grąžina priežastį; E2 (atmetimas), E4 (įspėjimas) | TA1–TA4 |
| 1.3.3.1 Atsako laikas | Užraktas laikomas tik transakcijos metu (`12-funkcijos.md`) | Našumo ir apkrovos testavimas |
| 1.3.3.2 Pasiekiamumas | Sintetinė stebėsena veikimo etape (Ganto diagrama, 6.3) | Naktiniai sintetiniai testai |
| 1.3.3.3 Vienalaikės rezervacijos | Operacijos PA2, PA4, PA11, PA22 užrakina motociklą prieš *tikrintiUzimtuma* | TA4 |
| 1.3.4.1 Duomenų dubliavimas ir atsarginės kopijos | Gamybinė infrastruktūra ir atkūrimo patikra (Ganto diagrama, 5.1, 6.4) | Atkūrimo bandymas |
| 1.3.4.2 Istoriniai duomenys | Nuoma, Išdavimas, Grąžinimas netrinami; nuomos būsena „užbaigta“ (`08`, `10`) | Bandymas ištrinti užbaigtą nuomą |
| 1.3.4.3 Klaidų taisymas ir atnaujinimai | Garantinė priežiūra (Ganto diagrama, 6.1) | Netestuojamas – priežiūros darbų tvarka, ne programos savybė |
| 1.3.5.1 Prieiga pagal vaidmenis | Paskyra (Vaidmuo) | TA1 (1) |
| 1.3.5.2 Duomenų apsauga | Paskyra (Slaptažodžio maiša); HTTPS (Ganto diagrama, 3.6, 5.1) | HTTPS nukreipimo ir maišos patikra |

## C. Atvirkštinė patikra

| Kas tikrinta | Rezultatas |
|---|---|
| Kiekvienas funkcinis reikalavimas 1.2.1–1.2.5 turi panaudos atvejį, procesą, esybę ir patikrą | Taip (A lentelė) |
| Kiekvienas nefunkcinis reikalavimas turi patikrą | Taip, išskyrus 1.3.4.3 (priežastis – `14-testavimas.md`) |
| Kiekvienas panaudos atvejis PA1–PA22 turi reikalavimą, procesą ir struktūrinės schemos funkciją tuo pačiu pavadinimu | Taip (22 iš 22) |
| Kiekvienas «include» ir «extend» ryšys atitinka iškvietimą struktūrinėje schemoje | Taip (PA6 – 5 kartus, PA7 – 2, PA12 – 2, PA13, PA14, PA15 – po 1) |
| Kiekvienas procesas P1–P7 turi panaudos atvejį ir šaką struktūrinėje schemoje | Taip |
| Kiekviena saugykla DS1–DS8 turi rašantį ir skaitantį procesą | Taip; Kategoriją (DS2) joks procesas nerašo, nes tai klasifikatorius, įvedamas diegiant sistemą |
| Kiekviena esybė (16) ir lentelė (18) priklauso saugyklai ir reikalavimui | Taip (`08` aprėpties lentelė, `10` „Ryšys su loginiu modeliu…“) |
| Kiekviena 2.2.1 skyriaus funkcija turi panaudos atvejį ir testavimo atvejį | Taip: *tikrintiUzimtuma* – PA6, TA1, TA4; *tikrintiKlientoTeise* – PA7, TA2; *skaiciuotiKaina* – PA13, PA14, TA3 |
| Kiekvienas testavimo atvejis susietas su panaudos atvejais ir reikalavimais | Taip (TA1–TA4) |
| Kiekvienas maketas E1–E5 susietas su panaudos atvejais ir reikalavimais | Taip |
| Perspektyviniai reikalavimai 1.6.1–1.6.4 neįtraukti į diagramas, duomenų modelį ir testus | Taip; minimi tik 1.6 skyriuje ir Ganto diagramoje (6.5) |

Sąmoningi ryšių trūkumai, kurie jau paaiškinti artefaktuose: Darbuotojas įrašomas į Nuomą, Išdavimą, Grąžinimą, Techninę priežiūrą ir Perkėlimą neskaitant DS8, nes darbuotojas žinomas iš prisijungimo, o prisijungimas nevaizduojamas (`09-dsd.md`); kliento paskyros sukūrimas registruojantis nevaizduojamas dėl tos pačios priežasties.

## Pavadinimų ir skaičių patikra

- Visų `.drawio` diagramų (07, 08, 09, 10, 11) užrašai sutampa su aprašymais: 22 panaudos atvejų, 7 procesų, 8 saugyklų, 3 išorinių esybių, 16 esybių, 18 lentelių ir 3 funkcijų programoje pavadinimai vienodi.
- Skaičiai visuose artefaktuose vienodi: 22 panaudos atvejai (16 operacijų ir 6 iškviečiamos funkcijos), 7 procesai, 8 saugyklos, 49 srautai, 16 esybių, 18 lentelių, 29 ryšiai, 14 nefunkcinių reikalavimų, 4 testavimo atvejai, 15 duomenų taisyklių patikrų.
- Senieji pavadinimai (`tikrintiPrieinamuma`, „Lygis“, „Prisijungimo bandymas“, „Pradžios data“, „vienos krypties nuoma“) likę tik pakeitimų istorijoje (būsenos eilutėse ir `sprendimai.md`).

## Rasti neatitikimai ir pataisymai

1. `13-dizainas.md`, `14-testavimas.md` ir `15-ganto-diagrama.md` būsena buvo „juodraštis, laukia peržiūros“, nors žingsniai patvirtinti – pakeista į „baigta“.
2. `13-dizainas.md` ekranų lentelėje E4 nebuvo PA9, nors E4 rodo, kodėl nuomos negalima išduoti – pridėtas PA9.
3. `14-testavimas.md` 3.1.2 skyriaus lentelėje prie 1.2.1 nurodytas tik TA4, nors paieška atliekama ir TA2 1 žingsnyje – pridėtas TA2.

Kitų neatitikimų nerasta.

## Kas perkeliama į ataskaitą

Ataskaitos priede „Atsekamumo matrica“ pateikiama A lentelė be stulpelių „Aktoriai“ ir „Maketas“ ir B lentelė. C lentelė, pavadinimų patikra ir pataisymų sąrašas lieka tik darbo medžiagoje.
