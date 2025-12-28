# Implementation Tasks

## Phase 1: High Priority (Biggest Realism Gains)

### Task 1.1: Add Ctrl+S Save Operation
- [x] Add `press_ctrl_s()` method to `KeyboardActivity` class
- [x] Implement SendInput call for Ctrl+S key combination
- [x] Add post-save pause timing (0.2-0.5s)
- [x] Integrate into typing activity completion (70% probability)
- [x] Add logging for save operations
- [ ] Test save operation in VS Code

**Validation:** Run typing activity 20 times, verify ~14 saves occur

### Task 1.2: Implement Double-Click Word Selection
- [x] Add `double_click_word()` method to `MouseActivity` class
- [x] Generate double-click mouse event at current cursor position
- [x] Add selection confirmation pause (100-300ms)
- [x] Create `edit_with_selection_workflow()` in `CompositeActivity`
- [x] Chain: double-click → pause → type replacement → save
- [ ] Test word selection in editor

**Validation:** Execute workflow 10 times, observe word selections before edits

### Task 1.3: Implement Ctrl+F Search Workflow
- [x] Add `press_ctrl_f()` method to `KeyboardActivity` class
- [x] Add `type_search_term()` with slower deliberate typing (80-150ms/char)
- [x] Add `press_escape()` method to close search
- [x] Create `search_workflow()` in `CompositeActivity`
- [x] Chain: Ctrl+F → pause → type term → Enter → pause → Escape
- [x] Add configurable search terms list
- [ ] Test search in VS Code

**Validation:** Execute search workflow, verify search dialog opens and closes correctly

### Task 1.4: Implement Read-Before-Write Pattern
- [x] Create `read_code_section()` method in `CompositeActivity`
- [x] Implement 2-4 scroll events with 1.5-3.5s pauses between
- [x] Add thinking pause before typing (0.5-1.5s)
- [x] Modify `type_random_text()` to optionally call read pattern first (40% probability)
- [x] Add configuration for read-first probability
- [ ] Test read-then-type sequence

**Validation:** Observe 20 typing activities, verify ~8 include prior reading

### Task 1.5: Add Home/End Line Navigation
- [x] Add `press_home()` method to `KeyboardActivity`
- [x] Add `press_end()` method to `KeyboardActivity`
- [x] Add cursor positioning pause (50-150ms)
- [x] Integrate into typing workflows (25% of edits)
- [x] Create `edit_at_line_boundary()` workflow
- [ ] Test navigation in editor

**Validation:** Monitor navigation key usage during editing sessions

## Phase 2: Medium Priority

### Task 2.1: Implement Undo/Redo Sequences
- [ ] Add `press_ctrl_z()` method to `KeyboardActivity` (undo)
- [ ] Add `press_ctrl_y()` method to `KeyboardActivity` (redo)
- [ ] Add undo/redo pause timing (200-400ms)
- [ ] Create `correction_sequence()` workflow
- [ ] Integrate into typing activity (5% trigger probability)
- [ ] Chain: pause → undo 1-3x → thinking pause → optional redo → resume
- [ ] Test correction patterns

**Validation:** Run 100 typing chars, verify ~5 corrections occur

### Task 2.2: Create Developer State Machine
- [ ] Create new file `activity_simulator/developer_states.py`
- [ ] Define `DeveloperState` enum (READING, CODING, DEBUGGING, REVIEWING)
- [ ] Implement `DeveloperStateMachine` class
- [ ] Define state-specific activity weight adjustments
- [ ] Implement state transition probability matrix
- [ ] Add state duration tracking (min/max per state)
- [ ] Add state transition logic
- [ ] Test state transitions over time

**Validation:** Run 1-hour session, verify state transitions occur with expected frequencies

### Task 2.3: Integrate State Machine with Activity Selection
- [ ] Modify `ActivityDaemon` to instantiate state machine
- [ ] Pass current state to activity selection logic
- [ ] Adjust activity weights based on current state
- [ ] Adjust timing intervals per state (CODING=faster, READING=slower)
- [ ] Log state transitions
- [ ] Test state-driven activity selection

**Validation:** Observe activity patterns change appropriately per state

### Task 2.4: Implement Time-of-Day Behavior Adjustments
- [ ] Modify `get_circadian_multiplier()` in `TimingRandomizer`
- [ ] Add morning catchup pattern (9-11am: +30% READING state)
- [ ] Add peak productivity pattern (11am-1pm: +40% CODING state)
- [ ] Add post-lunch adjustment (1-3pm: slower timing, more errors)
- [ ] Add afternoon cleanup (3-5pm: +25% REVIEWING state)
- [ ] Remove 4pm sys.exit() hard stop
- [ ] Test throughout full work day

**Validation:** Run simulator 9am-5pm, verify patterns shift appropriately

### Task 2.5: Implement Copy-Paste Workflows
- [ ] Add `press_ctrl_c()` method to `KeyboardActivity` (copy)
- [ ] Add `press_ctrl_v()` method to `KeyboardActivity` (paste)
- [ ] Add `select_text_block()` method (Shift+Arrows or Ctrl+A in context)
- [ ] Create `copy_paste_workflow()` in `CompositeActivity`
- [ ] Chain: select → copy → pause → switch tab → navigate → paste → review
- [ ] Add optional paste-and-modify (40% probability)
- [ ] Test copy-paste between files

**Validation:** Execute copy-paste workflow, observe clipboard operations

