from peak import Peak, name_outputs, family_closure
from peak.mapper.utils import rebind_type
from functools import lru_cache
from hwtypes import Enum
import magma
from ast_tools.passes import apply_passes, if_inline, loop_unroll
from ast_tools.macros import inline, unroll
from peak.family import AbstractFamily
from .isa import Signed_t, MUL_t



@family_closure
def MUL_fc(family : AbstractFamily):
    def MUL_bw(in_width, out_width):

        Data_out = family.BitVector[out_width]
        Data_in = family.BitVector[in_width]
        SInt = family.Signed
        SData = SInt[in_width]
        UInt = family.Unsigned
        UData = UInt[in_width]
        UDataMul = UInt[2*in_width]
        Bit = family.Bit

        @family.assemble(locals(), globals())
        class MUL(Peak):
            @apply_passes([if_inline()])
            @name_outputs(res=Data_out)
            def __call__(self, instr: MUL_t, signed_: Signed_t, a:Data_in, b:Data_in) -> (Data_out):

                if instr == MUL_t.datagate:
                    a = Data_in(0)
                    b = Data_in(0)

                if Bit(signed_ == Signed_t.signed):
                    mula, mulb = UDataMul(SData(a).sext(in_width)), UDataMul(SData(b).sext(in_width))
                else:
                    mula, mulb = UData(a).zext(in_width), UData(b).zext(in_width)


                mul = mula * mulb
                # res=0

                if inline(out_width == in_width):
                    if instr == MUL_t.Mult0:
                        res = mul[:in_width]
                    else:
                        res = mul[in_width:2*in_width]
                elif inline(out_width == 2*in_width):
                    res = mul
                else:
                    res = mul[:out_width]
                    
                return res

            # print(inspect.getsource(__call__)) 
        return MUL
    return MUL_bw