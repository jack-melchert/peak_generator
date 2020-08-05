from peak.family import *
import hwtypes
import inspect
import os
import logging

from peak import Peak, family_closure, name_outputs
from peak import family
from peak.family import AbstractFamily
from hwtypes import Tuple

from .isa import inst_arch_closure
from .sim import fp_pe_arch_closure, pe_arch_closure

def exec_source(source, name, globals):
    path = ".ast_tools"
    file_name = os.path.join(path, f"{name}.py")
    print(file_name)
    os.makedirs(path, exist_ok=True)
    with open(file_name, 'w') as fp:
        fp.write(source)
    try:
        code = compile(source, filename=file_name, mode='exec')
    except Exception as e:
        logging.exception("Error compiling source")
        raise e from None
    _locals = {}
    try:
        exec(code, globals, _locals)
    except Exception as e:
        logging.exception("Error executing code")
        raise e from None

    #Need to write out a file, then exec using 'compile'
    return _locals[name]

def wrapped_peak_class(arch, fp=False):

    if fp:
        PE_fc = fp_pe_arch_closure(arch)
    else:
        PE_fc = pe_arch_closure(arch)
    Inst_fc = inst_arch_closure(arch)

    inputs = PE_fc.Py.input_t
    outputs = PE_fc.Py.output_t

    new_inputs = {}

    instr_name = 'inst'
    instr_type = inputs.field_dict['inst']

    new_inputs[instr_name] = inputs[instr_name]

    if fp:
        new_inputs_str = "fp_vals : fp_vals_t, inst : Inst, "
        pe_call_inputs = "fp_vals, inst, "
    else:
        new_inputs_str = "inst : Inst, "
        pe_call_inputs = "inst, "

    tuple_inputs_str = ""
    constructed_tuples = ""


    for name, type_ in inputs.field_dict.items(): 
        if name != instr_name and name != "fp_vals":

            if issubclass(type_, hwtypes.Tuple):
                tuple_inputs_str += "    " + name + "_tuple_t = Tuple["
                pe_call_inputs += name + "_constructed, "
                constructed_tuples += name + "_constructed = " + name + "_constructor(*["

                for ind, i in enumerate(inputs[name]):
                    if issubclass(i, hwtypes.BitVector):
                        new_inputs[name + str(ind)] = "Data"
                        new_inputs_str += name + str(ind) + " : Data, "
                        tuple_inputs_str += "Data, "
                        width = len(i)
                        constructed_tuples += name + str(ind) + ", "
                    elif issubclass(i, hwtypes.Bit):
                        new_inputs[name + str(ind)] = "Bit"
                        new_inputs_str += name + str(ind) + " : Bit, "
                        tuple_inputs_str += "Bit, "
                        constructed_tuples += name + str(ind) + ", "
                
                tuple_inputs_str = tuple_inputs_str[:-2]
                tuple_inputs_str += "]\n    "+name+"_constructor = family.get_constructor("+name+"_tuple_t)\n"
                constructed_tuples = constructed_tuples[:-2]
                constructed_tuples += "])\n            "
            else:
                if issubclass(type_, hwtypes.BitVector):
                    new_inputs[name] = "Data"
                    new_inputs_str += name + " : Data, "
                    width = len(type_)
                else:
                    new_inputs[name] = "Bit"
                    new_inputs_str += name + " : Bit, "
                pe_call_inputs += name + ", "

    pe_call_inputs = pe_call_inputs[:-2]
    new_inputs_str = new_inputs_str[:-2]


    outputs_str = ""
    outputs_type_str = ""
    new_outputs_str = ""
    outputs_expanded = ""
    named_outputs = "@name_outputs("

    for idx, (name, type_) in enumerate(outputs.field_dict.items()): 
        
        if issubclass(type_, hwtypes.Tuple):
            outputs_type_str += str(name) + ", "
            
            for ind, i in enumerate(outputs[name]):
                if issubclass(i, hwtypes.BitVector):
                    outputs_str += "Data, "
                    out_width = len(i)
                    named_outputs += f"{name}_{ind} = Data, "
                    outputs_expanded += f"{name}[{ind}], "
                elif issubclass(i, hwtypes.Bit):
                    outputs_str += "Bit, "
                    named_outputs += f"{name}_{ind} = Bit, "
                    outputs_expanded += f"{name}[{ind}], "
        elif issubclass(type_, hwtypes.BitVector):
            outputs_str += "Data, "
            outputs_type_str += str(name) + ", "
            outputs_expanded += f"{name}, "
            named_outputs += str(name) + " = Data, "
        elif issubclass(type_, hwtypes.Bit):
            outputs_str += "Bit, "
            outputs_type_str += str(name) + ", "
            outputs_expanded += f"{name}, "
            named_outputs += str(name) + " = Bit, "
            

    named_outputs = named_outputs[:-2]
    named_outputs += ")"
    outputs_str = outputs_str[:-2]
    outputs_type_str = outputs_type_str[:-2]
    outputs_expanded = outputs_expanded[:-2]

    if fp:
        fp_str = '''
    from hwtypes import Product
    class fp_val(Product):
        res = Data
        res_p = Bit
        Z = Bit
        N = Bit
        C = Bit
        V = Bit        

    fp_vals_t = Tuple[(fp_val for _ in range('''+str(arch.num_fp_alu)+'''))]
'''
    else:
        fp_str = ""

    new_peak_class = '''
@family_closure
def PE_wrapped_fc(family: AbstractFamily):
    Data = family.BitVector['''+ str(width) +''']
    Bit = family.Bit
''' + fp_str + '''
    Inst = Inst_fc(family)
''' + tuple_inputs_str + '''
    @family.assemble(locals(), globals())
    class PE_wrapped(Peak):
        def __init__(self):
            self.PE : PE_fc(family) = PE_fc(family)()
        '''+named_outputs+'''
        def __call__(self, ''' + new_inputs_str + ''') -> (''' + outputs_str + '''):
            ''' + constructed_tuples + '''
            ''' + outputs_type_str + ''' = self.PE(''' + pe_call_inputs + ''')
            return ''' + outputs_expanded + '''
    
    return PE_wrapped
'''
    # print(new_peak_class)
    _globals = dict(
        Peak=Peak,
        AbstractFamily=AbstractFamily,
        family_closure=family_closure,
        name_outputs=name_outputs,
        family=family,
        Inst_fc=Inst_fc,
        # Inst=Inst,
        PE_fc=PE_fc,
        Tuple=Tuple
    )

    return exec_source(new_peak_class, "PE_wrapped_fc", _globals)