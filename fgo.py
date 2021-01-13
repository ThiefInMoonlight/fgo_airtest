# -*- encoding=utf8 -*-
__author__ = "xuecm"

import os
import time

from airtest.core.api import *

auto_setup(__file__)
import random
import sys
logDir ='E:/fgoLog/'
map = {
    'menu_button': Template(r"tpl1610378834413.png", record_pos=(0.427, 0.248), resolution=(1581, 889)),
    'reenter_battle': Template(r"tpl1610201774476.png", record_pos=(0.157, 0.16), resolution=(1581, 889)),
    'attack_button': Template(r"tpl1610201201151.png", record_pos=(0.384, 0.188), resolution=(1581, 889)),
    'battle_finish_sign': Template(r"tpl1610205928892.png", record_pos=(-0.002, -0.03), resolution=(1581, 889)),
    'feed_apple_decide': Template(r"tpl1610206565610.png", record_pos=(0.158, 0.155), resolution=(1581, 889)),
    'AP_recover': Template(r"tpl1610206410989.png", record_pos=(-0.007, -0.229), resolution=(1581, 889)),
    # 'rainbow_box': "",
    # 'refresh_decide': "",
    'friend_sign': Template(r"tpl1610207591586.png", record_pos=(0.188, -0.107), resolution=(1581, 889)),
    'apple_type1': Template(r"tpl1610206543885.png", record_pos=(-0.206, -0.029), resolution=(1581, 889)),
    'apple_type2': Template(r"tpl1610206543885.png", record_pos=(-0.206, -0.029), resolution=(1581, 889)),
    'apple_type3': Template(r"tpl1610206543885.png", record_pos=(-0.206, -0.029), resolution=(1581, 889)),
}

skillTimeSleep = 8
atkTimeSleep = 5
pageChangeTimeSleep = 100
normalTimeSleep = 5

maxLoop = 1000
appleUsedNum = 0
battleClearNum = 0
lisoNum = 0
globalAppleType = 0
appleTypes = {
    1: ["金", "apple_type1"],
    2: ["银", "apple_type2"],
    3: ["铜", "apple_type3"]
}


class Core:
    logFileName = ""
    def __init__(self):
        pass

    def existPic(self, picName):
        result = False
        if map is None:
            result = False
        if picName == '' or picName is None:
            result = False
#         if not map.has_key(picName):
#             result = False
        if map[picName] == '' or map[picName] is None:
            result = False
        result = exists(map[picName])
        if result == False:
            self.log("{} 不存在".format(picName))
            result = False, (-1, -1)
        else:
            self.log("已找到{}，坐标({},{})".format(picName, result[0], result[1]))
            result = True, result
        return result

    def coreTouch(self, x, y, msg="", sleepTime=1):
        core.log("点击坐标（{},{})".format(x, y))
        touch((x, y))
        self.coreSleep(sleepTime, msg)

    def coreSleep(self, time, msg=""):
        core.log("sleep time : {}s,{}".format(time, msg))
        sleep(time)

    def createLogFile(self, filename):

        """
        创建日志文件夹和日志文件
        :param filename:
        :return:
        """
        self.logFileName = filename
        path = filename[0:filename.rfind("/")]
        if not os.path.isdir(path):  # 无文件夹时创建
            os.makedirs(path)
        if not os.path.isfile(filename):  # 无文件时创建
            fd = open(filename, mode="w")
            fd.close()
        else:
            pass


    def log(self, msg, level=1):
        print(self.logFileName)
        # level 1 debug级别 2 info级别
        if level >= 1:
            log = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" "+msg+"\n"
            print (log)
            f = open(self.logFileName,'a')
            f.write(log)
            f.close()




core = Core()
tempFileName = "fgo"+time.strftime("%Y-%m-%d", time.localtime())+".log"
core.createLogFile(logDir+tempFileName)

# 切面切换
class SceneCheck:
    def waitBackToMenu(self):
        loop = 0
        # 是否在主界面
        flag, position = core.existPic('menu_button')
        while bool(1 - flag):
            loop += 1
            if loop > maxLoop:
                break
            core.coreSleep(1, "等待进入主界面")
            flag, position = core.existPic('menu_button')
            if flag:
                break
            flag, position = core.existPic('reenter_battle')
            if flag:
                break
        if not flag:
            quitWithMsg("等待进入主界面过长，退出脚本")

    def waitForBattleStart(self):
        loop = 0
        flag, position = core.existPic('attack_button')
        while bool(1 - flag):
            loop += 1
            if loop > maxLoop:
                break
            core.coreSleep(1, "等待进入战斗界面")
            flag, position = core.existPic('attack_button')
        if not flag:
            quitWithMsg("等待进入战斗界面过长，退出脚本")

    def waitForFriendShowReady(self):
        loop = 0
        flag, position = core.existPic('friend_sign')
        while bool(1 - flag):
            loop += 1
            if loop > maxLoop:
                break
            core.coreSleep(1, "等待进入助战界面")
            flag, position = core.existPic('friend_sign')
            if flag:
                break
        if not flag:
            quitWithMsg("等待进入助战界面过长，退出脚本")

    def waitForBattleEnd(self):
        loop = 0
        while True:
            loop += 1
            if loop > maxLoop:
                break
            core.coreSleep(1, "等待进入战斗结算界面")
            flag, position = core.existPic('battle_finish_sign')
            if flag:
                return True
            flag, position = core.existPic('attack_button')
            if flag:
                # 翻车了 没打完
                return False
        return False


sceneCheck = SceneCheck()


