"""
Cipher v2 Theme

Centralized design system.
Do not hardcode colors inside widgets.
"""
from pathlib import Path
# --------------------------------------------------
# Theme Manager
# --------------------------------------------------

CURRENT_THEME = "dark"

CURRENT_ACCENT = "Blue"

_registered_widgets = set()

def refresh_theme() -> None:
    """
    Public API to refresh all registered widgets
    without changing the current theme.
    """

    _refresh_registered_widgets()

def _refresh_registered_widgets() -> None:
    """
    Refresh all registered widgets after a theme,
    accent or font change.
    """

    for widget in list(_registered_widgets):

        try:

            if hasattr(widget, "apply_theme"):
                widget.apply_theme()

        except RuntimeError:

            _registered_widgets.discard(widget)

ACCENTS = {
    "Blue": {
        "PRIMARY": "#4F8CFF",
        "PRIMARY_HOVER": "#6AA5FF",
        "PRIMARY_PRESSED": "#3478F6",
    },
    "Green": {
        "PRIMARY": "#22C55E",
        "PRIMARY_HOVER": "#4ADE80",
        "PRIMARY_PRESSED": "#16A34A",
    },
    "Purple": {
        "PRIMARY": "#8B5CF6",
        "PRIMARY_HOVER": "#A78BFA",
        "PRIMARY_PRESSED": "#7C3AED",
    },
    "Orange": {
        "PRIMARY": "#F97316",
        "PRIMARY_HOVER": "#FB923C",
        "PRIMARY_PRESSED": "#EA580C",
    },
    "Red": {
        "PRIMARY": "#EF4444",
        "PRIMARY_HOVER": "#F87171",
        "PRIMARY_PRESSED": "#DC2626",
    },

}

THEMES = {

    "dark": {
        "BACKGROUND": "#111827",
        "SURFACE": "#1F2937",
        "SURFACE_LIGHT": "#374151",
        "TEXT": "#F9FAFB",
        "TEXT_MUTED": "#9CA3AF",
        "BORDER": "#374151",
    },

    "light": {
        "BACKGROUND": "#F8FAFC",
        "SURFACE": "#FFFFFF",
        "SURFACE_LIGHT": "#F1F5F9",
        "TEXT": "#111827",
        "TEXT_MUTED": "#64748B",
        "BORDER": "#CBD5E1",
    },

    "midnight": {
        "BACKGROUND": "#050816",
        "SURFACE": "#111827",
        "SURFACE_LIGHT": "#1E293B",
        "TEXT": "#E2E8F0",
        "TEXT_MUTED": "#94A3B8",
        "BORDER": "#334155",
    },

    "cyber": {
        "BACKGROUND": "#0B0F19",
        "SURFACE": "#121826",
        "SURFACE_LIGHT": "#1A2335",
        "TEXT": "#00FFD5",
        "TEXT_MUTED": "#57F3D8",
        "BORDER": "#00FFD5",
    },

}

# --------------------------------------------------
# Colors
# --------------------------------------------------

BACKGROUND = THEMES[CURRENT_THEME]["BACKGROUND"]
SURFACE = THEMES[CURRENT_THEME]["SURFACE"]
SURFACE_LIGHT = THEMES[CURRENT_THEME]["SURFACE_LIGHT"]

PRIMARY = ACCENTS[CURRENT_ACCENT]["PRIMARY"]
PRIMARY_HOVER = ACCENTS[CURRENT_ACCENT]["PRIMARY_HOVER"]
PRIMARY_PRESSED = ACCENTS[CURRENT_ACCENT]["PRIMARY_PRESSED"]

PRIMARY_OVERLAY = "rgba(79, 140, 255, 0.15)"
PRIMARY_OVERLAY_HOVER = "rgba(79, 140, 255, 0.25)"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
ERROR = "#EF4444"

TEXT = THEMES[CURRENT_THEME]["TEXT"]
TEXT_MUTED = THEMES[CURRENT_THEME]["TEXT_MUTED"]
TEXT_SECONDARY = TEXT_MUTED

BORDER = THEMES[CURRENT_THEME]["BORDER"]

USER_BUBBLE = "#2563EB"
ASSISTANT_BUBBLE = "#1E293B"
SYSTEM_BUBBLE = "#14532D"

CODE_BACKGROUND = "#111827"



# --------------------------------------------------
# Status Badge Colors
# --------------------------------------------------

STATUS_ONLINE_BG = "#166534"
STATUS_OFFLINE_BG = "#7C2D12"
STATUS_LISTENING_BG = "#2563EB"
STATUS_THINKING_BG = "#7C3AED"
STATUS_SPEAKING_BG = "#EA580C"
STATUS_READY_BG = "#14532D"
STATUS_THINKING_TEXT = "#C084FC"
STATUS_SPEAKING_TEXT = "#FB923C"


