#!/bin/sh
# Motociklų nuomos IS: dviejų vienu metu pateiktų rezervacijų pavyzdys (NFR 1.3.3.3, artefaktai/12-funkcijos.md).
# Du klientai per dvi atskiras sesijas rezervuoja tą patį motociklą tam pačiam laikotarpiui. Funkcija "rezervuoti"
# (darbas/funkcijos.sql) po patikrinimų palaukia 3 s, kad antroji sesija spėtų pradėti tikrinimą.
#   1) su užraktu: antroji sesija laukia, kol pirmoji baigs transakciją, ir gauna „Motociklas užimtas“;
#   2) be užrakto: abi sesijos nemato viena kitos rezervacijos ir abi ją įrašo – taip būtų be užrakto.
# Įrašytos rezervacijos po kiekvieno bandymo ištrinamos.
#
# Prisijungimas – PostgreSQL aplinkos kintamaisiais (PGHOST, PGPORT, PGUSER, PGDATABASE, PGPASSWORD), pvz.,
# Docker duomenų bazei: PGHOST=localhost PGPORT=5433 PGUSER=motonuoma PGPASSWORD=motonuoma PGDATABASE=motonuoma
# Paleidimas: sh darbas/lygiagreti_rezervacija.sh

KVIETIMAS="SET motonuoma.dabar = '2026-11-19 12:00';
SELECT * FROM \"rezervuoti\"(%s, 22, '2027-05-05 10:00', '2027-05-08 10:00', 1, 1, %s, 3);"

A=$(mktemp); B=$(mktemp)
trap 'rm -f "$A" "$B"' EXIT

bandymas() {
    echo "== $1"
    # shellcheck disable=SC2059
    psql -X -q -c "$(printf "$KVIETIMAS" 1 "$2")" > "$A" &
    sleep 1
    # shellcheck disable=SC2059
    psql -X -q -c "$(printf "$KVIETIMAS" 2 "$2")" > "$B" &
    wait
    echo "Klientas 1:"; sed -n '3p' "$A"
    echo "Klientas 2:"; sed -n '3p' "$B"
    psql -X -q -c "DELETE FROM \"Nuoma\" WHERE \"Motociklo ID\" = 22 AND \"Planuojama pradžia\" = '2027-05-05 10:00'"
}

bandymas "Su užraktu (taip veikia sistema)" true
bandymas "Be užrakto (tik palyginimui)" false
