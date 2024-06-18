from myemerge import __version__
from os import system
from myemerge.reusing.github import download_from_github
from myemerge.gettext import _
from sys import argv


def release():
    print(_("New Release:"))
    print(_("  * Change version and date in __init__.py"))
    print(_("  * Change version in pyproject.toml"))
    print(_("  * Edit Changelog in README"))
    print("  * poe translate")
    print("  * mcedit myemerge/locale/es.po")
    print("  * poe translate")
    print("  * git commit -a -m 'myemerge-{}'".format(__version__))
    print("  * git push")
    print(_("  * Make a new tag in github"))
    print(_("  * Create a new gentoo ebuild with the new version"))
    print(_("  * Upload to portage repository")) 

def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o myemerge/locale/myemerge.pot myemerge/*.py myemerge/objects/*.py")
        system("msgmerge -N --no-wrap -U myemerge/locale/es.po myemerge/locale/myemerge.pot")
        system("msgmerge -N --no-wrap -U myemerge/locale/fr.po myemerge/locale/myemerge.pot")
        system("msgfmt -cv -o myemerge/locale/es/LC_MESSAGES/myemerge.mo myemerge/locale/es.po")
        system("msgfmt -cv -o myemerge/locale/fr/LC_MESSAGES/myemerge.mo myemerge/locale/fr.po")

def reusing():
    """
        Actualiza directorio reusing
        poe reusing
        poe reusing --local
    """
    local=False
    if len(argv)==2 and argv[1]=="--local":
        local=True
        print("Update code in local without downloading was selected with --local")
    if local is False:
        download_from_github('turulomio','reusingcode','python/github.py', 'myemerge/reusing')
        download_from_github('turulomio','reusingcode','python/cpupower.py', 'myemerge/reusing')
        download_from_github('turulomio','reusingcode','python/myconfigparser.py', 'myemerge/reusing')
        download_from_github('turulomio','reusingcode','python/github.py', 'myemerge/reusing/')
        download_from_github('turulomio','reusingcode','python/file_functions.py', 'myemerge/reusing/')

