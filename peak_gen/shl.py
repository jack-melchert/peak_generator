from peak import Peak, name_outputs, family_closure
# from .common import DATAWIDTH
import magma
from peak.family import AbstractFamily

@family_closure
def SHL_fc(family : AbstractFamily):
    def SHL_bw(width):

        Data = family.BitVector[width]
        Bit = family.Bit
        UInt = family.Unsigned
        SInt = family.Signed
        UData = UInt[width]

        @family.assemble(locals(), globals())
        class SHL(Peak):
            @name_outputs(res=Data, res_p=Bit, Z=Bit, N=Bit, C=Bit, V=Bit)
            def __call__(self, a: Data, b: Data) -> (Data, Bit, Bit, Bit, Bit, Bit):


                res, res_p = a << b, Bit(0)
                V = Bit(0)
                C = Bit(0)
                N = Bit(res[-1])
                Z = (res == 0)

                return res, res_p, Z, N, C, V

        return SHL
    return SHL_bw
