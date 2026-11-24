#!/usr/bin/env python3
"""Ataskaitos surinkimas: ataskaita/ataskaita.md + šablono kopija -> .docx.

Naudojimas (iš saugyklos šaknies): python3 ataskaita/irankiai/surinkti.py
Paskui `ataskaita/irankiai/word.sh` atnaujina turinį Word programoje ir išsaugo PDF.

Šablono kopijos (ataskaita/sablono-kopija.docx) imamas titulinis lapas, turinys, stiliai,
poraštė ir puslapio parametrai; visa šablono dalis po turiniu (gairės) pakeičiama
sugeneruotu turiniu. Naudojama tik standartinė Python biblioteka.

ataskaita.md sintaksė (Markdown poaibis):
  # 1. Sistemos analizė            antraštės 1–4 lygio; numeris tikrinamas su automatine numeracija
  ##### EKRANAS01. Paieška              paryškinta pastraipa (5 lygis, be numeracijos)
  # Šaltiniai {-}                   antraštė be numerio
  - punktas / * punktas / 1. punktas  sąrašai (didesnė įtrauka nei pirmojo punkto – antras lygis);
                                    tuščios eilutės tarp punktų sąrašo nenutraukia, numeruotas sąrašas
                                    prasideda iš naujo nuo punkto „1.“
  eilutė, kurios gale 2 tarpai      eilutės lūžis; sąrašo punkte po jo gali eiti eilutė be įtraukos
  Lentelė: Pavadinimas {#lent:id plotis=1,2,3 maza}
  | a | b |                         lentelė (pirma eilutė – antraštė)
  ![Pavadinimas {#pav:id}](kelias.png){plotis=16 aukstis=20 failai=a.drawio,b.png}
                                    failai= – šaltinio failai; po paveikslu rodomos jų piktogramos su
                                    nuorodomis į failus viešoje GitHub saugykloje (main šaka)
  ::: reikalavimas FR 1.2.1 funkcinis | Pavadinimas    ... :::
  ::: ta 1 | Pavadinimas  (Aprašymas:, Pradiniai duomenys (sąlygos prieš):, žingsnių lentelė, Sąlygos po:)  :::
                                    po „Pradiniai duomenys (sąlygos prieš):“ (iki lentelės) ir po „Sąlygos po:“
                                    (iki bloko pabaigos) gali eiti punktai „- “ (iki 3 lygių pagal įtrauką)
                                    ir pastraipos; „Sąlygos po“ – paskutinė lentelės eilutė
  ::: gulscias ... :::              gulsčias puslapis (atskiras skyrius)
  \\pagebreak                        naujas puslapis
  @pav:id, @lent:id                 nuoroda į paveikslo ar lentelės numerį
  Paveikslų ir lentelių pavadinimai (taip pat reikalavimų ir TA) dedami po objektu centre (stilius Caption);
  Markdown faile lentelės pavadinimas rašomas prieš lentelę. Nuoroda į paveikslą ar lentelę veda į jo pradžią.

Formatavimas – tik stiliais (STYLES): Normal (Times New Roman 12 pt, viengubas intervalas, pirmos eilutės
įtrauka 1,4 cm, abipusė lygiuotė), Heading 1–5, Antraštė 1/2 be numerio, List Paragraph, Šaltinių sąrašas,
Caption, Paveikslas, Paveikslo šaltiniai, Lentelės tekstas / antraštė, Reikalavimo tekstas, Turinio antraštė,
toc 1–3, Kodas (Consolas, fonas #E8EDF4), Kodas lentelėje (be fono), Vidinė nuoroda. Titulinio lapo stiliai (Titulinis …) Normal nepaveldi – lapas nepakinta.
  Vidinės nuorodos sudaromos automatiškai (žymės – skyrių antraštėse, reikalavimų ir TA lentelėse, paveiksluose,
  lentelėse, šaltinių sąraše ir pirmame lentelės stulpelyje, kur ID pasirodo pirmą kartą):
  skyriaus numeris (1.1.4; „3 skyrius“), FR 1.2.1, NFR 1.3.1.1, PR 1.6.1, PA1, TA1, P1, DS1, E1, EKRANAS01, [1],
  „1 priedas“, „Ganto diagrama, 5.4“ (į Ganto diagramos paveikslą {#pav:gantas}). Reikalavimo numeris – tipo žymė
  ir skyriaus numeris per tarpą (FR 1.2.1); skaičius be žymės tekste visada yra skyriaus numeris.
  **paryškinta**, *pasvira*, _pasvira_, `kodas`, <u>pabraukta</u>, <ud>pabraukta punktyru</ud>, [tekstas](url), <br>
  <!-- komentaras -->                į ataskaitą nepatenka
"""
import os
import re
import struct
import subprocess
import sys
import zipfile
from urllib.parse import quote
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC_MD = os.path.join(ROOT, 'ataskaita', 'ataskaita.md')
TEMPLATE = os.path.join(ROOT, 'ataskaita', 'sablono-kopija.docx')
OUT = os.path.join(ROOT, 'ataskaita', 'Brrrum_IS_ataskaita.docx')
SISTEMA = 'Brrrūm'
ICON_TOOL_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ikona.swift')
TMP = os.environ.get('TMPDIR', '/tmp')

# Puslapio geometrija (twips): A4, šablono paraštės
PG_W, PG_H = 11906, 16838
M_TOP, M_BOTTOM, M_LEFT, M_RIGHT = 709, 709, 1418, 851
TEXT_W = PG_W - M_LEFT - M_RIGHT            # 9637
TEXT_W_LAND = PG_H - M_LEFT - M_RIGHT       # 14569
EMU_PER_TWIP = 635
CM = 567  # twips

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R_IMAGE = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
R_LINK = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink'

LANG = '<w:lang w:val="lt-LT"/>'


def die(msg):
    sys.exit('KLAIDA: ' + msg)


# ---------------------------------------------------------------- dokumento būsena
class Doc:
    def __init__(self, files):
        self.files = files
        self.rels = []          # (rId, type, target, external)
        self.next_rid = 1000
        self.next_pic = 1000
        self.media = {}         # kelias -> rId
        self.counters = {'pav': 0, 'lent': 0}
        self.labels = {}
        self.heading = [0, 0, 0, 0]
        self.numbering_nums = []
        self.next_num = 300
        self.link_count = 0
        self.icon_cache = {}
        self.landscape = False
        self.sections = 0       # kiek skyrių pertraukų įterpta
        self.secs = set()       # skyrių numeriai (be galinio taško)
        self.ids = set()        # ID, turintys žymę (FR 1.2.1, PA1, ...)
        self.table_ids = set()  # ID, kurių žymė dedama pirmame lentelės stulpelyje
        self.defined = set()
        self.sources = 0
        self.in_sources = False
        self.src_n = 0
        self.self_ref = None    # ID, kurio apibrėžimas dabar rašomas (į save nesiejama)
        self.next_bm = 90000
        self.unresolved = {}
        self.nolink = False

    def rid(self, typ, target, external=False):
        self.next_rid += 1
        r = 'rId%d' % self.next_rid
        self.rels.append((r, typ, target, external))
        return r


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        die('ne PNG failas: ' + path)
    return struct.unpack('>II', head[16:24])


# ---------------------------------------------------------------- tekstas eilutėje
INLINE = re.compile(r'(\*\*(?P<b>.+?)\*\*|`(?P<c>[^`]+)`|(?<![\w*])\*(?P<i>[^*\s][^*]*?)\*(?!\w)'
                    r'|(?<![\w_])_(?P<i2>[^_\s][^_]*?)_(?![\w_])'
                    r'|<u>(?P<u>.+?)</u>|<ud>(?P<ud>.+?)</ud>|\[(?P<lt>[^\]]+)\]\((?P<lu>https?://[^)]+)\)'
                    r'|(?P<br><br>)|@(?P<ref>(?:pav|lent):[\w-]+)'
                    r'|(?P<src>\[(?P<srcn>\d+)\](?!\())'
                    r'|(?P<gantt>Ganto diagrama, \d+\.\d+(?:, \d+\.\d+)*)'
                    r'|(?P<id>\b(?:(?:N?FR|PR) \d+(?:\.\d+)+(?!\.?\d)|EKRANAS\d{2}|PA\d+|TA\d+|DS\d+|P\d+|E\d)\b)'
                    r'|(?P<pr>\b(?P<prn>\d+) pried(?:as|o|e|ą|ui)\b)'
                    r'|(?P<sec>(?<![\d.,\w])\d+(?:\.\d+)+(?!\d|\.\d)|\b\d+(?= skyri))'
                    r')')

LINK_STYLE = 'Vidinenuoroda'
GANTT_LABEL = 'pav:gantas'


def bookmark(doc, xml, name):
    """Žymė pirmos pastraipos tekstui (po <w:pPr>)."""
    doc.next_bm += 1
    i = xml.index('</w:pPr>') + len('</w:pPr>') if '</w:pPr>' in xml else xml.index('<w:p>') + len('<w:p>')
    j = xml.index('</w:p>', i)
    return (xml[:i] + '<w:bookmarkStart w:id="%d" w:name="%s"/>' % (doc.next_bm, name) + xml[i:j]
            + '<w:bookmarkEnd w:id="%d"/>' % doc.next_bm + xml[j:])


