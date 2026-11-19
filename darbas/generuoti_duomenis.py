#!/usr/bin/env python3
"""Generuoja bandomuosius (išgalvotus) duomenis darbas/duomenys.sql.

Duomenys sugeneruojami deterministiškai (fiksuotas atsitiktinių skaičių sėklos numeris), todėl
paleidus skriptą dar kartą gaunamas tas pats failas. Paleidimas: python3 darbas/generuoti_duomenis.py

Laikoma, kad duomenų bazės būsena atitinka 2026-11-19 12:00 (DABAR). Sugeneruojama:
- 2025 ir 2026 metų sezonų (balandžio–spalio mėn.) užbaigtos ir atšauktos nuomos;
- viena šiuo metu vykdoma nuoma (būsena „aktyvi“);
- 2027 metų sezono rezervacijos, sudarytos 2026 m. lapkritį;
- techninė priežiūra prieš sezoną ir sezono metu, perkėlimai tarp filialų (taip pat suplanuoti 2027 m.).

Visi motociklų užimtumo laikotarpiai nepersidengia ir atitinka motociklo buvimo vietos taisyklę
(artefaktai/08-loginis-er.md). Galutinė kaina = nuomos parų skaičius × paros kaina + bauda;
bauda – pakopos su didžiausia „Vėlavimas nuo“ reikšme, neviršijančia vėlavimo valandomis, suma
(laikina taisyklė, bus patikslinta 12 žingsnyje aprašant funkciją skaiciuotiKaina).
"""
import math
import random
from datetime import date, datetime, timedelta
from pathlib import Path

R = random.Random(2026)
DABAR = datetime(2026, 11, 19, 12, 0)
OUT = Path(__file__).with_name('duomenys.sql')

# ---------------------------------------------------------------- klasifikatoriai

FILIALAI = [  # ID, miestas, adresas, telefonas
    (1, 'Vilnius', 'Žalgirio g. 135, Vilnius', '+370 5 219 4410'),
    (2, 'Kaunas', 'Savanorių pr. 287, Kaunas', '+370 37 408 215'),
    (3, 'Klaipėda', 'Taikos pr. 141, Klaipėda', '+370 46 380 512'),
]
KATEGORIJOS = [
    ('AM', 'Mopedai ir lengvieji keturračiai (iki 45 km/h)'),
    ('A1', 'Lengvieji motociklai (iki 125 cm³ ir 11 kW)'),
    ('A2', 'Vidutinės galios motociklai (iki 35 kW)'),
    ('A', 'Visi motociklai'),
]
GAMINTOJAI = [(1, 'Ducati'), (2, 'BMW'), (3, 'Honda'), (4, 'Yamaha')]
TIPAI = [(1, 'Gatvės'), (2, 'Nuotykių'), (3, 'Turistinis'), (4, 'Sportinis'), (5, 'Klasikinis')]

# ID, pavadinimas, tūris cm3, galia kW, sąnaudos l/100 km, gamintojas, tipas, kategorija,
# kiek motociklų, paros kaina 2025 (2026 – brangiau), užstatas, populiarumas, ar leidžiama į užsienį
MODELIAI = [
    (1, 'Monster', 937, 82.0, 5.2, 1, 1, 'A', 3, 99, 800, 1.0, False),
    (2, 'Multistrada V4', 1158, 125.0, 6.6, 1, 2, 'A', 2, 159, 1500, 0.9, True),
    (3, 'Scrambler Icon', 803, 54.0, 5.2, 1, 5, 'A', 2, 89, 700, 0.9, False),
    (4, 'Panigale V2', 955, 114.0, 6.0, 1, 4, 'A', 2, 149, 1500, 0.7, False),
    (5, 'R 1300 GS', 1300, 107.0, 4.8, 2, 2, 'A', 3, 149, 1200, 1.3, True),
    (6, 'R 1250 RT', 1254, 100.0, 4.8, 2, 3, 'A', 2, 139, 1200, 0.9, True),
    (7, 'F 900 R', 895, 77.0, 4.6, 2, 1, 'A', 2, 95, 700, 0.8, False),
    (8, 'G 310 R', 313, 25.0, 3.3, 2, 1, 'A2', 3, 55, 400, 1.0, False),
    (9, 'CB500 Hornet', 471, 35.0, 3.6, 3, 1, 'A2', 4, 59, 400, 1.2, False),
    (10, 'NC750X', 745, 43.1, 3.5, 3, 3, 'A', 3, 79, 600, 1.0, True),
    (11, 'CRF1100L Africa Twin', 1084, 75.0, 5.0, 3, 2, 'A', 3, 119, 1000, 1.1, True),
    (12, 'CB125R', 125, 11.0, 2.2, 3, 1, 'A1', 3, 39, 300, 0.8, False),
    (13, 'MT-07', 689, 54.0, 4.2, 4, 1, 'A', 4, 79, 600, 1.2, False),
    (14, 'Ténéré 700', 689, 54.0, 4.3, 4, 2, 'A', 2, 99, 800, 1.0, True),
    (15, 'Tracer 9 GT', 890, 87.0, 5.0, 4, 3, 'A', 2, 115, 900, 0.9, True),
]
NUOTRAUKA = {1: 'ducati-monster', 2: 'ducati-multistrada-v4', 3: 'ducati-scrambler-icon', 4: 'ducati-panigale-v2',
             5: 'bmw-r-1300-gs', 6: 'bmw-r-1250-rt', 7: 'bmw-f-900-r', 8: 'bmw-g-310-r', 9: 'honda-cb500-hornet',
             10: 'honda-nc750x', 11: 'honda-africa-twin', 12: 'honda-cb125r', 13: 'yamaha-mt-07',
             14: 'yamaha-tenere-700', 15: 'yamaha-tracer-9-gt'}
