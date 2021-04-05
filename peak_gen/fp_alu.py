from peak import Peak, name_outputs, family_closure, Const
from hwtypes import Enum, SMTFPVector, FPVector, RoundingMode
import magma
from peak.mapper.utils import rebind_type
from peak.family import AbstractFamily
from .common import BFloat16_fc
from peak.family import MagmaFamily, SMTFamily
from .isa import FP_ALU_t
from .isa import Signed_t
from ast_tools.passes import apply_passes, if_inline, loop_unroll
from ast_tools.macros import inline, unroll



@family_closure
def FP_ALU_fc(family : AbstractFamily):
    def FP_ALU_bw(width):

        Data = family.BitVector[width]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[width]
        UInt = family.Unsigned
        UData = UInt[width]


        fp_unit_t = fp_unit_fc(family)(width)


        @family.assemble(locals(), globals())
        class FP_ALU(Peak):

            def __init__(self):
                self.fp_unit : fp_unit_t = fp_unit_t()

            @name_outputs(res=Data, res_p=Bit, Z=Bit, N=Bit, C=Bit, V=Bit)
            def __call__(self, fp_alu: FP_ALU_t, signed_: Signed_t, a: Data, b: Data) -> (Data, Bit, Bit, Bit, Bit, Bit):
                

                res, res_p, Z, N, C, V = self.fp_unit(fp_alu, signed_, a, b)

                return res, res_p, Z, N, C, V

        return FP_ALU
    return FP_ALU_bw


