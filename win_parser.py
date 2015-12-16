from parser import Parser

class WinParser(Parser):
  @classmethod
  def prepare_program_code_conditions(cls, target):
    conditions = []
    conditions.append({'min': 0x0, 'max': 0x60000000})
    return conditions
