from argparse import ArgumentParser
from myemerge.gettext import _
from myemerge.objects.command import command
from myemerge.reusing.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_freq, sys_get_cpu_max_scaling_freq, is_cpufreq_configured
from myemerge.reusing.myconfigparser import MyConfigParser
from myemerge.version import __version__, __versiondate__
from os import environ, system
from sys import exit

def main():
    parser=ArgumentParser(description=_("My method to update my Gentoo System"))
    parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
    parser.add_argument('--config', help=_("Write a config file in /etc/myemerge/myemerge.ini"),  action='store_true',  default=False)
    parser.add_argument('--rebuild', help=_("Rebuild the whole Gentoo system"),  action='store_true',  default=False)
    parser.add_argument('--ccache_stats', help=_("Shows ccache statistics"),  action='store_true',  default=False)
    parser.add_argument('--nosync', help=_("Do not make emerge --sync"),  action='store_true',  default=False)
    parser.add_argument('--noclean', help=_("Do not clean innecesary packages after compilation"),  action='store_true',  default=False)

    args=parser.parse_args()

    config=MyConfigParser('/etc/myemerge/myemerge.ini')
    cpu_hz=config.get('cpupower','cpu_hz',  str(sys_get_cpu_max_freq()))

    environ["CCACHE_DIR"]="/var/cache/ccache" #CCache path of portage
    ##ccache is only used if it's set in /etc/portage/make.conf
    if args.ccache_stats==True:
        if args.ccache_stats==True:
            system("ccache -s")
            exit(0)
    
    if args.config==True: #Writes a config file
        config.save()
        print(_("You must set your settings in /etc/myemerge/myemerge.ini. Use man myemerge for help."))
        exit(0)


    if is_cpufreq_configured():
        cpu_hz_before=sys_get_cpu_max_scaling_freq()
        sys_set_cpu_max_scaling_freq(int(cpu_hz))
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

    if is_cpufreq_configured():
        sys_set_cpu_max_scaling_freq(cpu_hz_before)
        print(_("CPUs frequency set to {0}").format(int(cpu_hz_before)))
