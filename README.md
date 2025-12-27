# MyEmerge [![Github - Downloads](https://shields.io/github/downloads/turulomio/myemerge/total?label=Github%20downloads )](https://github.com/turulomio/myemerge/)

## Configuration

My emerge recomends the use of ccache.

To see statistics with `myemerge --ccache_stats` you must set in /etc/portage/make.conf the following lines:
```bash
  CCACHE_DIR="/var/cache/ccache"
  FEATURES="ccache"
```
