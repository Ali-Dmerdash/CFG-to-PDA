import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

def parser(input,var,terminals):
    """
    :type input: file
    :type var: set(string)
    :type terminals: set(string)
    :rtype: dict(string:list(string))
    """
    cfg = {}
    with open(input, 'r',encoding='utf-8') as file:
        for line in file:

            parts = line.split('->')
 
            variables = parts[0].strip()
            var.update(variables)

            productions = parts[1].split('|')
            productions = [prod.strip() for prod in productions]

            for symbol in parts[1].strip():
                if symbol.islower():
                    terminals.add(symbol)

            cfg[variables] = productions
        return cfg

def toPDA(cfg, var, terminals):
    """
    :type cfg: dict(string:list(string))
    :type var: set(string)
    :type terminals: set(string)
    :rtype: nx.MultiDiGraph
    """
    pda_graph = nx.MultiDiGraph()

    pda_graph.add_edge(1, 2, label=f"(Ɛ,Ɛ -> $)")

    pda_graph.add_edge(2, 3, label=f"(Ɛ,Ɛ -> {list(var)[0]})")

    main_loop_node = 3
    main_loop_str = ""

    single_productions = {}
    for key, value in cfg.items():
        single_productions[key] = [production for production in value if len(production) == 1]
        for production in single_productions[key]:
            value.remove(production)

    # print(cfg)
    # print(single_productions)

    for key, values in single_productions.items():
        for value in values:
            main_loop_str += f"(Ɛ,{key} -> {value})\n"
    
    for term in terminals:
        main_loop_str += f"({term},{term} -> Ɛ)\n"


    # print(main_loop_str)
    pda_graph.add_edge(main_loop_node, main_loop_node, label=main_loop_str)
    
    state_count = 3
    for variable, productions in cfg.items(): 
        for production in productions:
            first_letter = 1
            for i in range(len(production)- 1, -1, -1):

                if first_letter:
                    first_letter = 0
                    pda_graph.add_edge(main_loop_node, state_count+1, label=f"(Ɛ,{variable} -> {production[i]})")
                
                elif i == 0:
                    pda_graph.add_edge(state_count, main_loop_node, label=f"(Ɛ,Ɛ -> {production[i]})")
                    break

                else :
                    pda_graph.add_edge(state_count, state_count+1, label=f"(Ɛ,Ɛ -> {production[i]})")

                state_count+=1

    state_count += 1
    pda_graph.add_edge(main_loop_node, state_count,label="(Ɛ,$ -> Ɛ)",color="blue")

    pda_graph.nodes[state_count]["color"] = "blue"
    pda_graph.nodes[state_count]["shape"] = "doublecircle"

    return pda_graph




input = 'cfg.txt'
var = set()
terminals = set()

cfg = parser(input,var,terminals)

# print("Variables:", var)
# print("Terminals:", terminals)
# print("CFG:", cfg)

pda_graph = toPDA(cfg, var, terminals)
agraph = to_agraph(pda_graph)
agraph.layout('dot')
agraph.draw('pda_graph.png', prog='dot', args='-Gnodesep=1 -Granksep=1')