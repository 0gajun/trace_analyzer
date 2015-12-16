import sys
from model.basic_block import BasicBlock
from parser import Parser
from win_parser import WinParser
from flow_analyzer import FlowAnalyzer
from graph_module.renderer import Renderer

def invalid_arg_err_msg():
  print('number of arguments is wrong')
  print('<cmd> <target_binary_path> <trace_file_path> <output_file_path>')

def main():
  if len(sys.argv) < 4:
    invalid_arg_err_msg()
    sys.exit(1)
  target_binary_path = sys.argv[1]
  trace_file_path = sys.argv[2]
  output_file_path = sys.argv[3]

  # Parse logfile and split into basic block objects
  #basic_blocks = Parser.parse(target_binary_path, trace_file_path)
  basic_blocks = WinParser.parse(target_binary_path, trace_file_path)
  print("basic_blocks: " + str(len(basic_blocks)))
  # chain basic blocks according to traced control flow
  analysis_result = FlowAnalyzer(basic_blocks).analyze()
  print("analysis_result: " + str(len(analysis_result.basic_blocks)))

  # delete unused references
  del basic_blocks

  # Render graph
  Renderer.render(analysis_result.basic_blocks, analysis_result.first_block, output_file_path)

if __name__ == "__main__":
  main()
