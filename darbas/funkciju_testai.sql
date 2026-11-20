-- Motociklų nuomos IS: 2.2.1 skyriaus funkcijų (darbas/funkcijos.sql) pavyzdžiai su bandomaisiais duomenimis.
-- Kiekvienoje eilutėje stulpelis „Sutampa“ turi būti true. Vykdoma įkėlus schema.sql, duomenys.sql ir funkcijos.sql.
-- Dviejų vienu metu vykdomų rezervacijų (1.3.3.3) pavyzdys – darbas/lygiagreti_rezervacija.sh.

SET motonuoma.dabar = '2026-11-19 12:00';

WITH atvejai (nr, atvejis, tiketina, gauta) AS (
    -- tikrintiUzimtuma. CB500 Hornet (motociklas 22, dabar Vilniuje) rezervuotas 2027-05-12 10:00 – 2027-05-15 10:00
    -- (Vilnius → Klaipėda) ir 2027-05-24 10:00 – 2027-05-26 10:00 (Klaipėdoje).
    SELECT 'U1', 'Nuoma sutampa su rezervacija',
           'Motociklas užimtas 2027-05-12 10:00 – 2027-05-15 10:00 (nuoma)',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(22, '2027-05-13 10:00', '2027-05-14 10:00', 1, 1))
    UNION ALL
    SELECT 'U2', 'Pradžioje motociklas bus kitame filiale (2 taisyklė)',
           'Laikotarpio pradžioje motociklas bus filiale Klaipėda',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(22, '2027-05-20 10:00', '2027-05-22 10:00', 1, 1))
    UNION ALL
    SELECT 'U3', 'Grąžinimas į kitą filialą prieš rezervaciją pradiniame (3 taisyklė)',
           'Motociklą reikia grąžinti į filialą Vilnius, nes 2027-05-12 10:00 ten prasideda kita jo nuoma',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(22, '2027-05-05 10:00', '2027-05-08 10:00', 1, 2))
    UNION ALL
    SELECT 'U4', 'Tie patys laikai, grąžinimas į tą patį filialą', 'laisvas',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(22, '2027-05-05 10:00', '2027-05-08 10:00', 1, 1))
    UNION ALL
    SELECT 'U5', 'Techninė priežiūra, sutampanti su rezervacija',
           'Motociklas užimtas 2027-05-12 10:00 – 2027-05-15 10:00 (nuoma)',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(22, '2027-05-14 08:00', '2027-05-14 17:00', NULL, NULL))
    UNION ALL
    SELECT 'U6', 'Techninė priežiūra tarp rezervacijų (vieta netikrinama)', 'laisvas',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(22, '2027-05-20 08:00', '2027-05-20 17:00', NULL, NULL))
    UNION ALL
    SELECT 'U7', 'Perkėlimas iš filialo, kuriame motociklo nebus (po 2027-03-29 perkėlimo jis Klaipėdoje)',
           'Laikotarpio pradžioje motociklas bus filiale Klaipėda',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(20, '2027-04-01 09:00', '2027-04-01 15:00', 1, 2))
    UNION ALL
    SELECT 'U8', 'Rezervacijos 642 keitimas (PA4) – sena rezervacija netikrinama', 'laisvas',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(15, '2027-04-15 11:00', '2027-04-19 11:00', 2, 2, 642))
    UNION ALL
    SELECT 'U9', 'Tas pats laikotarpis kaip nauja rezervacija',
           'Motociklas užimtas 2027-04-14 11:00 – 2027-04-18 11:00 (nuoma)',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(15, '2027-04-15 11:00', '2027-04-19 11:00', 2, 2))
    UNION ALL
    SELECT 'U10', 'Nebenaudojamas motociklas', 'Motociklas nebenaudojamas',
           (SELECT CASE WHEN uzimtas THEN priezastis ELSE 'laisvas' END
            FROM "tikrintiUzimtuma"(30, '2027-05-05 10:00', '2027-05-08 10:00', 2, 2))
    -- tikrintiKlientoTeise. Klientas 26: A1, A2, A iki 2027-05-10; klientas 33 – tik A1; klientas 35 – be kategorijų.
    UNION ALL
    SELECT 'K1', 'Kategorija galioja visą nuomą (F 900 R, A)', 'turi teisę',
           (SELECT CASE WHEN "turiTeise" THEN 'turi teisę' ELSE priezastis END
            FROM "tikrintiKlientoTeise"(26, 15, '2027-04-18 11:00'))
    UNION ALL
    SELECT 'K2', 'Kategorija baigiasi nuomos metu',
           'A kategorija galioja iki 2027-05-10, o nuoma baigiasi 2027-05-12',
           (SELECT CASE WHEN "turiTeise" THEN 'turi teisę' ELSE priezastis END
            FROM "tikrintiKlientoTeise"(26, 15, '2027-05-12 11:00'))
    UNION ALL
    SELECT 'K3', 'Kategorija baigiasi nuomos pabaigos dieną – dar galioja', 'turi teisę',
           (SELECT CASE WHEN "turiTeise" THEN 'turi teisę' ELSE priezastis END
            FROM "tikrintiKlientoTeise"(26, 15, '2027-05-10 18:00'))
    UNION ALL
    SELECT 'K4', 'Netinkama kategorija (A1 – Panigale V2 reikia A)', 'Vairuotojo pažymėjime nėra A kategorijos',
           (SELECT CASE WHEN "turiTeise" THEN 'turi teisę' ELSE priezastis END
            FROM "tikrintiKlientoTeise"(33, 8, '2027-05-12 11:00'))
    UNION ALL
    SELECT 'K5', 'Pažymėjime nėra motociklų kategorijų', 'Vairuotojo pažymėjime nėra A2 kategorijos',
           (SELECT CASE WHEN "turiTeise" THEN 'turi teisę' ELSE priezastis END
            FROM "tikrintiKlientoTeise"(35, 22, '2027-05-12 11:00'))
    -- skaiciuotiKaina („galutinė kaina / bauda“)
    UNION ALL
    SELECT 'S1', 'Nuoma 631: 2 paros × 60 €, grąžinta 3 val. vėliau (pakopa nuo 3 val. – 25 €)', '145.00 / 25.00',
           (SELECT "galutineKaina" || ' / ' || bauda FROM "skaiciuotiKaina"(631, '2026-11-12 13:00'))
    UNION ALL
    SELECT 'S2', 'Nuoma 632: laukusio kliento pradžia pakeista į 13:20, 23 val. 40 min. → 1 para', '60.00 / 0.00',
           (SELECT "galutineKaina" || ' / ' || bauda FROM "skaiciuotiKaina"(632, '2026-11-13 12:40'))
    UNION ALL
    SELECT 'S3', 'Nuoma 391 (NC750X 2026): grąžinta laiku', '168.00 / 0.00',
           (SELECT "galutineKaina" || ' / ' || bauda FROM "skaiciuotiKaina"(391, '2026-05-25 10:00'))
    UNION ALL
    SELECT 'S4', 'Nuoma 391: grąžinta 2 val. anksčiau – kaina nemažinama', '168.00 / 0.00',
           (SELECT "galutineKaina" || ' / ' || bauda FROM "skaiciuotiKaina"(391, '2026-05-25 08:00'))
    UNION ALL
    SELECT 'S5', 'Nuoma 391: 10 min. vėliau – pakopa nuo 0 val. (10 €)', '178.00 / 10.00',
           (SELECT "galutineKaina" || ' / ' || bauda FROM "skaiciuotiKaina"(391, '2026-05-25 10:10'))
    UNION ALL
    SELECT 'S6', 'Nuoma 391: 3 val. 33 min. vėliau – pakopa nuo 2 val. (30 €), nesumuojama', '198.00 / 30.00',
           (SELECT "galutineKaina" || ' / ' || bauda FROM "skaiciuotiKaina"(391, '2026-05-25 13:33'))
    UNION ALL
    SELECT 'S7', 'Nuoma 52 (CB125R 2025, tarifas be pakopų): 4 val. vėliau – baudos nėra', '117.00 / 0.00',
           (SELECT "galutineKaina" || ' / ' || bauda FROM "skaiciuotiKaina"(52, '2025-05-10 18:17'))
    UNION ALL
    SELECT 'S8', 'Nuoma 475 (Panigale V2): rezervuota iki 2026-07-01 – tarifas 159 €', '189.00 / 30.00',
           (SELECT "galutineKaina" || ' / ' || bauda FROM "skaiciuotiKaina"(475, '2026-07-19 12:16'))
    UNION ALL
    SELECT 'S9', 'Visi grąžinimai: funkcijos rezultatas lygus įrašytai kainai ir baudai (nesutampančių)', '0',
           (SELECT COUNT(*)::TEXT FROM "Grąžinimas" g CROSS JOIN LATERAL "skaiciuotiKaina"(g."Nuomos ID", g."Laikas") k
            WHERE k."galutineKaina" <> g."Galutinė kaina" OR k.bauda <> g."Bauda")
)
SELECT nr AS "Nr.", atvejis AS "Atvejis", tiketina AS "Tikėtina", gauta AS "Gauta", tiketina = gauta AS "Sutampa"
FROM atvejai;
