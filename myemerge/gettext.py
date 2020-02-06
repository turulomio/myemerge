from gettext import translation
from pkg_resources import resource_filename

def _(s):
    t=translation('myemerge', resource_filename("myemerge","locale"))
    return t.gettext(s)
