import Cocoa

let TITLE = "Hermes"
let MESSAGE = "完成"
let DURATION = 4.0
let BACKGROUND_COLOR = NSColor(
    calibratedRed: 43.0 / 255.0,
    green: 43.0 / 255.0,
    blue: 43.0 / 255.0,
    alpha: 245.0 / 255.0
)
let TEXT_COLOR = NSColor(
    calibratedRed: 242.0 / 255.0,
    green: 245.0 / 255.0,
    blue: 247.0 / 255.0,
    alpha: 1.0
)
let MIN_WIDTH: CGFloat = 180
let MIN_HEIGHT: CGFloat = 54
let MAX_TEXT_WIDTH: CGFloat = 420
let HORIZONTAL_PADDING: CGFloat = 22
let VERTICAL_PADDING: CGFloat = 10
let CORNER_RADIUS: CGFloat = 8
let TITLE_FONT_SIZE: CGFloat = 13
let MESSAGE_FONT_SIZE: CGFloat = 12
let MESSAGE_SPACING: CGFloat = 6
let TITLE_MAX_HEIGHT: CGFloat = 38
let MESSAGE_MAX_HEIGHT: CGFloat = 68
let TITLE_MAX_LINES = 2
let MESSAGE_MAX_LINES = 4

let args = CommandLine.arguments
let toastTitle = args.count > 1 ? args[1] : TITLE
let toastMessage = args.count > 2 ? args[2] : MESSAGE
let toastDuration = args.count > 3 ? (Double(args[3]) ?? DURATION) : DURATION

final class ToastWindow: NSPanel {
    override var canBecomeKey: Bool { false }
    override var canBecomeMain: Bool { false }
}

func makeLabel(_ value: String, font: NSFont, maxLines: Int) -> NSTextField {
    let label = NSTextField(labelWithString: value)
    label.font = font
    label.textColor = TEXT_COLOR
    label.alignment = .center
    label.lineBreakMode = .byWordWrapping
    label.maximumNumberOfLines = maxLines
    label.translatesAutoresizingMaskIntoConstraints = false
    return label
}

let app = NSApplication.shared
app.setActivationPolicy(.accessory)

let titleLabel = makeLabel(
    toastTitle,
    font: NSFont.boldSystemFont(ofSize: TITLE_FONT_SIZE),
    maxLines: TITLE_MAX_LINES
)
let messageLabel = makeLabel(
    toastMessage,
    font: NSFont.systemFont(ofSize: MESSAGE_FONT_SIZE),
    maxLines: MESSAGE_MAX_LINES
)

NSLayoutConstraint.activate([
    titleLabel.widthAnchor.constraint(lessThanOrEqualToConstant: MAX_TEXT_WIDTH),
    messageLabel.widthAnchor.constraint(lessThanOrEqualToConstant: MAX_TEXT_WIDTH),
])

let stack = NSStackView(views: [titleLabel, messageLabel])
stack.orientation = .vertical
stack.alignment = .centerX
stack.spacing = MESSAGE_SPACING
stack.translatesAutoresizingMaskIntoConstraints = false

let contentView = NSView()
contentView.wantsLayer = true
contentView.layer?.backgroundColor = BACKGROUND_COLOR.cgColor
contentView.layer?.cornerRadius = CORNER_RADIUS
contentView.layer?.masksToBounds = true
contentView.addSubview(stack)

NSLayoutConstraint.activate([
    stack.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: HORIZONTAL_PADDING),
    stack.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -HORIZONTAL_PADDING),
    stack.topAnchor.constraint(equalTo: contentView.topAnchor, constant: VERTICAL_PADDING),
    stack.bottomAnchor.constraint(equalTo: contentView.bottomAnchor, constant: -VERTICAL_PADDING),
])

let fittingSize = stack.fittingSize
let windowWidth = min(
    max(fittingSize.width + (HORIZONTAL_PADDING * 2), MIN_WIDTH),
    MAX_TEXT_WIDTH + (HORIZONTAL_PADDING * 2)
)
let windowHeight = max(fittingSize.height + (VERTICAL_PADDING * 2), MIN_HEIGHT)
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
