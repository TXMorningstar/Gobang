from config import *
from modules.game import *

# 棋盘的各种方法
class Board(object):
    # 初始化棋盘的各种数据
    def __init__(self):
        self._step = 0

    # 根据设置来定义一个棋盘，生成一个二维列表表示棋盘
    def generate(self):
        self._board = [[config.slot_patterns for i in range(config.x)] for i in range(config.y)]

    # 返回棋盘的二维列表
    def getBoard(self):
        return self._board

    # 返回下一个将会落下的棋子，实现交替落子
    # 每次调用时都会更新自身
    def nextChess(self):
        # 如果回合数可以被2整除，则返回黑棋图案，否则返回白棋图案
        if self._step % 2 == 0:
            self._step += 1
            return config.chess_black
        else:
            self._step += 1
            return config.chess_white

    # 返回当前回合的棋子
    def getNowChess(self):
        if self._step % 2 == 0:
            return "○"
        else:
            return "●"
    # 返回当前回合的棋子
    def getNextChess(self):
        if self._step % 2 == 0:
            return "●"
        else:
            return "○"

    # 向玩家发送落子提示
    def announceNextMove(self):
        nowChess = self.getNowChess()
        print("现在该%s落棋" % nowChess)
        print("向哪里落棋，格式为“横,竖”，例如1,1\n")

    # 放置棋子
    def place(self,x,y):
        if self._board[y][x] == config.slot_patterns: #如果被选中的区域没有棋子
            self._board[y][x] = self.nextChess() #落子
        else:
            print("这个地方已经有棋子了") #禁止落子
            raise ValueError

    # 以适合玩家阅读的方式打印目前的棋盘
    def update(self):
        print("----"*config.x) #分割线
        # 打印x轴坐标
        print("    ",end="") #对齐y
        for i in range(config.x):
            print(str(i).ljust(2), end = "  ")
            if i == config.x - 1:
                print("\n")

        # 打印棋盘的二维数组
        for x in range(config.x):
            print(str(x).ljust(4), end = "")  # 打印y轴坐标
            for y in range(config.y):
                print(self._board[x][y],end="  ")
            print("\n")
        print("----"*config.x) #分割线

    # 检查玩家是否已经获胜
    def judge(self,x,y):
        count = 0
        # 横向判定,列表中的数字代表检测方向
        for i in range(-4,5):
            if x+i < config.x and x+i >= 0:
                if self._board[y][x+i] == self.getNextChess():
                    # print(self._board[y][x+i])##################################调试用
                    count += 1
                else:
                    # print(self._board[y][x+i])##################################调试用
                    count = 0
            # 是否有人胜利
            if count == 5:
                print("---------------------------------------\n"*32)
                return "Win"

        # 纵向判定
        for i in range(-4,5):
            if y+i < config.y and y+i >= 0:
                if self._board[y+i][x] == self.getNextChess():
                    # print(self._board[y+i][x])##################################调试用
                    count += 1
                else:
                    # print(self._board[y+i][x])##################################调试用
                    count = 0
            # 是否有人胜利
            if count == 5:
                print("---------------------------------------\n"*32)
                return "Win"

        # 斜向判定
        for direc in [-1,1]:
            for i in range(-4,5):
                if y+i*direc < config.y and y+i*direc >= 0 and x+i < config.x and x+i >= 0:
                    # print(direc,end="---")######################################调试用
                    # print(self._board[y+i*direc][x+i])##########################调试用
                    if self._board[y+i*direc][x+i] == self.getNextChess():
                        count += 1
                    else:
                        count = 0
                    # 是否有人获胜
                    if count == 5:
                        print("---------------------------------------\n"*32)
                        return "Win"
