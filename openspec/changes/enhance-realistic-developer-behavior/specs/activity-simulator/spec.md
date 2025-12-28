# Activity Simulator Spec Delta

## MODIFIED Requirements

### Requirement: Human-Like Activity Simulation
The system SHALL simulate realistic human computer activity with randomized timing and natural patterns, INCLUDING developer-specific workflows and keyboard shortcuts.

#### Scenario: Frequent save operations during coding
- **WHEN** keyboard typing activity completes
- **THEN** Ctrl+S is pressed with 70% probability
- **AND** save occurs 0.3-1.0 seconds after typing stops
- **AND** brief pause follows save (0.2-0.5s)

#### Scenario: Word selection before editing
- **WHEN** code editing workflow is initiated
- **AND** modification mode is selected
- **THEN** double-click word selection is performed
- **AND** pause occurs (0.1-0.3s) before typing replacement
- **AND** typing begins at selected location

#### Scenario: Search workflow execution
- **WHEN** search activity is scheduled
- **THEN** Ctrl+F shortcut is pressed
- **AND** pause occurs (100-200ms) for search dialog
- **AND** search term is typed with deliberate speed (80-150ms per char)
- **AND** Enter key is pressed to execute search
- **AND** reading pause occurs (1-3s)
- **AND** Escape key closes search dialog

#### Scenario: Read-before-write pattern
- **WHEN** typing activity is about to execute
- **AND** read-first pattern is selected (40% probability)
- **THEN** scrolling occurs first (2-4 scroll events)
- **AND** reading pause follows each scroll (1.5-3.5s)
- **AND** navigation to edit point occurs
- **AND** thinking pause precedes typing (0.5-1.5s)
- **AND** typing activity executes

#### Scenario: Line navigation with Home/End keys
- **WHEN** within-line editing is selected
- **THEN** Home or End key is pressed before typing
- **AND** cursor positioning pause occurs (0.1-0.3s)
- **AND** typing or deletion occurs at line boundary

#### Scenario: Undo/redo correction sequence
- **WHEN** typing activity is in progress
- **AND** correction pattern triggers (5% probability during typing)
- **THEN** typing pauses
- **AND** Ctrl+Z (undo) is pressed 1-3 times
- **AND** thinking pause occurs (0.3-0.8s)
- **AND** Ctrl+Y (redo) may be pressed (30% probability)
- **AND** corrected typing resumes or new approach begins

#### Scenario: Copy-paste workflow between files
- **WHEN** copy-paste activity is scheduled
- **THEN** text selection occurs (Shift+Arrows or Ctrl+A in context)
- **AND** Ctrl+C is pressed
- **AND** brief pause occurs (0.2-0.5s)
- **AND** file/tab switch occurs (Ctrl+Tab)
- **AND** navigation to paste location occurs
- **AND** Ctrl+V is pressed
- **AND** pasted content is reviewed (pause 1-2s)
- **AND** modifications to pasted code occur (optional, 40% probability)

#### Scenario: Comment toggle operation
- **WHEN** comment activity is scheduled
- **THEN** line selection or cursor positioning occurs
- **AND** Ctrl+/ is pressed
- **AND** brief pause follows (0.2-0.5s)
- **AND** navigation continues or typing resumes

### Requirement: Behavioral State Management
The system SHALL maintain developer behavioral states (READING, CODING, DEBUGGING, REVIEWING) that influence activity selection and timing patterns.

#### Scenario: State transition to READING_CODE
- **WHEN** state transitions to READING_CODE
- **THEN** scrolling activity weight increases to 50%
- **AND** typing activity weight decreases to 10%
- **AND** navigation activity weight increases to 30%
- **AND** average pause between actions increases (2-5s)
- **AND** state persists for 3-8 minutes before transition

#### Scenario: State transition to ACTIVE_CODING
- **WHEN** state transitions to ACTIVE_CODING
- **THEN** typing activity weight increases to 50%
- **AND** save operations occur frequently (70% after typing)
- **AND** search activities increase (15% probability)
- **AND** average pause between actions decreases (0.5-2s)
- **AND** state persists for 5-15 minutes before transition

