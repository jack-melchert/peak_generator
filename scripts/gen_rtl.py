from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch, graph_arch
import magma as m
import sys, os
from peak import family

arch = read_arch(str(sys.argv[1]))
PE_fc = arch_closure(arch)
PE = PE_fc(family.MagmaFamily())

if not os.path.exists('scripts/build'):
    os.makedirs('scripts/build')
m.compile(f"scripts/build/PE", PE, output="coreir-verilog")


graph_arch(arch)