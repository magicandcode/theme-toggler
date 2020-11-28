import pathlib

from callback import set_terminal_theme, set_vscode_theme, toggle_system_mode
from theme import AppTheme, AppThemes


THEMES: AppThemes = [
        AppTheme(
            app_name='vscode',
            keys='workbench.colorTheme',
            light_name='Default Light+',
            dark_name='Default Dark+',
            path=pathlib.Path(
                '/Users/magicandcode/Library/Application Support/Code/User/'
                'settings.json'
                # todo: Use paths tuple and try to use any
                # '/mnt/c/Users/magicandcode/AppData/Roaming/Code/User/'
                # 'settings.json'
                ),
            windows_path=pathlib.Path(
                r'C:\Users\magicandcode\AppData\Roaming\Code\User'
                r'\settings.json'),
            toggle_callback=set_vscode_theme,
        ),
        AppTheme(
            app_name='terminal',
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
        AppTheme(
            app_name='system',
            keys=None,
            light_name=None,
            dark_name=None,
            path=None,
            windows_path=None,
            toggle_callback=toggle_system_mode,
        ),
    ]
