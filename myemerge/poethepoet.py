from myemerge import __version__
from subprocess import run


def release():
    print("""Nueva versión:
  * Crear un nuevo issue en github con el nombre myemerge-NUEVAVERSION
  * poe release
  * Cambiar la version en pyproject.toml
  * Cambiar la versión y la fecha en __init__.py
  * poe release
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
    run("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o myemerge/locale/myemerge.pot myemerge/*.py", shell=True, check=True)
    run(["msgmerge", "-N", "--no-wrap", "-U", "myemerge/locale/es.po", "myemerge/locale/myemerge.pot"], check=True)
    run(["msgmerge", "-N", "--no-wrap", "-U", "myemerge/locale/fr.po", "myemerge/locale/myemerge.pot"], check=True)
    run(["msgfmt", "-cv", "-o", "myemerge/locale/es/LC_MESSAGES/myemerge.mo", "myemerge/locale/es.po"], check=True)
    run(["msgfmt", "-cv", "-o", "myemerge/locale/fr/LC_MESSAGES/myemerge.mo", "myemerge/locale/fr.po"], check=True)

