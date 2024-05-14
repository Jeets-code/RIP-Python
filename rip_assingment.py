# RIP Assignment

import re

input_ports = []
output_ports = {}


# Read router files

def read_file(filename):
    lines = []
    try:
        file = open(filename, 'r')
    except:
        print("File not found")
        sys.exit()

    for line in file.readlines():
        line = re.split(', | |\n',line)
        lines.append(line)

    print(lines)
    return lines


# Make input port  list

def get_inputs(lines):
    
    #lines = read_file(filename)
    
    for i in range(1, len(lines[1]) -1):
        if int(lines[1][i]) in range(1024, 64000):
            if int(lines[1][i]) not in input_ports:
                input_ports.append(int(lines[1][i]))
        else:
            print('Invalid output port number')
            break
    
    print(input_ports)

# Make Output port dictionary



# Intialise table

lines = read_file("router1.cfg")
get_inputs(lines)

