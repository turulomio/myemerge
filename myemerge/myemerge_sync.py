from argparse import ArgumentParser
from myemerge.gettext import _
from myemerge.commons import command
from myemerge.reusing.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_freq, sys_get_cpu_max_scaling_freq, is_cpufreq_configured
from myemerge.reusing.myconfigparser import MyConfigParser
from myemerge import __version__, __versiondate__
from os import environ, system, path
from shutil import which
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
    filename='/etc/myemerge/myemerge.ini'
    config=MyConfigParser(filename)
    config.get('cpupower','cpu_hz',  sys_get_cpu_max_freq())
        
    if path.exists(filename) is False: #Writes a config file
        config.save()
        print(Style.BRIGHT + Fore.GREEN + _("Your '{0}' config file has been created. You can change your settings editing it.").format(filename) + Style.RESET_ALL)
    
    return config

def main():
    colorama_init()
    has_cpupower=check_app_ccache()
    has_ccache=check_app_cpupower()
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
            system("ccache -s")
        else:
            print(Style.BRIGHT + Fore.RED + _("ccache command wasn't found in your system.") + Style.RESET_ALL)
        exit(0)
            



    if has_cpupower and is_cpufreq_configured():
        cpu_hz_before=sys_get_cpu_max_scaling_freq()
        cpu_hz=config.getInteger('cpupower', 'cpu_hz')
        sys_set_cpu_max_scaling_freq(cpu_hz)
        print(_("CPUs frequency set to {0}").format(int(cpu_hz)))

    if args.rebuild==True:
        command("emaint cleanresume -f")
        command("emerge -ev world --keep-going y")
        command("emerge @preserved-rebuild")
        command("revdep-rebuild -i -- --keep-going y")
    else:
        if args.nosync is False:
            command("emerge --sync")
        command("emaint cleanresume -f")
        command("emerge --update --newuse --deep -v --keep-going y @world --backtrack=60 --with-bdeps y --changed-deps y")
        command("emerge -v  @preserved-rebuild --keep-going y")
        if args.noclean is False:
            command("eclean-dist -d")

    if has_cpupower and is_cpufreq_configured():
        sys_set_cpu_max_scaling_freq(cpu_hz_before)
        print(_("CPUs frequency set to {0}").format(int(cpu_hz_before)))
