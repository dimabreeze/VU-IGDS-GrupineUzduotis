// Šaltinio failo piktograma ataskaitai: lapo ženklas su failo plėtiniu (failo pavadinimas rašomas ataskaitoje po piktograma).
// Naudojimas: swift ikona.swift <failo pavadinimas> <išvesties PNG>
import AppKit

let args = CommandLine.arguments
guard args.count == 3 else {
    FileHandle.standardError.write("naudojimas: swift ikona.swift <pavadinimas> <out.png>\n".data(using: .utf8)!)
    exit(1)
}
let name = args[1]
let out = args[2]
let ext = (name as NSString).pathExtension.uppercased()

// Spalva pagal plėtinį
let color: NSColor
switch ext {
case "DRAWIO": color = NSColor(calibratedRed: 0.95, green: 0.55, blue: 0.10, alpha: 1)
case "XLSX": color = NSColor(calibratedRed: 0.13, green: 0.45, blue: 0.27, alpha: 1)
case "PNG": color = NSColor(calibratedRed: 0.15, green: 0.39, blue: 0.92, alpha: 1)
case "HTML", "CSS": color = NSColor(calibratedRed: 0.49, green: 0.23, blue: 0.93, alpha: 1)
default: color = NSColor.darkGray
}

let scale: CGFloat = 3
let W: CGFloat = 60, H: CGFloat = 62
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(W * scale), pixelsHigh: Int(H * scale),
                           bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                           colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
rep.size = NSSize(width: W, height: H)
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
NSColor.white.setFill()
NSRect(x: 0, y: 0, width: W, height: H).fill()

// Lapas su užlenktu kampu
let pw: CGFloat = 44, ph: CGFloat = 56, fold: CGFloat = 12
let px = (W - pw) / 2, py = (H - ph) / 2
let page = NSBezierPath()
page.move(to: NSPoint(x: px, y: py))
page.line(to: NSPoint(x: px + pw, y: py))
page.line(to: NSPoint(x: px + pw, y: py + ph - fold))
page.line(to: NSPoint(x: px + pw - fold, y: py + ph))
page.line(to: NSPoint(x: px, y: py + ph))
page.close()
NSColor(calibratedWhite: 0.97, alpha: 1).setFill()
page.fill()
NSColor(calibratedWhite: 0.45, alpha: 1).setStroke()
page.lineWidth = 1.2
page.stroke()
let corner = NSBezierPath()
corner.move(to: NSPoint(x: px + pw - fold, y: py + ph))
corner.line(to: NSPoint(x: px + pw - fold, y: py + ph - fold))
corner.line(to: NSPoint(x: px + pw, y: py + ph - fold))
corner.stroke()

// Plėtinio juosta
let band = NSRect(x: px - 6, y: py + 10, width: pw + 12, height: 16)
color.setFill()
NSBezierPath(roundedRect: band, xRadius: 3, yRadius: 3).fill()
let bandStyle = NSMutableParagraphStyle(); bandStyle.alignment = .center
let extAttrs: [NSAttributedString.Key: Any] = [
    .font: NSFont.boldSystemFont(ofSize: ext.count > 4 ? 8.5 : 10),
    .foregroundColor: NSColor.white, .paragraphStyle: bandStyle]
(ext as NSString).draw(in: NSRect(x: band.minX, y: band.minY + 2, width: band.width, height: 13), withAttributes: extAttrs)

NSGraphicsContext.restoreGraphicsState()
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: out))
