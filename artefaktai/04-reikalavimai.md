# 4. Reikalavimai

Medžiaga ataskaitos skyriams 1.2, 1.3 ir 1.6.

**Būsena:** 1.2 skyrius (funkciniai reikalavimai) ir 1.3 skyrius (nefunkciniai reikalavimai) baigti 2026-11-18. 1.6 skyrius (perspektyviniai reikalavimai) baigtas 2026-11-18. Rengiant loginę ER diagramą (8 žingsnis, 2026-11-18) patikslinti FR 1.2.1, FR 1.2.2, FR 1.2.4, FR 1.2.5 ir NFR 1.3.2.4: įtrauktas motociklų perkėlimas tarp filialų, motociklo buvimo vietos taisyklė ir kiekvienos pažymėjimo kategorijos galiojimas. Rengiant duomenų srautų diagramą (9 žingsnis, 2026-11-18) iš NFR 1.3.5.2 išbraukti nesėkmingų prisijungimų žurnalas ir paskyros blokavimas, nes prisijungimas į darbą neįtraukiamas. Po 1 kontrolinio taško (2026-11-19) patikslinti FR 1.2.2 (išdavimo ir grąžinimo filialai pasirenkami rezervuojant), FR 1.2.4 (priežiūra negali sutapti ir su vykstančia nuoma) ir FR 1.2.5 (perkėlimui taikoma motociklo buvimo vietos taisyklė). Aprašant funkcijas (12 žingsnis, 2026-11-19) pridėtas perspektyvinis reikalavimas PR 1.6.4 (nuolaidos ir kompensacijos). Papildyta 2026-11-28: į FR 1.2.3 įtrauktas pažymėjimo tikrinimas išduodant.

## 1.2. Funkciniai reikalavimai

Reikalavimo numerį sudaro tipo žymė ir skyriaus, kuriame reikalavimas aprašytas, numeris: 
* FR – funkcinis reikalavimas (FR 1.2.1–FR 1.2.5), 
* NFR – nefunkcinis reikalavimas (NFR 1.3.1.1–NFR 1.3.5.2), 
* PR – perspektyvinis reikalavimas (PR 1.6.1–PR 1.6.4, 1.6 skyrius). 

Reikalavimų numeriai suteikiami vieną kartą ir toliau nekeičiami: pagal juos susiejamos diagramos, funkcijos ir testai. Pavadinimai po numeriu skirti nuorodoms darbe.

### FR 1.2.1. Motociklų paieška

| ***Nr. FR 1.2.1*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Klientas turi galėti rasti laisvus motociklus pagal nuomos datas, filialą, charakteristikas (pvz., tipą, variklio tūrį, galią), reikiamą vairuotojo pažymėjimo kategoriją ir galimybę išvažiuoti į užsienį. Paieškos rezultatuose nerodomi motociklai, kurie pasirinktomis datomis yra rezervuoti, išnuomoti, techninėje priežiūroje ar perkeliami, taip pat motociklai, kurie nuomos pradžioje bus kitame filiale. |

### FR 1.2.2. Rezervacija ir jos valdymas

| ***Nr. FR 1.2.2*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Klientas (arba filialo darbuotojas kliento vardu) turi galėti rezervuoti laisvą motociklą, pasirinkęs išdavimo ir grąžinimo filialus ir pateikęs vairuotojo pažymėjimo duomenis, ir iš karto gauti patvirtinimą, kuriame nurodyta nuomos kaina, užstatas ir baudų už pavėluotą grąžinimą tarifai. Sistema rezervacijos ar jos pakeitimo neleidžia, jei pasirinktos datos sutampa su kita rezervacija, technine priežiūra ar perkėlimu, jei nuomos pradžioje motociklas bus ne išdavimo filiale arba po grąžinimo nebus tame filiale, kuriame prasideda kita jo rezervacija ar perkėlimas, taip pat jei kliento pažymėjime nėra motociklui tinkamos kategorijos, galiojančios visą nuomos laikotarpį. Klientas turi galėti peržiūrėti, keisti ir atšaukti savo rezervacijas asmeninėje paskyroje. |

