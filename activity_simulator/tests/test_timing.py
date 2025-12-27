"""
Tests for timing randomization
"""
import pytest
from activity_simulator.timing import TimingRandomizer, MarkovChain, BehavioralPatternModel


def test_timing_randomizer_intervals():
    config = {"base_interval": 180, "intensity": "medium"}
    timer = TimingRandomizer(config)
    
    interval = timer.get_next_interval("work")
    assert 20 <= interval <= 600
    
    interval = timer.get_next_interval("break")
    assert 20 <= interval <= 600


def test_timing_randomizer_pause_duration():
    config = {"base_interval": 180, "intensity": "medium"}
    timer = TimingRandomizer(config)
    
    pause = timer.get_pause_duration("mouse_move")
    assert pause > 0
    
    pause = timer.get_pause_duration("type")
    assert pause > 0


def test_markov_chain():
    chain = MarkovChain()
    
    initial_state = chain.get_state()
    assert initial_state in chain.states
    
    next_state = chain.next_state()
    assert next_state in chain.states


def test_behavioral_pattern_model():
    model = BehavioralPatternModel()
    
    state = model.get_current_state()
    assert state in ["work", "break", "reading", "typing", "browsing"]
    
    model.update(10)
    assert not model.is_in_break()
