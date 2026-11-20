# Motociklų nuomos IS – dažniausi darbo veiksmai.
# Sąrašas: make (arba make help). Komandos vykdomos iš projekto šakninio aplanko.
# Suderinama su macOS make 3.81 (be .ONESHELL).

SHELL := /bin/bash

# --- Docker duomenų bazė (darbas/docker-compose.yml)
DC      := docker compose -f darbas/docker-compose.yml
DB_EXEC := $(DC) exec -T db psql -X -q -v ON_ERROR_STOP=1 -U motonuoma -d motonuoma
DB_ENV  := PGHOST=localhost PGPORT=5433 PGUSER=motonuoma PGPASSWORD=motonuoma PGDATABASE=motonuoma

# --- PostgreSQL 18 iš Homebrew (psql kompiuteryje ir laikinas serveris be Docker)
PGBIN    := /opt/homebrew/opt/postgresql@18/bin
export PATH := $(PGBIN):$(PATH)
LOCAL_DIR  := $(or $(TMPDIR),/tmp)/motonuoma-pg
LOCAL_PORT := 55432
LOCAL_ENV  := LC_ALL=en_US.UTF-8 PGHOST=127.0.0.1 PGPORT=$(LOCAL_PORT) PGUSER=postgres PGDATABASE=motonuoma

# --- Rezultatų tikrinimas: patikra.sql – visur 0 pažeidimų, funkciju_testai.sql – visur „Sutampa“ = t
TIKRINTI_PATIKRA := awk -F'|' '{print} $$3 != 0 {klaida = 1} END {if (klaida) {print "KLAIDA: yra pažeidimų"; exit 1} else print "Gerai: pažeidimų nėra (" NR " patikrų)"}'
TIKRINTI_TESTUS  := awk -F'|' '{print} $$5 != "t" {klaida = 1} END {if (klaida) {print "KLAIDA: ne visi atvejai sutampa"; exit 1} else print "Gerai: visi " NR " atvejai sutampa"}'

.DEFAULT_GOAL := help
.PHONY: help db-up db-down db-reset db-psql db-patikra db-testai db-lygiagreti db-tikrinti \
        local-tikrinti duomenys diagramos dizainas ataskaita visi

help: ## Šis sąrašas
	@echo "Naudojimas: make <tikslas>"
	@echo
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-16s %s\n", $$1, $$2}'

# ---------------------------------------------------------------- Docker

db-up: ## Paleisti Docker duomenų bazę (localhost:5433) ir palaukti, kol bus įkelta
	@docker info >/dev/null 2>&1 || { echo "Docker nepaleistas – paleiskite OrbStack (open -a OrbStack)"; exit 1; }
	@$(DC) up -d
	@echo -n "Laukiama, kol bus įkelti duomenys ir funkcijos"; \
	for i in $$(seq 1 60); do \
	  if $(DB_EXEC) -Atc "SELECT 1 FROM pg_proc WHERE proname = 'rezervuoti'" 2>/dev/null | grep -q 1; then echo " – paruošta."; exit 0; fi; \
	  echo -n "."; sleep 2; \
	done; echo; echo "Duomenų bazė nepasiruošė per 2 min. (žr. docker compose -f darbas/docker-compose.yml logs)"; exit 1

db-down: ## Sustabdyti Docker duomenų bazę (duomenys išsaugomi)
	@$(DC) down

db-reset: ## Sukurti Docker duomenų bazę iš naujo (pakeitus schema.sql, duomenys.sql ar funkcijos.sql)
	@$(DC) down -v
	@$(MAKE) --no-print-directory db-up

db-psql: ## Interaktyvus psql Docker duomenų bazėje (\q – išeiti)
	@$(DC) exec db psql -U motonuoma -d motonuoma

db-patikra: ## Taisyklių patikra (darbas/patikra.sql) Docker duomenų bazėje
	@$(DC) exec -T db psql -X -q -U motonuoma -d motonuoma -f /patikra.sql
	@$(DC) exec -T db psql -X -q -At -U motonuoma -d motonuoma -f /patikra.sql | $(TIKRINTI_PATIKRA) | tail -1

db-testai: ## Funkcijų pavyzdžiai (darbas/funkciju_testai.sql) Docker duomenų bazėje
	@$(DC) exec -T db psql -X -q -U motonuoma -d motonuoma -f /funkciju_testai.sql
	@$(DC) exec -T db psql -X -q -At -U motonuoma -d motonuoma -f /funkciju_testai.sql | $(TIKRINTI_TESTUS) | tail -1

