import subprocess
from model.basic_block import BasicBlock

class Parser:
  @classmethod
  def parse(cls, target_binary_path, trace_file_path):
    conditions = cls.prepare_user_code_conditions(target_binary_path)
    return cls.parse_raw_trace_to_basic_blocks(trace_file_path, conditions)

  @classmethod
  def is_user_code(cls, hex_addr, conditions):
    for cond in conditions:
      if cond['min'] <= hex_addr and hex_addr <= cond['max']:
        return True
    return False

  @classmethod
  def get_raw_segment_addresses(cls, target):
    command = 'readelf --segments %s | awk \'BEGIN { RS = ""; FS = "\\n"}; NR == 2\' | \
        awk \'{print $3 " " $6}\' | grep "0x"' % target
    # TODO: fix OS command injection valunerbility
    return subprocess.check_output(command, shell = True, universal_newlines=True).split('\n')

  @classmethod
  def prepare_user_code_conditions(cls, target):
    conditions = []
    segment_addr_array = cls.get_raw_segment_addresses(target)
    for segment_addr in segment_addr_array:
      addr_and_size = [int(x, 16) for x in segment_addr.split()]
      if len(addr_and_size) < 2:
        continue
      cond = {'min' : addr_and_size[0], 'max' : (addr_and_size[0] + addr_and_size[1])}
      conditions.append(cond)
    return conditions

  @classmethod
  def get_insn_addr_from_trace_line(cls, line):
    if not line.startswith('0x'):
      return -1
    return int(line.split(':')[0], 16)

  @classmethod
  def gen_basic_block(cls, _id, instructions, is_user_code):
    return BasicBlock(_id, instructions, is_user_code)

  @classmethod
  def parse_raw_trace_to_basic_blocks(cls, trace_file_path, conditions):
    trace_file = open(trace_file_path, 'r')
    basic_block_id = 0
    is_processing_user_code = False
    basic_blocks = []
    instructions = []
    
    line = trace_file.readline()
    while line:
      addr = cls.get_insn_addr_from_trace_line(line)
      if addr == -1:
        if instructions:
          basic_blocks.append(cls.gen_basic_block(basic_block_id, instructions, is_processing_user_code))
          basic_block_id = basic_block_id + 1
          instructions = []
      else:
        if cls.is_user_code(addr, conditions):
          is_processing_user_code = True
        else:
          is_processing_user_code = False
        instructions.append(line.replace('\n', '\\l'))
      line = trace_file.readline()
    return basic_blocks
