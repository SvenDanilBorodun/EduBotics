from asyncio import CancelledError
from loguru import logger

logger.info("🎓 EduBotics wird gestartet - Dein Lernbegleiter für Robotik! 🤖")

import sys

print(f"sys.stdout.encoding = {sys.stdout.encoding}")

import io

# Fix encoding issues on Windows
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

from phosphobot import __version__

_splash_shown = False


def print_edubotics_splash():
    global _splash_shown
    if not _splash_shown:
        print(
            f"""[bold bright_blue]
    ╔══════════════════════════════════════════════════════════════════════════════════╗
    ║                              🎓 [bright_green]EduBotics[/bright_green] 🤖                              ║
    ║                        [bright_cyan]Dein Robotik-Lernbegleiter[/bright_cyan]                         ║
    ╠══════════════════════════════════════════════════════════════════════════════════╣
    ║                                                                                  ║
    ║    🔬 [yellow]Experimentieren[/yellow]  │  🔧 [green]Programmieren[/green]  │  🚀 [magenta]Entdecken[/magenta]           ║
    ║                                                                                  ║
    ║         [bright_white]"Lernen durch Machen - Robotik für alle!"[/bright_white]                    ║
    ║                                                                                  ║
    ║    Version: [bright_yellow]{__version__}[/bright_yellow]                                                        ║
    ║    Für deutsche Schüler und Studenten entwickelt 🇩🇪                            ║
    ║                                                                                  ║
    ╚══════════════════════════════════════════════════════════════════════════════════╝[/bold bright_blue]

    [bright_green]✨ Willkommen bei EduBotics! Lass uns gemeinsam die Welt der Robotik erkunden! ✨[/bright_green]
    [cyan]💡 Tipp: Verwende '--help' für alle verfügbaren Befehle[/cyan]
            """
        )
        _splash_shown = True


print_edubotics_splash()

import platform
import threading

from phosphobot.utils import fetch_latest_brew_version

_version_check_started = False


def fetch_latest_version():
    try:
        version = fetch_latest_brew_version(fail_silently=True)
        if version != "unknown" and (version != "v" + __version__):
            if platform.system() == "Darwin":
                logger.warning(
                    f"🎓 [bright_green]Neue EduBotics Version {version} verfügbar![/bright_green] \n📦 Update mit: [cyan]brew update && brew upgrade edubotics[/cyan]"
                )
            elif platform.system() == "Linux":
                logger.warning(
                    f"🎓 [bright_green]Neue EduBotics Version {version} verfügbar![/bright_green] \n📦 Update mit: [cyan]sudo apt update && sudo apt upgrade edubotics[/cyan]"
                )
            else:
                logger.warning(
                    f"🎓 [bright_green]Neue EduBotics Version {version} verfügbar![/bright_green] \n📦 Update-Anleitung: [cyan]https://edubotics.de/installation#windows[/cyan]"
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
import uvicorn
from phosphobot.configs import config
from phosphobot.types import SimulationMode


def init_telemetry() -> None:
    """
    This is used for automatic crash reporting.
    """
    from phosphobot.sentry import init_sentry

    init_sentry()


def get_local_ip() -> str:
    """
    Get the local IP address of the server.
    """
    try:
        # Create a temporary socket to get the local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Doesn't actually send data
            server_ip = s.getsockname()[0]
    except Exception:
        server_ip = "localhost"
    return server_ip


cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


def version_callback(value: bool):
    if value:
        print(f"🎓 [bright_green]EduBotics[/bright_green] [bright_yellow]{__version__}[/bright_yellow] 🤖\n[cyan]Dein Robotik-Lernbegleiter für deutsche Studenten![/cyan]")
        raise typer.Exit()


@cli.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="🎓 Zeige die EduBotics Version und beende das Programm",
            callback=version_callback,
        ),
    ] = False,
):
    """
    🎓 [bright_green]EduBotics[/bright_green] - Dein interaktiver Robotik-Lernserver für deutsche Studenten! 🤖
    
    [bright_cyan]Lerne Robotik durch praktisches Experimentieren:[/bright_cyan]
    • 🔬 Steuere Roboter in Echtzeit
    • 📈 Sammle und analysiere Daten
    • 📚 Verstehe Robotik-Konzepte
    • 🎯 Entwickle eigene Anwendungen
    """
    pass


