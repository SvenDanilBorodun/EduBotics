# 🚀 EduBotics Binary Build Guide

This guide explains how to create a new executable binary after making changes to the frontend and backend code.

## 📋 Prerequisites

- **Python 3.10+** with `uv` package manager
- **Node.js and npm** for frontend builds
- **Windows environment** (for .exe builds)
- All project dependencies installed

## 🔄 Complete Build Process

### 1. 🎨 Frontend Changes (if any)

If you made changes to the dashboard frontend:

```bash
# Navigate to the dashboard directory
cd dashboard

# Install dependencies (if not already done)
npm install

# Build the frontend
npm run build

# Copy the built frontend to the backend resources
# The build output should go to phosphobot/resources/dist
cp -r dist/* ../phosphobot/resources/dist/
```

### 2. 🔧 Backend Environment Setup

```bash
# Navigate to the phosphobot directory
cd phosphobot

# Ensure Python dependencies are up to date
uv sync --python 3.10

# Activate the virtual environment (if needed)
# uv venv will create .venv automatically
```

### 3. 🏗️ Build the Binary

#### Option A: Using the Comprehensive Spec File (Recommended)

```bash
# Navigate to the phosphobot directory
cd phosphobot

# Build using the optimized spec file
uv run pyinstaller edubotics.spec --clean
```

#### Option B: Using Direct PyInstaller Command

```bash
# Navigate to the phosphobot directory
cd phosphobot

# Get wasmtime path for data inclusion
python -c "import wasmtime; import os; print(os.path.dirname(wasmtime.__file__))"

# Build with comprehensive options (replace <wasmtime_path> with actual path)
uv run pyinstaller --onefile \
  --name edubotics \
  --add-data "resources;resources" \
  --add-data "<wasmtime_path>;wasmtime" \
  --additional-hooks-dir "./hooks" \
  --hidden-import phosphobot \
  --collect-all phosphobot \
  --collect-all wasmtime \
  --collect-all fastapi \
  --collect-all uvicorn \
  --collect-all pydantic \
  --collect-all numpy \
  --collect-all scipy \
  --collect-all cv2 \
  --collect-all pybullet \
  --collect-all matplotlib \
  --collect-all pandas \
  --collect-all serial \
  --collect-all dynamixel_sdk \
  --collect-all pyrealsense2 \
  --collect-all go2_webrtc_driver \
  --collect-all websockets \
  --collect-all httpx \
  --collect-all cryptography \
  --collect-all pygments \
  --clean \
  -c phosphobot/main.py
```

### 4. 📁 File Locations

After the build completes:

- **Spec file**: `phosphobot/edubotics.spec`
- **Build directory**: `phosphobot/build/edubotics/`
- **Distribution directory**: `phosphobot/dist/`
- **Final binary**: `dist/edubotics.exe`

### 5. 🚀 Move Binary to Project Root

```bash
# Move the binary to the project root for easy access
cd ..  # Back to EduBotics root directory
cp phosphobot/dist/edubotics.exe ./edubotics.exe
```

## ✅ Testing the Binary

### Basic Functionality Test

```bash
# Test version command
./edubotics.exe --version

# Test help command
./edubotics.exe --help

# Test run command help
./edubotics.exe run --help
```

### Full Server Test

```bash
# Start the server in simulation mode (for testing)
./edubotics.exe run --simulation --port 8080

# Open browser to http://localhost:8080 to verify dashboard works
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Missing Dependencies
```bash
# Error: Module not found during runtime
# Solution: Add missing modules to the spec file hidden imports
```

#### 2. Data Files Missing
```bash
# Error: Data files not found
# Solution: Ensure all data directories are included in the spec file
```

#### 3. Large Binary Size
```bash
# The binary may be 300MB+ due to comprehensive dependencies
# This is normal for a complete robotics platform
```

#### 4. Build Errors
```bash
# Clean previous builds
uv run pyinstaller edubotics.spec --clean

# Check the warn-edubotics.txt file for missing modules
cat build/edubotics/warn-edubotics.txt
```

## 📊 Build Statistics

Expected results for a successful build:

- **Binary size**: ~327MB
- **Data files**: 13,000+ entries
- **Binaries**: 500+ entries  
- **Hidden imports**: 6,000+ modules
- **Build time**: 5-10 minutes

## 🎯 Optimization Tips

### For Development Builds

If you're doing frequent testing and don't need all features:

1. Remove heavy dependencies from the spec file temporarily
2. Use `--debug` flag for better error reporting
3. Consider building without UPX compression for faster builds

### For Production Builds

1. Always use the comprehensive spec file
2. Include all hardware driver dependencies
3. Test thoroughly on target deployment machines
4. Document any specific hardware requirements

## 📝 Spec File Maintenance

The `edubotics.spec` file contains:

- **Core modules**: All essential EduBotics dependencies
- **Data files**: Resources, wasmtime, go2_webrtc_driver, etc.
- **Hidden imports**: 6,000+ modules for complete functionality
- **Smart exclusions**: Only unnecessary modules excluded

When adding new dependencies:

1. Add the module to `core_modules` list
2. Add any specific hidden imports to `essential_imports`
3. Include data files if the module requires them
4. Test the binary thoroughly

## 🚨 Important Notes

- **Always test the binary** after building to ensure all functionality works
- **The spec file is optimized for completeness** - it includes everything needed
- **Build on the target OS** - Windows builds require Windows environment
- **Keep the original spec file** as a backup before making changes
- **Document any custom modifications** for future reference

## 📞 Support

If you encounter issues:

1. Check the build logs in `build/edubotics/`
2. Review the warnings in `warn-edubotics.txt`
3. Verify all dependencies are installed correctly
4. Test the source code works before building the binary

---

*This binary includes the complete EduBotics/PhosphoBot robotics platform with all hardware drivers, AI capabilities, and web dashboard functionality.*