# Azure Portal Configuration Helper

A Windows utility that assists with Azure portal navigation and resource management tasks.

## Features

- **Safe Clicking**: Only clicks in predefined safe zones (sidebar, content area)
- **Tab Switching**: Switches between browser tabs using Ctrl+Tab
- **Scrolling**: Scrolls up/down to explore content
- **Browser Detection**: Only runs when browser is active
- **No Typing**: Never types anything
- **No Destructive Actions**: Never clicks delete or dangerous buttons

## Installation

This tool uses the existing virtual environment from `activity_simulator`:

```bash
cd /home/hn/Desktop/watah/click

# Activate the existing venv
source ../activity_simulator/venv/bin/activate  # Linux/Mac
# or
..\activity_simulator\venv\Scripts\activate  # Windows

# Install required packages (if not already installed)
pip install numpy pyyaml pywin32
```

## Usage

### Basic Usage

**Quick Start (Windows):**
```bash
# Just double-click start_azure.bat
# Or from command line:
start_azure.bat
```

**Manual Start:**
```bash
# Make sure you're in the click directory
cd /home/hn/Desktop/watah/click

# Activate venv
..\activity_simulator\venv\Scripts\activate

# Run the helper
python azure_setup.py
```

**Stop the Service:**
```bash
# Double-click stop_azure.bat
# Or from command line:
stop_azure.bat
```

### What It Does

The helper will:
1. Check if a browser window is active
2. Randomly select an activity based on weights in `config.yaml`:
   - **Click in content area** (40%): Clicks on resources, links in main area
   - **Click in sidebar** (30%): Clicks on menu items in left sidebar
   - **Switch tab** (20%): Switches between browser tabs
   - **Scroll down** (8%): Scrolls down to see more content
   - **Scroll up** (2%): Scrolls up
3. Wait 5-15 seconds before next activity
4. Repeat

### Configuration

Edit `config.yaml` to customize:

```yaml
timing:
  min_interval: 5    # Minimum seconds between actions
  max_interval: 15   # Maximum seconds between actions

activities:
  click_content:
    weight: 0.40     # 40% chance
  click_sidebar:
    weight: 0.30     # 30% chance
  switch_tab:
    weight: 0.20     # 20% chance
  scroll_down:
    weight: 0.08     # 8% chance
  scroll_up:
    weight: 0.02     # 2% chance
```

### Safe Zones

The simulator only clicks in predefined safe zones:

- **Sidebar**: Left 5-20% of screen, middle 30-80% vertically
  - Good for: Menu items, navigation
- **Content**: Center 25-85% of screen, middle 25-75% vertically
  - Good for: Resources, links, tables
- **Tabs**: Top center 15-70%, top 8-12% vertically
  - Good for: Browser tabs (not currently used for clicking)

These zones avoid:
- Delete buttons
- Destructive actions
- Top/bottom edges
- Right edge (close buttons)

## Stopping the Service

**Using batch file:**
```bash
stop_azure.bat
```

**Manual stop:**
- Press `Ctrl+C` in the console window (if running manually)
- Or use Task Manager to end the `pythonw.exe` process

## Logs

The service logs all activities to `azure_config.log`:

```
2025-12-30 08:30:15 - AzurePortalHelper - INFO - Starting Azure portal configuration service...
2025-12-30 08:30:15 - AzurePortalHelper - INFO - >>> Executing: click_content
2025-12-30 08:30:15 - AzurePortalHelper - INFO - Clicked in content at (650, 420)
2025-12-30 08:30:15 - AzurePortalHelper - INFO - ✓ click_content completed
2025-12-30 08:30:15 - AzurePortalHelper - INFO - Next activity in 8.3 seconds
```

## Use Case: Azure Portal Exploration

Perfect for simulating someone exploring Azure Portal:
- Clicks on SQL servers, databases, resources
- Navigates through menu items
- Switches between tabs
- Scrolls to see more resources
- Never clicks delete or destructive actions

## Requirements

- Windows OS
- Python 3.7+
- Browser (Chrome, Edge, Firefox, etc.)
- Packages: numpy, pyyaml, pywin32

## Safety Features

1. **Browser Detection**: Only runs when browser is active
2. **Safe Zones**: Only clicks in predefined safe areas
3. **No Typing**: Never types anything
4. **No Delete**: Avoids dangerous buttons by design
5. **Smooth Movement**: Mouse moves smoothly like a human

## Troubleshooting

**Simulator not clicking:**
- Make sure browser window is active and in focus
- Check logs for errors
- Verify screen resolution matches expected zones

**Clicking in wrong areas:**
- Adjust zone ranges in `config.yaml`
- Check screen resolution

**Too fast/slow:**
- Adjust `min_interval` and `max_interval` in `config.yaml`

## Architecture

- `azure_setup.py`: Main service logic
- `win32_input.py`: Windows input injection (copied from activity_simulator)
- `config.yaml`: Configuration file
- `start_azure.bat`: Start service in background (hidden)
- `stop_azure.bat`: Stop the service
- Uses existing venv from `activity_simulator`

## Stealth Features

- **Inconspicuous naming**: Files named as "Azure configuration" tools
- **Background execution**: Runs with `pythonw.exe` (no console window)
- **File logging**: Logs to `azure_config.log` instead of console
- **Process name**: Appears as `pythonw.exe` in Task Manager (common Windows process)
- **Hidden operation**: No visible windows when running

## License

Same as activity_simulator (MIT)
