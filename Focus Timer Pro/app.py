import streamlit as st
import time
import json
from datetime import datetime, timedelta
from timer_manager import TimerManager
from data_manager import DataManager
from themes import THEMES

# Initialize session state
if 'timer_manager' not in st.session_state:
    st.session_state.timer_manager = TimerManager()
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = 'Ocean Blue'
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'focus_duration': 25,
        'short_break': 5,
        'long_break': 15,
        'sessions_until_long_break': 4,
        'auto_start_breaks': False,
        'auto_start_focus': False,
        'notifications_enabled': True
    }

def apply_custom_css():
    """Apply custom CSS for the selected theme"""
    theme = THEMES[st.session_state.current_theme]
    css = f"""
    <style>
    /* Mobile-first responsive design */
    .timer-display {{
        text-align: center;
        font-size: clamp(2.5rem, 8vw, 4rem);
        font-weight: bold;
        color: {theme['primary']};
        margin: 1rem 0 2rem 0;
        font-family: 'Courier New', monospace;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        line-height: 1.2;
    }}
    
    .session-type {{
        text-align: center;
        font-size: clamp(1rem, 4vw, 1.5rem);
        color: {theme['secondary']};
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        word-wrap: break-word;
    }}
    
    .progress-bar {{
        width: 100%;
        height: 20px;
        background-color: {theme['background']};
        border-radius: 10px;
        margin: 1rem 0;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
        touch-action: none;
    }}
    
    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, {theme['primary']}, {theme['accent']});
        border-radius: 10px;
        transition: width 0.3s ease;
    }}
    
    .stats-card {{
        background: {theme['background']};
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid {theme['primary']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        word-wrap: break-word;
    }}
    
    .control-button {{
        margin: 0.25rem;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        min-height: 44px;
        touch-action: manipulation;
        font-size: 0.9rem;
    }}
    
    .start-button {{
        background: {theme['success']};
        color: white;
    }}
    
    .pause-button {{
        background: {theme['warning']};
        color: white;
    }}
    
    .stop-button {{
        background: {theme['danger']};
        color: white;
    }}
    
    .metric-value {{
        font-size: clamp(1.2rem, 4vw, 2rem);
        font-weight: bold;
        color: {theme['primary']};
    }}
    
    .session-history {{
        max-height: 300px;
        overflow-y: auto;
        background: {theme['background']};
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        -webkit-overflow-scrolling: touch;
    }}
    
    /* Mobile specific adjustments */
    @media (max-width: 768px) {{
        .timer-display {{
            margin: 0.5rem 0 1.5rem 0;
        }}
        
        .session-type {{
            font-size: 1.1rem;
            letter-spacing: 0.5px;
            margin-bottom: 0.75rem;
        }}
        
        .control-button {{
            padding: 0.875rem 0.75rem;
            font-size: 0.85rem;
            margin: 0.125rem;
        }}
        
        .stats-card {{
            padding: 0.75rem;
            margin: 0.25rem 0;
        }}
        
        .session-history {{
            max-height: 250px;
            padding: 0.75rem;
        }}
        
        /* Ensure proper spacing on mobile */
        .stButton > button {{
            width: 100% !important;
            margin: 0.125rem 0 !important;
            min-height: 44px !important;
            font-size: 0.9rem !important;
        }}
        
        /* Improve metric display on mobile */
        .metric-value {{
            font-size: 1.5rem;
        }}
        
        /* Better sidebar on mobile */
        .css-1d391kg {{
            padding: 1rem 0.5rem;
        }}
    }}
    
    /* Very small mobile devices */
    @media (max-width: 480px) {{
        .timer-display {{
            font-size: 2rem;
            margin: 0.25rem 0 1rem 0;
        }}
        
        .session-type {{
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
        }}
        
        .control-button {{
            font-size: 0.8rem;
            padding: 0.75rem 0.5rem;
        }}
        
        .stats-card {{
            padding: 0.5rem;
            font-size: 0.9rem;
        }}
    }}
    
    /* Tablet adjustments */
    @media (min-width: 769px) and (max-width: 1024px) {{
        .timer-display {{
            font-size: 3.5rem;
        }}
        
        .session-type {{
            font-size: 1.3rem;
        }}
    }}
    
    /* Touch-friendly improvements */
    button {{
        touch-action: manipulation;
        -webkit-tap-highlight-color: transparent;
    }}
    
    /* Prevent zoom on input focus for iOS */
    input, select, textarea {{
        font-size: 16px !important;
    }}
    
    /* Smooth scrolling */
    html {{
        scroll-behavior: smooth;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def format_time(seconds):
    """Format seconds into MM:SS format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def main():
    st.set_page_config(
        page_title="Focus Timer Pro",
        page_icon="⏰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    apply_custom_css()
    
    # Sidebar for settings and theme selection
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # Theme selection
        st.subheader("🎨 Theme")
        new_theme = st.selectbox(
            "Choose Theme",
            options=list(THEMES.keys()),
            index=list(THEMES.keys()).index(st.session_state.current_theme)
        )
        if new_theme != st.session_state.current_theme:
            st.session_state.current_theme = new_theme
            st.rerun()
        
        st.divider()
        
        # Timer settings
        st.subheader("⏱️ Timer Settings")
        st.session_state.settings['focus_duration'] = st.slider(
            "Focus Duration (minutes)", 1, 60, st.session_state.settings['focus_duration']
        )
        st.session_state.settings['short_break'] = st.slider(
            "Short Break (minutes)", 1, 30, st.session_state.settings['short_break']
        )
        st.session_state.settings['long_break'] = st.slider(
            "Long Break (minutes)", 1, 60, st.session_state.settings['long_break']
        )
        st.session_state.settings['sessions_until_long_break'] = st.slider(
            "Sessions until Long Break", 2, 10, st.session_state.settings['sessions_until_long_break']
        )
        
        st.divider()
        
        # Auto-start settings
        st.subheader("🔄 Auto-start")
        st.session_state.settings['auto_start_breaks'] = st.checkbox(
            "Auto-start breaks", st.session_state.settings['auto_start_breaks']
        )
        st.session_state.settings['auto_start_focus'] = st.checkbox(
            "Auto-start focus after breaks", st.session_state.settings['auto_start_focus']
        )
        
        st.divider()
        
        # Data export
        st.subheader("📊 Data Export")
        if st.button("Export Session Data"):
            data = st.session_state.data_manager.export_data()
            st.download_button(
                label="Download JSON",
                data=json.dumps(data, indent=2),
                file_name=f"focus_timer_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Main content
    st.title("🎯 Focus Timer Pro")
    st.markdown("*Boost your productivity with customizable focus sessions*")
    
    # Timer display section - responsive layout
    # Use different layouts for mobile vs desktop
    if st.session_state.get('mobile_layout', False) or True:  # Always use mobile-friendly layout
        # Single column layout for better mobile experience
        st.markdown('<div class="timer-container">', unsafe_allow_html=True)
        
        # Session type indicator
        session_type = st.session_state.timer_manager.get_session_type_display()
        st.markdown(f'<div class="session-type">{session_type}</div>', unsafe_allow_html=True)
        
        # Timer display
        remaining_time = st.session_state.timer_manager.get_remaining_time()
        time_display = format_time(remaining_time)
        st.markdown(f'<div class="timer-display">{time_display}</div>', unsafe_allow_html=True)
        
        # Progress bar
        progress = st.session_state.timer_manager.get_progress()
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress * 100}%"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Control buttons - responsive grid
        # Check if we're on mobile for button layout
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            if st.button("▶️ Start", use_container_width=True, key="start_btn"):
                st.session_state.timer_manager.start_timer(st.session_state.settings)
                st.rerun()
            
            if st.button("⏹️ Stop", use_container_width=True, key="stop_btn"):
                st.session_state.timer_manager.stop_timer()
                st.rerun()
        
        with button_col2:
            if st.button("⏸️ Pause", use_container_width=True, key="pause_btn"):
                st.session_state.timer_manager.pause_timer()
                st.rerun()
            
            if st.button("🔄 Reset", use_container_width=True, key="reset_btn"):
                st.session_state.timer_manager.reset_timer()
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics section - responsive layout
    st.divider()
    st.subheader("📈 Today's Progress")
    
    stats = st.session_state.data_manager.get_daily_stats()
    
    # Mobile-friendly metrics layout
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.metric(
            label="Focus Sessions",
            value=stats['focus_sessions'],
            delta=f"+{stats['focus_sessions']} today"
        )
        
        st.metric(
            label="Break Time",
            value=f"{stats['total_break_time']//60}h {stats['total_break_time']%60}m",
            delta=f"+{stats['total_break_time']//60}h today"
        )
    
    with stat_col2:
        st.metric(
            label="Total Focus Time",
            value=f"{stats['total_focus_time']//60}h {stats['total_focus_time']%60}m",
            delta=f"+{stats['total_focus_time']//60}h today"
        )
        
        st.metric(
            label="Productivity Score",
            value=f"{stats['productivity_score']:.1f}%",
            delta=f"Based on {stats['focus_sessions']} sessions"
        )
    
    # Session history
    st.divider()
    st.subheader("📅 Recent Sessions")
    
    history = st.session_state.data_manager.get_recent_sessions(10)
    if history:
        for session in history:
            session_date = datetime.fromisoformat(session['start_time']).strftime("%H:%M")
            duration = session['duration'] // 60
            session_type = session['session_type'].title()
            
            st.markdown(f"""
            <div class="stats-card">
                <strong>{session_date}</strong> - {session_type} Session 
                <span style="float: right;">{duration} minutes</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No sessions completed yet. Start your first focus session!")
    
    # Auto-refresh when timer is running
    if st.session_state.timer_manager.is_running():
        # Update timer state
        session_completed = st.session_state.timer_manager.update()
        
        if session_completed:
            # Log completed session
            st.session_state.data_manager.log_session(
                st.session_state.timer_manager.get_completed_session_data()
            )
            
            # Show completion message
            st.success(f"🎉 {session_type} session completed!")
            
            # Auto-start next session if enabled
            next_session = st.session_state.timer_manager.get_next_session_type()
            if ((next_session in ['short_break', 'long_break'] and st.session_state.settings['auto_start_breaks']) or
                (next_session == 'focus' and st.session_state.settings['auto_start_focus'])):
                st.session_state.timer_manager.start_next_session(st.session_state.settings)
        
        # Refresh every second when running
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()