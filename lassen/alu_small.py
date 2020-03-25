from peak import Peak, name_outputs, family_closure, assemble
from magma import Enum
import magma


class ALU_t(Enum):
    Add = 0
    Sub = 1


class Signed_t(Enum):
    unsigned = 0
    signed = 1

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
        UInt = family.Unsigned
        UData = UInt[width]

        @assemble(family, locals(), globals())
        class ALU(Peak):
            @name_outputs(res=Data, res_p=Bit, Z=Bit, N=Bit, C=Bit, V=Bit)
            def __call__(self, alu: ALU_t, signed_: Signed_t, a: Data, b: Data, d:Bit) -> (Data, Bit, Bit, Bit, Bit, Bit):


                res, C = UData(a).adc(UData(b), Bit(0))
                V = overflow(a, b, res)
                res_p = C
                N = Bit(res[-1])
                Z = (res == 0)

                return res, res_p, Z, N, C, V

        return ALU
    return ALU_bw




# MagmaADT[Config, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](config_data)
# config_data_bits
# MagmaADT[Config, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](config_data)
# config_data_bits
# MagmaADT[Config, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](config_data)
# config_data_bits
# MagmaADT[Tuple[Bits[(16, Bit)], Bits[(16, Bit)]], <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inputs)
# 0
# MagmaADT[Tuple[Bits[(16, Bit)], Bits[(16, Bit)]], <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inputs)
# 1
# MagmaADT[Enables, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](enables)
# clk_en
# MagmaADT[Enables, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](enables)
# clk_en
# MagmaADT[Enables, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](enables)
# clk_en
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inst)
# alu
# MagmaADT[Tuple[ALU_t], <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](AnonymousValue_140373784325072)
# 0
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inst)
# signed
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inst)
# lut
# MagmaADT[ALU_t, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.In: 0>](O0)
# 0


# MagmaADT[Config, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](config_data)
# config_data_bits
# MagmaADT[Config, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](config_data)
# config_data_bits
# MagmaADT[Config, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](config_data)
# config_data_bits
# MagmaADT[Tuple[Bits[(16, Bit)], Bits[(16, Bit)]], <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inputs)
# 0
# MagmaADT[Tuple[Bits[(16, Bit)], Bits[(16, Bit)]], <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inputs)
# 1
# MagmaADT[Enables, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](enables)
# clk_en
# MagmaADT[Enables, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](enables)
# clk_en
# MagmaADT[Enables, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](enables)
# clk_en
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inst)
# alu
# MagmaADT[Tuple[ALU_t], <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](AnonymousValue_140639265650704)
# 0
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inst)
# signed
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inst)
# lut

# MagmaADT[ALU_t, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.In: 0>](O0)
# 0

# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.In: 0>](inst)
# alu
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.In: 0>](inst)
# signed
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.In: 0>](inst)
# lut
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.In: 0>](inst)
# cond




# self_cond_alu_0 = alu_res_p_0
# self_cond_lut_0 = lut_res_0
# self_cond_Z_0 = Z_0
# self_cond_N_0 = N_0
# self_cond_C_0 = C_0
# self_cond_V_0 = V_0
# res_p_0 = io.self_cond_O
# outputs_0 = []
# mux_idx_out_0 = 0
# output_temp_0 = signals_0[arch.outputs[0][0]]
# outputs_0.append(output_temp_0)
# __magma_ssa_return_value_0 = (self_modules_0_alu_0,
#     self_modules_0_signed__0, self_modules_0_a_0, self_modules_0_b_0,
#     self_modules_0_d_0, self_regd_config_data_0, self_regd_config_we_0,
#     self_regd_clk_en_0, self_rege_config_data_0, self_rege_config_we_0,
#     self_rege_clk_en_0, self_regf_config_data_0, self_regf_config_we_0,
#     self_regf_clk_en_0, self_cond_code_0, self_cond_alu_0,
#     self_cond_lut_0, self_cond_Z_0, self_cond_N_0, self_cond_C_0,
#     self_cond_V_0, self_lut_lut_0, self_lut_bit0_0, self_lut_bit1_0,
#     self_lut_bit2_0, outputs_0[0], res_p_0, read_config_data_0)
# (O0, O1, O2, O3, O4, O5, O6, O7, O8, O9, O10, O11, O12, O13, O14, O15,
#     O16, O17, O18, O19, O20, O21, O22, O23, O24, O25, O26, O27
#     ) = __magma_ssa_return_value_0



# MagmaADT[Config, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](config_data)
# config_data_bits
# MagmaADT[Config, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](config_data)
# config_data_bits
# MagmaADT[Config, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](config_data)
# config_data_bits
# MagmaADT[Tuple[Bits[(16, Bit)], Bits[(16, Bit)]], <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inputs)
# 0
# MagmaADT[Tuple[Bits[(16, Bit)], Bits[(16, Bit)]], <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inputs)
# 1
# MagmaADT[Enables, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](enables)
# clk_en
# MagmaADT[Enables, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](enables)
# clk_en
# MagmaADT[Enables, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](enables)
# clk_en
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inst)
# lut
# MagmaADT[Inst, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.Out: 1>](inst)
# cond
# MagmaADT[Cond_t, <class 'peak.assembler.assembler.Assembler'>, Bits, <Direction.In: 0>](O11)
# 0