### FR 1.2.3. Išdavimas ir grąžinimas

| ***Nr. FR 1.2.3*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Filialo darbuotojas turi galėti matyti savo filialo išdavimų ir grąžinimų tvarkaraštį ir įforminti motociklo išdavimą bei grąžinimą, įskaitant grąžinimą į kitą filialą. Išdavimo ir grąžinimo metu darbuotojas užfiksuoja motociklo ridą ir trumpai aprašo jo būklę. Išduodant darbuotojas sutikrina kliento pateiktą vairuotojo pažymėjimą su sistemoje užregistruotais duomenimis ir, jei jie nesutampa, juos pataiso; sistema motociklo neišduoda, jei kliento pažymėjime nėra motociklui tinkamos kategorijos, galiojančios visą nuomos laikotarpį. Grąžinant sistema pagal tarifus apskaičiuoja galutinę nuomos kainą ir baudą už pavėluotą grąžinimą. |

### FR 1.2.4. Techninė priežiūra

| ***Nr. FR 1.2.4*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Filialo darbuotojas turi galėti iš anksto suplanuoti motociklo techninės priežiūros laikotarpį; tuo laikotarpiu motociklas nerodomas paieškoje ir jo negalima rezervuoti. Sistema neleidžia suplanuoti priežiūros, jei jos laikotarpis sutampa su rezervacija, vykstančia nuoma ar perkėlimu. Neplanuotos priežiūros atveju darbuotojas pirmiausia susisiekia su klientu, pasiūlo kitą motociklą ir perkelia rezervaciją arba ją atšaukia, o tik tada suplanuoja priežiūrą. |

### FR 1.2.5. Parko administravimas ir ataskaitos

| ***Nr. FR 1.2.5*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Administratorius turi galėti tvarkyti filialus, motociklų modelius, motociklus, tarifus ir darbuotojų paskyras, matyti esamą ir istorinį parko užimtumą ir formuoti statistines ataskaitas. Jis taip pat turi galėti suplanuoti vieno ar kelių motociklų perkėlimą į kitą filialą, jei perkėlimo laikotarpis nesutampa su šių motociklų rezervacijomis, vykstančiomis nuomomis ir technine priežiūra, jei perkėlimo pradžioje motociklai bus filiale, iš kurio perkeliama, ir jei kita jų rezervacija ar perkėlimas (jei yra) prasideda filiale, į kurį jie perkeliami. Perkėlimo laikotarpiu šie motociklai nerodomi paieškoje ir jų negalima rezervuoti. |

### Reikalavimų ryšys su vartotojais ir IS tikslais

Pagalbinė lentelė darbui (į ataskaitą neperkeliama); tikslų numeriai pagal `01-sritis-ir-tikslai.md`.

| Reikalavimas | Vartotojai | IS tikslai |
|---|---|---|
| FR 1.2.1 Motociklų paieška | klientas, filialo darbuotojas | 1, 4 |
| FR 1.2.2 Rezervacija ir jos valdymas | klientas, filialo darbuotojas | 1, 2, 3, 4, 5 |
| FR 1.2.3 Išdavimas ir grąžinimas | filialo darbuotojas | 3, 4, 5 |
| FR 1.2.4 Techninė priežiūra | filialo darbuotojas | 1 |
| FR 1.2.5 Parko administravimas ir ataskaitos | administratorius | 4, 6 |

## 1.3. Nefunkciniai reikalavimai

Nefunkciniai reikalavimai apibrėžia, KAIP sistema turi veikti, ir taikomi visai sistemai. Kiekvienas jų suformuluotas taip, kad būtų galima patikrinti matuojant.

### 1.3.1. Reikalavimai sistemos išvaizdai

#### NFR 1.3.1.1. Prisitaikanti sąsaja

