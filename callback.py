import json
# todo: Check platform.
try:
    import winreg
except ModuleNotFoundError:
    IS_WINDOWS = False
else:
    IS_WINDOWS = True

from theme import AppTheme, AppThemes, ThemeMode


# Windows Registry key for personalisation settings of current user.
CURRENT_USER_PERSONALIZE_KEY: str = (
    r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')


def set_vscode_theme(theme: AppTheme):
    """Set theme mode for VS Code.

    Open JSON settings and update the dictionary, setting opposite
      theme mode.

    Args:
        theme (AppTheme): App theme for VS Code
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
            try:
                settings = json.load(f)
            except json.JSONDecodeError as e:
                raise e
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
        # Catch any exception to allow the script to continue running to
        #   set theme mode for other apps even if this app fails.
        print('Failed to set VSCode theme.')
        print(repr(e))


def set_terminal_theme(theme: AppTheme):
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
            toggled_theme_name = theme.names[theme.mode == theme.modes.light]

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
        # Catch any exception to allow the script to continue running to
        #   set theme mode for other apps even if this app fails.
        print('Failed to set Terminal theme.')
        print(repr(e))


def toggle_system_mode(mode: ThemeMode) -> bool:
    """Toggle apps and system mode."""
    try:
        with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                CURRENT_USER_PERSONALIZE_KEY,
                access=winreg.KEY_ALL_ACCESS) as hkey:
            # Change mode for both apps and system theme to sync mode.
            winreg.SetValueEx(
                hkey, 'AppsUseLightTheme', 0, winreg.REG_DWORD, mode.value)
            winreg.SetValueEx(
                hkey, 'SystemUsesLightTheme', 0, winreg.REG_DWORD, mode.value)
            return True
    except Exception:
        return False


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
