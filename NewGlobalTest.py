import os


os.system("adb shell rm /sdcard/cur_state.xml")
# generate the xml file
os.system("adb shell uiautomator dump /sdcard/cur_state.xml")
# pull the file to PC
os.system("adb pull /sdcard/cur_state.xml")
