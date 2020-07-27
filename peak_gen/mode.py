# from peak import Peak, gen_register, family_closure
# from hwtypes import Enum
# from hwtypes.adt_util import rebind_type
# from functools import lru_cache
# from peak.family import AbstractFamily

# @lru_cache(None)
# def gen_register_mode(T, init=0):
#     @family_closure
#     def RegisterWithConst_fc(family : AbstractFamily):
#         T_f = rebind_type(T, family)
#         Reg = gen_register(T_f, init)(family)
#         Bit = family.Bit

#         @family.assemble(locals(), globals())
#         class RegisterWithConst(Peak):
#             def __init__(self):
#                 self.register: Reg = Reg()

#             #Outputs register_value
#             def __call__(self, config_data : T_f, config_we : Bit, clk_en: Bit) -> (T_f, T_f):
                
#                 reg_val = self.register(config_data, config_we)

#                 return config_data, reg_val
#         return RegisterWithConst
#     return RegisterWithConst_fc
