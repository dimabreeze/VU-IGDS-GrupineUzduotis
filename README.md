# Motociklų nuomos informacinė sistema

VU MIF, Informacinių sistemų inžinerija, I kursas.
Dalykas „Informacinės ir grupinio darbo sistemos“ (lekt. Gediminas Navickas), grupinė užduotis.

Studentai: Dmitrij Kosmakov, Antanas Čypas.

Darbo planas: [`planas.md`](planas.md). Priimti sprendimai: [`sprendimai.md`](sprendimai.md).

| Aplankas | Turinys |
|---|---|
| `artefaktai/` | Tekstinės dalys pagal plano žingsnius |
| `diagramos/` | Diagramų šaltiniai (`.drawio`) ir paveikslai (`.png`) |
| `saltiniai/` | Ataskaitos šablonas, laboratorinio darbo ER diagrama, dėstytojo anksčiau priimtos panaudos atvejų (PAD) ir duomenų srautų (DSD) diagramos, paskaitų skaidrės |
| `darbas/` | Darbinė medžiaga: rinkos apžvalga, konkurentų svetainių ekrano nuotraukos, bandomoji duomenų bazė (žr. žemiau) ir kt. |
| `ataskaita/` | Galutinė ataskaita (`.docx`) |

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
| `lygiagreti_rezervacija.sh` | Dviejų vienu metu pateiktų rezervacijų pavyzdys (1.3.3.3): su užraktu įrašoma tik viena |
| `docker-compose.yml` | Duomenų bazės paleidimas Docker konteineryje |

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
