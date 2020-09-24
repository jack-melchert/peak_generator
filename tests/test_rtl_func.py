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
from peak_gen import CoreIRContext


def test_add():
    CoreIRContext(reset=True)
    arch = read_arch("examples/misc_tests/test_add.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()
    
    inputs = [BitVector[16](42),BitVector[16](42)]

    res_comp = inputs[0] + inputs[1]

    res_pe_bv = PE_bv(inst_gen(), inputs)

    assert res_comp == res_pe_bv[0].value
    rtl_tester(arch, inst_gen(), inputs, res_comp)


def test_mul():
    CoreIRContext(reset=True)
    arch = read_arch("examples/misc_tests/test_mul.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()

    inputs = [BitVector[16](42),BitVector[16](42)]

    res_comp = inputs[0] * inputs[1]

    res_pe_bv = PE_bv(inst_gen(), inputs)
    assert res_comp == res_pe_bv[0].value
    rtl_tester(arch, inst_gen(), inputs, res_comp)

def test_alu():
    CoreIRContext(reset=True)
    arch = read_arch("examples/misc_tests/test_alu.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()

    inputs = [BitVector[16](42),BitVector[16](42)]

    res_comp = inputs[0] + inputs[1]
    res_pe_bv = PE_bv(inst_gen(alu=[ALU_t.Add]), inputs)
    assert res_comp == res_pe_bv[0].value
    rtl_tester(arch, inst_gen(alu=[ALU_t.Add]), inputs, res_comp)

    res_comp = inputs[0] - inputs[1]
    res_pe_bv = PE_bv(inst_gen(alu=[ALU_t.Sub]), inputs)
    assert res_comp == res_pe_bv[0].value
    rtl_tester(arch, inst_gen(alu=[ALU_t.Sub]), inputs, res_comp)



def test_mux():
    CoreIRContext(reset=True)
    arch = read_arch("examples/misc_tests/lassen.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()

    inputs = [BitVector[16](42),BitVector[16](42)]

    res_comp = inputs[0] * inputs[1]
    res_pe_bv = PE_bv(inst_gen(mux_out=[BitVector[1](1)]), inputs)
    assert res_comp == res_pe_bv[0].value
    rtl_tester(arch, inst_gen(mux_out=[BitVector[1](1)]), inputs, res_comp)

    res_comp = inputs[0] + inputs[1]
    res_pe_bv = PE_bv(inst_gen(mux_out=[BitVector[1](0)]), inputs)
    assert res_comp == res_pe_bv[0].value
    rtl_tester(arch, inst_gen(mux_out=[BitVector[1](0)]), inputs, res_comp)
