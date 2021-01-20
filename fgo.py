# -*- encoding=utf8 -*-
__author__ = "xuecm"

import os
import time

from airtest.core.api import *

auto_setup(__file__)
import random
import sys

logDir = 'C:/fgoLog/'
map = {
    'menu_button': Template(r"tpl1610378834413.png", record_pos=(0.427, 0.248), resolution=(1581, 889)),
    'reenter_battle': Template(r"tpl1610201774476.png", record_pos=(0.157, 0.16), resolution=(1581, 889)),
    'attack_button': Template(r"tpl1610201201151.png", record_pos=(0.384, 0.188), resolution=(1581, 889)),
    'battle_finish_sign': Template(r"tpl1610805274890.png", record_pos=(-0.353, -0.136), resolution=(1581, 889)),
    'feed_apple_decide': Template(r"tpl1610206565610.png", record_pos=(0.158, 0.155), resolution=(1581, 889)),
    'AP_recover': Template(r"tpl1610206410989.png", record_pos=(-0.007, -0.229), resolution=(1581, 889)),
    'start_battle': Template(r"tpl1610208679019.png", record_pos=(-0.007, -0.229), resolution=(1581, 889)),
    'quit_battle': Template(r"tpl1610805772693.png", record_pos=(0.371, 0.247), resolution=(1581, 889)),
    # 'rainbow_box': "",
    'refresh_decide': Template(r"tpl1610815463019.png", record_pos=(0.165, -0.181), resolution=(1581, 889)),
    'friend_sign': Template(r"tpl1610207591586.png", record_pos=(0.188, -0.107), resolution=(1581, 889)),
    'apple_type1': Template(r"tpl1610816462463.png", record_pos=(-0.208, -0.026), resolution=(1581, 889)),
    'apple_type2': Template(r"tpl1610816476626.png", record_pos=(-0.208, 0.087), resolution=(1581, 889)),
    'apple_type3': Template(r"tpl1610206543885.png", record_pos=(-0.206, -0.029), resolution=(1581, 889)),

    #     'CBA_name_pic': Template(r"tpl1610814182310.png", record_pos=(0.237, -0.017), resolution=(1581, 889)),
    #     'kongming_name_pic':Template(r"tpl1610814359537.png", record_pos=(0.237, 0.136), resolution=(1581, 889)),

    #     'meilin_name_pic':Template(r"tpl1610815294353.png", record_pos=(0.237, 0.128), resolution=(1581, 889)),
    'CBA_name_pic': Template(r"tpl1610816953292.png", record_pos=(-0.153, -0.043), resolution=(1581, 889)),
    'kongming_name_pic': Template(r"tpl1610816962826.png", record_pos=(-0.111, 0.103), resolution=(1581, 889)),
    'meilin_name_pic': Template(r"tpl1610816982721.png", record_pos=(-0.164, 0.089), resolution=(1581, 889)),

}

# round1 = {"skills": [[1, 1], [1, 3], [3, 1], [3, 3]], "masterSkills": [[2, 2]], "hoguNo": 3}
# round2 = {"skills": [], "masterSkills": [], "hoguNo": 1}
# round3 = {"skills": [], "masterSkills": [], "hoguNo": 2}

round1 = {"skills": [[2, 2], [2, 3], [1, 1], ], "masterSkills": [], "hoguNo": 1}
round2 = {"skills": [[1, 3], [2, 1, 1]], "masterSkills": [], "hoguNo": 1}
round3 = {"skills": [[2, 1, 1], [2, 2], [2, 3, 1], [3, 1, 1], [3, 2], [3, 3, 1], [1, 2, 1]],
          "masterSkills": [[3, 2, 4]], "hoguNo": 1}

