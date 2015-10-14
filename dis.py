import subprocess
import sys

def is_user_code(hex_addr, conditions):
  for cond in conditions:
    if cond['min'] <= hex_addr and hex_addr <= cond['max']:
      return True
  return False

def get_raw_segment_addresses(target):
  command = 'readelf --segments %s | awk \'BEGIN { RS = ""; FS = "\\n"}; NR == 2\' | \
      awk \'{print $3 " " $6}\' | grep "0x"' % target

  # TODO: fix OS command injection valunerbility
  parsed = subprocess.check_output(command, shell = True, universal_newlines=True)
  return parsed.split('\n')

def prepare_user_code_conditions(target):
  conditions = []
  segment_addr_array = get_raw_segment_addresses(target)
  for segment_addr in segment_addr_array:
    addr_and_size = list(map(lambda x:int(x, 16), segment_addr.split()))
    if len(addr_and_size) < 2:
      continue
    cond = {'min' : addr_and_size[0], 'max' : (addr_and_size[0] + addr_and_size[1])}
    conditions.append(cond)
  return conditions

def get_insn_addr_from_trace_line(line):
  if not line.startswith('0x'):
    return -1
  return int(line.split(':')[0], 16)

def extract_user_code_trace_from_raw_trace(trace_file_path, conditions):
  is_processing_user_code = False
  is_in_block = False
  trace_file = open(trace_file_path, 'r')
  
  line = trace_file.readline()
  while line:
    addr = get_insn_addr_from_trace_line(line)
    if addr == -1 and is_processing_user_code:
      is_in_block = False
    else:
      if is_user_code(addr, conditions):
        if not is_processing_user_code:
          print('<<<<<<<<<<User Code<<<<<<<<<<<<<')
          is_processing_user_code = True
        if not is_in_block:
          print('IN:')
          is_in_block = True
        print(line, end='')
      elif is_processing_user_code:
        print('>>>>>>>>>Not User Code>>>>>>>>>>>')
        is_processing_user_code = False
    line = trace_file.readline()

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print('number of argument is wrong')
    sys.exit(1)
  target = sys.argv[1]
  trace_file_path = sys.argv[2]
  conditions = prepare_user_code_conditions(target)
  extract_user_code_trace_from_raw_trace(trace_file_path, conditions)

