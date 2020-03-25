from .common import DATAWIDTH
from peak import Const, family_closure
from hwtypes import Tuple, Product
import magma as m

def config_arch_closure(arch):
    @family_closure
    def Config_fc(family):
        Data = family.BitVector[arch.input_width]
        Bit = family.Bit
        BitConfigData = family.BitVector[3]

        ConfigDataList = Tuple[(Data for _ in range(arch.num_const_reg))]


        class Config(Product):

            config_data_bits = BitConfigData

            if (arch.num_const_reg > 0):
                config_data = ConfigDataList


        return Config
    return Config_fc