@family_closure
def fp_unit_fc(family):
    def fp_unit_width(width):
    
        Data = family.BitVector[width]
        Bit = family.Bit
        SInt = family.Signed
        SData = SInt[width]
        UInt = family.Unsigned
        UData = UInt[width]

        BFloat16 = BFloat16_fc(family)
        FPExpBV = family.BitVector[8]
        FPFracBV = family.BitVector[7]

        def bv2float(bv):
            return BFloat16.reinterpret_from_bv(bv)

        def float2bv(bvf):
            return BFloat16.reinterpret_as_bv(bvf)

        def fp_get_exp(val : Data):
            return val[7:15]

        def fp_get_frac(val : Data):
            return val[:7]

        def fp_is_zero(val : Data):
            return (fp_get_exp(val) == FPExpBV(0)) & (fp_get_frac(val) == FPFracBV(0))

        def fp_is_inf(val : Data):
            return (fp_get_exp(val) == FPExpBV(-1)) & (fp_get_frac(val) == FPFracBV(0))

        def fp_is_neg(val : Data):
            return Bit(val[-1])


        @family.assemble(locals(), globals())
        class fp_unit(Peak):

            @apply_passes([if_inline()])
            @name_outputs(res=Data, res_p=Bit, Z=Bit, N=Bit, C=Bit, V=Bit)
            def __call__(self, alu: FP_ALU_t, signed_: Signed_t, a: Data, b: Data) -> (Data, Bit, Bit, Bit, Bit, Bit):

            
                if inline(not isinstance(family, SMTFamily)):

                    a_inf = fp_is_inf(a)
                    b_inf = fp_is_inf(b)
                    a_neg = fp_is_neg(a)
                    b_neg = fp_is_neg(b)
                    C = Bit(0)
                    N = Bit(0)
                    Z = Bit(0)
                    res_p = Bit(0)
                    

                    if alu == FP_ALU_t.FCnvExp2F:
                        expa0 = family.BitVector[8](a[7:15])
                        biased_exp0 = SInt[9](expa0.zext(1))
                        unbiased_exp0 = SInt[9](biased_exp0 - SInt[9](127))
                        if (unbiased_exp0 < 0):
                            sign = family.BitVector[16](0x8000)
                            abs_exp0 = -unbiased_exp0
                        else:
                            sign = family.BitVector[16](0x0000)
                            abs_exp0 = unbiased_exp0
                        abs_exp = family.BitVector[8](abs_exp0[0:8])
                        scale = SInt[16](-127)
                        # for bit_pos in range(8):
                        #   if (abs_exp[bit_pos]==Bit(1)):
                        #     scale = bit_pos
                        if (abs_exp[0] == Bit(1)):
                            scale = SInt[16](0)
                        if (abs_exp[1] == Bit(1)):
                            scale = SInt[16](1)
                        if (abs_exp[2] == Bit(1)):
                            scale = SInt[16](2)
                        if (abs_exp[3] == Bit(1)):
                            scale = SInt[16](3)
                        if (abs_exp[4] == Bit(1)):
                            scale = SInt[16](4)
                        if (abs_exp[5] == Bit(1)):
                            scale = SInt[16](5)
                        if (abs_exp[6] == Bit(1)):
                            scale = SInt[16](6)
                        if (abs_exp[7] == Bit(1)):
                            scale = SInt[16](7)
                        normmant_mul_left = SInt[16](abs_exp)
                        normmant_mul_right = (SInt[16](7)-scale)
                        normmant_mask = SInt[16](0x7F)
                    else: #alu == FP_ALU_t.FCnvInt2F:
                        if signed_ == Signed_t.signed:
                            sign = family.BitVector[16]((a) & 0x8000)
                        else:
                            sign = family.BitVector[16](0)
                        if (sign[15] == Bit(1)):
                            abs_input = family.BitVector[16](-SInt[16](a))
                        else:
                            abs_input = family.BitVector[16](a)
                        scale = SInt[16](-127)
                        # for bit_pos in range(8):
                        #   if (abs_exp[bit_pos]==Bit(1)):
                        #     scale = bit_pos
                        if (abs_input[0] == Bit(1)):
                            scale = SInt[16](0)
                        if (abs_input[1] == Bit(1)):
                            scale = SInt[16](1)
                        if (abs_input[2] == Bit(1)):
                            scale = SInt[16](2)
                        if (abs_input[3] == Bit(1)):
                            scale = SInt[16](3)
                        if (abs_input[4] == Bit(1)):
                            scale = SInt[16](4)
                        if (abs_input[5] == Bit(1)):
                            scale = SInt[16](5)
                        if (abs_input[6] == Bit(1)):
                            scale = SInt[16](6)
                        if (abs_input[7] == Bit(1)):
                            scale = SInt[16](7)
                        if (abs_input[8] == Bit(1)):
                            scale = SInt[16](8)
                        if (abs_input[9] == Bit(1)):
                            scale = SInt[16](9)
                        if (abs_input[10] == Bit(1)):
                            scale = SInt[16](10)
                        if (abs_input[11] == Bit(1)):
                            scale = SInt[16](11)
                        if (abs_input[12] == Bit(1)):
                            scale = SInt[16](12)
                        if (abs_input[13] == Bit(1)):
                            scale = SInt[16](13)
                        if (abs_input[14] == Bit(1)):
                            scale = SInt[16](14)
                        if (abs_input[15] == Bit(1)):
                            scale = SInt[16](15)
                        normmant_mul_left = SInt[16](abs_input)
                        normmant_mul_right = (SInt[16](15)-scale)
                        normmant_mask = SInt[16](0x7f00)

                    #if (alu == FP_ALU_t.FCnvInt2F) | (alu == FP_ALU_t.FCnvExp2F):
                    if (scale >= 0):
                        normmant = family.BitVector[16](
                            (normmant_mul_left << normmant_mul_right) & normmant_mask)
                    else:
                        normmant = family.BitVector[16](0)

                    if alu == FP_ALU_t.FCnvInt2F:
                        normmant = family.BitVector[16](normmant) >> 8

                    biased_scale = scale + 127
                    to_float_result = (sign | ((family.BitVector[16](biased_scale) << 7) & (
                            0xFF << 7)) | normmant)

                    res = Data(0)
                    res_p = Bit(0)

                
                    if (alu == FP_ALU_t.FP_add) | (alu == FP_ALU_t.FP_sub) | (alu == FP_ALU_t.FP_cmp):
                        #Flip the sign bit of b
                        if (alu == FP_ALU_t.FP_sub) | (alu == FP_ALU_t.FP_cmp):
                            b = (Data(1) << (width-1)) ^ b
                        a_fpadd = bv2float(a)
                        b_fpadd = bv2float(b)
                        res = float2bv(a_fpadd + b_fpadd)
                        res_p = Bit(0)
                    elif alu == FP_ALU_t.FP_mult:
                        a_fpmul = bv2float(a)
                        b_fpmul = bv2float(b)
                        res = float2bv(a_fpmul * b_fpmul)
                        res_p = Bit(0)
                    elif alu == FP_ALU_t.FGetMant:
                        res, res_p = (a & 0x7F), Bit(0)
                    elif alu == FP_ALU_t.FAddIExp:
                        sign = family.BitVector[16]((a & 0x8000))
                        exp = UData(a)[7:15]
                        exp_check = exp.zext(1)
                        exp = exp + UData(b)[0:8]
                        exp_check = exp_check + UData(b)[0:9]
                        # Augassign not supported by magma yet
                        # exp += SInt[8](b[0:8])
                        # exp_check += SInt[9](b[0:9])
                        exp_shift = family.BitVector[16](exp)
                        exp_shift = exp_shift << 7
                        mant = family.BitVector[16]((a & 0x7F))
                        res, res_p = (sign | exp_shift | mant), (exp_check > 255)
                    elif alu == FP_ALU_t.FSubExp:
                        signa = family.BitVector[16]((a & 0x8000))
                        expa = UData(a)[7:15]
                        signb = family.BitVector[16]((b & 0x8000))
                        expb = UData(b)[7:15]
                        expa = (expa - expb + 127)
                        exp_shift = family.BitVector[16](expa)
                        exp_shift = exp_shift << 7
                        manta = family.BitVector[16]((a & 0x7F))
                        res, res_p = ((signa | signb) | exp_shift | manta), Bit(0)
                    elif alu == FP_ALU_t.FCnvExp2F:
                        res, res_p = to_float_result, Bit(0)
                    elif alu == FP_ALU_t.FGetFInt:
                        signa = family.BitVector[16]((a & 0x8000))
                        manta = family.BitVector[16]((a & 0x7F)) | 0x80
                        expa0 = UData(a)[7:15]
                        biased_exp0 = SInt[9](expa0.zext(1))
                        unbiased_exp0 = SInt[9](biased_exp0 - SInt[9](127))
                        if (unbiased_exp0 < 0):
                            manta_shift0 = family.BitVector[23](0)
                        else:
                            manta_shift0 = family.BitVector[23](
                                manta) << family.BitVector[23](unbiased_exp0)
                        unsigned_res0 = family.BitVector[23](manta_shift0 >> family.BitVector[23](7))
                        unsigned_res = family.BitVector[16](unsigned_res0[0:16])
                        if (signa == 0x8000):
                            signed_res = -SInt[16](unsigned_res)
                        else:
                            signed_res = SInt[16](unsigned_res)
                        # We are not checking for overflow when converting to int
                        res, res_p, V = signed_res, Bit(0), (expa0 >  family.BitVector[8](142))
                    elif alu == FP_ALU_t.FGetFFrac:
                        signa = family.BitVector[16]((a & 0x8000))
                        manta = family.BitVector[16]((a & 0x7F)) | 0x80
                        expa0 = family.BitVector[8](a[7:15])
                        biased_exp0 = SInt[9](expa0.zext(1))
                        unbiased_exp0 = SInt[9](biased_exp0 - SInt[9](127))

                        if (unbiased_exp0 < 0):
                            manta_shift1 = family.BitVector[16](
                                manta) >> family.BitVector[16](-unbiased_exp0)
                        else:
                            manta_shift1 = family.BitVector[16](
                                manta) << family.BitVector[16](unbiased_exp0)
                        unsigned_res = family.BitVector[16]((manta_shift1 & 0x07F))
                        if (signa == 0x8000):
                            signed_res = -SInt[16](unsigned_res)
                        else:
                            signed_res = SInt[16](unsigned_res)

                        # We are not checking for overflow when converting to int
                        res, res_p = signed_res, Bit(0)
                    elif alu == FP_ALU_t.FCnvInt2F:
                        res, res_p = to_float_result, Bit(0)
                    

                    if (alu == FP_ALU_t.FP_sub) | (alu == FP_ALU_t.FP_add) | (alu == FP_ALU_t.FP_mult) | (alu==FP_ALU_t.FP_cmp):
                        Z = fp_is_zero(res)
                    else:
                        Z = (res == SData(0))

                    if (alu == FP_ALU_t.FP_cmp):
                        if (a_inf & b_inf) & (a_neg == b_neg):
                            Z = Bit(1)

                    N = Bit(res[-1])

                    self.res = res
                    self.res_p = res_p
                    self.Z = Z
                    self.N = N
                    self.C = C
                    self.V = V

                return self.res, self.res_p, self.Z, self.N, self.C, self.V

            def _set_fp(self, res: Data, res_p: Bit, Z: Bit, N: Bit, C: Bit, V: Bit):
                self.res = res
                self.res_p = res_p
                self.Z = Z
                self.N = N
                self.C = C
                self.V = V

        return fp_unit
    return fp_unit_width