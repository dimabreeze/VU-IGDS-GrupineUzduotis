"""Iliustracijos funkcijų taisyklėms (draw.io).

Sugeneruoja keturias `.drawio` diagramas `artefaktai/` kataloge:

  12-sutapimas.drawio              – užimtumo laikotarpių sutapimas (2.2.1, „Bendros sąvokos“)
  08-buvimo-vietos-taisykle.drawio – motociklo buvimo vietos taisyklė (1.5.2.4, 2.2.1)
  12-lygiagreti-rezervacija.drawio – dvi vienu metu pateiktos rezervacijos (2.2.1, NFR 1.3.3.3)
  12-pavelavimas.drawio            – pavėluotas grąžinimas (2.2.1)

Datos ir laikai – tie patys kaip pavyzdžiuose `artefaktai/12-funkcijos.md`; pakeitus pavyzdį,
pakeičiamas ir šis skriptas. PNG eksportuojami `make diagramos`.
Paleidimas: python3 ataskaita/irankiai/iliustracijos.py (arba `make iliustracijos`).
"""
import html
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'artefaktai')

OCC = 'rounded=0;whiteSpace=wrap;html=1;fillColor=#fad7ac;strokeColor=#b46504;fontSize=11;'
BAD = 'rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=11;'
OK = 'rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;'
GHOST = 'rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;dashed=1;fontSize=11;fontColor=#666666;'
LANE = 'rounded=0;whiteSpace=wrap;html=1;strokeColor=none;'
TXT = 'text;html=1;whiteSpace=wrap;align=left;verticalAlign=middle;fontSize=12;'
TICK = 'align=center;fontSize=10;fontColor=#666666;'
VGRID = 'endArrow=none;html=1;strokeColor=#e6e6e6;'
AX = 'endArrow=classic;html=1;strokeColor=#333333;endSize=6;'
RED, GREEN, BROWN = '#b85450', '#4d7a3a', '#b46504'


class D:
    def __init__(self):
        self.cells, self.n = [], 1

    def _id(self):
        self.n += 1
        return 'c%d' % self.n

    def box(self, x, y, w, h, val='', style=TXT):
        i = self._id()
        self.cells.append(
            '<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%g" y="%g" width="%g" height="%g" as="geometry"/></mxCell>'
            % (i, html.escape(val), style, x, y, w, h))

    def text(self, x, y, w, h, val, extra=''):
        self.box(x, y, w, h, val, TXT + extra)

    def line(self, x1, y1, x2, y2, style=VGRID):
        i = self._id()
        self.cells.append(
            '<mxCell id="%s" value="" style="%s" edge="1" parent="1">'
            '<mxGeometry relative="1" as="geometry">'
            '<mxPoint x="%g" y="%g" as="sourcePoint"/><mxPoint x="%g" y="%g" as="targetPoint"/>'
            '</mxGeometry></mxCell>' % (i, style, x1, y1, x2, y2))

    def save(self, name):
        xml = ('<mxfile><diagram name="%s"><mxGraphModel><root><mxCell id="0"/>'
               '<mxCell id="1" parent="0"/>%s</root></mxGraphModel></diagram></mxfile>\n'
               % (name, ''.join(self.cells)))
        with open(os.path.join(OUT, name + '.drawio'), 'w', encoding='utf-8') as f:
            f.write(xml)


def sutapimas():
    """Esamas laikotarpis L ir keturi nauji laikotarpiai: du sutampa, du tik liečiasi."""
    d = D()
    X0, PD = 200, 70                     # 2027-05-11 00:00; 70 px per parą
    x = lambda h: X0 + h * PD / 24       # h – valandos nuo 2027-05-11 00:00
    rows = [80, 125, 170, 215, 260]
    top, bot = 60, 290
    for day in range(7):
        d.line(x(day * 24), top, x(day * 24), bot)
        d.text(x(day * 24) - 35, bot + 2, 70, 16, '2027-05-%02d' % (11 + day), TICK)
    d.line(X0, bot, x(150), bot, AX)
    for h, lab in ((34, 'L.pradžia<br>2027-05-12 10:00'), (106, 'L.pabaiga<br>2027-05-15 10:00')):
        d.line(x(h), top - 4, x(h), bot, 'endArrow=none;html=1;strokeColor=%s;dashed=1;' % BROWN)
        d.text(x(h) - 60, top - 38, 120, 32, lab, 'align=center;fontSize=10;fontColor=%s;' % BROWN)
    d.text(0, rows[0] - 12, 195, 24, '<b>Esamas laikotarpis L</b>')
    d.box(x(34), rows[0] - 12, x(106) - x(34), 24, 'Nuoma', OCC)
    naujieji = [
        (10, 46, BAD, '✗ 1. Sutampa iš dalies'),
        (48, 72, BAD, '✗ 2. Sutampa (L viduje)'),
        (106, 132, OK, '✓ 3. Prasideda, kai L baigiasi'),
        (2, 34, OK, '✓ 4. Baigiasi, kai L prasideda'),
    ]
    for y, (s, e, st, lab) in zip(rows[1:], naujieji):
        d.text(0, y - 12, 195, 24, lab, 'fontColor=%s;' % (RED if st == BAD else GREEN))
        d.box(x(s), y - 10, x(e) - x(s), 20, '', st)
    d.text(0, bot + 26, 640, 22,
           'Sutampa, jei <b>L.pradžia &lt; pabaiga</b> ir <b>pradžia &lt; L.pabaiga</b>. '
           'Liečiantis tą pačią minutę – nesutampa.')
    d.save('12-sutapimas')


