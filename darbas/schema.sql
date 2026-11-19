-- Motociklų nuomos IS: duomenų bazės schema (fizinė ER diagrama, 10 žingsnis).
-- (Ataskaitoje nepateikiama, skirta savikontrolei)
--
-- Lentelių ir atributų vardai sutampa su diagramos diagramos/10-fizinis-er.drawio vardais (todėl rašomi dvigubose kabutėse).
-- Patikrinta PostgreSQL 18 (2026-11-19).

-- Personalas ir paskyros

CREATE TABLE "Paskyra" (
    "ID"                  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Prisijungimo vardas" VARCHAR(50)  NOT NULL UNIQUE,
    "Slaptažodžio maiša"  VARCHAR(255) NOT NULL,
    "Vaidmuo"             VARCHAR(16)  NOT NULL
        CHECK ("Vaidmuo" IN ('klientas', 'darbuotojas', 'administratorius'))
);

-- Parkas ir filialai

CREATE TABLE "Filialas" (
    "ID"        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Miestas"   VARCHAR(50)  NOT NULL,
    "Adresas"   VARCHAR(128) NOT NULL,
    "Telefonas" VARCHAR(20)  NOT NULL
);

CREATE TABLE "Kategorija" (
    "Kodas"     VARCHAR(3)   PRIMARY KEY,
    "Aprašymas" VARCHAR(255) NOT NULL
);

CREATE TABLE "Gamintojas" (
    "ID"          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Pavadinimas" VARCHAR(64) NOT NULL UNIQUE
);

CREATE TABLE "Motociklo tipas" (
    "ID"          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Pavadinimas" VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "Motociklo modelis" (
    "ID"                INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Pavadinimas"       VARCHAR(64)  NOT NULL,
    "Variklio tūris"    SMALLINT     NOT NULL CHECK ("Variklio tūris" > 0),
    "Galia"             DECIMAL(5,1) NOT NULL CHECK ("Galia" > 0),
    "Degalų sąnaudos"   DECIMAL(3,1) NOT NULL CHECK ("Degalų sąnaudos" > 0),
    "Nuotrauka"         VARCHAR(255) NOT NULL,
    "Gamintojo ID"      INTEGER      NOT NULL REFERENCES "Gamintojas" ("ID"),
    "Tipo ID"           INTEGER      NOT NULL REFERENCES "Motociklo tipas" ("ID"),
    "Kategorijos kodas" VARCHAR(3)   NOT NULL REFERENCES "Kategorija" ("Kodas"),
    UNIQUE ("Gamintojo ID", "Pavadinimas")
);

CREATE TABLE "Motociklas" (
    "ID"                             INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Valstybinis numeris"            VARCHAR(10) NOT NULL UNIQUE,
    "VIN"                            CHAR(17)    NOT NULL UNIQUE,
    "Pagaminimo metai"               SMALLINT    NOT NULL CHECK ("Pagaminimo metai" >= 1900),
    "Rida"                           INTEGER     NOT NULL CHECK ("Rida" >= 0),
    "Leidžiama išvažiuoti į užsienį" BOOLEAN     NOT NULL DEFAULT FALSE,
    "Naudojamas"                     BOOLEAN     NOT NULL DEFAULT TRUE,
    "Modelio ID"                     INTEGER     NOT NULL REFERENCES "Motociklo modelis" ("ID"),
    "Filialo ID"                     INTEGER     NOT NULL REFERENCES "Filialas" ("ID")
);

CREATE TABLE "Tarifas" (
    "ID"          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Paros kaina" DECIMAL(8,2) NOT NULL CHECK ("Paros kaina" > 0),
    "Užstatas"    DECIMAL(8,2) NOT NULL CHECK ("Užstatas" >= 0),
    "Galioja nuo" DATE         NOT NULL,
    "Galioja iki" DATE,
    "Modelio ID"  INTEGER      NOT NULL REFERENCES "Motociklo modelis" ("ID"),
    CHECK ("Galioja iki" IS NULL OR "Galioja iki" >= "Galioja nuo")
);

CREATE TABLE "Baudos pakopa" (
    "Tarifo ID"           INTEGER      NOT NULL REFERENCES "Tarifas" ("ID") ON DELETE CASCADE,
    "Vėlavimas nuo (val.)" INTEGER     NOT NULL CHECK ("Vėlavimas nuo (val.)" >= 0),
    "Bauda"               DECIMAL(8,2) NOT NULL CHECK ("Bauda" > 0),
    PRIMARY KEY ("Tarifo ID", "Vėlavimas nuo (val.)")
);

-- Klientai

CREATE TABLE "Klientas" (
    "ID"                 INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Vardas"             VARCHAR(50)  NOT NULL,
    "Pavardė"            VARCHAR(50)  NOT NULL,
    "Gimimo data"        DATE         NOT NULL,
    "El. paštas"         VARCHAR(254) UNIQUE,
    "Telefonas"          VARCHAR(20)  NOT NULL,
    "Pažymėjimo numeris" VARCHAR(20)  NOT NULL UNIQUE,
    "Paskyros ID"        INTEGER      UNIQUE REFERENCES "Paskyra" ("ID")
);

