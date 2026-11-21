# Motociklų nuomos informacinė sistema

VU MIF, Informacinių sistemų inžinerija, I kursas.
Dalykas „Informacinės ir grupinio darbo sistemos“ (lekt. Gediminas Navickas), grupinė užduotis.

Studentai: Dmitrij Kosmakov, Antanas Čypas.

Darbo planas: [`planas.md`](planas.md). Priimti sprendimai: [`sprendimai.md`](sprendimai.md).

| Aplankas | Turinys |
|---|---|
| `artefaktai/` | Tekstinės dalys pagal plano žingsnius, prie jų – diagramų šaltiniai (`.drawio`, Ganto diagramos – `.xlsx`) ir paveikslai (`.png`) tuo pačiu numeriu; `13-dizainas/` – sąsajos maketai (HTML, CSS ir jų paveikslai) |
| `saltiniai/` | Ataskaitos šablonas, laboratorinio darbo ER diagrama, dėstytojo anksčiau priimtos panaudos atvejų (PAD) ir duomenų srautų (DSD) diagramos bei Ganto diagrama (`lab-GANTT-diagrama.xlsx`), paskaitų skaidrės |
| `darbas/` | Darbinė medžiaga: rinkos apžvalga, konkurentų svetainių ekrano nuotraukos, bandomoji duomenų bazė (žr. žemiau) ir kt. |
| `ataskaita/` | Galutinė ataskaita (`MotoNuoma_IS_ataskaita.docx` ir `.pdf`), jos tekstas `ataskaita.md`, šablono kopija ir surinkimo įrankiai (`irankiai/`) |

Dažniausi veiksmai (duomenų bazės paleidimas, patikros, diagramų eksportas) surinkti `Makefile`; sąrašas – komanda `make` šakniniame aplanke (žr. „Greitas paleidimas su make“ žemiau).

## Ataskaitos surinkimas

Ataskaita surenkama iš `ataskaita/ataskaita.md` į šablono kopiją `ataskaita/sablono-kopija.docx`; šablonas `saltiniai/` nekeičiamas. Viskas atliekama komanda `make ataskaita` arba dviem komandomis šakniniame aplanke:

```bash
python3 ataskaita/irankiai/surinkti.py
```

```bash
sh ataskaita/irankiai/word.sh
```

Pirmoji sukuria `ataskaita/MotoNuoma_IS_ataskaita.docx`, antroji Microsoft Word programoje atnaujina laukus ir turinį ir išsaugo `ataskaita/MotoNuoma_IS_ataskaita.pdf` (jei ataskaita jau atidaryta Word programoje, ji uždaroma neišsaugojus). Reikia macOS, Microsoft Word ir Swift (šaltinio failų piktogramoms). Tekstas taisomas tik `ataskaita.md`: rankiniai `.docx` pakeitimai perrenkant dingsta. `ataskaita.md` sintaksė (reikalavimų ir testavimo atvejų blokai, paveikslų ir lentelių pavadinimai, nuorodos) aprašyta `surinkti.py` pradžioje. Po paveikslais pateikiamos nuorodos į jų šaltinio failus šioje GitHub saugykloje (`main` šaka), todėl tie failai turi būti išsiųsti į GitHub ir negali būti pervadinti.

## Bandomoji duomenų bazė

Savikontrolei sukurta PostgreSQL duomenų bazė su išgalvotais duomenimis (ataskaitoje nepateikiama). Failai aplanke `darbas/`:

| Failas | Paskirtis |
|---|---|
| `schema.sql` | Lentelės ir apribojimai pagal fizinę ER diagramą (`artefaktai/10-lenteles.md`) |
| `duomenys.sql` | Bandomieji duomenys: 3 filialai, 15 modelių, 40 motociklų, 40 klientų, 2025–2026 m. sezonų nuomos, 2027 m. rezervacijos, techninė priežiūra, perkėlimai, pavėluoto grąžinimo ir laukusio kliento atvejis. Būsena – 2026-11-19 12:00 |
| `generuoti_duomenis.py` | Skriptas, kuris sugeneruoja `duomenys.sql` (`python3 darbas/generuoti_duomenis.py`); duomenis keisti per jį, o ne rankomis |
| `patikra.sql` | Taisyklių, kurių neužtikrina duomenų bazės apribojimai, patikra (15 patikrų); visose eilutėse turi būti 0 pažeidimų |
| `funkcijos.sql` | 2.2.1 skyriaus funkcijos `tikrintiUzimtuma`, `tikrintiKlientoTeise`, `skaiciuotiKaina` ir operacijos pavyzdys `rezervuoti` (PL/pgSQL, `artefaktai/12-funkcijos.md`) |
| `funkciju_testai.sql` | Funkcijų pavyzdžiai su tikėtinu ir gautu rezultatu; stulpelyje „Sutampa“ visur turi būti `t` |
| `lygiagreti_rezervacija.sh` | Dviejų vienu metu pateiktų rezervacijų pavyzdys (NFR 1.3.3.3): su užraktu įrašoma tik viena |
| `docker-compose.yml` | Duomenų bazės paleidimas Docker konteineryje |

