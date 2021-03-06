# coding=utf-8
import random
import string
import os
import xml.etree.ElementTree as ET
import math

# global
unique_id = 1
states = []


class Event:
    def __init__(self, event_type, widget_index, bounds):
        self.event_type = event_type
        self.widget_index = widget_index
        # self.widget = widget
        self.bounds = bounds
        self.Q_value = 20
        self.visited_counter = 1


class State:
    def __init__(self):
        self.widgets = []
        self.events = []

    def create_events(self):
        # generate events through attributes of widgets
        widgets = self.widgets
        for widget_index in range(len(widgets)):
            if widgets[widget_index][3]['clickable'] == 'true' or widgets[widget_index][3]['focusable'] == 'true' \
                    or widgets[widget_index][3]['checkable'] == 'true' or widgets[widget_index][3]['focused']:
                if widgets[widget_index][3]['class'] == "android.widget.EditText":
                    single_event = Event("write", widget_index, widgets[widget_index][3]['bounds'])
                    self.events.append(single_event)
                else:
                    single_event = Event("click", widget_index, widgets[widget_index][3]['bounds'])
                    self.events.append(single_event)
            if widgets[widget_index][3]['long-clickable'] == 'true':
                single_event = Event("long_click", widget_index, widgets[widget_index][3]['bounds'])
                self.events.append(single_event)
            if widgets[widget_index][3]['scrollable'] == 'true':
                single_event = Event("vertical_scroll", widget_index, widgets[widget_index][3]['bounds'])
                self.events.append(single_event)
                single_event = Event("horizontal_scroll", widget_index, widgets[widget_index][3]['bounds'])
                self.events.append(single_event)


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
        print("adb shell input tap " + str(x) + " " + str(y))
        os.system("adb shell input tap " + str(x) + " " + str(y))
    elif event.event_type == "write":
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        print("adb shell input text" + " " + random_str)
        os.system("adb shell input text" + " " + random_str)
    elif event.event_type == "long_click":
        print("adb shell input swipe" + " " + str(x) + " " + str(y) + " " + str(x + 1) + " " + str(y + 1)
                  + " " + "1000")
        os.system("adb shell input swipe" + " " + str(x) + " " + str(y) + " " + str(x + 1) + " " + str(y + 1)
                  + " " + "1000")
    elif event.event_type == "vertical_scroll":
        print("adb shell input swipe" + " " + str(x) + " " + str(y) + " " + str(x) + " " + str(y1) +
                  " " + "500")
        os.system("adb shell input swipe" + " " + str(x) + " " + str(y) + " " + str(x) + " " + str(y1) +
                  " " + "500")
    elif event.event_type == "horizontal_scroll":
        print("adb shell input swipe" + " " + str(x) + " " + str(y) + " " + str(x1) + " " + str(y) +
                  " " + "500")
        os.system("adb shell input swipe" + " " + str(x) + " " + str(y) + " " + str(x1) + " " + str(y) +
                  " " + "500")



def create_xml(file_name):
    os.system("adb shell rm /sdcard/" + file_name)
    # generate the xml file
    os.system("adb shell uiautomator dump /sdcard/" + file_name)
    # pull the file to PC
    os.system("adb pull /sdcard/" + file_name)


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


def judge_if_same(state1, state2):
    if len(state1.widgets) == len(state2.widgets):
        for index in range(len(state1.widgets)):
            if state1.widgets[index][0] != state2.widgets[index][0] or state1.widgets[index][1] != \
                    state2.widgets[index][1]:
                return False
        return True
    else:
        return False


def create_state(file_name):
    global states
    single_state = State()
    create_xml(file_name)
    single_state.widgets = get_xml_data(file_name)
    # for i in single_state.widgets:
    #     print(i)
    # judge if cur_state is in states
    if_same_flag = False
    single_index = -1
    for state_index in range(0, len(states)):
        if judge_if_same(states[state_index], single_state):
            if_same_flag = True
            single_index = state_index
            break
    # print(if_same_flag)
    if not if_same_flag:
        print("new state")
        states.append(single_state)
        single_index = len(states) - 1
        states[single_index].create_events()
        # print(states[single_index].widgets)
    else:
        print("old state" + str(single_index))
    return single_index


def select_best_event(state_index):
    global states
    random.shuffle(states[state_index].events)
    # random
    cur_state = states[state_index]
    max_Q_value = 0
    selected_event_index = 0
    # print("len(cur_state.events)=" + str(len(cur_state.events)))
    for event_index in range(len(cur_state.events)):
        if cur_state.events[event_index].Q_value > max_Q_value:
            max_Q_value = cur_state.events[event_index].Q_value
            selected_event_index = event_index
    return selected_event_index


def cal_discount(event_num):
    # 0.9 × e−0.1×(|E |−1)
    return 0.9 * math.e ** (- 0.1 * (event_num - 1))


def app_restart():
    os.system("adb shell am force-stop cz.martykan.forecastie")
    os.system("adb shell am start -n cz.martykan.forecastie/.activities.SplashActivity")


if __name__ == '__main__':
    # global states
    # current state
    # for i in range(2):
    rate = 0.02
    rate_increase = 0
    while True:
        rdm = random.random()
        if rdm <= rate:
            # 退出重进
            app_restart()
        print(" ")
        for state_index in range(len(states)):
            print("state" + str(state_index + 1) + "               ", end="")
            for event in states[state_index].events:
                print(str(event.Q_value) + " ", end="")
            print(" ")
        unique_id = 1
        cur_state_index = create_state("cur_state.xml")
        # states[cur_index] represents the cur_state
        print("")
        selected_event_index = select_best_event(cur_state_index)
        # print(selected_event_index)
        selected_event = states[cur_state_index].events[selected_event_index]
        event_execute(selected_event)
        print(selected_event.event_type +
              " visited_counter= " + str(selected_event.visited_counter) +
              " Q_value= " + str(selected_event.Q_value)
              )
        states[cur_state_index].events[selected_event_index].visited_counter += 1

        unique_id = 1
        next_state_index = create_state("next_state.xml")
        discount_factors = cal_discount(len(states[next_state_index].events))
        # enter new state
        # Q(s, e∗) = R(e∗, s, s′) +γ · maxe∈Es′ Q(s′, e)
        # R(e, s, s′) = 1/xe
        new_event_index = select_best_event(next_state_index)  # event that have max Q-value
        max_Q_value = states[next_state_index].events[new_event_index].Q_value
        if max_Q_value == 0:
            states[cur_state_index].events[selected_event_index].Q_value = 0
            app_restart()
            print("State invalid")
            continue
        # reward + γ ×maxValue;
        if judge_if_same(states[cur_state_index], states[next_state_index]):
            print("Event not work")
            # states[cur_state_index].events[selected_event_index].Q_value = 0
            states[cur_state_index].events[new_event_index].Q_value = 0
            rate_increase += 0.02
        else:
            print("Event works")
            selected_Q_value = 1 / states[next_state_index].events[new_event_index].visited_counter \
                               + discount_factors * max_Q_value
            print("selected_Q_value= " + str(selected_Q_value))
            states[cur_state_index].events[selected_event_index].Q_value = selected_Q_value
            rate_increase = 0