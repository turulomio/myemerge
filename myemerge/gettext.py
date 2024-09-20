from gettext import translation
from importlib.resources import files

def _(s):
    try:
        t=translation('myemerge', files("myemerge")/"locale")
        return t.gettext(s)
    except:
        return s
