# monkey_lab
基于Q-learning的安卓自动化测试工具

### 项目细节

- adb启动APP

  `adb shell dumpsys package > ./package.txt `

  `adb  shell am start -n xxxxxx/xxxx`

  实例：

  - `adb  shell am start -n cz.martykan.forecastie/.activities.SplashActivity `

- adb关闭APP

  `adb shell am force-stop xxxxxx`

  实例：

  - `adb shell am force-stop cz.martykan.forecastie`

- 数据结构

  - state： 装有当前所有event的set
    - {a, b, c, d, ... [widgets数组]}
    - a.eventType = 'clickable’
    - a.widget = id(widgets数组id)
    - a.counter = 0
    - a.MaxQvalue = 0
    - 注意：上下左右滑动四个type的实现

### 测试方法

1. adb shell am instrument cz.martykan.forecastie/cz.martykan.forecastie.test.JacocoInstrumentation
2. adb pull data/data/cz.martykan.forecastie/files/coverage.ec
3. 移动coverage.ec到/build/outputs/code-coverage/connected(如果目录不存在则手动创建)
4. 生成代码覆盖率报告：app/Tasks/reporting/ gradle jacocoTestReport





