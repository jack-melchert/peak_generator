from .sim import pe_arch_closure
from .isa import inst_arch_closure
from .common import *
import magma
import coreir

_cache = None
def CoreIRContext(reset=False) -> coreir.Context:
    global _cache
    if not reset and _cache is not None:
        return _cache
    if reset:
        magma.frontend.coreir_.ResetCoreIR()
    c = magma.backend.coreir_.CoreIRContextSingleton().get_instance()
    if reset:
        c.load_library("commonlib")
        _cache = c
    return c