MIN_METAI = {2: 2021, 4: 2022, 5: 2024, 9: 2024, 11: 2022, 14: 2021, 15: 2021}
WMI = {1: 'ZDM', 2: 'WB1', 3: 'JH2', 4: 'JYA'}
VIN_RAIDES = 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789'
METU_KODAS = {2021: 'M', 2022: 'N', 2023: 'P', 2024: 'R', 2025: 'S', 2026: 'T'}
LT_RAIDES = 'ABCDEFGHJKLMNPRSTUVZ'

PRIEZIUROS_PRIEZASTYS = ['Sezoninė apžiūra', 'Tepalų ir filtrų keitimas', 'Padangų keitimas',
                         'Stabdžių kaladėlių keitimas', 'Grandinės ir žvaigždžių keitimas', 'Akumuliatoriaus keitimas']
ISDAVIMO_BUKLES = ['Be pastabų', 'Be pastabų', 'Be pastabų', 'Tvarkingas, bakas pilnas',
                   'Smulkūs įbrėžimai ant kairiojo šoninio dangčio (užfiksuoti anksčiau)',
                   'Nedidelis įbrėžimas ant bako (užfiksuotas anksčiau)']
GRAZINIMO_BUKLES = ['Be pastabų', 'Be pastabų', 'Be pastabų', 'Purvinas, reikia plauti',
                    'Bakas ne pilnas', 'Naujas smulkus įbrėžimas ant veidrodėlio',
                    'Nusidėvėjusi galinė padanga', 'Purvinas po kelionės žvyrkeliais']


def sql(v):
    if v is None:
        return 'NULL'
    if isinstance(v, bool):
        return 'TRUE' if v else 'FALSE'
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, datetime):
        return f"TIMESTAMP '{v:%Y-%m-%d %H:%M:%S}'"
    if isinstance(v, date):
        return f"DATE '{v:%Y-%m-%d}'"
    return "'" + str(v).replace("'", "''") + "'"


def telefonas():
    return '+3706' + ''.join(R.choice('0123456789') for _ in range(7))


def maisa():
    abc = './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return '$2b$12$' + ''.join(R.choice(abc) for _ in range(53))


# ---------------------------------------------------------------- tarifai

TARIFAI = []      # (ID, kaina, užstatas, nuo, iki, modelis)
PAKOPOS = []      # (tarifas, nuo val., bauda)


def pakopos(tid, kaina, klase, modelis, metai):
    if modelis == 12 and metai == 2025:
        return  # tarifas be baudų pakopų – bauda neskaičiuojama
    if modelis == 10 and metai == 2026:
        rows = [(0, 10), (2, 30), (24, kaina)]  # pakopa nuo 0 val.
    elif klase == 'S':
        rows = [(1, 10), (3, 25), (24, kaina)]
    elif klase == 'M':
        rows = [(1, 20), (3, 50), (24, kaina)]
    else:
        rows = [(1, 30), (3, 70), (24, kaina)]
    for nuo, b in rows:
        PAKOPOS.append((tid, nuo, b))


