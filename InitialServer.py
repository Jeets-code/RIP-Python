import socket, select, time, random, re, math, sys, json
from threading import Thread

global route_table, output_ports, route_table, self_name, timeout
input_ports = []
output_ports = {}



# Read router files

def read_file(filename):
    lines = []
    router_id = int(filename[6])
    try:
        file = open(filename, 'r')
    except:
        print("File not found")
        sys.exit()

    for line in file.readlines():
        line = re.split(', | |\n',line)
        lines.append(line)

    #print(lines)
    return lines, router_id

# Make input port  list

def get_inputs(lines):
    
    #lines = read_file(filename)
    
    for i in range(1, len(lines[1]) -1):
        if int(lines[1][i]) in range(1024, 64000):
            if int(lines[1][i]) not in input_ports:
                input_ports.append(int(lines[1][i]))
        else:
            print('Invalid input port number')
            break
    
    return input_ports

# Make Output port dictionary. Return port numbur, next hop and cost
#{destname: port}
#global route_table = output_ports organised to be {name: (next, cost)}

def get_outputs(lines):
    #lines = read_file(filename)
    
    for i in range(1,len(lines[2])):
        output_line = lines[2][i]
        output = output_line.split('-')
        output_port = int(output[0])
        cost = int(output[1])
        dest_name = int(output[2])
        
        if output_port in range(1024,64000):
            if dest_name not in output_ports.keys():
                output_ports[dest_name] = output_port
                route_table[dest_name] = (dest_name, cost)
        else:
            print('Invalid output port number')
            break
        
    return output_ports, dest_name, cost
    
    


# Intialise empty table


def route_table(output_ports, dest_name, cost):
    route_table = {}
    time_out = 0
    flag = False
    route_table[next_hop] = [cost, dest_name, flag, time_out]
    return route_table



def server(inports, output_ports):

    #=====================Input Ports==========================
    global sock_list
    sock_list = []
    for i in range(len(inports)):
        sock_list.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        sock_list[i].bind(("", inports[i]))
    print("Output connected!")
    
    Thread(target = main_routing).start()  
    Thread(target = wait_30).start()
          
    #Receiving other packets
    
def main_routing(route_table):
    global route_table, sock_list
    print("Ready to receive data")
    while True:
        ready_socks, x, y = select.select(sock_list, [], [])
        for sock in ready_socks:
            data, addr = sock.recvfrom(1024)
            sock_ip, port_no = sock.getsockname()
            data, source = data_parse(data, port_no)
            #data  is currently in the form dest: cost 
            assume_dead(False, source)
            changed = False
            for dest in data:
                if int(dest) in route_table:
                    #if new cost is lower
                    if data[dest] + route_table[source][1] < route_table[int(dest)][1] and data[dest] <= 15:
                        route_table[int(dest)] = (source, data[dest] + route_table[source][1])
                        changed = True
                    #Else if source router changes metrics
                    elif route_table[int(dest)][0] == source and route_table[int(dest)][0] != data[dest] + route_table[source][1]:
                        route_table[int(dest)] = (source, data[dest] + route_table[source][1])                   
                else:
                    route_table[int(dest)] = (source, data[dest] + route_table[source][1])
                    changed = True
            if changed:
                send_routing()
                #print("The routing table is:")
                #print(route_table)
    return route_table

def rip_header(router_id):
    # header in line with RIP specs
    command = 2
    version = 2
    zero = 0
    header = [command, version, zero]
    return header 


#def rip_entry(route_table):

##Doesn't work 
    #entry = []
    #for dest in route_table.keys():
        #cost = route_table[dest][1]
        #entry.append((cost, cost))
    #return entry


def rip_packet(header, entry):
    #Combine the header and the entry in a packet
    packet = {}
    packet['header'] = haeder
    packet['entry'] = entry
    return packet

#check if the packet is valid or not?????

#sprate function for printing the table
#Destinatin | Cost | Next Hop | Time out |
               

def data_parse(data, port_no):
    #Error checks inputs and returns data dictionary and source name
    # Need to declare source address in initial thing
    #More here once we start adding the real rip stuff
    data = json.loads(data.decode())
    source = list(data)[0]
    #print("Received:")
    #print(data)
    #print("From {}".format(source))
    return data, int(source)

def wait_30():
    while True:
        time.sleep(timeout + (random.randint(0,200) // 100))
        send_routing()

#outports is destname: ports. route_table is destname: next, cost
def send_routing():
    global route_table, output_ports
    for dest in output_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = (socket.gethostname(), output_ports[dest])
        
        assume_dead(True, dest)
        
        # temporary for testing.
        localtable = {self_name: 0}
        
        for goal in route_table:
            if dest == goal:
                pass
            #if we are sending to the nexthop:
            elif dest == route_table[goal][0]:
                localtable[goal] = 16
            else:
                localtable[goal] = route_table[goal][1]
            # do some more stuff to encode localtable
            # print(localtable)
        sock.sendto(json.dumps(localtable).encode(), address)
        sock.close()
    #print("Sent data to connected ports")
    
dead = {}
last_metric = {}

def assume_dead(dying, router):
    #this is a really dumb idea that might work, 
    # Where every time router sends stuff it increments, and resets every receive
    if dying:
        if router in dead:
            dead[router] += 1
            if dead[router] == 5:
                print("Contact lost with router {}".format(router))
                last_metric[router] = route_table[router]
                route_table[router] = (router, 16)
                print("Route table changed to:")
                print(route_table)
                send_routing()
        else: 
            dead[router] = 1
    else: 
        if router in dead and dead[router] >= 5:
            print("Router {} reconnected. Restoring to last known metric".format(router))
            route_table[router] = last_metric[router]         
        dead[router] = 0    
        
        
        
        
        
        
        
        
def main(filename):
    #Main function to run everything
    ##Can possibly timeout here 
    lines = read_file(filename)
    input_ports = get_inputs(lines)
    output_ports, dest_name, cost = get_outputs(lines)
    route_table(output_ports, dest_name, cost)
    routing_table = main_routing(route_table)
    server(input_ports, output_ports)
                    

filename = sys.argv[1]
main(filename)