def buvimo_vieta():
    """Motociklo kelias tarp filialų ir trys norimos nuomos (1 – galima, 2 ir 3 – ne)."""
    d = D()
    X0, PD = 90, 28                      # 2027-05-04 00:00; 28 px per parą
    x = lambda day, hour=0: X0 + (day - 4) * PD + hour * PD / 24
    lanes = {'Vilnius': 40, 'Kaunas': 100, 'Klaipėda': 160}
    LH = 60
    xr = x(24)
    for k, (name, y) in enumerate(lanes.items()):
        d.box(0, y - LH / 2, xr, LH, '', LANE + ('fillColor=#f5f5f5;' if k % 2 == 0 else 'fillColor=#ffffff;'))
        d.text(6, y - 12, 84, 24, '<b>%s</b>' % name)
    bot = 160 + LH / 2
    for day in range(4, 25, 2):
        d.line(x(day), 10, x(day), bot)
    for day in range(4, 25, 4):
        d.text(x(day) - 35, bot + 2, 70, 16, '2027-05-%02d' % day, TICK)
    d.line(X0, bot, xr + 10, bot, AX)

    V, K, KL = lanes['Vilnius'], lanes['Kaunas'], lanes['Klaipėda']
    kelias = 'endArrow=none;html=1;strokeColor=#666666;strokeWidth=4;'
    d.line(X0, V, x(12, 10), V, kelias)
    d.line(x(15, 10), KL, xr, KL, kelias)
    d.line(x(12, 10), V, x(15, 10), KL,
           'endArrow=block;endFill=1;html=1;strokeColor=%s;strokeWidth=6;endSize=4;' % BROWN)
    d.text(x(14, 6), (V + K) / 2 - 12, 160, 32, 'Rezervuota nuoma<br>Vilnius → Klaipėda',
           'fontSize=10;fontColor=%s;' % BROWN)
    d.text(x(8), V + 4, 120, 16, 'motociklas Vilniuje', 'fontSize=10;fontColor=#666666;')
    d.text(x(19), KL + 4, 120, 16, 'motociklas Klaipėdoje', 'fontSize=10;fontColor=#666666;')

    rodykle = 'endArrow=block;endFill=1;html=1;strokeColor=%s;strokeWidth=3;dashed=1;endSize=4;'
    d.line(x(5), V - 14, x(8), V - 14, rodykle % '#82b366')
    d.text(x(5) - 4, V - 30, 40, 16, '<b>1</b> ✓', 'fontSize=10;fontColor=%s;' % GREEN)
    d.line(x(5), V + 2, x(8), K, rodykle % RED)
    d.text(x(8) + 4, K - 8, 40, 16, '<b>2</b> ✗', 'fontSize=10;fontColor=%s;' % RED)
    d.line(x(20), V - 14, x(22), V - 14, rodykle % RED)
    d.text(x(20) - 4, V - 30, 40, 16, '<b>3</b> ✗', 'fontSize=10;fontColor=%s;' % RED)

    y = bot + 26
    for txt, col in (('<b>1</b> ✓ 2027-05-05 – 2027-05-08, Vilnius → Vilnius: motociklas laisvas.', GREEN),
                     ('<b>2</b> ✗ 2027-05-05 – 2027-05-08, Vilnius → Kaunas: 3 taisyklė – '
                      '2027-05-12 kita nuoma prasideda Vilniuje.', RED),
                     ('<b>3</b> ✗ 2027-05-20 – 2027-05-22 iš Vilniaus: 2 taisyklė – '
                      'tuo metu motociklas bus Klaipėdoje.', RED)):
        d.text(0, y, xr, 20, txt, 'fontSize=11;fontColor=%s;' % col)
        y += 20
    d.save('08-buvimo-vietos-taisykle')


