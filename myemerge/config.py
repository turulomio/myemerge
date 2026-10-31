"""Configuration module for myemerge.

Manages loading, creating, and validating settings stored in
`/etc/myemerge/myemerge.ini`.
"""

from pathlib import Path
from colorama import Fore, Style
from configparser_rb.core import ConfigParserRB
from pycpufreq import sys_get_cpu_max_freq
from myemerge.gettext import _

DEFAULT_CONFIG_PATH = Path('/etc/myemerge/myemerge.ini')


class Config:
    """Represents the myemerge configuration."""

    def __init__(self, filename: Path | str = DEFAULT_CONFIG_PATH):
        self.filename = Path(filename)
        self.parser = ConfigParserRB(str(self.filename))
        self._load()

    def _load(self):
        """Loads or creates the configuration file and verifies permissions."""
        # Use existing value in config if present; default to current max freq
        self.parser.get('cpupower', 'cpu_hz', sys_get_cpu_max_freq())
        self.parser.get('ccache', 'use', 'False')

        if not self.filename.exists():
            self.parser.save()
            try:
                self.filename.chmod(0o644)
            except OSError:
                pass
            print(Style.BRIGHT + Fore.GREEN + _("Your '{0}' config file has been created. You can change your settings editing it.").format(self.filename) + Style.RESET_ALL)
        else:
            self._check_permissions()

    def _check_permissions(self):
        """Warns if the config file has insecure permissions or ownership."""
        try:
            file_stat = self.filename.stat()
            file_mode = file_stat.st_mode & 0o777
            if file_mode & 0o022 != 0:
                print(Style.BRIGHT + Fore.YELLOW + _("Warning: '{0}' is writable by group or others ({1:o}).").format(self.filename, file_mode) + Style.RESET_ALL)
            if file_stat.st_uid != 0:
                print(Style.BRIGHT + Fore.YELLOW + _("Warning: '{0}' is not owned by root.").format(self.filename) + Style.RESET_ALL)
        except OSError:
            pass

    @property
    def cpu_hz(self) -> int:
        """Target CPU frequency in Hz applied during emerge execution."""
        return self.parser.getInteger('cpupower', 'cpu_hz')

    @property
    def use_ccache(self) -> bool:
        """Whether ccache support and environment configuration are enabled."""
        return self.parser.getBoolean('ccache', 'use', 'False')


def load_config(filename: Path | str = DEFAULT_CONFIG_PATH) -> Config:
    """Helper function to load a Config instance."""
    return Config(filename)

