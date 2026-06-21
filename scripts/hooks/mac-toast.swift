import Cocoa

let args = CommandLine.arguments
let toastTitle = args.count > 1 ? args[1] : "Hermes"
let toastMessage = args.count > 2 ? args[2] : "Finished"
let toastDuration = args.count > 3 ? (Double(args[3]) ?? 4.0) : 4.0

let backgroundColor = NSColor(calibratedRed: 0.17, green: 0.17, blue: 0.17, alpha: 0.96)
let textColor = NSColor(calibratedRed: 0.95, green: 0.96, blue: 0.97, alpha: 1.0)

final class ToastWindow: NSPanel {
    override var canBecomeKey: Bool { false }
    override var canBecomeMain: Bool { false }
}

func makeLabel(_ value: String, font: NSFont, maxLines: Int) -> NSTextField {
    let label = NSTextField(labelWithString: value)
    label.font = font
    label.textColor = textColor
    label.alignment = .center
    label.lineBreakMode = .byWordWrapping
    label.maximumNumberOfLines = maxLines
    label.translatesAutoresizingMaskIntoConstraints = false
    return label
}

let app = NSApplication.shared
app.setActivationPolicy(.accessory)

let maxTextWidth: CGFloat = 420
let titleLabel = makeLabel(toastTitle, font: NSFont.boldSystemFont(ofSize: 13), maxLines: 2)
let messageLabel = makeLabel(toastMessage, font: NSFont.systemFont(ofSize: 12), maxLines: 4)

NSLayoutConstraint.activate([
    titleLabel.widthAnchor.constraint(lessThanOrEqualToConstant: maxTextWidth),
    messageLabel.widthAnchor.constraint(lessThanOrEqualToConstant: maxTextWidth),
])

let stack = NSStackView(views: [titleLabel, messageLabel])
stack.orientation = .vertical
stack.alignment = .centerX
stack.spacing = 6
stack.translatesAutoresizingMaskIntoConstraints = false

let contentView = NSView()
contentView.wantsLayer = true
contentView.layer?.backgroundColor = backgroundColor.cgColor
contentView.layer?.cornerRadius = 8
contentView.layer?.masksToBounds = true
contentView.addSubview(stack)

NSLayoutConstraint.activate([
    stack.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 22),
    stack.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -22),
    stack.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 10),
    stack.bottomAnchor.constraint(equalTo: contentView.bottomAnchor, constant: -10),
])

let fittingSize = stack.fittingSize
let windowWidth = min(max(fittingSize.width + 44, 180), maxTextWidth + 44)
let windowHeight = max(fittingSize.height + 20, 54)
contentView.frame = NSRect(x: 0, y: 0, width: windowWidth, height: windowHeight)

let window = ToastWindow(
    contentRect: NSRect(x: 0, y: 0, width: windowWidth, height: windowHeight),
    styleMask: [.borderless, .nonactivatingPanel],
    backing: .buffered,
    defer: false
)
window.isOpaque = false
window.backgroundColor = .clear
window.hasShadow = true
window.level = .statusBar
window.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .transient, .ignoresCycle]
window.contentView = contentView
window.center()
window.orderFrontRegardless()

DispatchQueue.main.asyncAfter(deadline: .now() + max(0.5, toastDuration)) {
    window.orderOut(nil)
    app.terminate(nil)
}

app.run()
