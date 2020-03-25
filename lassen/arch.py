import json

class Arch():
    def __init__(self, input_width, output_width, num_inputs, num_outputs, num_alu, num_mul, num_reg, num_const_reg, num_mux_in0, num_mux_in1, num_reg_mux, num_output_mux, inputs, outputs, enable_input_regs, enable_output_regs):
        self.input_width = input_width
        self.output_width = output_width
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_alu = num_alu
        self.num_mul = num_mul
        self.num_reg = num_reg
        self.num_const_reg = num_const_reg
        self.num_mux_in0 = num_mux_in0
        self.num_mux_in1 = num_mux_in1
        self.num_reg_mux = num_reg_mux
        self.num_output_mux = num_output_mux
        self.inputs = inputs
        self.outputs = outputs
        self.modules = []
        self.regs = []
        self.const_regs = []
        self.enable_input_regs = enable_input_regs
        self.enable_output_regs = enable_output_regs
			
class module():
    def __init__(self, id, type_, in0, in1, in_width, out_width):
        self.id = id
        self.type_ = type_
        self.in0 = in0
        self.in1 = in1
        self.in_width = in_width
        self.out_width = out_width

class reg():
    def __init__(self, id, in_, width):
        self.id = id
        self.in_ = in_
        self.width = width

class const_reg():
    def __init__(self, id, width):
        self.id = id
        self.width = width


def read_arch(json_file_str):
    # with open('examples/test_json.json') as json_file:

    with open(json_file_str) as json_file:
        json_in = json.loads(json_file.read())
        num_alu = 0
        num_mul = 0
        num_reg = 0
        num_const_reg = 0
        num_mux_in0 = 0
        num_mux_in1 = 0
        num_reg_mux = 0
        modules_json = json_in['modules']
        modules = []
        const_regs = []
        regs = []
        inputs = []
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
                num_const_reg += 1
                new_const_reg = const_reg(module_json['id'], module_json.get('width', width))
                const_regs.append(new_const_reg)
            
            else:
                new_module = module( module_json['id'], module_json['type'], module_json['in0'], module_json.get('in1'), module_json.get('in_width', width), module_json.get('out_width', width))
                
                if new_module.type_ == "alu":
                    num_alu += 1
                elif new_module.type_ == "mul":
                    num_mul += 1
                elif not new_module.type_ == "add":
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

                if new_module.id in ids:
                    raise ValueError('Two modules with the same ID')
                else:
                    ids.append(new_module.id)

                modules.append(new_module)

        unique_inputs = [entry for entry in inputs if entry not in ids]
        num_inputs = len(unique_inputs)
        num_outputs = len(json_in['outputs'])

        print(unique_inputs)

        for module_ in modules:
            if not isinstance(module_.in0, list):
                module_.in0 = [module_.in0]
            if not isinstance(module_.in1, list):
                module_.in1 = [module_.in1]

        outputs = []
        num_output_mux = 0
        for out in json_in['outputs']:
            out_new = out
            if not isinstance(out, list):
                out_new = [out]
            
            if len(out_new) > 1:
                num_output_mux += 1

            outputs.append(out_new)


        arch = Arch(width, json_in.get('output_width', width), num_inputs, num_outputs, num_alu, num_mul, 
                    num_reg, num_const_reg, num_mux_in0, num_mux_in1, num_reg_mux, num_output_mux, unique_inputs, outputs, 
                    json_in.get('enable_input_regs', False), json_in.get('enable_output_regs', False))
        arch.modules = modules
        arch.regs = regs
        arch.const_regs = const_regs
        return arch


def graph_arch(arch: Arch):
    from graphviz import Digraph

    graph = Digraph()
    inputs_subgraph = Digraph()
    pe_subgraph = Digraph()
    outputs_subgraph = Digraph()
    inputs_subgraph.attr(rank='min')
    
    inputs_subgraph.attr('node', shape='circle')
    for input in arch.inputs:
        inputs_subgraph.node(str(input), str(input))

    graph.subgraph(inputs_subgraph)

    mux_in0_idx = 0
    mux_in1_idx = 0

    for module in arch.modules:
        if module.type_ == "alu":
            pe_subgraph.attr('node', shape='box')
            pe_subgraph.node(str(module.id), "alu")
        if module.type_ == "add":
            pe_subgraph.attr('node', shape='box')
            pe_subgraph.node(str(module.id), "add")
        elif module.type_ == "mul":
            pe_subgraph.attr('node', shape='box')
            pe_subgraph.node(str(module.id), "mul")
        
        if len(module.in0) > 1:
            pe_subgraph.attr('node', shape='invtrapezium')
            pe_subgraph.node("mux_in0_" + str(mux_in0_idx), "mux_in0_" + str(mux_in0_idx))

            for in0 in module.in0:
                pe_subgraph.edge(str(in0), "mux_in0_" + str(mux_in0_idx))

            pe_subgraph.edge("mux_in0_" + str(mux_in0_idx),str(module.id))  
            mux_in0_idx += 1
        else:
            pe_subgraph.edge(str(module.in0[0]), str(module.id))
    
        if len(module.in1) > 1:
            pe_subgraph.attr('node', shape='invtrapezium')
            pe_subgraph.node("mux_in1_" + str(mux_in1_idx), "mux_in1_" + str(mux_in1_idx))

            for in1 in module.in1:
                pe_subgraph.edge(str(in1), "mux_in1_" + str(mux_in1_idx))

            pe_subgraph.edge("mux_in1_" + str(mux_in1_idx),str(module.id))  
            mux_in1_idx += 1
        else:
            pe_subgraph.edge(str(module.in1[0]), str(module.id))


    # import pdb; pdb.set_trace()
    mux_reg_idx = 0
    for reg in arch.regs:
        pe_subgraph.attr('node', shape='box')
        pe_subgraph.node(str(reg.id), "reg")

        if len(reg.in_) > 1:
            pe_subgraph.attr('node', shape='invtrapezium')
            pe_subgraph.node("mux_reg_" + str(mux_reg_idx), "mux_reg_" + str(mux_reg_idx))

            for in_ in reg.in_:
                pe_subgraph.edge(str(in_), "mux_reg_" + str(mux_reg_idx))

            pe_subgraph.edge("mux_reg_" + str(mux_reg_idx), str(reg.id))  
            mux_reg_idx += 1
        else:
            pe_subgraph.edge(str(reg.in_[0]), str(reg.id))


    for reg in arch.const_regs:
        pe_subgraph.attr('node', shape='box')
        pe_subgraph.node(str(reg.id), "const")

    graph.subgraph(pe_subgraph)

    mux_out_idx = 0
    outputs_subgraph.attr(rank='max')
    outputs_subgraph.attr('node', shape='circle')
    for i, output in enumerate(arch.outputs):
        
        outputs_subgraph.node("out_" + str(i), "out" + str(i))
        outputs_subgraph.attr('node', shape='circle')
        if len(output) > 1:
            graph.attr('node', shape='invtrapezium')
            graph.node("mux_out_" + str(mux_out_idx), "mux_out_" + str(mux_out_idx))

            for out in output:
                graph.edge(str(out), "mux_out_" + str(mux_out_idx))

            graph.edge("mux_out_" + str(mux_out_idx), "out_" + str(i))
            mux_out_idx += 1
        else:
            graph.edge(str(output[0]), "out_" + str(i))


    graph.subgraph(outputs_subgraph)

    # print(graph.source)
    graph.render("arch_graph", view=False)
