from collections import deque

from intcode import read_program, run_program

start_program = read_program('input.txt')

walk_cmd_ascii = [ord(x) for x in list('WALK')] + [10]
run_cmd_ascii = [ord(x) for x in list('RUN')] + [10]

def convert_cmd_to_ascii(cmd_str : str):
    return [ord(x) for x in list(cmd_str)] + walk_cmd_ascii

def convert_cmd_to_ascii_run(cmd_str : str):
    return [ord(x) for x in list(cmd_str)] + run_cmd_ascii

# jump only if D is not a hole and any area between IS a hole
cmd = """NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
AND D J
"""
cmd_ascii = convert_cmd_to_ascii(cmd)
p_input = deque(cmd_ascii)
output = list(run_program(start_program, p_input))
print(output[-1])

#part 2
# jump only if D is not a hole and any area between IS a hole
# jump only position 5 is not a hole or if position 8 is not a hole
# Reverse via Not T T
cmd_part2 = """NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT E T
NOT T T
OR H T
AND T J
"""
cmd_ascii_part2 = convert_cmd_to_ascii_run(cmd_part2)
p_input_part2 = deque(cmd_ascii_part2)
output_part2 = list(run_program(start_program, p_input_part2))
#fail_output_str = ''.join(['-' if chr(x) == '.' else chr(x) for x in output_part2[:-1]])
#print(fail_output_str, end = '')
print(output_part2[-1])