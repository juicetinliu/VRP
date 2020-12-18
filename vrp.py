import xml.etree.ElementTree as ET 
import math,copy

# CREATING THE INSTANCE FILE
# vrp_source = 'A/A-n32-k5'
vrp_source = 'B/B-n31-k5'
# vrp_source = 'P/P-n40-k5'
# vrp_source = 'B/B-n51-k7'

nodes = []
requests = []

def generate_instance_xml():
    vrp_file = open(vrp_source + '.vrp', 'r') 
    vrp_lines = vrp_file.readlines() 
    
    takenodes = False
    takerequests = False
    capacity = 0

    for i, line in enumerate(vrp_lines):
        if takerequests:
            if "DEPOT_SECTION" in line:
                takerequests = False
            else:
                requests.append(tuple([int(x) for x in line.split()]))
        if takenodes:
            if "DEMAND_SECTION" in line:
                takenodes = False
                takerequests = True
            else:
                nodes.append(tuple([int(x) for x in line.split()]))
        if "NODE_COORD_SECTION" in line:
            takenodes = True
        if "CAPACITY" in line:
            capacity = int(line.split(':')[1])

    instance = ET.Element('instance')

    information = ET.SubElement(instance, 'info')
    dataset = ET.SubElement(information, 'dataset')
    name = ET.SubElement(information, 'name')
    dataset.text = "LmAo"
    name.text = "LuL"

    node_network = ET.SubElement(instance, 'network') 
    node_nodes = ET.SubElement(node_network, 'nodes')

    for node in nodes:
        node_el = ET.SubElement(node_nodes, 'node') 
        node_el.set('id', str(node[0] - 1))
        if(node[0] == 1):
            node_el.set('type', "0")
        else:
            node_el.set('type', "1")
        x = ET.SubElement(node_el, 'cx') 
        y = ET.SubElement(node_el, 'cy') 
        x.text = str(node[1])
        y.text = str(node[2])

    fleet = ET.SubElement(instance, 'fleet') 
    vehicle_profile = ET.SubElement(fleet, 'vehicle_profile') 
    vehicle_profile.set('type', "0")
    dep_node = ET.SubElement(vehicle_profile, "departure_node") 
    arr_node = ET.SubElement(vehicle_profile, "arrival_node") 
    vehicle_cap = ET.SubElement(vehicle_profile, "capacity")
    dep_node.text = '1'
    arr_node.text = '1'
    vehicle_cap.text = str(capacity)

    node_requests = ET.SubElement(instance, 'requests') 

    for i,request in enumerate(requests[1:]):
        request_el = ET.SubElement(node_requests, 'request') 
        request_el.set('id', str(i))
        request_el.set('node', str(request[0] - 1))
        q = ET.SubElement(request_el, 'quantity') 
        q.text = str(request[1])

    data_xml = ET.tostring(instance) 
    
    with open("xml/" + vrp_source.split("/")[1] + ".xml", "wb") as f: 
        f.write(data_xml) 


    vrp_file.close()

# CONVERTING BASELINE SOLUTION TO NODE FORM
def baseline_sol_to_text():
    vrp_file = open(vrp_source + '.sol', 'r') 
    vrp_lines = vrp_file.readlines() 

    path = "0"
    cost = 0
    num_cars = 0
    for line in vrp_lines:
        if "Route" in line:
            routes = line.split(":")[1]
            for node in routes.split():
                node = str(int(node))
                path += " " + node
            path += " 0"
            num_cars += 1
        if "Cost" in line:
            cost = int(line.split()[1])

    print("Baseline:", path)
    print("Cost:", cost, "Cars:", num_cars)
    vrp_file.close()

def convert_array_to_text():
    # sol = [0, 12, 1, 13, 7, 16, 0, 14, 22, 9, 8, 11, 4, 28, 18, 6, 26, 0, 20, 5, 25, 10, 15, 29, 27, 0, 21, 31, 19, 17, 2, 3, 23, 0, 24, 30, 0]
    sol = [0, 3, 1, 19, 24, 11, 15, 14, 0, 4, 29, 22, 23, 12, 8, 0, 5, 25, 18, 16, 21, 0, 6, 9, 17, 13, 30, 7, 0, 20, 27, 10, 2, 26, 28, 0]
    # sol = [0, 1, 22, 20, 35, 36, 3, 28, 31, 26, 8, 0, 4, 19, 13, 25, 14, 24, 23, 7, 0, 9, 10, 33, 39, 30, 34, 21, 29, 16, 32, 0, 11, 2, 38, 5, 37, 15, 17, 12, 0, 18, 6, 27, 0]
    # sol = [0, 4, 43, 11, 6, 48, 3, 19, 33, 0, 5, 36, 40, 16, 34, 38, 2, 10, 17, 0, 7, 26, 28, 14, 42, 13, 0, 8, 12, 37, 32, 31, 27, 41, 0, 9, 49, 30, 24, 22, 46, 25, 0, 15, 50, 23, 47, 45, 0, 18, 39, 29, 0, 21, 44, 20, 1, 35, 0]
    path = ""
    for n in sol:
        path += str(n) + " "
    print(path)

def distance(nodea, nodeb):
    return math.sqrt((nodea[1]-nodeb[1]) ** 2 + (nodea[2]-nodeb[2]) ** 2)

def greedy_nearest_neighbor():
    num_cars = 1
    nodelist = copy.deepcopy(nodes)
    startingnode = nodelist[0]

    greedypath = str(startingnode[0] - 1) + " "
    maxcapacity = 100
    curcapacity = 0
    totaldist = 0

    visited = [False] * len(nodes)     

    visited[0] = True
    
    curnode = startingnode
    while any([not v for v in visited]):
        found = False
        #calculate nearest neighbor
        nodelist = sorted(nodelist, key=lambda node: distance(curnode,node))
        for n in nodelist:
            if not found:
                nodeid = n[0]
                if not visited[nodeid-1]:
                    if curcapacity + requests[nodeid-1][1] > maxcapacity:
                        greedypath += str(startingnode[0] - 1) + " "
                        totaldist += distance(curnode, startingnode)
                        curnode = startingnode
                        curcapacity = 0
                        found = True
                        num_cars += 1
                    else:
                        visited[nodeid-1] = True
                        greedypath += str(nodeid - 1) + " "
                        totaldist += distance(curnode, n)
                        curcapacity += requests[nodeid-1][1]
                        curnode = n
                        found = True
    greedypath += str(startingnode[0] - 1)
    totaldist += distance(curnode, startingnode)
    print("Greedy:", greedypath)
    print("Cost:", totaldist, "Cars:", num_cars)


generate_instance_xml()
baseline_sol_to_text()
greedy_nearest_neighbor()
convert_array_to_text()