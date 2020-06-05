
from peak import Peak, family_closure
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function(Peak):
        def __call__(self, const0 : Data, in0 : Data, in1 : Data) -> Data:
            
            return ((in0 + in1) + const0)
      
    return mapping_function
