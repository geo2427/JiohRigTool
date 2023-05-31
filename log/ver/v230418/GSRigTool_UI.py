#-*- coding: utf-8 -*-
import sys, imp, os
import pymel.all as pm
import maya.mel as mel
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial

import GSRigTool_Core as core
imp.reload(core)

from util.modules.CorrectiveJntRig import CorrectiveJntRig_Core as crtv
imp.reload(crtv)


class GSRigUI(QtWidgets.QMainWindow):
    TITLE = 'GSRigTool'
    VERSION  = '230418'
    # ICON = '/home/jioh.kim/Desktop/pipe/wip/A/GSRigTool/util/resources/GSLogo.png'

    def __init__(self, parent=None):
        super(GSRigUI, self).__init__()

        self.setWindowTitle("{}_v{}".format(self.TITLE, self.VERSION))
        # self.setWindowIcon(QtGui.QIcon(self.ICON))
        self.setGeometry(1800,500,375,400)
        self.setMinimumWidth(375)
        
        # WIDGET
        self.AVS5_btn = QtWidgets.QPushButton("Run `AdvancedSkeleton9Fix`", self, fixedHeight=40, styleSheet="background: rgb(120,100,110);")
        self.biped_btn = QtWidgets.QPushButton("Import `biped.ma`", self)
        self.fitSetup_btn = QtWidgets.QPushButton("Fit Setup", self)
        self.autoOrient_btn = QtWidgets.QPushButton("Auto-Orient", self)
        self.jointAxis_cb = QtWidgets.QCheckBox("joint-axis", self)
        self.poleVector_cb = QtWidgets.QCheckBox("pole-vector(미완)", self)
        self.separator = QtWidgets.QFrame(styleSheet="background-color: gray;")
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.crtvGuide_btn = QtWidgets.QPushButton("Corrective Guides", self) # minimumWidth=163.5
        # self.crtvGuide_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, singleStep=1, minimum=1, maximum=100, value=30) # fixedWidth = 163
        self.crtvGuideDel_btn = QtWidgets.QPushButton("Delete Corrective", self)
        self.asymmetry_btn = QtWidgets.QPushButton("Asymmetry", self)
        self.asymmetryDel_btn = QtWidgets.QPushButton("Delete Asymmetry", self)
        self.fitBuild_btn = QtWidgets.QPushButton("Build AdvancedSkeleton", self, fixedHeight=40, styleSheet="background: rgb(130,90,100);")
        self.fitToggle_btn = QtWidgets.QPushButton("Toggle Fit", self)
        self.fitReBuild_btn = QtWidgets.QPushButton("ReBuild", self)
        self.preRigAll_cb = QtWidgets.QCheckBox("All", self, checked=1)
        self.preHier_cb = QtWidgets.QCheckBox("Milki Hierarchy", self, visible=False)
        self.preIKSub_cb = QtWidgets.QCheckBox("IKSubArm", self, visible=False)
        self.preOnoff_cb = QtWidgets.QCheckBox("OnoffCtrl", self, visible=False)
        self.preRig_btn = QtWidgets.QPushButton("Pre Rig", self)
        self.pubCheck_btn = QtWidgets.QPushButton("Pub Check", self)

        # CONNECT
        self.AVS5_btn.clicked.connect(partial(core.AdvancedSekelton5))
        self.biped_btn.clicked.connect(partial(core.importBiped))
        self.fitSetup_btn.clicked.connect(partial(core.fitSetup))
        self.autoOrient_btn.clicked.connect(partial(core.autoOrientSetup))
        self.jointAxis_cb.toggled.connect(self.displayJointAxis)
        self.poleVector_cb.toggled.connect(self.displayPoleVector)
        self.crtvGuide_btn.clicked.connect(partial(crtv.importCrtvGuide))
        self.crtvGuideDel_btn.clicked.connect(partial(crtv.deleteCrtvGuide))
        # self.crtvGuide_slider.valueChanged.connect(self.crtvSlider)
        self.asymmetry_btn.clicked.connect(partial(core.asymmetrySetup))
        self.asymmetry_btn.clicked.connect(partial(crtv.mirrorGuide))
        self.asymmetryDel_btn.clicked.connect(partial(core.delAsymmetrySetup))
        self.fitBuild_btn.clicked.connect(partial(core.fitBuild))
        self.fitBuild_btn.clicked.connect(partial(crtv.main))
        self.fitToggle_btn.clicked.connect(partial(core.fitToggleAVS))
        self.fitToggle_btn.clicked.connect(partial(crtv.toggleCrtvGuide))
        self.fitReBuild_btn.clicked.connect(partial(core.fitReBuild))
        self.fitReBuild_btn.clicked.connect(partial(crtv.ReBuildMain))
        self.preRigAll_cb.toggled.connect(self.preRigCheck)
        self.preRig_btn.clicked.connect(self.preRigRun)
        self.pubCheck_btn.clicked.connect(partial(core.pubCheck))

        # LAYOUT
        AVS5_layout = QtWidgets.QVBoxLayout()
        # AVS5_layout.setAlignment(QtCore.Qt.AlignCenter)/
        AVS5_layout.addWidget(self.AVS5_btn)

        display_layout = QtWidgets.QHBoxLayout()
        display_layout.addWidget(self.jointAxis_cb)
        display_layout.addWidget(self.poleVector_cb)
        
        crtv_layout = QtWidgets.QHBoxLayout()
        crtv_layout.addWidget(self.crtvGuide_btn)
        crtv_layout.addWidget(self.crtvGuideDel_btn)
        # crtv_layout.addWidget(self.crtvGuide_slider)
        
        asym_layout = QtWidgets.QHBoxLayout()
        asym_layout.addWidget(self.asymmetry_btn)
        asym_layout.addWidget(self.asymmetryDel_btn)

        fit_layout = QtWidgets.QVBoxLayout()
        fit_layout.addWidget(self.biped_btn)
        fit_layout.addWidget(self.fitSetup_btn)
        fit_layout.addWidget(self.autoOrient_btn)
        fit_layout.addLayout(display_layout)
        fit_layout.addWidget(self.separator)
        fit_layout.addLayout(asym_layout)
        fit_layout.addLayout(crtv_layout)
             
        rebuild_layout = QtWidgets.QHBoxLayout()
        rebuild_layout.addWidget(self.fitToggle_btn)
        rebuild_layout.addWidget(self.fitReBuild_btn)
           
        build_layout = QtWidgets.QVBoxLayout()
        build_layout.addWidget(self.fitBuild_btn)
        build_layout.addLayout(rebuild_layout)

        self.preSec_layout = QtWidgets.QVBoxLayout()
        self.preSec_layout.addWidget(self.preRigAll_cb)
        self.preSec_layout.addWidget(self.preHier_cb)
        self.preSec_layout.addWidget(self.preIKSub_cb)
        self.preSec_layout.addWidget(self.preOnoff_cb)
        
        pre_layout = QtWidgets.QHBoxLayout()
        pre_layout.addLayout(self.preSec_layout)
        pre_layout.addWidget(self.preRig_btn)

        check_layout = QtWidgets.QVBoxLayout()
        check_layout.addWidget(self.pubCheck_btn)
        
        
        # GROUPBOX
        AVS5_gb = QtWidgets.QGroupBox('Run AVS')
        AVS5_gb.setLayout(AVS5_layout)
        
        fit_gb = QtWidgets.QGroupBox('Fit Setup')
        fit_gb.setLayout(fit_layout)
        
        build_gb = QtWidgets.QGroupBox('Build')
        build_gb.setLayout(build_layout)
        
        pre_gb = QtWidgets.QGroupBox('Pre Rig')
        pre_gb.setLayout(pre_layout)

        check_gb = QtWidgets.QGroupBox('Pub Check')
        check_gb.setLayout(check_layout)

        # WINDOW
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(AVS5_gb)
        main_layout.addWidget(fit_gb)
        main_layout.addWidget(build_gb)
        main_layout.addWidget(pre_gb)
        main_layout.addWidget(check_gb)
        main_layout.addStretch(1)

        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    
    ##########################################################################################
    ##########################################################################################
    
    
    def displayJointAxis(self):
        
        onoff = self.jointAxis_cb.isChecked()

        jntL = pm.listRelatives('Root', ad=True)
        for jnt in jntL:
            child = pm.listRelatives(jnt, c=True)
            if not child:
                continue
            pm.setAttr(jnt+'.displayLocalAxis', onoff)


    def displayPoleVector(self):
        pass
    
    
    def preRigCheck(self):
        
        if self.preRigAll_cb.isChecked():
            self.preHier_cb.setVisible(0)
            self.preIKSub_cb.setVisible(0)
            self.preOnoff_cb.setVisible(0)

        else:
            self.preHier_cb.setChecked(1)
            self.preIKSub_cb.setChecked(1)
            self.preOnoff_cb.setChecked(1)
            
            self.preHier_cb.setVisible(1)
            self.preIKSub_cb.setVisible(1)
            self.preOnoff_cb.setVisible(1)
            
    
    def preRigRun(self):
        
        print("\n[ Pre-RIG ]")
        
        if self.preRigAll_cb.isChecked():
            with pm.UndoChunk():
                core.milkiHierarchy()
                core.addIKSubArm()
                core.createOnOffCtrl()
        
        else:
            if self.preHier_cb.isChecked():
                with pm.UndoChunk():
                    core.milkiHierarchy()
                
            if self.preIKSub_cb.isChecked():
                with pm.UndoChunk():
                    core.addIKSubArm()
                
            if self.preOnoff_cb.isChecked():
                with pm.UndoChunk():
                    core.createOnOffCtrl()
                
            
    # def crtvSlider(self, var):
    #     val = self.crtvGuide_slider.value()
    #     realVal = float(val) / 10
    #     print(realVal)
    #     return realVal
    
    # def crtvSlider_2(self):
    #     self.crtvSlider(var)


# if __name__ == '__main__':
#   app = QApplication(sys.argv)
#   ex = MyApp()
#   sys.exit(app.exec_())

