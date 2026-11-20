#!/usr/bin/env python3
"""Ataskaitos surinkimas: ataskaita/ataskaita.md + šablono kopija -> .docx.

Naudojimas (iš saugyklos šaknies): python3 ataskaita/irankiai/surinkti.py
Paskui `ataskaita/irankiai/word.sh` atnaujina turinį Word programoje ir išsaugo PDF.

Šablono kopijos (ataskaita/sablono-kopija.docx) imamas titulinis lapas, turinys, stiliai,
poraštė ir puslapio parametrai; visa šablono dalis po turiniu (gairės) pakeičiama
sugeneruotu turiniu. Naudojama tik standartinė Python biblioteka.

ataskaita.md sintaksė (Markdown poaibis):
  # 1. Sistemos analizė            antraštės 1–4 lygio; numeris tikrinamas su automatine numeracija
  ##### E1. Paieška                 paryškinta pastraipa (5 lygis, be numeracijos)
  # Šaltiniai {-}                   antraštė be numerio
  - punktas / 1. punktas            sąrašai (įtrauka 2 tarpais – antras lygis)
  Lentelė: Pavadinimas {#lent:id plotis=1,2,3 maza}
  | a | b |                         lentelė (pirma eilutė – antraštė)
  ![Pavadinimas {#pav:id}](kelias.png){plotis=16 aukstis=20 failai=a.drawio,b.png}
                                    failai= – šaltinio failai; po paveikslu rodomos jų piktogramos su
                                    nuorodomis į failus viešoje GitHub saugykloje (main šaka)
  ::: reikalavimas 1.2.1 funkcinis | Pavadinimas    ... :::
  ::: ta 1 | Pavadinimas  (Aprašymas:, Pradiniai duomenys (sąlygos prieš):, žingsnių lentelė)  :::
  ::: gulscias ... :::              gulsčias puslapis (atskiras skyrius)
  \\pagebreak                        naujas puslapis
  @pav:id, @lent:id                 nuoroda į paveikslo ar lentelės numerį
  **paryškinta**, *pasvira*, `kodas`, <u>pabraukta</u>, <ud>pabraukta punktyru</ud>, [tekstas](url), <br>
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
OUT = os.path.join(ROOT, 'ataskaita', 'MotoNuoma_IS_ataskaita.docx')
SISTEMA = 'MotoNuoma'
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
                    r'|<u>(?P<u>.+?)</u>|<ud>(?P<ud>.+?)</ud>|\[(?P<lt>[^\]]+)\]\((?P<lu>https?://[^)]+)\)'
                    r'|(?P<br><br>)|@(?P<ref>(?:pav|lent):[\w-]+))')


def run(text, b=False, i=False, code=False, u=None, sz=None, color=None, style=None):
    rpr = ''
    if style:
        rpr += '<w:rStyle w:val="%s"/>' % style
    if code:
        rpr += '<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>'
    if b:
        rpr += '<w:b/><w:bCs/>'
    if i:
        rpr += '<w:i/><w:iCs/>'
    if color:
        rpr += '<w:color w:val="%s"/>' % color
    if sz:
        rpr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz)
    elif code:
        rpr += '<w:sz w:val="21"/><w:szCs w:val="21"/>'
    if u:
        rpr += '<w:u w:val="%s"/>' % u
    rpr += LANG
    return '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, escape(text))


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
            out.append(run(g['c'], b=b, i=i, code=True, sz=(sz - 1 if sz else None)))
        elif g['i'] is not None:
            out.append(inline(doc, g['i'], b=b, i=True, sz=sz))
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
            out.append(run(str(doc.labels[g['ref']]), b=b, i=i, sz=sz))
        pos = m.end()
    if pos < len(text):
        out.append(run(text[pos:], b=b, i=i, sz=sz))
    return ''.join(out)


def para(doc, text, style='Magistrodarbotekstas', ppr_extra='', b=False, i=False, sz=None, jc='both',
         first_line=None, spacing='<w:spacing w:line="360" w:lineRule="auto"/>'):
    ind = '' if first_line is None else '<w:ind w:firstLine="%d"/>' % first_line
    jcx = '<w:jc w:val="%s"/>' % jc if jc else ''
    return ('<w:p><w:pPr><w:pStyle w:val="%s"/>%s%s%s%s<w:rPr>%s</w:rPr></w:pPr>%s</w:p>'
            % (style, ppr_extra, spacing, ind, jcx, LANG, inline(doc, text, b=b, i=i, sz=sz)))


# ---------------------------------------------------------------- antraštės
HEAD_STYLES = {1: 'MagistrodarboHeading1', 2: 'MagistrodarboHeading2',
               3: 'StyleMagistrodarboHeading3Linespacing15lines', 4: 'MagistrodarboHeading4'}


def heading(doc, level, text):
    nonum = text.endswith('{-}')
    text = text.replace('{-}', '').strip()
    if level == 5:
        return para(doc, text, b=True, ppr_extra='<w:keepNext/>', first_line=0, jc='left',
                    spacing='<w:spacing w:before="120" w:line="360" w:lineRule="auto"/>')
    # šablono MagistrodarboHeading3 stilius išjungia „keep with next“, o 4 lygis per jį paveldi
    # 3 lygio struktūrą ir patenka į TURINĮ (\o "1-3"), todėl abu dalykai nurodomi tiesiogiai
    extra = '<w:keepNext/>'
    if level == 1:
        extra += '<w:pageBreakBefore/>'
    if nonum:
        extra += '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr><w:ind w:left="0" w:firstLine="0"/>'
    else:
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
    if level == 1 and not nonum:
        text = text.upper()
    olvl = '<w:outlineLvl w:val="3"/>' if level == 4 else ''
    return ('<w:p><w:pPr><w:pStyle w:val="%s"/>%s%s<w:rPr>%s</w:rPr></w:pPr>%s</w:p>'
            % (HEAD_STYLES[level], extra, olvl, LANG, inline(doc, text)))


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
    sp = ('<w:spacing w:after="0" w:line="240" w:lineRule="auto"/>' if in_table
          else '<w:spacing w:line="360" w:lineRule="auto"/>')
    style = 'Lentelestekstas' if in_table else 'Magistrodarbotekstas'
    return ('<w:p><w:pPr><w:pStyle w:val="%s"/><w:numPr><w:ilvl w:val="%d"/><w:numId w:val="%d"/></w:numPr>'
            '%s<w:jc w:val="%s"/><w:rPr>%s</w:rPr></w:pPr>%s</w:p>'
            % (style, ilvl, num_id, sp, 'left' if in_table or 'http' in text else 'both', LANG,
               inline(doc, text, sz=sz)))


# ---------------------------------------------------------------- paveikslai ir šaltinio failų nuorodos
def caption(doc, kind, text, keep_next=False):
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
    jc = 'center' if kind == 'pav' else 'left'
    kn = '<w:keepNext/>' if keep_next else ''
    xml = ('<w:p><w:pPr><w:pStyle w:val="Caption"/>%s<w:jc w:val="%s"/><w:rPr>%s</w:rPr></w:pPr>'
           '<w:fldSimple w:instr=" SEQ %s \\* ARABIC \\* MERGEFORMAT "><w:r><w:rPr><w:b/>%s</w:rPr><w:t>%d</w:t></w:r></w:fldSimple>'
           '%s%s</w:p>' % (kn, jc, LANG, seq, LANG, n, run(' ' + word, b=True), inline(doc, ' ' + text)))
    return xml, opts


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
            '<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Paveikslas"/>'
            '<w:keepNext/><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>'
            '</w:pPr>%s</w:p></w:tc>' % (cw, c) for c in cells)
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
    xml = ('<w:p><w:pPr><w:pStyle w:val="Paveikslas"/><w:keepNext/><w:jc w:val="center"/></w:pPr>%s</w:p>'
           % picture(doc, path, w, h, clean_cap))
    att = [a for a in o.get('failai', '').split(',') if a]
    cap, _ = caption(doc, 'pav', cap_text, keep_next=bool(att))
    xml += cap
    if att:
        objs = []
        for a in att:
            ap = os.path.normpath(os.path.join(os.path.dirname(SRC_MD), a))
            if not os.path.exists(ap):
                die('nėra šaltinio failo ' + ap)
            objs.append(source_link(doc, ap))
        xml += ('<w:p><w:pPr><w:pStyle w:val="Paveikslas"/><w:keepNext/><w:spacing w:before="60" w:after="60"/>'
                '<w:jc w:val="center"/></w:pPr>%s</w:p>'
                % run('Šaltinio failai GitHub saugykloje (atidaromi spustelėjus):', i=True, sz=18))
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
        paras.append('<w:p><w:pPr><w:pStyle w:val="Lentelestekstas"/>%s<w:rPr>%s</w:rPr></w:pPr>%s</w:p>'
                     % ('<w:keepNext/>' if header else '', LANG, inline(doc, text, b=header or bold, sz=sz)))
    return '<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>' % (tcpr, ''.join(paras))


def table(doc, cap_text, lines):
    cap_xml, opts = caption(doc, 'lent', cap_text, keep_next=True)
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
    out = [cap_xml, '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="%d" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="85" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar>'
           '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
           '</w:tblPr><w:tblGrid>%s</w:tblGrid>' % (total, grid)]
    short = len(rows) <= SHORT_TABLE
    start = len(out)
    for k, r in enumerate(rows):
        hdr = k == 0
        trpr = '<w:trPr><w:cantSplit/>%s</w:trPr>' % ('<w:tblHeader/>' if hdr else '')
        nonempty = [c for c in r if c]
        if not hdr and len(nonempty) == 1 and not r[0] and n > 2:
            # grupės eilutė: vienas tekstas per visą plotį
            out.append('<w:tr>%s%s</w:tr>' % (trpr, cell(doc, nonempty[0], total, sz, span=n, shade='F2F2F2')))
            continue
        out.append('<w:tr>%s%s</w:tr>' % (trpr, ''.join(
            cell(doc, c, ws[j], sz, header=hdr, shade='D9D9D9' if hdr else None) for j, c in enumerate(r))))
    if short:  # visos eilutės, išskyrus paskutinę, laikomos su kita
        out[start:-1] = [keep_next(x) for x in out[start:-1]]
    out.append('</w:tbl>')
    out.append(spacer())
    return ''.join(out)


SHORT_TABLE = 15


def keep_next(xml):
    return re.sub(r'(<w:pStyle w:val="[^"]*"/>)(?!<w:keepNext/>)', r'\1<w:keepNext/>', xml)


def spacer():
    return '<w:p><w:pPr><w:pStyle w:val="Lentelestekstas"/><w:spacing w:after="120"/></w:pPr></w:p>'


def tpl_par(doc, text_runs, bold=False, keep=False):
    return ('<w:p><w:pPr><w:pStyle w:val="Magistrodarbotekstas"/>' + ('<w:keepNext/>' if keep else '') +
            '<w:spacing w:line="360" w:lineRule="auto"/>'
            '<w:ind w:firstLine="0"/><w:jc w:val="both"/><w:rPr>%s%s</w:rPr></w:pPr>%s</w:p>'
            % ('<w:b/>' if bold else '', LANG, text_runs))


def requirement(doc, nr, typ, name, text):
    cap, _ = caption(doc, 'lent', '%s %s' % (nr, name), keep_next=True)
    w1, w2 = TEXT_W // 2, TEXT_W - TEXT_W // 2
    tc = lambda w, body, span='': ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr>%s</w:tc>'
                                   % (w, span, body))
    r1 = (tc(w1, tpl_par(doc, run('Nr. ' + nr, b=True, i=True), keep=True)) +
          tc(w2, tpl_par(doc, run('Reikalavimo tipas: ' + typ, b=True, i=True), keep=True)))
    r2 = tc(TEXT_W, tpl_par(doc, run('Aprašymas: ', b=True, i=True) + inline(doc, text)),
            '<w:gridSpan w:val="2"/>')
    return (cap + '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="%d" w:type="dxa"/>'
            '<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
            'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid><w:gridCol w:w="%d"/>'
            '<w:gridCol w:w="%d"/></w:tblGrid><w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>'
            '<w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr></w:tbl>' % (TEXT_W, w1, w2, r1, r2) + spacer())


def test_case(doc, nr, name, block):
    cap, _ = caption(doc, 'lent', 'Testavimo atvejis Nr. %s „%s“' % (nr, name), keep_next=True)
    desc = pre = ''
    tlines = []
    for l in block:
        if l.startswith('Aprašymas:'):
            desc = l[len('Aprašymas:'):].strip()
        elif l.startswith('Pradiniai duomenys (sąlygos prieš):'):
            pre = l[len('Pradiniai duomenys (sąlygos prieš):'):].strip()
        elif l.strip().startswith('|'):
            tlines.append(l)
    steps = [split_row(l) for l in tlines if not re.match(r'^\s*\|?\s*:?-{3,}', l)][1:]
    # stulpeliai kaip šablone: Nr., žingsnis, laukiamas rezultatas (2 tinklelio stulpeliai), Pavyko?, Pastabos
    g = [543, 3344, 947, 2532, 1191, 1070]
    sz = 20

    def c(text, w, span=1, b=False, shade=None, label=None):
        tcpr = '<w:tcW w:w="%d" w:type="dxa"/>' % w
        if span > 1:
            tcpr += '<w:gridSpan w:val="%d"/>' % span
        if shade:
            tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade
        body = (run(label, b=True, sz=sz) if label else '') + inline(doc, text, b=b, sz=sz)
        return ('<w:tc><w:tcPr>%s</w:tcPr><w:p><w:pPr><w:pStyle w:val="Lentelestekstas"/><w:rPr>%s</w:rPr></w:pPr>'
                '%s</w:p></w:tc>' % (tcpr, LANG, body))
    tr = lambda cells, hdr=False: '<w:tr><w:trPr><w:cantSplit/>%s</w:trPr>%s</w:tr>' % (
        '<w:tblHeader/>' if hdr else '', cells)
    rows = [tr(c('Testavimo atvejo Nr. %s' % nr, sum(g[:3]), 3, b=True) + c(name, sum(g[3:]), 3, b=True)),
            tr(c(desc, sum(g), 6, label='Aprašymas: ')),
            tr(c(pre, sum(g), 6, label='Pradiniai duomenys (sąlygos prieš): ')),
            tr(c('Nr.', g[0], b=True, shade='D9D9D9') + c('Testavimo atvejo (scenarijaus) žingsnis', g[1], b=True, shade='D9D9D9')
               + c('Laukiamas rezultatas', g[2] + g[3], 2, b=True, shade='D9D9D9')
               + c('Pavyko gauti laukiamą rezultatą? (Taip/Ne)', g[4], b=True, shade='D9D9D9')
               + c('Klaidos, pastabos', g[5], b=True, shade='D9D9D9'))]
    for s in steps:
        if len(s) < 3:
            die('TA %s žingsnyje per mažai langelių: %s' % (nr, s))
        rows.append(tr(c(s[0], g[0]) + c(s[1], g[1]) + c(s[2], g[2] + g[3], 2)
                       + c(s[3] if len(s) > 3 else '', g[4]) + c(s[4] if len(s) > 4 else '', g[5])))
    return (cap + '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="%d" w:type="dxa"/>'
            '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="85" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar>'
            '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" '
            'w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid>%s</w:tblGrid>%s</w:tbl>'
            % (sum(g), ''.join('<w:gridCol w:w="%d"/>' % x for x in g), ''.join(rows)) + spacer())


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


def convert(doc, md, sect_tpl):
    md = re.sub(r'<!--.*?-->', '', md, flags=re.S)
    doc.labels = collect_labels(md)
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
            m = re.match(r'::: reikalavimas\s+([\d.]+)\s+(\S+)\s*\|\s*(.+)$', s)
            if not m:
                die('blogas reikalavimo blokas: ' + s)
            body = []
            k += 1
            while lines[k].strip() != ':::':
                body.append(lines[k].strip())
                k += 1
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
            out.append(table(doc, pending_caption, tl))
            pending_caption = None
            continue
        if re.match(r'^(\s*)(- |\d+\. )', line):
            items = []
            while k < len(lines) and re.match(r'^(\s*)(- |\d+\. )', lines[k]):
                mm = re.match(r'^(\s*)(- |\d+\. )(.*)$', lines[k])
                text = mm.group(3)
                k += 1
                while k < len(lines) and lines[k].strip() and not re.match(r'^(\s*)(- |\d+\. )', lines[k]) \
                        and lines[k].startswith('  '):
                    text += ' ' + lines[k].strip()
                    k += 1
                items.append((1 if mm.group(1) else 0, mm.group(2) != '- ', text))
            nums = {}
            for lvl, numbered, text in items:
                key = (lvl, numbered)
                if key not in nums:
                    nums[key] = new_num(doc, ABS_DECIMAL if numbered else ABS_BULLET)
                for kk in list(nums):
                    if kk[0] > lvl:
                        del nums[kk]
                out.append(list_par(doc, text, nums[key], lvl))
            continue
        # pastraipa
        buf = [s]
        k += 1
        while k < len(lines) and lines[k].strip() and not re.match(
                r'^(#{1,5}\s|!\[|\||Lentelė:|:::|\\pagebreak|\s*- |\s*\d+\. )', lines[k].strip()):
            buf.append(lines[k].strip())
            k += 1
        out.append(para(doc, ' '.join(buf)))
    if doc.landscape:
        die('neuždarytas ::: gulscias blokas')
    return ''.join(out), first_section


# ---------------------------------------------------------------- stiliai ir numeracija
EXTRA_STYLES = (
    '<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/>'
    '<w:next w:val="Magistrodarbotekstas"/><w:uiPriority w:val="35"/><w:unhideWhenUsed/><w:qFormat/>'
    '<w:pPr><w:spacing w:before="60" w:after="120" w:line="240" w:lineRule="auto"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="lt-LT"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Lentelestekstas"><w:name w:val="Lentelės tekstas"/>'
    '<w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="20"/><w:szCs w:val="20"/><w:lang w:val="lt-LT"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Paveikslas"><w:name w:val="Paveikslas"/>'
    '<w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="120" w:after="0" w:line="240" w:lineRule="auto"/>'
    '<w:jc w:val="center"/></w:pPr><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
    'w:cs="Times New Roman"/><w:lang w:val="lt-LT"/></w:rPr></w:style>')

ABSTRACTS = (
    '<w:abstractNum w:abstractNumId="%d"><w:multiLevelType w:val="hybridMultilevel"/>' % ABS_BULLET
    + ''.join('<w:lvl w:ilvl="%d"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="%s"/>'
              '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="%d" w:hanging="357"/></w:pPr>'
              '<w:rPr><w:rFonts w:ascii="%s" w:hAnsi="%s" w:hint="default"/></w:rPr></w:lvl>'
              % (lv, sym, left, font, font)
              for lv, sym, left, font in [(0, '', 1077, 'Symbol'), (1, 'o', 1434, 'Courier New'),
                                          (2, '', 357, 'Symbol')])
    + '</w:abstractNum>'
    + '<w:abstractNum w:abstractNumId="%d"><w:multiLevelType w:val="hybridMultilevel"/>' % ABS_DECIMAL
    + ''.join('<w:lvl w:ilvl="%d"><w:start w:val="1"/><w:numFmt w:val="%s"/><w:lvlText w:val="%s"/>'
              '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="%d" w:hanging="357"/></w:pPr></w:lvl>'
              % (lv, fmt, txt, left) for lv, fmt, txt, left in [(0, 'decimal', '%1.', 1077),
                                                                 (1, 'lowerLetter', '%2)', 1434)])
    + '</w:abstractNum>')


def patch_styles(xml):
    xml = xml.replace('<w:lang w:val="en-US"/>', '<w:lang w:val="lt-LT"/>')
    xml = re.sub(r'<w:style [^>]*w:styleId="Caption".*?</w:style>', '', xml, flags=re.S)
    # 4 lygio antraštė paveldi 3 lygio struktūrą (per MagistrodarboHeading3), todėl pateko į TURINĮ (\o "1-3")
    xml = re.sub(r'(<w:style [^>]*w:styleId="MagistrodarboHeading4".*?<w:pPr>)(.*?)(</w:pPr>)',
                 lambda m: m.group(1) + m.group(2) + '<w:outlineLvl w:val="3"/>' + m.group(3), xml, count=1, flags=re.S)
    return xml.replace('</w:styles>', EXTRA_STYLES + '</w:styles>')


def patch_numbering(xml, nums):
    # abstraktūs apibrėžimai turi eiti prieš <w:num>
    i = xml.index('<w:num ')
    xml = xml[:i] + ABSTRACTS + xml[i:]
    return xml.replace('</w:numbering>', ''.join(nums) + '</w:numbering>')


def patch_title(xml):
    # Sistemos pavadinimas yra du kartus (teksto laukas ir jo VML atsarginė kopija); geltonas žymėjimas pašalinamas
    n = xml.count('Sistemos pavadinimas')
    if n != 2:
        die('šablone „Sistemos pavadinimas“ rasta %d kartų' % n)
    xml = xml.replace('Sistemos pavadinimas', SISTEMA)
    return xml.replace('<w:highlight w:val="yellow"/>', '')


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
    print('Surinkta: %s (%d pav., %d lent., %d nuorodos į šaltinio failus, %.1f MB)'
          % (os.path.relpath(OUT, ROOT), doc.counters['pav'], doc.counters['lent'], doc.link_count,
             os.path.getsize(OUT) / 1e6))


if __name__ == '__main__':
    main()
