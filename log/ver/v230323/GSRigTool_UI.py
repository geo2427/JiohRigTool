# coding:utf-8
import sys, imp, os
import pymel.all as pm
import maya.cmds as cmds
import maya.mel as mel
from PySide2 import QtCore, QtWidgets
from functools import partial

import GSRigTool_Core as core
imp.reload(core)


class GSRigUI(QtWidgets.QMainWindow):
    TITLE = 'GS RigTool'
    VERSION  = '230323'

    def __init__(self):
        super(GSRigUI, self).__init__()

        self.setWindowTitle("{} v{}".format(self.TITLE, self.VERSION))
        self.setGeometry(150,350,300,400)
        self.setMinimumWidth(300)

        # WIDGET
        self.biped_btn = QtWidgets.QPushButton("Import `biped.ma`", self)
        self.fitSetup_btn = QtWidgets.QPushButton("Fit Setup", self)
        self.asymmetry_btn = QtWidgets.QPushButton("Asymmetry", self)
        self.del_asymmetry_btn = QtWidgets.QPushButton("Delete Asymmetry", self)
        self.fitBuild_btn = QtWidgets.QPushButton("Build AdvancedSkeleton", self)

        self.priAxis_cb = QtWidgets.QComboBox(self)
        self.priAxis_cb.addItems(["X", "Y", "Z", "-X", "-Y", "-Z"])
        self.priAxis_cb.setCurrentText("Y")
        self.secAxis_cb = QtWidgets.QComboBox(self)
        self.secAxis_cb.addItems(["X", "Y", "Z", "-X", "-Y", "-Z"])
        self.secAxis_cb.setCurrentText("Z")
        self.fitMode_btn = QtWidgets.QPushButton("Fit Mode", self)

        self.preRig_btn = QtWidgets.QPushButton("Pre Rig", self)
        self.pubCheck_btn = QtWidgets.QPushButton("Pub Check", self)

        # CONNECT
        self.biped_btn.clicked.connect(partial(core.importBiped))
        self.fitSetup_btn.clicked.connect(partial(core.fitSetup))
        self.asymmetry_btn.clicked.connect(partial(core.asymmetrySetup))
        self.del_asymmetry_btn.clicked.connect(partial(core.delAsymmetrySetup))
        # self.priAxis_cb.currentIndexChanged.connect(partial(core.changedAxis))
        # self.secAxis_cb.currentIndexChanged.connect(partial(core.changedAxis))
        # self.fitMode_btn.clicked.connect(partial(core.editFitMode))
        # self.fitBuild_btn.clicked.connect(partial(core.fitBuild))
        self.preRig_btn.clicked.connect(partial(core.preRig))
        self.pubCheck_btn.clicked.connect(partial(core.pubCheck))

        # LAYOUT
        fitMode_layout = QtWidgets.QHBoxLayout()
        fitMode_layout.addWidget(self.priAxis_cb)
        fitMode_layout.addWidget(self.secAxis_cb)
        fitMode_layout.addWidget(self.fitMode_btn)

        asym_layout = QtWidgets.QHBoxLayout()
        asym_layout.addWidget(self.asymmetry_btn)
        asym_layout.addWidget(self.del_asymmetry_btn)

        fit_layout = QtWidgets.QVBoxLayout()
        fit_layout.addWidget(self.biped_btn)
        fit_layout.addWidget(self.fitSetup_btn)
        fit_layout.addLayout(asym_layout)
        fit_layout.addWidget(self.fitBuild_btn)
        fit_layout.addLayout(fitMode_layout)

        pre_layout = QtWidgets.QVBoxLayout()
        pre_layout.addWidget(self.preRig_btn)

        check_layout = QtWidgets.QVBoxLayout()
        check_layout.addWidget(self.pubCheck_btn)
        
        # GROUPBOX
        fit_gb = QtWidgets.QGroupBox('Fit Setup')
        fit_gb.setLayout(fit_layout)

        pre_gb = QtWidgets.QGroupBox('Pre Rig')
        pre_gb.setLayout(pre_layout)

        check_gb = QtWidgets.QGroupBox('Pub Check')
        check_gb.setLayout(check_layout)

        # WINDOW
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addStretch(1)
        main_layout.addWidget(fit_gb)
        main_layout.addWidget(pre_gb)
        main_layout.addWidget(check_gb)
        main_layout.addStretch(1)

        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
