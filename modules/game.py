import socket
import random
import time
from config import *

class Game(object):
    def __init__(self, dest_ip):
        self._command = []

        if dest_ip == "":
            self.multi = False
        else:
            self.multi = True
            # self.dest_addr = (dest_ip, 5472)
            self.dest_addr = (dest_ip, 5471)
            self.net = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # self.net.bind(('', 5471))
            self.net.bind(('', 5472))
            print("绑定端口至5471,")
            print("正在等待回应………")

    # 这个方法用于获取用户输入
    def userInput(self,input):
        self._command.append(input)
        return self._command[-1]

    # 这个方法会处理所有命令并使用命令对应的方法
    def commandRespond(self, obj):
        cmd = self._command[-1]

        if cmd == "/help":
            Command().help()
        elif cmd == "/start" and config.status != "Start":
            Command().start(obj)
        elif cmd == "/restart" and config.status == "Start":
            Command().restart(obj)
        elif cmd == "/setting":
            Command().setting(obj)
        elif cmd == "/exit":
            self.net.close()
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
            if x < config.x and y < config.y and len(command) == 2:
                obj.place(x,y)
                obj.update()
                obj.announceNextMove()
                # 判断玩家是否已经获胜
                if obj.judge(x,y) == "Win":
                    config.status = "Winning"
                    self.sendChess(command)
            else:
                # print("无效坐标，请检查您的输入是否有误")
                raise ValueError
        # 出现错误时返回无效坐标错误
        except ValueError:
            print("无效坐标，请检查您的输入是否有误")
            return False
        return True

    def net_check(self):
        if self.multi:
            while True:
                try:
                    self.net.sendto(b"check", self.dest_addr)  # 尝试第一次握手
                    recv_msg, self.dest_addr = self.net.recvfrom(1024)  # 检查对方是否有发送信息给自己
                    # 如果收到的消息是check，说明这个电脑是后入的，需要给先入的电脑发送消息确认连接
                    if recv_msg == b"check":
                        print("匹配成功")
                        time.sleep(1)
                        self.net.sendto(b"connect", self.dest_addr)  # 连接成功后再发送一次消息进行第二次握手以确保另一位玩家也可以了解到这边的状况
                        return
                    # 如果收到的消息是connect，说明这个电脑是先入的，不需要再给对方主机发送消息确认连接
                    elif recv_msg == b"connect":
                        print("连接成功")
                        return
                    else:
                        print("连接失败，自动返回单人模式")
                        self.multi = False
                        return
                except ConnectionResetError:
                    pass

    def throwCoin(self, obj):
        if self.multi:
            while True:
                coin = str(random.randint(0,1))  # 抛一次硬币决定先后手
                self.net.sendto(coin.encode('utf-8'), self.dest_addr)  # 告诉另一位玩家你的结果
                oppoCoin, self.dest_addr = self.net.recvfrom(1024)
                # 如果双方的硬币都不一样，就根据彼此的硬币决定先后手开始游戏
                if coin != oppoCoin.decode('utf-8'):
                    if coin == '0':
                        print("您获得了后手")
                    else:
                        print("您获得了先手")
                    return int(coin)

    def listenForChess(self):
        print("对手正在思考中……")
        oppoChess , self.dest_addr = self.net.recvfrom(1024)
        oppoChess = oppoChess.decode('utf-8')
        return oppoChess

    def sendChess(self,info):
        print(info)
        self.net.sendto(info.encode('utf-8'), self.dest_addr)


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
        print("/exit".ljust(23,"-"), "退出".rjust(6,"—"))

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
