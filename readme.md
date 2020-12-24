# 五子棋v1.0
在学习python的时候突发奇想想要做个五子棋来玩玩，于是就随手写下了这个小游戏。

原理很简单：
创建一个二维列表用于存放棋盘信息，然后用设置中定义的棋盘样式显示这个棋盘
玩家输入坐标便可以控制落子，每次落子后切换一下棋子图案
在每次玩家输入后，进行四次检测：横向、竖向、右上、右下方向检测是否有五颗样式相同的棋子连在了一起，如果有的话，宣布游戏结束
在写了一些功能后，我发现有必要新增一个以/开头的命令系统，于是重写了一下框架。
如果玩家输入以/开头的字符时，程序会把这段字符按照命令处理，进行一些特殊的处理，如开始游戏、进入设置、重新开始游戏

有很多功能我都懒得做了，现在想先学点别的东西（比如自动寻路）
目前可以使用的命令有
/start ----- 开始
/restart --- 重新开始
/help ------ 帮助
int,int ---- 下棋
