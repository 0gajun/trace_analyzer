import pygraphviz as pgv

class Renderer:
  @classmethod
  def render_graph(cls, original_bbs, output_path):
    basic_blocks = cls.non_user_code_reduction(original_bbs)
    print(str(len(basic_blocks)))
    G=pgv.AGraph(directed=True, fontname='Arial')
    G.node_attr['shape'] = 'box'
    bbs = [bb.instructions_str() for bb in basic_blocks]
    G.add_nodes_from(bbs)
    prev_bb = None
    prev_bb_insn_str = ""
    for bb in basic_blocks:
      bb_insn_str = bb.instructions_str()
      if prev_bb and prev_bb_insn_str:
        G.add_edge(prev_bb_insn_str, bb_insn_str)
        G.get_node(bb_insn_str).attr['label'] = bb_insn_str
      if bb.is_user_code:
        G.get_node(bb_insn_str).attr['color']='red'
      prev_bb = bb
      prev_bb_insn_str = bb_insn_str

    print('start layout')
    G.layout(prog='dot')
    print('finished layout\nstart draw')
    G.draw(output_path)
    print('finished')

  @classmethod
  def non_user_code_reduction(cls, original_basic_blocks):
    user_code_bbs = []
    is_processing_user_code = False
    prev_bb = None
    for bb in original_basic_blocks:
      if bb.is_user_code:
        if not prev_bb.is_user_code:
          tmp_bb = prev_bb
          tmp_bb.instructions = cls.reduce_instructions(tmp_bb.instructions)
          user_code_bbs.append(tmp_bb)
        user_code_bbs.append(bb)
      else:
        if prev_bb != None and prev_bb.is_user_code:
          tmp_bb = bb
          tmp_bb.instructions = cls.reduce_instructions(tmp_bb.instructions)
          user_code_bbs.append(tmp_bb)
      prev_bb = bb
    return user_code_bbs

  @classmethod
  def reduce_instructions(cls, instructions):
    return instructions[0].split()[0] + '\\l...\\l' + instructions[-1].split()[0]

