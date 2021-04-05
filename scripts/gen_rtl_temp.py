from peak_gen.sim import pe_arch_closure
from peak_gen.arch import read_arch, graph_arch
import magma as m
import sys, os
from peak import family
import glob



filename = str(sys.argv[1])
block_name = filename.split("/")[2].split(".")[0]
arch = read_arch(filename)
PE_fc = pe_arch_closure(arch)
PE = PE_fc(family.MagmaFamily())

if not os.path.exists('scripts/building_blocks'):
    os.makedirs('scripts/building_blocks')
m.compile(f"scripts/building_blocks/{block_name}", PE, output="coreir-verilog", namespaces=["commonlib"])