**Greitas paleidimas su make** (iš šakninio aplanko):

| Komanda | Ką daro |
|---|---|
| `make db-tikrinti` | Paleidžia Docker duomenų bazę ir atlieka visas patikras: taisyklių patikrą, funkcijų pavyzdžius ir lygiagrečias rezervacijas |
| `make db-up` / `make db-down` | Paleidžia (ir palaukia, kol įkelti duomenys) / sustabdo Docker duomenų bazę |
| `make db-reset` | Sukuria Docker duomenų bazę iš naujo (pakeitus `schema.sql`, `duomenys.sql` ar `funkcijos.sql`) |
| `make db-patikra`, `make db-testai`, `make db-lygiagreti` | Atskiros patikros Docker duomenų bazėje |
| `make db-psql` | Interaktyvus `psql` Docker duomenų bazėje |
| `make local-tikrinti` | Visos patikros be Docker: laikina PostgreSQL 18 duomenų bazė sukuriama ir po patikrų ištrinama |
| `make duomenys` | Iš naujo sugeneruoja `duomenys.sql` |
| `make iliustracijos` | Iš naujo sugeneruoja funkcijų taisyklių iliustracijas (`artefaktai/08-buvimo-vietos-taisykle.drawio`, `12-sutapimas`, `12-lygiagreti-rezervacija`, `12-pavelavimas`) skriptu `ataskaita/irankiai/iliustracijos.py` |
| `make diagramos` | Eksportuoja visas `.drawio` diagramas į PNG (ER diagramos – mastelis 1.5, iliustracijos – 3, kitos – 2) |
| `make dizainas` | Eksportuoja sąsajos maketus (`artefaktai/13-dizainas/*.html`) į PNG per Google Chrome (reikia Node.js ≥ 22 ir interneto šriftui Inter) |
| `make ataskaita` | Surenka ataskaitą: `.docx` ir PDF per Microsoft Word (žr. „Ataskaitos surinkimas“) |

Patikros baigiasi eilute „Gerai: …“, o radus pažeidimą – „KLAIDA: …“ ir klaidos kodu. `db-lygiagreti` ir `local-tikrinti` reikia PostgreSQL 18 iš Homebrew (`brew install postgresql@18`), `diagramos` – draw.io.

**Su Docker** (reikia Docker Desktop arba OrbStack):

```bash
cd darbas
docker compose up -d
docker compose exec db psql -U motonuoma -d motonuoma -f /patikra.sql
docker compose exec db psql -U motonuoma -d motonuoma -f /funkciju_testai.sql
```

Lygiagrečių rezervacijų pavyzdžiui reikia kompiuteryje įdiegto `psql`:

```bash
PGHOST=localhost PGPORT=5433 PGUSER=motonuoma PGPASSWORD=motonuoma PGDATABASE=motonuoma sh lygiagreti_rezervacija.sh
```

Prisijungimas (pvz., DBeaver): `localhost:5433`, duomenų bazė `motonuoma`, vartotojas ir slaptažodis `motonuoma`. Pakeitus `schema.sql`, `duomenys.sql` ar `funkcijos.sql`, duomenų bazę sukurti iš naujo: `docker compose down -v && docker compose up -d`. Sustabdyti neprarandant duomenų: `docker compose down`.

**SQL užklausos Docker duomenų bazėje.** Komandos vykdomos aplanke `darbas/`, kai konteineris paleistas. Lentelių ir atributų vardai rašomi dvigubose kabutėse (pvz., `"Motociklo modelis"`), todėl komandinėje eilutėje visą užklausą reikia apgaubti viengubomis kabutėmis.

Viena užklausa:

```bash
docker compose exec db psql -U motonuoma -d motonuoma -c 'SELECT "Miestas", "Telefonas" FROM "Filialas";'
```

Užklausos iš failo kompiuteryje (`-T` reikalingas, kai failas perduodamas per `<`):

```bash
docker compose exec -T db psql -U motonuoma -d motonuoma < uzklausa.sql
```

Interaktyvus darbas (`\dt` – lentelių sąrašas, `\d "Nuoma"` – lentelės struktūra, `\q` – išeiti):

```bash
docker compose exec db psql -U motonuoma -d motonuoma
```

Jei kompiuteryje įdiegtas `psql`, galima jungtis ir tiesiogiai:

```bash
PGPASSWORD=motonuoma psql -h localhost -p 5433 -U motonuoma -d motonuoma -c 'SELECT COUNT(*) FROM "Nuoma";'
```

**Be Docker** (įdiegtas PostgreSQL 18):

```bash
createdb motonuoma
psql -d motonuoma -f darbas/schema.sql
psql -d motonuoma -f darbas/duomenys.sql
psql -d motonuoma -f darbas/funkcijos.sql
psql -d motonuoma -f darbas/patikra.sql
psql -d motonuoma -f darbas/funkciju_testai.sql
PGDATABASE=motonuoma sh darbas/lygiagreti_rezervacija.sh
```
