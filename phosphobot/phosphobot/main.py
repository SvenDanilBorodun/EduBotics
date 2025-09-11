"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🤖 EduBotics Hauptprogramm 🤖                      ║
║                                                                              ║
║  Ein benutzerfreundliches Robotik-Steuerungssystem für Bildungszwecke        ║
║  Entwickelt für Schüler und Lehrkräfte                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
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
        logger.info("✅ Windows-Zeichenkodierung erfolgreich angepasst")
    except Exception:
        pass  # Ignoriere Fehler, falls bereits konfiguriert


from rich import print

from phosphobot import __version__

_splash_shown = False


def print_phospho_splash() -> None:
    """
    🎨 Zeigt den bunten EduBotics Willkommensbildschirm
    Wird nur einmal beim Start angezeigt
    """
    global _splash_shown
    if not _splash_shown:
        print(
            f"""[cyan]
    
[bold blue][/bold blue]
[bold blue][/bold blue]                                                                              [bold blue][/bold blue]
[bold blue][/bold blue]     [bold magenta]███████╗██████╗ ██╗   ██╗██████╗  ██████╗ ████████╗██╗ ██████╗███████╗[/bold magenta]     [bold blue][/bold blue]  
[bold blue][/bold blue]     [bold magenta]██╔════╝██╔══██╗██║   ██║██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝██╔════╝[/bold magenta]     [bold blue][/bold blue]  
[bold blue][/bold blue]     [bold magenta]█████╗  ██║  ██║██║   ██║██████╔╝██║   ██║   ██║   ██║██║     ███████╗[/bold magenta]     [bold blue][/bold blue]  
[bold blue][/bold blue]     [bold magenta]██╔══╝  ██║  ██║██║   ██║██╔══██╗██║   ██║   ██║   ██║██║     ╚════██║[/bold magenta]     [bold blue][/bold blue]  
[bold blue][/bold blue]     [bold magenta]███████╗██████╔╝╚██████╔╝██████╔╝╚██████╔╝   ██║   ██║╚██████╗███████║[/bold magenta]     [bold blue][/bold blue]  
[bold blue][/bold blue]     [bold magenta]╚══════╝╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝ ╚═════╝╚══════╝[/bold magenta]     [bold blue][/bold blue]  
[bold blue][/bold blue]                                                                              [bold blue][/bold blue]
[bold blue][/bold blue]                    [bold yellow]🤖 Robotik-Bildungssystem 🎓[/bold yellow]                       [bold blue][/bold blue]               
[bold blue][/bold blue]                                                                              [bold blue][/bold blue]
[bold blue][/bold blue]                          [bold white]Version {__version__:^10}[/bold white]                         [bold blue][/bold blue]                   
[bold blue][/bold blue]                      [dim]Copyright © 2025 EduBotics Team[/dim]                     [bold blue][/bold blue]               
[bold blue][/bold blue]                        [dim]Powered by phospho technology[/dim]                    [bold blue][/bold blue]              
[bold blue][/bold blue]                                                                              [bold blue][/bold blue]
[bold blue][/bold blue]               [bold green]✨ Willkommen zur Zukunft der Robotik! ✨[/bold green]                  [bold blue][/bold blue]
[bold blue][/bold blue]                                                                              [bold blue][/bold blue]
[bold blue][/bold blue]
    
            [/cyan]"""
        )
        _splash_shown = True


print_phospho_splash()

import platform
import threading

from phosphobot.utils import fetch_latest_brew_version

_version_check_started = False