def anchor_name(kind, key):
    return '_%s_%s' % (kind, re.sub(r'\W', '_', key))


def ilink(name, runs):
    return '<w:hyperlink w:anchor="%s" w:history="1">%s</w:hyperlink>' % (name, runs)


def run(text, b=False, i=False, code=False, u=None, sz=None, color=None, style=None, upright=False):
    rpr = ''
    if style or code:
        rpr += '<w:rStyle w:val="%s"/>' % (style or 'Kodas')
    if b:
        rpr += '<w:b/><w:bCs/>'
    if i:
        rpr += '<w:i/><w:iCs/>'
    elif upright:   # kodas kursyvinėje antraštėje ar pavadinime – tiesus (simbolio stilius kursyvo neatšaukia)
        rpr += '<w:i w:val="0"/><w:iCs w:val="0"/>'
    if color:
        rpr += '<w:color w:val="%s"/>' % color
    if sz:
        rpr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz)
    if u:
        rpr += '<w:u w:val="%s"/>' % u
    rpr += LANG
    return '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, escape(text))


def code_runs(text, b=False, i=False, sz=None):
    """`kodas`: tekste – stilius Kodas (fonas, iš šonų siauri neskaidomi tarpai, kad fonas neliestų raidžių);
    lentelėje (sz nurodytas) – Kodas lentelėje be fono, 1 pt mažesnis už lentelės tekstą.
    Trumpo kodo tarpai neskaidomi, kad, pvz., „1:N“, „NOT NULL“ nebūtų perkelti į kitą eilutę; ilgesnės sąlygos
    (pvz., „L.pradžia < pabaiga“) keliamos per tarpus, kitaip abipusė lygiuotė ištempia eilutę."""
    if len(text) <= 13:
        text = text.replace(' ', '\u00a0')
    if sz:
        return run(text, b=b, i=i, sz=sz - 2, style='KodasLenteleje', upright=True)
    pad = run('\u00a0', sz=6, style='Kodas', upright=True)
    return pad + run(text, b=b, i=i, code=True, upright=True) + pad


def inline(doc, text, b=False, i=False, sz=None):
    out = []
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append(run(text[pos:m.start()], b=b, i=i, sz=sz))
        g = m.groupdict()
        if g['b'] is not None:
            out.append(inline(doc, g['b'], b=True, i=i, sz=sz))
        elif g['c'] is not None:
            out.append(code_runs(g['c'], b=b, i=i, sz=sz))
        elif g['i'] is not None or g['i2'] is not None:
            out.append(inline(doc, g['i'] if g['i'] is not None else g['i2'], b=b, i=True, sz=sz))
        elif g['u'] is not None:
            out.append(run(g['u'], b=b, i=i, u='single', sz=sz))
        elif g['ud'] is not None:
            out.append(run(g['ud'], b=b, i=i, u='dash', sz=sz))
        elif g['lt'] is not None:
            rid = doc.rid(R_LINK, g['lu'], external=True)
            out.append('<w:hyperlink r:id="%s" w:history="1">%s</w:hyperlink>'
                       % (rid, run(g['lt'], b=b, i=i, sz=sz, style='Hyperlink')))
        elif g['br'] is not None:
            out.append('<w:r><w:br/></w:r>')
        elif g['ref'] is not None:
            if g['ref'] not in doc.labels:
                die('nežinoma nuoroda @' + g['ref'])
            kind = g['ref'].split(':')[0]
            out.append(ilink(anchor_name(kind, str(doc.labels[g['ref']])),
                             run(str(doc.labels[g['ref']]), b=b, i=i, sz=sz, style=LINK_STYLE)))
        elif g['src'] is not None:
            n = int(g['srcn'])
            out.append(ilink(anchor_name('src', str(n)), run(g['src'], b=b, i=i, sz=sz, style=LINK_STYLE))
                       if 1 <= n <= doc.sources and not doc.in_sources and not doc.nolink else run(g['src'], b=b, i=i, sz=sz))
        elif g['gantt'] is not None:
            # „Ganto diagrama, 5.1, 6.4“ – nuoroda į Ganto diagramos paveikslą; skaičiai neatskiriami nuo žodžių
            t = g['gantt'].replace(', ', ',\u00a0')
            n = doc.labels.get(GANTT_LABEL)
            if n is None:
                die('nėra Ganto diagramos paveikslo žymės @' + GANTT_LABEL)
            out.append(run(t, b=b, i=i, sz=sz) if doc.nolink else
                       ilink(anchor_name('pav', str(n)), run(t, b=b, i=i, sz=sz, style=LINK_STYLE)))
        elif g['id'] is not None:
            t = g['id']
            shown = t.replace(' ', '\u00a0')  # „FR 1.2.1“ – žymė neatskiriama nuo numerio
            if t in doc.ids and t != doc.self_ref and not doc.nolink:
                out.append(ilink(anchor_name('r', t), run(shown, b=b, i=i, sz=sz, style=LINK_STYLE)))
            else:
                if t not in doc.ids:
                    doc.unresolved[t] = doc.unresolved.get(t, 0) + 1
                out.append(run(shown, b=b, i=i, sz=sz))
        elif g['pr'] is not None:
            out.append(ilink(anchor_name('priedas', g['prn']), run(g['pr'], b=b, i=i, sz=sz, style=LINK_STYLE))
                       if g['prn'] in doc.secs_appendix and not doc.nolink else run(g['pr'], b=b, i=i, sz=sz))
        elif g['sec'] is not None:
            t = g['sec']
            out.append(ilink(anchor_name('s', t), run(t, b=b, i=i, sz=sz, style=LINK_STYLE))
                       if t in doc.secs and not doc.nolink else run(t, b=b, i=i, sz=sz))
        pos = m.end()
    if pos < len(text):
        out.append(run(text[pos:], b=b, i=i, sz=sz))
    return ''.join(out)


def para(doc, text, style='Normal'):
    """Pastraipa; visas formatavimas – stiliuje (žr. STYLES)."""
    return ('<w:p><w:pPr><w:pStyle w:val="%s"/><w:rPr>%s</w:rPr></w:pPr>%s</w:p>'
            % (style, LANG, inline(doc, text)))


# ---------------------------------------------------------------- antraštės
HEAD_STYLES = {1: 'Heading1', 2: 'Heading2', 3: 'Heading3', 4: 'Heading4'}
NONUM_STYLES = {1: 'Heading1Benumerio', 2: 'Heading2Benumerio'}


def heading(doc, level, text):
    nonum = text.endswith('{-}')
    text = text.replace('{-}', '').strip()
    if level == 5:
        m = ID_HEAD.match(text)
        doc.self_ref = m.group(1) if m else None
        xml = para(doc, text, style='Heading5')
        doc.self_ref = None
        if m and m.group(1) not in doc.defined:
            doc.defined.add(m.group(1))
            xml = bookmark(doc, xml, anchor_name('r', m.group(1)))
        return xml
    doc.in_sources = text.startswith('Šaltiniai')
    bm = None
    # numeracija, „keep with next“, 1 lygio naujas puslapis ir TURINIO lygiai – antraščių stiliuose
    if nonum and level not in NONUM_STYLES:
        die('antraštė be numerio galima tik 1 ir 2 lygio: ' + text)
    if not nonum:
        doc.heading[level - 1] += 1
        for k in range(level, 4):
            doc.heading[k] = 0
        expected = '.'.join(str(x) for x in doc.heading[:level]) + '.'
        m = re.match(r'^(\d+(?:\.\d+)*\.?)\s+(.*)$', text)
        if not m and level == 4:
            m = re.match(r'^()(.*)$', text)  # 4 lygio numeris neprivalomas – sunumeruojama automatiškai
        elif not m:
            die('antraštėje nėra numerio: ' + text)
        num = m.group(1) if m.group(1).endswith('.') else m.group(1) + '.'
        if m.group(1) and num != expected:
            die('antraštės numeris %s, o turėtų būti %s: %s' % (num, expected, text))
        text = m.group(2)
        bm = anchor_name('s', expected[:-1])
    if level == 1 and not nonum:
        text = text.upper()
    if nonum:
        mp = re.match(r'^(\d+) priedas', text)
        if mp:
            bm = anchor_name('priedas', mp.group(1))
    doc.nolink = True
    xml = ('<w:p><w:pPr><w:pStyle w:val="%s"/><w:rPr>%s</w:rPr></w:pPr>%s</w:p>'
           % ((NONUM_STYLES if nonum else HEAD_STYLES)[level], LANG, inline(doc, text)))
    doc.nolink = False
    return bookmark(doc, xml, bm) if bm else xml


# ---------------------------------------------------------------- sąrašai
def new_num(doc, abstract):
    doc.next_num += 1
    n = doc.next_num
    doc.numbering_nums.append(
        '<w:num w:numId="%d"><w:abstractNumId w:val="%d"/>'
        '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>' % (n, abstract))
    return n


