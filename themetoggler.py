#!/usr/bin/env python3
import concurrent.futures

from settings import THEMES
from theme import ThemeMode
from callback import get_current_mode


def main():
    """Toggle themes between dark and light mode based on systems mode.

    Args:
        themes: List with "registered" themes
    """
    toggled_mode: ThemeMode = get_toggled_mode(get_current_mode(THEMES))
    print('\nSetting themes...')
    # Get toggled mode based on current system mode.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tuple(executor.map(toggle_theme_mode(toggled_mode), THEMES))


def toggle_theme_mode(toggled_mode):
    """Toggle mode for theme."""
    def wrapper(theme):
        theme.mode = toggled_mode
        print(f'{theme.app_name}, {theme.mode}')
        try:
            theme.toggle_callback(theme)
            print(f'{theme.app_name}, {theme.mode}')
        except Exception as e:
            print(f'Unable to set mode for {theme.app_name}: {e}')
    return wrapper


def get_toggled_mode(current_mode: ThemeMode) -> ThemeMode:
    """Get toggled mode based on current mode."""
    return ThemeMode(current_mode == ThemeMode.dark)


if __name__ == "__main__":
    main()
