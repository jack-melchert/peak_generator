import json

class Arch():
    def __init__(self, input_width, output_width, num_inputs, num_bit_inputs, num_outputs, num_bit_outputs, num_alu, num_mul, num_add, num_reg, num_mux, num_const_inputs, num_mux_in0, num_mux_in1, num_mux_sel, num_reg_mux, num_output_mux, inputs, bit_inputs, outputs, bit_outputs, enable_input_regs, enable_output_regs):
        self.input_width = input_width
        self.output_width = output_width
        self.num_inputs = num_inputs
        self.num_bit_inputs = num_bit_inputs
        self.num_outputs = num_outputs
        self.num_bit_outputs = num_bit_outputs
        self.num_alu = num_alu
        self.num_mul = num_mul
        self.num_add = num_add
        self.num_reg = num_reg
        self.num_mux = num_mux
        self.num_const_inputs = num_const_inputs
        self.num_mux_in0 = num_mux_in0
        self.num_mux_in1 = num_mux_in1
        self.num_mux_sel = num_mux_sel
        self.num_reg_mux = num_reg_mux
        self.num_output_mux = num_output_mux
        self.inputs = inputs
        self.bit_inputs = bit_inputs
        self.outputs = outputs
        self.bit_outputs = bit_outputs
        self.modules = []
        self.regs = []
        self.const_inputs = []
        self.enable_input_regs = enable_input_regs
        self.enable_output_regs = enable_output_regs
			
class module():
    def __init__(self, id, type_, in0, in1, in_width, out_width, sel=[""]):
        self.id = id
        self.type_ = type_
        self.in0 = in0
        self.in1 = in1
        self.sel = sel
        self.in_width = in_width
        self.out_width = out_width

class reg():
    def __init__(self, id, in_, width):
        self.id = id
        self.in_ = in_
        self.width = width

class const_input():
    def __init__(self, id, width):
        self.id = id
        self.width = width


def read_arch(json_file_str):

    with open(json_file_str) as json_file:
        json_in = json.loads(json_file.read())
        num_alu = 0
        num_add = 0
        num_mul = 0
        num_reg = 0
        num_mux = 0
        num_const_inputs = 0
        num_mux_in0 = 0
        num_mux_in1 = 0
        num_mux_sel = 0 
        num_reg_mux = 0
        modules_json = json_in['modules']
        modules = []
        const_inputs = []
        regs = []
        inputs = []
        bit_inputs = []
        ids = []
        width = json_in.get('input_width', 16)

        for module_json in modules_json:
            if module_json['type'] == "reg":
                num_reg += 1
                new_reg = reg(module_json['id'], module_json['in'], module_json.get('width', width))
                
                if not isinstance(new_reg.in_, list):
                    new_reg.in_ = [new_reg.in_]

                for in0 in new_reg.in_:
                    if in0 not in inputs:
                        inputs.append(in0)
                if len(new_reg.in_) > 1:
                    num_reg_mux += 1

                if new_reg.id in inputs:
                    inputs.remove(new_reg.id)

                if new_reg.id in ids:
                    raise ValueError('Two modules with the same ID')
                else:
                    ids.append(new_reg.id)

                regs.append(new_reg)
            elif module_json['type'] == "const":
                num_const_inputs += 1
                new_const_input = const_input(module_json['id'], module_json.get('width', width))

                if new_const_input.id in inputs:
                    inputs.remove(new_const_input.id)

                if new_const_input.id in ids:
                    raise ValueError('Two modules with the same ID')
                else:
                    ids.append(new_const_input.id)

                const_inputs.append(new_const_input)
            
            else:
                new_module = module( module_json['id'], module_json['type'], module_json['in0'], module_json.get('in1'), module_json.get('in_width', width), module_json.get('out_width', width), module_json.get('sel'))
                
                if new_module.type_ == "alu":
                    num_alu += 1
                elif new_module.type_ == "mul":
                    num_mul += 1
                elif new_module.type_ == "mux":
                    num_mux += 1
                elif new_module.type_ == "add":
                    num_add += 1
                else:
                    raise ValueError('Unrecognized module type in specification')

                if not isinstance(new_module.in0, list):
                    new_module.in0 = [new_module.in0]
                for in0 in new_module.in0:
                    if in0 not in inputs:
                        inputs.append(in0)
                if len(new_module.in0) > 1:
                    num_mux_in0 += 1

                if not isinstance(new_module.in1, list):
                    new_module.in1 = [new_module.in1]
                for in1 in new_module.in1:
                    if in1 not in inputs:
                        inputs.append(in1)
                if len(new_module.in1) > 1:
                    num_mux_in1 += 1

                if new_module.type_ == "mux":
                    if not isinstance(new_module.sel, list):
                        new_module.sel = [new_module.sel]
                    for sel in new_module.sel:
                        if sel not in bit_inputs:
                            bit_inputs.append(sel)
                    if len(new_module.sel) > 1:
                        num_mux_sel += 1

                if new_module.id in ids:
                    raise ValueError('Two modules with the same ID')
                else:
                    ids.append(new_module.id)

                modules.append(new_module)

        unique_inputs = sorted([entry for entry in inputs if entry not in ids])
        unique_bit_inputs = sorted([entry for entry in bit_inputs if entry not in ids])
        num_inputs = len(unique_inputs)
        num_bit_inputs = len(unique_bit_inputs)
        num_outputs = len(json_in['outputs'])
        num_bit_outputs = len(json_in['bit_outputs'])

        print(unique_inputs)
        print(unique_bit_inputs)
        for module_ in modules:
            if not isinstance(module_.in0, list):
                module_.in0 = [module_.in0]
            if not isinstance(module_.in1, list):
                module_.in1 = [module_.in1]
            if not isinstance(module_.sel, list):
                module_.sel = [module_.sel]

        outputs = []
        num_output_mux = 0
        for out in json_in['outputs']:
            out_new = out
            if not isinstance(out, list):
                out_new = [out]
            
            if len(out_new) > 1:
                num_output_mux += 1

            outputs.append(out_new)

        bit_outputs = []
        for bit_out in json_in['bit_outputs']:
            bit_outputs.append(bit_out)

        arch = Arch(width, json_in.get('output_width', width), num_inputs, num_bit_inputs, num_outputs, num_bit_outputs, num_alu, num_mul, num_add,
                    num_reg, num_mux, num_const_inputs, num_mux_in0, num_mux_in1, num_mux_sel, num_reg_mux, num_output_mux, unique_inputs, unique_bit_inputs, outputs, bit_outputs, 
                    json_in.get('enable_input_regs', False), json_in.get('enable_output_regs', False))
        arch.modules = modules
        arch.regs = regs
        arch.const_inputs = const_inputs
        return arch


