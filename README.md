# MyEmerge [![Github - Downloads](https://shields.io/github/downloads/turulomio/myemerge/total?label=Github%20downloads )](https://github.com/turulomio/myemerge/)

## Configuration

My emerge recomends the use of ccache.

To see statistics with `myemerge --ccache_stats` you must set in /etc/portage/make.conf the following lines:
```bash
  CCACHE_DIR="/var/cache/ccache"
  FEATURES="ccache"
```

## Changelog

### 1.0.0 (2025-04-13)
- Migrated to poetry>2.0.0

### 0.10.0 (2024-09-20)
- Fixed problem with pytz dependency
- Updated dependencies
- Updated reusing

### 0.9.0 (2024-06-18)
- Improving package
- Updated dependencies

### 0.8.0 (2023-05-15)
- Migrated to pyproject.toml
- Fixed bugs with cpupower module

### 0.7.0 (2022-05-04)
- Set again max_cpu_frequency option in config

### 0.6.0 (2021-11-22)
- Added --nosync and --noclean parameters
- Removed config code. Added CCACHE_DIR to all script to use it one needed.

### 0.5.0
- You can use portage ccache statistics.

### 0.4.0
- Fixed bug when cpufreq isn't configured in kernel.
- Executable renamed to myemerge.
- Created --rebuild parameter to rebuild the whole Gentoo system.

### 0.3.0
- You can set your compile CPU frequency in Hz. Max CPU capacity by default.

### 0.2.0
- Code was converted to a python module
- Added /etc/myemerge config file
- You can run scripts with minimum cpu frequency

### 0.1.0
- Imported from old scripts
