# fgo.air
推荐使用 雷电模拟器 （设置 宽 828 高 1792 as ipone11）

##### 前置需求

1.  adb 安卓调试工具
2. airtest 网易提供的自动化测试工具，使用编辑器版 或者 py 包版本均可

airtest 推荐安装py包版本，不需要渲染前端，减少更多的性能消耗, 同时增加一个bat文件可以点击开始。

fgo.py文件末尾，提供3种方法，可以自行注释使用

## 下面介绍如何使用我的脚本：
- ### 打开后界面
选择菜单 文件-打开脚本
![打开后界面](https://upload-images.jianshu.io/upload_images/13825041-70801a49fc769464.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- ### 进入游戏选择关卡
打开模拟器进入游戏，选择你要打的关卡并且选择助战阶级到caster阶，因为默认的助战是cba，找不到相应的助战程序会出错。

![caster阶的助战](https://upload-images.jianshu.io/upload_images/13825041-b4fbffb38499a351.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- ### 选择游戏画面
点击设备窗上的选择游戏画面然后选择相应的模拟器画面

![image.png](https://upload-images.jianshu.io/upload_images/13825041-0091855404f6f636.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- ### 修改脚本代码
将**脚本编辑窗**中的代码移到最后，找到这一行代码决定这整个脚本的行为：
1. #### start_FGO_process
```PYTHON
start_FGO_process(30, 2, "CBA")
```
这个函数有三个参数，参数意义分别是：打副本次数，体力不足时使用苹果种类（0123依次表示不用苹果或使用金银铜苹果），选择的助战英灵（不填表示默认选择第一个助战，` "CBA"`表示[斯卡哈・斯卡蒂](https://fgo.wiki/w/%E6%96%AF%E5%8D%A1%E5%93%88%C2%B7%E6%96%AF%E5%8D%A1%E8%92%82)，`"kongming"`表示[诸葛孔明〔埃尔梅罗Ⅱ世〕](https://fgo.wiki/w/%E8%AF%B8%E8%91%9B%E5%AD%94%E6%98%8E%E3%80%94%E5%9F%83%E5%B0%94%E6%A2%85%E7%BD%97%E2%85%A1%E4%B8%96%E3%80%95)，`"meilin"`表示[梅林](https://fgo.wiki/w/%E6%A2%85%E6%9E%97)）可以按照你的需求修改这几个参数。

2. #### 每回合的技能和宝具使用配置
找到`roundConfig1`，`roundConfig2`，`roundConfig3`，分别表示123回合使用的技能和宝具。
```
roundConfig1 = {"skills": [[2, 2], [2, 3], [1, 1], ], "masterSkills": [], "hoguNo": 1}
roundConfig2 = {"skills": [[1, 3], [2, 1, 1], [3, 1, 1], [1, 2, 1]], "masterSkills": [[3, 2, 4]], "hoguNo": 1}
roundConfig3 = {"skills": [[2, 1, 1], [2, 2], [2, 3, 1], [3, 2], [3, 3, 1]],"masterSkills": [], "hoguNo": 1}
```
以`roundConfig2`为例。
英灵使用的技能是：一号英灵使用3技能，2号英灵使用1技能对1号英灵生效，3号英灵使用1技能对1号英灵生效，1号英灵使用2技能对1号英灵生效。
使用御主礼装（换人礼装）：使用技能3对2号英灵和4号英灵进行换位。
使用宝具：1号英灵使用宝具。
可以按你的box修改这些技能和宝具配置，最终要做到：**保证宝具清掉1面2面，3面可以留一只残血怪后面靠平A解决**，若无法做到这些程序会出错。

我的配置如下，非满破宝石的宇宙凛加孔明和双CBA加换人礼装：

![参考配置](https://upload-images.jianshu.io/upload_images/13825041-ce47f801631d6c1f.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- ### 运行脚本
![万事皆备点击运行](https://upload-images.jianshu.io/upload_images/13825041-6ab58d7511de1c3b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
程序运行结束后还会同时在`C:\fgoLog`输出日志文件
![日志文件](https://upload-images.jianshu.io/upload_images/13825041-fe45149caada9270.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


