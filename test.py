# coding=utf-8
import random
import time
import os
import subprocess


class Widget():

    def __init__(self, text, id, widget_class, x1, y1, x2, y2, clickable, long_clickable, checkable, focusable, scrollable):
        self.text = text
        self.id = id        
        self.widget_class = widget_class
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.clickable = clickable
        self.long_clickable = long_clickable
        self.focusable = focusable
        self.checkable = checkable
        self.scrollable = scrollable

    def print_widget(self):
        print(self.widget_class, text, "[",x1, y1,"]", "[",x2, y2,"]")
    

def pickOneApp(fileName):

    file = open(fileName, 'r', encoding="utf-8").read()
    filelines = file.split("<")
    widgets = []
    for line in filelines:
        # pick up the widget
        if (line.find("node") == 0):
        
            text = line[line.find("text=")+6 : line.find("resource-id")-2]
            
            
            id = line[line.find("resource-id=")+13 : line.find("class=")-2]
            
            widget_class = line[line.find("class=")+7 : line.find("package=")-2]
            
            numbers = line[line.find("bounds=")+8 : line.rfind("\"")]
            
            x1 = int(numbers[1: numbers.find(",")])
            y1 = int(numbers[numbers.find(",")+1 : numbers.find("]")])
            x2 = int(numbers[numbers.rfind("[")+1 : numbers.rfind(",")])
            y2 = int(numbers[numbers.rfind(",")+1 : numbers.rfind("]")])
            
            clickableM = line[line.find("clickable=")+11 : line.find("enabled")-2]
            if clickableM == "false":
                clickable = False
            else:
                clickable = True

            long_clickableM = line[line.find("long-clickable=")+16 : line.find("password=")-2]
            if long_clickableM == "false":
                long_clickable = False
            else:
                long_clickable = True

            checkableM = line[line.find("checkable=")+11 : line.find("checked=")-2]
            if checkableM == "false":
                checkable = False
            else:
                checkable = True

            focusableM = line[line.find("focusable=")+11 : line.find("focused=")-2]
            if focusableM == "false":
                focusable = False
            else:
                focusable = True

            scrollableM = line[line.find("scrollable=")+12 : line.find("long-clickable")-2]
            if scrollableM == "false":
                scrollable = False
            else:
                scrollable = True

            if (clickable or long_clickable or checkable or focusable or scrollable):

                widgets.append(Widget(text, id,  widget_class, x1, y1, x2, y2, 
                clickable, long_clickable, checkable,focusable, scrollable))

                # print(widget_class ,clickable, checkable,focusable, scrollable, x1, x2, y1, y2, numbers)

    return widgets

if __name__ == '__main__':

    
    for i in range(5):
        # delete the old xml file
        os.system("adb shell rm /sdcard/test.xml")

        # generate the xml file
        os.system("adb shell uiautomator dump /sdcard/test.xml")
        
        # pull the file to PC
        os.system("adb pull /sdcard/test.xml")
        
        path = "./"
        # path = "C:/android/sdk/tools/bin/"

        xml_file = "test.xml"

        widgets = []

        # get the widgets' information from the xml file
        widgets = pickOneApp( path + xml_file )
        print(len(widgets))



        # randomly touch a widget
        index = random.randint(0, len(widgets)-1)


        # if clickable 
        if (widgets[index].clickable == True):
            x = (widgets[index].x1 + widgets[index].x2)/2
            y = (widgets[index].y1 + widgets[index].y2)/2
            os.system("adb shell input tap "+str(x)+" "+str(y))
            print(str(x)+", "+str(y)+" has been clicked")

        # if scrollable
        if (widgets[index].scrollable == True):
            actionIndex = random.randint(1, 4)
            startX = (widgets[index].x1 + widgets[index].x2)/2
            startY = (widgets[index].y1 + widgets[index].y2)/2
            endX = 0
            endY = 0
            scrollTime = 500

            # left scroll 
            if (actionIndex == 1):
                endX = widgets[index].x1
                endY = startY 
                print("left scroll")

            # right scroll
            elif (actionIndex == 1):
                endX = widgets[index].x2
                endY = startY 
                print("right scroll")


            # up scroll
            elif (actionIndex == 1):
                endX = startX
                endY = widgets[index].y1
                print("up scroll")


            # down scroll
            elif (actionIndex == 1):
                endX = startX
                endY = widgets[index].y2
                print("down scroll")

            os.system("adb shell input swipe "+str(startX)+" "+str(startY)+" "+str(endX)+" "+str(endY)+" "+str(scrollTime))


