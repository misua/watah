## ADDED Requirements

### Requirement: CLI Interface
The system SHALL provide a command-line interface with start, stop, status, and config commands for managing the activity simulator daemon.

#### Scenario: Start daemon successfully
- **WHEN** user runs `activity-simulator start`
- **THEN** daemon process starts in background
- **AND** PID file is created
- **AND** success message is displayed

#### Scenario: Stop daemon successfully
- **WHEN** user runs `activity-simulator stop`
- **AND** daemon is running
- **THEN** daemon process terminates gracefully
- **AND** PID file is removed
- **AND** success message is displayed

#### Scenario: Check daemon status
- **WHEN** user runs `activity-simulator status`
- **THEN** current daemon state is displayed (running/stopped)
- **AND** uptime is shown if running
- **AND** last activity timestamp is shown

#### Scenario: Configure settings
- **WHEN** user runs `activity-simulator config --intensity medium`
- **THEN** configuration file is updated
- **AND** daemon reloads configuration if running

### Requirement: Background Daemon Process
The system SHALL run as a Unix daemon process that detaches from the terminal and operates in the background.

#### Scenario: Daemon initialization
- **WHEN** daemon starts
- **THEN** process detaches from terminal
- **AND** PID file is written to `/var/run/activity-simulator.pid` or `~/.activity-simulator/pid`
- **AND** log file is created
- **AND** signal handlers are registered

#### Scenario: Daemon shutdown
- **WHEN** daemon receives SIGTERM or SIGINT
- **THEN** all activities are stopped gracefully
- **AND** PID file is removed
- **AND** shutdown is logged

### Requirement: Human-Like Activity Simulation
The system SHALL simulate realistic human computer activity with randomized timing and natural patterns.

#### Scenario: Mouse movement simulation
- **WHEN** mouse activity is scheduled
- **THEN** cursor moves along natural curved path
- **AND** movement speed varies realistically
- **AND** movement distance is randomized within configured bounds

#### Scenario: VSCode tab switching
- **WHEN** VSCode tab switch activity is scheduled
- **AND** VSCode is detected as running
- **THEN** keyboard shortcut (Ctrl+Tab or Ctrl+PageDown) is sent
- **AND** action is logged

#### Scenario: Scrolling simulation
- **WHEN** scrolling activity is scheduled
- **THEN** scroll wheel events are generated
- **AND** scroll amount is randomized within configured range
- **AND** scroll direction varies naturally

#### Scenario: Keyboard activity simulation
- **WHEN** keyboard activity is scheduled
- **THEN** safe key combinations are sent (e.g., Ctrl+Tab, Alt+Tab)
- **AND** no text input is generated
- **AND** actions do not interfere with user work

### Requirement: Activity Scheduling
The system SHALL schedule activities using Gaussian-distributed random intervals to mimic human behavior patterns.

#### Scenario: Calculate next activity interval
- **WHEN** previous activity completes
- **THEN** next interval is calculated using Gaussian distribution
- **AND** interval uses configured mean and standard deviation
- **AND** minimum interval of 10 seconds is enforced

#### Scenario: Select activity type
- **WHEN** scheduling next activity
- **THEN** activity type is selected based on configured weights
- **AND** disabled activities are excluded
- **AND** selection is randomized

#### Scenario: Respect active hours
- **WHEN** current time is outside configured active hours
- **THEN** no activities are scheduled
- **AND** daemon waits until next active period

### Requirement: User Input Detection and Safety
The system SHALL detect actual user input and pause all simulated activities to prevent interference with user work.

#### Scenario: Detect user keyboard input
- **WHEN** user presses any key
- **THEN** all scheduled activities are paused immediately
- **AND** pause timer starts
- **AND** pause event is logged

#### Scenario: Detect user mouse input
- **WHEN** user moves mouse or clicks
- **THEN** all scheduled activities are paused immediately
- **AND** pause timer starts

#### Scenario: Resume after idle period
- **WHEN** no user input detected for configured pause duration (default 5 seconds)
- **THEN** activity scheduling resumes
- **AND** next activity is scheduled
- **AND** resume event is logged

#### Scenario: Emergency stop hotkey
- **WHEN** user presses emergency stop hotkey (Ctrl+Alt+Q)
- **THEN** daemon stops immediately
- **AND** all activities cease
- **AND** daemon exits gracefully

### Requirement: Configuration Management
The system SHALL support YAML configuration files for customizing activity patterns, timing, and behavior.

