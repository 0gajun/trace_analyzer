class BasicBlock:
  def __init__(self, _id, instructions, is_user_code):
    self._id = _id
    self.instructions = instructions
    self.next_bbs = []
    self.prev_bbs = []
    self.is_user_code = is_user_code

  def instructions_str(self):
    # return "BLOCK_ID:" + str(self._id)  + "\\l" + "".join(self.instructions)
    return "\\l" + "".join(self.instructions)