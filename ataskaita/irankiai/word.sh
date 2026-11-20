#!/bin/sh
# Uždaro jau atidarytą ataskaitą (nesaugodamas), atnaujina .docx laukus ir turinį (TURINYS) Word programoje, išsaugo dokumentą ir PDF.
set -e
F="${1:-ataskaita/MotoNuoma_IS_ataskaita.docx}"
DOCX=$(cd "$(dirname "$F")" && pwd)/$(basename "$F")
PDF="${DOCX%.docx}.pdf"
osascript <<OSA
with timeout of 900 seconds
tell application "Microsoft Word"
  -- jei ataskaita jau atidaryta, Word grąžintų seną versiją ir ją įrašytų ant naujai surinktos
  repeat with k from (count of documents) to 1 by -1
    try
      if (posix full name of document k) is "$DOCX" then close document k saving no
    end try
  end repeat
  open POSIX file "$DOCX"
  set d to active document
  update fields (text object of d)
  update (table of contents 1 of d)
  save d
  save as d file name (POSIX file "$PDF" as text) file format format PDF
  close d saving no
end tell
end timeout
OSA
# Word kai kurioms vidinėms nuorodoms PDF faile neįrašo paskirties – atkuriama pagal nuorodos tekstą
TOOL="${TMPDIR:-/tmp}/ataskaita-pdf-nuorodos"
SRC="$(dirname "$0")/pdf-nuorodos.swift"
if [ ! -x "$TOOL" ] || [ "$TOOL" -ot "$SRC" ]; then swiftc -O -o "$TOOL" "$SRC"; fi
"$TOOL" "$PDF"
