from myemerge.objects.command import command
from myemerge.myconfigparser import MyConfigParser
from myemerge.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_freq, sys_get_cpu_max_scaling_freq
from os import makedirs

def main():
    config=MyConfigParser('/etc/myemerge/myemerge.ini')

    cpu_hz_before=sys_get_cpu_max_scaling_freq()
    cpu_hz=config.get('cpupower','cpu_hz',  str(sys_get_cpu_max_freq()))
    sys_set_cpu_max_scaling_freq(int(cpu_hz))    

    command("emaint cleanresume -f")
    command("emerge -ev world --keep-going y")
    command("emerge @preserved-rebuild")
    command("revdep-rebuild -i -- --keep-going y")

    sys_set_cpu_max_scaling_freq(cpu_hz_before)

    config.save()
