from peak_gen.sim import fp_pe_arch_closure, pe_arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
from peak_gen.peak_wrapper import wrapped_peak_class
from peak import Peak, family_closure, Const
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
from hwtypes import BitVector, Tuple, Bit
import sys
from peak import family
from peak.family import AbstractFamily
from peak.mapper import RewriteRule
from peak.assembler.assembled_adt import  AssembledADT
from peak.assembler.assembler import Assembler
import pdb
import json
import copy 
from pysmt.logics import QF_BV
import time
from lassen.sim import PE_fc
# from metamapper.irs.coreir.ir import gen_peak_CoreIR

def peak_op_bw():
    @family_closure
    def Peak_Op_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        Data32 = family.Unsigned[32]
        SInt = family.Signed[16]
        UInt = family.Unsigned[16]
        Bit = family.Bit
        @family.assemble(locals(), globals())
        class Peak_Op(Peak):
            def __call__(self, a : Data, b: Const(Data)) -> Data:
                # temp = a - b
                # temp_abs = Data(temp) < Data(0)
                # res = temp_abs.ite(Data(-Data(temp)), Data(Data(temp)))

                res = a >> b

                # res = a * b
                
                # temp_abs = Data(a) < Data(0)
                # res = temp_abs.ite(Data(-Data(a)), Data(Data(a)))
                return res
        return Peak_Op
    return Peak_Op_fc

def test_rr():
    # arch = read_arch(str(sys.argv[1]))
    # PE_fc = pe_arch_closure(arch)
    # PE_fc = wrapped_peak_class(arch, debug=True)

#    constraints = {("inputs0",): ('data176',), ("inputs1",): ('data177',), ("inputs2",): ('data178',), ("inputs3",): ('data179',), ("inputs4",): ('data180',), ("inputs5",): ('data181',), ("inputs6",): ('data182',)}


    arch_mapper = ArchMapper(PE_fc)
    # arch_mapper = ArchMapper(PE_fc)
    ir_fc = peak_op_bw()
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)

    times = []
    for t in range(10):
        start = time.time()
        solution = ir_mapper.solve('btor', external_loop=True, logic=QF_BV)
        end = time.time()
        times.append(end-start)

    breakpoint()
    print("time elapsed:", end-start)

    if solution is None: 
        print("No solution found")
    else:
        print("Solution found!")
        print(solution.ibinding)
        pretty_print_binding(solution.obinding) 
        counter_example = solution.verify()

        if counter_example is None:
            print("Passed verification")
        else:
            print("Failed verification")
            print(counter_example)

test_rr()