### Task 2.6: Implement Comment Toggle Operation
- [ ] Add `press_ctrl_slash()` method to `KeyboardActivity` (Ctrl+/)
- [ ] Add line positioning before comment
- [ ] Add comment operation pause (150-300ms)
- [ ] Create `toggle_comment_workflow()`
- [ ] Integrate into REVIEWING state activities
- [ ] Test comment toggle in VS Code

**Validation:** Execute comment workflow, verify lines get commented/uncommented

## Phase 3: Low Priority (Polish)

### Task 3.1: Multi-Cursor Simulation (Placeholder)
- [ ] Research multi-cursor keyboard shortcuts
- [ ] Design multi-cursor workflow pattern
- [ ] Implement if time permits and earlier phases successful

**Note:** Can defer or skip based on Phase 1-2 results

### Task 3.2: Terminal Interactions
- [ ] Add `press_ctrl_backtick()` method (open terminal)
- [ ] Create `terminal_workflow()`: open → type command → wait → close
- [ ] Add common developer commands list (git status, npm test, etc.)
- [ ] Test terminal operations

**Validation:** Execute terminal workflow, verify terminal opens/closes

### Task 3.3: Advanced IDE Shortcuts
- [ ] Add `press_ctrl_space()` for autocomplete simulation
- [ ] Add `ctrl_click_navigation()` for go-to-definition
- [ ] Create workflows for these advanced features
- [ ] Test in VS Code

### Task 3.4: Line Movement Commands
- [ ] Add `press_alt_up()` method (move line up)
- [ ] Add `press_alt_down()` method (move line down)
- [ ] Create `reorder_code_workflow()`
- [ ] Test line movement

## Phase 4: Configuration and Testing

### Task 4.1: Update Configuration Schema
- [ ] Add `developer_behaviors` section to config.yaml
- [ ] Add `save_frequency` setting (default: 0.7)
- [ ] Add `search_frequency` setting (default: 0.15)
- [ ] Add `read_before_write_probability` setting (default: 0.4)
- [ ] Add `undo_redo_probability` setting (default: 0.05)
- [ ] Add `state_machine_enabled` setting (default: true)
- [ ] Add `time_of_day_adjustments` setting (default: true)
- [ ] Add `enable_end_of_day_shutdown` setting (default: false)
- [ ] Update config.example.yaml with new settings
- [ ] Update README with behavior configuration documentation

**Validation:** Load config, verify all settings parse correctly

### Task 4.2: Remove 4pm Shutdown Logic
- [x] Locate sys.exit() calls in `timing.py` (lines ~100-110)
- [x] Remove or comment out 4pm hard stop logic
- [x] Replace with optional frequency reduction if configured
- [x] Test simulator continues past 4pm
- [x] Add configuration flag for optional shutdown

**Validation:** Run simulator from 3:45pm to 4:15pm, verify no exit

### Task 4.3: Enhanced Logging for New Behaviors
- [ ] Add debug logging for all new keyboard shortcuts
- [ ] Add state transition logging
- [ ] Add workflow execution logging
- [ ] Add timing adjustment logging (time-of-day)
- [ ] Create log analysis script to verify patterns

**Validation:** Review logs, ensure all new behaviors are traceable

### Task 4.4: Integration Testing
- [ ] Test complete edit-save workflow (10 iterations)
- [ ] Test search-edit-save workflow (10 iterations)
- [ ] Test read-before-write patterns (20 iterations)
- [ ] Test state transitions over 30-minute session
- [ ] Test time-of-day adjustments (full day simulation)
- [ ] Test copy-paste workflows (10 iterations)
- [ ] Verify no interference with actual user input
- [ ] Verify all Win32 SendInput calls succeed

**Validation:** All workflows execute without errors, logs show expected patterns

### Task 4.5: Manual Observation and Pattern Analysis
- [ ] Run 1-hour observation session with detailed logging
- [ ] Record activity types, frequencies, and timings
- [ ] Analyze for detectable patterns or anomalies
- [ ] Compare against actual developer behavior
- [ ] Identify any remaining robotic patterns
- [ ] Document findings and refinement needs

**Validation:** Activity patterns pass visual inspection, no obvious anomalies

### Task 4.6: Documentation Updates
- [ ] Update README.md with new developer behavior features
- [ ] Document new configuration options
- [ ] Add examples of new workflows
- [ ] Update QUICKSTART.md if needed
- [ ] Document state machine behavior
- [ ] Add troubleshooting section for new features

**Validation:** Documentation accurately reflects implemented features

## Dependencies and Sequencing

**Must Complete Before Others:**
- Task 1.1-1.5 (High priority) must complete before Phase 2
- Task 2.2 (State Machine) must complete before Task 2.3 (Integration)
- Task 4.1 (Config) should complete early for use throughout

**Can Parallelize:**
- Phase 1 tasks (1.1-1.5) are independent, can be done in any order
- Phase 2 tasks except 2.2→2.3 dependency
- Phase 3 tasks are fully independent

**Optional/Can Skip:**
- Phase 3 tasks if Phase 1-2 provide sufficient realism
- Individual keyboard shortcuts if proven redundant

## Testing Strategy

After each task:
1. Unit test the specific method/function
2. Integration test within larger workflow
3. Manual observation in real VS Code environment
4. Review logs for proper execution
5. Verify no errors or anomalies

After each phase:
1. Extended observation session (30-60 minutes)
2. Statistical analysis of activity patterns
3. Comparison against actual human developer session
4. Identify gaps for next phase

Final validation:
1. Full 8-hour simulation (9am-5pm)
2. Comprehensive log analysis
3. No detectable patterns or anomalies
4. Passes visual inspection as human-like behavior