#### Scenario: State transition to DEBUGGING
- **WHEN** state transitions to DEBUGGING
- **THEN** file switching increases (Ctrl+Tab 25% of actions)
- **AND** search activity increases to 30%
- **AND** reading pauses lengthen (2-6s)
- **AND** selective small edits occur (line or word level)
- **AND** undo/redo patterns increase (10% probability)
- **AND** state persists for 4-10 minutes before transition

#### Scenario: State transition to REVIEWING
- **WHEN** state transitions to REVIEWING
- **THEN** scrolling becomes primary activity (60%)
- **AND** scrolling speed decreases (longer pauses)
- **AND** typing becomes rare (5% of actions)
- **AND** comment additions occur (Ctrl+/, comment text)
- **AND** save operations occur after comments
- **AND** state persists for 2-5 minutes before transition

#### Scenario: State-based Markov transitions
- **WHEN** current state duration exceeds minimum threshold
- **THEN** transition probability is evaluated
- **AND** transition follows defined probability matrix
- **AND** READING → ACTIVE_CODING (60%), REVIEWING (20%), DEBUGGING (20%)
- **AND** ACTIVE_CODING → ACTIVE_CODING (40%), DEBUGGING (30%), REVIEWING (20%), READING (10%)
- **AND** DEBUGGING → ACTIVE_CODING (50%), DEBUGGING (25%), READING (15%), REVIEWING (10%)
- **AND** REVIEWING → ACTIVE_CODING (40%), READING (35%), DEBUGGING (15%), REVIEWING (10%)

### Requirement: Time-of-Day Behavioral Patterns
The system SHALL adjust activity patterns based on time of day to simulate realistic developer work rhythms.

#### Scenario: Morning catchup period (9-11am)
- **WHEN** current time is 9am-11am
- **THEN** READING_CODE state probability increases by 30%
- **AND** file switching frequency increases
- **AND** typing speed starts slower and accelerates
- **AND** search activities increase (reviewing overnight changes)

#### Scenario: Peak productivity (11am-1pm)
- **WHEN** current time is 11am-1pm
- **THEN** ACTIVE_CODING state probability increases by 40%
- **AND** typing occurs in longer bursts
- **AND** save frequency peaks
- **AND** activity interval decreases (more frequent actions)

#### Scenario: Post-lunch adjustment (1-3pm)
- **WHEN** current time is 1pm-3pm
- **THEN** activity frequency decreases slightly (10-15%)
- **AND** reading pauses lengthen (post-meal sluggishness)
- **AND** mistake frequency increases slightly (more typos, more undo)

#### Scenario: Afternoon cleanup (3-5pm)
- **WHEN** current time is 3pm-5pm
- **THEN** REVIEWING state probability increases by 25%
- **AND** comment activity increases
- **AND** save operations increase (finishing work)
- **AND** typing sessions become shorter

## REMOVED Requirements

### Requirement: Fixed End-of-Day Shutdown
The system SHALL NOT enforce a hard shutdown at 4pm to allow extended testing and flexible work schedules.

#### Scenario: 4pm hard stop removed
- **WHEN** time reaches 4:00pm-4:30pm
- **THEN** activities continue (no sys.exit)
- **AND** activity frequency may optionally reduce if configured
- **AND** circadian multiplier adjusts activity timing instead of stopping

## ADDED Requirements

### Requirement: Advanced IDE Keyboard Shortcuts
The system SHALL support simulation of common IDE keyboard shortcuts used by developers throughout their workflow.

#### Scenario: Ctrl+S save shortcut
- **WHEN** save operation is triggered
- **THEN** Ctrl+S key combination is sent via SendInput
- **AND** success is validated
- **AND** operation is logged

#### Scenario: Ctrl+F search initiation
- **WHEN** search workflow begins
- **THEN** Ctrl+F key combination is sent
- **AND** search dialog opening pause occurs
- **AND** cursor is positioned in search field (simulated)

