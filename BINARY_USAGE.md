# EduBotics Binary Executable Usage

## Overview

This document describes how to use the `edubotics.exe` binary executable that has been created from the EduBotics/phosphobot project. This single executable file contains all the necessary components to run the phosphobot robotics platform.

## Features

The `edubotics.exe` binary includes:
- Complete phosphobot server with web dashboard
- All hardware drivers and robot controllers
- Simulation capabilities (PyBullet integration)
- Camera and sensor support
- AI/ML model integration
- Web interface for robot control and dataset recording

## Basic Usage

### Get Version Information
```bash
./edubotics.exe --version
```

### Run the Server
```bash
./edubotics.exe run
```

This starts the phosphobot server with default settings:
- Host: 0.0.0.0 (all interfaces)
- Port: 80 (with fallback to 8020-8039 if port 80 is unavailable)
- Simulation: headless mode
- Web dashboard accessible at: http://localhost:80

### Custom Configuration
```bash
./edubotics.exe run --host=127.0.0.1 --port=8080 --simulation=headless --no-telemetry
```

## Command Line Options

### Global Options
- `--version, -v`: Show version information and exit
- `--help`: Show help message

### Run Command Options
- `--host`: Host to bind to (default: 0.0.0.0)
- `--port`: Port to bind to (default: 80)
- `--simulation`: Simulation mode - 'headless' or 'gui' (default: headless)
- `--only-simulation`: Only run simulation (default: false)
- `--simulate-cameras`: Simulate cameras (default: false)
- `--realsense`: Enable RealSense camera (default: true)
- `--can`: Enable CAN scanning (default: true)
- `--cameras`: Enable cameras (default: true)
- `--max-opencv-index`: Maximum OpenCV camera index to search (default: 10)
- `--reload`: Reload server on file changes - for development (default: false)
- `--profile`: Enable performance profiling (default: false)
- `--crash-telemetry`: Enable crash reporting (default: true)
- `--usage-telemetry`: Enable usage analytics (default: true)
- `--telemetry`: Enable all telemetry (default: true)

### Info Command
```bash
./edubotics.exe info
```

Shows system information including:
- Available serial ports
- Camera information
- Hardware status

Options:
- `--opencv`: Show OpenCV build information
- `--servos`: Show servo diagnostics information

## Examples

### Basic Robot Control
```bash
# Start with default settings for robot control
./edubotics.exe run

# Access the web dashboard at http://localhost:80
```

### Development Mode
```bash
# Start with local development settings
./edubotics.exe run --host=127.0.0.1 --port=8080 --no-telemetry
```

### Simulation Only
```bash
# Run simulation only with GUI
./edubotics.exe run --only-simulation --simulation=gui --simulate-cameras
```

### Hardware Diagnostics
```bash
# Check hardware status
./edubotics.exe info --opencv --servos
```

## Web Dashboard

Once the server is running, you can access the web dashboard at:
- Default: http://localhost:80
- Custom: http://localhost:[PORT] (where [PORT] is your specified port)

The dashboard provides:
- Robot control interface
- Dataset recording capabilities
- AI model training and inference
- Camera feeds and sensor data
- System monitoring and diagnostics

## File Structure

The binary executable is self-contained and includes:
- All Python dependencies
- Frontend web assets
- Resource files and configurations
- Hardware drivers and libraries

## Requirements

- Windows 10/11 (x64)
- No additional Python installation required
- Hardware-specific drivers may be needed for certain robots/cameras

## Troubleshooting

### Port Issues
If port 80 is unavailable, the server will automatically try ports 8020-8039.

### Hardware Access
Some hardware features may require administrator privileges or specific drivers.

### Simulation Mode
Use `--simulation=headless` for server deployment or `--simulation=gui` for development with visual feedback.

## Original Project

This binary was built from the EduBotics project (phosphobot):
- GitHub: https://github.com/phospho-app/phosphobot
- Documentation: https://docs.phospho.ai
- Support: contact@phospho.ai

## License

MIT License - See the original project for full license details.