# 4. Reikalavimai

Medžiaga ataskaitos skyriams 1.2, 1.3 ir 1.6.

**Būsena: juodraštis.** Galutinės formuluotės, numeriai (1.2.N, 1.3.N.N, 1.6.N) ir lentelių forma bus nustatyti 4–6 žingsniuose.

## Funkciniai reikalavimai (preliminarus sąrašas)

1. **Motociklų paieška.** Klientas ieško laisvų motociklų pagal nuomos datas, filialą, charakteristikas, vairuotojo pažymėjimo kategoriją ir galimybę išvažiuoti į užsienį.
2. **Rezervacija su momentiniu patvirtinimu.** Klientas (arba darbuotojas kliento vardu) rezervuoja laisvą motociklą, pateikia vairuotojo pažymėjimo duomenis ir iš karto mato nuomos kainą ir papildomus mokėjimus (užstatą ir baudų už pavėluotą grąžinimą tarifus). Sistema neleidžia rezervuoti, jei pasirinktos datos sutampa su kita nuoma arba suplanuota technine priežiūra.
3. **Rezervacijų valdymas asmeninėje paskyroje.** Klientas peržiūri, keičia ir atšaukia savo rezervacijas.
4. **Motociklo išdavimas, grąžinimas ir techninė priežiūra.** Filialo darbuotojas įformina išdavimą ir grąžinimą, įskaitant grąžinimą į kitą filialą, mato savo filialo išdavimų ir grąžinimų tvarkaraštį ir planuoja motociklų techninės priežiūros laikotarpius. Sistema neleidžia suplanuoti priežiūros, jei jos laikotarpis sutampa su rezervacija; neplanuotos priežiūros atveju darbuotojas pirmiausia susisiekia su klientu, pasiūlo kitą motociklą ir perkelia arba atšaukia rezervaciją. Sistema apskaičiuoja galutinę kainą ir baudą už pavėluotą grąžinimą.
5. **Parko valdymas ir statistinės ataskaitos.** Administratorius tvarko filialus, motociklų modelius, motociklus, tarifus ir darbuotojų paskyras, peržiūri esamus ir istorinius parko užimtumo duomenis ir formuoja statistines ataskaitas.

## Nefunkcinių reikalavimų užuomazgos

Kilo iš `01-sritis-ir-tikslai.md` ir `02-vartotojai.md`; bus suformuluoti 5 žingsnyje.

- Sąsaja lietuvių ir anglų kalbomis.
- Sąsaja pritaikyta išmaniesiems telefonams.
- Naujas filialo darbuotojas sistemą išmoksta per maždaug vieną valandą.
- Užbaigtos nuomos netrinamos: istoriniai duomenys reikalingi statistinėms ataskaitoms.

## Perspektyviniai reikalavimai (kandidatai)

Kandidatų sąrašas pateiktas `01-sritis-ir-tikslai.md` skyriuje „Sistemos ribos“; atranka bus atlikta 6 žingsnyje.
