
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
        def __call__(self, const0 : Const(Data), const1 : Const(Data), const2 : Const(Data), in1 : Data, in2 : Data, in3 : Data, in0 : Data) -> Data:
  
            return (((in1 + (const0 * in0)) + (const2 * in3)) + (const1 * in2))
      
    return mapping_function
