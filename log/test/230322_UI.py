import sys, imp, os
import pymel.all as pm
import maya.cmds as cmds
import maya.mel as mel
from PySide2 import QtCore, QtWidgets


class GSRigUI(QtWidgets.QMainWindow):
    TITLE = 'GS RigTool'
    VERSION  = '230322'

    def __init__(self):
        super(GSRigUI, self).__init__()

        self.setWindowTitle("{} v{}".format(self.TITLE, self.VERSION))
        self.setGeometry(350,500,400,400)

        # WIDGET
        self.fitSetup_btn = QtWidgets.QPushButton("Fit Setup", self)
        self.asymmetry_cb = QtWidgets.QCheckBox("Asymmetry", self)
        self.preRig_btn = QtWidgets.QPushButton("Pre Rig", self)
        self.pubCheck_btn = QtWidgets.QPushButton("Pub Check", self)

        # CONNECT
        self.fitSetup_btn.clicked.connect(self.fitSetup)
        self.asymmetry_cb.clicked.connect(self.asymmetryRig)
        self.preRig_btn.clicked.connect(self.preRig)
        self.preRig_btn.clicked.connect(self.correctPV)
        self.pubCheck_btn.clicked.connect(self.pubCheck)

        # LAYOUT
        fit_layout = QtWidgets.QVBoxLayout()
        fit_layout.addWidget(self.fitSetup_btn)
        fit_layout.addWidget(self.asymmetry_cb)

        pre_layout = QtWidgets.QVBoxLayout()
        pre_layout.addWidget(self.preRig_btn)

        check_layout = QtWidgets.QVBoxLayout()
        check_layout.addWidget(self.pubCheck_btn)
        
        fit_gb = QtWidgets.QGroupBox('Fit Setup')
        fit_gb.setFixedSize(300,150)
        fit_gb.setLayout(fit_layout)

        pre_gb = QtWidgets.QGroupBox('Pre Rig')
        pre_gb.setFixedSize(300,150)
        pre_gb.setLayout(pre_layout)

        check_gb = QtWidgets.QGroupBox('Pub Check')
        check_gb.setFixedSize(300,150)
        check_gb.setLayout(check_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addStretch(1)
        main_layout.addWidget(fit_gb)
        main_layout.addWidget(pre_gb)
        main_layout.addWidget(check_gb)
        main_layout.addStretch(1)

        # WINDOW
        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


    def fitSetup(self):
        print('FIT SETUP')

    def asymmetryRig(self):
        print('Asymmetry')

    def preRig(self):
        print('PRE RIG')

    def correctPV(self):
        print('CORRECT POLE VECTOR')
    
    def pubCheck(self):
        print('PUB CHECK')


GS_window = GSRigUI()
GS_window.show()