ABS_BULLET, ABS_DECIMAL = 90, 91


def list_par(doc, text, num_id, ilvl, in_table=False, sz=None):
    style = 'Lentelestekstas' if in_table else 'Saltiniusarasas' if doc.in_sources else 'ListParagraph'
    jc = '<w:jc w:val="left"/>' if 'http' in text and not in_table else ''  # ilgų adresų neištempti
    return ('<w:p><w:pPr><w:pStyle w:val="%s"/><w:numPr><w:ilvl w:val="%d"/><w:numId w:val="%d"/></w:numPr>'
            '%s<w:rPr>%s</w:rPr></w:pPr>%s</w:p>'
            % (style, ilvl, num_id, jc, LANG, inline(doc, text, sz=sz)))


# ---------------------------------------------------------------- paveikslai ir šaltinio failų nuorodos
def caption(doc, kind, text, keep_next=False):
    """Paveikslo ar lentelės pavadinimas (dedamas po objektu). Grąžina (xml, parinktys, žymės vardas) –
    žymę kviečiantysis uždeda ant objekto pradžios, kad nuoroda vestų į paveikslo ar lentelės viršų."""
    m = re.search(r'\{([^}]*)\}\s*$', text)
    opts = m.group(1) if m else ''
    text = text[:m.start()].strip() if m else text.strip()
    doc.counters[kind] += 1
    n = doc.counters[kind]
    lab = re.search(r'#((?:pav|lent):[\w-]+)', opts)
    if lab and doc.labels.get(lab.group(1)) != n:
        die('žymės numeris nesutampa (pirmas perėjimas): ' + lab.group(1))
    seq = 'pav' if kind == 'pav' else 'lentele'
    word = 'pav.' if kind == 'pav' else 'lentelė.'
    # po pavadinimo eina šaltinio failų nuorodos – mažesnis tarpas
    kn = '<w:keepNext/><w:spacing w:after="60"/>' if keep_next else ''
    xml = ('<w:p><w:pPr><w:pStyle w:val="Caption"/>%s<w:rPr>%s</w:rPr></w:pPr>'
           '<w:fldSimple w:instr=" SEQ %s \\* ARABIC \\* MERGEFORMAT "><w:r><w:rPr>%s</w:rPr><w:t>%d</w:t></w:r></w:fldSimple>'
           '%s%s</w:p>' % (kn, LANG, seq, LANG, n, run(' ' + word), inline(doc, ' ' + text)))
    return xml, opts, anchor_name(kind, str(n))


def media_rid(doc, path):
    if path not in doc.media:
        name = 'media/rep%d%s' % (len(doc.media) + 1, os.path.splitext(path)[1].lower())
        with open(path, 'rb') as f:
            doc.files['word/' + name] = f.read()
        doc.media[path] = doc.rid(R_IMAGE, name)
    return doc.media[path]


def picture(doc, path, cx_twip, cy_twip, descr, link_rid=None):
    rid = media_rid(doc, path)
    doc.next_pic += 1
    pid = doc.next_pic
    cx, cy = cx_twip * EMU_PER_TWIP, cy_twip * EMU_PER_TWIP
    return ('<w:r><w:rPr><w:noProof/></w:rPr><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="%d" cy="%d"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            '<wp:docPr id="%d" name="Paveikslas %d" descr="%s">%s</wp:docPr>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
            '</wp:inline></w:drawing></w:r>'
            % (cx, cy, pid, pid, escape(descr, {'"': '&quot;'}),
               '<a:hlinkClick xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" r:id="%s"/>' % link_rid
               if link_rid else '', pid, escape(os.path.basename(path)), rid, cx, cy))


def icon_png(doc, filename):
    if filename in doc.icon_cache:
        return doc.icon_cache[filename]
    tool = os.path.join(TMP, 'ataskaita-ikona')
    if not os.path.exists(tool) or os.path.getmtime(tool) < os.path.getmtime(ICON_TOOL_SRC):
        subprocess.run(['swiftc', '-O', '-o', tool, ICON_TOOL_SRC], check=True)
    out = os.path.join(TMP, 'ataskaita-ikona-%d.png' % len(doc.icon_cache))
    subprocess.run([tool, filename, out], check=True)
    doc.icon_cache[filename] = out
    return out


def repo_url():
    """Viešos GitHub saugyklos adresas iš git „origin“ (pvz., https://github.com/savininkas/saugykla)."""
    url = subprocess.run(['git', '-C', ROOT, 'remote', 'get-url', 'origin'],
                         capture_output=True, text=True, check=True).stdout.strip()
    m = re.match(r'^(?:git@github\.com:|https://github\.com/)([^/]+/[^/]+?)(?:\.git)?$', url)
    if not m:
        die('origin nėra GitHub saugykla: ' + url)
    return 'https://github.com/' + m.group(1)


REPO = None
BRANCH = 'main'


def source_link(doc, path):
    """Šaltinio failo nuoroda: failas GitHub saugykloje. .drawio atidaromas draw.io peržiūros
    programoje naršyklėje, kiti failai – GitHub puslapyje. Grąžina (piktograma, pavadinimas)."""
    global REPO
    REPO = REPO or repo_url()
    rel = os.path.relpath(path, ROOT)
    if subprocess.run(['git', '-C', ROOT, 'ls-files', '--error-unmatch', rel], capture_output=True).returncode:
        die('failas neįtrauktas į git, nuoroda neveiks: ' + rel)
    name = re.sub(r'^\d+-', '', os.path.basename(path))  # be artefakto eilės numerio
    if name.endswith('.drawio'):
        raw = '%s/%s/%s' % (REPO.replace('https://github.com/', 'https://raw.githubusercontent.com/'),
                            BRANCH, quote(rel))
        url = 'https://viewer.diagrams.net/?lightbox=1&nav=1&title=%s#U%s' % (quote(name), quote(raw, safe=''))
    else:
        url = '%s/blob/%s/%s' % (REPO, BRANCH, quote(rel))
    doc.link_count += 1
    lrid = doc.rid(R_LINK, url, external=True)
    icon = ('<w:hyperlink r:id="%s" w:history="1">%s</w:hyperlink>'
            % (lrid, picture(doc, icon_png(doc, name), 600, 620, name, link_rid=lrid)))
    # pavadinimas – teksto nuoroda: Word, eksportuodamas PDF, išsaugo tik teksto nuorodas
    text = '<w:hyperlink r:id="%s" w:history="1">%s</w:hyperlink>' % (lrid, run(name, sz=16, style='Hyperlink'))
    return icon, text


