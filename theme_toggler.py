#!/usr/bin/env python3
import json

from settings import THEMES
from theme import AppTheme, AppThemes, ThemeMode


# todo: Check platform.
try:
    import winreg
except ModuleNotFoundError:
    IS_WINDOWS = False
else:
    IS_WINDOWS = True

# Windows Registry key for personalisation settings of current user.
CURRENT_USER_PERSONALIZE_KEY: str = (r'SOFTWARE\Microsoft\Windows'
                                     r'\CurrentVersion\Themes\Personalize')


def main():
    """Toggle themes between dark and light mode based on systems mode.

    Args:
        themes: List with "registered" themes
    """
    # Get toggled mode based on current system mode.
    toggled_mode = get_toggled_mode(get_current_mode(THEMES))
    print('\nSetting themes...')

    for theme in THEMES:
        # Set toggled mode.
        theme.mode = toggled_mode
        theme.toggle_callback(theme)
    if IS_WINDOWS:
        print(f'Setting system theme to: {toggled_mode.name}')
        toggle_system_mode(toggled_mode)
    print()


def get_current_mode(themes: AppThemes) -> ThemeMode:
    """Get current mode based on reference key."""
    try:
        # todo: Check platform and add more platforms.
        with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                CURRENT_USER_PERSONALIZE_KEY,
                access=winreg.KEY_READ) as hkey:
            return (ThemeMode.light
                    if winreg.QueryValueEx(hkey, 'AppsUseLightTheme')[0]
                    else ThemeMode.dark)
    except Exception:
        # Get current theme based on app mode as fallback.
        return get_current_app_mode(themes)


def get_current_app_mode(themes: AppThemes, theme_id: int = 0) -> ThemeMode:
    """Return current app mode.

    Use first theme in themes sequence as reference by default.

    Return light theme by default to toggle to dark theme; the theme
      will be changed to the opposite theme of what this returns.
    """
    # Get first theme, if this fails there's no use to continue the
    #   program so it's ok to have an exception.
    # todo: Catch exception to display a more clear error message?
    theme: AppTheme = themes[0]
    try:
        theme = themes[theme_id]
    except (IndexError, TypeError):
        pass

    # Get current mode.
    path = theme.path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            pass
    except FileNotFoundError:
        path = theme.windows_path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            return theme.modes(settings[theme.keys] == theme.light_name)
    except Exception:
        # Fallback to light theme mode.
        return ThemeMode.light


def get_toggled_mode(current_mode: ThemeMode) -> ThemeMode:
    """Get toggled mode based on current mode."""
    return ThemeMode(current_mode == ThemeMode.dark)


# todo: Implement better solution for toggling system mode and for more
#   platforms.
if IS_WINDOWS:
    def toggle_system_mode(mode: ThemeMode):
        """Toggle apps and system mode."""
        with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                CURRENT_USER_PERSONALIZE_KEY,
                access=winreg.KEY_ALL_ACCESS) as hkey:
            # Change mode for both apps and system theme to sync mode.
            winreg.SetValueEx(
                hkey, 'AppsUseLightTheme', 0, winreg.REG_DWORD, mode.value)
            winreg.SetValueEx(
                hkey, 'SystemUsesLightTheme', 0, winreg.REG_DWORD, mode.value)


if __name__ == "__main__":
    main()
