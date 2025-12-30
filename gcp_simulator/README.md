# Activity Simulator

Windows activity simulator with advanced anti-detection capabilities designed to evade monitoring software like Insightful, Time Doctor, Hubstaff, and similar tools.

## Features

- **Low-level Windows input injection** using SendInput API with hardware-level simulation
- **Multi-layered timing randomization** (Gaussian, Poisson, micro-jitter)
- **Behavioral pattern modeling** (work sessions, breaks, circadian rhythms)
- **Monitoring software detection** and adaptive behavior
- **Statistical fingerprint avoidance** (no perfect intervals, no patterns)
- **User input detection** with automatic pause/resume
- **Composite activity workflows** (file editing, browsing, tab switching)
- **Configurable activity types and weights**

## Installation

### Requirements

- Windows 10 or later
- Python 3.8 or later

### Install from source

```bash
cd activity_simulator
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

### Post-installation

After installation, the `activity-sim` command will be available in your terminal.

## Quick Start

### 1. Initialize configuration

```bash
activity-sim init-config
```

This creates a default configuration file at `~/.activity_sim/config.yaml`.

### 2. Test input injection

```bash
activity-sim test
```

This performs a single mouse movement and scroll to verify the input injection is working.

### 3. Start the simulator

```bash
activity-sim start
```

The simulator will run in the foreground. Press `Ctrl+C` to stop.

### 4. Check status

```bash
activity-sim status
```

### 5. Stop the simulator

```bash
activity-sim stop
```

## Configuration

Edit `~/.activity_sim/config.yaml` to customize behavior:

```yaml
daemon:
  pid_file: activity_sim.pid
  log_file: activity_sim.log
  log_level: INFO

timing:
  base_interval: 180  # Base interval in seconds
  intensity: medium   # low, medium, high
  enable_circadian: true

activities:
  mouse_movement:
    enabled: true
    weight: 0.3
  mouse_scroll:
    enabled: true
    weight: 0.25
  keyboard_navigation:
    enabled: true
    weight: 0.15
  keyboard_typing:
    enabled: true
    weight: 0.1
  tab_switching:
    enabled: true
    weight: 0.1
  composite_workflows:
    enabled: true
    weight: 0.1

safety:
  pause_on_user_input: true
  pause_duration: 30  # Seconds of inactivity before resuming
  emergency_stop_hotkey: ctrl+alt+q
  safe_zone: current_screen

anti_detection:
  enable_monitoring_detection: true
  detection_interval: 300  # Check every 5 minutes
  adaptive_behavior: true
  entropy_injection: true
```

## Usage

### Basic Commands

```bash
# Start simulator
activity-sim start

# Stop simulator
activity-sim stop

# Check status
activity-sim status

# Restart simulator
activity-sim restart

# Test input injection
activity-sim test

# Initialize config file
activity-sim init-config

# Use custom config file
activity-sim --config /path/to/config.yaml start
```

### Running in Background

To run the simulator in the background on Windows, use `pythonw.exe`:

```bash
pythonw -m activity_simulator.cli start
```

Or create a Windows Task Scheduler task to run at startup.

### Windows Task Scheduler Setup

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Activity Simulator"
4. Trigger: "At log on"
5. Action: "Start a program"
6. Program: `pythonw.exe`
7. Arguments: `-m activity_simulator.cli start`
8. Working directory: Your Python Scripts directory

## How It Works

### Anti-Detection Techniques

1. **Low-Level Input Injection**: Uses Windows `SendInput` API with hardware-level flags to bypass high-level message hooks that monitoring software typically uses.

2. **Behavioral Pattern Modeling**: Simulates realistic human work patterns including:
   - Work sessions (20-50 minutes)
   - Break periods (5-15 minutes)
   - Circadian rhythm adjustments
   - Context switching between tasks

3. **Multi-Layered Timing Randomization**:
   - Gaussian distribution for base timing
   - Poisson process for jitter
   - Micro-jitter (±50-200ms) to avoid perfect intervals
   - Markov chains for state transitions

4. **Activity Correlation**:
   - Mouse movement before clicks
   - Pauses after actions
   - Realistic composite workflows

5. **Statistical Fingerprint Avoidance**:
   - No perfect intervals
   - No repeated sequences
   - Dynamic activity frequency
   - High entropy in all parameters

6. **Monitoring Software Detection**:
   - Detects known monitoring processes
   - Detects Windows API hooks
   - Adapts behavior when monitoring is detected

### Safety Features

- **Automatic pause on user input**: Detects real mouse/keyboard activity and pauses simulation
- **Configurable pause duration**: Resumes after specified inactivity period
- **Safe zones**: Keeps activity within specified screen boundaries
- **Comprehensive logging**: All activities logged for debugging

## Troubleshooting

### "Access Denied" errors

Run your terminal as Administrator if you encounter permission errors.

### Input not working

1. Test with `activity-sim test`
2. Check if antivirus is blocking the script
3. Verify Python has necessary permissions

### Monitoring software still detecting

1. Enable adaptive mode in config
2. Increase timing randomization
3. Reduce activity frequency
4. Check logs for detection events

## Development

### Project Structure

```
activity_simulator/
├── activity_simulator/
│   ├── __init__.py
│   ├── win32_input.py      # Windows SendInput API wrapper
│   ├── activities.py       # Activity implementations
│   ├── timing.py           # Timing randomization
│   ├── monitoring.py       # Monitoring detection
│   ├── config.py           # Configuration management
│   ├── daemon.py           # Daemon controller
│   └── cli.py              # CLI interface
├── tests/
├── pyproject.toml
├── setup.py
├── requirements.txt
└── README.md
```

### Running Tests

```bash
pytest tests/
```

## Disclaimer

This tool is for educational and research purposes. Use responsibly and in accordance with your organization's policies and local laws. The authors are not responsible for misuse of this software.

## License

MIT License
