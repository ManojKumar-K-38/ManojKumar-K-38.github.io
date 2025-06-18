import time
from datetime import datetime
from enum import Enum

class SessionType(Enum):
    FOCUS = "focus"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"

class TimerState(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"

class TimerManager:
    def __init__(self):
        self.state = TimerState.STOPPED
        self.current_session = SessionType.FOCUS
        self.session_count = 0
        self.start_time = None
        self.pause_time = None
        self.duration = 0
        self.remaining_time = 0
        self.session_start = None
        
    def start_timer(self, settings):
        """Start the timer with current session type"""
        if self.state == TimerState.PAUSED:
            pause_duration = time.time() - self.pause_time
            self.start_time += pause_duration
        else:
            self.duration = self._get_session_duration(settings)
            self.remaining_time = self.duration
            self.start_time = time.time()
            self.session_start = datetime.now()
        
        self.state = TimerState.RUNNING
        self.pause_time = None
    
    def pause_timer(self):
        """Pause the current timer"""
        if self.state == TimerState.RUNNING:
            self.state = TimerState.PAUSED
            self.pause_time = time.time()
    
    def stop_timer(self):
        """Stop the current timer"""
        self.state = TimerState.STOPPED
        self.start_time = None
        self.pause_time = None
        self.remaining_time = 0
    
    def reset_timer(self):
        """Reset timer to initial state"""
        self.stop_timer()
        self.current_session = SessionType.FOCUS
        self.session_count = 0
    
    def update(self):
        """Update timer state and return True if session completed"""
        if self.state != TimerState.RUNNING:
            return False
        
        elapsed = time.time() - self.start_time
        self.remaining_time = max(0, self.duration - elapsed)
        
        if self.remaining_time <= 0:
            self._complete_session()
            return True
        
        return False
    
    def _complete_session(self):
        """Mark current session as completed and prepare for next"""
        self.state = TimerState.COMPLETED
        
        if self.current_session == SessionType.FOCUS:
            self.session_count += 1
        
        self._set_next_session()
    
    def _set_next_session(self):
        """Set the next session type based on current state"""
        if self.current_session == SessionType.FOCUS:
            if self.session_count % 4 == 0:
                self.current_session = SessionType.LONG_BREAK
            else:
                self.current_session = SessionType.SHORT_BREAK
        else:
            self.current_session = SessionType.FOCUS
    
    def start_next_session(self, settings):
        """Start the next session automatically"""
        self.start_timer(settings)
    
    def _get_session_duration(self, settings):
        """Get duration in seconds for current session type"""
        if self.current_session == SessionType.FOCUS:
            return settings['focus_duration'] * 60
        elif self.current_session == SessionType.SHORT_BREAK:
            return settings['short_break'] * 60
        else:
            return settings['long_break'] * 60
    
    def get_remaining_time(self):
        """Get remaining time in seconds"""
        return self.remaining_time
    
    def get_progress(self):
        """Get progress as a percentage (0.0 to 1.0)"""
        if self.duration == 0:
            return 0.0
        return max(0.0, (self.duration - self.remaining_time) / self.duration)
    
    def get_session_type_display(self):
        """Get formatted session type for display"""
        type_map = {
            SessionType.FOCUS: "🎯 Focus Session",
            SessionType.SHORT_BREAK: "☕ Short Break",
            SessionType.LONG_BREAK: "🌟 Long Break"
        }
        return type_map.get(self.current_session, "🎯 Focus Session")
    
    def get_next_session_type(self):
        """Get the next session type as string"""
        if self.current_session == SessionType.FOCUS:
            return "short_break" if self.session_count % 4 != 0 else "long_break"
        else:
            return "focus"
    
    def is_running(self):
        """Check if timer is currently running"""
        return self.state == TimerState.RUNNING
    
    def is_paused(self):
        """Check if timer is paused"""
        return self.state == TimerState.PAUSED
    
    def get_completed_session_data(self):
        """Get data for the completed session"""
        return {
            'session_type': self.current_session.value,
            'duration': self.duration,
            'start_time': self.session_start.isoformat() if self.session_start else None,
            'end_time': datetime.now().isoformat(),
            'completed': True
        }
