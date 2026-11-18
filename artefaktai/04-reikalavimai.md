# 4. Reikalavimai

Medžiaga ataskaitos skyriams 1.2, 1.3 ir 1.6.

**Būsena:** 1.2 skyrius (funkciniai reikalavimai) ir 1.3 skyrius (nefunkciniai reikalavimai) baigti 2026-11-18. 1.6 skyrius (perspektyviniai reikalavimai) baigtas 2026-11-18.

## 1.2. Funkciniai reikalavimai

Reikalavimų numeriai suteikiami vieną kartą ir toliau nekeičiami: pagal juos susiejamos diagramos, funkcijos ir testai. Pavadinimai po numeriu skirti nuorodoms darbe.

### 1.2.1. Motociklų paieška

| ***Nr. 1.2.1*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Klientas turi galėti rasti laisvus motociklus pagal nuomos datas, filialą, charakteristikas (pvz., tipą, variklio tūrį, galią), reikiamą vairuotojo pažymėjimo kategoriją ir galimybę išvažiuoti į užsienį. Paieškos rezultatuose nerodomi motociklai, kurie pasirinktomis datomis yra rezervuoti, išnuomoti arba techninėje priežiūroje. |

### 1.2.2. Rezervacija ir jos valdymas

| ***Nr. 1.2.2*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Klientas (arba filialo darbuotojas kliento vardu) turi galėti rezervuoti laisvą motociklą, pateikęs vairuotojo pažymėjimo duomenis, ir iš karto gauti patvirtinimą, kuriame nurodyta nuomos kaina, užstatas ir baudų už pavėluotą grąžinimą tarifai. Sistema rezervacijos ar jos pakeitimo neleidžia, jei pasirinktos datos sutampa su kita rezervacija ar technine priežiūra, pažymėjimo kategorija netinka pasirinktam motociklui arba pažymėjimo galiojimas baigiasi anksčiau nei nuoma. Klientas turi galėti peržiūrėti, keisti ir atšaukti savo rezervacijas asmeninėje paskyroje. |

### 1.2.3. Išdavimas ir grąžinimas

| ***Nr. 1.2.3*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Filialo darbuotojas turi galėti matyti savo filialo išdavimų ir grąžinimų tvarkaraštį ir įforminti motociklo išdavimą bei grąžinimą, įskaitant grąžinimą į kitą filialą. Išdavimo ir grąžinimo metu darbuotojas užfiksuoja motociklo ridą ir trumpai aprašo jo būklę. Grąžinant sistema pagal tarifus apskaičiuoja galutinę nuomos kainą ir baudą už pavėluotą grąžinimą. |

### 1.2.4. Techninė priežiūra

| ***Nr. 1.2.4*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Filialo darbuotojas turi galėti iš anksto suplanuoti motociklo techninės priežiūros laikotarpį; tuo laikotarpiu motociklas nerodomas paieškoje ir jo negalima rezervuoti. Sistema neleidžia suplanuoti priežiūros, jei jos laikotarpis sutampa su rezervacija. Neplanuotos priežiūros atveju darbuotojas pirmiausia susisiekia su klientu, pasiūlo kitą motociklą ir perkelia rezervaciją arba ją atšaukia, o tik tada suplanuoja priežiūrą. |

### 1.2.5. Parko administravimas ir ataskaitos

| ***Nr. 1.2.5*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Administratorius turi galėti tvarkyti filialus, motociklų modelius, motociklus, tarifus ir darbuotojų paskyras. Jis taip pat turi matyti esamą ir istorinį parko užimtumą ir formuoti statistines ataskaitas. |

### Reikalavimų ryšys su vartotojais ir IS tikslais

Pagalbinė lentelė darbui (į ataskaitą neperkeliama); tikslų numeriai pagal `01-sritis-ir-tikslai.md`.

