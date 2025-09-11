"""
🤖 EduBotics - Robotik-Steuerungssystem für Bildungszwecke
Ein benutzerfreundliches System entwickelt für Schüler und Lehrkräfte
"""

# ============================================================================
# SCHRITT 1: GRUNDLEGENDE IMPORTS UND SYSTEMKONFIGURATION
# ============================================================================

from asyncio import CancelledError
from loguru import logger

logger.info("🚀 Starte EduBotics System...")

import sys

print(f"📝 System-Zeichenkodierung: {sys.stdout.encoding}")

import io

# ============================================================================
# SCHRITT 2: WINDOWS-KOMPATIBILITÄT (Zeichenkodierung)
# ============================================================================

# 🔧 Behebe Kodierungsprobleme auf Windows-Systemen
if sys.platform.startswith("win") and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace"
        )
    except Exception:
        pass  # Ignore if already wrapped or in unsupported environment


from rich import print
from rich.console import Console
from rich.text import Text
from rich.align import Align

console = Console()

from phosphobot import __version__

_splash_shown = False


def print_phospho_splash() -> None:
    global _splash_shown
    if not _splash_shown:
        # Moderne ASCII-Art ohne Boxen
        print(
            f"""[cyan]
            
     [bold magenta]███████╗██████╗ ██╗   ██╗██████╗  ██████╗ ████████╗██╗ ██████╗███████╗[/bold magenta]
     [bold blue]██╔════╝██╔══██╗██║   ██║██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝██╔════╝[/bold blue]
     [bold cyan]█████╗  ██║  ██║██║   ██║██████╔╝██║   ██║   ██║   ██║██║     ███████╗[/bold cyan]
     [bold green]██╔══╝  ██║  ██║██║   ██║██╔══██╗██║   ██║   ██║   ██║██║     ╚════██║[/bold green]
     [bold yellow]███████╗██████╔╝╚██████╔╝██████╔╝╚██████╔╝   ██║   ██║╚██████╗███████║[/bold yellow]
     [bold red]╚══════╝╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝ ╚═════╝╚══════╝[/bold red]

                     [bold yellow]🤖 Robotik-Bildungssystem 🎓[/bold yellow]
                   [bold green]Für deutsche Schulen entwickelt[/bold green]
                        
                      [bold white]Version {__version__:^10}[/bold white]
                   [dim]© 2025 EduBotics Team[/dim]
                    [dim]Powered by phospho[/dim]
                         
            [bold green]✨ Willkommen zur Zukunft der Robotik! ✨[/bold green]

[/cyan]"""
        )
        
        console.print("\n")
        console.print("   [bold cyan]🚀 SCHNELLSTART[/bold cyan] - So geht's los:\n")
        console.print("      [bold white]→[/bold white] Tippe: [bold green on grey15] phosphobot run [/bold green on grey15]  und drücke Enter")
        console.print("      [bold white]→[/bold white] Öffne: [bold blue underline]http://localhost[/bold blue underline] in deinem Browser")
        console.print("      [bold white]→[/bold white] [bold yellow]Starte[/bold yellow] die Roboter-Steuerung! 🎮\n")
        
        console.print("   [dim]💡 Tipp: Für Hilfe tippe[/dim] [bold white on grey23] phosphobot --help [/bold white on grey23]\n")
        
        _splash_shown = True


print_phospho_splash()

import platform
import threading

from phosphobot.utils import fetch_latest_brew_version

_version_check_started = False


def fetch_latest_version() -> None:
    try:
        version = fetch_latest_brew_version(fail_silently=True)
        if version != "unknown" and (version != "v" + __version__):
            console.print("\n")
            if platform.system() == "Darwin":
                console.print("   ✨ [bold green]Neue Version verfügbar![/bold green]", version)
                console.print("   📦 Update mit: [bold]brew update && brew upgrade EduBotics[/bold]")
            elif platform.system() == "Linux":
                console.print("   ✨ [bold green]Neue Version verfügbar![/bold green]", version)
                console.print("   📦 Update mit: [bold]sudo apt update && sudo apt upgrade EduBotics[/bold]")
            else:
                console.print("   ✨ [bold green]Neue Version verfügbar![/bold green]", version)
                console.print("   📦 Infos unter: [bold blue]https://docs.edubotics.ai/installation#windows[/bold blue]")
    except Exception:
        pass