| ***Nr. NFR 1.3.1.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Sistemos sąsaja turi tinkamai veikti ekranuose nuo 360 px pločio, be viršutinės ribos. Siauruose ekranuose elementai nepersidengia ir nėra horizontalios slinkties juostos, o plačiuose ekranuose turinys neišsitempia per visą plotį, bet lieka sugrupuotas. |

#### NFR 1.3.1.2. Vieningas stilius

| ***Nr. NFR 1.3.1.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Visi sistemos puslapiai turi naudoti vienodą spalvų paletę, šriftus ir mygtukų išdėstymą, apibrėžtus 2.3.2 skyriuje. |

#### NFR 1.3.1.3. Motociklo kortelė

| ***Nr. NFR 1.3.1.3*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Paieškos rezultatuose kiekvienas motociklo modelis, kurio bent vienas motociklas atitinka paieškos sąlygas, rodomas kortele su nuotrauka, modelio pavadinimu, pagrindinėmis charakteristikomis (tipas, variklio tūris, galia, reikiama pažymėjimo kategorija) ir paros kaina, kad modelius būtų galima palyginti neatidarant atskiro puslapio. |

### 1.3.2. Reikalavimai naudojimo paprastumui

#### NFR 1.3.2.1. Kalbos

| ***Nr. NFR 1.3.2.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Sąsaja turi būti lietuvių ir anglų kalbomis. Kalbą galima pakeisti bet kuriame puslapyje neprarandant įvestų duomenų. |

#### NFR 1.3.2.2. Darbuotojo mokymas

| ***Nr. NFR 1.3.2.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Naujas filialo darbuotojas po ne ilgesnio kaip 3 valandų mokymo turi savarankiškai atlikti pagrindines operacijas: rezervaciją kliento vardu, motociklo išdavimą ir grąžinimą bei techninės priežiūros planavimą. |

#### NFR 1.3.2.3. Trumpas rezervacijos kelias

| ***Nr. NFR 1.3.2.3*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Klientas nuo motociklo pasirinkimo paieškos rezultatuose iki rezervacijos patvirtinimo turi pereiti ne daugiau kaip 3 ekranus (neskaičiuojant prisijungimo). |

#### NFR 1.3.2.4. Aiški atsisakymo priežastis

| ***Nr. NFR 1.3.2.4*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Jei rezervacija ar jos pakeitimas neleidžiami, sistema turi nurodyti konkrečią priežastį: datos užimtos; motociklas nuomos pradžioje bus kitame filiale; motociklo negalima grąžinti į pasirinktą filialą, nes kita jo rezervacija ar perkėlimas prasideda kitame filiale; netinka pažymėjimo kategorija arba jos galiojimas baigiasi anksčiau nei nuoma. |

### 1.3.3. Reikalavimai veikimo charakteristikoms

#### NFR 1.3.3.1. Atsako laikas

| ***Nr. NFR 1.3.3.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Paieškos rezultatai ir rezervacijos patvirtinimas turi būti parodyti ne vėliau kaip per 2 s, o kiti puslapiai – per 3 s, kai sistema vienu metu naudojasi iki 300 vartotojų. |

#### NFR 1.3.3.2. Pasiekiamumas

| ***Nr. NFR 1.3.3.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Sistema turi veikti visą parą, 7 dienas per savaitę, ir būti pasiekiama ne mažiau kaip 99 % laiko. Nuomos sezono metu (balandžio–spalio mėn.) šis reikalavimas taikomas esant iki 300, o ne sezono metu – iki 50 vienu metu prisijungusių vartotojų. |

#### NFR 1.3.3.3. Vienalaikės rezervacijos

| ***Nr. NFR 1.3.3.3*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Jei du vartotojai vienu metu rezervuoja tą patį motociklą sutampančioms datoms, sistema turi patvirtinti tik vieną rezervaciją, o kitam vartotojui pranešti, kad motociklas jau užimtas. |

### 1.3.4. Reikalavimai sistemos priežiūrai

#### NFR 1.3.4.1. Duomenų dubliavimas ir atsarginės kopijos

