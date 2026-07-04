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
BACKGROUND_COLOR = "#FF2B2B2B"
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
TOP_CENTER_RATIO = 0.35
TOP_MARGIN = 24
PROGRESS_HEIGHT = 3
PROGRESS_COLOR = "#FFF2F5F7"
PROGRESS_TRACK_COLOR = "#FF4A4F54"
CENTER_CLOSE_RATIO = 0.30


def escape_powershell(value: str) -> str:
    return value.replace("'", "''")


def is_wsl() -> bool:
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        return "microsoft" in Path("/proc/version").read_text(encoding="utf-8").lower()
    except OSError:
        return False


def ensure_macos_helper():
    helper = Path(__file__).with_name("mac-toast")
    source = Path(__file__).with_name("mac-toast.swift")
    if not source.exists():
        return helper if helper.exists() else None

    if helper.exists() and helper.stat().st_mtime >= source.stat().st_mtime:
        return helper

    swiftc = shutil.which("swiftc")
    if swiftc is None:
        return helper if helper.exists() else None

    result = subprocess.run(
        [swiftc, str(source), "-o", str(helper)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        return helper if helper.exists() else None

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
        "Add-Type -AssemblyName PresentationCore\n"
        "Add-Type @'\n"
        "using System;\n"
        "using System.Runtime.InteropServices;\n"
        "public static class HermesToastWin32 {\n"
        "  public const int GWL_EXSTYLE = -20;\n"
        "  public const int WS_EX_TOOLWINDOW = 0x00000080;\n"
        "  public const int WS_EX_NOACTIVATE = 0x08000000;\n"
        "  [DllImport(\"user32.dll\")] public static extern int GetWindowLong(IntPtr hWnd, int nIndex);\n"
        "  [DllImport(\"user32.dll\")] public static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong);\n"
        "  [DllImport(\"gdi32.dll\")] public static extern IntPtr CreateRoundRectRgn(int nLeftRect, int nTopRect, int nRightRect, int nBottomRect, int nWidthEllipse, int nHeightEllipse);\n"
        "  [DllImport(\"user32.dll\")] public static extern int SetWindowRgn(IntPtr hWnd, IntPtr hRgn, bool bRedraw);\n"
        "}\n"
        "'@\n"
        "$w=New-Object System.Windows.Window\n"
        f"$w.Title='{escape_powershell(title)}'\n"
        "$w.WindowStyle='None'\n"
        "$w.AllowsTransparency=$false\n"
        "$w.ResizeMode='NoResize'\n"
        "$w.Topmost=$true\n"
        "$w.ShowActivated=$false\n"
        "$w.Focusable=$false\n"
        "$w.ShowInTaskbar=$false\n"
        "$w.SizeToContent='WidthAndHeight'\n"
        "$w.WindowStartupLocation='Manual'\n"
        f"$w.Background='{BACKGROUND_COLOR}'\n"
        f"$w.MinWidth={MIN_WIDTH}\n"
        f"$w.MinHeight={MIN_HEIGHT}\n"
        "$root=New-Object System.Windows.Controls.Grid\n"
        "$contentRow=New-Object System.Windows.Controls.RowDefinition\n"
        "$contentRow.Height='Auto'\n"
        "$progressRow=New-Object System.Windows.Controls.RowDefinition\n"
        f"$progressRow.Height='{PROGRESS_HEIGHT}'\n"
        "$root.RowDefinitions.Add($contentRow) | Out-Null\n"
        "$root.RowDefinitions.Add($progressRow) | Out-Null\n"
        "$panel=New-Object System.Windows.Controls.StackPanel\n"
        "$panel.Orientation='Vertical'\n"
        "$panel.HorizontalAlignment='Center'\n"
        "$panel.VerticalAlignment='Center'\n"
        f"$panel.Margin='{HORIZONTAL_PADDING},{VERTICAL_PADDING},{HORIZONTAL_PADDING},{VERTICAL_PADDING}'\n"
        "$border=New-Object System.Windows.Controls.Border\n"
        "$border.Padding='0'\n"
        "$border.Margin='0'\n"
        f"$border.MinWidth={MIN_WIDTH}\n"
        f"$border.MinHeight={MIN_HEIGHT}\n"
        f"$border.MaxWidth={MAX_TEXT_WIDTH + (HORIZONTAL_PADDING * 2)}\n"
        f"$border.CornerRadius={CORNER_RADIUS}\n"
        f"$border.Background='{BACKGROUND_COLOR}'\n"
        "$border.Child=$root\n"
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
        "[System.Windows.Controls.Grid]::SetRow($panel,0)\n"
        "$root.Children.Add($panel) | Out-Null\n"
        "$progressTrack=New-Object System.Windows.Controls.Grid\n"
        f"$progressTrack.Height={PROGRESS_HEIGHT}\n"
        "$progressTrack.HorizontalAlignment='Stretch'\n"
        "$progressTrack.VerticalAlignment='Bottom'\n"
        f"$progressTrack.Background='{PROGRESS_TRACK_COLOR}'\n"
        "$progressTrack.ClipToBounds=$true\n"
        "$progressBar=New-Object System.Windows.Controls.Border\n"
        f"$progressBar.Height={PROGRESS_HEIGHT}\n"
        "$progressBar.HorizontalAlignment='Stretch'\n"
        "$progressBar.VerticalAlignment='Stretch'\n"
        f"$progressBar.Background='{PROGRESS_COLOR}'\n"
        "$progressScale=New-Object System.Windows.Media.ScaleTransform\n"
        "$progressScale.ScaleX=1\n"
        "$progressScale.ScaleY=1\n"
        "$progressBar.RenderTransform=$progressScale\n"
        "$progressBar.RenderTransformOrigin=New-Object System.Windows.Point -ArgumentList 0,0.5\n"
        "$progressTrack.Children.Add($progressBar) | Out-Null\n"
        "[System.Windows.Controls.Grid]::SetRow($progressTrack,1)\n"
        "$root.Children.Add($progressTrack) | Out-Null\n"
        "$w.Content=$border\n"
        "$script:isClosing=$false\n"
        "function Close-HermesToast {\n"
        "  if ($script:isClosing) { return }\n"
        "  $script:isClosing=$true\n"
        "  if ($closeTimer) { $closeTimer.Stop() }\n"
        "  $progressScale.BeginAnimation([System.Windows.Media.ScaleTransform]::ScaleXProperty,$null)\n"
        "  $w.Close()\n"
        "}\n"
        "$border.Add_PreviewMouseDown({Close-HermesToast})\n"
        "$border.Add_MouseMove({\n"
        "  $position=[System.Windows.Input.Mouse]::GetPosition($border)\n"
        "  $width=$border.ActualWidth\n"
        "  $height=$border.ActualHeight\n"
        "  if ($width -le 0 -or $height -le 0) { return }\n"
        f"  $xMin=$width * ((1 - {CENTER_CLOSE_RATIO}) / 2)\n"
        f"  $xMax=$width * ((1 + {CENTER_CLOSE_RATIO}) / 2)\n"
        f"  $yMin=$height * ((1 - {CENTER_CLOSE_RATIO}) / 2)\n"
        f"  $yMax=$height * ((1 + {CENTER_CLOSE_RATIO}) / 2)\n"
        "  if ($position.X -ge $xMin -and $position.X -le $xMax -and $position.Y -ge $yMin -and $position.Y -le $yMax) { Close-HermesToast }\n"
        "})\n"
        "$w.Add_SourceInitialized({\n"
        "  $helper=New-Object System.Windows.Interop.WindowInteropHelper -ArgumentList $w\n"
        "  $style=[HermesToastWin32]::GetWindowLong($helper.Handle,[HermesToastWin32]::GWL_EXSTYLE)\n"
        "  $style=$style -bor [HermesToastWin32]::WS_EX_TOOLWINDOW -bor [HermesToastWin32]::WS_EX_NOACTIVATE\n"
        "  [HermesToastWin32]::SetWindowLong($helper.Handle,[HermesToastWin32]::GWL_EXSTYLE,$style) | Out-Null\n"
        "})\n"
        "$w.Add_ContentRendered({\n"
        "  $workArea=[System.Windows.SystemParameters]::WorkArea\n"
        "  $w.Left=$workArea.Left + (($workArea.Width - $w.ActualWidth) / 2)\n"
        f"  $targetCenterY=$workArea.Top + ($workArea.Height * {TOP_CENTER_RATIO})\n"
        f"  $w.Top=[Math]::Max($workArea.Top + {TOP_MARGIN}, $targetCenterY - ($w.ActualHeight / 2))\n"
        "  $helper=New-Object System.Windows.Interop.WindowInteropHelper -ArgumentList $w\n"
        "  $source=[System.Windows.PresentationSource]::FromVisual($w)\n"
        "  $scaleX=1.0\n"
        "  $scaleY=1.0\n"
        "  if ($source -and $source.CompositionTarget) {\n"
        "    $scaleX=$source.CompositionTarget.TransformToDevice.M11\n"
        "    $scaleY=$source.CompositionTarget.TransformToDevice.M22\n"
        "  }\n"
        "  $regionWidth=[Math]::Max(1,[int][Math]::Round($w.ActualWidth * $scaleX))\n"
        "  $regionHeight=[Math]::Max(1,[int][Math]::Round($w.ActualHeight * $scaleY))\n"
        f"  $regionRadiusX=[Math]::Max(1,[int][Math]::Round({CORNER_RADIUS * 2} * $scaleX))\n"
        f"  $regionRadiusY=[Math]::Max(1,[int][Math]::Round({CORNER_RADIUS * 2} * $scaleY))\n"
        "  $region=[HermesToastWin32]::CreateRoundRectRgn(0,0,$regionWidth + 1,$regionHeight + 1,$regionRadiusX,$regionRadiusY)\n"
        "  if ($region -ne [IntPtr]::Zero) {[HermesToastWin32]::SetWindowRgn($helper.Handle,$region,$true) | Out-Null}\n"
        "  $closeTimer.Start()\n"
        "  $progressAnimation=New-Object System.Windows.Media.Animation.DoubleAnimation\n"
        "  $progressAnimation.From=1.0\n"
        "  $progressAnimation.To=0.0\n"
        "  $progressAnimation.Duration=New-Object System.Windows.Duration -ArgumentList ([TimeSpan]::FromMilliseconds($script:toastTimeoutMs))\n"
        "  $progressAnimation.FillBehavior='HoldEnd'\n"
        "  $progressScale.BeginAnimation([System.Windows.Media.ScaleTransform]::ScaleXProperty,$progressAnimation)\n"
        "})\n"
        "$w.Add_Closed({[System.Windows.Threading.Dispatcher]::CurrentDispatcher.InvokeShutdown()})\n"
        f"$script:toastTimeoutMs={timeout_ms}\n"
        "$closeTimer=New-Object System.Windows.Threading.DispatcherTimer\n"
        f"$closeTimer.Interval=[TimeSpan]::FromMilliseconds({timeout_ms})\n"
        "$closeTimer.Add_Tick({Close-HermesToast})\n"
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


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default=TITLE)
    parser.add_argument("--message", default=MESSAGE)
    parser.add_argument("--duration", type=float, default=DURATION)
    parser.add_argument("--skip-tool-name", action="append", default=[])
    parsed = parser.parse_args(args)
    return parsed.title, parsed.message, parsed.duration, set(parsed.skip_tool_name)


def read_hook_input() -> dict:
    try:
        input_data = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}
    return input_data if isinstance(input_data, dict) else {}


