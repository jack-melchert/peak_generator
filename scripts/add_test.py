from peak_gen.sim import fp_pe_arch_closure, pe_arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
from peak_gen.peak_wrapper import wrapped_peak_class
from peak import Peak, family_closure, Const
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
from hwtypes import BitVector, Tuple, Bit
import sys
from peak import family
from peak.family import AbstractFamily
from peak.mapper import RewriteRule
from peak.assembler.assembled_adt import  AssembledADT
from peak.assembler.assembler import Assembler
import pdb
import json
import copy 
from pysmt.logics import QF_BV
import time
# from lassen.sim import PE_fc
# from metamapper.irs.coreir.ir import gen_peak_CoreIR



arch = read_arch(str(sys.argv[1]))
# PE_fc = pe_arch_closure(arch)
PE_fc = wrapped_peak_class(arch)

    


