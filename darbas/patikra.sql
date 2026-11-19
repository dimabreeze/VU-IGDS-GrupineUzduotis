-- Motociklų nuomos IS: duomenų vientisumo patikra.
-- Tikrinamos taisyklės, kurių duomenų bazės apribojimai neužtikrina, o turi užtikrinti sistemos funkcijos
-- (artefaktai/10-lenteles.md, skyrius „Taisyklės, kurias tikrina sistemos funkcijos“).
-- Kiekvienoje eilutėje „Pažeidimų“ turi būti 0. Vykdoma įkėlus darbas/schema.sql ir darbas/duomenys.sql.
-- Laiko skirtumai skaičiuojami PostgreSQL funkcija EXTRACT(EPOCH FROM ...).

WITH
dabar AS (SELECT TIMESTAMP '2026-11-19 12:00:00' AS laikas),  -- duomenų būsenos laikas (duomenys.sql)

-- Motociklo užimtumo laikotarpiai: nuomos (be atšauktų), techninė priežiūra ir perkėlimai.
-- Pavėluotai grąžintos nuomos laikotarpis baigiasi faktiniu grąžinimo laiku.
uzimtumas AS (
    SELECT n."Motociklo ID" AS moto, 'nuoma' AS rusis, n."ID" AS id, n."Planuojama pradžia" AS pradzia,
           CASE WHEN g."Laikas" > n."Planuojama pabaiga" THEN g."Laikas" ELSE n."Planuojama pabaiga" END AS pabaiga,
           n."Išdavimo filialo ID" AS fil_pradzioje, n."Grąžinimo filialo ID" AS fil_pabaigoje,
           n."Būsena" = 'užbaigta' AS baigtas
    FROM "Nuoma" n LEFT JOIN "Grąžinimas" g ON g."Nuomos ID" = n."ID"
    WHERE n."Būsena" <> 'atšaukta'
    UNION ALL
    SELECT tp."Motociklo ID", 'priežiūra', tp."ID", tp."Pradžia", tp."Pabaiga", NULL, NULL,
           tp."Pabaiga" <= (SELECT laikas FROM dabar)
    FROM "Techninė priežiūra" tp
    UNION ALL
    SELECT pm."Motociklo ID", 'perkėlimas', p."ID", p."Pradžia", p."Pabaiga", p."Iš filialo ID", p."Į filialo ID",
           p."Pabaiga" <= (SELECT laikas FROM dabar)
    FROM "Perkėlimas" p JOIN "Perkeliamas motociklas" pm ON pm."Perkėlimo ID" = p."ID"
),
-- Laikotarpiai, keičiantys motociklo vietą (be priežiūros), su ankstesnio laikotarpio pabaigos filialu.
vieta AS (
    SELECT u.*, LAG(u.fil_pabaigoje) OVER (PARTITION BY u.moto ORDER BY u.pradzia) AS ankstesnis_fil,
           ROW_NUMBER() OVER (PARTITION BY u.moto, u.baigtas ORDER BY u.pradzia DESC) AS nuo_galo
    FROM uzimtumas u
    WHERE u.rusis <> 'priežiūra'
),
grazinimas AS (
    SELECT g.*, n."Planuojama pradžia" AS pradzia, n."Planuojama pabaiga" AS pabaiga, n."Tarifo ID" AS tarifas,
           t."Paros kaina" AS paros_kaina,
           CEILING(EXTRACT(EPOCH FROM (n."Planuojama pabaiga" - n."Planuojama pradžia")) / 86400) AS paros,
           EXTRACT(EPOCH FROM (g."Laikas" - n."Planuojama pabaiga")) / 3600 AS velavimas_val
    FROM "Grąžinimas" g JOIN "Nuoma" n ON n."ID" = g."Nuomos ID" JOIN "Tarifas" t ON t."ID" = n."Tarifo ID"
),
apskaiciuota AS (
    SELECT gr."Nuomos ID", gr."Galutinė kaina", gr."Bauda",
           CASE WHEN gr.velavimas_val <= 0 THEN 0
                ELSE COALESCE((SELECT bp."Bauda" FROM "Baudos pakopa" bp
                               WHERE bp."Tarifo ID" = gr.tarifas AND bp."Vėlavimas nuo (val.)" <= gr.velavimas_val
                               ORDER BY bp."Vėlavimas nuo (val.)" DESC FETCH FIRST 1 ROW ONLY), 0) END AS bauda,
           gr.paros * gr.paros_kaina AS nuomos_kaina
    FROM grazinimas gr
)

