from config import *
from modules.board import *
from modules.game import *

# 实例化对象
board = Board()
game = Game()

# 游戏开始前的提示信息
print("---------------五子棋---------------")
print("---------输入/help获取帮助----------")
print()


# 程序开始运行，通过循环不断使用户输入信息并反应
while True:
    # 让玩家进行输入
    command = game.userInput(input(">>"))

    # 根据玩家输入内容做出反应
    # 在这之前先防止玩家输入了空文本
    if command == "":
        Command().badinput()

    # 如果玩家输入以“/”开头的字符串则以指令判断
    elif command[0] == "/":
        game.commandRespond(board)

    # 如果玩家输入了不以“/”开头的字符串则默认是落子动作
    elif config.status == "Start" and command[0] != "/":
        game.place(board,command)

    # 只是以防万一，不认识的全部错误输入
    else:
        Command().badinput()

    # 在完成输入后换行以便于阅读
    print()
