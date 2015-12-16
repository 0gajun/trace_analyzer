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
    i = 0

    while i < len(self.bbs):
      start_index = i
      start_bb = self.bbs[i]
      # 連続するブロックの個数を取得
      count = self.get_block_count(start_bb.is_program_code, start_index)

      if start_bb.is_program_code:
        reduced.extend(self.bbs[start_index:start_index + count])
      else:
        last_bb = self.bbs[start_index + count - 1]
        reduced.append(self.create_reduced_block(start_bb, last_bb, count))

      i = i + count

    self.bbs = reduced

  # is_program_codeと一致するstart_indexから始まる連続するブロックの数を返す
  def get_block_count(self, is_program_code, start_index):
    i = start_index
    while i < len(self.bbs):
      bb = self.bbs[i]

      # 引数のblock種別と変わったら連続でないと判断しbreak
      # 今回のループのブロックは含めないため i - 1する
      if bb.is_program_code != is_program_code:
        i = i - 1
        break
      # 最終ブロックであればbreak
      if self.bbs[-1] == bb:
        break
      i = i + 1
    return i - start_index + 1

  def create_reduced_block(self, start_bb, end_bb, reduction_count):
    reduced_insns = start_bb.instructions[0] + '\\l...\\lreduction_count: ' + str(reduction_count) + '\\l...\\l' + end_bb.instructions[len(end_bb.instructions) - 1]
    return BasicBlock(0, [reduced_insns], False)
