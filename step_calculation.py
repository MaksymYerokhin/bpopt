import csv
import xml.etree.ElementTree as ET
import os

def step_calc(pools={}):
    local_act = 1000000
    total_cost = 0
    utils = {}
    namespaces1 = {'qbp': 'http://www.qbp-simulator.com/Schema201212'}
    tree = ET.parse('./CopiedModel.bpmn')
    root = tree.getroot()
    data = root.find("qbp:processSimulationInfo", namespaces1).find(
        "qbp:resources", namespaces1).getchildren()

    if(pools != {}):
        # reassign resources
        for child in data:
            child.attrib["totalAmount"] = str(pools[child.attrib["name"]])
        tree.write("./CopiedModel.bpmn")

    for child in data:
        pools[child.attrib["name"]] = int(child.attrib["totalAmount"])
        total_cost += int(child.attrib["costPerHour"]) * \
            int(child.attrib["totalAmount"])

    # Check cycle time with bimp
    if os.system("java -jar ./Simod/external_tools/bimp/qbp-simulator-engine-original.jar ./CopiedModel.bpmn -csv ./Simod/external_tools/bimp/output.csv"):
        raise RuntimeError('program {} failed!')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = dir_path + "/Simod/external_tools/bimp/output.csv"
    output_data = csv.reader(open(output_path))

    start_resources = False
    for _, row in enumerate(output_data):
        if(len(row) > 1):
            if(start_resources == True):
                utils[row[0]] = float(int(row[1]))/100
            if(row[1] == "Utilization %"):
                start_resources = True
        else:
            start_resources = False

        if(len(row) > 2):
            if(row[0] == "Process Cycle Time (s)"):
                local_act = float(row[2])

    print("utils = ", utils)
    return (local_act, pools, total_cost, utils)