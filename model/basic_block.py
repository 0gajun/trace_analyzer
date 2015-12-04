import hashlib

class BasicBlock:
  def __init__(self, _id, instructions, is_program_code):
    self._id = _id
    self.instructions = instructions
    self.next_bbs = []
    self.prev_bbs = []
    self.is_program_code = is_program_code
    #self.key = hashlib.md5("".join(self.instructions).encode('utf-8')).hexdigest()
    self.key = "".join(self.instructions)

  def instructions_str(self):
    # return "BLOCK_ID:" + str(self._id)  + "\\l" + "".join(self.instructions)
    return "\\l" + "".join(self.instructions)

