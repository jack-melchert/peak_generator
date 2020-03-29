from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch, graph_arch
import magma as m
import sys
import pdb
import pytest
import glob, os

@pytest.mark.parametrize("arch_file", glob.glob('./**/*.json', recursive=True))
def test_gen_rtl(arch_file):
    print(arch_file)
    arch = read_arch(arch_file)
    PE_fc = arch_closure(arch)
    PE = PE_fc(m.get_family())
    m.compile(f"examples/build/PE", PE, output="coreir-verilog")