def links_table(items):
    """Piktogramos su pavadinimais po jomis – nematoma lentelė, centruota."""
    cw = 2700
    def row(cells):
        return '<w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>' % ''.join(
            '<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Paveikslosaltiniai"/>'
            '<w:keepNext/></w:pPr>%s</w:p></w:tc>' % (cw, c) for c in cells)
    none = ''.join('<w:%s w:val="nil"/>' % e for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    return ('<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>%s</w:tblBorders>'
            '<w:tblLayout w:type="fixed"/><w:tblLook w:val="0000"/></w:tblPr><w:tblGrid>%s</w:tblGrid>%s%s</w:tbl>'
            % (cw * len(items), none, '<w:gridCol w:w="%d"/>' % cw * len(items),
               row([i for i, _ in items]), row([t for _, t in items])))


def figure(doc, cap_text, path, opts):
    path = os.path.normpath(os.path.join(os.path.dirname(SRC_MD), path))
    if not os.path.exists(path):
        die('nėra paveikslo ' + path)
    o = dict(re.findall(r'(\w+)=([^\s}]+)', opts))
    wpx, hpx = png_size(path)
    max_w = TEXT_W_LAND if doc.landscape else TEXT_W
    max_h = (PG_W - 2 * M_TOP - 3 * CM) if doc.landscape else (PG_H - 2 * M_TOP - 4 * CM)
    if o.get('failai'):
        max_h -= 3 * CM
    w = int(float(o['plotis']) * CM) if 'plotis' in o else max_w
    w = min(w, max_w)
    h = int(w * hpx / wpx)
    lim_h = int(float(o['aukstis']) * CM) if 'aukstis' in o else max_h
    if h > lim_h:
        h = lim_h
        w = int(h * wpx / hpx)
    clean_cap = re.sub(r'\s*\{[^}]*\}\s*$', '', cap_text)
    xml = ('<w:p><w:pPr><w:pStyle w:val="Paveikslas"/></w:pPr>%s</w:p>'
           % picture(doc, path, w, h, clean_cap))
    att = [a for a in o.get('failai', '').split(',') if a]
    cap, _, bm = caption(doc, 'pav', cap_text, keep_next=bool(att))
    xml = bookmark(doc, xml, bm) + cap
    if att:
        objs = []
        for a in att:
            ap = os.path.normpath(os.path.join(os.path.dirname(SRC_MD), a))
            if not os.path.exists(ap):
                die('nėra šaltinio failo ' + ap)
            objs.append(source_link(doc, ap))
        xml += ('<w:p><w:pPr><w:pStyle w:val="Paveikslosaltiniai"/><w:keepNext/><w:spacing w:before="60" w:after="60"/>'
                '</w:pPr>%s</w:p>' % run('Šaltinio failai GitHub saugykloje (atidaromi spustelėjus):', i=True))
        xml += links_table(objs) + spacer()
    return xml


# ---------------------------------------------------------------- lentelės
def split_row(line):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|') and not line.endswith('\\|'):
        line = line[:-1]
    cells, cur, k = [], '', 0
    while k < len(line):
        if line[k] == '\\' and k + 1 < len(line) and line[k + 1] == '|':
            cur += '|'
            k += 2
            continue
        if line[k] == '|':
            cells.append(cur.strip())
            cur = ''
        else:
            cur += line[k]
        k += 1
    cells.append(cur.strip())
    return cells


def plain_len(s):
    return len(re.sub(r'[*`]|<[^>]+>|@\w+:', '', s))


def col_widths(rows, total, rel=None):
    n = len(rows[0])
    if rel:
        rel = [float(x) for x in rel.split(',')]
        if len(rel) != n:
            die('plotis= stulpelių skaičius nesutampa: %s' % rel)
    else:
        rel = []
        for c in range(n):
            lens = [plain_len(r[c]) for r in rows if c < len(r)]
            longest_word = max([max([len(w) for w in r[c].split()] or [1]) for r in rows if c < len(r)] or [1])
            avg = sum(lens) / max(1, len(lens))
            rel.append(max(avg ** 0.7, longest_word * 0.9, 3))
    s = sum(rel)
    ws = [int(total * x / s) for x in rel]
    ws[-1] += total - sum(ws)
    return ws


def cell(doc, text, width, sz, header=False, span=1, shade=None, bold=False):
    tcpr = '<w:tcW w:w="%d" w:type="dxa"/>' % width
    if span > 1:
        tcpr += '<w:gridSpan w:val="%d"/>' % span
    if shade:
        tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade
    paras = []
    # punktai langelyje: „- “ eilutės atskirtos <br>
    parts = re.split(r'<br>', text) if '<br>- ' in text or text.startswith('- ') else [text]
    if len(parts) > 1 and all(p.startswith('- ') or not p.strip() for p in parts):
        nid = new_num(doc, ABS_BULLET)
        for p in parts:
            if p.strip():
                paras.append(list_par(doc, p[2:], nid, 2, in_table=True, sz=sz))
    else:
        paras.append('<w:p><w:pPr><w:pStyle w:val="%s"/><w:rPr>%s</w:rPr></w:pPr>%s</w:p>'
                     % ('Lentelesantraste' if header else 'Lentelestekstas', LANG, inline(doc, text, b=bold, sz=sz)))
    return '<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>' % (tcpr, ''.join(paras))


def table(doc, cap_text, lines):
    cap_xml, opts, bm = caption(doc, 'lent', cap_text)
    o = dict(re.findall(r'(\w+)=([^\s}]+)', opts))
    small = 'maza' in opts.split()
    sz = 18 if small else 20
    rows = [split_row(l) for l in lines if not re.match(r'^\s*\|?\s*:?-{3,}', l)]
    n = len(rows[0])
    for r in rows:
        if len(r) != n:
            die('lentelės eilutėje %d langeliai, o antraštėje %d: %s' % (len(r), n, '|'.join(r)))
    total = TEXT_W_LAND if doc.landscape else TEXT_W
    ws = col_widths(rows, total, o.get('plotis'))
    grid = ''.join('<w:gridCol w:w="%d"/>' % w for w in ws)
    out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="%d" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="85" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar>'
           '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
           '</w:tblPr><w:tblGrid>%s</w:tblGrid>' % (total, grid)]
    short = len(rows) <= SHORT_TABLE
    start = 1
    for k, r in enumerate(rows):
        hdr = k == 0
        trpr = '<w:trPr><w:cantSplit/>%s</w:trPr>' % ('<w:tblHeader/>' if hdr else '')
        nonempty = [c for c in r if c]
        if not hdr and len(nonempty) == 1 and not r[0] and n > 2:
            # grupės eilutė: vienas tekstas per visą plotį
            out.append('<w:tr>%s%s</w:tr>' % (trpr, cell(doc, nonempty[0], total, sz, span=n, shade='F2F2F2')))
            continue
        cells = []
        for j, c in enumerate(r):
            defin = not hdr and j == 0 and c in doc.table_ids and c not in doc.defined
            doc.self_ref = c if defin else None
            x = cell(doc, c, ws[j], sz, header=hdr, shade='D9D9D9' if hdr else None)
            doc.self_ref = None
            if defin:
                doc.defined.add(c)
                x = bookmark(doc, x, anchor_name('r', c))
            cells.append(x)
        out.append('<w:tr>%s%s</w:tr>' % (trpr, ''.join(cells)))
    # pavadinimas po lentele laikomas su paskutine eilute; trumpa lentelė – visa viename puslapyje
    out[start if short else -1:] = [keep_next(x) for x in out[start if short else -1:]]
    out.append('</w:tbl>')
    out[0] = bookmark(doc, ''.join(out[:2]), bm)
    del out[1]
    out.append(cap_xml)
    return ''.join(out)


SHORT_TABLE = 15


def keep_next(xml):
    return re.sub(r'(<w:pStyle w:val="[^"]*"/>)(?!<w:keepNext/>)', r'\1<w:keepNext/>', xml)


def gap_before_table(out):
    """Tarpas tarp teksto (ar sąrašo) ir po jo einančios lentelės: tekstas be tarpų tarp pastraipų,
    todėl be jo lentelė prisiliestų prie teksto. Po antraštės ar pavadinimo tarpo jau yra."""
    last = re.findall(r'<w:pStyle w:val="([^"]+)"/>', out[-1]) if out else []
    if last and last[-1] in ('Normal', 'ListParagraph', 'Saltiniusarasas'):
        out.append('<w:p><w:pPr><w:pStyle w:val="Lentelestekstas"/><w:keepNext/><w:spacing w:before="0" w:after="0"/>'
                   '<w:rPr><w:sz w:val="12"/><w:szCs w:val="12"/></w:rPr></w:pPr></w:p>')


def spacer():
    return '<w:p><w:pPr><w:pStyle w:val="Lentelestekstas"/><w:spacing w:after="120"/></w:pPr></w:p>'


def tpl_par(doc, text_runs, bold=False, keep=False):
    return ('<w:p><w:pPr><w:pStyle w:val="Reikalavimotekstas"/>' + ('<w:keepNext/>' if keep else '') +
            '<w:rPr>%s%s</w:rPr></w:pPr>%s</w:p>' % ('<w:b/>' if bold else '', LANG, text_runs))


def requirement(doc, nr, typ, name, text):
    doc.self_ref = nr
    cap, _, bm = caption(doc, 'lent', '%s %s' % (nr, name))
    doc.self_ref = None
    doc.defined.add(nr)
    w1, w2 = TEXT_W // 2, TEXT_W - TEXT_W // 2
    tc = lambda w, body, span='': ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr>%s</w:tc>'
                                   % (w, span, body))
    r1 = (tc(w1, tpl_par(doc, run('Nr. ' + nr.replace(' ', '\u00a0'), b=True, i=True), keep=True)) +
          tc(w2, tpl_par(doc, run('Reikalavimo tipas: ' + typ, b=True, i=True), keep=True)))
    r2 = tc(TEXT_W, tpl_par(doc, run('Aprašymas: ', b=True, i=True) + inline(doc, text), keep=True),
            '<w:gridSpan w:val="2"/>')
    tbl = ('<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="%d" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
           'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid><w:gridCol w:w="%d"/>'
           '<w:gridCol w:w="%d"/></w:tblGrid><w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>'
           '<w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr></w:tbl>' % (TEXT_W, w1, w2, r1, r2))
    return bookmark(doc, bookmark(doc, tbl, bm), anchor_name('r', nr)) + cap


def cell_list(doc, lines, where, sz):
    """Langelio tęsinys iš Markdown eilučių: punktai („- “ / „* “, iki 3 lygių pagal įtrauką) ir pastraipos.

    Tuščia eilutė baigia punktą ar pastraipą; eilutė be žymės tuoj po punkto – jo tęsinys."""
    blocks, indents, cur = [], [], None
    for l in lines:
        if not l.strip():
            cur = None
            continue
        m = LIST_RE.match(l)
        if m:
            if m.group(2)[0].isdigit():
                die('%s: numeruotas sąrašas nepalaikomas: %s' % (where, l.strip()))
            ind = len(m.group(1))
            while indents and indents[-1] > ind:
                indents.pop()
            if not indents or indents[-1] < ind:
                indents.append(ind)
            if len(indents) > 3:
                die('%s: daugiau nei 3 sąrašo lygiai: %s' % (where, l.strip()))
            cur = [len(indents) - 1, [l[m.end():]]]
            blocks.append(cur)
        elif cur is not None:
            cur[1].append(l)
        else:
            indents = []
            cur = [None, [l]]
            blocks.append(cur)
    out = []
    nid = new_num(doc, ABS_BULLET) if any(b[0] is not None for b in blocks) else None
    for lvl, parts in blocks:
        text = join_lines(parts)
        if lvl is None:
            out.append('<w:p><w:pPr><w:pStyle w:val="Lentelestekstas"/><w:rPr>%s</w:rPr></w:pPr>%s</w:p>'
                       % (LANG, inline(doc, text, sz=sz)))
        else:
            out.append(list_par(doc, text, nid, 2 + lvl, in_table=True, sz=sz))  # 2–4 lygiai – lentelėms
    return ''.join(out)