skillTimeSleep = 8
atkTimeSleep = 5
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

    def existPic(self, picName="temp", pic=None):
        result = False
        if pic is None:
            if map is None:
                result = False
            if picName == '' or picName is None:
                result = False
            #         if not map.has_key(picName):
            #             result = False
            if map[picName] == '' or map[picName] is None:
                result = False
            result = exists(map[picName])
        else:
            result = exists(pic)
        if result == False:
            self.log("{} 不存在".format(picName), level=1)
            result = False, (-1, -1)
        else:
            self.log("已找到{}，坐标({},{})".format(picName, result[0], result[1]), level=1)
            result = True, result
        return result

    def coreTouch(self, x, y, msg="", sleepTime=1):
        core.log("点击坐标（{},{}),{}".format(x, y, msg), level=1)
        touch((x, y))
        self.coreSleep(sleepTime, msg)

    def coreSleep(self, time, msg=""):
        core.log("sleep time : {}s,{}".format(time, msg), level=1)
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
            log = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + msg + "\n"
            print (log)
            f = open(self.logFileName, 'a')
            f.write(log)
            f.close()


core = Core()
tempFileName = "fgo" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ".log"
core.createLogFile(logDir + tempFileName)


# 切面切换
class SceneCheck:
    def waifForStageChange(self, pic, info):
        loop = 0
        flag, position = core.existPic(pic)
        while bool(1 - flag):
            loop += 1
            if loop > maxLoop:
                break
            core.coreSleep(1, "等待{}".format(info))
            flag, position = core.existPic(pic)
        if not flag:
            quitWithMsg("等待{}过长，退出脚本".format(info))

    def waitForTeamScene(self):
        self.waifForStageChange('start_battle', "进入阵容界面")

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
        self.waifForStageChange('attack_button', "进入战斗界面")

    def waitForFriendShowReady(self):
        self.waifForStageChange('friend_sign', "进入助战界面")

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
    core.coreTouch(1400, 740, "点击attack", 3)
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


def useHeroSkill(heroNo, skillNo, target=0):
    y = 710
    if heroNo == 1:
        x = 90
    elif heroNo == 2:
        x = 480
    elif heroNo == 3:
        x = 870
    x += 110 * (skillNo - 1)
    core.coreTouch(x, y, "{}号英灵的{}技能".format(heroNo, skillNo), skillTimeSleep)
    if target != 0:
        core.coreTouch(400 + 300 * (target - 1), 560, "对{}号英灵使用".format(target), skillTimeSleep)


def useMasterSkill(skillNo, heroNo=0, changeHeroNo=0):
    # 410,425
    # 910,430
    # 170,426
    #     791,768
    core.coreTouch(1470, 380, "魔术礼装技能菜单", normalTimeSleep)
    core.coreTouch(1120 + 110 * (skillNo - 1), 380, "魔术礼装{}技能".format(skillNo), normalTimeSleep)
    if changeHeroNo == 0:
        if heroNo != 0:
            core.coreTouch(400 + 300 * (heroNo - 1), 560, "对{}号英灵使用".format(heroNo), normalTimeSleep)
    else:
        core.coreTouch(170 + 240 * (heroNo - 1), 430, "选择交换{}号英灵".format(heroNo), normalTimeSleep)
        core.coreTouch(170 + 240 * (changeHeroNo - 1), 430, "选择交换{}号英灵".format(changeHeroNo), normalTimeSleep)
        core.coreTouch(790, 770, "确认交换", normalTimeSleep)
        sceneCheck.waitForBattleStart()


def hogutankai(heroNo):
    # 1080 800 520
    core.coreTouch(520 + 280 * (heroNo - 1), 250, "宝具使用")


def atkByPosition(order):
    core.coreTouch(150 + 320 * (order - 1), 600, "指令卡{}".format(order), atkTimeSleep)


def doOneRoundByConfig(config):
    sceneCheck.waitForBattleStart()
    skills = config["skills"]
    masterSkills = config["masterSkills"]
    hoguNo = config["hoguNo"]

    for masterSkill in masterSkills:
        if len(masterSkill) == 1:
            useMasterSkill(masterSkill[0])
        elif len(masterSkill) == 2:
            useMasterSkill(masterSkill[0], masterSkill[1])
        else:
            useMasterSkill(masterSkill[0], masterSkill[1], masterSkill[2])
    for skill in skills:
        if len(skill) == 3:
            useHeroSkill(skill[0], skill[1], skill[2])
        else:
            useHeroSkill(skill[0], skill[1])

    card(hoguNo)


def doOneBattle():
    # Turn1
    doOneRoundByConfig(round1)
    # Turn2
    doOneRoundByConfig(round2)

    # Turn3
    doOneRoundByConfig(round3)


