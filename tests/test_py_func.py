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

def test_add():
    arch = read_arch("examples/misc_tests/test_add.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()
    
    inputs = [BitVector.random(16),BitVector.random(16)]

    res_comp = inputs[0] + inputs[1]

    res_pe_bv = PE_bv(inst_gen(), inputs)

    assert res_comp == res_pe_bv[0].value


def test_mul():
    arch = read_arch("examples/misc_tests/test_mul.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()

    inputs = [BitVector.random(8),BitVector.random(8)]

    res_comp = inputs[0] * inputs[1]

    res_pe_bv = PE_bv(inst_gen(), inputs)
    assert res_comp == res_pe_bv[0].value

def test_alu():
    arch = read_arch("examples/misc_tests/test_alu.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()

    inputs = [BitVector.random(16),BitVector.random(16)]

    res_comp = inputs[0] + inputs[1]
    res_pe_bv = PE_bv(inst_gen(alu=[ALU_t.Add]), inputs)
    assert res_comp == res_pe_bv[0].value

    res_comp = inputs[0] - inputs[1]
    res_pe_bv = PE_bv(inst_gen(alu=[ALU_t.Sub]), inputs)
    assert res_comp == res_pe_bv[0].value


def test_multiple_outs():
    arch = read_arch("examples/misc_tests/test_multiple_outs.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()

    inputs = [BitVector.random(8),BitVector.random(8)]

    res_comp = inputs[0] + inputs[1]
    res_pe_bv = PE_bv(inst_gen(alu=[ALU_t.Add]), inputs)
    assert res_comp == res_pe_bv[0].value

    res_comp = inputs[0] * inputs[1]
    assert res_comp == res_pe_bv[1].value

def test_fma():
    arch = read_arch("examples/misc_tests/fma_pipelined.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()

    inputs = [BitVector.random(8),BitVector.random(8),BitVector.random(8)]

    res_comp = inputs[0] * inputs[1] + inputs[2]
    res_pe_bv = PE_bv(inst_gen(), inputs)
    assert inputs[2] == res_pe_bv[0].value

    res_pe_bv = PE_bv(inst_gen(), inputs)
    assert res_comp == res_pe_bv[0].value

def test_mux():
    arch = read_arch("examples/misc_tests/lassen.json")
    PE_fc = pe_arch_closure(arch)
    inst_gen = asm_arch_closure(arch)(family.PyFamily())
    PE_bv = PE_fc.Py()

    inputs = [BitVector.random(8),BitVector.random(8)]

    res_comp = inputs[0] * inputs[1]
    res_pe_bv = PE_bv(inst_gen(mux_out=[BitVector[1](1)]), inputs)
    assert res_comp == res_pe_bv[0].value

    res_comp = inputs[0] + inputs[1]
    res_pe_bv = PE_bv(inst_gen(mux_out=[BitVector[1](0)]), inputs)
    assert res_comp == res_pe_bv[0].value


