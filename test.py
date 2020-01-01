# coding=utf-8
import random
import string
import os
import xml.etree.ElementTree as ET
import math

unique_id = 1

def walkData(root_node, level, required_list, focused_flag):
    global unique_id
    unique_id += 1
    # transverse every single node
    children_node = list(root_node)
    if root_node.tag == "node":
        if root_node.attrib["resource-id"] == "map":
            print("Do not enter map")
        elif root_node.attrib["clickable"] == "true" \
                or root_node.attrib['scrollable'] == "true" \
                or root_node.attrib['long-clickable'] == "true" \
                or (root_node.attrib['focusable'] == "true" and root_node.attrib['focused'] == "false") \
                or root_node.attrib['checkable'] == "true":
            temp_list = [unique_id, level, root_node.tag, root_node.attrib]
            required_list.append(temp_list)
        elif root_node.attrib['focused'] == "true" and root_node.attrib['focusable'] == "true":
            focused_flag = True
        if focused_flag and len(children_node) == 0:
            # print("hello")
            temp_list = [unique_id, level, root_node.tag, root_node.attrib]
            required_list.append(temp_list)
    if len(children_node) != 0:
        for child in children_node:
            walkData(child, level + 1, required_list, focused_flag)
    return


def get_xml_data(file_name):
    level = 1  # depth of 1
    required_list = []
    root = ET.parse(file_name).getroot()
    walkData(root, level, required_list, False)
    return required_list


rl = get_xml_data("cur_state.xml")
for i in rl:
    print(i)
