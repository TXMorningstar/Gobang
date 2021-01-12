from config import *
from modules.board import *
from modules.game import *

def main():
    # 实例化对象
    board = Board()
    game = Game(input("如需进行多人游戏，请输入对手ip，否则直接回车\n>>"))

    # 进行多人游戏的初始化
    game.net_check()
    global TURN
    TURN = game.throwCoin(board)
    if game.multi:
        Command().start(board)


    # 游戏开始前的提示信息
    print("---------输入/help获取帮助----------")

    print()
    # 程序开始运行，通过循环不断使用户输入信息并反应
    while True:
        # 多人模式 #############################################################
        #######################################################################
        if game.multi:

            # 我的回合 #########################################################
            if TURN == 1:
                print("===我的回合===")
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
                    if game.place(board,command):  # 如果玩家输入的坐标有效
                        # 向对手发送落子信息，随后切换回合
                        game.sendChess(command)
                        TURN = 0
                # 只是以防万一，不认识的全部错误输入
                else:
                    Command().badinput()

            # 对手回合 #########################################################
            else:
                print("===对手回合===")
                oppoChess = game.listenForChess()
                print(oppoChess)
                print(type(oppoChess))
                game.place(board, oppoChess)
                TURN = 1


        # 单人模式 #############################################################
        #######################################################################
        else:
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





if __name__ == "__main__":
    main()
