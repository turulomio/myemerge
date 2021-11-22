# Configuration

My emerge recomends the use of ccache.

To see statistics with `myemerge --ccache_stats` you must set in /etc/portage/make.conf the following lines:
```bash
  CCACHE_DIR="/var/cache/ccache"
  FEATURES="ccache"
```

# Changelog

## 0.5.0
- You can use portage ccache statistics.

## 0.4.0
- Fixed bug when cpufreq isn't configured in kernel.
- Executable renamed to myemerge.
- Created --rebuild parameter to rebuild the whole Gentoo system.

## 0.3.0
- You can set your compile CPU frequency in Hz. Max CPU capacity by default.

## 0.2.0
- Code was converted to a python module
- Added /etc/myemerge config file
- You can run scripts with minimum cpu frequency

## 0.1.0
- Imported from old scripts
