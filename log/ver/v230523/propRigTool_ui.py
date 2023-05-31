
#-*- coding: utf-8 -*-
import sys, imp, os
import pymel.all as pm
import maya.mel as mel
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial

import propRigTool_Core as core
imp.reload(core)


class PropUI(QtWidgets.QMainWindow):
    TITLE = 'PropRigTool'
    VERSION  = '230523'

    def __init__(self, parent=None):
        super(PropUI, self).__init__()

        self.setWindowTitle("{}_v{}".format(self.TITLE, self.VERSION))
        self.setGeometry(500,350,350,500)
        self.setMinimumWidth(350)
                
        # WIDGET
        self.mainCtrl_btn = QtWidgets.QPushButton("Create Base Rig", self, fixedHeight=40, styleSheet="background: rgb(110,110,140);")
        self.vtx_label = QtWidgets.QLabel('※ 각 축에 해당하는 vertex를 선택하세요.', self)
        self.vtxRig_btn = QtWidgets.QPushButton("Make Ctrl", self, fixedHeight=40, styleSheet="background: rgb(110,110,140);")
        
        # CONNECT
        self.mainCtrl_btn.clicked.connect(partial(core.createMainSystem))
        self.vtxRig_btn.clicked.connect(partial(core.createVtxRig))

        # LAYOUT
        prop1_layout = QtWidgets.QVBoxLayout()
        prop1_layout.addWidget(self.mainCtrl_btn)
        
        prop2_layout = QtWidgets.QVBoxLayout()
        prop2_layout.addWidget(self.vtx_label)
        prop2_layout.addLayout(self.getVtxLayout())
        prop2_layout.addWidget(self.vtxRig_btn)
        
        # GROUPBOX
        prop1_gb = QtWidgets.QGroupBox('')
        prop1_gb.setLayout(prop1_layout)
        
        prop2_gb = QtWidgets.QGroupBox('')
        prop2_gb.setLayout(prop2_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(prop1_gb)
        main_layout.addWidget(prop2_gb)
        main_layout.addStretch(1)

        # WINDOW
        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
    
    
    def getVtxLayout(self):
        
        main_lay = QtWidgets.QVBoxLayout()

        for xyz in ['X', 'Y', 'Z', '-Y']:
            
            sub_lay = QtWidgets.QHBoxLayout()

            self.vtx_line = QtWidgets.QLineEdit(Enabled=False, fixedHeight=30)
            self.vtx_btn = QtWidgets.QPushButton(xyz, fixedHeight=30, fixedWidth=100)
            
            self.vtx_btn.clicked.connect(self.vtxBtnClicked)
            
            sub_lay.addWidget(self.vtx_line)
            sub_lay.addWidget(self.vtx_btn)
            main_lay.addLayout(sub_lay)
            
        return main_lay
    
    
    def vtxBtnClicked(self):
        
        aa = self.vtx_line.objectName()
        bb = self.vtx_btn.objectName()
        print(aa, bb)