@cli.command()
def info(
    opencv: Annotated[bool, typer.Option(help="📷 Zeige OpenCV Informationen für Kamera-Debugging")] = False,
    servos: Annotated[bool, typer.Option(help="⚙️ Zeige Servo-Motor Informationen für Hardware-Debugging")] = False,
):
    """
    🔍 [bright_yellow]Hardware-Diagnose:[/bright_yellow] Zeige alle seriellen Ports und Kamera-Informationen
    
    [bright_cyan]Perfekt für:[/bright_cyan]
    • 🔌 Hardware-Verbindungen prüfen
    • 📷 Kamera-Probleme lösen
    • ⚙️ Servo-Motoren konfigurieren
    • 🔧 Technische Probleme diagnostizieren
    """
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports()
    pid_list = [port.pid for port in ports]
    serial_numbers = [port.serial_number for port in ports]

    print("\n")
    print(
        f"🔌 [bright_green]Verfügbare serielle Ports:[/bright_green] [cyan]{', '.join([port.device for port in ports]) or 'Keine gefunden'}[/cyan]"
    )
    print(
        f"🏷️ [bright_green]Seriennummern:[/bright_green] [cyan]{', '.join([str(sn) for sn in serial_numbers]) or 'Keine verfügbar'}[/cyan]"
    )
    print(f"🆔 [bright_green]Hardware PIDs:[/bright_green] [cyan]{' '.join([str(pid) for pid in pid_list]) or 'Keine erkannt'}[/cyan]")
    print("\n")

    import cv2

    from phosphobot.camera import get_all_cameras

    cameras = get_all_cameras()
    time.sleep(0.5)
    cameras_status = cameras.status().model_dump_json(indent=4)
    cameras.stop()
    print(f"📷 [bright_green]Kamera-Status:[/bright_green]\n[cyan]{cameras_status}[/cyan]")

    if opencv:
        print(cv2.getBuildInformation())

    if servos:
        from phosphobot.hardware.motors.feetech import dump_servo_states_to_file  # type: ignore
        from phosphobot.utils import get_home_app_path

        # Diagnose SO-100 servos
        for port in ports:
            if port.pid == 21971:
                dump_servo_states_to_file(
                    get_home_app_path() / f"servo_states_{port.device}.csv",
                    port.device,
                )

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
def update():
    """
    📦 [bright_green]EduBotics Update-Hilfe:[/bright_green] Zeige wie du auf die neueste Version aktualisierst
    
    [bright_cyan]Halte deine Lernumgebung immer aktuell![/bright_cyan]
    • ✨ Neue Funktionen
    • 🔧 Verbesserungen
    • 🛡️ Sicherheitsupdates
    """
    if platform.system() == "Darwin":
        logger.warning(
            "🍎 [bright_green]macOS Update:[/bright_green] Führe folgenden Befehl aus:\n"
            "📦 [cyan]brew update && brew upgrade edubotics[/cyan]"
        )
    elif platform.system() == "Linux":
        logger.warning(
            "🐧 [bright_green]Linux Update:[/bright_green] Führe folgenden Befehl aus:\n"
            "📦 [cyan]sudo apt update && sudo apt upgrade edubotics[/cyan]"
        )
    else:
        logger.warning(
            "💻 [bright_green]Windows Update:[/bright_green] Besuche die Dokumentation:\n"
            "🌐 [cyan]https://edubotics.de/installation#windows[/cyan]\n"
            "💡 [yellow]Tipp: Lade die neueste Version direkt von der Website herunter![/yellow]"
        )


