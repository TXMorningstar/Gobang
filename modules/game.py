from config import *
from modules.board import *

class Game(object):
    def __init__(self):
        self._command = []

    # 这个方法用于获取用户输入
    def userInput(self,input):
        self._command.append(input)
        return self._command[-1]

    # 这个方法会处理所有命令并使用命令对应的方法
    def commandRespond(self, obj):
        if self._command[-1] == "/help":
            Command().help()
        elif self._command[-1] == "/start" and config.status != "Start":
            Command().start(obj)
        elif self._command[-1] == "/restart" and config.status == "Start":
            Command().restart(obj)
        elif self._command[-1] == "/setting":
            Command().setting(obj)
        else:
            Command().badinput()

    # 这个方法用于放置棋子
    def place(self, obj, command):
        # 检查输入是否复合格式，如果格式合法则放置棋子
        try:
            # 分割玩家输入的命令并组成列表方便读取
            command = command.split(",")

            # 将command转换为int
            for i in range(len(command)):
                int(command[i],10)

            # 赋值变量方便查阅
            x = int(command[0],10)
            y = int(command[-1],10)

            # 再次检查输入是否合法：是否超出棋盘边界、命令长度是否规范
            if x <= config.x and y <= config.y and len(command) == 2:
                obj.place(x,y)
                obj.update()
                obj.announceNextMove()
                if obj.judge(x,y) == "Win":
                    config.status = "Winning"
            else:
                # print("无效坐标，请检查您的输入是否有误")
                raise ValueError
        # 出现错误时返回无效坐标错误
        except ValueError:
            print("无效坐标，请检查您的输入是否有误")


class Command(object):
    def badinput(self):
        print("无效输入，请检查您的输入是否有误\n您可以输入/help查看所有指令")

    def help(self):
        print("==============帮助界面==============")
        print("/help".ljust(23,"-"), "显示帮助".rjust(6,"—"))
        print("/start".ljust(23,"-"), "开始游戏".rjust(6,"—"))
        print("/setting".ljust(23,"-"), "游戏设置".rjust(6,"—"))
        print("/close".ljust(23,"-"), "结束游戏".rjust(6,"—"))
        print("/restart".ljust(23,"-"), "重新开始游戏".rjust(6,"—"))
        print("/last".ljust(23,"-"), "上一条指令".rjust(6,"—"))
        print("/undo".ljust(23,"-"), "撤销".rjust(6,"—"))
        print("/giveup".ljust(23,"-"), "投降".rjust(6,"—"))

    def start(self, obj):
        config.status = "Start"
        obj.generate()
        obj.update()
        obj.announceNextMove()

    def restart(self,obj):
        config.status = "Start"
        obj.generate()
        obj.update()
        obj.announceNextMove()

    def setting(self,obj):
        print("等我心情来了就写")