def test_case(doc, nr, name, block):
    cap, _, bm = caption(doc, 'lent', 'Testavimo atvejis Nr. %s „%s“' % (nr, name))
    doc.defined.add('TA' + nr)
    desc = pre = post = None
    pre_lines = []   # eilutės po „Pradiniai duomenys (sąlygos prieš):“ iki žingsnių lentelės (sąrašas)
    post_lines = []  # eilutės po „Sąlygos po:“ iki bloko pabaigos (sąrašas)
    tlines = []
    cur = None
    for l in block:
        if l.startswith('Aprašymas:'):
            desc = l[len('Aprašymas:'):].strip()
            cur = None
        elif l.startswith('Pradiniai duomenys (sąlygos prieš):'):
            pre = l[len('Pradiniai duomenys (sąlygos prieš):'):].strip()
            cur = pre_lines
        elif l.startswith('Sąlygos po:'):
            post = l[len('Sąlygos po:'):].strip()
            cur = post_lines
        elif l.strip().startswith('|') and cur is not post_lines:
            tlines.append(l)
            cur = None
        elif cur is not None:
            cur.append(l)
    for what, val in (('Aprašymas:', desc), ('Pradiniai duomenys (sąlygos prieš):', pre), ('Sąlygos po:', post)):
        if val is None:
            die('TA %s: nėra eilutės „%s“' % (nr, what))
    steps = [split_row(l) for l in tlines if not re.match(r'^\s*\|?\s*:?-{3,}', l)][1:]
    # stulpeliai kaip šablone: Nr., žingsnis, laukiamas rezultatas (2 tinklelio stulpeliai), Pavyko?, Pastabos
    g = [543, 3344, 947, 2532, 1191, 1070]
    sz = 20

    def c(text, w, span=1, b=False, shade=None, label=None, extra=''):
        tcpr = '<w:tcW w:w="%d" w:type="dxa"/>' % w
        if span > 1:
            tcpr += '<w:gridSpan w:val="%d"/>' % span
        if shade:
            tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade
        body = (run(label, b=True, sz=sz) if label else '') + inline(doc, text, b=b, sz=sz)
        return ('<w:tc><w:tcPr>%s</w:tcPr><w:p><w:pPr><w:pStyle w:val="%s"/><w:rPr>%s</w:rPr></w:pPr>'
                '%s</w:p>%s</w:tc>' % (tcpr, 'Lentelesantraste' if shade else 'Lentelestekstas', LANG, body, extra))
    tr = lambda cells, hdr=False: '<w:tr><w:trPr><w:cantSplit/>%s</w:trPr>%s</w:tr>' % (
        '<w:tblHeader/>' if hdr else '', cells)
    rows = [tr(c('Testavimo atvejo Nr. %s' % nr, sum(g[:3]), 3, b=True) + c(name, sum(g[3:]), 3, b=True)),
            tr(c(desc, sum(g), 6, label='Aprašymas: ')),
            tr(c(pre, sum(g), 6, label='Pradiniai duomenys (sąlygos prieš): ',
                 extra=cell_list(doc, pre_lines, 'TA %s pradiniai duomenys' % nr, sz))),
            tr(c('Nr.', g[0], b=True, shade='D9D9D9') + c('Testavimo atvejo (scenarijaus) žingsnis', g[1], b=True, shade='D9D9D9')
               + c('Laukiamas rezultatas', g[2] + g[3], 2, b=True, shade='D9D9D9')
               + c('Pavyko gauti laukiamą rezultatą? (Taip/Ne)', g[4], b=True, shade='D9D9D9')
               + c('Klaidos, pastabos', g[5], b=True, shade='D9D9D9'))]
    for s in steps:
        if len(s) < 3:
            die('TA %s žingsnyje per mažai langelių: %s' % (nr, s))
        rows.append(tr(c(s[0], g[0]) + c(s[1], g[1]) + c(s[2], g[2] + g[3], 2)
                       + c(s[3] if len(s) > 3 else '', g[4]) + c(s[4] if len(s) > 4 else '', g[5])))
    rows.append(tr(c(post, sum(g), 6, label='Sąlygos po: ',
                     extra=cell_list(doc, post_lines, 'TA %s sąlygos po' % nr, sz))))
    rows[-1] = keep_next(rows[-1])  # pavadinimas po lentele – su paskutine eilute
    tbl = ('<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="%d" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="85" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar>'
           '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" '
           'w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid>%s</w:tblGrid>%s</w:tbl>'
           % (sum(g), ''.join('<w:gridCol w:w="%d"/>' % x for x in g), ''.join(rows)))
    return bookmark(doc, bookmark(doc, tbl, bm), anchor_name('r', 'TA' + nr)) + cap


# ---------------------------------------------------------------- skyriai (puslapio orientacija)
def sect_xml(sect_tpl, landscape, first):
    s = sect_tpl
    if not first:
        s = s.replace('<w:titlePg/>', '')
        s = re.sub(r'<w:pgNumType [^>]*/>', '', s)
    if landscape:
        s = re.sub(r'<w:pgSz [^>]*/>', '<w:pgSz w:w="%d" w:h="%d" w:orient="landscape"/>' % (PG_H, PG_W), s)
    return s


# ---------------------------------------------------------------- Markdown apdorojimas
def collect_labels(md):
    """Pirmas perėjimas: paveikslų ir lentelių numeriai pagal žymes."""
    labels = {}
    n = {'pav': 0, 'lent': 0}
    for line in md.split('\n'):
        s = line.strip()
        if s.startswith('!['):
            n['pav'] += 1
            m = re.search(r'#(pav:[\w-]+)', s)
            if m:
                labels[m.group(1)] = n['pav']
        elif s.startswith('Lentelė:') or s.startswith('::: reikalavimas') or s.startswith('::: ta '):
            n['lent'] += 1
            m = re.search(r'#(lent:[\w-]+)', s)
            if m:
                labels[m.group(1)] = n['lent']
    return labels


LIST_RE = re.compile(r'^(\s*)([-*] |\d+\. )')
HARD_BR = re.compile(r'\S {2,}$')


def join_lines(parts):
    """Sujungia eilutes į vieną pastraipą; eilutė su 2 tarpais gale – eilutės lūžis."""
    out = ''
    for i, p in enumerate(parts):
        if i:
            out += '<br>' if HARD_BR.search(parts[i - 1]) else ' '
        out += p.strip()
    return out.strip()


ID_RE = r'(?:(?:N?FR|PR) \d+(?:\.\d+)+|EKRANAS\d{2}|PA\d+|TA\d+|DS\d+|P\d+|E\d)'
ID_HEAD = re.compile(r'^(' + ID_RE + r')\b')


def collect_anchors(doc, md):
    """Pirmas perėjimas: skyrių numeriai, ID su žymėmis ir šaltinių skaičius."""
    h = [0, 0, 0, 0]
    doc.secs_appendix = set()
    in_src = False
    tables = []
    for line in md.split('\n'):
        s = line.strip()
        m = re.match(r'^(#{1,5})\s+(.*)$', s)
        if m:
            lv, t = len(m.group(1)), m.group(2)
            in_src = t.startswith('Šaltiniai')
            if lv == 5:
                mm = ID_HEAD.match(t)
                if mm:
                    doc.ids.add(mm.group(1))
            elif t.endswith('{-}'):
                mp = re.match(r'^(\d+) priedas', t)
                if mp:
                    doc.secs_appendix.add(mp.group(1))
            else:
                h[lv - 1] += 1
                for k in range(lv, 4):
                    h[k] = 0
                doc.secs.add('.'.join(str(x) for x in h[:lv]))
            continue
        mr = re.match(r'::: reikalavimas\s+((?:N?FR|PR) [\d.]+)\s', s)
        if mr:
            doc.ids.add(mr.group(1))
        mt = re.match(r'::: ta\s+(\d+)', s)
        if mt:
            doc.ids.add('TA' + mt.group(1))
        if in_src and re.match(r'^\d+\. ', s):
            doc.sources += 1
        if s.startswith('|') and not re.match(r'^\|?\s*:?-{3,}', s):
            tables.append(split_row(s)[0])
    for c in tables:  # ID, kurie apibrėžiami tik lentelėse – pirmame stulpelyje, kur pasirodo pirmą kartą
        if re.fullmatch(ID_RE, c) and c not in doc.ids:
            doc.ids.add(c)
            doc.table_ids.add(c)