| Reikalavimas | Vartotojai | IS tikslai |
|---|---|---|
| 1.2.1 Motociklų paieška | klientas, filialo darbuotojas | 1, 4 |
| 1.2.2 Rezervacija ir jos valdymas | klientas, filialo darbuotojas | 1, 2, 3, 4, 5 |
| 1.2.3 Išdavimas ir grąžinimas | filialo darbuotojas | 3, 4 |
| 1.2.4 Techninė priežiūra | filialo darbuotojas | 1 |
| 1.2.5 Parko administravimas ir ataskaitos | administratorius | 6 |

## 1.3. Nefunkciniai reikalavimai

Nefunkciniai reikalavimai apibrėžia, KAIP sistema turi veikti, ir taikomi visai sistemai. Kiekvienas jų suformuluotas taip, kad būtų galima patikrinti matuojant.

### 1.3.1. Reikalavimai sistemos išvaizdai

#### 1.3.1.1. Prisitaikanti sąsaja

| ***Nr. 1.3.1.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Sistemos sąsaja turi tinkamai veikti ekranuose nuo 360 px pločio, be viršutinės ribos. Siauruose ekranuose elementai nepersidengia ir nėra horizontalios slinkties juostos, o plačiuose ekranuose turinys neišsitempia per visą plotį, bet lieka sugrupuotas. |

#### 1.3.1.2. Vieningas stilius

| ***Nr. 1.3.1.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Visi sistemos puslapiai turi naudoti vienodą spalvų paletę, šriftus ir mygtukų išdėstymą, apibrėžtus 2.3.2 skyriuje. |

#### 1.3.1.3. Motociklo kortelė

| ***Nr. 1.3.1.3*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Paieškos rezultatuose kiekvienas motociklas rodomas kortele su nuotrauka, modelio pavadinimu, pagrindinėmis charakteristikomis (tipas, variklio tūris, galia, reikiama pažymėjimo kategorija) ir paros kaina, kad motociklus būtų galima palyginti neatidarant atskiro puslapio. |

### 1.3.2. Reikalavimai naudojimo paprastumui

#### 1.3.2.1. Kalbos

| ***Nr. 1.3.2.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Sąsaja turi būti lietuvių ir anglų kalbomis. Kalbą galima pakeisti bet kuriame puslapyje neprarandant įvestų duomenų. |

#### 1.3.2.2. Darbuotojo apmokymas

| ***Nr. 1.3.2.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Naujas filialo darbuotojas po ne ilgesnio kaip 3 valandų mokymo turi savarankiškai atlikti pagrindines operacijas: rezervaciją kliento vardu, motociklo išdavimą ir grąžinimą bei techninės priežiūros planavimą. |

#### 1.3.2.3. Trumpas rezervacijos kelias

| ***Nr. 1.3.2.3*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Klientas nuo motociklo pasirinkimo paieškos rezultatuose iki rezervacijos patvirtinimo turi pereiti ne daugiau kaip 3 ekranus (neskaičiuojant prisijungimo). |

#### 1.3.2.4. Aiški atsisakymo priežastis

| ***Nr. 1.3.2.4*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Jei rezervacija ar jos pakeitimas neleidžiami, sistema turi nurodyti konkrečią priežastį: datos užimtos, netinka pažymėjimo kategorija arba pažymėjimas baigia galioti anksčiau nei nuoma. |

### 1.3.3. Reikalavimai veikimo charakteristikoms

#### 1.3.3.1. Atsako laikas

| ***Nr. 1.3.3.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Paieškos rezultatai ir rezervacijos patvirtinimas turi būti parodyti ne vėliau kaip per 2 s, o kiti puslapiai – per 3 s, kai sistema vienu metu naudojasi iki 300 vartotojų. |

#### 1.3.3.2. Pasiekiamumas

| ***Nr. 1.3.3.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Sistema turi veikti visą parą, 7 dienas per savaitę, ir būti pasiekiama ne mažiau kaip 99 % laiko. Nuomos sezono metu (balandžio–spalio mėn.) šis reikalavimas taikomas esant iki 300, o ne sezono metu – iki 50 vienu metu prisijungusių vartotojų. |

#### 1.3.3.3. Vienalaikės rezervacijos