def lygiagreti():
    """Du vartotojai vienu metu rezervuoja tą patį motociklą."""
    d = D()
    XA, W, XM, WM, XB = 0, 210, 235, 110, 370
    galva = 'rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;'
    d.box(XA, 0, W, 40, '<b>Vartotojas A</b><br>rezervacija (PA2)', galva)
    d.box(XM, 0, WM, 40, '<b>Motociklo įrašas</b><br>(užraktas)',
          'rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=11;')
    d.box(XB, 0, W, 40, '<b>Vartotojas B</b><br>rezervacija (PA2)', galva)
    for xc in (XA + W / 2, XM + WM / 2, XB + W / 2):
        d.line(xc, 40, xc, 380, 'endArrow=none;html=1;strokeColor=#999999;dashed=1;')
    zingsnis = 'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#666666;fontSize=11;'
    for y, t in ((55, '1. Pradeda transakciją'), (95, '2. Užrakina motociklą'),
                 (135, '3. tikrintiUzimtuma → laisvas'), (175, '4. Įrašo rezervaciją'),
                 (215, '5. Patvirtina → užraktas nuimamas')):
        d.box(XA, y, W, 30, t, zingsnis)
    d.box(XB, 75, W, 30, '1. Pradeda transakciją', zingsnis)
    d.box(XB, 115, W, 30, '2. Bando užrakinti motociklą', zingsnis)
    d.box(XB, 155, W, 90, 'laukia, kol A baigs', GHOST + 'rounded=1;')
    d.box(XB, 255, W, 30, '2. Gauna užraktą', zingsnis)
    d.box(XB, 295, W, 30, '3. tikrintiUzimtuma → <b>užimtas</b>', BAD + 'rounded=1;')
    d.box(XB, 335, W, 40, '4. Atšaukia transakciją, rodo<br>„Motociklas užimtas …“', BAD + 'rounded=1;')
    xc = XM + WM / 2
    d.box(xc - 14, 95, 28, 150, '', OCC)
    d.text(xc + 18, 155, 40, 30, 'laiko<br>A', 'fontSize=10;fontColor=%s;' % BROWN)
    d.box(xc - 14, 255, 28, 120, '', OCC)
    d.text(xc + 18, 300, 40, 30, 'laiko<br>B', 'fontSize=10;fontColor=%s;' % BROWN)
    d.line(XA + W, 110, xc - 14, 110, 'endArrow=block;endFill=1;html=1;strokeColor=#333333;endSize=5;')
    d.line(XB, 130, xc + 14, 130, 'endArrow=block;endFill=1;html=1;strokeColor=#333333;dashed=1;endSize=5;')
    d.text(0, 390, XB + W, 22, 'Iš dviejų vienu metu pateiktų rezervacijų įrašoma tik viena.')
    d.save('12-lygiagreti-rezervacija')


def pavelavimas():
    """Ankstesnė nuoma grąžinta 3 val. pavėluotai, kitos rezervacijos pradžia perkelta."""
    d = D()
    X0, PH = 120, 16                     # 2026-11-12 06:00; 16 px per valandą
    x = lambda h: X0 + (h - 6) * PH      # h – valandos nuo 2026-11-12 00:00
    top, bot = 30, 190
    for h, lab in ((6, '06:00<br>2026-11-12'), (10, '10:00'), (14, '14:00'), (18, '18:00'),
                   (24, '00:00<br>2026-11-13'), (30, '06:00'), (37, '13:00')):
        d.line(x(h), top, x(h), bot)
        d.text(x(h) - 35, bot + 2, 70, 28, lab, TICK + 'verticalAlign=top;')
    d.line(X0, bot, x(39), bot, AX)
    d.text(0, 55, 118, 30, 'Ankstesnė nuoma<br>(nuo 2026-11-10)', 'fontSize=11;')
    d.box(X0, 58, x(10) - X0, 24, '', OCC)
    d.box(x(10), 58, x(13) - x(10), 24, '', BAD)
    d.text(x(13 + 20 / 60) + 6, 58, 120, 24, 'vėluoja 3 val.', 'fontSize=11;fontColor=%s;' % RED)
    d.text(0, 100, 118, 30, 'Kita rezervacija<br>(planuota)', 'fontSize=11;')
    d.box(x(11), 103, x(37) - x(11), 24, '11:00 – 2026-11-13 13:00: 26 val. → 2 paros', GHOST)
    d.text(0, 145, 118, 30, 'Kita rezervacija<br>(pakeista, PA4)', 'fontSize=11;')
    d.box(x(13 + 20 / 60), 148, x(37) - x(13 + 20 / 60), 24,
          '13:20 – 2026-11-13 13:00: 23 val. 40 min. → 1 para', OK)
    d.line(x(13), top, x(13), bot, 'endArrow=none;html=1;strokeColor=%s;dashed=1;' % RED)
    d.line(x(13 + 20 / 60), top, x(13 + 20 / 60), bot, 'endArrow=none;html=1;strokeColor=%s;dashed=1;' % GREEN)
    d.text(x(13) - 102, top - 20, 98, 16, 'grąžinta 13:00', 'align=right;fontSize=11;fontColor=%s;' % RED)
    d.text(x(13 + 20 / 60) + 4, top - 20, 100, 16, 'išduota 13:20', 'fontSize=11;fontColor=%s;' % GREEN)
    d.text(0, bot + 36, x(39), 22,
           'Klientas palaukė: rezervacijos pradžia perkelta į išdavimo laiką, tarifas nesikeičia.')
    d.save('12-pavelavimas')


if __name__ == '__main__':
    sutapimas()
    buvimo_vieta()
    lygiagreti()
    pavelavimas()