def reenter_battle():
    sceneCheck.waitBackToMenu()
    # 确认已经返回菜单界面，或检测到连续出击按键
    flag, position = core.existPic('reenter_battle')
    if flag:
        core.coreTouch(1040, 700, "连续出击")


def apple_feed(appleType=0):
    global appleUsedNum, globalAppleType
    globalAppleType = appleType
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
    core.coreSleep(8, "战斗结束")
    #     flag, position = core.existPic('rainbow_box')  # 检测是否掉礼装，若掉落则短信提醒
    #     if flag:
    #         lisoNum += 1
    #         core.log("礼装掉落+1，已掉落{}张".format(lisoNum))
    core.coreTouch(986, 565, "不请求加好友", 5)
    core.coreTouch(235, 525, "拒绝好友申请", 5)  # 拒绝好友申请

    core.coreTouch(1376, 834, "离开结算界面", 5)  # 离开结算界面
    global battleClearNum
    battleClearNum += 1
    logBattleEnd()


def budao():
    while True:
        while True:
            core.coreSleep(1, "等待战斗结束")
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


def find_friend(servant=""):
    sceneCheck.waitForFriendShowReady()

    flag = servant != ""
    # 310CBA直到找到为止
    # 1164,417
    # 1164,659
    loop = 0
    while flag:
        loop += 1
        if loop > maxLoop:
            break
        flag, position = core.existPic(servant + '_name_pic')
        if flag:
            core.coreSleep(1.5, "成功找到{}助战".format(servant))
            core.coreTouch(position[0], position[1], "选择助战" + servant)
            return True
        flag, position = core.existPic('refresh_decide')
        core.coreTouch(position[0], position[1], "刷新好友")
        core.coreTouch(1033, 693, "确认刷新好友")
        sceneCheck.waitForFriendShowReady()
    core.coreTouch(559, 343, "未找到助战英灵{},选择第一个助战".format(servant))
    return False


def battle_start():
    sceneCheck.waitForTeamScene()
    core.coreTouch(1400, 740, "开始战斗")


def quitWithMsg(errMsg):
    core.log(errMsg)
    core.coreTouch(0, 0, "退出脚本")
    logQuitMsg()
    sys.exit(0)


def logBattleEnd():
    global appleUsedNum, globalAppleType, lisoNum, battleClearNum
    core.log('已通关 {} 次'.format(battleClearNum), level=2)
    if globalAppleType != 0:
        core.log('已用了 {} {}苹果,礼装掉落 {} 个'.format(appleUsedNum, appleTypes[globalAppleType][0], lisoNum), level=2)


def logQuitMsg():
    global appleUsedNum, globalAppleType, lisoNum, battleClearNum

    core.log('共通关 {} 次'.format(battleClearNum), level=2)
    if globalAppleType != 0:
        core.log('共用了 {} {}苹果,礼装掉落 {} 个'.format(appleUsedNum, appleTypes[globalAppleType][0], lisoNum), level=2)


def start_FGO_process(times=1, appleType=0, servant=""):
    for i in range(0, times):
        find_friend(servant)
        #         battle_start()
        doOneBattle()
        quit_battle()
        reenter_battle()
        apple_feed(appleType)
    quitWithMsg("")


# core.existPic('reenter_battle')
# doOneBattle()
start_FGO_process(30, 2, "CBA")
# doOneRoundByConfig(round1)
# doOneRoundByConfig(round3)
# quit_battle()
# core.existPic(pic = Template(r"tpl1610812989049.png", record_pos=(0.002, 0.206), resolution=(1581, 889)))
# core.existPic(pic = Template(r"tpl1610814182310.png", record_pos=(0.237, -0.017), resolution=(1581, 889)))
# core.existPic(pic = Template(r"tpl1610814359537.png", record_pos=(0.237, 0.136), resolution=(1581, 889)))
# core.existPic(pic = Template(r"tpl1610815532809.png", record_pos=(0.154, 0.158), resolution=(1581, 889)))
# reenter_battle()

# find_friend("CBA")

#     # Turn3
# doOneRoundByConfig(round3)
