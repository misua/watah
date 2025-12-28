# Change: Enhance Realistic Developer Behavior Simulation

## Why
Current activity simulation uses basic typing and mouse movements but lacks the nuanced behaviors that real developers exhibit throughout their workday. Monitoring software may detect patterns through absence of common developer actions like frequent saves, code navigation shortcuts, search operations, and realistic editing workflows. We need to add high-fidelity developer-specific behaviors to improve detection evasion and simulate actual coding work patterns.

Additionally, the 4pm auto-shutdown feature prevents thorough testing and should be disabled temporarily.

## What Changes
### High Priority Enhancements (Biggest Realism Gains):
1. **Frequent Save Operations** - Add Ctrl+S keypresses throughout editing sessions
2. **Word Selection Editing** - Double-click word selection before making edits
3. **Code Search Workflows** - Implement Ctrl+F search patterns with realistic typing and navigation
4. **Read-Before-Write Patterns** - Add deliberate code reading (scrolling/pausing) before typing
5. **Line Navigation** - Use Home/End keys within lines during editing

### Medium Priority Enhancements:
6. **Undo/Redo Sequences** - Simulate code revision with Ctrl+Z/Ctrl+Y patterns
7. **Context-Based State Machine** - Transition between READING, CODING, DEBUGGING, REVIEWING states
8. **Time-of-Day Behavior** - Adjust activity patterns based on time (morning catchup, afternoon cleanup)
9. **Copy-Paste Workflows** - Simulate code reuse with Ctrl+C/V between files
10. **Comment Toggle** - Use Ctrl+/ to comment/uncomment code blocks

### Low Priority Enhancements (Polish):
11. **Multi-Cursor Simulation** - Advanced IDE editing patterns
12. **Terminal Interactions** - Open terminal (Ctrl+`), run commands, close
13. **Advanced IDE Shortcuts** - Ctrl+Space autocomplete, Ctrl+Click navigation
14. **Line Movement** - Alt+Up/Down to reorder code

### Configuration Changes:
- Disable 4pm auto-shutdown in circadian timing for testing purposes

## Impact
- Affected specs: `activity-simulator` (modifications to existing capability)
- Affected code: 
  - `activity_simulator/activities.py` - New keyboard shortcuts and workflow methods
  - `activity_simulator/timing.py` - Remove 4pm shutdown, add state-based timing
  - `activity_simulator/daemon.py` - State machine integration
  - `activity_simulator/config.py` - New behavior configuration options
- External dependencies: No new dependencies
- Breaking changes: None (pure additions and optional feature removal)
