import pygraphviz as pgv

class Renderer:
  @classmethod
  def render_graph(cls, original_bbs, output_path):
    basic_blocks = cls.non_program_code_reduction(original_bbs)
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
      if bb.is_program_code:
        G.get_node(bb_insn_str).attr['color']='red'
      prev_bb = bb
      prev_bb_insn_str = bb_insn_str

    print('start layout')
    G.layout(prog='dot')
    print('finished layout\nstart draw')
    G.draw(output_path)
    print('finished')

  @classmethod
  def render(cls, basic_blocks, start_bb, output_file_path):
    G=pgv.AGraph(directed=True, fontname='Arial')
    G.node_attr['shape'] = 'box'
    bbs = [bb.instructions_str() for bb in basic_blocks]
    G.add_nodes_from(bbs)

    start_insn = start_bb.instructions_str()
    for bb in basic_blocks:
      bb_insn_str = bb.instructions_str()
      G.get_node(bb_insn_str).attr['label'] = bb_insn_str
      for next_bb in bb.next_bbs:
        G.add_edge(bb_insn_str, next_bb.instructions_str())
      if bb.is_program_code:
        G.get_node(bb_insn_str).attr['color']='red'
      if bb_insn_str == start_insn:
        G.get_node(bb_insn_str).attr['color']='green'

    print('start layout')
    G.layout(prog='dot')
    print('finished layout\nstart draw')
    G.draw(output_file_path)
    print('finished')

  @classmethod
  def non_program_code_reduction(cls, original_basic_blocks):
    program_code_bbs = []
    is_processing_program_code = False
    prev_bb = None
    for bb in original_basic_blocks:
      if bb.is_program_code:
        if not prev_bb.is_program_code:
          tmp_bb = prev_bb
          tmp_bb.instructions = cls.reduce_instructions(tmp_bb.instructions)
          program_code_bbs.append(tmp_bb)
        program_code_bbs.append(bb)
      else:
        if prev_bb != None and prev_bb.is_program_code:
          tmp_bb = bb
          tmp_bb.instructions = cls.reduce_instructions(tmp_bb.instructions)
          program_code_bbs.append(tmp_bb)
      prev_bb = bb
    return program_code_bbs

  @classmethod
  def reduce_instructions(cls, instructions):
    return instructions[0].split()[0] + '\\l...\\l' + instructions[-1].split()[0]