def card(hoguNum=0):
    sceneCheck.waitForBattleStart()
    core.coreTouch(960, 510, "点击attack", 3)
    atkNum = 3
    if hoguNum != 0:
        hogutankai(hoguNum)
        atkNum = 2
    randomIndex = random.sample(range(1, 5), atkNum)  # 随机指令牌

    for i in randomIndex:
        atkByPosition(i)
    if hoguNum != 0:
        core.log('使用{} 宝具')
    else:
        core.log('随机平A')


def useHeroSkill(heroNum, skillNum, target=0):
    y = 710
    if heroNum == 1:
        x = 90
    elif heroNum == 2:
        x = 480
    elif heroNum == 3:
        x = 870
    x += 110 * (skillNum - 1)
    # todo 完善target逻辑
    core.coreTouch(x, y, "对{}号英灵使用{}号英灵的{}技能".format(target, heroNum, skillNum), skillTimeSleep)


def useMasterSkill(skillNum, heroNum=0):
    core.coreTouch(1470, 380, "魔术礼装技能菜单", normalTimeSleep)
    core.coreTouch(1120 + 110 * (skillNum - 1), 380, "魔术礼装{}技能".format(skillNum), normalTimeSleep)
    if heroNum != 0:
        core.coreTouch(400 + 300 * (heroNum - 1), 560, "对{}号英灵使用".format(heroNum), normalTimeSleep)


def hogutankai(heroNum):
    # 1080 800 520
    core.coreTouch(520 + 280 * (heroNum - 1), 250, "宝具使用")


def atkByPosition(order):
    core.coreTouch(150 + 320 * (order - 1), "指令卡{}".format(order), 2)


def doOneBattle():
    # 判断是否进入战斗界面
    sceneCheck.waitForBattleStart()
    # Turn1
    useHeroSkill(1, 1, 0)
    useHeroSkill(1, 3, 0)
    useHeroSkill(3, 1, 0)
    useHeroSkill(3, 3, 0)
    useMasterSkill(2, 2)

    card(3)

    sceneCheck.waitForBattleStart()

    # Turn2

    card(1)

    sceneCheck.waitForBattleStart()
    # Turn3

    card(2)


def reenter_battle():
    sceneCheck.waitBackToMenu()
    # 确认已经返回菜单界面，或检测到连续出击按键
    flag, position = core.existPic('reenter_battle')
    if flag:
        core.coreTouch(705, 475, "再次挑战")


def apple_feed(appleType=0):
    global appleUsedNum, globalAppleType
    core.coreSleep(5, "战斗结束等待检查体力是否充足")
    flag, position = core.existPic('AP_recover')
    if flag:
        if appleType == 0:
            quitWithMsg('体力用完且不允许使用苹果，退出')
        flag, position = core.existPic(appleTypes[globalAppleType][1])
        if flag:
            str = "使用" + appleTypes[globalAppleType][0] + "苹果"
            core.coreTouch(709, position[1], str, 1.5)
            flag, position = core.existPic('feed_apple_decide')
            core.coreTouch(position[0], position[1], str + "确认")
            appleUsedNum += 1
            core.log('体力不足，使用{}苹果'.format(appleTypes[globalAppleType][0]))
        else:
            quitWithMsg('苹果数量不足')


def quit_battle():
    global lisoNum
    battleEnd = sceneCheck.waitForBattleEnd()
    if not battleEnd:
        core.log('翻车，进入补刀程序')
        budao()
    core.log(' Battle finished')
    core.coreSleep(1)
    flag, position = core.existPic('rainbow_box')  # 检测是否掉礼装，若掉落则短信提醒
    if flag:
        lisoNum += 1
        core.log("礼装掉落+1，已掉落{}张".format(lisoNum))
    core.coreTouch(986, 565, "不请求加好友")
    core.coreTouch(235, 525, "拒绝好友申请")  # 拒绝好友申请


def budao():
    while True:
        while True:
            core.coreSleep(1)
            flag, position = core.existPic('battle_finish_sign')
            if flag:
                break
            flag, position = core.existPic('attack_button')
            if flag:
                break
        flag, position = core.existPic('attack_button')
        if flag:
            card()
        else:
            break


def find_friend(servant):
    sceneCheck.waitForFriendShowReady()

    # todo:找310CBA直到找到为止
    loop = 0
    while False:
        loop += 1
        if loop > maxLoop:
            break
        flag, position = core.existPic(servant + '_skill_level')
        if flag:
            core.log(' Success find', servant)
            core.coreSleep(1.5)
            core.coreTouch(position[0], position[1] - 60, "选择助战" + servant, 1.5)
            core.coreTouch(1005, 570, "开始战斗", 1.5)
            return True
        flag, position = core.existPic('refresh_decide')
        core.coreTouch(position[0], position[1], "刷新好友")
        core.coreTouch(710, 110, "确认刷新好友")
    core.coreTouch(559, 343, "未找到" + servant + ",选择第一个助战")
    core.coreTouch(1005, 570, "开始战斗", 1.5)
    return False


def quitWithMsg(errMsg):
    core.log(errMsg)
    core.coreTouch(0, 0, "退出脚本")
    logQuitMsg()
    sys.exit(0)


def logQuitMsg():
    global appleUsedNum, globalAppleType, lisoNum, battleClearNum

    core.log('通关 {} 次'.format(battleClearNum), level=2)
    core.log('用了 {} {}苹果,礼装掉落 {} 个'.format(appleUsedNum, appleTypes[globalAppleType][0], lisoNum), level=2)


def start_FGO_process(times=1, appleType=0, servant="CBA"):
    global globalAppleType
    globalAppleType = appleType
    for i in range(0, times):
        find_friend(servant)
        doOneBattle()
        quit_battle()
        reenter_battle()
        apple_feed(appleType)
    quitWithMsg("")


start_FGO_process(3)








