from argparse import ArgumentParser
from myemerge.gettext import _
from pycpufreq import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_freq, sys_get_cpu_max_scaling_freq, is_cpufreq_configured
from configparser_rb.core  import ConfigParserRB
from myemerge import __version__, __versiondate__
from os import environ
from pathlib import Path
from shutil import which
from subprocess import run
from sys import exit
from colorama import init as colorama_init,  Fore, Style

def check_app_cpupower():
    if which("cpupower") is None:
        print(Style.BRIGHT + Fore.RED + _("cpupower command wasn't found in your system. You won't be able to manage cpu frequencies. Be carefull with your system temperature") + Style.RESET_ALL)
        return False
    return True

def check_app_ccache():
    if which("ccache") is None:
        print(Style.BRIGHT + Fore.RED + _("ccache command wasn't found in your system.") + Style.RESET_ALL)
        return False
    return True
    
def load_config():
    """
        If file is not found creates a new one. Returns a config object
    """
    filename = Path('/etc/myemerge/myemerge.ini')
    config = ConfigParserRB(str(filename))
    config.get('cpupower', 'cpu_hz', sys_get_cpu_max_freq())
        
    if not filename.exists(): #Writes a config file
        config.save()
        filename.chmod(0o644)
        print(Style.BRIGHT + Fore.GREEN + _("Your '{0}' config file has been created. You can change your settings editing it.").format(filename) + Style.RESET_ALL)
    else:
        file_stat = filename.stat()
        file_mode = file_stat.st_mode & 0o777
        if file_mode & 0o022 != 0:
            print(Style.BRIGHT + Fore.YELLOW + _("Warning: '{0}' is writable by group or others ({1:o}).").format(filename, file_mode) + Style.RESET_ALL)
        if file_stat.st_uid != 0:
            print(Style.BRIGHT + Fore.YELLOW + _("Warning: '{0}' is not owned by root.").format(filename) + Style.RESET_ALL)
    
    return config

def main():
    colorama_init()
    has_cpupower=check_app_cpupower()
    has_ccache=check_app_ccache()
    parser=ArgumentParser(description=_("My method to update my Gentoo System"))
    parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
    parser.add_argument('--rebuild', help=_("Rebuild the whole Gentoo system"),  action='store_true',  default=False)
    parser.add_argument('--ccache_stats', help=_("Shows ccache statistics"),  action='store_true',  default=False)
    parser.add_argument('--nosync', help=_("Do not make emerge --sync"),  action='store_true',  default=False)
    parser.add_argument('--noclean', help=_("Do not clean innecesary packages after compilation"),  action='store_true',  default=False)

    args=parser.parse_args()
    
    config=load_config()


    environ["CCACHE_DIR"]="/var/cache/ccache" #CCache path of portage
    ##ccache is only used if it's set in /etc/portage/make.conf
    if args.ccache_stats==True:
        if has_ccache:
            run(["ccache", "-s"], check=True)
        else:
            print(Style.BRIGHT + Fore.RED + _("ccache command wasn't found in your system.") + Style.RESET_ALL)
        exit(0)
            



    if has_cpupower and is_cpufreq_configured():
        cpu_hz_before=sys_get_cpu_max_scaling_freq()
        cpu_hz=config.getInteger('cpupower', 'cpu_hz')
        sys_set_cpu_max_scaling_freq(cpu_hz)
        print(_("CPUs frequency set to {0}").format(int(cpu_hz)))

    if args.rebuild==True:
        run(["emaint", "cleanresume", "-f"], check=True)
        run(["emerge", "-ev", "world", "--keep-going", "y"], check=True)
        run(["emerge", "@preserved-rebuild"], check=True)
        run(["revdep-rebuild", "-i", "--", "--keep-going", "y"], check=True)
    else:
        if args.nosync is False:
            run(["emerge", "--sync"], check=True)
        run(["emaint", "cleanresume", "-f"], check=True)
        run(["emerge", "--update", "--newuse", "--deep", "-v", "--keep-going", "y", "@world", "--backtrack=60", "--with-bdeps", "y", "--changed-deps", "y"], check=True)
        run(["emerge", "-v", "@preserved-rebuild", "--keep-going", "y"], check=True)
        if args.noclean is False:
            run(["eclean-dist", "-d"], check=True)

    if has_cpupower and is_cpufreq_configured():
        sys_set_cpu_max_scaling_freq(cpu_hz_before)
        print(_("CPUs frequency set to {0}").format(int(cpu_hz_before)))
