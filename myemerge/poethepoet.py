from myemerge import __version__
from os import system
from myemerge.reusing.github import download_from_github
from myemerge.reusing.file_functions import replace_in_file
from myemerge.gettext import _
from sys import argv


def release():
    print(_("New Release:"))
    print(_("  * Change version and date in version.py"))
    print(_("  * Edit Changelog in README"))
    print("  * python setup.py doc")
    print("  * mcedit locale/es.po")
    print("  * python setup.py doc")
    print("  * python setup.py install")
    print("  * git commit -a -m 'myemerge-{}'".format(__version__))
    print("  * git push")
    print("  * python setup.py uninstall")
    print(_("  * Make a new tag in github"))
    print(_("  * Create a new gentoo ebuild with the new version"))
    print(_("  * Upload to portage repository")) 

def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/myemerge.pot *.py myemerge/*.py myemerge/objects/*.py")
        system("msgmerge -N --no-wrap -U locale/es.po locale/myemerge.pot")
        system("msgmerge -N --no-wrap -U locale/fr.po locale/myemerge.pot")
        system("msgfmt -cv -o myemerge/locale/es/LC_MESSAGES/myemerge.mo locale/es.po")
        system("msgfmt -cv -o myemerge/locale/fr/LC_MESSAGES/myemerge.mo locale/fr.po")

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
        download_from_github('turulomio','reusingcode','python/casts.py', 'myemerge/reusing')
        download_from_github('turulomio','reusingcode','python/github.py', 'myemerge/reusing')
        download_from_github('turulomio','reusingcode','python/cpupower.py', 'myemerge/reusing')
        download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'myemerge/reusing')
        download_from_github('turulomio','reusingcode','python/myconfigparser.py', 'myemerge/reusing')
        download_from_github('turulomio','reusingcode','python/github.py', 'myemerge/reusing/')
        download_from_github('turulomio','reusingcode','python/file_functions.py', 'myemerge/reusing/')
        
    replace_in_file("myemerge/reusing/myconfigparser.py",  "from casts",  "from .casts")
    replace_in_file("myemerge/reusing/myconfigparser.py",  "from datetime_functions",  "from .datetime_functions")