def sukurti_tarifus():
    tid = 0
    for m in MODELIAI:
        mid, kaina25, uzst = m[0], m[9], m[10]
        klase = 'S' if kaina25 < 70 else ('M' if kaina25 < 120 else 'L')
        kaina26 = kaina25 + (5 if kaina25 < 100 else 10)
        tid += 1
        TARIFAI.append((tid, kaina25, uzst, date(2025, 1, 1), date(2025, 12, 31), mid))
        pakopos(tid, kaina25, klase, mid, 2025)
        if mid == 4:  # Panigale V2: 2026 m. kaina pakeista sezono viduryje
            tid += 1
            TARIFAI.append((tid, kaina26, uzst, date(2026, 1, 1), date(2026, 6, 30), mid))
            pakopos(tid, kaina26, klase, mid, 2026)
            tid += 1
            TARIFAI.append((tid, kaina26 + 10, uzst, date(2026, 7, 1), None, mid))
            pakopos(tid, kaina26 + 10, klase, mid, 2026)
        else:
            tid += 1
            TARIFAI.append((tid, kaina26, uzst, date(2026, 1, 1), None, mid))
            pakopos(tid, kaina26, klase, mid, 2026)


def tarifas(modelis, diena):
    for t in TARIFAI:
        if t[5] == modelis and t[3] <= diena and (t[4] is None or diena <= t[4]):
            return t
    raise ValueError((modelis, diena))


def bauda(tid, velavimas_val):
    if velavimas_val <= 0:
        return 0
    tinka = [p for p in PAKOPOS if p[0] == tid and p[1] <= velavimas_val]
    return max(tinka, key=lambda p: p[1])[2] if tinka else 0


# ---------------------------------------------------------------- žmonės

PASKYROS = []      # (ID, vardas, maiša, vaidmuo)
DARBUOTOJAI = []   # (ID, vardas, pavardė, el. paštas, tel., filialas, paskyra)
KLIENTAI = []      # (ID, vardas, pavardė, gimimo data, el. paštas, tel., pažymėjimas, paskyra)
KL_KAT = []        # (klientas, kategorija, galioja iki)
TEISES = {}        # klientas -> {kategorija: galioja iki}


def sukurti_zmones():
    pid = 0
    darb = [('Administratorius', 1, None), ('Administratorius', 2, 1)]
    darb += [('Darbuotojas', i, f) for i, f in zip(range(1, 8), [1, 1, 1, 2, 2, 3, 3])]
    for did, (vardas, nr, fil) in enumerate(darb, start=1):
        pid += 1
        prisij = f'{vardas.lower()}_{nr}'
        PASKYROS.append((pid, prisij, maisa(), vardas.lower()))
        DARBUOTOJAI.append((did, vardas, str(nr), f'{prisij}@gmail.com', telefonas(), fil, pid))

    numeriai = R.sample(range(10_000_000, 99_999_999), 40)
    for kid in range(1, 41):
        su_paskyra = kid <= 34
        prisij = f'klientas_{kid}'
        paskyra = None
        if su_paskyra:
            pid += 1
            PASKYROS.append((pid, prisij, maisa(), 'klientas'))
            paskyra = pid
        if kid <= 26:
            kategorijos, metai = ['A1', 'A2', 'A'], (1965, 1998)
        elif kid <= 32:
            kategorijos, metai = ['A1', 'A2'], (1996, 2006)
        elif kid <= 34:
            kategorijos, metai = ['A1'], (2004, 2008)
        elif kid <= 36:
            kategorijos, metai = [], (1980, 2000)   # tik B kategorija – motociklų nuomotis negali
        else:
            kategorijos, metai = ['A1', 'A2', 'A'], (1970, 1995)
        gim = date(R.randint(*metai), R.randint(1, 12), R.randint(1, 28))
        KLIENTAI.append((kid, 'Klientas', str(kid), gim, f'{prisij}@gmail.com' if su_paskyra else None,
                         telefonas(), str(numeriai[kid - 1]), paskyra))
        galioja = date(R.randint(2028, 2038), R.randint(1, 12), R.randint(1, 28))
        if kid == 26:
            galioja = date(2027, 5, 10)  # kategorijos galiojimas baigiasi 2027 m. sezono pradžioje
        TEISES[kid] = {}
        for k in kategorijos:
            KL_KAT.append((kid, k, galioja))
            TEISES[kid][k] = galioja


