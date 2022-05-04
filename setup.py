from setuptools import setup, Command
import gettext
import os
import platform
import site

gettext.install('myemerge', 'myemerge/locale')

class Procedure(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
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

class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/myemerge*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/myemerge*")
        else:
            print(_("Uninstall command only works in Linux"))

class Doc(Command):
    description = "Update man pages and translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/myemerge.pot *.py myemerge/*.py myemerge/objects/*.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/myemerge.pot")
        os.system("msgmerge -N --no-wrap -U locale/fr.po locale/myemerge.pot")
        os.system("msgfmt -cv -o myemerge/locale/es/LC_MESSAGES/myemerge.mo locale/es.po")
        os.system("msgfmt -cv -o myemerge/locale/fr/LC_MESSAGES/myemerge.mo locale/fr.po")

class Reusing(Command):
    description = "Download modules from https://github.com/turulomio/reusingcode/"
    user_options = [
      # The format is (long option, short option, description).
      ( 'local', None, 'Update files without internet'),
  ]

    def initialize_options(self):
        self.local=False


    def finalize_options(self):
        pass

    def run(self):
        from sys import path
        path.append("myemerge/reusing")
        from github import download_from_github
        if self.local is False:
            download_from_github('turulomio','reusingcode','python/casts.py', 'myemerge/reusing')
            download_from_github('turulomio','reusingcode','python/github.py', 'myemerge/reusing')
            download_from_github('turulomio','reusingcode','python/cpupower.py', 'myemerge/reusing')
            download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'myemerge/reusing')
            download_from_github('turulomio','reusingcode','python/myconfigparser.py', 'myemerge/reusing')
            download_from_github('turulomio','reusingcode','python/github.py', 'myemerge/reusing/')
            download_from_github('turulomio','reusingcode','python/file_functions.py', 'myemerge/reusing/')
            download_from_github('turulomio','reusingcode','python/percentage.py', 'myemerge/reusing/')
            download_from_github('turulomio','reusingcode','python/currency.py', 'myemerge/reusing/')
        
        from file_functions import replace_in_file
        replace_in_file("myemerge/reusing/casts.py","from currency","from myemerge.reusing.currency")
        replace_in_file("myemerge/reusing/casts.py","from percentage","from myemerge.reusing.percentage")

    ########################################################################


## Version of modele captured from version to avoid problems with package dependencies
__version__= None
with open('myemerge/version.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]

setup(name='myemerge',
    version=__version__,
    description='My method to update my Gentoo System',
    long_description="Project web page is in https://github.com/turulomio/myemerge",
    long_description_content_type='text/markdown',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: System Administrators',
                 'Topic :: System :: Systems Administration',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3',
                ],
    keywords='change permissions ownner files directories',
    url='https://github.com/turulomio/myemerge',
    author='turulomio',
    author_email='turulomio@yahoo.es',
    license='GPL-3',
    packages=['myemerge'],
    entry_points = {'console_scripts': [
                                        'myemerge=myemerge.myemerge_sync:main',
                                       ],
                   },
    install_requires=['setuptools'],
    cmdclass={
               'doc': Doc,
               'uninstall': Uninstall,
               'procedure': Procedure,
               'reusing': Reusing,
             },
    zip_safe=False,
    include_package_data=True
    )

_=gettext.gettext#To avoid warnings
