// Maketų eksportas į PNG (13 žingsnis, 2.3.2 skyrius).
// Paleidimas iš projekto šakninio aplanko: node artefaktai/13-dizainas/eksportuoti.mjs [failo-vardo-dalis]
// Reikia: Node.js ≥ 22 (įtaisytas WebSocket) ir Google Chrome. Šriftas „Inter“ įkeliamas iš Google Fonts,
// todėl reikia interneto ryšio. Kiekvienas maketas atveriamas nurodytu ekrano pločiu (CSS pikseliais)
// ir nufotografuojamas visu aukščiu su 2 kartų raiška.
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const APLANKAS = dirname(fileURLToPath(import.meta.url));
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9334;
const MASTELIS = 2;

// failas, plotis, didžiausias aukštis (null – visas puslapis), rezultatas
const MAKETAI = [
  ['e1-paieska.html', 360, 1460, '13-e1-paieska-360.png'],
  ['e1-paieska.html', 1280, null, '13-e1-paieska-1280.png'],
  ['e2-rezervacijos-duomenys.html', 360, null, '13-e2-rezervacijos-duomenys-360.png'],
  ['e2-rezervacijos-duomenys.html?atsisakymas', 360, null, '13-e2-atsisakymas-360.png'],
  ['e3-patvirtinimas.html', 360, null, '13-e3-patvirtinimas-360.png'],
  ['e4-tvarkarastis.html', 1280, null, '13-e4-tvarkarastis-1280.png'],
  ['e5-parko-uzimtumas.html', 1280, null, '13-e5-parko-uzimtumas-1280.png'],
];
const filtras = process.argv[2];

const profilis = mkdtempSync(join(tmpdir(), 'maketai-'));
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profilis}`,
  '--hide-scrollbars', '--no-first-run', '--allow-file-access-from-files', 'about:blank'], { stdio: 'ignore' });
const miegoti = ms => new Promise(r => setTimeout(r, ms));

try {
  let taikiniai;
  for (let i = 0; i < 50 && !taikiniai; i++) {
    try { taikiniai = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); } catch { await miegoti(200); }
  }
  const ws = new WebSocket(taikiniai.find(t => t.type === 'page').webSocketDebuggerUrl);
  await new Promise(r => (ws.onopen = r));
  let id = 0;
  const laukia = new Map();
  ws.onmessage = e => { const m = JSON.parse(e.data); if (laukia.has(m.id)) { laukia.get(m.id)(m.result); laukia.delete(m.id); } };
  const siusti = (method, params = {}) => new Promise(r => { laukia.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });
  const vertinti = async js => (await siusti('Runtime.evaluate', { expression: js, awaitPromise: true, returnByValue: true })).result.value;

  for (const [failas, plotis, maxAukstis, rezultatas] of MAKETAI) {
    if (filtras && !failas.includes(filtras)) continue;
    await siusti('Emulation.setDeviceMetricsOverride', { width: plotis, height: 800, deviceScaleFactor: MASTELIS, mobile: plotis < 768 });
    const [kelias, uzklausa] = failas.split('?');
    const url = pathToFileURL(join(APLANKAS, kelias)).href + (uzklausa ? '?' + uzklausa : '');
    await siusti('Page.navigate', { url });
    await miegoti(500);
    await vertinti('new Promise(r => document.readyState === "complete" ? r() : addEventListener("load", r))');
    await vertinti('document.fonts.ready.then(() => true)');
    const aukstis = await vertinti('Math.ceil(document.documentElement.scrollHeight)');
    const h = maxAukstis ? Math.min(aukstis, maxAukstis) : aukstis;
    await siusti('Emulation.setDeviceMetricsOverride', { width: plotis, height: h, deviceScaleFactor: MASTELIS, mobile: plotis < 768 });
    await miegoti(300);
    const vaizdas = await siusti('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: plotis, height: h, scale: 1 } });
    writeFileSync(join(APLANKAS, rezultatas), Buffer.from(vaizdas.data, 'base64'));
    console.log(`${rezultatas}: ${plotis}×${h} (PNG ${plotis * MASTELIS}×${h * MASTELIS})`);
  }
  ws.close();
} finally {
  chrome.kill();
  await miegoti(300);
  rmSync(profilis, { recursive: true, force: true });
}
