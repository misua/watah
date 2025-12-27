# Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Python
If you don't have Python installed:
1. Download Python 3.8+ from https://www.python.org/downloads/
2. **Important**: Check "Add Python to PATH" during installation

### Step 2: Install Activity Simulator
Open Command Prompt in the `activity_simulator` folder and run:

```cmd
install.bat
```

Or manually:
```cmd
pip install -e .
```

## First Run (2 minutes)

### 1. Initialize Configuration
```cmd
activity-sim init-config
```

### 2. Test It Works
```cmd
activity-sim test
```

You should see your mouse move and scroll.

### 3. Start the Simulator
```cmd
activity-sim start
```

Press `Ctrl+C` to stop.

## Running in Background

### Option A: Use the batch file
Double-click `start.bat` to run in background.

### Option B: Command line
```cmd
pythonw -m activity_simulator.cli start
```

### Check if it's running
```cmd
activity-sim status
```

### Stop it
```cmd
activity-sim stop
```

## Configuration

Edit `%USERPROFILE%\.activity_sim\config.yaml` to customize:

- **Timing**: Adjust `intensity` (low/medium/high) and `base_interval`
- **Activities**: Enable/disable specific activities and adjust weights
- **Safety**: Configure pause behavior and safe zones

## Auto-Start on Windows Login

### Method 1: Startup Folder
1. Press `Win+R`, type `shell:startup`, press Enter
2. Create shortcut to `start.bat`

### Method 2: Task Scheduler
1. Open Task Scheduler
2. Create Basic Task → "Activity Simulator"
3. Trigger: "At log on"
4. Action: Start `pythonw.exe` with arguments `-m activity_simulator.cli start`

## Troubleshooting

### Mouse not moving?
- Run Command Prompt as Administrator
- Check antivirus isn't blocking it
- Try `activity-sim test` to diagnose

### "Python not found"?
- Reinstall Python with "Add to PATH" checked
- Or use full path: `C:\Python3X\python.exe`

### Still being detected?
1. Edit config: increase `base_interval` to 240-300
2. Set `intensity: low`
3. Enable `adaptive_behavior: true`
4. Check logs: `type %USERPROFILE%\.activity_sim\activity_sim.log`

## What It Does

The simulator performs random human-like activities:
- Mouse movements (smooth Bezier curves)
- Scrolling (up/down with random amounts)
- Tab switching (Ctrl+Tab)
- Keyboard navigation (arrow keys, Page Up/Down)
- Typing random text
- Composite workflows (file editing, browsing)

**Safety features**:
- Automatically pauses when you use your mouse/keyboard
- Resumes after 30 seconds of inactivity (configurable)
- All activities logged for debugging

## Commands Cheat Sheet

```cmd
activity-sim start          # Start simulator
activity-sim stop           # Stop simulator
activity-sim status         # Check if running
activity-sim restart        # Restart simulator
activity-sim test           # Test input injection
activity-sim init-config    # Create config file
activity-sim --help         # Show all commands
```

## Next Steps

1. **Customize timing**: Edit config to adjust activity frequency
2. **Review logs**: Check `%USERPROFILE%\.activity_sim\activity_sim.log`
3. **Monitor detection**: Logs will show if monitoring software is detected
4. **Adjust weights**: Change which activities happen more often

## Important Notes

- The simulator uses **low-level Windows API** to inject input
- It **detects monitoring software** and adapts behavior
- It **pauses automatically** when you use your computer
- All timing is **randomized** to avoid detection patterns
- Activities follow **realistic human behavioral patterns**

Enjoy your automated activity simulation! 🎯