db-lygiagreti: ## Dvi vienu metu pateiktos rezervacijos (NFR 1.3.3.3) Docker duomenų bazėje
	@$(DB_ENV) sh darbas/lygiagreti_rezervacija.sh

db-tikrinti: db-up db-patikra db-testai db-lygiagreti ## Paleisti Docker duomenų bazę ir atlikti visas patikras

# ---------------------------------------------------------------- be Docker

local-tikrinti: ## Visos patikros laikinoje PostgreSQL 18 duomenų bazėje be Docker (sukuriama ir ištrinama)
	@command -v initdb >/dev/null || { echo "Nerastas PostgreSQL 18 ($(PGBIN)): brew install postgresql@18"; exit 1; }
	@rm -rf "$(LOCAL_DIR)"; \
	$(LOCAL_ENV) initdb -U postgres -D "$(LOCAL_DIR)" >/dev/null || exit 1; \
	$(LOCAL_ENV) pg_ctl -D "$(LOCAL_DIR)" -l "$(LOCAL_DIR).log" -w \
	  -o "-p $(LOCAL_PORT) -k '' -c listen_addresses=127.0.0.1" start >/dev/null || exit 1; \
	trap '$(LOCAL_ENV) pg_ctl -D "$(LOCAL_DIR)" stop >/dev/null; rm -rf "$(LOCAL_DIR)" "$(LOCAL_DIR).log"' EXIT; \
	$(LOCAL_ENV) createdb motonuoma && \
	$(LOCAL_ENV) psql -X -q -v ON_ERROR_STOP=1 -f darbas/schema.sql -f darbas/duomenys.sql -f darbas/funkcijos.sql && \
	echo "== Taisyklių patikra" && \
	$(LOCAL_ENV) psql -X -q -At -f darbas/patikra.sql | $(TIKRINTI_PATIKRA) && \
	echo "== Funkcijų pavyzdžiai" && \
	$(LOCAL_ENV) psql -X -q -At -f darbas/funkciju_testai.sql | $(TIKRINTI_TESTUS) && \
	echo "== Lygiagrečios rezervacijos" && \
	$(LOCAL_ENV) sh darbas/lygiagreti_rezervacija.sh

# ---------------------------------------------------------------- failai

duomenys: ## Iš naujo sugeneruoti darbas/duomenys.sql (generuoti_duomenis.py)
	@python3 darbas/generuoti_duomenis.py

diagramos: ## Eksportuoti visas diagramas į PNG (draw.io)
	@command -v drawio >/dev/null || { echo "Nerastas drawio (brew install --cask drawio)"; exit 1; }
	drawio -x -f png -s 2   -b 20 -o artefaktai/07-panaudos-atvejai.png   artefaktai/07-panaudos-atvejai.drawio
	drawio -x -f png -s 1.5 -b 20 -o artefaktai/08-loginis-er.png         artefaktai/08-loginis-er.drawio
	drawio -x -f png -s 2   -b 20 -o artefaktai/09-dsd.png                artefaktai/09-dsd.drawio
	drawio -x -f png -s 1.5 -b 20 -o artefaktai/10-fizinis-er.png         artefaktai/10-fizinis-er.drawio
	drawio -x -f png -s 2   -b 20 -o artefaktai/11-strukturine-schema.png artefaktai/11-strukturine-schema.drawio
	@echo "Atidarykite PNG ir patikrinkite, ar jie pilni (ER diagramoms mastelis 1.5 – esant 2 drawio nupiešia ne viską)."

dizainas: ## Eksportuoti dizaino maketus į PNG (Google Chrome, Node.js ≥ 22, internetas šriftui)
	@command -v node >/dev/null || { echo "Nerastas Node.js"; exit 1; }
	node artefaktai/13-dizainas/eksportuoti.mjs

ataskaita: ## Surinkti ataskaitą: .docx, Word programoje atnaujinti turinį ir išsaugoti PDF (atidaryta ataskaita uždaroma neišsaugojus)
	python3 ataskaita/irankiai/surinkti.py
	sh ataskaita/irankiai/word.sh

visi: duomenys local-tikrinti ## Sugeneruoti duomenis ir patikrinti be Docker