#### Scenario: Double-click word selection
- **WHEN** word selection is needed
- **THEN** double-click mouse event is generated at current cursor position
- **AND** selection pause occurs (100-300ms)
- **AND** selected state is tracked for subsequent operations

#### Scenario: Ctrl+Z undo operation
- **WHEN** undo action is triggered
- **THEN** Ctrl+Z key combination is sent
- **AND** undo pause occurs (200-400ms)
- **AND** visual review pause follows

#### Scenario: Ctrl+Y redo operation
- **WHEN** redo action is triggered after undo
- **THEN** Ctrl+Y key combination is sent
- **AND** redo pause occurs (200-400ms)

#### Scenario: Ctrl+C copy operation
- **WHEN** copy workflow begins
- **THEN** text selection occurs
- **AND** Ctrl+C key combination is sent
- **AND** clipboard operation pause occurs (100-200ms)

#### Scenario: Ctrl+V paste operation
- **WHEN** paste workflow executes
- **THEN** cursor positioning occurs
- **AND** Ctrl+V key combination is sent
- **AND** paste completion pause occurs (200-500ms)
- **AND** pasted content review pause follows

#### Scenario: Ctrl+/ comment toggle
- **WHEN** commenting action is triggered
- **THEN** line positioning occurs (Home key or line selection)
- **AND** Ctrl+/ key combination is sent
- **AND** comment operation pause occurs (150-300ms)

#### Scenario: Home key line start navigation
- **WHEN** line start positioning is needed
- **THEN** Home key is pressed
- **AND** cursor positioning pause occurs (50-150ms)

#### Scenario: End key line end navigation
- **WHEN** line end positioning is needed
- **THEN** End key is pressed
- **AND** cursor positioning pause occurs (50-150ms)

### Requirement: Composite Developer Workflows
The system SHALL provide realistic multi-step developer workflows that chain related actions in natural sequences.

#### Scenario: Complete edit-save workflow
- **WHEN** edit-save workflow is scheduled
- **THEN** read-before-write pattern executes (optional, 40%)
- **AND** code location navigation occurs
- **AND** word selection occurs (optional, 60%)
- **AND** typing activity executes
- **AND** review pause follows typing (0.5-1.5s)
- **AND** Ctrl+S save occurs
- **AND** completion pause follows (0.3-0.8s)

#### Scenario: Search-edit-save workflow
- **WHEN** search-edit workflow is scheduled
- **THEN** Ctrl+F search initiates
- **AND** search term is typed
- **AND** search executes (Enter)
- **AND** results are reviewed (pause 1-3s)
- **AND** search closes (Escape)
- **AND** navigation to found location occurs
- **AND** edit workflow executes
- **AND** save operation completes workflow

#### Scenario: Code review workflow
- **WHEN** code review activity is scheduled
- **THEN** scrolling occurs with reading pauses (2-5s per section)
- **AND** occasional navigation to specific lines
- **AND** comment addition occurs (30% probability)
- **AND** continued scrolling resumes
- **AND** session ends with save if comments added

### Requirement: Configuration for Developer Behaviors
The system SHALL provide configuration options for developer-specific behavior patterns and state management.

#### Scenario: Configure developer state weights
- **WHEN** configuration specifies state weights
- **THEN** initial state selection uses configured probabilities
- **AND** transition matrix respects configured biases
- **AND** state durations use configured ranges

#### Scenario: Configure keyboard shortcut frequencies
- **WHEN** configuration specifies shortcut usage rates
- **THEN** save frequency (post-typing) uses configured probability
- **AND** search activity frequency uses configured rate
- **AND** undo/redo occurrence uses configured probability

#### Scenario: Configure time-of-day adjustments
- **WHEN** configuration enables time-based patterns
- **THEN** activity weights adjust per configured time brackets
- **AND** state transition probabilities shift by time of day
- **AND** timing intervals adjust according to schedule

#### Scenario: Disable end-of-day shutdown
- **WHEN** configuration sets `timing.enable_end_of_day_shutdown` to false
- **THEN** no sys.exit occurs at 4pm
- **AND** circadian multiplier continues adjusting activity frequency
- **AND** activities continue through evening hours
