import pygraphviz as pgv

class Renderer:
  def render_graph(basic_blocks, output_path):
    G=pgv.AGraph(directed=True)
    G.node_attr['shape'] = 'box'

    G.add_nodes_from([bb.instructions_str() for bb in basic_blocks])
    prev_bb = None
    prev_bb_insn_str = ""
    for bb in basic_blocks:
      bb_insn_str = bb.instructions_str()
      if prev_bb and prev_bb_insn_str:
        G.add_edge(prev_bb_insn_str, bb_insn_str)
      if bb.is_user_code:
        G.get_node(bb_insn_str).attr['color']='green'
      prev_bb = bb
      prev_bb_insn_str = bb_insn_str

    print('start layout')
    G.layout(prog='dot')
    print('finished layout\nstart draw')
    G.draw('graph.png')
    print('finished')
