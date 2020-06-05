# from .common import DATAWIDTH
# from peak import Const, family_closure
# from hwtypes import Tuple, Product
# import magma as m
# from peak.family import AbstractFamily

# def enables_arch_closure(arch):
#     @family_closure
#     def Enables_fc(family : AbstractFamily):
#         Bit = family.Bit
#         enablesList = Tuple[(Bit for _ in range(arch.num_reg))]

#         class Enables(Product):

#             clk_en = Bit
#             if (arch.num_reg > 0):
#                 reg_enables = enablesList

#         return Enables
#     return Enables_fc
