#!/usr/bin/env python3
import json
import pathlib

from callback import set_terminal_theme, set_vscode_theme
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


def main(themes):
    """Toggle themes between dark and light mode based on systems mode.

    Args:
        themes: List with "registered" themes
    """
    # Get toggled mode based on current system mode.
    toggled_mode = get_toggled_mode(get_current_mode(themes))
    print('\nSetting themes...')

    for theme in themes:
        # Set toggled mode.
        theme.mode = toggled_mode
        theme.toggle_callback(theme)
    if IS_WINDOWS:
        print(f'Setting system theme to: {toggled_mode.name}')
        toggle_mode(toggled_mode)
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
        return get_current_app_mode(themes)


def get_current_app_mode(themes: AppThemes, theme_id: int = 0) -> ThemeMode:
    """Return current app mode.

    Use first theme in themes sequence as reference by default.

    Return light theme by default to toggle to dark theme.
    """
    theme: AppTheme
    try:
        theme = themes[theme_id]
    except (IndexError, TypeError):
        theme = themes[0]

    # Change current mode.
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
        return ThemeMode.light


def get_toggled_mode(current_mode: ThemeMode) -> ThemeMode:
    """Get toggled mode based on current mode."""
    return ThemeMode(current_mode == ThemeMode.dark)


# todo: Implement better solution for toggling system mode and for more
#   platforms.
if IS_WINDOWS:
    def toggle_mode(mode: ThemeMode):
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
    themes: AppThemes = [
        AppTheme(
            option='vscode',
            keys='workbench.colorTheme',
            light_name='Default Light+',
            dark_name='Default Dark+',
            path=pathlib.Path(
                '/mnt/c/Users/magicandcode/AppData/Roaming/Code/User/'
                'settings.json'),
            windows_path=pathlib.Path(
                r'C:\Users\magicandcode\AppData\Roaming\Code\User'
                r'\settings.json'),
            toggle_callback=set_vscode_theme,
        ),
        AppTheme(
            option='terminal',
            keys='profiles:defaults:colorScheme',
            light_name='OneLight',
            dark_name='Dracula',
            path=pathlib.Path(
                '/mnt/c/Users/magicandcode/AppData/Local/Packages/'
                'Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/'
                'settings.json'),
            windows_path=pathlib.Path(
                r'C:\Users\magicandcode\AppData\Local\Packages'
                r'\Microsoft.WindowsTerminal_8wekyb3d8bbwe'
                r'\LocalState\settings.json'),
            toggle_callback=set_terminal_theme,
        ),
    ]
    main(themes)
