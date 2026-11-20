-- Motociklų nuomos IS: 2.2.1 skyriuje aprašytų funkcijų įgyvendinimas savikontrolei
-- (artefaktai/12-funkcijos.md; ataskaitoje nepateikiamas). PostgreSQL 18, PL/pgSQL.
-- Įkeliama po darbas/schema.sql ir darbas/duomenys.sql; pavyzdžiai – darbas/funkciju_testai.sql.
--
-- Funkcijos tik tikrina ir skaičiuoja, duomenų nekeičia. Transakciją ir užraktus valdo jas kviečianti
-- operacija – čia jai pavyzdys yra funkcija "rezervuoti" (PA2).
--
-- Dabartinis laikas imamas iš nustatymo motonuoma.dabar (bandomųjų duomenų būsena – 2026-11-19 12:00),
-- o jei jis nenustatytas – tikrasis laikas. Nustatymas: SET motonuoma.dabar = '2026-11-19 12:00';

CREATE OR REPLACE FUNCTION "dabar"() RETURNS TIMESTAMP LANGUAGE sql STABLE AS $$
    SELECT COALESCE(NULLIF(current_setting('motonuoma.dabar', true), '')::TIMESTAMP, LOCALTIMESTAMP)
$$;

-- Dar nesibaigę motociklo užimtumo laikotarpiai (pagalbinė funkcija).
-- Nuoma: pradžia – planuojama; pabaiga – rezervuotos nuomos planuojama, vykstančios – vėlesnis iš planuojamos
-- pabaigos ir dabartinio laiko. Užbaigtos ir atšauktos nuomos, pasibaigusi priežiūra ir perkėlimai nerenkami:
-- jų rezultatas jau įrašytas motociklo filiale.
CREATE OR REPLACE FUNCTION "motociklo laikotarpiai"("motociklasId" INTEGER, "keiciamaNuomaId" INTEGER)
RETURNS TABLE (rusis VARCHAR, pradzia TIMESTAMP, pabaiga TIMESTAMP, "pradziosFilialas" INTEGER, "pabaigosFilialas" INTEGER)
LANGUAGE sql STABLE AS $$
    SELECT 'nuoma'::VARCHAR, n."Planuojama pradžia",
           CASE WHEN n."Būsena" = 'aktyvi' THEN GREATEST(n."Planuojama pabaiga", "dabar"()) ELSE n."Planuojama pabaiga" END,
           n."Išdavimo filialo ID", n."Grąžinimo filialo ID"
    FROM "Nuoma" n
    WHERE n."Motociklo ID" = "motociklasId" AND n."Būsena" IN ('rezervuota', 'aktyvi')
      AND n."ID" IS DISTINCT FROM "keiciamaNuomaId"
    UNION ALL
    SELECT 'techninė priežiūra', tp."Pradžia", tp."Pabaiga", NULL, NULL
    FROM "Techninė priežiūra" tp
    WHERE tp."Motociklo ID" = "motociklasId" AND tp."Pabaiga" > "dabar"()
    UNION ALL
    SELECT 'perkėlimas', p."Pradžia", p."Pabaiga", p."Iš filialo ID", p."Į filialo ID"
    FROM "Perkėlimas" p JOIN "Perkeliamas motociklas" pm ON pm."Perkėlimo ID" = p."ID"
    WHERE pm."Motociklo ID" = "motociklasId" AND p."Pabaiga" > "dabar"()
$$;

-- 1. tikrintiUzimtuma – Tikrinti motociklo užimtumą (PA6, P1)
CREATE OR REPLACE FUNCTION "tikrintiUzimtuma"(
    "motociklasId" INTEGER, pradzia TIMESTAMP, pabaiga TIMESTAMP,
    "pradziosFilialasId" INTEGER, "pabaigosFilialasId" INTEGER, "keiciamaNuomaId" INTEGER DEFAULT NULL)
RETURNS TABLE (uzimtas BOOLEAN, priezastis VARCHAR) LANGUAGE plpgsql STABLE AS $$
#variable_conflict use_variable
DECLARE
    m "Motociklas"%ROWTYPE;
    l RECORD;
    fil INTEGER;
