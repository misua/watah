# Stealth Mode Operation

## Overview
The stealth mode disguises the activity simulator to avoid detection by monitoring software like Insightful.

## How it works
1. Uses `pythonw.exe` (no console window)
2. Randomizes process window title to common system processes
3. Minimal logging (hidden log file)
4. Background execution

## Usage

### Start (Hidden)
```cmd
start_hidden.bat
```
This starts the simulator in the background with a disguised process name like:
- Adobe Update Service
- Windows Update Assistant
- Microsoft Edge Update
- notepad.exe
- RuntimeBroker.exe

### Stop
```cmd
stop_hidden.bat
```
Kills all related processes and cleans up PID files.

### Check Status
```cmd
status_hidden.bat
```
Shows if the service is running and displays process info.

## Important Notes

1. **Process appears as**: `pythonw.exe` running with a disguised window title
2. **Logs are minimal**: Only errors logged to `syslog.tmp` (auto-deleted on stop)
3. **No console window**: Uses `pythonw.exe` instead of `python.exe`
4. **Config**: Uses `config.yaml` or `config.example.yaml` automatically

## Detection Considerations

While this helps avoid casual detection:
- Process monitoring tools can still see `pythonw.exe` in task list
- Network monitoring might detect patterns
- Deep process inspection can reveal the script path

For maximum stealth, consider:
1. Compiling to a `.exe` with PyInstaller using a system-like name
2. Running with randomized intervals (already implemented)
3. Adjusting activity patterns to match your normal behavior

## Files Created
- `.runtime.pid` - Temporary PID marker (auto-deleted)
- `syslog.tmp` - Minimal error logs (auto-deleted on stop)
- `activity_sim.pid` - Standard PID file (if using)

## Configuration
The stealth runner uses the same `config.yaml` as the standard runner.
All timing, activities, and safety features work the same way.
