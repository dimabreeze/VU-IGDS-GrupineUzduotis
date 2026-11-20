// Word (macOS) eksportuodamas PDF sugadina dalį vidinių nuorodų:
//   1) kai kurioms įrašo paskirties objektą, kurio PDF faile nėra (/Dest 1694 0 R be „1694 0 obj“), –
//      tokia nuoroda niekur neveda (pvz., į antraštes, po kurių eina didelis paveikslas);
//   2) žymei puslapio apačioje kartais nurodo kitą puslapį (pvz., turinio eilutė „1.1.2. IS tikslai“).
// Įrankis kiekvienai vidinei nuorodai pagal jos tekstą nustato, kas turi būti paskirties puslapyje:
//   turinio eilutė „3.2. Testavimo atvejai ..... 76“ -> eilutė „3.2. Testavimo atvejai“;
//   skyrius „1.1.4“, ekranas „EKRANAS01“            -> eilutė, prasidedanti „1.1.4. “ / „EKRANAS01. “;
//   „FR 1.2.1“, „NFR 1.3.3.3“, „PR 1.6.1“                -> „Nr. FR 1.2.1“ (reikalavimo lentelė);
//   „Ganto diagrama, 5.4“                           -> Ganto diagramos paveikslo pavadinimas;
//   „TA2“                                           -> „Testavimo atvejo Nr. 2“ (TA lentelės pirmas langelis);
//   „PA1“, „P1“, „DS1“, „E1“                         -> eilutė „PA1 …“ (lentelės eilutė);
//   „[12]“, „3“ (skyrius), „1 priedas“              -> eilutė „12. “ / „3. “ / „1 priedas. “.
// Antraštės, reikalavimai, TA ir ekranai dokumente yra vienoje vietoje – nuoroda nukreipiama ten, kur jie iš
// tikrųjų yra (Word kartais nurodo puslapį, esantį 1–2 puslapiais toliau). Lentelių eilutės (PA, P, DS, E) ir
// šaltiniai – artimiausias puslapis nuo Word nurodytojo (±2), kuriame yra tas tekstas. Neradus – klaida.
// Naudojimas: pdf-nuorodos ataskaita.pdf
import Foundation
import PDFKit

let path = CommandLine.arguments[1]
guard let doc = PDFDocument(url: URL(fileURLWithPath: path)) else { fatalError("KLAIDA: neatidaromas \(path)") }

// visi tarpai (tabuliacija, nelaužomas tarpas, eilutės lūžis) – vienas paprastas tarpas
func norm(_ s: String) -> String {
    s.components(separatedBy: .whitespacesAndNewlines).filter { !$0.isEmpty }.joined(separator: " ")
}

// puslapiai su turiniu (TURINYS) – juose paskirties neieškoma
var tocPages = Set<Int>()
for i in 0..<min(6, doc.pageCount) where (doc.page(at: i)?.string ?? "").contains("....") { tocPages.insert(i) }

typealias Test = (String) -> Bool   // ar (normalizuota) eilutė yra paskirtis