BEGIN
    SELECT * INTO m FROM "Motociklas" WHERE "ID" = "motociklasId";
    -- 1. Nebenaudojamas motociklas
    IF NOT m."Naudojamas" THEN
        RETURN QUERY SELECT true, 'Motociklas nebenaudojamas'::VARCHAR; RETURN;
    END IF;
    -- 2–3. Sutampantis laikotarpis
    SELECT * INTO l FROM "motociklo laikotarpiai"("motociklasId", "keiciamaNuomaId") x
    WHERE x.pradzia < pabaiga AND pradzia < x.pabaiga
    ORDER BY x.pradzia LIMIT 1;
    IF FOUND THEN
        RETURN QUERY SELECT true, format('Motociklas užimtas %s – %s (%s)',
            to_char(l.pradzia, 'YYYY-MM-DD HH24:MI'), to_char(l.pabaiga, 'YYYY-MM-DD HH24:MI'), l.rusis)::VARCHAR;
        RETURN;
    END IF;
    -- 4. Techninė priežiūra motociklo vietos nekeičia
    IF "pradziosFilialasId" IS NULL THEN
        RETURN QUERY SELECT false, NULL::VARCHAR; RETURN;
    END IF;
    -- 5–6. Kur motociklas bus laikotarpio pradžioje
    SELECT x."pabaigosFilialas" INTO fil FROM "motociklo laikotarpiai"("motociklasId", "keiciamaNuomaId") x
    WHERE x.rusis <> 'techninė priežiūra' AND x.pabaiga <= pradzia
    ORDER BY x.pabaiga DESC LIMIT 1;
    fil := COALESCE(fil, m."Filialo ID");
    IF fil <> "pradziosFilialasId" THEN
        RETURN QUERY SELECT true, format('Laikotarpio pradžioje motociklas bus filiale %s',
            (SELECT "Miestas" FROM "Filialas" WHERE "ID" = fil))::VARCHAR;
        RETURN;
    END IF;
    -- 7. Kur prasideda kitas laikotarpis
    SELECT * INTO l FROM "motociklo laikotarpiai"("motociklasId", "keiciamaNuomaId") x
    WHERE x.rusis <> 'techninė priežiūra' AND x.pradzia >= pabaiga
    ORDER BY x.pradzia LIMIT 1;
    IF FOUND AND l."pradziosFilialas" <> "pabaigosFilialasId" THEN
        RETURN QUERY SELECT true, format('Motociklą reikia grąžinti į filialą %s, nes %s ten prasideda %s',
            (SELECT "Miestas" FROM "Filialas" WHERE "ID" = l."pradziosFilialas"),
            to_char(l.pradzia, 'YYYY-MM-DD HH24:MI'),
            CASE l.rusis WHEN 'nuoma' THEN 'kita jo nuoma' ELSE 'kitas jo perkėlimas' END)::VARCHAR;
        RETURN;
    END IF;
    -- 8. Motociklas laisvas
    RETURN QUERY SELECT false, NULL::VARCHAR;
END $$;

-- 2. tikrintiKlientoTeise – Tikrinti vairuotojo pažymėjimą (PA7, P2)
CREATE OR REPLACE FUNCTION "tikrintiKlientoTeise"("klientasId" INTEGER, "motociklasId" INTEGER, pabaiga TIMESTAMP)
RETURNS TABLE ("turiTeise" BOOLEAN, priezastis VARCHAR) LANGUAGE plpgsql STABLE AS $$
DECLARE
    kodas VARCHAR;
    galioja DATE;
BEGIN
    -- 1. Modeliui reikiama kategorija
    SELECT mm."Kategorijos kodas" INTO kodas
    FROM "Motociklas" m JOIN "Motociklo modelis" mm ON mm."ID" = m."Modelio ID" WHERE m."ID" = "motociklasId";
    -- 2. Ar klientas ją turi
    SELECT kk."Galioja iki" INTO galioja FROM "Kliento kategorija" kk
    WHERE kk."Kliento ID" = "klientasId" AND kk."Kategorijos kodas" = kodas;
    IF NOT FOUND THEN
        RETURN QUERY SELECT false, format('Vairuotojo pažymėjime nėra %s kategorijos', kodas)::VARCHAR; RETURN;
    END IF;
    -- 3. Ar galioja visą nuomos laikotarpį
    IF galioja < CAST(pabaiga AS DATE) THEN
        RETURN QUERY SELECT false, format('%s kategorija galioja iki %s, o nuoma baigiasi %s',
            kodas, to_char(galioja, 'YYYY-MM-DD'), to_char(pabaiga, 'YYYY-MM-DD'))::VARCHAR;
        RETURN;
    END IF;
    RETURN QUERY SELECT true, NULL::VARCHAR;
END $$;

-- 3. skaiciuotiKaina – Apskaičiuoti galutinę nuomos kainą (PA13, PA14, P3)
CREATE OR REPLACE FUNCTION "skaiciuotiKaina"("nuomaId" INTEGER, "grazinimoLaikas" TIMESTAMP)
RETURNS TABLE ("galutineKaina" DECIMAL(10,2), bauda DECIMAL(10,2)) LANGUAGE plpgsql STABLE AS $$
DECLARE
    n RECORD;
    paros INTEGER;
    velavimas NUMERIC;
    b DECIMAL(10,2) := 0;
