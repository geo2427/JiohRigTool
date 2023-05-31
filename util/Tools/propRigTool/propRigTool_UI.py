#-*- coding: utf-8 -*-
import sys, imp, os
import pymel.all as pm
import maya.mel as mel
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial

import propRigTool_Core as core
imp.reload(core)

server_path = '/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool'
icon_path = server_path + '/util/resources/kk_icons/'


class PropUI(QtWidgets.QMainWindow):
    TITLE = 'PropRigTool'
    VERSION  = 'v001'
    
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def __init__(self, parent=None):
        super(PropUI, self).__init__()

        self.setWindowTitle("{}_v{}".format(self.TITLE, self.VERSION))
        self.setGeometry(500,350,350,500)
        self.setMinimumWidth(350)
        self.center()

        # WIDGET
        self.mainCtrl_btn = QtWidgets.QPushButton("Create Base Rig", self, fixedHeight=40, styleSheet="background: rgb(120,120,140);")
        self.vtx_label = QtWidgets.QLabel('※ 각 축에 해당하는 vertex를 선택하세요.', self)
        self.vtx_line1 = QtWidgets.QLineEdit('Primary', Enabled=False, fixedHeight=30)
        self.vtx_btn1 = QtWidgets.QPushButton('Z', fixedHeight=30, fixedWidth=100)
        self.vtx_line2 = QtWidgets.QLineEdit('Up', Enabled=False, fixedHeight=30)
        self.vtx_btn2 = QtWidgets.QPushButton('Y', fixedHeight=30, fixedWidth=100)
        self.vtx_line3 = QtWidgets.QLineEdit('Down', Enabled=False, fixedHeight=30)
        self.vtx_btn3 = QtWidgets.QPushButton('-Y', fixedHeight=30, fixedWidth=100)
        self.name_label = QtWidgets.QLabel('Name : ', self)
        self.name_line = QtWidgets.QLineEdit(self)
        self.vtxGuide_btn = QtWidgets.QPushButton("Guide", self, fixedHeight=40)
        self.vtxRig_btn = QtWidgets.QPushButton("Create Rig", self, fixedHeight=40, fixedWidth=200, styleSheet="background: rgb(110,110,140);")
        
        size1 = QtCore.QSize(35,35)
        self.ctrl01_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b01.XPM'),  iconSize=size1, objectName='0')
        self.ctrl02_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b02.XPM'),  iconSize=size1, objectName='1')
        self.ctrl03_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b03.XPM'),  iconSize=size1, objectName='2')
        self.ctrl04_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b04.XPM'),  iconSize=size1, objectName='3')
        self.ctrl05_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b05.XPM'),  iconSize=size1, objectName='4')
        self.ctrl06_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b06.XPM'),  iconSize=size1, objectName='5')
        self.ctrl07_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b07.XPM'),  iconSize=size1, objectName='6')
        self.ctrl08_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b08.XPM'),  iconSize=size1, objectName='7')
        self.ctrl09_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b09.XPM'),  iconSize=size1, objectName='8')
        self.ctrl10_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b10.XPM'),  iconSize=size1, objectName='9')
        self.ctrl11_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b11.XPM'),  iconSize=size1, objectName='10')
        self.ctrl12_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b12.XPM'),  iconSize=size1, objectName='11')
        self.ctrl13_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b13.XPM'),  iconSize=size1, objectName='12')
        self.ctrl14_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b14.XPM'),  iconSize=size1, objectName='13')
        self.ctrl15_icon = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path + '/b15.XPM'),  iconSize=size1, objectName='14')
        
        size2 = QtCore.QSize(39,35)
        self.color00_btn = QtWidgets.QPushButton(self, text='0', styleSheet="background: rgb(120,120,120); color: black", objectName='0', fixedSize=size2)
        self.color01_btn = QtWidgets.QPushButton(self, text='1', styleSheet="background: rgb(0,0,0); color: white;", objectName='1', fixedSize=size2)
        self.color02_btn = QtWidgets.QPushButton(self, text='2', styleSheet="background: rgb(191,191,191); color: black;", objectName='2', fixedSize=size2)
        self.color03_btn = QtWidgets.QPushButton(self, text='3', styleSheet="background: rgb(128,128,128); color: black;", objectName='3', fixedSize=size2)
        self.color04_btn = QtWidgets.QPushButton(self, text='4', styleSheet="background: rgb(204,0,51); color: black;", objectName='4', fixedSize=size2)
        self.color05_btn = QtWidgets.QPushButton(self, text='5', styleSheet="background: rgb(0,4,96); color: white;", objectName='5', fixedSize=size2)
        self.color06_btn = QtWidgets.QPushButton(self, text='6', styleSheet="background: rgb(0,0,255); color: black;", objectName='6', fixedSize=size2)
        self.color07_btn = QtWidgets.QPushButton(self, text='7', styleSheet="background: rgb(0,77,0); color: black;", objectName='7', fixedSize=size2)
        self.color08_btn = QtWidgets.QPushButton(self, text='8', styleSheet="background: rgb(38,0,67); color: white;", objectName='8', fixedSize=size2)
        self.color09_btn = QtWidgets.QPushButton(self, text='9', styleSheet="background: rgb(204,0,204); color: black;", objectName='9', fixedSize=size2)
        self.color10_btn = QtWidgets.QPushButton(self, text='10', styleSheet="background: rgb(153,77,51); color: black;", objectName='10', fixedSize=size2)
        self.color11_btn = QtWidgets.QPushButton(self, text='11', styleSheet="background: rgb(64,33,33); color: white;", objectName='11', fixedSize=size2)
        self.color12_btn = QtWidgets.QPushButton(self, text='12', styleSheet="background: rgb(179,51,0); color: black;", objectName='12', fixedSize=size2)
        self.color13_btn = QtWidgets.QPushButton(self, text='13', styleSheet="background: rgb(255,0,0); color: black;", objectName='13', fixedSize=size2)
        self.color14_btn = QtWidgets.QPushButton(self, text='14', styleSheet="background: rgb(0,255,0); color: black;", objectName='14', fixedSize=size2)
        self.color15_btn = QtWidgets.QPushButton(self, text='15', styleSheet="background: rgb(0,77,153); color: black;", objectName='15', fixedSize=size2)
        self.color16_btn = QtWidgets.QPushButton(self, text='16', styleSheet="background: rgb(255,255,255); color: black;", objectName='16', fixedSize=size2)
        self.color17_btn = QtWidgets.QPushButton(self, text='17', styleSheet="background: rgb(255,255,0); color: black;", objectName='17', fixedSize=size2)
        self.color18_btn = QtWidgets.QPushButton(self, text='18', styleSheet="background: rgb(0,255,255); color: black;", objectName='18', fixedSize=size2)
        self.color19_btn = QtWidgets.QPushButton(self, text='19', styleSheet="background: rgb(67,255,163); color: black;", objectName='19', fixedSize=size2)
        self.color20_btn = QtWidgets.QPushButton(self, text='20', styleSheet="background: rgb(255,179,179); color: black;", objectName='20', fixedSize=size2)
        self.color21_btn = QtWidgets.QPushButton(self, text='21', styleSheet="background: rgb(230,179,128); color: black;", objectName='21', fixedSize=size2)
        self.color22_btn = QtWidgets.QPushButton(self, text='22', styleSheet="background: rgb(255,255,102); color: black;", objectName='22', fixedSize=size2)
        self.color23_btn = QtWidgets.QPushButton(self, text='23', styleSheet="background: rgb(0,179,102); color: black;", objectName='23', fixedSize=size2)
        self.color24_btn = QtWidgets.QPushButton(self, text='24', styleSheet="background: rgb(153,102,51); color: black;", objectName='24', fixedSize=size2)
        self.color25_btn = QtWidgets.QPushButton(self, text='25', styleSheet="background: rgb(161,16,43); color: black;", objectName='25', fixedSize=size2)
        self.color26_btn = QtWidgets.QPushButton(self, text='26', styleSheet="background: rgb(102,153,51); color: black;", objectName='26', fixedSize=size2)
        self.color27_btn = QtWidgets.QPushButton(self, text='27', styleSheet="background: rgb(51,161,89); color: black;", objectName='27', fixedSize=size2)
        self.color28_btn = QtWidgets.QPushButton(self, text='28', styleSheet="background: rgb(46,161,161); color: black;", objectName='28', fixedSize=size2)
        self.color29_btn = QtWidgets.QPushButton(self, text='29', styleSheet="background: rgb(46,102,161); color: black;", objectName='29', fixedSize=size2)
        self.color30_btn = QtWidgets.QPushButton(self, text='30', styleSheet="background: rgb(110,46,161); color: black;", objectName='30', fixedSize=size2)
        self.color31_btn = QtWidgets.QPushButton(self, text='31', styleSheet="background: rgb(161,46,102); color: black;", objectName='31', fixedSize=size2)
        
        # CONNECT
        self.mainCtrl_btn.clicked.connect(partial(core.createMainSystem))
        self.vtx_btn1.clicked.connect(partial(core.AddItemLine, self.vtx_line1))
        self.vtx_btn2.clicked.connect(partial(core.AddItemLine, self.vtx_line2))
        self.vtx_btn3.clicked.connect(partial(core.AddItemLine, self.vtx_line3))
        self.vtx_line1.textChanged.connect(self.getModName)
        self.vtxGuide_btn.clicked.connect(partial(core.createVtxRigGuide, self.vtx_line1,self.vtx_line2,self.vtx_line3, self.name_line))
        self.vtxRig_btn.clicked.connect(partial(core.createVtxRig, self.name_line))
        
        self.ctrl01_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl01_icon))
        self.ctrl02_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl02_icon))
        self.ctrl03_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl03_icon))
        self.ctrl04_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl04_icon))
        self.ctrl05_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl05_icon))
        self.ctrl06_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl06_icon))
        self.ctrl07_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl07_icon))
        self.ctrl08_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl08_icon))
        self.ctrl09_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl09_icon))
        self.ctrl10_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl10_icon))
        self.ctrl11_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl11_icon))
        self.ctrl12_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl12_icon))
        self.ctrl13_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl13_icon))
        self.ctrl14_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl14_icon))
        self.ctrl15_icon.clicked.connect(partial(core.createCtrlShape, self.ctrl15_icon))
        
        self.color00_btn.clicked.connect(partial(core.setOverrideColor, self.color00_btn))
        self.color01_btn.clicked.connect(partial(core.setOverrideColor, self.color01_btn))
        self.color02_btn.clicked.connect(partial(core.setOverrideColor, self.color02_btn))
        self.color03_btn.clicked.connect(partial(core.setOverrideColor, self.color03_btn))
        self.color04_btn.clicked.connect(partial(core.setOverrideColor, self.color04_btn))
        self.color05_btn.clicked.connect(partial(core.setOverrideColor, self.color05_btn))
        self.color06_btn.clicked.connect(partial(core.setOverrideColor, self.color06_btn))
        self.color07_btn.clicked.connect(partial(core.setOverrideColor, self.color07_btn))
        self.color08_btn.clicked.connect(partial(core.setOverrideColor, self.color08_btn))
        self.color09_btn.clicked.connect(partial(core.setOverrideColor, self.color09_btn))
        self.color10_btn.clicked.connect(partial(core.setOverrideColor, self.color10_btn))
        self.color11_btn.clicked.connect(partial(core.setOverrideColor, self.color11_btn))
        self.color12_btn.clicked.connect(partial(core.setOverrideColor, self.color12_btn))
        self.color13_btn.clicked.connect(partial(core.setOverrideColor, self.color13_btn))
        self.color14_btn.clicked.connect(partial(core.setOverrideColor, self.color14_btn))
        self.color15_btn.clicked.connect(partial(core.setOverrideColor, self.color15_btn))
        self.color16_btn.clicked.connect(partial(core.setOverrideColor, self.color16_btn))
        self.color17_btn.clicked.connect(partial(core.setOverrideColor, self.color17_btn))
        self.color18_btn.clicked.connect(partial(core.setOverrideColor, self.color18_btn))
        self.color19_btn.clicked.connect(partial(core.setOverrideColor, self.color19_btn))
        self.color20_btn.clicked.connect(partial(core.setOverrideColor, self.color20_btn))
        self.color21_btn.clicked.connect(partial(core.setOverrideColor, self.color21_btn))
        self.color22_btn.clicked.connect(partial(core.setOverrideColor, self.color22_btn))
        self.color23_btn.clicked.connect(partial(core.setOverrideColor, self.color23_btn))
        self.color24_btn.clicked.connect(partial(core.setOverrideColor, self.color24_btn))
        self.color25_btn.clicked.connect(partial(core.setOverrideColor, self.color25_btn))
        self.color26_btn.clicked.connect(partial(core.setOverrideColor, self.color26_btn))
        self.color27_btn.clicked.connect(partial(core.setOverrideColor, self.color27_btn))
        self.color28_btn.clicked.connect(partial(core.setOverrideColor, self.color28_btn))
        self.color29_btn.clicked.connect(partial(core.setOverrideColor, self.color29_btn))
        self.color30_btn.clicked.connect(partial(core.setOverrideColor, self.color30_btn))
        self.color31_btn.clicked.connect(partial(core.setOverrideColor, self.color31_btn))

        # LAYOUT
        baseRig_layout = QtWidgets.QVBoxLayout()
        baseRig_layout.addWidget(self.mainCtrl_btn)
        
        vtx_lay1 = QtWidgets.QHBoxLayout()
        vtx_lay1.addWidget(self.vtx_line1)
        vtx_lay1.addWidget(self.vtx_btn1)
        vtx_lay2 = QtWidgets.QHBoxLayout()
        vtx_lay2.addWidget(self.vtx_line2)
        vtx_lay2.addWidget(self.vtx_btn2)
        vtx_lay3 = QtWidgets.QHBoxLayout()
        vtx_lay3.addWidget(self.vtx_line3)
        vtx_lay3.addWidget(self.vtx_btn3)
        
        name_lay = QtWidgets.QHBoxLayout()
        name_lay.addWidget(self.name_label)
        name_lay.addWidget(self.name_line)
        
        vtxRigBtn_lay = QtWidgets.QHBoxLayout()
        vtxRigBtn_lay.addWidget(self.vtxGuide_btn)
        vtxRigBtn_lay.addWidget(self.vtxRig_btn)
        
        vtxRig_layout = QtWidgets.QVBoxLayout()
        vtxRig_layout.addWidget(self.vtx_label)
        vtxRig_layout.addLayout(vtx_lay1)
        vtxRig_layout.addLayout(vtx_lay2)
        vtxRig_layout.addLayout(vtx_lay3)
        vtxRig_layout.addLayout(name_lay)
        vtxRig_layout.addLayout(vtxRigBtn_lay)
        
        kk_lay1 = QtWidgets.QHBoxLayout()
        kk_lay1.addWidget(self.ctrl01_icon)
        kk_lay1.addWidget(self.ctrl02_icon)
        kk_lay1.addWidget(self.ctrl03_icon)
        kk_lay1.addWidget(self.ctrl04_icon)
        kk_lay1.addWidget(self.ctrl05_icon)
        
        kk_lay2 = QtWidgets.QHBoxLayout()
        kk_lay2.addWidget(self.ctrl06_icon)
        kk_lay2.addWidget(self.ctrl07_icon)
        kk_lay2.addWidget(self.ctrl08_icon)
        kk_lay2.addWidget(self.ctrl09_icon)
        kk_lay2.addWidget(self.ctrl10_icon)
        
        kk_lay3 = QtWidgets.QHBoxLayout()
        kk_lay3.addWidget(self.ctrl11_icon)
        kk_lay3.addWidget(self.ctrl12_icon)
        kk_lay3.addWidget(self.ctrl13_icon)
        kk_lay3.addWidget(self.ctrl14_icon)
        kk_lay3.addWidget(self.ctrl15_icon)
        
        kk_layout = QtWidgets.QVBoxLayout()
        kk_layout.addLayout(kk_lay1)
        kk_layout.addLayout(kk_lay2)
        kk_layout.addLayout(kk_lay3)
        
        color_lay01 = QtWidgets.QHBoxLayout()
        color_lay01.addWidget(self.color00_btn)
        color_lay01.addWidget(self.color01_btn)
        color_lay01.addWidget(self.color02_btn)
        color_lay01.addWidget(self.color03_btn)
        color_lay01.addWidget(self.color04_btn)
        color_lay01.addWidget(self.color05_btn)
        color_lay01.addWidget(self.color06_btn)
        color_lay01.addWidget(self.color07_btn)
        
        color_lay02 = QtWidgets.QHBoxLayout()
        color_lay02.addWidget(self.color08_btn)
        color_lay02.addWidget(self.color09_btn)
        color_lay02.addWidget(self.color10_btn)
        color_lay02.addWidget(self.color11_btn)
        color_lay02.addWidget(self.color12_btn)
        color_lay02.addWidget(self.color13_btn)
        color_lay02.addWidget(self.color14_btn)
        color_lay02.addWidget(self.color15_btn)

        color_lay03 = QtWidgets.QHBoxLayout()
        color_lay03.addWidget(self.color16_btn)
        color_lay03.addWidget(self.color17_btn)
        color_lay03.addWidget(self.color18_btn)
        color_lay03.addWidget(self.color19_btn)
        color_lay03.addWidget(self.color20_btn)
        color_lay03.addWidget(self.color21_btn)
        color_lay03.addWidget(self.color22_btn)
        color_lay03.addWidget(self.color23_btn)
        
        color_lay04 = QtWidgets.QHBoxLayout()
        color_lay04.addWidget(self.color24_btn)
        color_lay04.addWidget(self.color25_btn)
        color_lay04.addWidget(self.color26_btn)
        color_lay04.addWidget(self.color27_btn)
        color_lay04.addWidget(self.color28_btn)
        color_lay04.addWidget(self.color29_btn)
        color_lay04.addWidget(self.color30_btn)
        color_lay04.addWidget(self.color31_btn)
        
        color_layout = QtWidgets.QVBoxLayout()
        color_layout.setSpacing(0)
        color_layout.addLayout(color_lay01)
        color_layout.addLayout(color_lay02)
        color_layout.addLayout(color_lay03)
        color_layout.addLayout(color_lay04)
        
        # GROUPBOX
        baseRig_gb = QtWidgets.QGroupBox('')
        baseRig_gb.setLayout(baseRig_layout)
        
        vtxRig_gb = QtWidgets.QGroupBox('')
        vtxRig_gb.setLayout(vtxRig_layout)
        
        kk_gb = QtWidgets.QGroupBox('')
        kk_gb.setLayout(kk_layout)
        
        color_gb = QtWidgets.QGroupBox('')
        color_gb.setLayout(color_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(baseRig_gb)
        main_layout.addWidget(vtxRig_gb)
        main_layout.addWidget(kk_gb)
        main_layout.addWidget(color_gb)
        main_layout.addStretch(1)

        # WINDOW
        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
    
    def getModName(self):
        
        pm.select(self.vtx_line1.text())
        text = str(pm.ls(hl=1)[0])
        self.name_line.setText(text)
        
        