ACTION_BUTTON = f"""
QPushButton {{
    background:{PRIMARY};
    color:white;
    border:none;
    border-radius:10px;
    padding:12px;
}}

QPushButton:hover {{
    background:{PRIMARY_HOVER};
}}
"""
# --------------------------------------------------
# Radius
# --------------------------------------------------

RADIUS_SMALL = 8
RADIUS = 14
RADIUS_LARGE = 16

# --------------------------------------------------
# Fonts
# --------------------------------------------------

FONT = "Segoe UI"

FONT_SIZES = {
    "Small": {
        "TITLE": 20,
        "HEADER": 15,
        "TEXT": 10,
        "SMALL": 9,
    },
    "Medium": {
        "TITLE": 22,
        "HEADER": 16,
        "TEXT": 11,
        "SMALL": 10,
    },
    "Large": {
        "TITLE": 24,
        "HEADER": 18,
        "TEXT": 12,
        "SMALL": 11,
    },
}

CURRENT_FONT_SIZE = "Medium"

TITLE_SIZE = FONT_SIZES[CURRENT_FONT_SIZE]["TITLE"]
HEADER_SIZE = FONT_SIZES[CURRENT_FONT_SIZE]["HEADER"]
TEXT_SIZE = FONT_SIZES[CURRENT_FONT_SIZE]["TEXT"]
SMALL_SIZE = FONT_SIZES[CURRENT_FONT_SIZE]["SMALL"]


# --------------------------------------------------
# Layout
# --------------------------------------------------

HEADER_HEIGHT = 72

SIDEBAR_WIDTH = 215
CHAT_SIDEBAR_WIDTH = 260

CONTENT_MARGIN = 15


# --------------------------------------------------
# Spacing
# --------------------------------------------------

SPACING_XS = 4
SPACING_SMALL = 8
SPACING = 12
SPACING_LARGE = 16
SPACING_XL = 24
SPACING_XXL = 32

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 760

# --------------------------------------------------
# UI Scale
# --------------------------------------------------

UI_SCALES = {
    "100%": 1.00,
    "125%": 1.25,
    "150%": 1.50,
    "175%": 1.75,
    "200%": 2.00,
}

CURRENT_UI_SCALE = "100%"
SCALE_FACTOR = UI_SCALES[CURRENT_UI_SCALE]

def scale(value: int | float) -> int:
    return int(round(value * SCALE_FACTOR))

# --------------------------------------------------
# Widget Sizes
# --------------------------------------------------
INPUT_PANEL = 48

BASE_BUTTON_HEIGHT = 42
BUTTON_HEIGHT = scale(BASE_BUTTON_HEIGHT)

BASE_ICON_SMALL = 16
ICON_SMALL = scale(BASE_ICON_SMALL)

BASE_ICON_MEDIUM = 20
ICON_MEDIUM = scale(BASE_ICON_MEDIUM)

BASE_ICON_LARGE = 24
ICON_LARGE = scale(BASE_ICON_LARGE)

STATUS_BADGE_HEIGHT = 32


# --------------------------------------------------
# Cards
# --------------------------------------------------

CARD_RADIUS = 18
BASE_CARD_PADDING = 16
CARD_PADDING = scale(BASE_CARD_PADDING)


# --------------------------------------------------
# Animation
# --------------------------------------------------

ANIMATION_SPEEDS = {
    "Slow": 300,
    "Normal": 200,
    "Fast": 100,
    "Instant": 0,
}

CURRENT_ANIMATION = "Normal"

ANIMATION_DURATION = ANIMATION_SPEEDS[CURRENT_ANIMATION]


# --------------------------------------------------
# Shadows
# --------------------------------------------------

SHADOW_BLUR = 24
SHADOW_ALPHA = 90

# --------------------------------------------------
# Hover Animation
# --------------------------------------------------

HOVER_DURATION = 150

# --------------------------------------------------
# Opacity
# --------------------------------------------------

DISABLED_OPACITY = 0.55

# --------------------------------------------------
# Icon Colors
# --------------------------------------------------

ICON_COLOR = "#CBD5E1"
ICON_ACTIVE = PRIMARY

# --------------------------------------------------
# Selection
# --------------------------------------------------

SELECTION = PRIMARY
def get_card_style():

    return f"""
QFrame {{
    background:{SURFACE};
    border:1px solid {BORDER};
    border-radius:{CARD_RADIUS}px;
}}

QFrame#Card:hover {{
    border:1px solid {PRIMARY};
    background:{SURFACE_LIGHT};
}}
"""

