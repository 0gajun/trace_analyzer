from model.analysis_result import AnalysisResult
from model.basic_block import BasicBlock

# analysis controll flow
# chaining basic blocks according to trace
class FlowAnalyzer:
  def __init__(self, basic_blocks):
    self.bbs = basic_blocks
    self.bb_table = {}

  def analyze(self):
    self.reduce_non_program_code()
    first_bb = self.bbs[0]
    prev_bb = None
    for bb in self.bbs:
      prev_bb = self.process_bb(prev_bb, bb)

    return AnalysisResult(list(self.bb_table.values()), first_bb, prev_bb)

  def process_bb(self, prev_bb, bb):
    if bb.key not in self.bb_table:
      self.bb_table[bb.key] = bb
    else:
      bb = self.bb_table[bb.key]

    if prev_bb != None:
      prev_bb.next_bbs.append(bb)
      bb.prev_bbs.append(prev_bb)

    return bb

  # reduce non program code basic blocks to one basic block
  def reduce_non_program_code(self):
    reduced = []
    processing_non_program_code = False
    start_bb = None
    reduction_bb_count = 0
    prev_bb = None
    for bb in self.bbs:
      if bb.is_program_code:
        if processing_non_program_code:
          reduced.append(self.create_reduced_block(start_bb, prev_bb, reduction_bb_count))
          processing_non_program_code = False
          start_bb = None
          reduction_bb_count = 0
        reduced.append(bb)
      else:
        # Non Program code
        if not processing_non_program_code:
          start_bb = bb
          processing_non_program_code = True
      prev_bb = bb
      reduction_bb_count = reduction_bb_count + 1
    self.bbs = reduced

  def create_reduced_block(self, start_bb, end_bb, reduction_count):
    reduced_insns = start_bb.instructions[0] + '\\l...\\lreduction_count: ' + str(reduction_count) + '\\l...\\l' + end_bb.instructions[0]
    return BasicBlock(0, [reduced_insns], False)
