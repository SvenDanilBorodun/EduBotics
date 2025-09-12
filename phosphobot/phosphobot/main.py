from loguru import logger

logger.info("Starting phosphobot...")

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


def print_phospho_splash() -> None:
    global _splash_shown
    if not _splash_shown:
        print(
            f"""[bright_blue]
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║    ███████ ██████  ██    ██ ██████   ██████  ████████ ██  ██████ ███████ ║
    ║    ██      ██   ██ ██    ██ ██   ██ ██    ██    ██    ██ ██      ██      ║
    ║    █████   ██   ██ ██    ██ ██████  ██    ██    ██    ██ ██      ███████ ║
    ║    ██      ██   ██ ██    ██ ██   ██ ██    ██    ██    ██ ██           ██ ║
    ║    ███████ ██████   ██████  ██████   ██████     ██    ██  ██████ ███████ ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
            [bold bright_green]🤖 EDUBOTICS v{__version__} 🤖[/bold bright_green]
      [dim]Robotik-Lernplattform für Schüler und Studenten[/dim]
            [yellow]📚 Mehr Infos: https://edubotics.de[/yellow]
            [/bright_blue]"""
        )
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
            if platform.system() == "Darwin":
                logger.warning(
                    f"🚀 EduBotics {version} verfügbar! Update mit: \nbrew update && brew upgrade edubotics"
                )
            elif platform.system() == "Linux":
                logger.warning(
                    f"🚀 EduBotics {version} verfügbar! Update mit: \nsudo apt update && sudo apt upgrade edubotics"
                )
            else:
                logger.warning(
                    f"🚀 EduBotics {version} verfügbar! Info: https://edubotics.de/installation"
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
    This is used for automatic crash reporting.
    """
    from phosphobot.sentry import init_sentry

    init_sentry()


cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


def version_callback(value: bool) -> None:
    if value:
        from rich import print
        print(f"[bold bright_blue]🤖 EduBotics Robotik-Plattform[/bold bright_blue] [bright_green]v{__version__}[/bright_green]")
        print("[dim]Bildungssoftware für Robotik und KI - Für deutsche Schüler entwickelt[/dim]")
        raise typer.Exit()


@cli.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="🔖 Zeige die Programmversion an und beende das Programm.",
            callback=version_callback,
        ),
    ] = False,
) -> None:
    """
    🤖 [bold bright_blue]EduBotics[/bold bright_blue] - Robotik-Lernplattform für deutsche Schüler
    
    [dim]Eine benutzerfreundliche Software zum Lernen von Robotik und KI.
    Steuere Roboter, sammle Daten und lerne durch praktische Erfahrungen![/dim]
    """
    pass


@cli.command()
def info(
    opencv: Annotated[bool, typer.Option(help="🎥 Zeige OpenCV-Kamera-Informationen an.")] = False,
    servos: Annotated[bool, typer.Option(help="🔧 Zeige Servo-Motor-Informationen an.")] = False,
) -> typer.Exit:
    """
    🔍 [bold bright_cyan]Hardware-Diagnose[/bold bright_cyan]
    
    [dim]Zeigt alle verfügbaren Schnittstellen (z.B. /dev/ttyUSB0) und 
    Kamera-Informationen an. Nützlich für die Fehlerbehebung.[/dim]
    """
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports()
    pid_list = [port.pid for port in ports]
    serial_numbers = [port.serial_number for port in ports]

    from rich import print
    print("\n" + "=" * 60)
    print("[bold bright_green]🔍 EduBotics Hardware-Diagnose[/bold bright_green]")
    print("=" * 60)
    
    print(f"[bright_cyan]🔌 Serielle Schnittstellen:[/bright_cyan] [yellow]{', '.join([port.device for port in ports]) if ports else 'Keine gefunden'}[/yellow]")
    print(f"[bright_cyan]🏷️  Seriennummern:[/bright_cyan] [yellow]{', '.join([str(sn) for sn in serial_numbers]) if serial_numbers else 'Keine verfügbar'}[/yellow]")
    print(f"[bright_cyan]🆔 Hardware-PIDs:[/bright_cyan] [yellow]{', '.join([str(pid) for pid in pid_list]) if pid_list else 'Keine gefunden'}[/yellow]")
    print("=" * 60)

    import cv2

    from phosphobot.camera import get_all_cameras

    cameras = get_all_cameras()
    time.sleep(0.5)
    cameras_status = cameras.status().model_dump_json(indent=4)
    cameras.stop()
    
    print(f"[bright_cyan]📷 Kamera-Status:[/bright_cyan]")
    print(f"[dim]{cameras_status}[/dim]")
    print("=" * 60)

    if opencv:
        print(f"[bright_cyan]🎥 OpenCV Build-Informationen:[/bright_cyan]")
        print(f"[dim]{cv2.getBuildInformation()}[/dim]")
        print("=" * 60)

    if servos:
        print(f"[bright_cyan]🔧 Servo-Diagnose:[/bright_cyan]")
        from phosphobot.hardware.motors.feetech import (  # type: ignore
            dump_servo_states_to_file,
        )
        from phosphobot.utils import get_home_app_path

        # Diagnose SO-100 servos
        servo_count = 0
        for port in ports:
            if port.pid == 21971:
                dump_servo_states_to_file(
                    str(get_home_app_path() / f"servo_states_{port.device}.csv"),
                    port.device,
                )
                servo_count += 1
        print(f"[yellow]✅ {servo_count} SO-100 Servos analysiert und in CSV-Datei gespeichert[/yellow]")
        print("=" * 60)
    
    print(f"[dim bright_blue]💡 Diagnose abgeschlossen! Nutze diese Infos für die Fehlerbehebung.[/dim bright_blue]")
    print("=" * 60 + "\n")
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
    📦 [bold bright_green]Software-Update[/bold bright_green]
    
    [dim]Zeigt Informationen an, wie du EduBotics auf die neueste Version aktualisieren kannst.[/dim]
    """
    from rich import print
    print("\n" + "=" * 50)
    print("[bold bright_green]📦 EduBotics Update-Anleitung[/bold bright_green]")
    print("=" * 50)
    
    if platform.system() == "Darwin":
        print("[bright_cyan]🍎 macOS Update:[/bright_cyan]")
        print("[yellow]brew update && brew upgrade edubotics[/yellow]")
    elif platform.system() == "Linux":
        print("[bright_cyan]🐧 Linux Update:[/bright_cyan]")
        print("[yellow]sudo apt update && sudo apt upgrade edubotics[/yellow]")
    else:
        print("[bright_cyan]🪟 Windows Update:[/bright_cyan]")
        print("[yellow]📚 Besuche: https://edubotics.de/installation[/yellow]")
    
    print("=" * 50)
    print("[dim bright_blue]💡 Nach dem Update starte EduBotics neu![/dim bright_blue]")
    print("=" * 50 + "\n")


@cli.command()
def run(
    chat: Annotated[bool, typer.Option(help="💬 Starte EduBotics im Chat-Modus.")] = False,
    host: Annotated[str, typer.Option(help="🌐 Server-Adresse (Standard: 0.0.0.0 für alle Geräte)")] = "0.0.0.0",
    port: Annotated[int, typer.Option(help="🔌 Port-Nummer für den Server")] = 80,
    simulation: Annotated[
        SimulationMode,
        typer.Option(
            help="🎮 Simulation im Hintergrund (headless) oder mit grafischer Oberfläche (gui)",
        ),
    ] = SimulationMode.headless,
    only_simulation: Annotated[
        bool, typer.Option(help="🖥️ Nur Simulation starten, keine echte Hardware")
    ] = False,
    simulate_cameras: Annotated[
        bool,
        typer.Option(help="📹 Simuliere virtuelle Kameras für Tests"),
    ] = False,
    realsense: Annotated[
        bool,
        typer.Option(help="🎥 Intel RealSense Kamera aktivieren"),
    ] = True,
    can: Annotated[
        bool,
        typer.Option(
            help="🔌 CAN-Bus Geräte suchen und aktivieren",
        ),
    ] = True,
    cameras: Annotated[
        bool,
        typer.Option(
            help="📷 Kamera-Erkennung aktivieren",
        ),
    ] = True,
    max_can_interfaces: Annotated[
        int,
        typer.Option(
            help="🔢 Maximale Anzahl erwarteter CAN-Schnittstellen",
        ),
    ] = 4,
    max_opencv_index: Annotated[
        int,
        typer.Option(
            help="🔍 Maximaler OpenCV Index für Kamera-Suche",
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
        typer.Option(help="📈 Absturzberichte deaktivieren"),
    ] = True,
    usage_telemetry: Annotated[
        bool,
        typer.Option(help="📊 Nutzungsstatistiken deaktivieren"),
    ] = True,
    telemetry: Annotated[
        bool,
        typer.Option(help="🚫 Alle Telemetrie-Daten deaktivieren"),
    ] = True,
) -> None:
    """
    🚀 [bold bright_green]EduBotics Dashboard und Server starten[/bold bright_green]
    
    [dim]Startet die EduBotics-Plattform zum Steuern deines Roboters,
    Sammeln von Daten und Lernen von Robotik-Konzepten![/dim]
    """
    from phosphobot.app import start_server

    if not chat:
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