@cli.command()
def run(
    host: Annotated[str, typer.Option(help="🌐 Server-Host Adresse (Standard: alle Interfaces)")] = "0.0.0.0",
    port: Annotated[int, typer.Option(help="🔌 Port für den EduBotics Lernserver (Standard: 80)")] = 80,
    simulation: Annotated[
        SimulationMode,
        typer.Option(
            help="🎮 Simulationsmodus: 'headless' (ohne GUI) oder 'gui' (mit grafischer Oberfläche)",
        ),
    ] = SimulationMode.headless,
    only_simulation: Annotated[
        bool, typer.Option(help="🗺️ Nur Simulation ohne echte Hardware (perfekt zum Lernen!)")
    ] = False,
    simulate_cameras: Annotated[
        bool,
        typer.Option(help="📷 Simuliere Kameras für das Lernen ohne echte Hardware"),
    ] = False,
    realsense: Annotated[
        bool,
        typer.Option(help="📹 Aktiviere RealSense 3D-Kamera für Tiefenwahrnehmung"),
    ] = True,
    can: Annotated[
        bool,
        typer.Option(
            help="🚗 Aktiviere CAN-Bus Geräte-Erkennung (deaktivieren bei Konflikten)",
        ),
    ] = True,
    cameras: Annotated[
        bool,
        typer.Option(
            help="📷 Aktiviere alle Kameras (deaktivieren bei Hardware-Konflikten)",
        ),
    ] = True,
    max_opencv_index: Annotated[
        int,
        typer.Option(
            help="🔢 Maximaler OpenCV Index für Kamera-Suche (Standard: 10)",
        ),
    ] = 10,
    reload: Annotated[
        bool,
        typer.Option(
            help="🔄 (Entwicklung) Auto-Reload bei Code-Änderungen (nicht mit Kameras verwenden)"
        ),
    ] = False,
    profile: Annotated[
        bool,
        typer.Option(
            help="📈 (Entwicklung) Performance-Profiling aktivieren (erzeugt profile.html)"
        ),
    ] = False,
    crash_telemetry: Annotated[
        bool,
        typer.Option(help="🛡️ Crash-Reporting zur Verbesserung der Software"),
    ] = True,
    usage_telemetry: Annotated[
        bool,
        typer.Option(help="📈 Nutzungsanalyse zur Verbesserung der Lernerfahrung"),
    ] = True,
    telemetry: Annotated[
        bool,
        typer.Option(help="📋 Alle Telemetrie-Funktionen (Crash- und Nutzungsdaten)"),
    ] = True,
):
    """
    🎓 [bright_green]Starte den EduBotics Lernserver![/bright_green] Experimentiere mit Robotik und sammle Erfahrungen!
    
    [bright_cyan]🚀 Was EduBotics für dich bereithält:[/bright_cyan]
    • 🕹️ Steuere Roboter per Tastatur, Gamepad oder Leader-Arm
    • ⚡ Trainiere KI-Modelle (ACT, π0, gr00t-n1.5) mit einem Klick
    • 🦾 Kompatibel mit SO-100, SO-101, Unitree Go2, Agilex Piper
    • 🚪 Entwicklerfreundliche API für eigene Projekte
    • 🤗 Voll kompatibel mit LeRobot und HuggingFace
    • 📸 Unterstützt alle Kameratypen (klassisch, Tiefe, Stereo)
    • 🖥️ Läuft auf macOS, Linux und Windows
    
    [bright_yellow]🎯 Perfekt für deutsche Studenten:[/bright_yellow]
    • 📚 Verstehe Robotik durch praktisches Lernen
    • 🔬 Sammle Datensätze in wenigen Minuten
    • 🧠 Lerne maschinelles Lernen hands-on
    • 🛡️ Sichere Lernumgebung mit Simulation
    
    [yellow]💡 Tipp: Starte mit --only-simulation zum gefahrlosen Experimentieren![/yellow]
    """

    config.SIM_MODE = simulation
    config.ONLY_SIMULATION = only_simulation
    config.SIMULATE_CAMERAS = simulate_cameras
    config.ENABLE_REALSENSE = realsense
    config.ENABLE_CAMERAS = cameras
    config.PORT = port
    config.PROFILE = profile
    config.CRASH_TELEMETRY = crash_telemetry  # Enable crash telemetry by default
    config.USAGE_TELEMETRY = usage_telemetry  # Enable usage telemetry by default
    config.ENABLE_CAN = can
    config.MAX_OPENCV_INDEX = max_opencv_index

    if not telemetry:
        config.CRASH_TELEMETRY = False
        config.USAGE_TELEMETRY = False

    # Start the FastAPI app using uvicorn with port retry logic
    ports = [port]
    if port == 80:
        ports += list(range(8020, 8040))  # 8020-8039 inclusive

    success = False
    for current_port in ports:
        if is_port_in_use(current_port, host):
            logger.warning(f"🚫 [yellow]Port {current_port} ist bereits belegt.[/yellow] 🔄 Versuche nächsten Port...")
            continue

        try:
            # Update config with current port
            config.PORT = current_port
            
            # Beautiful startup message for students
            logger.info(
                f"🚀 [bright_green]EduBotics startet erfolgreich![/bright_green]\n"
                f"🌐 [cyan]Zugriff über:[/cyan] [bright_blue]http://{get_local_ip()}:{current_port}[/bright_blue]\n"
                f"📚 [yellow]Lernmodus:[/yellow] [magenta]{'Nur Simulation' if only_simulation else 'Hardware + Simulation'}[/magenta]\n"
                f"🎓 [green]Viel Spaß beim Lernen mit Robotik![/green]"
            )

            uvicorn.run(
                "phosphobot.app:app",
                host=host,
                port=current_port,
                reload=reload,
                timeout_graceful_shutdown=1,
            )
            success = True
            break
        except OSError as e:
            if "address already in use" in str(e).lower():
                logger.warning(f"⚠️ [yellow]Port-Konflikt auf {current_port}:[/yellow] [red]{e}[/red]")
                continue
            logger.error(f"🔴 [red]Kritischer Server-Fehler:[/red] [bright_red]{e}[/bright_red]")
            raise typer.Exit(code=1)
        except KeyboardInterrupt:
            logger.debug("👋 [green]EduBotics wurde vom Benutzer gestoppt.[/green] [cyan]Auf Wiedersehen![/cyan]")
            raise typer.Exit(code=0)
        except CancelledError:
            logger.debug("✅ [green]EduBotics wurde sauber beendet.[/green] [cyan]Bis zum nächsten Mal![/cyan]")
            raise typer.Exit(code=0)
        # Log the full traceback for unexpected errors
        # except Exception as e:
        #     logger.error(f"Unexpected error: {e}")
        #     raise typer.Exit(code=1)

    if not success:
        logger.warning(
            "🔴 [red]Alle Ports fehlgeschlagen![/red]\n\n"
            "💡 [bright_cyan]Lösungsvorschläge:[/bright_cyan]\n"
            "• Verwende einen anderen Port: [green]edubotics run --port 8000[/green]\n"
            "• Prüfe belegte Ports: [yellow]sudo lsof -i :80[/yellow]\n"
            "• Starte im Simulation-Modus: [cyan]edubotics run --only-simulation[/cyan]\n\n"
            "📞 [yellow]Benötigst du Hilfe? Verwende [green]edubotics --help[/green][/yellow]"
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    cli()