# self_cond_alu_0 = alu_res_p_0
# self_cond_lut_0 = lut_res_0
# self_cond_Z_0 = Z_0
# self_cond_N_0 = N_0
# self_cond_C_0 = C_0
# self_cond_V_0 = V_0
# res_p_0 = io.self_cond_O
# outputs_0 = []
# mux_idx_out_0 = 0
# output_temp_0 = signals_0[arch.outputs[0][0]]
# outputs_0.append(output_temp_0)
# __magma_ssa_return_value_0 = (self_modules_0_a_0, self_modules_0_b_0,
#     self_regd_config_data_0, self_regd_config_we_0, self_regd_clk_en_0,
#     self_rege_config_data_0, self_rege_config_we_0, self_rege_clk_en_0,
#     self_regf_config_data_0, self_regf_config_we_0, self_regf_clk_en_0,
#     self_cond_code_0, self_cond_alu_0, self_cond_lut_0, self_cond_Z_0,
#     self_cond_N_0, self_cond_C_0, self_cond_V_0, self_lut_lut_0,
#     self_lut_bit0_0, self_lut_bit1_0, self_lut_bit2_0, outputs_0[0],
#     res_p_0, read_config_data_0)
# (O0, O1, O2, O3, O4, O5, O6, O7, O8, O9, O10, O11, O12, O13, O14, O15,
#     O16, O17, O18, O19, O20, O21, O22, O23, O24
#     ) = __magma_ssa_return_value_0








# inst=m.In(T)
# inputs=m.In(T0)
# enables=m.In(T1)
# config_addr=m.In(Data8)
# config_data=m.In(T2)
# config_en=m.In(Bit)
# self_modules_0_O0=m.In(T5)
# self_modules_0_O1=m.In(T6)
# self_modules_0_O2=m.In(T7)
# self_modules_0_O3=m.In(T8)
# self_modules_0_O4=m.In(T9)
# self_modules_0_O5=m.In(T10)
# self_regd_O0=m.In(T14)
# self_regd_O1=m.In(T15)
# self_rege_O0=m.In(T19)
# self_rege_O1=m.In(T20)
# self_regf_O0=m.In(T24)
# self_regf_O1=m.In(T25)
# self_cond_O=m.In(T33)
# self_lut_O=m.In(T38)

# O0=m.Out(T3)
# O1=m.Out(T4)
# O2=m.Out(T11)
# O3=m.Out(T12)
# O4=m.Out(T13)
# O5=m.Out(T16)
# O6=m.Out(T17)
# O7=m.Out(T18)
# O8=m.Out(T21)
# O9=m.Out(T22)
# O10=m.Out(T23)
# O11=m.Out(T26)
# O12=m.Out(T27)
# O13=m.Out(T28)
# O14=m.Out(T29)
# O15=m.Out(T30)
# O16=m.Out(T31)
# O17=m.Out(T32)
# O18=m.Out(T34)
# O19=m.Out(T35)
# O20=m.Out(T36)
# O21=m.Out(T37)
# O22=m.Out(Data)
# O23=m.Out(Bit)
# O24=m.Out(Data32)

# self_modules_0_a_0
# self_modules_0_b_0
# self_regd_config_data_0
# self_regd_config_we_0
# self_regd_clk_en_0
# self_rege_config_data_0
# self_rege_config_we_0
# self_rege_clk_en_0
# self_regf_config_data_0
# self_regf_config_we_0
# self_regf_clk_en_0
# self_cond_code_0
# self_cond_alu_0
# self_cond_lut_0
# self_cond_Z_0
# self_cond_N_0
# self_cond_C_0
# self_cond_V_0
# self_lut_lut_0
# self_lut_bit0_0
# self_lut_bit1_0
# self_lut_bit2_0
# outputs_0[0]
# res_p_0
# read_config_data_0



# self_modules_0_alu_0
# self_modules_0_signed__0
# self_modules_0_a_0
# self_modules_0_b_0
# self_modules_0_d_0
# self_regd_config_data_0
# self_regd_config_we_0
# self_regd_clk_en_0
# self_rege_config_data_0
# self_rege_config_we_0
# self_rege_clk_en_0
# self_regf_config_data_0
# self_regf_config_we_0
# self_regf_clk_en_0
# self_cond_code_0
# self_cond_alu_0
# self_cond_lut_0
# self_cond_Z_0
# self_cond_N_0
# self_cond_C_0
# self_cond_V_0
# self_lut_lut_0
# self_lut_bit0_0
# self_lut_bit1_0
# self_lut_bit2_0
# outputs_0[0]
# res_p_0
# read_config_data_0

# O0=m.Out(T3)
# O1=m.Out(T4)
# O2=m.Out(T5)
# O3=m.Out(T6)
# O4=m.Out(T7)
# O5=m.Out(T14)
# O6=m.Out(T15)
# O7=m.Out(T16)
# O8=m.Out(T19)
# O9=m.Out(T20)
# O10=m.Out(T21)
# O11=m.Out(T24)
# O12=m.Out(T25)
# O13=m.Out(T26)
# O14=m.Out(T29)
# O15=m.Out(T30)
# O16=m.Out(T31)
# O17=m.Out(T32)
# O18=m.Out(T33)
# O19=m.Out(T34)
# O20=m.Out(T35)
# O21=m.Out(T37)
# O22=m.Out(T38)
# O23=m.Out(T39)
# O24=m.Out(T40)
# O25=m.Out(Data)
# O26=m.Out(Bit)
# O27=m.Out(Data32)