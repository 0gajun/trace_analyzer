import sys
from model.basic_block import BasicBlock
from parser import Parser
from graph_module.renderer import Renderer

def invalid_arg_err_msg():
  print('number of arguments is wrong')
  print('<cmd> <target_binary_path> <trace_file_path> <output_file_path>')

if __name__ == "__main__":
  if len(sys.argv) < 4:
    invalid_arg_err_msg()
    sys.exit(1)
  target_binary_path = sys.argv[1]
  trace_file_path = sys.argv[2]
  output_file_path = sys.argv[3]

  basic_blocks = Parser.parse(target_binary_path, trace_file_path)
  Renderer.render_graph(basic_blocks, output_file_path)