| ***Nr. 1.3.3.3*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Jei du vartotojai vienu metu rezervuoja tą patį motociklą sutampančioms datoms, sistema turi patvirtinti tik vieną rezervaciją, o kitam vartotojui pranešti, kad motociklas jau užimtas. |

### 1.3.4. Reikalavimai sistemos priežiūrai

#### 1.3.4.1. Duomenų dubliavimas ir atsarginės kopijos

| ***Nr. 1.3.4.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Visi duomenų bazės įrašai realiuoju laiku dubliuojami į atsarginę duomenų bazę, be to, kas 24 valandas daroma atsarginė kopija, saugoma ne trumpiau kaip 30 dienų. Sutrikus sistemai, duomenys atkuriami ne ilgiau kaip per 4 valandas. |

#### 1.3.4.2. Istoriniai duomenys

| ***Nr. 1.3.4.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Užbaigtos nuomos iš sistemos netrinamos ir saugomos ne trumpiau kaip 5 metus, kad būtų galima formuoti statistines ataskaitas. |

#### 1.3.4.3. Klaidų taisymas ir atnaujinimai

| ***Nr. 1.3.4.3*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Sezono metu kritinės klaidos, dėl kurių neveikia rezervacija, išdavimas ar grąžinimas, ištaisomos ne vėliau kaip per 1 darbo dieną; planiniai atnaujinimai sezono metu diegiami tik 0–6 val. |

### 1.3.5. Reikalavimai saugumui

#### 1.3.5.1. Prieiga pagal vaidmenis

| ***Nr. 1.3.5.1*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Vartotojas gali atlikti tik savo vaidmeniui (klientas, filialo darbuotojas, administratorius) leistus veiksmus: klientas mato tik savo rezervacijas ir asmens duomenis, o tarifus ir darbuotojų paskyras keisti gali tik administratorius. |

#### 1.3.5.2. Prisijungimas ir duomenų apsauga

| ***Nr. 1.3.5.2*** | ***Reikalavimo tipas: nefunkcinis*** |
|---|---|
| ***Aprašymas:*** | Duomenys tarp naršyklės ir serverio perduodami tik šifruotu ryšiu (HTTPS), o slaptažodžiai saugomi tik kaip maišos reikšmės. Kiekvienas nesėkmingas prisijungimo bandymas įrašomas į saugumo žurnalą, o po 5 nesėkmingų bandymų iš eilės paskyra užblokuojama 15 minučių. |

## 1.6. Perspektyviniai reikalavimai

Šie reikalavimai neįeina į pirmąją sistemos versiją, tačiau galėtų būti įgyvendinti naujoje versijoje. Jie atrinkti iš `01-sritis-ir-tikslai.md` skyriuje „Sistemos ribos“ išvardytų galimybių.

### 1.6.1. Mokėjimas internetu

| ***Nr. 1.6.1*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Klientas rezervuodamas turi galėti internetu sumokėti avansą arba visą nuomos kainą per integruotą mokėjimų sistemą. Išdavimo metu filialo darbuotojas mato, kokia suma jau sumokėta ir kiek liko sumokėti. |

### 1.6.2. Išsamus pažeidimų registravimas

| ***Nr. 1.6.2*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Išdavimo ir grąžinimo metu filialo darbuotojas turi galėti pažymėti motociklo pažeidimus jo schemoje ir pridėti nuotraukų. Grąžinant sistema parodo naujus pažeidimus, kurių nebuvo išdavimo metu, ir susieja juos su ta nuoma. Visa motociklo pažeidimų istorija saugoma ir matoma kitiems darbuotojams. |

### 1.6.3. Integracija su buhalterinės apskaitos sistema

| ***Nr. 1.6.3*** | ***Reikalavimo tipas: funkcinis*** |
|---|---|
| ***Aprašymas:*** | Užbaigus nuomą, sistema turi automatiškai perduoti jos mokėjimų duomenis (sumą, PVM, mokėjimo datą ir būdą) į įmonės naudojamą buhalterinės apskaitos sistemą. Administratorius turi matyti, kurių nuomų duomenys perduoti, o kurių perdavimas nepavyko. |
