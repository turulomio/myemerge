from myemerge import __version__
from os import system
from myemerge.reusing.github import download_from_github
from sys import argv


def release():
    print("""Nueva versión:
  * Crear un nuevo issue en github con el nombre myemerge-NUEVAVERSION
  * Copiar el codigo de github para cambiar de versión y pegarlo en la consola
  * Cambiar la version en pyproject.toml
  * Cambiar la versión y la fecha en __init__.py
  * Modificar el Changelog README.md
  * poe translate
  * mcedit myemerge/locale/es.po
  * poe translate
  * git commit -a -m 'myemerge-{0}'
  * git push
  * Hacer un pull request con los cambios a master
  * Hacer un nuevo tag en GitHub
  * git checkout master
  * git pull
  * poetry build
  * poetry publish
  * Crea un nuevo ebuild en Gentoo con la nueva versión
  * Subelo al repositorio myportage
""".format(__version__))


def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o myemerge/locale/myemerge.pot myemerge/*.py")
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

