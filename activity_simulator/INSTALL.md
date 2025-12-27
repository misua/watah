# Installation Guide for Windows

## Prerequisites

1. **Python 3.8 or later**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Administrator privileges** (for some operations)

## Installation Steps

### Method 1: Install from source (Recommended)

1. Open Command Prompt or PowerShell

2. Navigate to the activity_simulator directory:
   ```cmd
   cd path\to\activity_simulator
   ```

3. Install the package:
   ```cmd
   pip install -e .
   ```

4. Verify installation:
   ```cmd
   activity-sim --help
   ```

### Method 2: Install dependencies only

1. Navigate to the activity_simulator directory:
   ```cmd
   cd path\to\activity_simulator
   ```

2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

3. Run directly:
   ```cmd
   python -m activity_simulator.cli --help
   ```

## Post-Installation Setup

### 1. Initialize Configuration

```cmd
activity-sim init-config
```

This creates a configuration file at `%USERPROFILE%\.activity_sim\config.yaml`

### 2. Test Input Injection

```cmd
activity-sim test
```

You should see the mouse move and scroll. If this works, the installation is successful.

### 3. Start the Simulator

```cmd
activity-sim start
```

Press `Ctrl+C` to stop.

## Running in Background

### Option 1: Using pythonw.exe

```cmd
pythonw -m activity_simulator.cli start
```

This runs without a console window.

### Option 2: Windows Task Scheduler (Auto-start on login)

1. Open Task Scheduler (`taskschd.msc`)

2. Click "Create Basic Task"

3. Configure:
   - **Name**: Activity Simulator
   - **Trigger**: When I log on
   - **Action**: Start a program
   - **Program**: `pythonw.exe`
   - **Arguments**: `-m activity_simulator.cli start`
   - **Start in**: `C:\Python3X\Scripts` (your Python Scripts directory)

4. Check "Run with highest privileges" if needed

5. Click Finish

### Option 3: Create a Startup Shortcut

1. Press `Win+R` and type `shell:startup`

2. Create a new shortcut:
   - **Target**: `pythonw.exe -m activity_simulator.cli start`
   - **Start in**: Your Python Scripts directory

3. Name it "Activity Simulator"

## Troubleshooting

### Issue: "pip is not recognized"

**Solution**: Add Python to PATH or use full path:
```cmd
C:\Python3X\Scripts\pip.exe install -e .
```

### Issue: "Access Denied" errors

**Solution**: Run Command Prompt as Administrator

### Issue: pywin32 installation fails

**Solution**: Install manually:
```cmd
pip install pywin32
python C:\Python3X\Scripts\pywin32_postinstall.py -install
```

### Issue: Input injection not working

**Solutions**:
1. Run as Administrator
2. Check antivirus settings (may block input injection)
3. Verify Python has necessary permissions
4. Test with `activity-sim test`

### Issue: "Module not found" errors

**Solution**: Reinstall dependencies:
```cmd
pip install --force-reinstall -r requirements.txt
```

### Issue: Monitoring software still detecting

**Solutions**:
1. Enable adaptive mode in config
2. Increase timing intervals
3. Reduce activity frequency
4. Check logs: `type %USERPROFILE%\.activity_sim\activity_sim.log`

## Uninstallation

```cmd
pip uninstall activity-simulator
```

Remove configuration directory:
```cmd
rmdir /s %USERPROFILE%\.activity_sim
```

## Verification

After installation, verify everything works:

```cmd
# Check version
activity-sim --help

# Test input
activity-sim test

# Check status
activity-sim status

# Start simulator
activity-sim start
```

## Next Steps

1. Review and customize `%USERPROFILE%\.activity_sim\config.yaml`
2. Adjust activity weights and timing
3. Configure safety settings
4. Set up auto-start if desired

## Support

For issues or questions, check the logs:
```cmd
type %USERPROFILE%\.activity_sim\activity_sim.log
```
