from peak_gen.alu import ALU_fc
from peak_gen.cond import Cond_fc
from peak_gen.lut import LUT_fc
from peak_gen.sim import pe_arch_closure
from peak_gen.arch import read_arch
from hwtypes import BitVector
import magma, pytest, glob
from peak import family

def test_cond():
    Cond_magma = Cond_fc(family.MagmaFamily())

def test_alu():
    ALU_magma = ALU_fc(family.MagmaFamily())

@pytest.mark.parametrize("arch_file", glob.glob('examples/**/*.json', recursive=True))
def test_PE(arch_file):
    arch = read_arch(str(arch_file))
    PE_fc = pe_arch_closure(arch)
    PE_magma = PE_fc(family.MagmaFamily())

def test_LUT():
    LUT_magma = LUT_fc(family.MagmaFamily())

