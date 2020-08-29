from peak import Peak, name_outputs, family_closure, Const
from hwtypes import Enum
import magma
from peak.mapper.utils import rebind_type
from peak.family import AbstractFamily
from .isa import Signed_t, BIT_ALU_t


@family_closure
def BIT_ALU_fc(family : AbstractFamily):
    def BIT_ALU_bw(width):

        Data = family.BitVector[width]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[width]
        UInt = family.Unsigned
        UData = UInt[width]

        @family.assemble(locals(), globals())
        class BIT_ALU(Peak):
            @name_outputs(res=Data, res_p=Bit, Z=Bit, N=Bit, C=Bit, V=Bit)
            def __call__(self, alu: BIT_ALU_t, a: Data, b: Data) -> (Data, Bit, Bit, Bit, Bit, Bit):
                
                if alu == BIT_ALU_t.And:
                    res, res_p = a & b, Bit(0)
                elif alu == BIT_ALU_t.Or:
                    res, res_p = a | b, Bit(0)
                else: #if alu == BIT_ALU_t.XOr:
                    res, res_p = a ^ b, Bit(0)

                C = Bit(0)
                V = Bit(0)
                N = Bit(res[-1])
                Z = (res == 0)

                return res, res_p, Z, N, C, V

        return BIT_ALU
    return BIT_ALU_bw