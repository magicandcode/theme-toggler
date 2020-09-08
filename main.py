#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum
import json
import pathlib
from typing import Callable
# todo: Check platform.
try:
    import winreg
except ModuleNotFoundError:
    IS_WINDOWS = False
else:
    IS_WINDOWS = True


class ThemeMode(Enum):
    """Represents the two modes of a theme."""
    dark: int = 0
    light: int = 1


@dataclass
class ApplicationTheme:
    """Represents the theme of an application.

    Set separate path for each supported platform to enable
    cross-platform and cross-device compatability.
    """
    option: str
    keys: str
    light_name: str
    dark_name: str
    path: pathlib.Path
    windows_path: pathlib.Path
    toggle_callback: Callable
    mode: ThemeMode = ThemeMode.dark
    settings_delimiter: str = ':'
    modes = ThemeMode.dark, ThemeMode.light

    @property
    def names(self):
        """Return names of dark and light themes for application."""
        return self.dark_name, self.light_name


def main(themes):
    """Toggle themes between dark and light mode based on systems mode.

    Args:
        themes: List with "registered" themes
    """
    # Get toggled mode based on current system mode.
    toggled_mode = get_toggled_mode(get_current_mode())
    print('\nSetting themes...')

    for theme in themes:
        # Set toggled mode.
        theme.mode = toggled_mode
        theme.toggle_callback(theme)
    if IS_WINDOWS:
        print(f'Setting system theme to: {toggled_mode.name}')
        toggle_mode(toggled_mode)
    print()


def set_vscode_theme(theme: ApplicationTheme):
    # Change current mode.
    path = theme.path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            pass
    except FileNotFoundError:
        path = theme.windows_path
    try:
        with open(path, 'r+', encoding='utf-8') as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                raise
            else:
                # Create new key or override previous value.  Ignore
                #   checking if the value is already correct, faster to
                #   just set it.  Get theme name from mode.
                settings[theme.keys] = theme.names[theme.mode.value]

                # Only truncate file if the content can be loaded, else
                #   there is risk of losing all existing settings if
                #   the script raises an error after truncating.
                f.seek(0)
                f.truncate()
                json.dump(settings, f, indent=2, separators=(', ', ': '))

            print('Set VSCode theme to:', settings[theme.keys])
    except Exception as e:
        # Catch exception to allow the script to run for other apps
        #   even if one fails to set a theme.
        print('Failed to set VSCode theme.')
        print(repr(e))


def set_terminal_theme(theme: ApplicationTheme):
    """Set theme by replacing theme name in string.

    Unable to load settings as JSON since it contains comments.
    """
    # Change current mode.
    path = theme.path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            pass
    except FileNotFoundError:
        path = theme.windows_path
    try:
        with open(path, 'r+', encoding='utf-8') as f:
            settings_string = ''
            key = theme.keys.split(theme.settings_delimiter)[-1]
            toggled_theme_name = theme.names[theme.mode == ThemeMode.light]

            # Search for line with key.
            current_theme_name = ''
            for line in f:
                if not current_theme_name and key in line and any(
                    name in line for name in theme.names
                ):
                    # Replace current theme with toggled theme.
                    #   Requires that theme name is either dark or
                    #   light theme.  Else keep "invalid" theme rather
                    #   than raising an exception.
                    current_theme_name = theme.names[theme.light_name in line]
                    line = line.replace(current_theme_name, toggled_theme_name)
                settings_string += line
            if current_theme_name:
                f.seek(0)
                f.truncate()
                # Write new settings to file.
                f.write(settings_string)

                print('Set Terminal theme to:', toggled_theme_name)
            else:
                raise ValueError(
                    'Failed to find valid current theme for Terminal.')
    except Exception as e:
        print('Failed to set Terminal theme.')
        print(repr(e))


def get_current_mode() -> ThemeMode:
    """Get current mode based on reference key."""
    try:
        # test:
        assert False
        # todo: Check platform and add more platforms.
        with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes'
                 r'\Personalize'),
                access=winreg.KEY_READ) as hkey:
            return (ThemeMode.light
                    if winreg.QueryValueEx(hkey, 'AppsUseLightTheme')[0]
                    else ThemeMode.dark)
    except Exception:
        return get_current_app_mode()


def get_current_app_mode() -> ThemeMode:
    """Return current app mode.

    Return light theme by default to toggle to dark theme.
    """
    theme: ApplicationTheme = themes[0]

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
            return theme.modes[settings[theme.keys] == theme.light_name]
    except Exception:
        return ThemeMode.light


def get_toggled_mode(current_mode: ThemeMode) -> ThemeMode:
    """Get toggled mode based on current mode."""
    return (ThemeMode.light
            if current_mode == ThemeMode.dark else ThemeMode.dark)


# todo: Implement better solution for toggling system mode and for more
#   platforms.
if IS_WINDOWS:
    def toggle_mode(mode: ThemeMode):
        """Toggle apps and system mode."""
        with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes'
                 r'\Personalize'),
                access=winreg.KEY_ALL_ACCESS) as hkey:
            # Change mode for both apps and system theme to sync mode.
            winreg.SetValueEx(
                hkey, 'AppsUseLightTheme', 0, winreg.REG_DWORD, mode.value)
            winreg.SetValueEx(
                hkey, 'SystemUsesLightTheme', 0, winreg.REG_DWORD, mode.value)


if __name__ == "__main__":
    themes = [
        ApplicationTheme(
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
        ApplicationTheme(
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