// taisyklė pagal nuorodos tekstą; global – ar paskirtis vienintelė dokumente (galima ieškoti visur)
func rule(_ raw: String) -> (test: Test, global: Bool)? {
    var t = raw.trimmingCharacters(in: .whitespacesAndNewlines)
    if let r = t.range(of: #"\s*\.{3,}[\s\S]*$"#, options: .regularExpression) {    // turinio eilutė
        let title = norm(String(t[..<r.lowerBound]))
        // ilga antraštė gali būti perkelta į kitą eilutę – tinka ir jos pirmoji eilutė
        return ({ $0 == title || ($0.count >= 12 && title.hasPrefix($0 + " ")) }, true)
    }
    if t.contains("Ganto") || t.contains("diagrama,") {   // „Ganto diagrama, 5.4“ (gali būti perkelta į kitą eilutę)
        return ({ $0.contains("pav.") && $0.contains("(Ganto diagrama)") }, true)
    }
    let source = t.hasPrefix("[")
    t = norm(t.trimmingCharacters(in: CharacterSet(charactersIn: "()[];,. ")))
    func match(_ re: String) -> Bool { t.range(of: re, options: .regularExpression) != nil }
    if source { return ({ $0.hasPrefix(t + ". ") || $0.contains(" \(t). ") || $0.hasSuffix(" \(t).") }, false) }   // „1. 2. 3. … 9. Bikerent…“
    if match(#"^\d+ pried"#) { return ({ $0.hasPrefix(t + ". ") || $0 == t }, true) }
    if match(#"^\d+(\.\d+)+$"#) || match(#"^EKRANAS\d+$"#) { return ({ $0.hasPrefix(t + ". ") }, true) }
    if match(#"^\d+$"#) { return ({ $0.hasPrefix(t + ". ") }, false) }             // „3 skyrius“
    if match(#"^(N?FR|PR) \d+(\.\d+)+$"#) { return ({ $0.contains("Nr. " + t) }, true) }
    if match(#"^TA\d+$"#) {
        let n = String(t.dropFirst(2))
        return ({ $0 == "Testavimo atvejo Nr. \(n)" || $0.hasPrefix("Testavimo atvejo Nr. \(n) ") }, true)   // TA lentelės viršus
    }
    if match(#"^(PA|DS|P|E)\d+$"#) { return ({ $0 == t || $0.hasPrefix(t + " ") }, false) }
    return nil
}

// lentelės eilutės ID (PA1, P1, DS1, E1) iš nuorodos teksto
func idKey(_ raw: String) -> String? {
    let t = norm(raw.trimmingCharacters(in: CharacterSet(charactersIn: "()[];,. \n")))
    return t.range(of: #"^(PA|DS|P|E)\d+$"#, options: .regularExpression) != nil ? t : nil
}

// puslapių eilutės (normalizuotos) su jų vieta tekste – skaitoma vieną kartą
let pageLines: [[(String, NSRange)]] = (0..<doc.pageCount).map { j in
    var out: [(String, NSRange)] = []
    let ns = (doc.page(at: j)!.string ?? "") as NSString
    ns.enumerateSubstrings(in: NSRange(location: 0, length: ns.length), options: .byLines) { line, r, _, _ in
        if let line = line { out.append((norm(line), r)) }
    }
    return out
}

// atitinkančių eilučių viršaus koordinatės puslapyje j
func hits(_ j: Int, _ test: Test) -> [CGFloat] {
    let page = doc.page(at: j)!
    return pageLines[j].filter { test($0.0) }.compactMap { page.selection(for: $0.1) }
        .map { min($0.bounds(for: page).maxY + 12, page.bounds(for: .mediaBox).maxY) }
}

func go(_ a: PDFAnnotation, _ j: Int, _ y: CGFloat) {
    a.action = PDFActionGoTo(destination: PDFDestination(page: doc.page(at: j)!, at: CGPoint(x: 0, y: y)))
}

var fixed = 0, moved = 0, failed: [String] = []
for i in 0..<doc.pageCount {
    let page = doc.page(at: i)!
    for a in page.annotations where a.type == "Link" && a.url == nil {
        let raw = page.selection(for: a.bounds)?.string ?? ""
        let k = ((a.destination ?? (a.action as? PDFActionGoTo)?.destination)?.page).map { doc.index(for: $0) }
        guard let (test, global) = rule(raw) else {
            if k == nil { failed.append("p\(i + 1) „\(norm(raw))“: nežinomas nuorodos tipas") }
            continue
        }
        var found: [(Int, CGFloat)] = []
        if global {   // vienintelė vieta dokumente
            for j in 0..<doc.pageCount where !tocPages.contains(j) { found += hits(j, test).map { (j, $0) } }
            if found.count != 1, let k = k, !hits(k, test).isEmpty { continue }   // keliose vietose, bet Word nurodė tinkamą
        } else if let k = k {   // artimiausias puslapis nuo Word nurodytojo
            for j in [k, k - 1, k + 1, k - 2, k + 2] where j >= 0 && j < doc.pageCount && !tocPages.contains(j) {
                if let y = hits(j, test).first { found = [(j, y)]; break }
            }
            // PDFKit kartais sujungia visą lentelės stulpelį į vieną eilutę („Nr. PA1 PA2 … PA22“) –
            // tada tinka Word nurodytas puslapis, jei jame yra šis ID kaip atskiras žodis
            if found.isEmpty, let key = idKey(raw),
               (doc.page(at: k)?.string ?? "").range(of: #"(^|\s)\#(key)(\s|$)"#, options: .regularExpression) != nil { continue }
        }
        guard found.count == 1 else {
            failed.append("p\(i + 1) „\(norm(raw))“ -> \(k.map { "p\($0 + 1)" } ?? "nėra"): rasta vietų \(found.count)")
            continue
        }
        let (j, y) = found[0]
        if k == j { continue }
        go(a, j, y)
        if k == nil { fixed += 1 } else { moved += 1 }
    }
}
if !failed.isEmpty {
    FileHandle.standardError.write("KLAIDA: PDF nuorodos nepataisytos:\n  \(failed.joined(separator: "\n  "))\n".data(using: .utf8)!)
    exit(1)
}
if fixed + moved > 0 {
    let tmp = URL(fileURLWithPath: path + ".tmp")
    guard doc.write(to: tmp) else { fatalError("KLAIDA: PDF neįrašytas") }
    _ = try FileManager.default.replaceItemAt(URL(fileURLWithPath: path), withItemAt: tmp)
}
print("PDF vidinės nuorodos: atkurta \(fixed), perkelta į tikrąjį puslapį \(moved)")
