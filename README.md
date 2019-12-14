# monkey_lab
for nothing

### 项目细节

- adb启动APP

  `adb shell dumpsys package > ./package.txt `

  `adb  shell am start -n xxxxxx/xxxx`

- adb关闭APP

  `adb shell am force-stop xxxxxx`

- 数据结构

  - state： 装有当前所有event的set
    - {a, b, c, d, ... [widgets数组]}
    - a.eventType = 'clickable’
    - a.widget = id(widgets数组id)
    - a.counter = 0
    - a.MaxQvalue = 0
    - 注意：上下左右滑动四个type的实现

    

  

  