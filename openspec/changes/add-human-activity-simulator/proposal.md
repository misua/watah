# Change: Human Activity Simulator CLI with Advanced Anti-Detection

## Why
Need a background Python CLI tool that simulates realistic human computer activity to evade monitoring software like Insightful. The tool must use advanced anti-detection techniques including kernel-level input injection, behavioral pattern modeling, and statistical fingerprint avoidance to remain undetectable by monitoring systems.

## What Changes
- New Python CLI application with background daemon capability
- **Kernel-level input injection** using evdev/uinput (bypasses X11 hooks)
- **Multi-layered timing randomization** (Gaussian + Poisson + Markov chains + micro-jitter)
- **Behavioral pattern modeling** (work sessions, breaks, circadian rhythms)
- **Activity correlation** (realistic action sequences)
- **Entropy injection** for all parameters (Bezier curves, varied timing)
- **Statistical fingerprint avoidance** (no perfect intervals, no patterns)
- **Monitoring software detection** and adaptive behavior
- VSCode integration for tab switching and scrolling
- Mouse movement and keyboard activity simulation
- Configurable activity patterns and intensity levels
- Safe operation that doesn't interfere with actual user work

## Impact
- Affected specs: `activity-simulator` (new capability)
- Affected code: New Python package with CLI entry point, advanced evasion modules
- External dependencies: `pywin32`, `pynput`, `numpy`, `scipy`, `PyYAML`, `click`
- Platform: Windows-specific (uses Win32 API via ctypes)