if not _version_check_started:
    thread = threading.Thread(target=fetch_latest_version, daemon=True)
    thread.start()
    _version_check_started = True

import socket
import time
from typing import Annotated

import typer

from phosphobot.types import SimulationMode


def init_telemetry() -> None:
    """
    This is used for automatic crash reporting.
    """
    from phosphobot.sentry import init_sentry

    init_sentry()


cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


def version_callback(value: bool) -> None:
    """📌 Zeigt die Version und beendet das Programm"""
    if value:
        console.print(f"\n   🤖 [bold cyan]EduBotics Version[/bold cyan] [bold yellow]{__version__}[/bold yellow]\n")
        raise typer.Exit()


@cli.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="📌 Zeige die EduBotics Version",
            callback=version_callback,
        ),
    ] = False,
) -> None:
    """
    🤖 [bold cyan]EduBotics[/bold cyan] - Robotik-Steuerung für Bildungszwecke
    
    🎓 Perfekt für Schüler und Lehrkräfte
    🚀 Einfach zu bedienen - Keine Programmierkenntnisse nötig
    🎮 Steuere Roboter über das Web-Dashboard
    📚 Ideal für den MINT-Unterricht
    
    [bold yellow]Hauptbefehle:[/bold yellow]
    
    • [bold green]phosphobot run[/bold green]     → Dashboard starten (das brauchst du!)
    • [bold blue]phosphobot info[/bold blue]    → Roboter-Informationen anzeigen
    • [bold cyan]phosphobot update[/bold cyan]  → System aktualisieren
    
    [dim]💡 Tipp: Starte mit 'phosphobot run' und öffne dann deinen Browser![/dim]
    """
    pass


@cli.command()
def info(
    opencv: Annotated[bool, typer.Option(help="📷 Zeige OpenCV Details")] = False,
    servos: Annotated[bool, typer.Option(help="⚙️ Zeige Servo-Motor Informationen")] = False,
) -> typer.Exit:
    """
    📊 [green]Zeigt System-Informationen und Hardware-Status[/green]
    
    🔍 Überprüfe deine Hardware-Verbindungen
    📷 Teste Kamera-Funktionalität
    🔌 Finde verbundene Roboter und Sensoren
    🛠️ Perfekt zur Fehlerbehebung
    
    [dim]💡 Verwende diesen Befehl, wenn dein Roboter nicht erkannt wird![/dim]
    """
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports()
    pid_list = [port.pid for port in ports]
    serial_numbers = [port.serial_number for port in ports]

    console.print("\n")
    console.print("   [bold cyan]📊 EDUBOTICS SYSTEM-INFORMATIONEN[/bold cyan]\n")
    
    # Roboter-Anschlüsse
    console.print("   [bold green]🔌 Verfügbare Roboter-Anschlüsse:[/bold green]")
    if ports:
        for i, port in enumerate(ports, 1):
            console.print(f"      {i}. [bold white]{port.device}[/bold white] • {port.description}")
    else:
        console.print("      [red]❌ Keine Roboter gefunden[/red]")
        console.print("      [dim]💡 Stelle sicher, dass dein Roboter angeschlossen ist[/dim]")
    
    # Seriennummern
    if serial_numbers and any(serial_numbers):
        console.print("\n   [bold green]🏷️ Geräte-Seriennummern:[/bold green]")
        for i, sn in enumerate(serial_numbers, 1):
            if sn:
                console.print(f"      {i}. [bold white]{sn}[/bold white]")
    
    # PIDs
    if pid_list and any(pid_list):
        console.print("\n   [bold green]🆔 Produkt-IDs:[/bold green]")
        for i, pid in enumerate(pid_list, 1):
            if pid:
                console.print(f"      {i}. [bold white]{pid}[/bold white]")
    
    console.print("\n")

    # Kamera-Informationen
    import cv2
    from phosphobot.camera import get_all_cameras

    console.print("   [bold blue]📷 KAMERA-STATUS[/bold blue]")
    console.print("   [yellow]⏳ Kameras werden überprüft...[/yellow]")
    
    cameras = get_all_cameras()
    time.sleep(0.5)
    cameras_status = cameras.status().model_dump_json(indent=4)
    cameras.stop()
    
    console.print("   [green]✅ Kamera erkannt und bereit![/green]")
    console.print(f"   [dim]{cameras_status}[/dim]")

    if opencv:
        console.print("\n   [bold cyan]📷 OPENCV TECHNISCHE DETAILS[/bold cyan]")
        console.print("   [dim yellow]⚠️ Für Experten[/dim yellow]\n")
        print(cv2.getBuildInformation())

    if servos:
        from phosphobot.hardware.motors.feetech import dump_servo_states_to_file
        from phosphobot.utils import get_home_app_path

        console.print("\n   [bold cyan]⚙️ SERVO-MOTOR DIAGNOSE[/bold cyan]")
        console.print("   [yellow]🔍 Analysiere Servo-Motoren...[/yellow]\n")
        
        for port in ports:
            if port.pid == 21971:
                console.print(f"      [blue]🔍 Untersuche Servo an {port.device}...[/blue]")
                dump_servo_states_to_file(
                    str(get_home_app_path() / f"servo_states_{port.device}.csv"),
                    port.device,
                )
                console.print(f"      [green]✅ Diagnose gespeichert![/green]")

    console.print("\n")
    raise typer.Exit()