BEGIN
    -- 1. Nuomos laikotarpis ir tarifas
    SELECT nm."Planuojama pradžia" AS pradzia, nm."Planuojama pabaiga" AS pabaiga, nm."Tarifo ID" AS tarifas,
           t."Paros kaina" AS paros_kaina
    INTO n FROM "Nuoma" nm JOIN "Tarifas" t ON t."ID" = nm."Tarifo ID" WHERE nm."ID" = "nuomaId";
    IF n.pabaiga <= n.pradzia THEN
        RAISE EXCEPTION 'Nuomos % pabaiga ne vėlesnė už pradžią', "nuomaId";
    END IF;
    -- 2. Parų skaičius, suapvalintas į viršų (≥ 1)
    paros := CEIL(EXTRACT(EPOCH FROM (n.pabaiga - n.pradzia)) / 86400);
    -- 3. Vėlavimas valandomis
    velavimas := EXTRACT(EPOCH FROM ("grazinimoLaikas" - n.pabaiga)) / 3600;
    -- 4. Bauda – pakopa su didžiausia „Vėlavimas nuo (val.)“, neviršijančia vėlavimo (PA14)
    IF velavimas > 0 THEN
        SELECT bp."Bauda" INTO b FROM "Baudos pakopa" bp
        WHERE bp."Tarifo ID" = n.tarifas AND bp."Vėlavimas nuo (val.)" <= velavimas
        ORDER BY bp."Vėlavimas nuo (val.)" DESC LIMIT 1;
        b := COALESCE(b, 0);
    END IF;
    -- 5. Galutinė kaina
    RETURN QUERY SELECT CAST(paros * n.paros_kaina + b AS DECIMAL(10,2)), b;
END $$;

-- Operacijos pavyzdys: Rezervuoti motociklą (PA2). Viena transakcija – užrakinti, patikrinti, įrašyti.
-- Kai funkcija iškviečiama atskiru sakiniu, transakcija baigiasi sakinio pabaigoje ir tik tada nuimami užraktai.
-- "uzrakinti" = false ir "lauktiSek" naudojami tik demonstruoti, kas nutiktų be užrakto (funkciju_testai.sql).
CREATE OR REPLACE FUNCTION "rezervuoti"(
    "klientasId" INTEGER, "motociklasId" INTEGER, pradzia TIMESTAMP, pabaiga TIMESTAMP,
    "isdavimoFilialasId" INTEGER, "grazinimoFilialasId" INTEGER,
    uzrakinti BOOLEAN DEFAULT true, "lauktiSek" NUMERIC DEFAULT 0)
RETURNS TABLE ("nuomaId" INTEGER, priezastis VARCHAR) LANGUAGE plpgsql AS $$
DECLARE
    u RECORD;
    t INTEGER;
    id INTEGER;
BEGIN
    -- 1. Užrakinti motociklo įrašą (kita operacija su tuo pačiu motociklu čia palauks)
    IF uzrakinti THEN
        PERFORM 1 FROM "Motociklas" WHERE "ID" = "motociklasId" FOR UPDATE;
    END IF;
    -- 2. Tarifas, galiojantis rezervavimo dieną; bendras užraktas – kol rezervacija neįrašyta, tarifo keisti negalima
    SELECT tr."ID" INTO t FROM "Tarifas" tr JOIN "Motociklas" m ON m."Modelio ID" = tr."Modelio ID"
    WHERE m."ID" = "motociklasId" AND tr."Galioja nuo" <= CAST("dabar"() AS DATE)
      AND (tr."Galioja iki" IS NULL OR tr."Galioja iki" >= CAST("dabar"() AS DATE))
    FOR SHARE OF tr;
    -- 3. Patikrinimai
    SELECT * INTO u FROM "tikrintiUzimtuma"("motociklasId", pradzia, pabaiga, "isdavimoFilialasId", "grazinimoFilialasId");
    IF u.uzimtas THEN
        RETURN QUERY SELECT NULL::INTEGER, u.priezastis; RETURN;
    END IF;
    SELECT * INTO u FROM "tikrintiKlientoTeise"("klientasId", "motociklasId", pabaiga);
    IF NOT u."turiTeise" THEN
        RETURN QUERY SELECT NULL::INTEGER, u.priezastis; RETURN;
    END IF;
    PERFORM pg_sleep("lauktiSek");  -- tik demonstracijai: kita operacija spėja pradėti tikrinimą
    -- 4. Įrašyti rezervaciją
    INSERT INTO "Nuoma" ("Sukūrimo laikas", "Planuojama pradžia", "Planuojama pabaiga", "Kliento ID", "Tarifo ID",
                         "Motociklo ID", "Išdavimo filialo ID", "Grąžinimo filialo ID")
    VALUES ("dabar"(), pradzia, pabaiga, "klientasId", t, "motociklasId", "isdavimoFilialasId", "grazinimoFilialasId")
    RETURNING "ID" INTO id;
    RETURN QUERY SELECT id, NULL::VARCHAR;
END $$;