def darbuotojas_filiale(fil):
    return R.choice([d[0] for d in DARBUOTOJAI if d[5] == fil and d[1] == 'Darbuotojas'])


def administratorius():
    return R.choice([d[0] for d in DARBUOTOJAI if d[1] == 'Administratorius'])


# ---------------------------------------------------------------- parkas ir laiko juosta

MOTOCIKLAI = []   # dict
NUOMOS, ISDAVIMAI, GRAZINIMAI, PRIEZIUROS, PERKELIMAI, PERK_MOTO = [], [], [], [], [], []


def vin(gam, metai):
    return WMI[gam] + ''.join(R.choice(VIN_RAIDES) for _ in range(6)) + METU_KODAS[metai] + \
        R.choice('ABCDEFGH') + ''.join(R.choice('0123456789') for _ in range(6))


def sukurti_motociklus():
    filialai = [1] * 17 + [2] * 12 + [3] * 11
    R.shuffle(filialai)
    numeriai, vinai = set(), set()
    mid = 0
    for m in MODELIAI:
        for _ in range(m[8]):
            mid += 1
            metai = R.randint(max(MIN_METAI.get(m[0], 2021), 2021), 2025)
            while True:
                vn = f'{R.randint(10, 99)} {"".join(R.choice(LT_RAIDES) for _ in range(3))}'
                if vn not in numeriai:
                    numeriai.add(vn)
                    break
            while True:
                v = vin(m[5], metai)
                if v not in vinai:
                    vinai.add(v)
                    break
            rida = R.randint(1500, 5000) + (2025 - metai) * R.randint(3000, 6000)
            MOTOCIKLAI.append(dict(id=mid, modelis=m[0], kategorija=m[7], pop=m[11], metai=metai, vn=vn, vin=v,
                                   rida=rida, uzsienis=m[12] and R.random() < 0.85, naudojamas=True,
                                   filialas=filialai[mid - 1], laisvas=datetime(2025, 3, 1), nuo2026=False))
    # du motociklai nupirkti 2026 m., vienas nurašytas po 2025 m. sezono
    for m in [MOTOCIKLAI[4], MOTOCIKLAI[30]]:
        m.update(metai=2026, nuo2026=True, rida=R.randint(20, 150), vin=m['vin'][:9] + 'T' + m['vin'][10:],
                 laisvas=datetime(2026, 3, 1))
    nurasytas = next(m for m in MOTOCIKLAI if m['modelis'] == 12)
    nurasytas.update(metai=2021, vin=nurasytas['vin'][:9] + 'M' + nurasytas['vin'][10:], nurasomas=True)


def tinkami_klientai(kategorija, iki):
    return [k for k, t in TEISES.items() if kategorija in t and t[kategorija] >= iki.date()]


def nauja_nuoma(m, pradzia, paros, grazinimo_fil, sukurta, busena, velavimas=None):
    pabaiga = pradzia + timedelta(days=paros)
    klientai = tinkami_klientai(m['kategorija'], pabaiga)
    kl = R.choice(klientai)
    turi_paskyra = KLIENTAI[kl - 1][7] is not None
    darb = None if (turi_paskyra and R.random() < 0.7) else darbuotojas_filiale(m['filialas'])
    t = tarifas(m['modelis'], sukurta.date())
    nid = len(NUOMOS) + 1
    NUOMOS.append(dict(id=nid, sukurta=sukurta, pradzia=pradzia, pabaiga=pabaiga, busena=busena, klientas=kl,
                       tarifas=t[0], motociklas=m['id'], isd_fil=m['filialas'], grz_fil=grazinimo_fil,
                       darbuotojas=darb))
    if busena in ('aktyvi', 'užbaigta'):
        isd_laikas = pradzia + timedelta(minutes=R.randint(0, 30))
        ISDAVIMAI.append((nid, isd_laikas, m['rida'], R.choice(ISDAVIMO_BUKLES), darbuotojas_filiale(m['filialas'])))
    if busena == 'užbaigta':
        grz = pabaiga + timedelta(minutes=velavimas)
        km = paros * R.randint(90, 320)
        m['rida'] += km
        val = velavimas / 60
        b = bauda(t[0], val)
        GRAZINIMAI.append((nid, grz, m['rida'], R.choice(GRAZINIMO_BUKLES), paros * t[1] + b, b,
                           darbuotojas_filiale(grazinimo_fil)))
        m['filialas'] = grazinimo_fil
        return grz
    return pabaiga


