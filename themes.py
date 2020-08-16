#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum
import json
import pathlib
import sys
from typing import Callable


class ThemeMode(Enum):
    dark: str = 'dark'
    light: str = 'light'


DEFAULT_MODE: ThemeMode = ThemeMode.dark


@dataclass
class ApplicationTheme:
    option: str
    settings_name: str
    light_name: str
    dark_name: str
    path: pathlib.Path
    toggle_callback: Callable
    mode: ThemeMode = DEFAULT_MODE
    settings_delimiter: str = ':'


def main(themes, args):
    mode = args[0] if args else DEFAULT_MODE
    mode = mode if mode in ThemeMode else DEFAULT_MODE
    for theme in themes:
        # Set toggled mode.
        theme.mode = mode
        theme.toggle_callback(theme)


def toggle_vscode_theme(theme: ApplicationTheme):
    print('toggle vscode theme')
    # Change current mode.
    try:
        with open(theme.path, 'r+', encoding='utf-8') as f:
            settings = json.load(f)
            f.seek(0)
            f.truncate()
            current_theme_name = settings[theme.settings_name]
            new_theme_name = (theme.light_name
                             if current_theme_name == theme.dark_name
                             else theme.dark_name)
            theme.mode = ThemeMode.light if theme.mode is ThemeMode.dark else ThemeMode.dark
            settings[theme.settings_name] = new_theme_name
            json.dump(settings, f, indent=2, separators=(', ', ': '))

        print('Set VSCode theme to:', new_theme_name)
    except Exception as e:
        print('Failed to set VSCode theme')
        print(repr(e))


def toggle_terminal_theme(theme: ApplicationTheme, mode: str = 'dark'):
    print('toggle terminal theme')
    # Change current mode.
    try:
        with open(theme.path, 'r+', encoding='utf-8') as f:
            settings_string = ''
            key = theme.settings_name.split(':')[-1]
            # Search for line with key.
            current_theme_name = ''
            for line in f:
                if key in line and not current_theme_name:
                    # Replace current theme with toggled theme.
                    current_theme_name = (theme.light_name
                                     if theme.light_name in line
                                     else theme.dark_name)
                    new_theme_name = (theme.light_name
                                      if current_theme_name == theme.dark_name
                                      else theme.dark_name) 
                    line = line.replace(current_theme_name, new_theme_name)
                settings_string += line
            f.seek(0)
            f.truncate()
            # Write new settings to file.
            f.write(settings_string)
            theme.mode = ThemeMode.light if theme.mode is ThemeMode.dark else ThemeMode.dark

        print('Set Terminal theme to:', new_theme_name)
    except Exception as e:
        print('Failed to set Terminal theme')
        print(repr(e))


if __name__ == "__main__":
    themes = [
        ApplicationTheme(
            option='vscode',
            settings_name='workbench.colorTheme',
            light_name='Default Light+',
            dark_name='Default Dark+',
            path=pathlib.Path(
                '/mnt/c/Users/magicandcode/AppData/Roaming/Code/User/settings.json'),
            toggle_callback=toggle_vscode_theme,
        ),
        ApplicationTheme(
            option='terminal',
            settings_name='profiles:defaults:colorScheme',
            light_name='OneLight',
            dark_name='Dracula',
            path=pathlib.Path(
                '/mnt/c/Users/magicandcode/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json'),
            toggle_callback=toggle_terminal_theme,
        ),
    ]
    main(themes, sys.argv[1:])

# export PATH=$PATH":/mnt/c/Users/magicandcode/.local/bin/"
# cp themes.py /mnt/c/Users/magicandcode/.local/bin/themes
