# 1. Dalykinė sritis, sistemos pagrindimas ir tikslai

Medžiaga ataskaitos skyriams 1.1.1 „Vartotojo poreikis ir sistemos pagrindimas“ ir 1.1.2 „IS tikslai“.

## Užsakovas

UAB „MotoNuoma“ yra motociklų nuomos įmonė, turinti tris filialus: Vilniuje, Kaune ir Klaipėdoje. Įmonės parką sudaro apie 40 motociklų, priklausančių 15 modelių: nuo lengvų A2 kategorijos motociklų iki didelių turistinių. Pagrindinis nuomos sezonas trunka nuo balandžio iki spalio.

## Dabartinė veikla

Klientai motociklus rezervuoja telefonu, el. paštu arba „Facebook“ žinutėmis. Filialo darbuotojas laisvus motociklus tikrina bendroje „Excel“ lentelėje, kurią pildo visi trys filialai. Išduodant motociklą pildoma popierinė nuomos sutartis, o nuomos kaina ir bauda už pavėluotą grąžinimą skaičiuojamos rankiniu būdu.

## Problemos

- **Dvigubos rezervacijos.** Ta pati lentelė pildoma keliose vietose, todėl tas pats motociklas kartais rezervuojamas dviem klientams tam pačiam laikotarpiui.
- **Didelės darbuotojų laiko sąnaudos.** Sezono metu didelė darbo dalis tenka atsakinėti į skambučius ir žinutes apie laisvus motociklus.
- **Klientas nemato pasiūlymo.** Jis negali pats patikrinti, kurie motociklai laisvi pasirinktomis datomis, ypač kituose filialuose.
- **Kainos klaidos.** Kaina ir baudos skaičiuojamos ranka, todėl pasitaiko klaidų ir ginčų su klientais.
- **Nenuoseklus vairuotojo teisių tikrinimas.** Ne visada patikrinama, ar kliento vairuotojo pažymėjimo kategorija (A2 ar A) leidžia vairuoti pasirinktą motociklą ir ar pažymėjimas dar galioja.
- **Vadovas neturi apžvalgos.** Parko užimtumą pagal filialus tenka skaičiuoti iš lentelės rankiniu būdu.

## Sistemos pagrindimas ir pagrindinės funkcijos

Šioms problemoms spręsti kuriama internetinė motociklų nuomos informacinė sistema. Ji leis:

- klientui internetu rasti laisvą motociklą pagal datas ir filialą ir jį rezervuoti;
- automatiškai neleisti rezervuoti motociklo, jei pasirinktos datos sutampa su kita nuoma;
- patikrinti kliento vairuotojo pažymėjimo kategoriją ir galiojimą;
- filialo darbuotojui įforminti motociklo išdavimą ir grąžinimą;
- automatiškai apskaičiuoti nuomos kainą ir baudą už pavėluotą grąžinimą;
- administratoriui tvarkyti filialus, motociklų modelius, motociklus ir tarifus bei matyti parko užimtumą.

## IS tikslai

1. **Panaikinti dvigubas rezervacijas.** Motociklo užimtumas tikrinamas vienoje bendroje duomenų bazėje rezervacijos metu.
2. **Sumažinti darbuotojų laiką, skiriamą rezervacijoms.** Dauguma rezervacijų atliekama internetu be darbuotojo dalyvavimo; darbuotojas tik išduoda ir priima motociklą.
3. **Užtikrinti skaidrią ir teisingą kainą.** Kaina ir baudos skaičiuojamos automatiškai pagal tarifą, o klientas mato galutinę kainą prieš rezervuodamas.
4. **Padidinti paslaugos prieinamumą.** Rezervuoti galima visą parą iš bet kurio įrenginio, matant visų filialų pasiūlymą.
5. **Sumažinti riziką įmonei.** Motociklas neišduodamas klientui, kurio pažymėjimo kategorija netinka arba pažymėjimas negalioja.
6. **Suteikti vadovui duomenų sprendimams priimti.** Sistema rodo parko užimtumą pagal filialus.

## Sistemos ribos

Į pirmąją sistemos versiją **neįeina** (kandidatai į 1.6 skyrių „Perspektyviniai reikalavimai“):

- mokėjimas internetu (šioje versijoje už nuomą sumokama filiale);
- motociklo pažeidimų registravimas;
- motociklo grąžinimas į kitą filialą;
- mobilioji programėlė.
