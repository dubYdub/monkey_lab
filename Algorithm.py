# coding=utf-8
import random
import time
import string
import os
import subprocess
import xml.etree.ElementTree as ET


# 全局唯一标识
unique_id = 1

class Event:
    def __init__(self,event_type, widget_index, bounds):
        self.event_type = event_type
        self.widget_index = widget_index
        # self.widget = widget
        self.bounds = bounds
        self.Q_value = 500


class State:
    def __init__(self):
        self.widgets = []
        self.events = []

    def create_events(self):
        # generate events through attributes of widgets
        widgets = self.widgets
        for widget_index in range(len(widgets)):
            if widgets[widget_index][3]['clickable'] == 'true' or widgets[widget_index][3]['focusable'] == 'true' \
                    or widgets[widget_index][3]['checkable'] == 'true' or widgets[widget_index][3]['enabled'] == 'true':
                single_event = Event("click", widget_index, widgets[widget_index][3]['bounds'])
                self.events.append(single_event)
            if widgets[widget_index][3]['focused'] == 'true':
                single_event = Event("write", widget_index, widgets[widget_index][3]['bounds'])
                self.events.append(single_event)
            if widgets[widget_index][3]['long-clickable'] == 'true':
                single_event = Event("long_click", widget_index, widgets[widget_index][3]['bounds'])
                self.events.append(single_event)
            if widgets[widget_index][3]['scrollable'] == 'true':
                single_event = Event("vertical_scroll",widget_index, widgets[widget_index][3]['bounds'])
                self.events.append(single_event)
                single_event = Event("horizontal_scroll",widget_index, widgets[widget_index][3]['bounds'])
                self.events.append(single_event)


# [48,1427][266,1492]
def handle_bounds(bounds):
    tmp = bounds.partition('][')
    list1 = tmp[0]
    list2 = tmp[2]
    list1 = list1.split(",")
    list2 = list2.split(",")
    # print(list1)
    x1 = int(list1[0][1:])
    y1 = int(list1[1])
    x2 = int(list2[0])
    y2 = int(list2[1][:-1])
    return x1, y1, x2, y2


def event_execute(event):
    x1, y1, x2, y2 = handle_bounds(event.bounds)
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    if event.event_type == "click":
        os.system("adb shell input tap " + str(x) + " " + str(y))
    elif event.event_type == "write" :
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        os.system("adb shell input text" + " " + random_str)
    elif event.event_type == "long_click" :
        os.system("adb shell input swipe" + " " + str(x) + " " + str(y) + " " + str(x + 1) + " " + str(y + 1)
                  + " " + "1000")
    elif event.event_type == "vertical_scroll" :
        os.system("adb shell input swipe" + " " + str(x) + " " + str(y) + " " + str(x) + " " + str(event.widget.y2) +
                  " " + "500")
    elif event.event_type == "horizontal_scroll" :
        os.system("adb shell input swipe" + " " + str(x) + " " + str(y) + " " + str(event.widget.x2) + " " + str(y) +
                  " " + "500")


def create_xml():
    os.system("adb shell rm /sdcard/cur_state.xml")
    # generate the xml file
    os.system("adb shell uiautomator dump /sdcard/cur_state.xml")
    # pull the file to PC
    os.system("adb pull /sdcard/cur_state.xml")


def walkData(root_node, level,required_list):
    global unique_id
    unique_id += 1
    # 遍历每个子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        temp_list = [unique_id, level, root_node.tag, root_node.attrib]
        required_list.append(temp_list)
        return
    for child in children_node:
        walkData(child, level + 1,required_list)
    return


def get_xml_data(file_name):
    level = 1  # depth of 1
    required_list = []
    root = ET.parse(file_name).getroot()
    walkData(root, level,required_list)
    return required_list


def judge_diff(state1,state2):
    if len(state1.widgets) == len(state2.widgets):
        for index in range(len(state1.widgets)):
            if state1.widgets[index][0] != state2.widgets[index][0] or state1.widgets[index][1] != state2.widgets[index][1]:
                return False
        return True
    else :
        return False


if __name__ == '__main__':
    # current state
    states = []
    # while True:
    for i in range(2):
        print(1)
        cur_state = State()
        create_xml()
        cur_widgets = get_xml_data("cur_state.xml")
        cur_state.widgets = cur_widgets

        # judge if cur_state is in states
        flag = False
        cur_index = -1
        for state_index in range(0,len(states)):
            if judge_diff(states[state_index], cur_state):
                flag = True
                cur_index = state_index
                break
        if flag:
            # index_ifexist is used
            i = 0
            # event
            # states[cur_index].events
        else:
            # print("enter")
            states.append(cur_state)
            cur_index = len(states) - 1
            states[cur_index].create_events()

        # execute event
        # random choose
        for item in states[cur_index].widgets:
            print(item)
        random_index = random.randint(0, len(states[cur_index].events) - 1)
        selected_event = states[cur_index].events[random_index]

        event_execute(selected_event)

# if __name__ == '__main__':
#     global unique_id
#     state_collection = []
#     xml_file = "cur_state.xml"
#     while true:
#         cur_state = State()
#         create_xml()
#         unique_id = 1
#         cur_widgets = getXmlData(path + xml_file)
#         cur_state.widgets = cur_widgets
        
#         # judge if this state is in state_collection
#         if (cur_state in state_collection):
#             # do nothing
#         else: 
#             cur_state.create_events()
#             state_collection.append(cur_state)

#         # choose the best Q-value event
#         max_Qvalue = 0
#         max_index = -1
#         for event_index in len(cur_state.events):
#             if cur_state.events[event_index] > max_Qvalue:
#                 max_Qvalue = cur_state.events[event_index]
#                 max_index = event_index
#         selected_event = cur_state.events[max_index]

#         execute_event(selected_event)

#         # enter new state
#         new_state = State()
#         create_xml()
#         new_widgets = analyze_xml(path + xml_file)
#         new_state.widgets = new_widgets
#         #
        
#         # judge if this state is in state_collection
#         if (cur_state in state_collection):
#             # do nothing
#         else: 
#             cur_state.create_events()
#             state_collection.append(cur_state)