SELECT * FROM (
SELECT 1 AS "Nr.", 'Motociklo užimtumo laikotarpiai nepersidengia' AS "Patikra", COUNT(*) AS "Pažeidimų"
FROM uzimtumas a JOIN uzimtumas b
  ON a.moto = b.moto AND (a.rusis, a.id) < (b.rusis, b.id) AND a.pradzia < b.pabaiga AND b.pradzia < a.pabaiga
UNION ALL
SELECT 2, 'Laikotarpis prasideda filiale, kuriame baigėsi ankstesnis (buvimo vietos taisyklė)', COUNT(*)
FROM vieta WHERE ankstesnis_fil IS NOT NULL AND fil_pradzioje <> ankstesnis_fil
UNION ALL
SELECT 3, 'Motociklo filialas – paskutinio baigto laikotarpio pabaigos filialas', COUNT(*)
FROM vieta v JOIN "Motociklas" m ON m."ID" = v.moto
WHERE v.baigtas AND v.nuo_galo = 1 AND m."Filialo ID" <> v.fil_pabaigoje
UNION ALL
SELECT 4, 'Vieno modelio tarifų galiojimo laikotarpiai nepersidengia', COUNT(*)
FROM "Tarifas" a JOIN "Tarifas" b
  ON a."Modelio ID" = b."Modelio ID" AND a."ID" < b."ID"
 AND a."Galioja nuo" <= COALESCE(b."Galioja iki", DATE '9999-12-31')
 AND b."Galioja nuo" <= COALESCE(a."Galioja iki", DATE '9999-12-31')
UNION ALL
SELECT 5, 'Nuomos tarifas – motociklo modelio, galiojęs rezervavimo dieną', COUNT(*)
FROM "Nuoma" n JOIN "Tarifas" t ON t."ID" = n."Tarifo ID" JOIN "Motociklas" m ON m."ID" = n."Motociklo ID"
WHERE t."Modelio ID" <> m."Modelio ID"
   OR CAST(n."Sukūrimo laikas" AS DATE) < t."Galioja nuo"
   OR CAST(n."Sukūrimo laikas" AS DATE) > COALESCE(t."Galioja iki", DATE '9999-12-31')
UNION ALL
SELECT 6, 'Klientas turi modelio kategoriją, galiojančią visą nuomos laikotarpį', COUNT(*)
FROM "Nuoma" n JOIN "Motociklas" m ON m."ID" = n."Motociklo ID"
JOIN "Motociklo modelis" mm ON mm."ID" = m."Modelio ID"
WHERE n."Būsena" <> 'atšaukta' AND NOT EXISTS (
    SELECT 1 FROM "Kliento kategorija" kk
    WHERE kk."Kliento ID" = n."Kliento ID" AND kk."Kategorijos kodas" = mm."Kategorijos kodas"
      AND kk."Galioja iki" >= CAST(n."Planuojama pabaiga" AS DATE))
UNION ALL
SELECT 7, 'Būsena atitinka išdavimą ir grąžinimą', COUNT(*)
FROM "Nuoma" n LEFT JOIN "Išdavimas" i ON i."Nuomos ID" = n."ID" LEFT JOIN "Grąžinimas" g ON g."Nuomos ID" = n."ID"
WHERE NOT ((n."Būsena" = 'užbaigta' AND i."Nuomos ID" IS NOT NULL AND g."Nuomos ID" IS NOT NULL)
        OR (n."Būsena" = 'aktyvi' AND i."Nuomos ID" IS NOT NULL AND g."Nuomos ID" IS NULL)
        OR (n."Būsena" IN ('rezervuota', 'atšaukta') AND i."Nuomos ID" IS NULL AND g."Nuomos ID" IS NULL))
UNION ALL
SELECT 8, 'Rida ir laikas grąžinant ne mažesni nei išduodant', COUNT(*)
FROM "Išdavimas" i JOIN "Grąžinimas" g ON g."Nuomos ID" = i."Nuomos ID"
WHERE g."Rida" < i."Rida" OR g."Laikas" <= i."Laikas"
UNION ALL
SELECT 9, 'Motociklo rida – paskutinio grąžinimo rida', COUNT(*)
FROM "Motociklas" m JOIN (
    SELECT n."Motociklo ID" AS moto, g."Rida",
           ROW_NUMBER() OVER (PARTITION BY n."Motociklo ID" ORDER BY g."Laikas" DESC) AS nr
    FROM "Grąžinimas" g JOIN "Nuoma" n ON n."ID" = g."Nuomos ID") p ON p.moto = m."ID" AND p.nr = 1
WHERE m."Rida" <> p."Rida"
UNION ALL
SELECT 10, 'Galutinė kaina ir bauda atitinka tarifą ir baudų pakopas', COUNT(*)
FROM apskaiciuota WHERE "Bauda" <> bauda OR "Galutinė kaina" <> nuomos_kaina + bauda
UNION ALL
SELECT 11, 'Perkėlimas turi bent vieną motociklą', COUNT(*)
FROM "Perkėlimas" p WHERE NOT EXISTS (SELECT 1 FROM "Perkeliamas motociklas" pm WHERE pm."Perkėlimo ID" = p."ID")
UNION ALL
SELECT 12, 'Paskyros vaidmuo atitinka savininką', COUNT(*)
FROM "Paskyra" p LEFT JOIN "Klientas" k ON k."Paskyros ID" = p."ID" LEFT JOIN "Darbuotojas" d ON d."Paskyros ID" = p."ID"
WHERE NOT ((p."Vaidmuo" = 'klientas' AND k."ID" IS NOT NULL AND d."ID" IS NULL)
        OR (p."Vaidmuo" IN ('darbuotojas', 'administratorius') AND d."ID" IS NOT NULL AND k."ID" IS NULL))
UNION ALL
SELECT 13, 'Rezervacija sukurta prieš nuomos pradžią', COUNT(*)
FROM "Nuoma" WHERE "Sukūrimo laikas" >= "Planuojama pradžia"
UNION ALL
SELECT 14, 'Nenaudojamas motociklas neturi laikotarpių ateityje', COUNT(*)
FROM uzimtumas u JOIN "Motociklas" m ON m."ID" = u.moto
WHERE NOT m."Naudojamas" AND u.pabaiga > (SELECT laikas FROM dabar)
) patikros
ORDER BY "Nr.";