def get_button_style():

    return f"""
QPushButton {{
    background:{PRIMARY};
    color:white;
    border:1px solid rgba(255,255,255,0.08);
    border-radius:{RADIUS}px;
    min-height:{BUTTON_HEIGHT}px;
    padding:0px 18px;
    font-size:10.5pt;
    font-weight:600;
}}

QPushButton:hover {{
    background:{PRIMARY_HOVER};
    border:1px solid rgba(255,255,255,0.16);
}}

QPushButton:pressed {{
    background:{PRIMARY_PRESSED};
}}

QPushButton:disabled {{
    background:rgba(255,255,255,0.08);
    color:rgba(255,255,255,0.45);
}}
"""
def get_input_style():

    return f"""
QLineEdit {{
    background:{CODE_BACKGROUND};
    color:{TEXT};
    border:1px solid {BORDER};
    border-radius:{RADIUS}px;
    padding:10px;
}}

QLineEdit:focus {{
    border:1px solid {PRIMARY};
}}
"""

def get_combobox_style():

    return f"""
QComboBox {{
    background:{CODE_BACKGROUND};
    color:{TEXT};
    border:1px solid {BORDER};
    border-radius:{RADIUS}px;
    padding:8px;
}}

QComboBox:hover {{
    border:1px solid {PRIMARY};
}}

QComboBox:focus {{
    border:1px solid {PRIMARY};
}}
"""

SCROLLBAR_STYLE = f"""
QScrollBar:vertical {{
    background:transparent;
    width:10px;
    margin:4px;
}}

QScrollBar::handle:vertical {{
    background:{SURFACE_LIGHT};
    border-radius:5px;
}}

QScrollBar::handle:vertical:hover {{
    background:{PRIMARY};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height:0;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background:none;
}}
"""

LIST_WIDGET_STYLE = f"""
QListWidget {{
    background:{SURFACE};
    border:1px solid {BORDER};
    border-radius:{CARD_RADIUS}px;
    color:{TEXT};
    outline:none;
}}

QListWidget::item {{
    padding:12px;
    border-radius:10px;
}}

QListWidget::item:selected {{
    background:{PRIMARY};
}}

QListWidget::item:hover {{
    background:{SURFACE_LIGHT};
}}
"""

CHECKBOX_STYLE = f"""
QCheckBox {{
    color:{TEXT};
    spacing:10px;
}}

QCheckBox::indicator {{
    width:18px;
    height:18px;
}}

QCheckBox::indicator:unchecked {{
    border:2px solid {BORDER};
    border-radius:5px;
    background:{CODE_BACKGROUND};
}}

QCheckBox::indicator:checked {{
    background:{PRIMARY};
    border:2px solid {PRIMARY};
}}
"""

GROUPBOX_STYLE = f"""
QGroupBox {{
    border:1px solid {BORDER};
    border-radius:{CARD_RADIUS}px;
    margin-top:12px;
    padding:18px;
    background:{SURFACE};
    font-weight:bold;
    color:{TEXT};
}}

QGroupBox::title {{
    subcontrol-origin:margin;
    left:16px;
    padding:0 6px;
}}
"""

STATUS_BADGE_STYLE = f"""
padding:8px 18px;
border-radius:14px;
font-weight:bold;
"""

def get_page_title_style():

    return f"""
font-size:{TITLE_SIZE}px;
font-weight:700;
color:{TEXT};
"""

PAGE_SUBTITLE_STYLE = f"""
font-size:11pt;
color:{TEXT_MUTED};
"""

INPUT_DIALOG_STYLE = f"""
QInputDialog {{
    background:{BACKGROUND};
}}

QLabel {{
    color:{TEXT};
}}

QLineEdit {{
    background:{SURFACE};
    color:{TEXT};
    border:1px solid {BORDER};
    border-radius:6px;
    padding:6px;
}}

QPushButton {{
    background:{PRIMARY};
    color:white;
    border:none;
    border-radius:6px;
    padding:6px 12px;
}}

QPushButton:hover {{
    background:{PRIMARY_HOVER};
}}
"""


MESSAGE_BOX_STYLE = f"""
QMessageBox {{
    background:{BACKGROUND};
}}

QLabel {{
    color:{TEXT};
    font-size:11pt;
}}

QPushButton {{
    background:{PRIMARY};
    color:white;
    border:none;
    border-radius:6px;
    padding:6px 16px;
    min-width:80px;
}}

QPushButton:hover {{
    background:{PRIMARY_HOVER};
}}

QPushButton:pressed {{
    background:{PRIMARY_HOVER};
}}
"""

SECTION_GAP = 24
CARD_GAP = 16

AVATAR_SIZE = 42

CHAT_BUBBLE_RADIUS = 18
CHAT_BUBBLE_PADDING = 14

CLICK_CURSOR = "PointingHandCursor"

ENABLE_ANIMATION = True
ENABLE_SHADOW = True
ENABLE_BLUR = False

ACCESSIBILITY = {
    "high_contrast": False,
    "reduced_motion": False,
    "large_click_targets": False,
}

