# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A university group assignment (VU MIF, course "Informacinės ir grupinio darbo sistemos"): analysis and design — **not implementation** — of an information system for a fictional motorcycle rental company UAB „MotoNuoma“. The deliverable is a filled-in report template (`saltiniai/GrupinesUzduotiesAtaskaitosSablonas_2026_v1.docx`): `ataskaita/MotoNuoma_IS_ataskaita.docx` and `.pdf`, built from `ataskaita/ataskaita.md` (step 16). Two students: Dmitrij Kosmakov and Antanas Čypas.

**Read `HANDOFF.md` first** (Russian): it holds the current state, the next step, how every finished step was done, and the working rules. Then `planas.md` (16-step plan, schedule, which lecture slides apply to each step) and `sprendimai.md` (dated decision log). Do not re-propose decisions already recorded there.

## Working rules (set by Dmitrij; full list in HANDOFF.md §3)

- **Languages:** discuss with the user in Russian; everything written to the repo — artifacts, `planas.md`, `sprendimai.md`, `README.md`, commit messages — in Lithuanian.
- **Discuss before writing.** Propose wording in chat (Lithuanian text, Russian explanation, list of open questions) without touching files. Items the user does not comment on count as accepted. "делай правки" allows editing files, not committing.
- **Commit only after explicit approval** ("ок"). Commit message style: `N žingsnis: <pavadinimas>`.
- **Keep all documents consistent.** Any changed fact (names, numbers, requirement IDs) must be updated everywhere it appears — grep across `artefaktai/`, `.drawio` files, `planas.md`, `sprendimai.md`, `README.md`, `darbas/*.sql`, `darbas/generuoti_duomenis.py` and `ataskaita/ataskaita.md` before reporting back. The report text is a separate copy of the artifacts (file references replaced by section numbers), so a change must be made in both.
- **No invented facts** about competitors or the market; write "nėra duomenų" if unknown.
- Requirement IDs (FR 1.2.1–FR 1.2.5 functional, NFR 1.3.1.1–NFR 1.3.5.2 non-functional, PR 1.6.1–PR 1.6.4 future: type prefix + template section number, written with a space; a bare number in text is always a section number) are assigned once and never renumbered; plain numbers in text are only section numbers; UI screens are EKRANAS01–EKRANAS05 (E1–E3 are DFD external entities); use cases are PA1–PA22, DFD processes P1–P7, data stores DS*, test cases TA*. These IDs are the links between diagrams, functions, tests and the traceability matrix (`artefaktai/16-atsekamumo-matrica.md`).
- Dates `yyyy-mm-dd`; diagrams aligned/symmetric; every diagram and image gets a caption.
- Terminology: use „grąžinimas į kitą filialą“ / „grąžinimas į tą patį filialą“; never „vienos krypties nuoma“.
- Other Claude sessions may edit this folder in parallel. Before committing check `git status`/`git diff`; if there are changes you didn't make, show them to the user instead of reverting or stashing.
- Plain `git push` can't prompt for credentials here; use `git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin main`.

## Layout and how the pieces connect

- `artefaktai/NN-*.md` — one text artifact per plan step (number = step number). Diagrams sit next to them with the same number: `.drawio` is the source, `.png` is exported from it (never edit PNGs directly; re-export).
  - Chain of models: requirements (`04`) → use cases (`07`) → logical ER, Chen notation (`08`) → DFD level 0 (`09`) → physical ER / 18 tables (`10`) → function structure chart (`11`) → functions (`12`) → UI mockups (`13-dizainas/`, HTML + shared `stilius.css`) → tests (`14`) → Gantt (`15`, `.xlsx` built from `saltiniai/lab-GANTT-diagrama.xlsx`) → traceability matrix (`16`).
- `darbas/` — self-check PostgreSQL database (not part of the report): `schema.sql` mirrors `artefaktai/10-lenteles.md`; `funkcijos.sql` implements the PL/pgSQL functions from `artefaktai/12-funkcijos.md` (`tikrintiUzimtuma`, `tikrintiKlientoTeise`, `skaiciuotiKaina`, operation `rezervuoti`). Table/column names are Lithuanian and double-quoted (e.g. `"Motociklo modelis"`). Changes to the design must be reflected in these files too.
  - `duomenys.sql` is generated deterministically by `generuoti_duomenis.py` — **edit the script, never the SQL**. Data state is fixed at 2026-11-19 12:00. Test cases in `14-testavimas.md` reference concrete rows from it.
- `ataskaita/` — the report. `ataskaita.md` (Markdown subset; syntax for requirement blocks `::: reikalavimas`, test cases `::: ta`, figure/table captions and `@pav:`/`@lent:` references is documented in the docstring of `irankiai/surinkti.py`) + `sablono-kopija.docx` (title page, TOC, styles) → `MotoNuoma_IS_ataskaita.docx`; figure and table numbers are assigned at build time. Under each figure the build adds links to its source files in the public GitHub repository (branch `main`), so those files must be pushed. Edit `ataskaita.md`, never the `.docx`/`.pdf`.
- `saltiniai/` — template, lab ER diagram, instructor-accepted example diagrams (PAD, DSD, Gantt) that define the expected style, lecture slides. Do not modify. The lab ER is a source of ideas, not a foundation; the work must exceed lab level.
- Read the `.docx` template as text with `textutil -convert txt -stdout <file>.docx`.

## Commands (run from repo root; `make` lists all)

- `make local-tikrinti` — full check without Docker: temporary PostgreSQL 18 (Homebrew, port 55432) → schema, data, functions → `patikra.sql` (15 rule checks, all must be 0) → `funkciju_testai.sql` (24 cases, column „Sutampa“ must be `t`) → concurrent-booking demo. Prints „Gerai: …“ or „KLAIDA: …“ with non-zero exit.
- `make db-tikrinti` — same checks in Docker (`darbas/docker-compose.yml`, postgres:18 on `localhost:5433`, user/password/db `motonuoma`; Docker = OrbStack, start with `open -a OrbStack`). `make db-reset` after changing `schema.sql`, `duomenys.sql` or `funkcijos.sql`. Individual checks: `make db-patikra`, `db-testai`, `db-lygiagreti`; shell: `make db-psql`.
- `make duomenys` — regenerate `darbas/duomenys.sql`.
- `make diagramos` — export all `.drawio` to PNG (ER diagrams at scale 1.5, others at 2; at scale 2 drawio truncates ER diagrams — open the PNGs to check).
- `python3 ataskaita/irankiai/surinkti.py && sh ataskaita/irankiai/word.sh` — build the report `.docx`, then in Microsoft Word (macOS, via AppleScript) update fields and the TOC and save the PDF. `word.sh` closes an already open copy of the report without saving. There is no `pdftotext`; to check the PDF text use a Swift PDFKit script (`PDFDocument(url:)`, `page(at:).string`). `word.sh` then runs `irankiai/pdf-nuorodos.swift`: Word for Mac writes some internal PDF links with missing or wrong-page destinations; the tool re-targets every internal link by its text (heading, „Nr. FR 1.2.1“, table row „PA1 …“) and fails if it cannot. Internal links/bookmarks are generated automatically by `surinkti.py` (section numbers, FR/NFR, PA, TA, P, DS, E, EKRANAS, [N], „1 priedas“); IDs get their bookmark where they are defined (requirement/TA caption, screen heading, otherwise the first table whose first column holds the ID).
- `make dizainas` — export `artefaktai/13-dizainas/*.html` mockups to PNG at 360 and 1280 px via headless Chrome (Node.js ≥ 22, internet for the Inter font).
