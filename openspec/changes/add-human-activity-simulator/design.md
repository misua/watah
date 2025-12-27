# Design: Human Activity Simulator

## Context
Creating a background Python CLI tool that simulates human-like computer activity to evade monitoring software like Insightful on Windows. The tool needs to run as a background service, perform realistic actions (mouse movement, scrolling, tab switching), use advanced anti-detection techniques, and avoid interfering with actual user work. Monitoring software typically tracks mouse/keyboard events, application usage, window focus changes, and idle time patterns through Windows API hooks.

## Goals / Non-Goals

### Goals
- Simulate realistic human activity patterns with natural timing
- Evade detection by monitoring software through advanced anti-detection techniques
- Run safely in background without disrupting user work
- Provide configurable activity intensity and patterns
- Support VSCode-specific interactions (tab switching, scrolling)
- Easy CLI interface for start/stop/status operations
- Mimic genuine human behavioral patterns (typing bursts, reading pauses, context switches)

### Non-Goals
- Not a full automation framework (only simulates idle-prevention activity)
- Not cross-platform initially (focus on Windows first)
- Not a screen recording or monitoring tool
- Not designed for gaming or application-specific automation

## Decisions

### Decision: Use low-level Windows input injection with SendInput API
**Rationale**: 
- Windows `SendInput` API with `HARDWAREINPUT` flag simulates hardware-level input events
- Monitoring software typically hooks `SendMessage`/`PostMessage` but `SendInput` with hardware flags bypasses these
- Use `ctypes` to call Win32 API directly for maximum control
- `pynput` for monitoring actual user input to pause simulation

**Alternatives considered**:
- `pyautogui` (easily detected, uses high-level Windows messaging that monitoring software hooks)
- `pydirectinput` (still detectable by API hooks)
- `keyboard` + `mouse` libraries (high-level, easily fingerprinted by monitoring software)

### Decision: Windows background service with pythonw
**Rationale**:
- Use `pythonw.exe` to run without console window
- Windows Task Scheduler for auto-start capability
- PID file management for process control
- Clean start/stop/status workflow via CLI

**Alternatives considered**:
- Windows Service (requires admin privileges, complex setup)
- Simple background process with `START /B` (less robust, harder to manage)

### Decision: Multi-layered timing randomization with behavioral patterns
**Rationale**:
- Combine multiple randomization techniques: Gaussian distribution, Poisson process, and Markov chains
- Model actual human work patterns: focused work sessions, break periods, context switching
- Add "micro-jitter" to all timing (±50-200ms) to avoid perfect intervals
- Implement circadian rhythm simulation (activity patterns change throughout day)
- Use different timing profiles for different activity types (reading vs typing vs navigating)

### Decision: Activity pause on user input detection
**Rationale**:
- Safety-first approach prevents interference with actual work
- Uses `pynput` listeners to detect keyboard/mouse events
- Resumes after configurable idle period (default 5 seconds)

### Decision: YAML configuration files
**Rationale**:
- Human-readable and easy to edit
- Supports complex nested structures for activity patterns
- Standard format with good Python library support (PyYAML)

## Architecture

### Components

```
activity-simulator/
├── cli.py              # CLI entry point (click-based)
├── daemon.py           # Daemon process manager
├── scheduler.py        # Activity scheduling and timing
├── behavioral/
│   ├── patterns.py     # Human behavior pattern models
│   ├── timing.py       # Multi-layered timing randomization
│   └── markov.py       # Markov chain state transitions
├── activities/
│   ├── mouse.py        # Mouse movement with Bezier curves
│   ├── keyboard.py     # Keyboard activity simulation
│   ├── vscode.py       # VSCode-specific actions
│   ├── scroll.py       # Scrolling simulation
│   └── composite.py    # Composite activities (correlated actions)
├── input/
│   ├── evdev_inject.py # Kernel-level input injection (evdev/uinput)
│   ├── device.py       # Virtual device management
│   └── monitor.py      # User input detection (pynput)
├── evasion/
│   ├── fingerprint.py  # Anti-fingerprinting techniques
│   ├── entropy.py      # Entropy injection for parameters
│   └── detector.py     # Monitoring software detection
├── safety.py           # User input detection and pause logic
├── config.py           # Configuration management
└── utils.py            # Helper functions
```

### Activity Flow

1. User starts daemon via CLI
2. Daemon loads configuration and initializes activity modules
3. Scheduler generates next activity based on weights and timing
4. Safety module checks for user input
5. If safe, execute activity with randomized parameters
6. Wait for next scheduled interval (Gaussian-distributed)
7. Repeat until stopped

## Risks / Trade-offs

### Risk: Accidental interference with user work
**Mitigation**: 
- Implement robust user input detection
- Add configurable pause duration
- Provide emergency stop hotkey (Ctrl+Alt+Q)
- Log all activities for debugging