#### Scenario: Load default configuration
- **WHEN** daemon starts without custom config
- **THEN** default configuration is loaded from `~/.activity-simulator/config.yaml`
- **AND** default values are used if file doesn't exist

#### Scenario: Load custom configuration
- **WHEN** user specifies config file with `--config` flag
- **THEN** specified configuration file is loaded
- **AND** configuration is validated
- **AND** errors are reported if invalid

#### Scenario: Reload configuration
- **WHEN** configuration file is modified
- **AND** daemon receives SIGHUP signal
- **THEN** configuration is reloaded
- **AND** new settings take effect for next activities
- **AND** reload event is logged

#### Scenario: Validate configuration
- **WHEN** configuration is loaded
- **THEN** all required fields are present
- **AND** values are within valid ranges
- **AND** activity weights sum to valid total
- **AND** validation errors are reported

### Requirement: Activity Boundaries
The system SHALL respect configured activity boundaries to ensure simulated actions stay within safe screen areas.

#### Scenario: Mouse movement within boundaries
- **WHEN** mouse movement is simulated
- **THEN** cursor stays within primary monitor bounds
- **AND** cursor does not move to screen edges
- **AND** safe zone margins are respected

#### Scenario: Detect application focus
- **WHEN** VSCode-specific activity is scheduled
- **THEN** system checks if VSCode window exists
- **AND** activity is skipped if VSCode not detected
- **AND** fallback activity is selected

### Requirement: Logging and Monitoring
The system SHALL log all activities, errors, and state changes for debugging and monitoring purposes.

#### Scenario: Log activity execution
- **WHEN** any activity is executed
- **THEN** activity type, timestamp, and parameters are logged
- **AND** log level is configurable (DEBUG, INFO, WARNING, ERROR)

#### Scenario: Log errors
- **WHEN** error occurs during activity execution
- **THEN** error details are logged with stack trace
- **AND** daemon continues operation
- **AND** error count is tracked

#### Scenario: Rotate log files
- **WHEN** log file exceeds configured size limit
- **THEN** log file is rotated
- **AND** old logs are compressed
- **AND** maximum number of log files is enforced

### Requirement: Intensity Levels
The system SHALL support configurable intensity levels (low, medium, high) that adjust activity frequency and variety.

#### Scenario: Low intensity mode
- **WHEN** intensity is set to low
- **THEN** mean interval is 180 seconds
- **AND** only mouse movement and scrolling are enabled
- **AND** activity parameters are conservative

#### Scenario: Medium intensity mode
- **WHEN** intensity is set to medium
- **THEN** mean interval is 120 seconds
- **AND** all activity types are enabled with balanced weights

#### Scenario: High intensity mode
- **WHEN** intensity is set to high
- **THEN** mean interval is 60 seconds
- **AND** all activity types are enabled
- **AND** activity parameters are more varied

### Requirement: Low-Level Windows Input Injection
The system SHALL use low-level Windows input injection via SendInput API with HARDWAREINPUT flag to bypass monitoring software detection at high-level message hooks.

#### Scenario: Initialize Win32 input injection
- **WHEN** daemon initializes
- **THEN** Win32 SendInput API is accessed via ctypes
- **AND** INPUT structures are prepared for keyboard and mouse
- **AND** HARDWAREINPUT flag is configured

#### Scenario: Inject mouse event at hardware level
- **WHEN** mouse movement activity is executed
- **THEN** events are injected via SendInput with HARDWAREINPUT flag
- **AND** events appear as hardware input to Windows
- **AND** high-level message hooks (SendMessage/PostMessage) are bypassed

#### Scenario: Inject keyboard event at hardware level
- **WHEN** keyboard activity is executed
- **THEN** key events are injected via SendInput with HARDWAREINPUT flag
- **AND** events bypass high-level API hooks

### Requirement: Behavioral Pattern Modeling
The system SHALL model realistic human work patterns including work sessions, breaks, and circadian rhythms.

#### Scenario: Work session simulation
- **WHEN** in work session state
- **THEN** activity frequency is high (mean 60-90 seconds)
- **AND** session duration is 20-50 minutes
- **AND** activity types favor productive actions

#### Scenario: Break period simulation
- **WHEN** in break state
- **THEN** activity frequency is low (mean 180-300 seconds)
- **AND** break duration is 5-15 minutes
- **AND** activity types favor browsing/reading

#### Scenario: Circadian rhythm adjustment
- **WHEN** time is early morning (6-9 AM)
- **THEN** activity ramps up gradually
- **WHEN** time is afternoon (2-4 PM)
- **THEN** activity slightly decreases (post-lunch dip)
- **WHEN** time is late evening (8+ PM)
- **THEN** activity tapers off