def atsitiktinis_velavimas():
    x = R.random()
    if x < 0.80:
        return -R.randint(0, 180)
    if x < 0.95:
        return R.randint(20, 300)
    return R.randint(360, 1800)


def grazinimo_filialas(fil):
    if R.random() < 0.15:
        return R.choice([f for f in (1, 2, 3) if f != fil])
    return fil


def prieziura(m, pradzia, val, priezastis):
    pabaiga = pradzia + timedelta(hours=val)
    PRIEZIUROS.append((len(PRIEZIUROS) + 1, pradzia, pabaiga, priezastis, m['id'], darbuotojas_filiale(m['filialas'])))
    return pabaiga


def perkelimas(diena, is_f, i_f, kiek, ateityje=False):
    pradzia, pabaiga = diena.replace(hour=9), diena.replace(hour=15)
    kandidatai = [m for m in MOTOCIKLAI if m['naudojamas'] and m['filialas'] == is_f and m['laisvas'] <= pradzia
                  and not (m.get('nuo2026') and diena.year == 2025)]
    if not kandidatai:
        return
    R.shuffle(kandidatai)
    pid = len(PERKELIMAI) + 1
    PERKELIMAI.append((pid, pradzia, pabaiga, is_f, i_f, administratorius()))
    for m in kandidatai[:kiek]:
        PERK_MOTO.append((pid, m['id']))
        m['filialas'] = i_f
        m['laisvas'] = pabaiga + timedelta(hours=R.randint(18, 40))


def sezonas(metai):
    pradzia, pabaiga = datetime(metai, 4, 1), datetime(metai, 10, 31)
    perkelimai = {date(2025, 5, 5): (3, 1, 2), date(2025, 7, 7): (2, 3, 2), date(2025, 9, 1): (1, 2, 2),
                  date(2026, 4, 27): (3, 1, 2), date(2026, 6, 15): (1, 3, 2), date(2026, 8, 17): (2, 1, 2),
                  date(2026, 10, 26): (3, 1, 3)}
    # sezoninė apžiūra prieš sezoną
    for m in MOTOCIKLAI:
        if not m['naudojamas'] or (metai == 2025 and m['nuo2026']):
            continue
        d = datetime(metai, 3, R.randint(10, 27), 8)
        m['laisvas'] = prieziura(m, d, R.choice([9, 33]), 'Sezoninė apžiūra') + timedelta(hours=16)
    diena = pradzia
    while diena <= pabaiga:
        p = perkelimai.get(diena.date())
        if p:
            perkelimas(diena, *p)
        for m in MOTOCIKLAI:
            if not m['naudojamas'] or (metai == 2025 and m['nuo2026']):
                continue
            start = diena.replace(hour=R.choice([9, 10, 10, 11, 12, 14]))
            if m['laisvas'] > start:
                continue
            savaitgalis = diena.weekday() in (3, 4, 5)
            if R.random() < 0.012 and diena.month in (6, 7, 8):
                pr = diena.replace(hour=8)
                m['laisvas'] = prieziura(m, pr, R.choice([9, 33]), R.choice(PRIEZIUROS_PRIEZASTYS[1:])) + timedelta(hours=15)
                continue
            if R.random() < 0.035 * m['pop'] * (1.8 if savaitgalis else 1.0):
                paros = R.choice([1, 1, 2, 2, 3, 3, 4, 5, 7])
                if start + timedelta(days=paros) > pabaiga.replace(hour=20):
                    continue
                sukurta = start - timedelta(days=R.randint(1, 45), hours=R.randint(0, 10))
                if R.random() < 0.08:  # atšaukta rezervacija laiko juostos neužima
                    nauja_nuoma(m, start, paros, m['filialas'], sukurta, 'atšaukta')
                    continue
                grz = nauja_nuoma(m, start, paros, grazinimo_filialas(m['filialas']), sukurta, 'užbaigta',
                                  atsitiktinis_velavimas())
                m['laisvas'] = grz + timedelta(hours=R.randint(20, 120))
        diena += timedelta(days=1)
    if metai == 2025:
        for m in MOTOCIKLAI:
            if m.get('nurasomas'):
                m['naudojamas'] = False


