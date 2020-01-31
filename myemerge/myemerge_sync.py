from myemerge.objects.command import command
from myemerge.myconfigparser import MyConfigParser
from myemerge.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_scaling_freq, sys_get_cpu_max_freq, is_cpufreq_configured
from os import makedirs

def main():
    config=MyConfigParser('/etc/myemerge/myemerge.ini')
    
    if is_cpufreq_configured():
        cpu_hz_before=sys_get_cpu_max_scaling_freq()
        cpu_hz=config.get('cpupower','cpu_hz',  str(sys_get_cpu_max_freq()))
        sys_set_cpu_max_scaling_freq(int(cpu_hz))

    command("emerge --sync")
    command("emaint cleanresume -f")
    command("emerge --update --newuse --deep -v --keep-going y @world --backtrack=60 --with-bdeps y --changed-deps y")
    command("emerge -v  @preserved-rebuild --keep-going y")
    command("eclean-dist -d")

    if is_cpufreq_configured():
        sys_set_cpu_max_scaling_freq(cpu_hz_before)

    config.save()
