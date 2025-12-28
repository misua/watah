# Design: Realistic Developer Behavior Enhancement

## Overview
This change enhances the activity simulator with high-fidelity developer-specific behaviors that go beyond basic mouse/keyboard actions. The design introduces a layered approach: immediate high-impact actions (saves, selections, searches) built on the existing architecture, followed by behavioral state management for more sophisticated patterns.

## Key Design Decisions

### 1. Incremental Enhancement Strategy
**Decision:** Add new capabilities to existing classes rather than rewriting core architecture.

**Rationale:** 
- Existing `KeyboardActivity`, `MouseActivity`, and `CompositeActivity` classes provide solid foundation
- Lower risk of introducing regressions
- Faster implementation and testing cycle
- Preserves proven anti-detection features (timing randomization, entropy injection)

**Implementation:**
- Extend `KeyboardActivity` with new shortcut methods (`press_ctrl_s()`, `press_ctrl_f()`, etc.)
- Add new composite workflows to `CompositeActivity` class
- Preserve existing Win32 input injection mechanisms

### 2. Behavioral State Machine
**Decision:** Introduce explicit developer states (READING, CODING, DEBUGGING, REVIEWING) with state-specific activity patterns.

**Rationale:**
- Real developers don't perform random actions; they follow cognitive workflows
- Different states have distinct action frequencies and types (e.g., READING = more scrolling, less typing)
- State transitions model realistic context switching
- Enables time-of-day behavior adjustments (morning = more READING, afternoon = REVIEWING)

**Architecture:**
```
DeveloperState (enum)
├── READING_CODE    → High scroll, low typing, medium navigation
├── ACTIVE_CODING   → High typing, frequent saves, searches
├── DEBUGGING       → File switching, searches, selective edits
└── REVIEWING       → Slow scroll, long pauses, occasional comments

State Transitions (Markov-like):
- READING → ACTIVE_CODING (60%)
- ACTIVE_CODING → DEBUGGING (30%)
- DEBUGGING → ACTIVE_CODING (50%)
- Any → REVIEWING (time-based: after sustained work)
```

**Implementation:**
- Add `DeveloperStateMachine` class in new module `activity_simulator/developer_states.py`
- Integrate with existing `TimingRandomizer` to adjust intervals per state
- Modify `ActivityDaemon` to consult state when selecting activities

### 3. Activity Sequencing and Correlation
**Decision:** Build "micro-workflows" that chain related actions with realistic pauses.

**Rationale:**
- Humans perform actions in predictable sequences (e.g., search → navigate → edit → save)
- Isolated actions look robotic; correlated sequences look human
- Enables realistic editing patterns (read → scroll → double-click word → edit → save)

**Pattern Examples:**
```python
# Edit Workflow
1. Scroll to code (reading)
2. Pause (thinking: 1-3s)
3. Double-click word
4. Type replacement
5. Press Ctrl+S (save)
6. Pause (reviewing: 0.5-1.5s)

# Search Workflow
1. Press Ctrl+F
2. Pause (100-200ms)
3. Type search term (slower, deliberate typing)
4. Press Enter
5. Pause (reading result: 1-3s)
6. Press Escape
7. Navigate to result location
```

### 4. Priority-Based Implementation
**Decision:** Implement in three phases matching priority levels (High → Medium → Low).

**Rationale:**
- High priority items provide 80% of realism improvement with 20% effort
- Allows early validation of approach before investing in complex features
- Each phase deliverable and testable independently
- Can abort low-priority work if sufficient realism achieved

### 5. Timing Adjustment: Remove 4pm Shutdown
**Decision:** Remove or make optional the hard 4pm cutoff in `TimingRandomizer.get_circadian_multiplier()`.

**Rationale:**
- Testing requires extended observation periods
- Shutdown prevents validation of late-afternoon/evening behavior patterns
- Real developers have variable schedules, not rigid cutoffs
- Can re-enable later with configuration flag

**Implementation:**
- Remove `sys.exit(0)` calls from timing.py
- Add configuration option `timing.enable_end_of_day_shutdown` (default: false)
- Replace with activity frequency reduction instead of hard stop

## Technical Considerations

### Keyboard Shortcut Reliability
- Use existing `press_ctrl_key_combo()` infrastructure
- Add validation logging for shortcut execution
- Implement fallback behaviors if shortcuts fail

### Activity Weight Rebalancing
- Existing weights may need adjustment to accommodate new activities
- Proposal: Reduce mouse_movement weight (0.3 → 0.2) to make room for developer actions
- Add new category: `developer_workflows` (weight: 0.15)

### State Persistence
- States should persist across activity cycles (not reset each action)
- Track state duration to trigger transitions (e.g., 5-15 min coding → break/review)
- Store in daemon instance, not global state

### Testing Strategy
- Unit tests for each new shortcut method
- Integration tests for workflow sequences
- Manual observation with detailed logging
- Validation: Record 1-hour session, analyze for patterns/anomalies

## Alternative Approaches Considered

### Alternative 1: ML-Based Behavior Learning
**Rejected Reason:** Overengineered for current need. Requires training data, complex infrastructure. Current statistical approach sufficient.

### Alternative 2: Record-and-Replay Human Sessions
**Rejected Reason:** Not scalable, requires constant updating, lacks adaptability. Generative approach more flexible.

### Alternative 3: Complete Rewrite with Behavior Trees
**Rejected Reason:** High risk, long timeline. Incremental enhancement delivers faster value with lower risk.

## Migration Path
No migration needed - all changes are additive and backward compatible. Existing configurations continue working unchanged.

## Success Criteria
- Visual observation: Activity patterns indistinguishable from human developer
- Statistical analysis: No detectable patterns in timing or action sequences
- Monitoring software: No alerts or anomalies detected during extended testing
- Code quality: Maintains existing test coverage and anti-detection features
