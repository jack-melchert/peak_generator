from peak import Peak, name_outputs, family_closure, assemble
from hwtypes import Enum as Enum_hw
from magma import Enum as Enum_m
import magma
from peak.mapper.utils import rebind_type


@family_closure
def ALU_t_fc(family):
    if (family == magma.get_family()):
        Enum = Enum_m
    else:
        Enum = Enum_hw

    class ALU_t(Enum):
        Add = 0
        Sub = 1
        Adc = 2
        Sbc = 6
        Abs = 3
        GTE_Max = 4
        LTE_Min = 5
        Sel = 8
        SHR = 0xf
        SHL = 0x11
        Or = 0x12
        And = 0x13
        XOr = 0x14


    class Signed_t(Enum):
        unsigned = 0
        signed = 1
  
    return ALU_t, Signed_t

def overflow(a, b, res):
    msb_a = a[-1]
    msb_b = b[-1]
    N = res[-1]
    return (msb_a & msb_b & ~N) | (~msb_a & ~msb_b & N)

@family_closure
def ALU_fc(family):
    def ALU_bw(width):

        Data = family.BitVector[width]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[width]
        UInt = family.Unsigned
        UData = UInt[width]
        ALU_t, Signed_t = ALU_t_fc(family)

        @assemble(family, locals(), globals())
        class ALU(Peak):
            @name_outputs(res=Data, res_p=Bit, Z=Bit, N=Bit, C=Bit, V=Bit)
            def __call__(self, alu: ALU_t, signed_: Signed_t, a: Data, b: Data, d:Bit) -> (Data, Bit, Bit, Bit, Bit, Bit):
                

                if signed_ == Signed_t.signed:
                    a_s = SData(a)
                    b_s = SData(b)
                    
                    gte_pred = a_s >= b_s
                    lte_pred = a_s <= b_s
                    abs_pred = a_s >= SData(0)
                    shr = Data(a_s >> b_s)
                else: #if signed_ == Signed_t.unsigned:
                    a_u = UData(a)
                    b_u = UData(b)
                    
                    gte_pred = a_u >= b_u
                    lte_pred = a_u <= b_u
                    abs_pred = a_u >= UData(0)
                    shr = Data(a_u >> b_u)
                res = Data(0)
                res_p = Bit(0)

                Cin = Bit(0)
                if (alu == ALU_t.Sub) | (alu == ALU_t.Sbc):
                    b = ~b

                if (alu == ALU_t.Add):
                    Cin = Bit(0)  
                    # Cin = d
                elif (alu == ALU_t.Sub):
                    Cin = Bit(1)
                elif (alu == ALU_t.Adc) | (alu == ALU_t.Sbc):
                    Cin = d
                    # Cin = Bit(0)

                C = Bit(0)
                V = Bit(0)
                if (alu == ALU_t.Add) | (alu == ALU_t.Sub) | (alu == ALU_t.Adc) | (alu == ALU_t.Sbc):
                    #adc needs to be unsigned
                    res, C = UData(a).adc(UData(b), Cin)
                    V = overflow(a, b, res)
                    res_p = C
                
                elif alu == ALU_t.GTE_Max:
                    # C, V = a-b?
                    res, res_p = gte_pred.ite(a, b), gte_pred
                elif alu == ALU_t.LTE_Min:
                    # C, V = a-b?
                    res, res_p = lte_pred.ite(a, b), lte_pred
                elif alu == ALU_t.Abs:
                    res, res_p = abs_pred.ite(a, -SInt[width](a)), Bit(a[-1])
                elif alu == ALU_t.Sel:
                    res, res_p = d.ite(a, b), Bit(0)
                elif alu == ALU_t.And:
                    res, res_p = a & b, Bit(0)
                elif alu == ALU_t.Or:
                    res, res_p = a | b, Bit(0)
                elif alu == ALU_t.XOr:
                    res, res_p = a ^ b, Bit(0)
                elif alu == ALU_t.SHR:
                    #res, res_p = a >> Data(b[:4]), Bit(0)
                    res, res_p = shr, Bit(0)
                elif alu == ALU_t.SHL:
                    #res, res_p = a << Data(b[:4]), Bit(0)
                    res, res_p = a << b, Bit(0)
                

                N = Bit(res[-1])
                Z = (res == 0)

                return res, res_p, Z, N, C, V

        return ALU
    return ALU_bw