def set_theme(theme: str) -> None:
    """
    Change active theme.
    """

    global CURRENT_THEME
    global BACKGROUND
    global SURFACE
    global SURFACE_LIGHT
    global PRIMARY
    global PRIMARY_HOVER
    global PRIMARY_PRESSED
    global TEXT
    global TEXT_SECONDARY
    global TEXT_MUTED
    global BORDER

    if theme not in THEMES:
        return

    
    palette = THEMES[theme]


    BACKGROUND = palette["BACKGROUND"]
    SURFACE = palette["SURFACE"]
    SURFACE_LIGHT = palette["SURFACE_LIGHT"]
    TEXT = palette["TEXT"]
    TEXT_MUTED = palette["TEXT_MUTED"]
    BORDER = palette["BORDER"]

    CURRENT_THEME = theme

    _refresh_registered_widgets()

def register_widget(widget):
    """
    Register a widget for theme refresh.
    """

    if widget is not None:
        _registered_widgets.add(widget)


def unregister_widget(widget):
    """
    Remove widget from theme refresh.
    """

    _registered_widgets.discard(widget)

def set_accent(accent: str) -> None:
    """
    Change the active accent color.
    """

    global CURRENT_ACCENT
    global PRIMARY
    global PRIMARY_HOVER
    global PRIMARY_PRESSED
    global ICON_ACTIVE
    global SELECTION

    if accent not in ACCENTS:
        return

    CURRENT_ACCENT = accent

    palette = ACCENTS[accent]

    PRIMARY = palette["PRIMARY"]
    PRIMARY_HOVER = palette["PRIMARY_HOVER"]
    PRIMARY_PRESSED = palette["PRIMARY_PRESSED"]

    ICON_ACTIVE = PRIMARY
    SELECTION = PRIMARY

    _refresh_registered_widgets()

def set_font_size(size: str) -> None:
    """
    Apply global font size preset.
    """

    global CURRENT_FONT_SIZE
    global TITLE_SIZE
    global HEADER_SIZE
    global TEXT_SIZE
    global SMALL_SIZE

    if size not in FONT_SIZES:
        return

    CURRENT_FONT_SIZE = size

    preset = FONT_SIZES[size]

    TITLE_SIZE = preset["TITLE"]
    HEADER_SIZE = preset["HEADER"]
    TEXT_SIZE = preset["TEXT"]
    SMALL_SIZE = preset["SMALL"]

    _refresh_registered_widgets()

def set_ui_scale(scale_name: str) -> None:
    """
    Apply UI scale preset.
    """

    global CURRENT_UI_SCALE
    global SCALE_FACTOR

    if scale_name not in UI_SCALES:
        return

    CURRENT_UI_SCALE = scale_name
    SCALE_FACTOR = UI_SCALES[scale_name]

    global CARD_PADDING
    global BUTTON_HEIGHT
    global ICON_SMALL
    global ICON_MEDIUM
    global ICON_LARGE

    CARD_PADDING = scale(BASE_CARD_PADDING)
    BUTTON_HEIGHT = scale(BASE_BUTTON_HEIGHT)

    ICON_SMALL = scale(BASE_ICON_SMALL)
    ICON_MEDIUM = scale(BASE_ICON_MEDIUM)
    ICON_LARGE = scale(BASE_ICON_LARGE)

    _refresh_registered_widgets()

def set_animation_speed(speed: str) -> None:
    """
    Apply animation speed preset.
    """

    global CURRENT_ANIMATION
    global ANIMATION_DURATION

    if speed not in ANIMATION_SPEEDS:
        return

    CURRENT_ANIMATION = speed
    ANIMATION_DURATION = ANIMATION_SPEEDS[speed]

    _refresh_registered_widgets()

def set_accessibility(
    *,
    high_contrast: bool | None = None,
    reduced_motion: bool | None = None,
    large_click_targets: bool | None = None,
) -> None:
    """
    Apply accessibility preferences.
    """

    global ENABLE_ANIMATION

    if high_contrast is not None:
        ACCESSIBILITY["high_contrast"] = high_contrast

    if reduced_motion is not None:
        ACCESSIBILITY["reduced_motion"] = reduced_motion
        ENABLE_ANIMATION = not reduced_motion

    if large_click_targets is not None:
        ACCESSIBILITY["large_click_targets"] = large_click_targets

    _refresh_registered_widgets()

CUSTOM_STYLESHEET = ""

def load_custom_stylesheet(path: str | Path) -> bool:
    """
    Load a user supplied QSS stylesheet.
    """

    global CUSTOM_STYLESHEET

    try:
        CUSTOM_STYLESHEET = Path(path).read_text(
            encoding="utf-8"
        )

        _refresh_registered_widgets()
        return True

    except Exception:
        CUSTOM_STYLESHEET = ""
        return False