#### Scenario: Context switching
- **WHEN** transitioning between work sessions
- **THEN** simulate realistic context switch (1-3 minutes)
- **AND** include application switching activities
- **AND** vary activity patterns for new context

### Requirement: Activity Correlation
The system SHALL correlate activities to simulate realistic human action sequences.

#### Scenario: Mouse movement before click
- **WHEN** click activity is scheduled
- **THEN** mouse movement is executed first
- **AND** movement ends near click target
- **AND** brief pause (100-300ms) before click

#### Scenario: Scrolling with reading pauses
- **WHEN** scrolling activity is executed
- **THEN** scroll in bursts (2-5 scroll events)
- **AND** pause 2-8 seconds between bursts
- **AND** simulate reading behavior

#### Scenario: Tab switch with mouse movement
- **WHEN** tab switch activity is scheduled
- **THEN** move mouse toward tab area
- **AND** execute keyboard shortcut
- **AND** pause briefly after switch

### Requirement: Entropy Injection
The system SHALL inject entropy into all activity parameters to avoid detection through statistical analysis.

#### Scenario: Mouse movement with Bezier curves
- **WHEN** mouse movement is executed
- **THEN** path follows randomized Bezier curve
- **AND** speed varies along path (acceleration/deceleration)
- **AND** path curvature is randomized
- **AND** no two movements use identical parameters

#### Scenario: Timing micro-jitter
- **WHEN** any timed interval is calculated
- **THEN** add random jitter of ±50-200ms
- **AND** jitter follows non-uniform distribution
- **AND** avoid perfect multiples or round numbers

#### Scenario: Parameter randomization
- **WHEN** any activity parameter is selected
- **THEN** sample from appropriate distribution (not fixed value)
- **AND** ensure high entropy in parameter space
- **AND** track recent values to avoid repetition

### Requirement: Statistical Fingerprint Avoidance
The system SHALL avoid detectable statistical patterns in activity generation.

#### Scenario: No perfect intervals
- **WHEN** scheduling activities
- **THEN** no two intervals are identical
- **AND** intervals do not follow arithmetic sequences
- **AND** no fixed ratios between intervals

#### Scenario: Pattern detection resistance
- **WHEN** generating activity sequence
- **THEN** track last 20 activities
- **AND** avoid repeating sequences of 3+ activities
- **AND** vary activity type distribution over time

#### Scenario: Frequency analysis resistance
- **WHEN** activities are executed over time
- **THEN** activity frequency varies dynamically
- **AND** no fixed periodicity in activity timing
- **AND** spectral analysis shows noise-like characteristics

### Requirement: Monitoring Software Detection
The system SHALL detect common monitoring software and adapt behavior accordingly.

#### Scenario: Detect monitoring processes
- **WHEN** daemon starts or periodically
- **THEN** check for known monitoring process names (Insightful, Time Doctor, Hubstaff, ActivTrak)
- **AND** check for Windows API hooks (SetWindowsHookEx)
- **AND** detection results are logged

#### Scenario: Adaptive behavior when detected
- **WHEN** monitoring software is detected
- **THEN** switch to more conservative activity patterns
- **AND** increase timing randomization
- **AND** reduce activity frequency slightly
- **AND** log adaptive mode activation

#### Scenario: API hook detection
- **WHEN** checking system state
- **THEN** detect Windows message hooks (GetMessage, SendMessage hooks)
- **AND** detect input event interceptors
- **AND** adjust injection method if hooks detected

### Requirement: Composite Activities
The system SHALL combine multiple actions into realistic composite activity sequences.

#### Scenario: File editing workflow
- **WHEN** composite file editing activity is scheduled
- **THEN** execute sequence: mouse move → click → pause → type burst → pause → scroll → type burst
- **AND** pauses vary realistically (1-5 seconds)
- **AND** sequence parameters are randomized

#### Scenario: Application navigation
- **WHEN** composite navigation activity is scheduled
- **THEN** execute sequence: mouse move → pause → click → pause → scroll → pause
- **AND** simulate realistic navigation timing
- **AND** vary sequence based on context

#### Scenario: Reading simulation
- **WHEN** composite reading activity is scheduled
- **THEN** execute sequence: scroll → long pause (5-15s) → scroll → long pause
- **AND** simulate eye movement patterns with small mouse movements
- **AND** vary reading speed based on time of day
