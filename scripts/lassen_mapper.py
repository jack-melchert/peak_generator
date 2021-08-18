
from peak import Peak, family_closure, Const
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
from hwtypes import BitVector, Tuple, Bit
import sys
from peak import family, name_outputs
from peak.family import AbstractFamily
from peak.mapper import RewriteRule
from peak.assembler.assembled_adt import  AssembledADT
from peak.assembler.assembler import Assembler
import pdb
import json
import copy 
import time
from lassen.sim import PE_fc
# from lassen.float.fpu import float_lib, RoundingMode
from pysmt.logics import QF_BV
# from metamapper.irs.coreir.ir import gen_peak_CoreIR

def peak_op_bw():
    @family_closure
    def Peak_Op_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        SData = family.Signed[16]
        Bit = family.Bit
        # @family.assemble(locals(), globals())
        class Peak_Op(Peak):

            def __call__(self, in_0 : Const(Data), in_1 : Data) -> Data:
                # return Bit(SData(in_0) <= SData(in_1 + 1))
                return in_0 * in_1 
        return Peak_Op
    return Peak_Op_fc

# def peak_op_bw():
#     @family_closure
#     def fp_mult_const_fc(family: AbstractFamily):
#         RoundMode_c = family.get_constructor(RoundingMode)
#         Data = family.BitVector[16]
#         FPMul = float_lib.Mul_fc(family)
#         @family.assemble(locals(), globals())
#         class fp_mult_const(Peak):
#             def __init__(self):
#                 self.Mul: FPMul = FPMul()
#             @name_outputs(out=Data)
#             def __call__(self, in0: Data, in1: Const(Data)) -> Data:
#                 rmode = RoundMode_c(RoundingMode.RNE)
#                 res = self.Mul(rmode, in0, in1)
#                 return res
#         return fp_mult_const
#     return fp_mult_const_fc

def test_rr():
    arch_mapper = ArchMapper(PE_fc)

    ir_fc = peak_op_bw()
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc, simple_formula=True)
    times = []
    for i in range(10):
        start = time.time()
        rewrite_rule = ir_mapper.solve('btor', logic=QF_BV, external_loop=True, itr_limit=80)
        end = time.time()
        times.append(end-start)
        print(end-start)

    print(times)

    # if solution is None: 
    #     print("No solution found")
    # else:
    #     print("Solution found!")
    #     # pretty_print_binding(solution.ibinding)
    #     # pretty_print_binding(solution.obinding) 
    #     counter_example = solution.verify()

    #     if counter_example is None:
    #         print("Passed verification")
    #     else:
    #         print("Failed verification")
    #         print(counter_example)

test_rr()