def is_port_in_use(port: int, host: str) -> bool:
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True


@cli.command()
def update() -> None:
    """
    📦 [green]Software-Update Informationen[/green]
    
    🔄 Halte EduBotics aktuell
    🛡️ Erhalte Sicherheitsupdates
    ✨ Bekomme neue Features
    🐛 Profitiere von Fehlerbehebungen
    
    [dim]💡 Frage deinen Lehrer, bevor du Updates durchführst![/dim]
    """
    console.print("\n")
    console.print("   [bold cyan]📦 EDUBOTICS UPDATE-ANLEITUNG[/bold cyan]\n")
    
    console.print("   [bold yellow]🚀 So hältst du EduBotics aktuell:[/bold yellow]\n")
    console.print("   [bold red]⚠️  WICHTIG: Frage immer deinen Lehrer vorher![/bold red]\n")
    
    if platform.system() == "Darwin":
        console.print("   🍎 [bold cyan]macOS Update:[/bold cyan]")
        console.print("      Führe im Terminal aus:")
        console.print("      [bold green on grey15] brew update && brew upgrade phosphobot [/bold green on grey15]")
    elif platform.system() == "Linux":
        console.print("   🐧 [bold cyan]Linux Update:[/bold cyan]")
        console.print("      Führe im Terminal aus:")
        console.print("      [bold green on grey15] sudo apt update && sudo apt upgrade phosphobot [/bold green on grey15]")
    else:
        console.print("   🪟 [bold cyan]Windows Update:[/bold cyan]")
        console.print("      Besuche die Dokumentation:")
        console.print("      [bold blue underline]https://docs.edubotics.ai/installation#windows[/bold blue underline]")
    
    console.print("\n   [bold green]🎓 Für Schüler:[/bold green]")
    console.print("      • Updates nur mit Erlaubnis durchführen")
    console.print("      • Updates bringen neue Features")
    console.print("      • Bei Problemen: Lehrer informieren")
    console.print("\n")