### Risk: Detection by monitoring software
**Mitigation**:
- Use kernel-level input injection (evdev/uinput) instead of X11/high-level APIs
- Multi-layered timing randomization (Gaussian + Poisson + Markov chains + micro-jitter)
- Behavioral pattern modeling (work sessions, breaks, circadian rhythms)
- Activity correlation (mouse movement before clicks, scrolling before reading)
- Entropy injection (vary all parameters: speed, acceleration, path curvature)
- Application context awareness (simulate realistic app usage patterns)
- Statistical fingerprint avoidance (no perfect intervals, no repeated sequences)

### Risk: Resource consumption
**Mitigation**:
- Lightweight activity implementations
- Configurable activity frequency
- Monitor CPU/memory usage in daemon
- Graceful degradation if system is busy

### Risk: VSCode-specific actions may fail
**Mitigation**:
- Detect if VSCode is running before VSCode-specific actions
- Fallback to generic activities if VSCode not available
- Configurable application detection

## Configuration Schema

```yaml
activity_simulator:
  intensity: medium  # low, medium, high
  active_hours:
    start: "09:00"
    end: "17:00"
  
  timing:
    mean_interval: 120  # seconds
    std_deviation: 30
    pause_on_input: 5   # seconds
  
  activities:
    mouse_movement:
      enabled: true
      weight: 0.3
      max_distance: 200  # pixels
    
    vscode_tab_switch:
      enabled: true
      weight: 0.3
      detect_vscode: true
    
    scrolling:
      enabled: true
      weight: 0.2
      scroll_amount: [1, 5]  # range
    
    keyboard_activity:
      enabled: true
      weight: 0.2
      safe_keys: ["ctrl+tab", "alt+tab"]
  
  safety:
    emergency_stop_hotkey: "ctrl+alt+q"
    pause_on_user_input: true
    activity_boundaries:
      enabled: true
      safe_zone: "current_screen"
```

## Migration Plan

N/A - This is a new capability with no existing system to migrate from.

## Anti-Detection Techniques

### 1. Low-Level Windows Input Injection
- Use Windows `SendInput` API with `HARDWAREINPUT` flag via `ctypes`
- Inject events at hardware simulation level, bypassing high-level message hooks
- Monitoring software hooking `SendMessage`/`PostMessage` won't intercept these events
- Direct Win32 API calls avoid detection by Python automation library fingerprinting

### 2. Behavioral Pattern Modeling
- **Work Sessions**: Simulate focused work periods (20-50 min) with high activity
- **Break Periods**: Reduce activity during breaks (5-15 min)
- **Circadian Rhythm**: Adjust activity patterns based on time of day
- **Context Switching**: Model realistic transitions between tasks
- **Reading Pauses**: Simulate periods of no input (reading, thinking)

### 3. Activity Correlation
- Mouse movement before clicks (humans don't teleport cursor)
- Scrolling followed by reading pauses
- Tab switches preceded by mouse movement to tab area
- Typing bursts with natural pauses (thinking, reading)
- Application focus changes with corresponding mouse/keyboard activity

### 4. Entropy Injection
- **Mouse Movement**: Vary speed, acceleration, path curvature using Bezier curves
- **Timing**: Add micro-jitter (±50-200ms) to all intervals
- **Scroll Amount**: Randomize scroll distance and speed
- **Key Timing**: Vary inter-key delays, simulate typing rhythm variations
- **Parameter Ranges**: Never use fixed values, always sample from distributions

### 5. Statistical Fingerprint Avoidance
- No perfect intervals (always add randomness)
- No repeated sequences (track recent activities, avoid patterns)
- No fixed ratios (vary activity type distribution over time)
- Entropy analysis resistance (ensure high entropy in all parameters)
- Frequency analysis resistance (vary activity frequency dynamically)

### 6. Monitoring Software Detection
- Detect common monitoring processes (Insightful, Time Doctor, Hubstaff, ActivTrak)
- Adjust behavior if monitoring detected (more conservative patterns)
- Check for Windows API hooks (SetWindowsHookEx, GetMessage hooks)
- Monitor system load to avoid detection during performance analysis

### 7. Composite Activities
- Combine multiple actions into realistic sequences
- Example: Move mouse → Pause → Click → Pause → Type → Pause
- Simulate realistic workflows (open file → read → edit → save)
- Vary composite patterns to avoid detection

## Open Questions

1. Should we support Windows/macOS initially or focus on Windows?
   - **Decision**: Start with Windows, add cross-platform support later if needed
   
2. How to handle multiple monitors?
   - **Decision**: Default to primary monitor, add multi-monitor support in future iteration
   
3. Should activities be plugin-based for extensibility?
   - **Decision**: Start with built-in activities, consider plugin architecture if users request custom activities