def graph_arch(arch: Arch):
    from graphviz import Digraph

    graph = Digraph()
    inputs_subgraph = Digraph()
    pe_subgraph = Digraph()
    outputs_subgraph = Digraph()
    inputs_subgraph.attr(rank='min')
    
    for input in arch.inputs:
        inputs_subgraph.node(str(input), str(input), shape='circle')

    for bit_input in arch.bit_inputs:
        inputs_subgraph.node(str(bit_input), str(bit_input), shape='circle')

    graph.subgraph(inputs_subgraph)

    mux_in0_idx = 0
    mux_in1_idx = 0
    mux_sel_idx = 0

    for module in arch.modules:
        if module.type_ == "alu":
            pe_subgraph.node(str(module.id), "alu", shape='box')
        elif module.type_ == "add":
            pe_subgraph.node(str(module.id), "add", shape='box')
        elif module.type_ == "mul":
            pe_subgraph.node(str(module.id), "mul", shape='box')
        elif module.type_ == "mux":
            pe_subgraph.node(str(module.id), "mux", shape='box')
                
            if len(module.sel) > 1:
                pe_subgraph.node("mux_sel_" + str(mux_sel_idx), "mux", shape='invtrapezium')

                for sel in module.sel:
                    pe_subgraph.edge(str(sel), "mux_sel_" + str(mux_sel_idx), style="dashed")

                pe_subgraph.edge("mux_sel_" + str(mux_sel_idx),str(module.id), style="dashed")  
                mux_sel_idx += 1
            else:
                pe_subgraph.edge(str(module.sel[0]), str(module.id), style="dashed")
        
        if len(module.in0) > 1:
            pe_subgraph.node("mux_in0_" + str(mux_in0_idx), "mux", shape='invtrapezium')

            for in0 in module.in0:
                pe_subgraph.edge(str(in0), "mux_in0_" + str(mux_in0_idx))

            pe_subgraph.edge("mux_in0_" + str(mux_in0_idx),str(module.id))  
            mux_in0_idx += 1
        else:
            pe_subgraph.edge(str(module.in0[0]), str(module.id))
    
        if len(module.in1) > 1:
            pe_subgraph.node("mux_in1_" + str(mux_in1_idx), "mux", shape='invtrapezium')

            for in1 in module.in1:
                pe_subgraph.edge(str(in1), "mux_in1_" + str(mux_in1_idx))

            pe_subgraph.edge("mux_in1_" + str(mux_in1_idx),str(module.id))  
            mux_in1_idx += 1
        else:
            pe_subgraph.edge(str(module.in1[0]), str(module.id))


    mux_reg_idx = 0
    for reg in arch.regs:
        pe_subgraph.node(str(reg.id), "reg", shape='box')

        if len(reg.in_) > 1:
            pe_subgraph.node("mux_reg_" + str(mux_reg_idx), "mux", shape='invtrapezium')

            for in_ in reg.in_:
                pe_subgraph.edge(str(in_), "mux_reg_" + str(mux_reg_idx))

            pe_subgraph.edge("mux_reg_" + str(mux_reg_idx), str(reg.id))  
            mux_reg_idx += 1
        else:
            pe_subgraph.edge(str(reg.in_[0]), str(reg.id))


    for const_idx, reg in enumerate(arch.const_inputs):
        pe_subgraph.node(str(reg.id), "const" + str(const_idx), shape='box')

    graph.subgraph(pe_subgraph)

    mux_out_idx = 0
    outputs_subgraph.attr(rank='max')
    for i, output in enumerate(arch.outputs):
        
        outputs_subgraph.node("out_" + str(i), "out" + str(i), shape='circle')
        if len(output) > 1:
            graph.node("mux_out_" + str(mux_out_idx), "mux", shape='invtrapezium')

            for out in output:
                graph.edge(str(out), "mux_out_" + str(mux_out_idx))

            graph.edge("mux_out_" + str(mux_out_idx), "out_" + str(i))
            mux_out_idx += 1
        else:
            graph.edge(str(output[0]), "out_" + str(i))

    for i, output in enumerate(arch.bit_outputs):
        
        outputs_subgraph.node("bit_out_" + str(i), "bit_out" + str(i), shape='circle')
        graph.edge(str(output), "bit_out_" + str(i), style="dashed")


    graph.subgraph(outputs_subgraph)

    # print(graph.source)
    graph.render("arch_graph", view=False)