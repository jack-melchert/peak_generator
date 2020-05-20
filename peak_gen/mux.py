from peak import Peak, name_outputs, family_closure
from peak.family import AbstractFamily



@family_closure
def MUX_fc(family : AbstractFamily):
    def MUX_bw(in_width):

        Data = family.BitVector[in_width]
        Bit = family.Bit

        @family.assemble(locals(), globals())
        class Mux(Peak):

            @name_outputs(res=Data)
            def __call__(self, a: Data, b: Data, sel: Bit) -> (Data):

                return sel.ite(b, a)
 
        return Mux
    return MUX_bw