def fetch_latest_version() -> None:
    """
    🔍 Überprüft, ob eine neue Version von EduBotics verfügbar ist
    Läuft im Hintergrund, um den Start nicht zu verlangsamen
    """
    try:
        version = fetch_latest_brew_version(fail_silently=True)
        if version != "unknown" and (version != "v" + __version__):
            # 🍎 macOS Update-Anweisung
            if platform.system() == "Darwin":
                logger.warning(
                    f"✨ Neue Version {version} von EduBotics verfügbar! \n"
                    f"📦 Aktualisieren mit: \n"
                    f"   brew update && brew upgrade EduBotics"
                )
            # 🐧 Linux Update-Anweisung
            elif platform.system() == "Linux":
                logger.warning(
                    f"✨ Neue Version {version} von EduBotics verfügbar! \n"
                    f"📦 Aktualisieren mit: \n"
                    f"   sudo apt update && sudo apt upgrade EduBotics"
                )
            # 🪟 Windows Update-Anweisung
            else:
                logger.warning(
                    f"✨ Neue Version {version} von EduBotics verfügbar! \n"
                    f"📦 Bitte besuche: https://docs.edubotics.ai/installation#windows"
                )
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
    📊 Initialisiert die automatische Fehlerberichterstattung
    Hilft uns, EduBotics zu verbessern!
    """
    from phosphobot.sentry import init_sentry

    init_sentry()


def get_local_ip() -> str:
    """
    🌐 Ermittelt die lokale IP-Adresse des Servers
    Nützlich für Netzwerkverbindungen im Klassenzimmer
    """
    try:
        # Erstelle einen temporären Socket zur IP-Ermittlung
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Google DNS (sendet keine echten Daten)
            server_ip = s.getsockname()[0]
    except Exception:
        server_ip = "localhost"
    return server_ip


# ============================================================================
# KOMMANDOZEILEN-INTERFACE (CLI)
# ============================================================================

cli = typer.Typer(
    no_args_is_help=True, 
    rich_markup_mode="rich",
    help="🤖 EduBotics - Das Robotik-Steuerungssystem für Bildung"
)


def version_callback(value: bool) -> None:
    """📌 Zeigt die Version und beendet das Programm"""
    if value:
        print(f"🤖 EduBotics Version {__version__}")
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
    🤖 EduBotics - Ein Robotik-Teleoperation-Server für Bildungszwecke
    
    Perfekt für Schüler und Lehrkräfte zum Lernen und Experimentieren!
    """
    pass


# ============================================================================
# INFO-KOMMANDO: ZEIGE SYSTEM-INFORMATIONEN
# ============================================================================

@cli.command()
def info(
    opencv: Annotated[bool, typer.Option(help="📷 Zeige OpenCV Details")] = False,
    servos: Annotated[bool, typer.Option(help="⚙️ Zeige Servo-Motor Informationen")] = False,
) -> typer.Exit:
    """
    📋 Zeigt alle verfügbaren Anschlüsse und Kameras
    
    Sehr nützlich für die Fehlersuche und Systemdiagnose!
    """
    import serial.tools.list_ports

    # 🔌 Sammle Informationen über serielle Ports
    ports = serial.tools.list_ports.comports()
    pid_list = [port.pid for port in ports]
    serial_numbers = [port.serial_number for port in ports]

    print("\n" + "═"*80)
    print("[bold cyan]        📊 EDUBOTICS SYSTEM-INFORMATIONEN 📊[/bold cyan]")
    print("═"*80 + "\n")
    
    print(f"[bold green]🔌 Verfügbare Roboter-Anschlüsse:[/bold green]")
    if ports:
        for i, port in enumerate(ports, 1):
            print(f"   {i}. [bold white]{port.device}[/bold white] - {port.description}")
    else:
        print("   [red]❌ Keine Roboter-Anschlüsse gefunden[/red]")
        print("   [dim]💡 Stelle sicher, dass dein Roboter angeschlossen ist[/dim]")
    
    print(f"\n[bold green]🏷️ Geräte-Seriennummern:[/bold green]")
    if serial_numbers and any(serial_numbers):
        for i, sn in enumerate(serial_numbers, 1):
            if sn:
                print(f"   {i}. [bold white]{sn}[/bold white]")
    else:
        print("   [yellow]⚠️ Keine Seriennummern gefunden[/yellow]")
        
    print(f"\n[bold green]🆔 Produkt-IDs (PIDs):[/bold green]")
    if pid_list and any(pid_list):
        for i, pid in enumerate(pid_list, 1):
            if pid:
                print(f"   {i}. [bold white]{pid}[/bold white]")
    else:
        print("   [yellow]⚠️ Keine PIDs gefunden[/yellow]")
    
    print("\n" + "─"*80 + "\n")

    # 📷 Kamera-Informationen
    import cv2
    from phosphobot.camera import get_all_cameras

    print("[bold blue]📷 KAMERA-STATUS 📷[/bold blue]")
    print("─"*80)
    print("[yellow]⏳ Kameras werden überprüft... Bitte warten...[/yellow]")
    cameras = get_all_cameras()
    time.sleep(0.5)
    cameras_status = cameras.status().model_dump_json(indent=4)
    cameras.stop()
    print(f"\n[green]✅ Kamera-Konfiguration:[/green]")
    print(f"[dim]{cameras_status}[/dim]")

    # OpenCV Details (optional)
    if opencv:
        print("\n" + "═"*80)
        print("[bold cyan]        📷 OPENCV BUILD-INFORMATIONEN 📷[/bold cyan]")
        print("═"*80)
        print("[dim][yellow]⚠️ Für Experten: Technische OpenCV-Details[/yellow][/dim]\n")
        print(cv2.getBuildInformation())

    # Servo-Motor Diagnose (optional)
    if servos:
        from phosphobot.hardware.motors.feetech import (  # type: ignore
            dump_servo_states_to_file,
        )
        from phosphobot.utils import get_home_app_path

        print("\n" + "═"*80)
        print("[bold cyan]        ⚙️ SERVO-MOTOR DIAGNOSE ⚙️[/bold cyan]")
        print("═"*80)
        print("[yellow]🔍 Analysiere Servo-Motoren... Dies kann etwas dauern...[/yellow]\n")
        
        # Diagnose für SO-100 Servos
        for port in ports:
            if port.pid == 21971:
                print(f"   [blue]🔍 Untersuche Servo an {port.device}...[/blue]")
                dump_servo_states_to_file(
                    str(get_home_app_path() / f"servo_states_{port.device}.csv"),
                    port.device,
                )
                print(f"   [green]✅ Diagnose gespeichert![/green]")

    raise typer.Exit()