def dabartis_ir_ateitis():
    # šiuo metu vykdomos nuomos (vėlyvo rudens kelionės)
    for mid, pr in [(9, datetime(2026, 11, 17, 10)), (25, datetime(2026, 11, 18, 11))]:
        m = MOTOCIKLAI[mid - 1]
        m['filialas_pries'] = m['filialas']
        nauja_nuoma(m, pr, 4, m['filialas'], pr - timedelta(days=6, hours=3), 'aktyvi')
        m['laisvas'] = pr + timedelta(days=6)
    # 2027 m. sezono pasiruošimas: apžiūra ir perkėlimas
    for m in MOTOCIKLAI:
        if m['naudojamas'] and R.random() < 0.3:
            m['laisvas'] = prieziura(m, datetime(2027, 3, R.randint(15, 24), 8), 33, 'Sezoninė apžiūra') + timedelta(hours=16)
        m['laisvas'] = max(m['laisvas'], datetime(2027, 3, 1))
    perkelimas(datetime(2027, 3, 29), 1, 3, 2, ateityje=True)
    # 2027 m. rezervacijos, sudarytos 2026 m. lapkritį
    diena = datetime(2027, 4, 1)
    while diena <= datetime(2027, 6, 30):
        for m in MOTOCIKLAI:
            if not m['naudojamas']:
                continue
            start = diena.replace(hour=R.choice([9, 10, 11, 12]))
            if m['laisvas'] > start or R.random() > 0.012 * m['pop']:
                continue
            paros = R.choice([2, 3, 3, 4, 5, 7])
            sukurta = datetime(2026, 11, R.randint(1, 18), R.randint(8, 22), R.randint(0, 59))
            busena = 'atšaukta' if R.random() < 0.1 else 'rezervuota'
            grz_f = grazinimo_filialas(m['filialas'])
            pab = nauja_nuoma(m, start, paros, grz_f if busena == 'rezervuota' else m['filialas'], sukurta, busena)
            if busena == 'rezervuota':
                m['ateities_filialas'] = grz_f
                m['filialas'] = grz_f  # tolesnės rezervacijos prasideda grąžinimo filiale
                m['laisvas'] = pab + timedelta(days=R.randint(2, 6))
        diena += timedelta(days=1)


def generuoti():
    sukurti_tarifus()
    sukurti_zmones()
    sukurti_motociklus()
    sezonas(2025)
    sezonas(2026)
    # dabartinis filialas – baigtų laikotarpių pabaiga (išsaugomas prieš planuojant ateitį)
    dabartinis = {m['id']: m['filialas'] for m in MOTOCIKLAI}
    rida_dabar = {m['id']: m['rida'] for m in MOTOCIKLAI}
    dabartis_ir_ateitis()
    for m in MOTOCIKLAI:
        m['filialas'] = dabartinis[m['id']]
        m['rida'] = rida_dabar[m['id']]


# ---------------------------------------------------------------- SQL

def insert(lentele, stulpeliai, eilutes, su_id=False):
    out = [f'-- {lentele}: {len(eilutes)} įr.']
    cols = ', '.join(f'"{c}"' for c in stulpeliai)
    over = ' OVERRIDING SYSTEM VALUE' if su_id else ''
    for i in range(0, len(eilutes), 50):
        dalis = eilutes[i:i + 50]
        out.append(f'INSERT INTO "{lentele}" ({cols}){over} VALUES')
        out.append(',\n'.join('    (' + ', '.join(sql(v) for v in e) + ')' for e in dalis) + ';')
    if su_id:
        out.append(f'ALTER TABLE "{lentele}" ALTER COLUMN "ID" RESTART WITH {len(eilutes) + 1};')
    return '\n'.join(out) + '\n'


