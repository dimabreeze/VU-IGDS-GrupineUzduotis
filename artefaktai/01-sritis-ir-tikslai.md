# 1. Dalykinė sritis, sistemos pagrindimas ir tikslai

Medžiaga ataskaitos skyriams 1.1.1 „Vartotojo poreikis ir sistemos pagrindimas“ ir 1.1.2 „IS tikslai“.

## Užsakovas

UAB „MotoNuoma“ yra motociklų nuomos įmonė, turinti tris filialus:  
    - Vilniuje, 
    - Kaune,
    - Klaipėdoje.  
Įmonės parką sudaro apie 40 motociklų, priklausančių 15 modelių: nuo lengvų A2 kategorijos motociklų iki didelių turistinių. 
Pagrindinis nuomos sezonas trunka nuo balandžio iki spalio.

## Dabartinė veikla

Klientai motociklus rezervuoja telefonu, el. paštu arba „Facebook“ žinutėmis. Filialo darbuotojas laisvus motociklus tikrina bendroje „Excel“ lentelėje, kurią pildo visi trys filialai. Išduodant motociklą pildoma popierinė nuomos sutartis, o nuomos kaina ir bauda už pavėluotą grąžinimą skaičiuojamos rankiniu būdu. Taikomas tik grąžinimas į tą patį filialą: motociklą reikia grąžinti ten, kur jis buvo paimtas.

Tokia praktika būdinga ir Lietuvos rinkai. Peržiūrėjus aštuonių Lietuvos motociklų nuomos įmonių svetaines, dauguma jų rezervacijas priima telefonu arba per formą, kurią vėliau rankiniu būdu patvirtina darbuotojas, todėl klientas neturi garantijos, kad motociklas bus laisvas. Paieška pagal datas yra tik keliose svetainėse, filtrus pagal motociklo tipą ir vairuotojo pažymėjimo kategoriją turi tik viena, o paieškos pagal kitas charakteristikas (variklio tūrį, galią ir pan.) nėra nė vienoje. Išsami analogų apžvalga pateikta `03-analogai.md`.

## Problemos

- **Dvigubos rezervacijos.** Ta pati lentelė pildoma keliose vietose, todėl tas pats motociklas kartais rezervuojamas dviem klientams tam pačiam laikotarpiui.
- **Nėra momentinio patvirtinimo.** Klientas sužino, ar motociklas laisvas, tik darbuotojui atsakius į skambutį ar žinutę.
- **Didelės darbuotojų laiko sąnaudos.** Sezono metu didelę darbo laiko dalį darbuotojams tenka skirti atsakinėjimui į skambučius ir žinutes apie laisvus motociklus.
- **Klientas nemato pasiūlymo.** Jis negali pats rasti motociklo pagal datas, filialą ar charakteristikas (variklio tūrį, tipą, vairuotojo pažymėjimo kategoriją).
- **Kainos klaidos.** Kaina ir baudos skaičiuojamos ranka, todėl pasitaiko klaidų ir ginčų su klientais.
- **Nenuoseklus vairuotojo teisių tikrinimas.** Ne visada patikrinama, ar kliento vairuotojo pažymėjimo kategorija (A2 ar A) leidžia vairuoti pasirinktą motociklą ir ar pažymėjimas dar galioja.
- **Nėra grąžinimo į kitą filialą.** Klientas, keliaujantis, pavyzdžiui, iš Vilniaus į Klaipėdą, turi grįžti į pradinį filialą.
- **Vadovas neturi apžvalgos.** Parko užimtumą pagal filialus tenka skaičiuoti iš lentelės rankiniu būdu.

## Sistemos pagrindimas ir pagrindinės funkcijos

Šioms problemoms spręsti kuriama internetinė motociklų nuomos informacinė sistema. Ji leis:

- klientui internetu rasti laisvą motociklą pagal datas, filialą, charakteristikas, vairuotojo pažymėjimo kategoriją ir galimybę išvažiuoti į užsienį;
- klientui (arba darbuotojui kliento vardu) rezervuoti motociklą, pasirinkus išdavimo ir grąžinimo filialus, su momentiniu patvirtinimu, iš karto matant nuomos kainą ir papildomus mokėjimus (užstatą ir baudų už pavėluotą grąžinimą tarifus);
- automatiškai neleisti rezervuoti motociklo, jei pasirinktos datos sutampa su kita nuoma, suplanuota technine priežiūra ar perkėlimu į kitą filialą arba jei motociklas tuo metu bus kitame filiale;
- rezervacijos metu užregistruoti kliento vairuotojo pažymėjimo duomenis ir patikrinti, ar jame yra motociklui tinkama kategorija ir ar ji galios visą nuomos laikotarpį;
- klientui asmeninėje paskyroje peržiūrėti, keisti ir atšaukti savo rezervacijas;
- filialo darbuotojui įforminti motociklo išdavimą ir grąžinimą (įskaitant grąžinimą į kitą filialą), užfiksuojant motociklo ridą ir būklę, matyti savo filialo išdavimų ir grąžinimų tvarkaraštį ir planuoti motociklų techninės priežiūros laikotarpius;
- automatiškai apskaičiuoti nuomos kainą ir baudą už pavėluotą grąžinimą;
- administratoriui tvarkyti filialus, motociklų modelius, motociklus, tarifus ir darbuotojų paskyras, planuoti motociklų perkėlimą tarp filialų, matyti esamą ir istorinį parko užimtumą bei formuoti statistines ataskaitas.

## IS tikslai

1. **Panaikinti dvigubas rezervacijas ir užtikrinti momentinį patvirtinimą.** Motociklo užimtumas tikrinamas vienoje bendroje duomenų bazėje rezervacijos metu, todėl klientas iš karto gauna galutinį atsakymą.
2. **Sumažinti darbuotojų laiką, skiriamą rezervacijoms.** Dauguma rezervacijų atliekama ir keičiama internetu be darbuotojo dalyvavimo; darbuotojas tik išduoda ir priima motociklą.
3. **Užtikrinti skaidrią ir teisingą kainą.** Kaina, užstatas ir baudos skaičiuojami automatiškai pagal tarifus, o klientas prieš rezervuodamas mato kainą, užstatą ir aiškius baudų už pavėluotą grąžinimą tarifus.
4. **Padidinti paslaugos prieinamumą.** Rezervuoti galima visą parą iš bet kurio įrenginio, matant visų filialų pasiūlymą; be to, galimas grąžinimas į kitą filialą.
5. **Sumažinti riziką įmonei.** Motociklas neišduodamas klientui, kurio pažymėjime nėra tinkamos kategorijos arba ji negalioja visą nuomos laikotarpį.
6. **Suteikti vadovui duomenų sprendimams priimti.** Sistema rodo esamus ir istorinius parko užimtumo duomenis.

## Sistemos ribos

Į pirmąją sistemos versiją **neįeina** (keturi iš jų aprašyti kaip perspektyviniai reikalavimai PR 1.6.1–PR 1.6.4):

- mokėjimas internetu ir integracija su mokėjimų sistema (šioje versijoje už nuomą sumokama filiale);
- mokėjimas dalimis;
- nuoma organizacijoms (juridiniams asmenims);
- integracija su buhalterinės apskaitos sistema;
- išsamus motociklo pažeidimų registravimas (šioje versijoje darbuotojas išdavimo ir grąžinimo metu tik užfiksuoja ridą ir trumpai aprašo būklę);
- nuolaidos ir kompensacijos klientams (šioje versijoje kompensaciją, pvz., klientui, kuris laukė pavėluotai grąžinto motociklo, įmonė suteikia už sistemos ribų);
- mobilioji programėlė.
