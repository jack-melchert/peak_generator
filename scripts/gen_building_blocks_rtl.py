from peak_gen.sim import pe_arch_closure
from peak_gen.arch import read_arch, graph_arch
import magma as m
import sys, os
from peak import family
import glob
import subprocess

files = glob.glob("examples/building_blocks/**")

for filename in files:
    subprocess.run(["python", "scripts/gen_rtl_temp.py", filename])
