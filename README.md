# MyEmerge [![Github - Downloads](https://shields.io/github/downloads/turulomio/myemerge/total?label=Github%20downloads)](https://github.com/turulomio/myemerge/)

A Python-based CLI tool designed to simplify, optimize, and automate Gentoo Linux system updates (`emerge`).

## Features

- **Automated Update Workflow**: Runs sync, world deep update, preserved rebuilds, reverse dependencies checks, and distfiles cleanup.
- **CPU Frequency Scaling Control**: Automatically limits or sets CPU scaling frequency during compilation (powered by [`pycpufreq`](https://github.com/turulomio/pycpufreq)) to prevent system thermal throttling or excessive heat.
- **Optional Ccache Integration**: Supports checking compiler cache statistics and sets Portage `CCACHE_DIR` automatically when enabled.
- **Security-Minded Configuration**: Enforces and verifies secure file ownership (`root:root`) and permissions on `/etc/myemerge/myemerge.ini`.

---

## Configuration

`myemerge` automatically creates and reads its configuration file at `/etc/myemerge/myemerge.ini`.

### Example Configuration

```ini
[cpupower]
# Maximum CPU frequency in Hz applied during emerge execution
# Defaults to your system's current maximum CPU scaling frequency
cpu_hz = 4600000

[ccache]
# Boolean flag to enable or disable ccache support (True / False)
# Defaults to False
use = False
```

### Configuration Options

| Section | Option | Type | Default | Description |
|---|---|---|---|---|
| `[cpupower]` | `cpu_hz` | Integer | System Max Freq | Maximum CPU scaling frequency (in Hz) applied while compiling packages. Restores previous frequency upon completion. |
| `[ccache]` | `use` | Boolean | `False` | When `True`, configures `CCACHE_DIR` and allows viewing cache stats. Set to `False` to disable ccache integration. |

---

## Ccache Setup

To take full advantage of `ccache` in Gentoo, ensure it is installed and configured in `/etc/portage/make.conf`:

```bash
FEATURES="ccache"
CCACHE_DIR="/var/cache/ccache"
```

You can view ccache statistics at any time by running:

```bash
myemerge --ccache_stats
```

If `ccache` is disabled in `/etc/myemerge/myemerge.ini` (`use = False`), `myemerge` will skip setting the environment variable and inform you when running `--ccache_stats`.

---

## Usage

```bash
myemerge [options]
```

### Command-Line Arguments

- `--help`, `-h`: Show help message and available options.
- `--version`: Show the version number and release date.
- `--rebuild`: Rebuild the whole Gentoo system (`emaint`, `emerge -ev world`, `@preserved-rebuild`, `revdep-rebuild`).
- `--ccache_stats`: Display ccache statistics (`ccache -s`).
- `--nosync`: Skip `emerge --sync` and proceed directly with package updates.
- `--noclean`: Skip cleaning unnecessary distfiles (`eclean-dist -d`) after compilation.

---

## Development

This project uses [Poetry](https://python-poetry.org/) and [Poe the Poet](https://github.com/nat-n/poethepoet) for task management.

```bash
# Update translations (.pot, .po, and compile .mo)
poetry run poe translate

# View release instructions
poetry run poe release
```
