from peak import Peak, name_outputs, family_closure
# from .common import DATAWIDTH
import magma
from peak.family import AbstractFamily

def overflow(a, b, res):
    msb_a = a[-1]
    msb_b = b[-1]
    N = res[-1]
    return (msb_a & msb_b & ~N) | (~msb_a & ~msb_b & N)

@family_closure
def SUB_fc(family : AbstractFamily):
    def SUB_bw(width):

        Data = family.BitVector[width]
        Bit = family.Bit
        UInt = family.Unsigned
        UData = UInt[width]

        @family.assemble(locals(), globals())
        class SUB(Peak):
            @name_outputs(res=Data, res_p=Bit, Z=Bit, N=Bit, C=Bit, V=Bit)
            def __call__(self, a: Data, b: Data) -> (Data, Bit, Bit, Bit, Bit, Bit):

                b = ~b
                res, C = UData(a).adc(UData(b), Bit(1))
                V = overflow(a, b, res)
                res_p = C
                N = Bit(res[-1])
                Z = (res == 0)

                return res, res_p, Z, N, C, V

        return SUB
    return SUB_bw