def is_port_in_use(port: int, host: str) -> bool:
    """
    🔍 Überprüft, ob ein Port bereits verwendet wird
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True


# ============================================================================
# UPDATE-KOMMANDO: ZEIGE UPDATE-INFORMATIONEN
# ============================================================================

@cli.command()
def update() -> None:
    """
    📦 Zeigt Informationen zur Software-Aktualisierung
    
    Halte EduBotics immer auf dem neuesten Stand!
    """
    print("\n" + "═"*80)
    print("[bold cyan]        📦 EDUBOTICS UPDATE-ANLEITUNG 📦[/bold cyan]")
    print("═"*80 + "\n")
    
    print("[bold yellow]🚀 Halte dein EduBotics System aktuell![/bold yellow]\n")
    
    if platform.system() == "Darwin":
        print("🍎 [bold cyan]macOS Update:[/bold cyan]")
        print("   Führe folgenden Befehl im Terminal aus:")
        print("   [green]brew update && brew upgrade phosphobot[/green]")
    elif platform.system() == "Linux":
        print("🐧 [bold cyan]Linux Update:[/bold cyan]")
        print("   Führe folgenden Befehl im Terminal aus:")
        print("   [green]sudo apt update && sudo apt upgrade phosphobot[/green]")
    else:
        print("🪟 [bold cyan]Windows Update:[/bold cyan]")
        print("   Bitte besuche die Dokumentation:")
        print("   [green]https://docs.edubotics.ai/installation#windows[/green]")
    
    print("\n" + "═"*80 + "\n")


# ============================================================================
# RUN-KOMMANDO: HAUPTFUNKTION ZUM STARTEN DES SERVERS
# ============================================================================

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
    
    Steuere deinen Roboter und nimm Datensätze auf!
    """
    from phosphobot.app import start_server

    if not chat:
        print("\n" + "═"*80)
        print("[bold cyan]        🚀 EDUBOTICS SERVER WIRD GESTARTET 🚀[/bold cyan]")
        print("═"*80)
        print("\n[yellow]⏳ Bitte warten... Das System wird initialisiert...[/yellow]")
        print("[dim]💡 Dies kann ein paar Sekunden dauern[/dim]\n")
        
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