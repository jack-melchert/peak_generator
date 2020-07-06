
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function(Peak):
        def __call__(self, in2 : Data, in1 : Data, bit_in0 : Bit) -> Data:
  
            return (in2 if bit_in0 == Bit(0) else in1)
      
    return mapping_function
