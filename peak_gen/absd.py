from peak import Peak, name_outputs, family_closure
# from .common import DATAWIDTH
import magma
from peak.family import AbstractFamily

@family_closure
def ABSD_fc(family : AbstractFamily):
    def ABSD_bw(width):

        Data = family.BitVector[width]
        Bit = family.Bit
        UInt = family.Unsigned
        SInt = family.Signed
        UData = UInt[width]
        SData = SInt[width]

        @family.assemble(locals(), globals())
        class ABSD(Peak):
            @name_outputs(res=Data, res_p=Bit, Z=Bit, N=Bit, C=Bit, V=Bit)
            def __call__(self, a: Data, b: Data) -> (Data, Bit, Bit, Bit, Bit, Bit):

                Cin = Bit(1)
                b = ~b
                temp, C = UData(a).adc(UData(b), Cin)
                temp_abs = SData(temp) < SData(0)
                res, res_p = temp_abs.ite(Data(-SData(temp)), Data(SData(temp))), Bit(0)

                V = Bit(0)
                C = Bit(0)
                N = Bit(res[-1])
                Z = (res == 0)

                return res, res_p, Z, N, C, V

        return ABSD
    return ABSD_bw
