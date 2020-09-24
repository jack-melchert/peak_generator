import fault
import magma
import shutil
from peak.assembler import Assembler, MagmaADT
from peak import wrap_with_disassembler
from peak_gen import pe_arch_closure, inst_arch_closure
from peak_gen.arch import read_arch
from peak_gen.asm import asm_arch_closure
from peak_gen.isa import ALU_t
from hwtypes import Bit, BitVector
from hwtypes.adt import Tuple
from peak import family
import os
import random
import pytest
from rtl_utils import rtl_tester



def test_mux():

    arch = read_arch("examples/misc_tests/lassen.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()
    
    inputs = [BitVector.random(16),BitVector.random(16)]

    res_comp = inputs[0] + inputs[1]

    inst = inst_gen()

    res_pe_bv = PE_bv(inst, inputs)

    assert res_comp == res_pe_bv[0].value
    rtl_tester(arch, inst, inputs, res_comp)

