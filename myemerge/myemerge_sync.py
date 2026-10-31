from argparse import ArgumentParser
from myemerge.gettext import _
from pycpufreq import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_scaling_freq, is_cpufreq_configured
from myemerge.config import load_config
from myemerge import __version__, __versiondate__
from os import environ, geteuid
from shutil import which
from subprocess import CalledProcessError, run
from sys import exit
from colorama import init as colorama_init,  Fore, Style

def check_app_ccache():
    if which("ccache") is None:
        print(Style.BRIGHT + Fore.RED + _("ccache command wasn't found in your system.") + Style.RESET_ALL)
        return False
    return True

def main():
    colorama_init()
    parser = ArgumentParser(description=_("My method to update my Gentoo System"))
    parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
    parser.add_argument('--rebuild', help=_("Rebuild the whole Gentoo system"),  action='store_true',  default=False)
    parser.add_argument('--ccache_stats', help=_("Shows ccache statistics"),  action='store_true',  default=False)
    parser.add_argument('--nosync', help=_("Do not make emerge --sync"),  action='store_true',  default=False)
    parser.add_argument('--noclean', help=_("Do not clean innecesary packages after compilation"),  action='store_true',  default=False)

    args = parser.parse_args()
    
    config = load_config()

    if config.use_ccache:
        has_ccache = check_app_ccache()
        environ["CCACHE_DIR"] = "/var/cache/ccache" #CCache path of portage
        ##ccache is only used if it's set in /etc/portage/make.conf
        if args.ccache_stats:
            if has_ccache:
                run(["ccache", "-s"], check=True)
            else:
                print(Style.BRIGHT + Fore.RED + _("ccache command wasn't found in your system.") + Style.RESET_ALL)
            exit(0)
    elif args.ccache_stats:
        print(Style.BRIGHT + Fore.RED + _("ccache is disabled in your configuration.") + Style.RESET_ALL)
        exit(0)

    if is_cpufreq_configured():
        cpu_hz_before = sys_get_cpu_max_scaling_freq()
        cpu_hz = config.cpu_hz
        if sys_set_cpu_max_scaling_freq(cpu_hz):
            print(_("CPUs frequency set to {0}").format(int(cpu_hz)))

    try:
        if args.rebuild:
            run(["emaint", "cleanresume", "-f"], check=True)
            run(["emerge", "-ev", "world", "--keep-going", "y"], check=True)
            run(["emerge", "@preserved-rebuild"], check=True)
            run(["revdep-rebuild", "-i", "--", "--keep-going", "y"], check=True)
        else:
            if not args.nosync:
                run(["emerge", "--sync"], check=True)
            run(["emaint", "cleanresume", "-f"], check=True)
            run(["emerge", "--update", "--newuse", "--deep", "-v", "--keep-going", "y", "@world", "--backtrack=60", "--with-bdeps", "y", "--changed-deps", "y"], check=True)
            run(["emerge", "-v", "@preserved-rebuild", "--keep-going", "y"], check=True)
            if not args.noclean:
                run(["eclean-dist", "-d"], check=True)
    except (CalledProcessError, PermissionError) as e:
        if geteuid() != 0:
            print(Style.BRIGHT + Fore.RED + _("Execution failed. myemerge requires root privileges to manage packages and CPU settings.") + Style.RESET_ALL)
            exit(1)
        raise e

    if is_cpufreq_configured():
        if sys_set_cpu_max_scaling_freq(cpu_hz_before):
            print(_("CPUs frequency set to {0}").format(int(cpu_hz_before)))
