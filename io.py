import sys

if len(sys.argv) != 2:
    raise IOError('filename not specified')
    sys.exit()


filename = sys.argv[1]

program = open(filename,'r')

instructions = []

for line in program:
    if line.startswith('#'):
        continue
    if line == '\n':
        continue
    if '#' in line:
        byte,comment = line.split(' #')
        instructions.append(int(byte.strip(),2))
    else:
        instructions.append(int(line.strip(),2))

print(instructions)

program.close()
