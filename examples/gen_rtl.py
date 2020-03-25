from lassen.sim import arch_closure
from lassen.arch import read_arch, graph_arch
import magma as m
import sys
import pdb


arch = read_arch(str(sys.argv[1]))
graph_arch(arch)

PE_fc = arch_closure(arch)

PE = PE_fc(m.get_family())


m.compile(f"examples/build/PE", PE, output="coreir-verilog")