def convert(doc, md, sect_tpl):
    md = re.sub(r'<!--.*?-->', '', md, flags=re.S)
    doc.labels = collect_labels(md)
    collect_anchors(doc, md)
    lines = md.split('\n')
    out = []
    k = 0
    pending_caption = None
    first_section = True

    while k < len(lines):
        line = lines[k]
        s = line.strip()
        if not s:
            k += 1
            continue
        if s == '\\pagebreak':
            out.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
            k += 1
            continue
        if s.startswith('::: gulscias'):
            out.append('<w:p><w:pPr><w:sectPr>%s</w:sectPr></w:pPr></w:p>'
                       % sect_xml(sect_tpl, False, first_section))
            first_section = False
            doc.landscape = True
            k += 1
            continue
        if s == ':::' and doc.landscape:
            out.append('<w:p><w:pPr><w:sectPr>%s</w:sectPr></w:pPr></w:p>' % sect_xml(sect_tpl, True, False))
            doc.landscape = False
            k += 1
            continue
        if s.startswith('::: reikalavimas'):
            m = re.match(r'::: reikalavimas\s+((?:N?FR|PR) [\d.]+)\s+(\S+)\s*\|\s*(.+)$', s)
            if not m:
                die('blogas reikalavimo blokas: ' + s)
            body = []
            k += 1
            while lines[k].strip() != ':::':
                body.append(lines[k].strip())
                k += 1
            gap_before_table(out)
            out.append(requirement(doc, m.group(1), m.group(2), m.group(3).strip(), ' '.join(x for x in body if x)))
            k += 1
            continue
        if s.startswith('::: ta '):
            m = re.match(r'::: ta\s+(\d+)\s*\|\s*(.+)$', s)
            body = []
            k += 1
            while lines[k].strip() != ':::':
                body.append(lines[k])
                k += 1
            gap_before_table(out)
            out.append(test_case(doc, m.group(1), m.group(2).strip(), body))
            k += 1
            continue
        m = re.match(r'^(#{1,5})\s+(.*)$', s)
        if m:
            out.append(heading(doc, len(m.group(1)), m.group(2)))
            k += 1
            continue
        m = re.match(r'^!\[(.+)\]\(([^)]+)\)(\{[^}]*\})?$', s)
        if m:
            out.append(figure(doc, m.group(1), m.group(2), (m.group(3) or '')[1:-1]))
            k += 1
            continue
        if s.startswith('Lentelė:'):
            pending_caption = s[len('Lentelė:'):].strip()
            k += 1
            continue
        if s.startswith('|'):
            tl = []
            while k < len(lines) and lines[k].strip().startswith('|'):
                tl.append(lines[k])
                k += 1
            if pending_caption is None:
                die('lentelė be pavadinimo: ' + tl[0])
            gap_before_table(out)
            out.append(table(doc, pending_caption, tl))
            pending_caption = None
            continue
        if LIST_RE.match(line):
            items = []
            base = len(LIST_RE.match(line).group(1))
            while True:
                mm = LIST_RE.match(lines[k])
                ind = len(mm.group(1))
                parts = [lines[k][mm.end():]]
                k += 1
                # tęsinys: eilutė su įtrauka arba (po eilutės lūžio) eilutė ne mažesne įtrauka nei punkto
                while k < len(lines) and lines[k].strip() and not LIST_RE.match(lines[k]) and (
                        len(lines[k]) - len(lines[k].lstrip()) > ind or
                        HARD_BR.search(parts[-1]) and len(lines[k]) - len(lines[k].lstrip()) >= ind):
                    parts.append(lines[k])
                    k += 1
                marker = mm.group(2).strip()
                numbered = marker[0].isdigit()
                restart = numbered and int(marker[:-1]) == 1 and bool(items)
                items.append((1 if ind > base else 0, numbered, restart, join_lines(parts)))
                # tuščios eilutės tarp punktų sąrašo nenutraukia
                j = k
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and LIST_RE.match(lines[j]):
                    k = j
                    continue
                break
            nums = {}
            for lvl, numbered, restart, text in items:
                key = (lvl, numbered)
                if key not in nums or restart:
                    nums[key] = new_num(doc, ABS_DECIMAL if numbered else ABS_BULLET)
                for kk in list(nums):
                    if kk[0] > lvl:
                        del nums[kk]
                x = list_par(doc, text, nums[key], lvl)
                if doc.in_sources and numbered and lvl == 0:
                    doc.src_n += 1
                    x = bookmark(doc, x, anchor_name('src', str(doc.src_n)))
                out.append(x)
            continue
        # pastraipa
        buf = [line]
        k += 1
        while k < len(lines) and lines[k].strip() and not re.match(
                r'^(#{1,5}\s|!\[|\||Lentelė:|:::|\\pagebreak|[-*] |\d+\. )', lines[k].strip()):
            buf.append(lines[k])
            k += 1
        out.append(para(doc, join_lines(buf)))
    if doc.landscape:
        die('neuždarytas ::: gulscias blokas')
    return ''.join(out), first_section


# ---------------------------------------------------------------- stiliai ir numeracija
# Stilių sistema (sprendimas 2026-11-21): pagrindinis tekstas – Normal, kiti stiliai paveldi jį.
# Šablono stiliai, kurie keičiami arba nenaudojami, pašalinami ir apibrėžiami iš naujo (STYLES).
# Titulinio lapo stiliai Normal nepaveldi: jie lieka su šablono numatytuoju formatavimu (docDefaults),
# todėl titulinis lapas atrodo kaip šablone.
CM14 = 794                      # 1,4 cm pirmos eilutės įtrauka
TNR = '<w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'


def _sz(n):
    return '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (n, n)


def _sp(before=0, after=0):
    return '<w:spacing w:before="%d" w:after="%d" w:line="240" w:lineRule="auto"/>' % (before, after)


def _style(sid, name, ppr='', rpr='', based='Normal', typ='paragraph', custom=True, extra=''):
    """Stiliaus apibrėžimas (elementų tvarka pagal OOXML schemą)."""
    return ('<w:style w:type="%s"%s w:styleId="%s"><w:name w:val="%s"/>%s%s<w:qFormat/>%s%s</w:style>'
            % (typ, ' w:customStyle="1"' if custom else '', sid, name,
               '<w:basedOn w:val="%s"/>' % based if based else '', extra,
               '<w:pPr>%s</w:pPr>' % ppr if ppr else '', '<w:rPr>%s</w:rPr>' % rpr if rpr else ''))


def _num(ilvl):
    return '<w:numPr><w:ilvl w:val="%d"/><w:numId w:val="1"/></w:numPr>' % ilvl


def _ind(left, hanging):
    return '<w:ind w:left="%d" w:hanging="%d"/>' % (left, hanging)


# antraščių įtraukos: (kairė, kabanti) – numeris nuo kairė−kabanti, tekstas ir kitos eilutės nuo kairė
HEAD_IND = {1: (567, 567), 2: (851, 851), 3: (CM14 + 1134, 1134), 4: (CM14 + 1134, 1134)}
TOC_W = TEXT_W - 10
DOT_TAB = '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="%d"/></w:tabs>' % TOC_W
NEXT = '<w:next w:val="Normal"/>'
HEAD_PPR = '<w:keepNext/><w:keepLines/>'