CREATE TABLE "Kliento kategorija" (
    "Kliento ID"        INTEGER    NOT NULL REFERENCES "Klientas" ("ID") ON DELETE CASCADE,
    "Kategorijos kodas" VARCHAR(3) NOT NULL REFERENCES "Kategorija" ("Kodas"),
    "Galioja iki"       DATE       NOT NULL,
    PRIMARY KEY ("Kliento ID", "Kategorijos kodas")
);

-- Personalas

CREATE TABLE "Darbuotojas" (
    "ID"          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Vardas"      VARCHAR(50)  NOT NULL,
    "Pavardė"     VARCHAR(50)  NOT NULL,
    "El. paštas"  VARCHAR(254) NOT NULL UNIQUE,
    "Telefonas"   VARCHAR(20)  NOT NULL,
    "Filialo ID"  INTEGER      REFERENCES "Filialas" ("ID"),
    "Paskyros ID" INTEGER      NOT NULL UNIQUE REFERENCES "Paskyra" ("ID")
);

-- Nuomos

CREATE TABLE "Nuoma" (
    "ID"                            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Sukūrimo laikas"               TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "Planuojama pradžia"            TIMESTAMP   NOT NULL,
    "Planuojama pabaiga"            TIMESTAMP   NOT NULL,
    "Būsena"                        VARCHAR(12) NOT NULL DEFAULT 'rezervuota'
        CHECK ("Būsena" IN ('rezervuota', 'aktyvi', 'užbaigta', 'atšaukta')),
    "Kliento ID"                    INTEGER     NOT NULL REFERENCES "Klientas" ("ID"),
    "Tarifo ID"                     INTEGER     NOT NULL REFERENCES "Tarifas" ("ID"),
    "Motociklo ID"                  INTEGER     NOT NULL REFERENCES "Motociklas" ("ID"),
    "Išdavimo filialo ID"           INTEGER     NOT NULL REFERENCES "Filialas" ("ID"),
    "Grąžinimo filialo ID"          INTEGER     NOT NULL REFERENCES "Filialas" ("ID"),
    "Užregistravusio darbuotojo ID" INTEGER     REFERENCES "Darbuotojas" ("ID"),
    CHECK ("Planuojama pabaiga" > "Planuojama pradžia")
);

CREATE TABLE "Išdavimas" (
    "Nuomos ID"     INTEGER      PRIMARY KEY REFERENCES "Nuoma" ("ID"),
    "Laikas"        TIMESTAMP    NOT NULL,
    "Rida"          INTEGER      NOT NULL CHECK ("Rida" >= 0),
    "Būklė"         VARCHAR(500) NOT NULL,
    "Darbuotojo ID" INTEGER      NOT NULL REFERENCES "Darbuotojas" ("ID")
);

CREATE TABLE "Grąžinimas" (
    "Nuomos ID"      INTEGER       PRIMARY KEY REFERENCES "Nuoma" ("ID"),
    "Laikas"         TIMESTAMP     NOT NULL,
    "Rida"           INTEGER       NOT NULL CHECK ("Rida" >= 0),
    "Būklė"          VARCHAR(500)  NOT NULL,
    "Galutinė kaina" DECIMAL(10,2) NOT NULL CHECK ("Galutinė kaina" >= 0),
    "Bauda"          DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK ("Bauda" >= 0),
    "Darbuotojo ID"  INTEGER       NOT NULL REFERENCES "Darbuotojas" ("ID")
);

-- Motociklų užimtumo laikotarpiai (be nuomų)

CREATE TABLE "Techninė priežiūra" (
    "ID"            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Pradžia"       TIMESTAMP    NOT NULL,
    "Pabaiga"       TIMESTAMP    NOT NULL,
    "Priežastis"    VARCHAR(255) NOT NULL,
    "Motociklo ID"  INTEGER      NOT NULL REFERENCES "Motociklas" ("ID"),
    "Darbuotojo ID" INTEGER      NOT NULL REFERENCES "Darbuotojas" ("ID"),
    CHECK ("Pabaiga" > "Pradžia")
);

CREATE TABLE "Perkėlimas" (
    "ID"            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Pradžia"       TIMESTAMP NOT NULL,
    "Pabaiga"       TIMESTAMP NOT NULL,
    "Iš filialo ID" INTEGER   NOT NULL REFERENCES "Filialas" ("ID"),
    "Į filialo ID"  INTEGER   NOT NULL REFERENCES "Filialas" ("ID"),
    "Darbuotojo ID" INTEGER   NOT NULL REFERENCES "Darbuotojas" ("ID"),
    CHECK ("Pabaiga" > "Pradžia"),
    CHECK ("Iš filialo ID" <> "Į filialo ID")
);

CREATE TABLE "Perkeliamas motociklas" (
    "Perkėlimo ID" INTEGER NOT NULL REFERENCES "Perkėlimas" ("ID") ON DELETE CASCADE,
    "Motociklo ID" INTEGER NOT NULL REFERENCES "Motociklas" ("ID"),
    PRIMARY KEY ("Perkėlimo ID", "Motociklo ID")
);
