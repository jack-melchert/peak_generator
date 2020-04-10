from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch, graph_arch
import sys, os, pytest, glob
from peak import family

@pytest.mark.parametrize("arch_file", glob.glob('examples/**/*.json', recursive=True))
def test_magma_family(arch_file):
    arch = read_arch(arch_file)
    PE_fc = arch_closure(arch)
    PE = PE_fc(family.MagmaFamily())


@pytest.mark.parametrize("arch_file", glob.glob('examples/**/*.json', recursive=True))
def test_py_family(arch_file):
    arch = read_arch(arch_file)
    PE_fc = arch_closure(arch)
    PE = PE_fc(family.PyFamily())

@pytest.mark.parametrize("arch_file", glob.glob('examples/**/*.json', recursive=True))
def test_smt_family(arch_file):
    arch = read_arch(arch_file)
    PE_fc = arch_closure(arch)
    PE = PE_fc(family.SMTFamily())