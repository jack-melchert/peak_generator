from peak_gen.alu import ALU_fc
from peak_gen.cond import Cond_fc
from peak_gen.lut import LUT_fc
from peak_gen.sim import pe_arch_closure
from peak_gen.arch import read_arch
from hwtypes import BitVector, SMTBit, SMTBitVector
from peak.assembler.assembler import Assembler
from peak.assembler.assembled_adt import AssembledADT
from peak.mapper.utils import aadt_product_to_dict
import pytest, glob
from peak import family

def create_input(T):
    aadt_t = AssembledADT[T, Assembler, SMTBitVector]
    width = Assembler(T).width
    aadt_val = aadt_t(SMTBitVector[width]())
    return aadt_product_to_dict(aadt_val)

def test_LUT():
    LUT_smt = LUT_fc(family.SMTFamily())
    inputs = create_input(LUT_smt.input_t)
    outputs = LUT_smt()(**inputs)

def test_cond():
    Cond_smt = Cond_fc(family.SMTFamily())
    inputs = create_input(Cond_smt.input_t)
    outputs = Cond_smt()(**inputs)


def test_alu():
    ALU_smt = ALU_fc(family.SMTFamily())(16)
    inputs = create_input(ALU_smt.input_t)
    outputs = ALU_smt()(**inputs)



