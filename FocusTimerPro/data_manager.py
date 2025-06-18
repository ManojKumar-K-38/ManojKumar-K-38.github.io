import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

class DataManager:
    def __init__(self):
        self.sessions = []
        self.daily_goals = {
            'focus_sessions': 8,
            'focus_minutes': 200
        }
    
    def log_session(self, session_data: Dict[str, Any]):
        """Log a completed session"""
        session_data['logged_at'] = datetime.now().isoformat()
        self.sessions.append(session_data)
        
        if len(self.sessions) > 1000:
            self.sessions = self.sessions[-1000:]
    
    def get_daily_stats(self, date: datetime = None) -> Dict[str, Any]:
        """Get statistics for a specific date (default: today)"""
        if date is None:
            date = datetime.now()
        
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        daily_sessions = [
            session for session in self.sessions
            if start_of_day <= datetime.fromisoformat(session['start_time']) < end_of_day
        ]
        
        focus_sessions = [s for s in daily_sessions if s['session_type'] == 'focus']
        break_sessions = [s for s in daily_sessions if s['session_type'] in ['short_break', 'long_break']]
        
        total_focus_time = sum(s['duration'] for s in focus_sessions) // 60
        total_break_time = sum(s['duration'] for s in break_sessions) // 60
        
        goal_sessions = self.daily_goals['focus_sessions']
        goal_minutes = self.daily_goals['focus_minutes']
        
        session_score = min(100, (len(focus_sessions) / goal_sessions) * 100) if goal_sessions > 0 else 0
        time_score = min(100, (total_focus_time / goal_minutes) * 100) if goal_minutes > 0 else 0
        productivity_score = (session_score + time_score) / 2
        
        return {
            'focus_sessions': len(focus_sessions),
            'total_focus_time': total_focus_time,
            'total_break_time': total_break_time,
            'productivity_score': productivity_score,
            'average_session_length': total_focus_time / len(focus_sessions) if focus_sessions else 0
        }
    
    def get_weekly_stats(self) -> Dict[str, Any]:
        """Get statistics for the current week"""
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        weekly_data = []
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            daily_stats = self.get_daily_stats(day)
            daily_stats['date'] = day.strftime('%Y-%m-%d')
            daily_stats['day_name'] = day.strftime('%A')
            weekly_data.append(daily_stats)
        
        total_focus_sessions = sum(day['focus_sessions'] for day in weekly_data)
        total_focus_time = sum(day['total_focus_time'] for day in weekly_data)
        average_productivity = sum(day['productivity_score'] for day in weekly_data) / 7
        
        return {
            'daily_breakdown': weekly_data,
            'total_focus_sessions': total_focus_sessions,
            'total_focus_time': total_focus_time,
            'average_productivity': average_productivity,
            'most_productive_day': max(weekly_data, key=lambda x: x['productivity_score'])['day_name']
        }
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent sessions"""
        sorted_sessions = sorted(
            self.sessions,
            key=lambda x: x['start_time'],
            reverse=True
        )
        return sorted_sessions[:limit]
    
    def get_session_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get session history for the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        return [
            session for session in self.sessions
            if datetime.fromisoformat(session['start_time']) >= cutoff_date
        ]
    
    def export_data(self) -> Dict[str, Any]:
        """Export all data for backup/analysis"""
        return {
            'sessions': self.sessions,
            'daily_goals': self.daily_goals,
            'export_timestamp': datetime.now().isoformat(),
            'total_sessions': len(self.sessions),
            'date_range': {
                'first_session': min(s['start_time'] for s in self.sessions) if self.sessions else None,
                'last_session': max(s['start_time'] for s in self.sessions) if self.sessions else None
            }
        }
    
    def import_data(self, data: Dict[str, Any]):
        """Import data from backup"""
        if 'sessions' in data:
            self.sessions.extend(data['sessions'])
            seen = set()
            unique_sessions = []
            for session in self.sessions:
                identifier = (session['start_time'], session['session_type'])
                if identifier not in seen:
                    seen.add(identifier)
                    unique_sessions.append(session)
            self.sessions = unique_sessions
        
        if 'daily_goals' in data:
            self.daily_goals.update(data['daily_goals'])
    
    def set_daily_goals(self, focus_sessions: int = None, focus_minutes: int = None):
        """Set daily productivity goals"""
        if focus_sessions is not None:
            self.daily_goals['focus_sessions'] = focus_sessions
        if focus_minutes is not None:
            self.daily_goals['focus_minutes'] = focus_minutes
    
    def get_streak_data(self) -> Dict[str, int]:
        """Calculate current and longest streaks"""
        if not self.sessions:
            return {'current_streak': 0, 'longest_streak': 0}
        
        session_dates = set()
        for session in self.sessions:
            if session['session_type'] == 'focus':
                date = datetime.fromisoformat(session['start_time']).date()
                session_dates.add(date)
        
        if not session_dates:
            return {'current_streak': 0, 'longest_streak': 0}
        
        sorted_dates = sorted(session_dates)
        
        current_streak = 0
        today = datetime.now().date()
        check_date = today
        
        while check_date in session_dates:
            current_streak += 1
            check_date -= timedelta(days=1)
        
        longest_streak = 1
        current_run = 1
        
        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] - sorted_dates[i-1] == timedelta(days=1):
                current_run += 1
                longest_streak = max(longest_streak, current_run)
            else:
                current_run = 1
        
        return {
            'current_streak': current_streak,
            'longest_streak': longest_streak
        }
