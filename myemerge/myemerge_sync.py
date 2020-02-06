from argparse import ArgumentParser
from myemerge.gettext import _
from myemerge.objects.command import command
from myemerge.myconfigparser import MyConfigParser
from myemerge.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_scaling_freq, sys_get_cpu_max_freq, is_cpufreq_configured
from myemerge.version import __version__, __versiondate__


def main():
    parser=ArgumentParser(description=_("My method to update my Gentoo System"))
    parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
    parser.add_argument('--config', help=_("Write a config file in /etc/myemerge/myemerge.ini"),  action='store_true',  default=False)
    parser.add_argument('--rebuild', help=_("Rebuild the whole Gentoo system"),  action='store_true',  default=False)
    args=parser.parse_args()
    config=MyConfigParser('/etc/myemerge/myemerge.ini')
     
    if args.config==True: #Writes a config file
        config.save()
        print("You must set your settings in /etc/mykernel/mykernel.ini. Use man mykernel for help.")
        exit(0)
    
    if is_cpufreq_configured():
        cpu_hz_before=sys_get_cpu_max_scaling_freq()
        cpu_hz=config.get('cpupower','cpu_hz',  str(sys_get_cpu_max_freq()))
        sys_set_cpu_max_scaling_freq(int(cpu_hz))
        
    if args.config==True: #Writes a config file
        config.save()
        print("You must set your settings in /etc/mykernel/mykernel.ini. Use man mykernel for help.")
        exit(0)

    if args.rebuild==True:
        command("emaint cleanresume -f")
        command("emerge -ev world --keep-going y")
        command("emerge @preserved-rebuild")
        command("revdep-rebuild -i -- --keep-going y")
    else:
        command("emerge --sync")
        command("emaint cleanresume -f")
        command("emerge --update --newuse --deep -v --keep-going y @world --backtrack=60 --with-bdeps y --changed-deps y")
        command("emerge -v  @preserved-rebuild --keep-going y")
        command("eclean-dist -d")

    if is_cpufreq_configured():
        sys_set_cpu_max_scaling_freq(cpu_hz_before)

    config.save()
