from peak_gen.alu import ALU_fc
from peak_gen.cond import Cond_fc
from peak_gen.lut import LUT_fc
from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch
from hwtypes import BitVector, SMTBit, SMTBitVector
from peak.assembler.assembler import Assembler
from peak.assembler.assembled_adt import AssembledADT
from peak.mapper.utils import aadt_product_to_dict
import pytest, glob

def create_input(T):
    aadt_t = AssembledADT[T, Assembler, SMTBitVector]
    width = Assembler(T).width
    aadt_val = aadt_t(SMTBitVector[width]())
    return aadt_product_to_dict(aadt_val)

def test_LUT():
    LUT_smt = LUT_fc(SMTBit.get_family())
    inputs = create_input(LUT_smt.input_t)
    outputs = LUT_smt()(**inputs)

def test_cond():
    Cond_smt = Cond_fc(SMTBit.get_family())
    inputs = create_input(Cond_smt.input_t)
    outputs = Cond_smt()(**inputs)


def test_alu():
    ALU_smt = ALU_fc(SMTBit.get_family())(16)
    inputs = create_input(ALU_smt.input_t)
    outputs = ALU_smt()(**inputs)

@pytest.mark.parametrize("arch_file", glob.glob('examples/**/*.json', recursive=True))
def test_PE(arch_file):
    arch = read_arch(str(arch_file))
    PE_fc = arch_closure(arch)
    PE_smt = PE_fc(SMTBit.get_family())
    inputs = create_input(PE_smt.input_t)
    outputs = PE_smt()(**inputs)