STYLES = ''.join([
    # pagrindinis tekstas
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>'
    '<w:pPr>%s<w:ind w:firstLine="%d"/><w:jc w:val="both"/></w:pPr><w:rPr>%s%s%s</w:rPr></w:style>'
    % (_sp(), CM14, TNR, _sz(24), LANG),
    # antraštės (numeracija – abstractNum 1, žr. patch_numbering)
    _style('Heading1', 'heading 1', HEAD_PPR + '<w:pageBreakBefore/>' + _num(0) + _sp(0, 240) + _ind(*HEAD_IND[1])
           + '<w:jc w:val="left"/><w:outlineLvl w:val="0"/>', '<w:b/><w:bCs/><w:caps/>' + _sz(36), custom=False, extra=NEXT),
    _style('Heading2', 'heading 2', HEAD_PPR + _num(1) + _sp(360, 120) + _ind(*HEAD_IND[2])
           + '<w:jc w:val="left"/><w:outlineLvl w:val="1"/>', '<w:b/><w:bCs/>' + _sz(32), custom=False, extra=NEXT),
    _style('Heading3', 'heading 3', HEAD_PPR + _num(2) + _sp(240, 120) + _ind(*HEAD_IND[3])
           + '<w:jc w:val="left"/><w:outlineLvl w:val="2"/>', '<w:b/><w:bCs/><w:i/><w:iCs/>' + _sz(28), custom=False, extra=NEXT),
    _style('Heading4', 'heading 4', HEAD_PPR + _num(3) + _sp(240, 120) + _ind(*HEAD_IND[4])
           + '<w:jc w:val="left"/><w:outlineLvl w:val="3"/>', '<w:i/><w:iCs/>' + _sz(24), custom=False, extra=NEXT),
    _style('Heading5', 'heading 5', HEAD_PPR + _sp(120, 60) + '<w:ind w:firstLine="0"/><w:jc w:val="left"/>'
           '<w:outlineLvl w:val="4"/>', '<w:b/><w:bCs/>', custom=False, extra=NEXT),
    _style('Heading1Benumerio', 'Antraštė 1 be numerio', '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'
           '<w:ind w:left="0" w:firstLine="0"/>', based='Heading1', extra=NEXT),
    _style('Heading2Benumerio', 'Antraštė 2 be numerio', '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'
           '<w:ind w:left="0" w:firstLine="0"/>', based='Heading2', extra=NEXT),
    # sąrašai (įtrauką nustato sąrašo lygis)
    _style('ListParagraph', 'List Paragraph', '<w:ind w:firstLine="0"/>', custom=False),
    _style('Saltiniusarasas', 'Šaltinių sąrašas', '<w:jc w:val="left"/>', based='ListParagraph'),
    # paveikslai, lentelės, pavadinimai
    _style('Caption', 'caption', '<w:keepLines/>' + _sp(60, 240) + '<w:ind w:firstLine="0"/><w:jc w:val="center"/>',
           '<w:i/><w:iCs/>' + _sz(22), custom=False, extra=NEXT),
    _style('Paveikslas', 'Paveikslas', '<w:keepNext/>' + _sp(120, 60) + '<w:ind w:firstLine="0"/><w:jc w:val="center"/>'),
    _style('Paveikslosaltiniai', 'Paveikslo šaltiniai', _sp() + '<w:ind w:firstLine="0"/><w:jc w:val="center"/>', _sz(18)),
    _style('Lentelestekstas', 'Lentelės tekstas', _sp(20, 20) + '<w:ind w:firstLine="0"/><w:jc w:val="left"/>', _sz(20)),
    _style('Lentelesantraste', 'Lentelės antraštė', '<w:keepNext/>', '<w:b/><w:bCs/>', based='Lentelestekstas'),
    _style('Reikalavimotekstas', 'Reikalavimo tekstas', _sp(40, 40) + '<w:ind w:firstLine="0"/>'),
    # turinys
    _style('Turinioantraste', 'Turinio antraštė', '<w:keepNext/>' + _sp(0, 240) + '<w:ind w:firstLine="0"/><w:jc w:val="center"/>',
           '<w:b/><w:bCs/><w:caps/>' + _sz(28), extra=NEXT),
    _style('TOC1', 'toc 1', DOT_TAB + _sp(120, 0) + _ind(567, 567) + '<w:jc w:val="left"/>', '<w:b/><w:bCs/><w:caps/>',
           custom=False, extra=NEXT),
    _style('TOC2', 'toc 2', DOT_TAB + _sp() + _ind(1134, 850) + '<w:jc w:val="left"/>', custom=False, extra=NEXT),
    _style('TOC3', 'toc 3', DOT_TAB + _sp() + _ind(1701, 1134) + '<w:jc w:val="left"/>', custom=False, extra=NEXT),
    # poraštė ir antraštė (puslapio numeris)
    _style('Header', 'header', '<w:tabs><w:tab w:val="center" w:pos="4153"/><w:tab w:val="right" w:pos="8306"/></w:tabs>'
           + _sp() + '<w:ind w:firstLine="0"/><w:jc w:val="left"/>', custom=False),
    _style('Footer', 'footer', '<w:tabs><w:tab w:val="center" w:pos="4153"/><w:tab w:val="right" w:pos="8306"/></w:tabs>'
           + _sp() + '<w:ind w:firstLine="0"/><w:jc w:val="left"/>', custom=False),
    # simbolių stiliai
    _style('Kodas', 'Kodas', rpr='<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:i w:val="0"/>'
           '<w:iCs w:val="0"/>' + _sz(21) + '<w:shd w:val="clear" w:color="auto" w:fill="E8EDF4"/>',
           based='DefaultParagraphFont', typ='character'),
    _style('KodasLenteleje', 'Kodas lentelėje', rpr='<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
           '<w:i w:val="0"/><w:iCs w:val="0"/>', based='DefaultParagraphFont', typ='character'),
    _style('Vidinenuoroda', 'Vidinė nuoroda', rpr='<w:color w:val="1F4E79"/>', based='DefaultParagraphFont', typ='character'),
    # titulinis lapas: be Normal paveldėjimo (šablono numatytasis formatavimas), lygiuotė – stiliuje
    _style('Titulinislapas', 'Titulinis lapas', based=None),
] + [_style(sid, name, '<w:jc w:val="%s"/>' % jc, based='Titulinislapas') for sid, name, jc in [
    ('Titulinisinstitucija', 'Titulinis – institucija', 'center'),
    ('Titulinispavadinimas', 'Titulinis – pavadinimas', 'center'),
    ('Titulinislaukas', 'Titulinis – laukas', 'right'),
    ('Titulinisreiksme', 'Titulinis – reikšmė', 'center'),
    ('Titulinispaaiskinimas', 'Titulinis – paaiškinimas', 'center'),
    ('Titulinistarpas', 'Titulinis – tarpas', 'center'),
    ('Titulinisvieta', 'Titulinis – vieta ir metai', 'center')]])

# šablono stiliai, kurie apibrėžiami iš naujo arba nenaudojami (pašalinami)
DROP_STYLES = re.compile(r'^(Normal|Heading\dChar|Heading\d|Magistro.*|StyleMagistro.*|Sutarties.*|Literatra1|Paskaitos.*'
                         r'|Terminas.*|Baktekstas|Title|TitleChar|Author|Address|AbstractText|Baigiamojodarbotekstas'
                         r'|BodyText|BodyTextChar|TOC[123]|ListParagraph|Header|HeaderChar|Footer|FooterChar|Caption)$')

ABSTRACTS = (
    '<w:abstractNum w:abstractNumId="%d"><w:multiLevelType w:val="hybridMultilevel"/>' % ABS_BULLET
    + ''.join('<w:lvl w:ilvl="%d"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="%s"/>'
              '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="%d" w:hanging="357"/></w:pPr>'
              '<w:rPr><w:rFonts w:ascii="%s" w:hAnsi="%s" w:hint="default"/></w:rPr></w:lvl>'
              % (lv, sym, left, font, font)
              for lv, sym, left, font in [(0, '', 1077, 'Symbol'), (1, 'o', 1434, 'Courier New'),
                                          # 2–4 lygiai – punktai lentelės langelyje
                                          (2, '', 357, 'Symbol'), (3, 'o', 714, 'Courier New'),
                                          (4, '', 1071, 'Wingdings')])
    + '</w:abstractNum>'
    + '<w:abstractNum w:abstractNumId="%d"><w:multiLevelType w:val="hybridMultilevel"/>' % ABS_DECIMAL
    + ''.join('<w:lvl w:ilvl="%d"><w:start w:val="1"/><w:numFmt w:val="%s"/><w:lvlText w:val="%s"/>'
              '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="%d" w:hanging="357"/></w:pPr></w:lvl>'
              % (lv, fmt, txt, left) for lv, fmt, txt, left in [(0, 'decimal', '%1.', 1077),
                                                                 (1, 'lowerLetter', '%2)', 1434)])
    + '</w:abstractNum>')


def patch_styles(xml):
    xml = xml.replace('<w:lang w:val="en-US"/>', '<w:lang w:val="lt-LT"/>')
    xml = re.sub(r'<w:style [^>]*w:styleId="([^"]+)"[^>]*>.*?</w:style>',
                 lambda m: '' if DROP_STYLES.match(m.group(1)) else m.group(0), xml, flags=re.S)
    xml = re.sub(r'<w:link w:val="(Heading\dChar|HeaderChar|FooterChar|TitleChar|BodyTextChar)"/>', '', xml)
    left = set(re.findall(r'<w:(?:basedOn|next|link) w:val="([^"]+)"', xml)) - set(re.findall(r'w:styleId="([^"]+)"', xml + STYLES))
    if left:
        die('stiliai nurodo pašalintus stilius: ' + ', '.join(sorted(left)))
    return xml.replace('</w:styles>', STYLES + '</w:styles>')


def heading_lvl(ilvl):
    left, hang = HEAD_IND[ilvl + 1]
    return ('<w:lvl w:ilvl="%d"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:pStyle w:val="Heading%d"/>%s'
            '<w:lvlText w:val="%s"/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="%d"/></w:tabs>%s</w:pPr>'
            '<w:rPr><w:rFonts w:hint="default"/></w:rPr></w:lvl>'
            % (ilvl, ilvl + 1, '<w:isLgl/>' if ilvl else '', '.'.join('%%%d' % (k + 1) for k in range(ilvl + 1)) + '.',
               left, _ind(left, hang)))


def patch_numbering(xml, nums):
    # antraščių numeracija (abstractNum 1, numId 1) susiejama su Heading1–Heading4
    m = re.search(r'<w:abstractNum [^>]*w:abstractNumId="1"[^>]*>.*?</w:abstractNum>', xml, re.S)
    an = m.group(0)
    for k in range(4):
        an = re.sub(r'<w:lvl w:ilvl="%d">.*?</w:lvl>' % k, lambda _: heading_lvl(k), an, count=1, flags=re.S)
    xml = xml[:m.start()] + an + xml[m.end():]
    # kiti šablono sąrašai nebesusieti su pašalintais stiliais
    xml = re.sub(r'<w:pStyle w:val="(?!Heading\d")[^"]*"/>', '', xml)
    # abstraktūs apibrėžimai turi eiti prieš <w:num>
    i = xml.index('<w:num ')
    xml = xml[:i] + ABSTRACTS + xml[i:]
    return xml.replace('</w:numbering>', ''.join(nums) + '</w:numbering>')