def rasyti():
    p = []
    p.append('-- Motociklų nuomos IS: bandomieji (išgalvoti) duomenys.\n'
             '-- Sugeneruota skriptu darbas/generuoti_duomenis.py – rankomis neredaguoti, o keisti generatorių.\n'
             f'-- Duomenų bazės būsena atitinka {DABAR:%Y-%m-%d %H:%M}. Įkeliama po darbas/schema.sql.\n'
             '-- Slaptažodžių maišos netikros (atsitiktinės eilutės).\n')
    p.append('BEGIN;\n')
    p.append(insert('Paskyra', ['ID', 'Prisijungimo vardas', 'Slaptažodžio maiša', 'Vaidmuo'], PASKYROS, True))
    p.append(insert('Filialas', ['ID', 'Miestas', 'Adresas', 'Telefonas'], FILIALAI, True))
    p.append(insert('Kategorija', ['Kodas', 'Aprašymas'], KATEGORIJOS))
    p.append(insert('Gamintojas', ['ID', 'Pavadinimas'], GAMINTOJAI, True))
    p.append(insert('Motociklo tipas', ['ID', 'Pavadinimas'], TIPAI, True))
    p.append(insert('Motociklo modelis', ['ID', 'Pavadinimas', 'Variklio tūris', 'Galia', 'Degalų sąnaudos', 'Nuotrauka',
                                          'Gamintojo ID', 'Tipo ID', 'Kategorijos kodas'],
                    [(m[0], m[1], m[2], m[3], m[4], f'nuotraukos/{NUOTRAUKA[m[0]]}.jpg', m[5], m[6], m[7]) for m in MODELIAI], True))
    p.append(insert('Motociklas', ['ID', 'Valstybinis numeris', 'VIN', 'Pagaminimo metai', 'Rida',
                                   'Leidžiama išvažiuoti į užsienį', 'Naudojamas', 'Modelio ID', 'Filialo ID'],
                    [(m['id'], m['vn'], m['vin'], m['metai'], m['rida'], m['uzsienis'], m['naudojamas'], m['modelis'],
                      m['filialas']) for m in MOTOCIKLAI], True))
    p.append(insert('Tarifas', ['ID', 'Paros kaina', 'Užstatas', 'Galioja nuo', 'Galioja iki', 'Modelio ID'], TARIFAI, True))
    p.append(insert('Baudos pakopa', ['Tarifo ID', 'Vėlavimas nuo (val.)', 'Bauda'], PAKOPOS))
    p.append(insert('Klientas', ['ID', 'Vardas', 'Pavardė', 'Gimimo data', 'El. paštas', 'Telefonas', 'Pažymėjimo numeris',
                                 'Paskyros ID'], KLIENTAI, True))
    p.append(insert('Kliento kategorija', ['Kliento ID', 'Kategorijos kodas', 'Galioja iki'], KL_KAT))
    p.append(insert('Darbuotojas', ['ID', 'Vardas', 'Pavardė', 'El. paštas', 'Telefonas', 'Filialo ID', 'Paskyros ID'],
                    DARBUOTOJAI, True))
    p.append(insert('Nuoma', ['ID', 'Sukūrimo laikas', 'Planuojama pradžia', 'Planuojama pabaiga', 'Būsena', 'Kliento ID',
                              'Tarifo ID', 'Motociklo ID', 'Išdavimo filialo ID', 'Grąžinimo filialo ID',
                              'Užregistravusio darbuotojo ID'],
                    [(n['id'], n['sukurta'], n['pradzia'], n['pabaiga'], n['busena'], n['klientas'], n['tarifas'],
                      n['motociklas'], n['isd_fil'], n['grz_fil'], n['darbuotojas']) for n in NUOMOS], True))
    p.append(insert('Išdavimas', ['Nuomos ID', 'Laikas', 'Rida', 'Būklė', 'Darbuotojo ID'], ISDAVIMAI))
    p.append(insert('Grąžinimas', ['Nuomos ID', 'Laikas', 'Rida', 'Būklė', 'Galutinė kaina', 'Bauda', 'Darbuotojo ID'],
                    GRAZINIMAI))
    p.append(insert('Techninė priežiūra', ['ID', 'Pradžia', 'Pabaiga', 'Priežastis', 'Motociklo ID', 'Darbuotojo ID'],
                    PRIEZIUROS, True))
    p.append(insert('Perkėlimas', ['ID', 'Pradžia', 'Pabaiga', 'Iš filialo ID', 'Į filialo ID', 'Darbuotojo ID'],
                    PERKELIMAI, True))
    p.append(insert('Perkeliamas motociklas', ['Perkėlimo ID', 'Motociklo ID'], PERK_MOTO))
    p.append('COMMIT;\n')
    OUT.write_text('\n'.join(p), encoding='utf-8')


if __name__ == '__main__':
    generuoti()
    rasyti()
    busenos = {}
    for n in NUOMOS:
        busenos[n['busena']] = busenos.get(n['busena'], 0) + 1
    print(f'{OUT.name}: motociklai {len(MOTOCIKLAI)}, klientai {len(KLIENTAI)}, nuomos {len(NUOMOS)} {busenos}, '
          f'priežiūros {len(PRIEZIUROS)}, perkėlimai {len(PERKELIMAI)}')
