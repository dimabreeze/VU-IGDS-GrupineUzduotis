# 4. Reikalavimai

Medžiaga ataskaitos skyriams 1.2, 1.3 ir 1.6.

**Būsena:** 1.2 skyrius (funkciniai reikalavimai) baigtas 2026-11-18. Nefunkciniai (1.3) ir perspektyviniai (1.6) reikalavimai dar juodraštis, bus suformuluoti 5–6 žingsniuose.

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

## Nefunkcinių reikalavimų užuomazgos

Kilo iš `01-sritis-ir-tikslai.md` ir `02-vartotojai.md`; bus suformuluoti 5 žingsnyje.

- Sąsaja lietuvių ir anglų kalbomis.
- Sąsaja pritaikyta išmaniesiems telefonams.
- Naujas filialo darbuotojas sistemą išmoksta per maždaug tris valandas.
- Užbaigtos nuomos netrinamos: istoriniai duomenys reikalingi statistinėms ataskaitoms.

## Perspektyviniai reikalavimai (kandidatai)

Kandidatų sąrašas pateiktas `01-sritis-ir-tikslai.md` skyriuje „Sistemos ribos“; atranka bus atlikta 6 žingsnyje.