def paragraph_spans(xml):
    """(pradžia, pabaiga, gylis) kiekvienai <w:p> pastraipai, įskaitant įdėtas (teksto laukuose)."""
    out, stack = [], []
    for m in re.finditer(r'<w:p[ >]|</w:p>', xml):
        if m.group(0) == '</w:p>':
            st = stack.pop()
            out.append((st, m.end(), len(stack)))
        else:
            stack.append(m.start())
    return out


def title_role(p):
    """Titulinio lapo pastraipos stilius pagal jos turinį."""
    if 'txbxContent' in p or '<w:drawing' in p or '<w:pict' in p:
        return 'Titulinislapas'                      # logotipas, teksto lauko inkaras
    t = ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p)).strip()
    if not t:
        return 'Titulinistarpas'
    if re.search(r'UNIVERSITETAS|FAKULTETAS|STUDIJŲ PROGRAMA', t):
        return 'Titulinisinstitucija'
    if t.endswith(':'):
        return 'Titulinislaukas'
    if t.startswith('('):
        return 'Titulinispaaiskinimas'
    if t.startswith('Vilnius'):
        return 'Titulinisvieta'
    return 'Titulinisreiksme'


def style_jc(sid):
    m = re.search(r'w:styleId="%s".*?</w:style>' % sid, STYLES, re.S)
    j = re.search(r'<w:jc w:val="(\w+)"/>', m.group(0))
    return j.group(1) if j else 'left'


def set_par_style(p, sid, keep_jc=True):
    """Pastraipai priskiria stilių; tiesioginė lygiuotė paliekama tik jei skiriasi nuo stiliaus."""
    head = re.match(r'<w:p(?: [^>]*)?>', p).group(0)
    rest = p[len(head):]
    m = re.match(r'<w:pPr>(.*?)</w:pPr>', rest, re.S) if rest.startswith('<w:pPr>') else None
    ppr = m.group(1) if m else ''
    tail = rest[m.end():] if m else rest
    ppr = re.sub(r'<w:pStyle w:val="[^"]*"/>', '', ppr)
    rpr = re.search(r'<w:rPr>.*?</w:rPr>', ppr, re.S)
    rpr = rpr.group(0) if rpr else ''
    body = ppr.replace(rpr, '') if rpr else ppr
    if keep_jc:
        j = re.search(r'<w:jc w:val="(\w+)"/>', body)
        cur = j.group(1) if j else 'left'
        body = re.sub(r'<w:jc w:val="\w+"/>', '', body)
        if cur != style_jc(sid):
            body += '<w:jc w:val="%s"/>' % cur
    return '%s<w:pPr><w:pStyle w:val="%s"/>%s%s</w:pPr>%s' % (head, sid, body, rpr, tail)


def patch_title(xml):
    # Sistemos pavadinimas yra du kartus (teksto laukas ir jo VML atsarginė kopija); geltonas žymėjimas pašalinamas
    n = xml.count('Sistemos pavadinimas')
    if n != 2:
        die('šablone „Sistemos pavadinimas“ rasta %d kartų' % n)
    xml = xml.replace('Sistemos pavadinimas', SISTEMA)
    xml = xml.replace('<w:highlight w:val="yellow"/>', '')
    # titulinio lapo ir turinio antraštės pastraipoms – savi stiliai (iki „TURINYS“ imtinai)
    toc = xml.index('>TURINYS<')
    spans = paragraph_spans(xml)
    edits = []
    for a, b, depth in spans:
        if a > toc:
            continue
        p = xml[a:b]
        if '>TURINYS<' in p:
            sid = 'Turinioantraste'
        elif depth > 0:
            sid = 'Titulinispavadinimas'             # teksto lauko vidus
        else:
            sid = title_role(p)
        edits.append((a, b, sid))
    # nuo galo; pastraipoje su įdėtomis pastraipomis keičiama tik jos pradžia (<w:p> ir <w:pPr>),
    # nes įdėtos (esančios toliau) jau pakeistos ir jos pabaigos vieta pasislinkusi
    for a, b, sid in sorted(edits, reverse=True):
        if len(re.findall(r'<w:p[ >]', xml[a:b])) > 1:
            head = re.match(r'<w:p(?: [^>]*)?>', xml[a:]).group(0)
            e = a + len(head)
            if xml.startswith('<w:pPr>', e):
                e = xml.index('</w:pPr>', e) + len('</w:pPr>')
            xml = xml[:a] + set_par_style(xml[a:e] + '</w:p>', sid)[:-len('</w:p>')] + xml[e:]
        else:
            xml = xml[:a] + set_par_style(xml[a:b], sid) + xml[b:]
    return xml


# ---------------------------------------------------------------- pagrindinė dalis
def main():
    global SRC_MD, OUT
    if len(sys.argv) > 1:
        SRC_MD = os.path.abspath(sys.argv[1])
    if len(sys.argv) > 2:
        OUT = os.path.abspath(sys.argv[2])
    if not os.path.exists(TEMPLATE):
        die('nėra šablono kopijos ' + TEMPLATE)
    with zipfile.ZipFile(TEMPLATE) as z:
        files = {n: z.read(n) for n in z.namelist() if not n.endswith('/')}
    doc = Doc(files)
    xml = files['word/document.xml'].decode('utf-8')

    body_start = xml.index('<w:body>') + len('<w:body>')
    body_end = xml.index('</w:body>')
    body = xml[body_start:body_end]
    sect_m = re.search(r'<w:sectPr\b[^>]*>.*?</w:sectPr>\s*$', body, re.S)
    sect_tpl = re.sub(r'^<w:sectPr\b[^>]*>|</w:sectPr>$', '', sect_m.group(0).strip())
    # šablono dalis iki pirmos 1 lygio antraštės (titulinis lapas ir turinys) paliekama
    cut = body.index('<w:pStyle w:val="MagistrodarboHeading1"/>')
    cut = body.rindex('<w:p ', 0, cut)
    front = patch_title(body[:cut])

    md = open(SRC_MD, encoding='utf-8').read()
    content, first_left = convert(doc, md, sect_tpl)
    final_sect = sect_xml(sect_tpl, False, first_left)
    new_body = front + content + '<w:sectPr>%s</w:sectPr>' % final_sect
    xml = xml[:body_start] + new_body + xml[body_end:]
    files['word/document.xml'] = xml.encode('utf-8')

    # eilutė prieš rankinį lūžį (<br>) lygiuojamame abiem pusėms tekste neištempiama
    st = files['word/settings.xml'].decode('utf-8')
    if '<w:doNotExpandShiftReturn/>' not in st:
        st = st.replace('<w:compat>', '<w:compat><w:doNotExpandShiftReturn/>', 1)
    files['word/settings.xml'] = st.encode('utf-8')
    files['word/styles.xml'] = patch_styles(files['word/styles.xml'].decode('utf-8')).encode('utf-8')
    files['word/numbering.xml'] = patch_numbering(files['word/numbering.xml'].decode('utf-8'),
                                                  doc.numbering_nums).encode('utf-8')
    rels = files['word/_rels/document.xml.rels'].decode('utf-8')
    add = ''.join('<Relationship Id="%s" Type="%s" Target="%s"%s/>'
                  % (r, t, escape(tg, {'"': '&quot;'}), ' TargetMode="External"' if ext else '')
                  for r, t, tg, ext in doc.rels)
    files['word/_rels/document.xml.rels'] = rels.replace('</Relationships>', add + '</Relationships>').encode('utf-8')
    ct = files['[Content_Types].xml'].decode('utf-8')
    for ext, typ in [('png', 'image/png')]:
        if 'Extension="%s"' % ext not in ct:
            ct = ct.replace('<Override ', '<Default Extension="%s" ContentType="%s"/><Override ' % (ext, typ), 1)
    files['[Content_Types].xml'] = ct.encode('utf-8')

    tmp = OUT + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
        order = ['[Content_Types].xml'] + [n for n in files if n != '[Content_Types].xml']
        for n in order:
            z.writestr(n, files[n])
    os.replace(tmp, OUT)
    if doc.unresolved:
        print('Įspėjimas: ID be žymės (nesusieti): ' + ', '.join('%s×%d' % kv for kv in sorted(doc.unresolved.items())))
    missing = doc.ids - doc.defined
    if missing:
        die('žymės nesukurtos: ' + ', '.join(sorted(missing)))
    print('Surinkta: %s (%d pav., %d lent., %d nuorodos į šaltinio failus, %.1f MB)'
          % (os.path.relpath(OUT, ROOT), doc.counters['pav'], doc.counters['lent'], doc.link_count,
             os.path.getsize(OUT) / 1e6))


if __name__ == '__main__':
    main()
