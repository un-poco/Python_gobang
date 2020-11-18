#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    双人对战GUI设计
'''
import sys
import time
sys.path.append('D:/Git/PY_gobang/GUI')
sys.path.append('D:/Git/PY_gobang/GUI/source')
sys.path.append('D:/Git/PY_gobang/AI')
from chessboard import ChessBoard
from ai import searcher
import MyButton
import numpy as np
# 客户端1代码
import socket
import threading

# 棋盘基本参数等
WIDTH = 760
HEIGHT = 650
MARGINXL = 100
MARGINXR = 164
MARGINX = 0.5 * (MARGINXL + MARGINXR)
MARGINY = 77
GRID = (WIDTH - 2 * MARGINX) / (15 - 1)
PIECE = 34
EMPTY = 0
BLACK = 1
WHITE = 2

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound
from PyQt5 import *





# ----------------------------------------------------------------------
# 重新定义Label类
# ----------------------------------------------------------------------

class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()


class GoBang(QWidget):
    backSignal = QtCore.pyqtSignal()  # 返回信号，用来和主界面连接
    def __init__(self):
        super().__init__()
        self.initUI()
        print(2)
        self.c = self.init_clent()


    def init_clent(self): # 客户端初始化
        # 创建 socket 对象
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 获取服务器ip地址 应该由界面输入 在这里直接用主机地址代替
        host = input('please input the server IP address : ')

        # 设置端口号
        port = 9999
        # 连接服务，指定主机和端口
        print(1)
        while True:
            time.sleep(0.5)
            try:
                res = c.connect((host, port))
                print(res)
                if not res:
                    print("connect server", res)
                    break
            except:
                print('等待联机')
        t1 = threading.Thread(target=self.client_recv)
        t1.start()
        return c

    def data_checkout(self, data):
        if data == 'r':
            self.gameover(WHITE)
        if data == 'c':
            # 执行重开函数
            self.piece_now = BLACK
            self.step = 0
            for piece in self.pieces:
                piece.clear()
            self.chessboard.reset()
            self.update()
            return False
        return True

    def client_recv(self):
        '''接收数据'''
        while True:
            try:
                data = self.c.recv(1024).decode()
                print(data)
                if self.data_checkout(data):
                    str_list = data.split(' ')
                    x, y = int(str_list[0]), int(str_list[1])
                    self.draw(x, y)
                    self.ai_down = True  # 解锁 允许鼠标点击下棋
            except:
                pass

    def initUI(self):  # UI初始化
        print(1)
        self.chessboard = ChessBoard()  # 棋盘类，详见chessboard.py

        palette1 = QPalette()  # 设置棋盘背景
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('source/游戏界面1.png')))
        self.setPalette(palette1)

        # self.setCursor(Qt.PointingHandCursor)  # 鼠标变成手指形状
        self.sound_piece = QSound("sound/move.wav")  # 加载落子音效
        self.sound_win = QSound("sound/win.wav")  # 加载胜利音效
        self.sound_defeated = QSound("sound/defeated.wav")  # 加载失败音效

        self.resize(WIDTH, HEIGHT)  # 画布大小，设为固定值，不允许缩放
        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))

        self.setWindowTitle("GoBang")  # 窗口名称
        self.setWindowIcon(QIcon('source/icon.ico'))  # 窗口图标

        # 所有按钮的图标和布局
        self.backBtn = MyButton.MyButton('source/返回按钮_hover.png',
                                         'source/返回按钮_normal.png',
                                         'source/返回按钮_press.png',
                                         parent=self)
        self.backBtn.move(610, 80)

        self.startBtn = MyButton.MyButton('source/开始按钮_hover.png',
                                          'source/开始按钮_normal.png',
                                          'source/开始按钮_press.png',
                                          parent=self)
        self.startBtn.move(610, 180)

        self.returnBtn = MyButton.MyButton('source/悔棋按钮_hover.png',
                                           'source/悔棋按钮_normal.png',
                                           'source/悔棋按钮_press.png',
                                           parent=self)
        self.returnBtn.move(610, 400)

        self.loseBtn = MyButton.MyButton('source/认输按钮_hover.png',
                                         'source/认输按钮_normal.png',
                                         'source/认输按钮_press.png',
                                         parent=self)
        self.loseBtn.move(610, 500)

        # 绑定按钮
        self.backBtn.clicked.connect(self.goBack)
        self.startBtn.clicked.connect(self.restart)
        self.loseBtn.clicked.connect(self.lose)
        self.returnBtn.clicked.connect(self.returnOneStep)

        # self.gameStatu = []

        self.black = QPixmap('source/black.png')  # 黑白棋子
        self.white = QPixmap('source/white.png')

        self.piece_now = BLACK



        self.step = 0 # 步数
        self.x, self.y = 1000, 1000



        self.pieces = [LaBel(self) for i in range(225)]  # 新建棋子标签，准备在棋盘上绘制棋子
        for piece in self.pieces:
            piece.setVisible(True)  # 图片可视
            piece.setScaledContents(True)  # 图片大小根据标签大小可变

        # self.mouse_point.raise_()  # 鼠标始终在最上层
        self.ai_down = False  # 主要是为了加锁，当值是False的时候在等待对方下棋，这时候己方鼠标点击失效，要忽略掉 mousePressEvent

        self.setMouseTracking(True)
        self.show()

    # 返回键设计，回到主菜单
    def goBack(self):
        self.backSignal.emit()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.backSignal.emit()

    def paintEvent(self, event):  # 画出指示箭头
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    # def mouseMoveEvent(self, e):  # 黑色棋子随鼠标移动
    #     # self.lb1.setText(str(e.x()) + ' ' + str(e.y()))
    #     self.mouse_point.move(e.x() - 16, e.y() - 16)

    def mousePressEvent(self, e):  # 玩家2下棋

        if e.button() == Qt.LeftButton and self.ai_down:
            x, y = e.x(), e.y()  # 鼠标坐标
            i, j = self.coordinate_transform_pixel2map(x, y)  # 对应棋盘坐标
            if not i is None and not j is None:  # 棋子落在棋盘上，排除边缘
                if self.chessboard.get_xy_on_logic_state(i, j) == EMPTY:  # 棋子落在空白处
                    t1 = (str(i), ' ', str(j))
                    t2 = ''.join(t1)
                    # 发送棋子坐标到服务器
                    self.c.send(t2.encode('utf-8'))
                    self.draw(i, j)
                    self.ai_down = False # 加锁 避免鼠标再点击


    def drawLines(self, qp):  # 绘制lines
        if self.step != 0:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(self.x - 5, self.y - 5, self.x + 3, self.y + 3)
            qp.drawLine(self.x + 3, self.y, self.x + 3, self.y + 3)
            qp.drawLine(self.x, self.y + 3, self.x + 3, self.y + 3)

    # 落子代码
    def draw(self, i, j):
        x, y = self.coordinate_transform_map2pixel(i, j)
        print('now now')
        print(self.piece_now)
        if self.piece_now == BLACK:
            self.pieces[self.step].setPixmap(self.black)  # 放置黑色棋子
            self.piece_now = WHITE
            self.chessboard.draw_xy(i, j, BLACK)
        else:
            self.pieces[self.step].setPixmap(self.white)  # 放置白色棋子
            self.piece_now = BLACK
            self.chessboard.draw_xy(i, j, WHITE)

        self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)  # 画出棋子

        self.sound_piece.play()  # 落子音效
        self.step += 1  # 步数+1

        winner = self.chessboard.anyone_win(i, j)  # 判断输赢
        if winner != EMPTY:
            # self.mouse_point.clear()
            self.gameover(winner)

    def coordinate_transform_map2pixel(self, i, j):
        # 从 chessMap 里的逻辑坐标到 UI 上的绘制坐标的转换
        return MARGINXL + j * GRID - PIECE / 2, MARGINY + i * GRID - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):
        # 从 UI 上的绘制坐标到 chessMap 里的逻辑坐标的转换
        i, j = int(round((y - MARGINY) / GRID)), int(round((x - MARGINXL) / GRID))
        # 有MAGIN, 排除边缘位置导致 i,j 越界
        if i < 0 or i >= 15 or j < 0 or j >= 15:
            return None, None
        else:
            return i, j

    # 这块代码后期还可以再改，用图片做出来应该会更好看
    def gameover(self, winner):
        if winner == BLACK:
            self.sound_win.play()
            reply = QMessageBox.question(self, 'You Lost!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            self.sound_defeated.play()
            reply = QMessageBox.question(self, 'You Win!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)


    # 认输功能键，不知道为什么卡的厉害。人机对战的认输还没写
    def lose(self):
        self.c.send('r'.encode())
        self.gameover(WHITE)
        self.backSignal.emit()

        self.close()


    # 重开，这个问题有点大，重新绘图我没实现。目前是把数组清空了，图没变(在上面重新画棋盘也太蠢了吧，刷新界面会比较好但是我没写出来:/)
    def restart(self):
        self.piece_now = BLACK
        self.step = 0
        for piece in self.pieces:
            piece.clear()
        self.chessboard.reset()
        self.update()
        self.c.send('c'.encode())

    # 这个理论上要做悔棋功能，看看写代码的同学是怎么实现的。
    def returnOneStep(self):
        return


class Mainwindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(760, 650)
        self.setWindowTitle("gobang")
        # 设置窗口图标
        self.setWindowIcon(QIcon("source/icon.ico"))

        # 设置背景图片
        p = QPalette(self.palette())  # 获得当前的调色板
        brush = QBrush(QImage("source/gobang_background.png"))
        p.setBrush(QPalette.Background, brush)  # 设置调色版
        self.setPalette(p)  # 给窗口设置调色板

        self.singlePlayerBtn = MyButton.MyButton('source/人机对战_hover.png',
                                                 'source/人机对战_normal.png',
                                                 'source/人机对战_press.png',
                                                 parent=self)
        self.singlePlayerBtn.move(250, 450)

        self.doublePlayerBtn = MyButton.MyButton('source/双人对战_hover.png',
                                                 'source/双人对战_normal.png',
                                                 'source/双人对战_press.png',
                                                 parent=self)
        self.doublePlayerBtn.move(250, 500)

        # 绑定开始双人游戏信号和槽函数
        self.doublePlayerBtn.clicked.connect(self.startDoubleGame)
        self.singlePlayerBtn.clicked.connect(self.startSingleGame)

    def startDoubleGame(self):
        # 构建双人对战界面
        self.doublePlayerGame = GoBang()
        # 绑定返回界面
        self.doublePlayerGame.backSignal.connect(self.showStartGame)

        self.doublePlayerGame.show()  # 显示游戏界面
        self.close()

    def startSingleGame(self):
        self.SingleGame = gobangGUI.GoBang()
        # self.SingleGame = SinglePlayerGame.SinglePlayerGame()
        self.SingleGame.backSignal.connect(self.showStartGame2)
        self.SingleGame.show()
        self.close()

    # 显示开始界面
    def showStartGame(self):
        self.show()
        self.doublePlayerGame.close()

    def showStartGame2(self):
        self.show()
        self.SingleGame.close()


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os
sys.path.append("D:/Pyfiles/PY_gobang/AI")
sys.path.append('D:/Git/PY_gobang/GUI/double_play')
import MyButton
import gobangGUI
import doublePlayerGUI

if __name__ == '__main__':
    '''
    app = QApplication(sys.argv)
    ex = GoBang()
    sys.exit(app.exec_())
    '''
    import cgitb

    cgitb.enable("text")
    a = QApplication(sys.argv)
    m = Mainwindow()
    m.show()
    sys.exit(a.exec_())