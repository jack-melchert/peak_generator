from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch, graph_arch
from peak import family
import magma as m
import sys
import pdb
import pytest
import glob, os


@pytest.mark.parametrize("arch_file", glob.glob('examples/**/*.json', recursive=True))
def test_gen_rtl(arch_file):
    arch = read_arch(arch_file)
    PE_fc = arch_closure(arch)
    PE = PE_fc(family.MagmaFamily())

    if not os.path.exists('tests/build'):
        os.makedirs('tests/build')

    m.compile(f"tests/build/PE", PE, output="coreir-verilog")