def should_skip_for_hook_input(skip_tool_names, input_data) -> bool:
    if not skip_tool_names:
        return False
    tool_name = input_data.get("tool_name") or input_data.get("toolName")
    return tool_name in skip_tool_names


def append_cwd_to_message(message: str, input_data: dict) -> str:
    cwd = input_data.get("cwd")
    if not isinstance(cwd, str) or not cwd.strip():
        return message

    cwd = cwd.strip()
    workspace = Path(cwd).name or cwd
    return f"工作区: {workspace}\n{message}"


def spawn_toast(title: str, message: str, duration: float) -> None:
    env = os.environ.copy()
    env[DISPLAY_ENV] = "1"
    with open(os.devnull, "rb") as stdin, open(os.devnull, "wb") as output:
        subprocess.Popen(
            [
                sys.executable,
                os.path.abspath(__file__),
                "--title",
                title,
                "--message",
                message,
                "--duration",
                str(duration),
            ],
            stdin=stdin,
            stdout=output,
            stderr=output,
            env=env,
            start_new_session=True,
        )


def main() -> None:
    title, message, duration, skip_tool_names = parse_args(sys.argv[1:])
    if os.environ.get(DISPLAY_ENV) == "1":
        show_toast(title, message, duration)
        return

    input_data = read_hook_input()
    if should_skip_for_hook_input(skip_tool_names, input_data):
        print(json.dumps({}))
        return
    spawn_toast(title, append_cwd_to_message(message, input_data), duration)
    print(json.dumps({}))


if __name__ == "__main__":
    main()
