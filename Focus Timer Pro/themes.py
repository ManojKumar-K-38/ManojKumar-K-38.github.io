"""
Color themes for the Focus Timer application.
All themes exclude pink colors as per requirements.
"""

THEMES = {
    'Ocean Blue': {
        'primary': '#4A90E2',
        'secondary': '#7BB3F0',
        'accent': '#2E86AB',
        'background': '#F0F4F8',
        'surface': '#FFFFFF',
        'success': '#28A745',
        'warning': '#FFC107',
        'danger': '#DC3545',
        'text': '#2C3E50'
    },
    
    'Forest Green': {
        'primary': '#27AE60',
        'secondary': '#58D68D',
        'accent': '#196F3D',
        'background': '#F1F8E9',
        'surface': '#FFFFFF',
        'success': '#2ECC71',
        'warning': '#F39C12',
        'danger': '#E74C3C',
        'text': '#1B4332'
    },
    
    'Purple Haze': {
        'primary': '#8E44AD',
        'secondary': '#BB8FCE',
        'accent': '#5B2C6F',
        'background': '#F4F1FB',
        'surface': '#FFFFFF',
        'success': '#27AE60',
        'warning': '#F39C12',
        'danger': '#E74C3C',
        'text': '#4A235A'
    },
    
    'Sunset Orange': {
        'primary': '#E67E22',
        'secondary': '#F5B041',
        'accent': '#D35400',
        'background': '#FDF2E9',
        'surface': '#FFFFFF',
        'success': '#27AE60',
        'warning': '#F39C12',
        'danger': '#E74C3C',
        'text': '#A04000'
    },
    
    'Midnight Dark': {
        'primary': '#3498DB',
        'secondary': '#85C1E9',
        'accent': '#2980B9',
        'background': '#2C3E50',
        'surface': '#34495E',
        'success': '#27AE60',
        'warning': '#F39C12',
        'danger': '#E74C3C',
        'text': '#ECF0F1'
    },
    
    'Earth Tones': {
        'primary': '#8D6E63',
        'secondary': '#BCAAA4',
        'accent': '#5D4037',
        'background': '#F5F5DC',
        'surface': '#FFFFFF',
        'success': '#689F38',
        'warning': '#FF8F00',
        'danger': '#D32F2F',
        'text': '#3E2723'
    },
    
    'Arctic Blue': {
        'primary': '#00ACC1',
        'secondary': '#4DD0E1',
        'accent': '#0097A7',
        'background': '#E0F2F1',
        'surface': '#FFFFFF',
        'success': '#00C853',
        'warning': '#FFB300',
        'danger': '#D50000',
        'text': '#004D40'
    },
    
    'Monochrome': {
        'primary': '#424242',
        'secondary': '#757575',
        'accent': '#212121',
        'background': '#FAFAFA',
        'surface': '#FFFFFF',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'danger': '#F44336',
        'text': '#212121'
    }
}

def get_theme_colors(theme_name: str) -> dict:
    """Get color scheme for a specific theme"""
    return THEMES.get(theme_name, THEMES['Ocean Blue'])

def get_available_themes() -> list:
    """Get list of available theme names"""
    return list(THEMES.keys())

def validate_theme(theme_name: str) -> bool:
    """Check if theme name is valid"""
    return theme_name in THEMES