| ***Nr. NFR 1.3.4.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Visi duomenų bazės įrašai realiuoju laiku dubliuojami į atsarginę duomenų bazę, be to, kas 24 valandas daroma atsarginė kopija, saugoma ne trumpiau kaip 30 dienų. Sutrikus sistemai, duomenys atkuriami ne ilgiau kaip per 4 valandas. |

#### NFR 1.3.4.2. Istoriniai duomenys

| ***Nr. NFR 1.3.4.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Užbaigtos nuomos iš sistemos netrinamos ir saugomos ne trumpiau kaip 5 metus, kad būtų galima formuoti statistines ataskaitas. |

#### NFR 1.3.4.3. Klaidų taisymas ir atnaujinimai

| ***Nr. NFR 1.3.4.3*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Sezono metu kritinės klaidos, dėl kurių neveikia rezervacija, išdavimas ar grąžinimas, ištaisomos ne vėliau kaip per 1 darbo dieną; planiniai atnaujinimai sezono metu diegiami tik 0–6 val. |

### 1.3.5. Reikalavimai saugumui

#### NFR 1.3.5.1. Prieiga pagal vaidmenis

| ***Nr. NFR 1.3.5.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Vartotojas gali atlikti tik savo vaidmeniui (klientas, filialo darbuotojas, administratorius) leistus veiksmus: klientas mato tik savo rezervacijas ir asmens duomenis, o tarifus ir darbuotojų paskyras keisti gali tik administratorius. |

#### NFR 1.3.5.2. Duomenų apsauga

| ***Nr. NFR 1.3.5.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Duomenys tarp naršyklės ir serverio perduodami tik šifruotu ryšiu (HTTPS), o slaptažodžiai saugomi tik kaip maišos reikšmės. |

## 1.6. Perspektyviniai reikalavimai

Šie reikalavimai neįeina į pirmąją sistemos versiją, tačiau galėtų būti įgyvendinti naujoje versijoje. Jie atrinkti iš `01-sritis-ir-tikslai.md` skyriuje „Sistemos ribos“ išvardytų galimybių.

### PR 1.6.1. Mokėjimas internetu

| ***Nr. PR 1.6.1*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Klientas rezervuodamas turi galėti internetu sumokėti avansą arba visą nuomos kainą per integruotą mokėjimų sistemą. Išdavimo metu filialo darbuotojas mato, kokia suma jau sumokėta ir kiek liko sumokėti. |

### PR 1.6.2. Išsamus pažeidimų registravimas

| ***Nr. PR 1.6.2*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Išdavimo ir grąžinimo metu filialo darbuotojas turi galėti pažymėti motociklo pažeidimus jo schemoje ir pridėti nuotraukų. Grąžinant sistema parodo naujus pažeidimus, kurių nebuvo išdavimo metu, ir susieja juos su ta nuoma. Visa motociklo pažeidimų istorija saugoma ir matoma kitiems darbuotojams. |

### PR 1.6.3. Integracija su buhalterinės apskaitos sistema

| ***Nr. PR 1.6.3*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Užbaigus nuomą, sistema turi automatiškai perduoti jos mokėjimų duomenis (sumą, PVM, mokėjimo datą ir būdą) į įmonės naudojamą buhalterinės apskaitos sistemą. Administratorius turi matyti, kurių nuomų duomenys perduoti, o kurių perdavimas nepavyko. |

### PR 1.6.4. Nuolaidos ir kompensacijos

| ***Nr. PR 1.6.4*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Filialo darbuotojas turi galėti suteikti klientui nuolaidą arba kompensaciją (suma ar procentais), nurodydamas priežastį (pvz., klientas laukė pavėluotai grąžinto motociklo), o administratorius – nustatyti didžiausią leidžiamą nuolaidą. Grąžinant sistema galutinę nuomos kainą apskaičiuoja įvertindama nuolaidą. Administratorius turi matyti visas suteiktas nuolaidas ir jų priežastis. |
