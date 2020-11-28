from dataclasses import dataclass
from enum import Enum
import pathlib
from typing import Callable, Sequence


class ThemeMode(Enum):
    """Represents the two modes of a theme, dark and light."""
    dark: int = 0
    light: int = 1


@dataclass
class AppTheme:
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
    mode: ThemeMode = ThemeMode.light  # Set default mode
    settings_delimiter: str = ':'
    modes: Enum = ThemeMode

    @property
    def names(self):
        """Return names of dark and light themes for application."""
        return self.dark_name, self.light_name


# Type alias to simplify themes typing.
AppThemes = Sequence[AppTheme]
