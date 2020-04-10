from peak import Peak, name_outputs, family_closure
from peak.mapper.utils import rebind_type
from functools import lru_cache
from hwtypes import Enum
import magma
from ast_tools.passes import begin_rewrite, end_rewrite, loop_unroll, if_inline
from ast_tools.macros import inline
from peak.family import AbstractFamily


class MUL_t(Enum):
    Mult0 = 0x0
    Mult1 = 0x1
    Mult1 = 0x2


class Signed_t(Enum):
    unsigned = 0
    signed = 1

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
            @end_rewrite()
            @if_inline()
            @begin_rewrite()
            @name_outputs(res=Data_out)
            def __call__(self, instr: MUL_t, signed_: Signed_t, a:Data_in, b:Data_in) -> (Data_out):

                if Bit(signed_ == Signed_t.signed):
                    a_s = SData(a)
                    b_s = SData(b)
                    mula, mulb = UDataMul(a_s.sext(in_width)), UDataMul(b_s.sext(in_width))
                else:
                    a_u = UData(a)
                    b_u = UData(b)
                    mula, mulb = a_u.zext(in_width), b_u.zext(in_width)
                    
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