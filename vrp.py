import xml.etree.ElementTree as ET 
import math,copy
import time

# CREATING THE INSTANCE FILE
# vrp_source = 'A/A-n32-k5'
# vrp_source = 'B/B-n31-k5'
# vrp_source = 'P/P-n40-k5'
# vrp_source = 'B/B-n51-k7'
vrp_source = 'VRP-Set-X/X/X-n401-k29'

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
    # sol = [0, 3, 1, 19, 24, 11, 15, 14, 0, 4, 29, 22, 23, 12, 8, 0, 5, 25, 18, 16, 21, 0, 6, 9, 17, 13, 30, 7, 0, 20, 27, 10, 2, 26, 28, 0]
    # sol = [0, 1, 22, 20, 35, 36, 3, 28, 31, 26, 8, 0, 4, 19, 13, 25, 14, 24, 23, 7, 0, 9, 10, 33, 39, 30, 34, 21, 29, 16, 32, 0, 11, 2, 38, 5, 37, 15, 17, 12, 0, 18, 6, 27, 0]
    # sol = [0, 4, 43, 11, 6, 48, 3, 19, 33, 0, 5, 36, 40, 16, 34, 38, 2, 10, 17, 0, 7, 26, 28, 14, 42, 13, 0, 8, 12, 37, 32, 31, 27, 41, 0, 9, 49, 30, 24, 22, 46, 25, 0, 15, 50, 23, 47, 45, 0, 18, 39, 29, 0, 21, 44, 20, 1, 35, 0]
    sol = [0, 7, 240, 51, 96, 363, 35, 162, 189, 106, 205, 0, 20, 66, 272, 336, 6, 350, 5, 87, 394, 67, 361, 0, 30, 383, 319, 104, 207, 93, 362, 343, 226, 372, 208, 204, 333, 179, 250, 160, 248, 4, 187, 313, 69, 276, 294, 390, 257, 86, 223, 61, 80, 340, 255, 0, 39, 315, 270, 233, 166, 74, 211, 202, 147, 83, 169, 22, 60, 0, 45, 37, 26, 82, 124, 303, 246, 388, 168, 98, 90, 157, 0, 50, 144, 121, 392, 253, 247, 266, 196, 378, 342, 122, 396, 141, 310, 298, 181, 273, 130, 338, 254, 277, 377, 239, 0, 72, 337, 330, 2, 24, 10, 352, 134, 364, 170, 0, 78, 14, 94, 81, 59, 344, 312, 118, 275, 114, 375, 0, 92, 348, 368, 132, 302, 293, 218, 100, 345, 0, 113, 77, 219, 261, 281, 231, 291, 123, 192, 0, 117, 279, 329, 241, 288, 25, 212, 393, 29, 395, 8, 152, 120, 0, 127, 174, 389, 251, 164, 23, 32, 367, 263, 381, 0, 135, 159, 58, 155, 161, 48, 171, 53, 154, 0, 139, 376, 371, 210, 335, 27, 31, 18, 306, 21, 73, 225, 236, 0, 140, 64, 101, 110, 163, 243, 308, 384, 108, 280, 49, 183, 284, 323, 97, 199, 379, 320, 62, 138, 274, 137, 116, 165, 65, 175, 398, 229, 0, 143, 209, 68, 13, 292, 149, 232, 88, 177, 0, 146, 33, 156, 301, 327, 43, 103, 190, 1, 188, 56, 349, 358, 295, 237, 360, 145, 322, 297, 102, 267, 215, 304, 316, 217, 334, 178, 0, 176, 332, 365, 42, 249, 12, 326, 193, 290, 129, 230, 0, 194, 214, 41, 221, 34, 128, 357, 203, 262, 324, 0, 195, 256, 228, 126, 40, 285, 9, 354, 95, 299, 0, 198, 373, 252, 111, 115, 380, 70, 220, 89, 15, 222, 0, 216, 260, 133, 347, 213, 356, 79, 150, 3, 307, 369, 397, 136, 76, 234, 172, 235, 0, 238, 374, 142, 245, 242, 119, 52, 201, 224, 283, 278, 0, 244, 185, 38, 44, 182, 287, 328, 125, 173, 325, 0, 259, 11, 85, 151, 57, 339, 84, 105, 112, 399, 54, 269, 0, 264, 167, 351, 191, 282, 107, 318, 331, 382, 184, 265, 0, 289, 366, 63, 109, 296, 16, 353, 28, 200, 317, 387, 314, 258, 19, 206, 47, 286, 300, 355, 370, 153, 385, 158, 131, 36, 180, 55, 148, 75, 305, 0, 341, 321, 227, 71, 309, 311, 197, 91, 359, 0, 346, 46, 17, 391, 99, 386, 271, 186, 268, 400, 0]
    path = ""
    for n in sol:
        path += str(n) + " "
    print(path)

def distance(nodea, nodeb):
    return math.sqrt((nodea[1]-nodeb[1]) ** 2 + (nodea[2]-nodeb[2]) ** 2)

def greedy_nearest_neighbor():
    t0 = time.time()
    num_cars = 1
    nodelist = copy.deepcopy(nodes)
    startingnode = nodelist[0]

    greedypath = str(startingnode[0] - 1) + " "
    # maxcapacity = 100
    maxcapacity = 745
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
    t1 = time.time()
    print("Time:", t1-t0)
    print("Greedy:", greedypath)
    print("Cost:", totaldist, "Cars:", num_cars)


generate_instance_xml()
baseline_sol_to_text()
greedy_nearest_neighbor()
convert_array_to_text()