@cli.command()
def run(
    chat: Annotated[bool, typer.Option(help="Run phosphobot in chat mode.")] = False,
    host: Annotated[str, typer.Option(help="🌐 Host-Adresse für den Server")] = "0.0.0.0",
    port: Annotated[int, typer.Option(help="🔌 Port für den Server")] = 80,
    simulation: Annotated[
        SimulationMode,
        typer.Option(
            help="🎮 Simulationsmodus (headless oder gui)",
        ),
    ] = SimulationMode.headless,
    only_simulation: Annotated[
        bool, typer.Option(help="🎮 Nur Simulation ausführen (ohne Hardware)")
    ] = False,
    simulate_cameras: Annotated[
        bool,
        typer.Option(help="📷 Simuliere virtuelle Kameras"),
    ] = False,
    realsense: Annotated[
        bool,
        typer.Option(help="📹 RealSense-Kamera aktivieren"),
    ] = True,
    can: Annotated[
        bool,
        typer.Option(
            help="🔗 CAN-Bus Scanning aktivieren",
        ),
    ] = True,
    cameras: Annotated[
        bool,
        typer.Option(
            help="📷 Kameras aktivieren",
        ),
    ] = True,
    max_can_interfaces: Annotated[
        int,
        typer.Option(
            help="Maximum expected CAN interfaces. Default is 4.",
        ),
    ] = 4,
    max_opencv_index: Annotated[
        int,
        typer.Option(
            help="🔢 Maximaler OpenCV-Index für Kamerasuche",
        ),
    ] = 10,
    reload: Annotated[
        bool,
        typer.Option(
            help="🔄 (Entwickler) Server bei Dateiänderungen neu laden"
        ),
    ] = False,
    profile: Annotated[
        bool,
        typer.Option(
            help="📊 (Entwickler) Performance-Profiling aktivieren"
        ),
    ] = False,
    crash_telemetry: Annotated[
        bool,
        typer.Option(help="📡 Absturz-Berichte aktivieren"),
    ] = True,
    usage_telemetry: Annotated[
        bool,
        typer.Option(help="📊 Nutzungsstatistiken aktivieren"),
    ] = True,
    telemetry: Annotated[
        bool,
        typer.Option(help="📡 Alle Telemetrie aktivieren"),
    ] = True,
) -> None:
    """
    🚀 [green]Startet das EduBotics Dashboard und den API-Server[/green]
    
    🎯 Hauptbefehl: Startet dein Robotik-Dashboard
    📱 Dashboard-URL: http://localhost
    🌐 Externer Zugriff: http://[deine-ip-adresse]
    
    🎮 Steuere deinen Roboter
    📸 Nimm Datensätze auf
    📊 Überwache Performance
    🔧 Konfiguriere Hardware
    """
    from phosphobot.app import start_server

    if not chat:
        console.print("\n")
        
        # Animierter Start-Header
        start_text = Text()
        start_text.append("🚀 ", style="bold")
        start_text.append("EDUBOTICS ", style="bold cyan")
        start_text.append("WIRD GESTARTET", style="bold green")
        console.print(Align.center(start_text))
        
        console.print("\n   [yellow]⏳ Bitte warten... System wird initialisiert...[/yellow]")
        console.print("   [dim]💡 Dies kann ein paar Sekunden dauern[/dim]\n")
        
        # Wichtige Informationen in einem übersichtlichen Format
        dashboard_url = f"http://localhost:{port}" if port != 80 else "http://localhost"
        
        console.print("   [bold green]📍 WICHTIGE INFORMATIONEN:[/bold green]\n")
        
        # Dashboard-Link hervorgehoben
        console.print("   🌐 Dashboard öffnen:")
        console.print(f"      [bold blue on grey15] {dashboard_url} [/bold blue on grey15]\n")
        
        if host == "0.0.0.0":
            console.print("   🔗 Externer Zugriff:")
            console.print("      Andere können über deine IP-Adresse zugreifen")
            console.print("      [dim]💡 Frage deinen Lehrer nach der IP[/dim]\n")
        
        # Klare Schritte ohne Nummerierung in Boxen
        console.print("   [bold yellow]🎯 NÄCHSTE SCHRITTE:[/bold yellow]\n")
        console.print("      [bold white]→[/bold white] Warte auf 'Server läuft'")
        console.print("      [bold white]→[/bold white] Öffne deinen Browser")
        console.print(f"      [bold white]→[/bold white] Gehe zu [bold blue]{dashboard_url}[/bold blue]")
        console.print("      [bold white]→[/bold white] Starte die Roboter-Steuerung! 🎮\n")
        
        console.print("   [dim]Drücke Strg+C zum Beenden[/dim]\n")
        
        start_server(
            host=host,
            port=port,
            reload=reload,
            simulation=simulation,
            only_simulation=only_simulation,
            simulate_cameras=simulate_cameras,
            realsense=realsense,
            can=can,
            cameras=cameras,
            max_opencv_index=max_opencv_index,
            max_can_interfaces=max_can_interfaces,
            profile=profile,
            crash_telemetry=crash_telemetry,
            usage_telemetry=usage_telemetry,
            telemetry=telemetry,
        )
    else:
        # Create a new thread with the server
        import threading

        # Start the server in a separate thread
        thread = threading.Thread(
            target=start_server,
            args=(
                host,
                port,
                reload,
                simulation,
                only_simulation,
                simulate_cameras,
                realsense,
                can,
                cameras,
                max_opencv_index,
                max_can_interfaces,
                profile,
                crash_telemetry,
                usage_telemetry,
                telemetry,
                True,  # silent mode to avoid logging text
            ),
            daemon=True,  # Ensure the thread exits when the main program exits
        )
        thread.start()

        # Launch in chat mode
        from phosphobot.chat.app import AgentApp

        app = AgentApp()
        app.run()


if __name__ == "__main__":
    cli()