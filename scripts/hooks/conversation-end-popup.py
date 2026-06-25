#!/usr/bin/env python3
import argparse
import base64
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

TITLE = "Hermes"
MESSAGE = "完成"
DURATION = 4.0
BACKGROUND_COLOR = "#F52B2B2B"
TEXT_COLOR = "#F2F5F7"
DISPLAY_ENV = "HERMES_POPUP_DISPLAY"
MIN_WIDTH = 180
MIN_HEIGHT = 54
MAX_TEXT_WIDTH = 420
HORIZONTAL_PADDING = 22
VERTICAL_PADDING = 10
CORNER_RADIUS = 8
TITLE_FONT_SIZE = 13
MESSAGE_FONT_SIZE = 12
MESSAGE_SPACING = 6
TITLE_MAX_HEIGHT = 38
MESSAGE_MAX_HEIGHT = 68


def escape_powershell(value: str) -> str:
    return value.replace("'", "''")


def is_wsl() -> bool:
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        return "microsoft" in Path("/proc/version").read_text(encoding="utf-8").lower()
    except OSError:
        return False


def read_hermes_payload() -> dict:
    if sys.stdin.isatty():
        return {}
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def ensure_macos_helper():
    helper = Path(__file__).with_name("mac-toast")
    if helper.exists():
        return helper

    source = Path(__file__).with_name("mac-toast.swift")
    if not source.exists():
        return None

    swiftc = shutil.which("swiftc")
    if swiftc is None:
        return None

    result = subprocess.run(
        [swiftc, str(source), "-o", str(helper)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        return None

    try:
        helper.chmod(0o755)
    except OSError:
        pass
    return helper


def show_macos_toast(title: str, message: str, duration: float) -> None:
    helper = ensure_macos_helper()
    if helper is None:
        return
    subprocess.run([str(helper), title, message, str(duration)], check=False)


def show_windows_toast(title: str, message: str, duration: float) -> None:
    fallback_powershell = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
    powershell = (
        shutil.which("powershell.exe")
        or shutil.which("pwsh.exe")
        or shutil.which("powershell")
    )
    if powershell is None and os.path.exists(fallback_powershell):
        powershell = fallback_powershell
    if powershell is None:
        return

    timeout_ms = max(1, int(duration * 1000))
    ps = (
        "Add-Type -AssemblyName PresentationFramework\n"
        "Add-Type @'\n"
        "using System;\n"
        "using System.Runtime.InteropServices;\n"
        "public static class HermesToastWin32 {\n"
        "  public const int GWL_EXSTYLE = -20;\n"
        "  public const int WS_EX_TOOLWINDOW = 0x00000080;\n"
        "  public const int WS_EX_NOACTIVATE = 0x08000000;\n"
        "  [DllImport(\"user32.dll\")] public static extern int GetWindowLong(IntPtr hWnd, int nIndex);\n"
        "  [DllImport(\"user32.dll\")] public static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong);\n"
        "}\n"
        "'@\n"
        "$w=New-Object System.Windows.Window\n"
        f"$w.Title='{escape_powershell(title)}'\n"
        "$w.WindowStyle='None'\n"
        "$w.AllowsTransparency=$true\n"
        "$w.ResizeMode='NoResize'\n"
        "$w.Topmost=$true\n"
        "$w.ShowActivated=$false\n"
        "$w.Focusable=$false\n"
        "$w.ShowInTaskbar=$false\n"
        "$w.SizeToContent='WidthAndHeight'\n"
        "$w.WindowStartupLocation='CenterScreen'\n"
        "$w.Background='Transparent'\n"
        f"$w.MinWidth={MIN_WIDTH}\n"
        f"$w.MinHeight={MIN_HEIGHT}\n"
        "$panel=New-Object System.Windows.Controls.StackPanel\n"
        "$panel.Orientation='Vertical'\n"
        "$panel.HorizontalAlignment='Center'\n"
        "$panel.VerticalAlignment='Center'\n"
        "$border=New-Object System.Windows.Controls.Border\n"
        f"$border.Padding='{HORIZONTAL_PADDING},{VERTICAL_PADDING},{HORIZONTAL_PADDING},{VERTICAL_PADDING}'\n"
        "$border.Margin='12'\n"
        f"$border.MinWidth={MIN_WIDTH}\n"
        f"$border.MinHeight={MIN_HEIGHT}\n"
        f"$border.MaxWidth={MAX_TEXT_WIDTH + (HORIZONTAL_PADDING * 2)}\n"
        f"$border.CornerRadius={CORNER_RADIUS}\n"
        f"$border.Background='{BACKGROUND_COLOR}'\n"
        "$shadow=New-Object System.Windows.Media.Effects.DropShadowEffect\n"
        "$shadow.BlurRadius=18\n"
        "$shadow.ShadowDepth=2\n"
        "$shadow.Opacity=0.38\n"
        "$shadow.Color='Black'\n"
        "$border.Effect=$shadow\n"
        "$border.Child=$panel\n"
        "$title=New-Object System.Windows.Controls.TextBlock\n"
        f"$title.Text='{escape_powershell(title)}'\n"
        f"$title.Foreground='{TEXT_COLOR}'\n"
        f"$title.FontSize={TITLE_FONT_SIZE}\n"
        "$title.FontWeight='Bold'\n"
        "$title.TextAlignment='Center'\n"
        "$title.TextWrapping='Wrap'\n"
        f"$title.MaxWidth={MAX_TEXT_WIDTH}\n"
        f"$title.MaxHeight={TITLE_MAX_HEIGHT}\n"
        "$title.HorizontalAlignment='Center'\n"
        "$message=New-Object System.Windows.Controls.TextBlock\n"
        f"$message.Text='{escape_powershell(message)}'\n"
        f"$message.Foreground='{TEXT_COLOR}'\n"
        f"$message.FontSize={MESSAGE_FONT_SIZE}\n"
        f"$message.Margin='0,{MESSAGE_SPACING},0,0'\n"
        "$message.TextAlignment='Center'\n"
        "$message.TextWrapping='Wrap'\n"
        f"$message.MaxWidth={MAX_TEXT_WIDTH}\n"
        f"$message.MaxHeight={MESSAGE_MAX_HEIGHT}\n"
        "$message.HorizontalAlignment='Center'\n"
        "$panel.Children.Add($title) | Out-Null\n"
        "$panel.Children.Add($message) | Out-Null\n"
        "$w.Content=$border\n"
        "$w.Add_SourceInitialized({\n"
        "  $helper=New-Object System.Windows.Interop.WindowInteropHelper -ArgumentList $w\n"
        "  $style=[HermesToastWin32]::GetWindowLong($helper.Handle,[HermesToastWin32]::GWL_EXSTYLE)\n"
        "  $style=$style -bor [HermesToastWin32]::WS_EX_TOOLWINDOW -bor [HermesToastWin32]::WS_EX_NOACTIVATE\n"
        "  [HermesToastWin32]::SetWindowLong($helper.Handle,[HermesToastWin32]::GWL_EXSTYLE,$style) | Out-Null\n"
        "})\n"
        "$w.Add_Closed({[System.Windows.Threading.Dispatcher]::CurrentDispatcher.InvokeShutdown()})\n"
        "$timer=New-Object System.Windows.Threading.DispatcherTimer\n"
        f"$timer.Interval=[TimeSpan]::FromMilliseconds({timeout_ms})\n"
        "$timer.Add_Tick({$timer.Stop();$w.Close()})\n"
        "$timer.Start()\n"
        "$w.Show()\n"
        "[System.Windows.Threading.Dispatcher]::Run()\n"
    )
    encoded = base64.b64encode(ps.encode("utf-16le")).decode("ascii")
    subprocess.run(
        [powershell, "-NoProfile", "-WindowStyle", "Hidden", "-EncodedCommand", encoded],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def show_toast(title: str, message: str, duration: float) -> None:
    if platform.system() == "Darwin":
        show_macos_toast(title, message, duration)
    elif platform.system() == "Windows" or is_wsl():
        show_windows_toast(title, message, duration)


def spawn_toast(args: argparse.Namespace) -> None:
    env = os.environ.copy()
    env[DISPLAY_ENV] = "1"
    command = [
        sys.executable,
        os.path.abspath(__file__),
        "--title",
        args.title,
        "--message",
        args.message,
        "--duration",
        str(args.duration),
    ]
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    else:
        kwargs["start_new_session"] = True

    with open(os.devnull, "rb") as stdin, open(os.devnull, "wb") as output:
        subprocess.Popen(
            command,
            stdin=stdin,
            stdout=output,
            stderr=output,
            env=env,
            **kwargs,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default=TITLE)
    parser.add_argument("--message", default=MESSAGE)
    parser.add_argument("--duration", type=float, default=DURATION)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if os.environ.get(DISPLAY_ENV) == "1":
        show_toast(args.title, args.message, args.duration)
        return

    read_hermes_payload()
    spawn_toast(args)
    print(json.dumps({}))


if __name__ == "__main__":
    main()
