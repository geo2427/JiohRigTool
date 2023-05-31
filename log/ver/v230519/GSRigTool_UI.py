#-*- coding: utf-8 -*-
import sys, imp, os
import pymel.all as pm
import maya.mel as mel
from functools import partial
from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import GSRigTool_Core as core
from util.modules.CorrectiveJntRig import CorrectiveJntRig_Core as crtv
from util.modules.deformerIssue import deformerIssue_Core as deformerIssue
from util.ui_commands import Container
imp.reload(core)
imp.reload(crtv)
imp.reload(deformerIssue)
imp.reload(Container)

        
server_path = "/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/"
icon_path = server_path + "/util/resources/"


class GSRigUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    TITLE = 'GSRigTool'
    VERSION  = '001'

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        self.setWindowTitle("{}_v{}".format(self.TITLE, self.VERSION))
        self.setGeometry(2400,500,370,400)
        self.setMinimumWidth(360)
        
        # TAB
        pre_tab = QtWidgets.QWidget()
        pre_tab.setLayout(self.create_pre_tab())
        
        rigging_tab = QtWidgets.QWidget()
        rigging_tab.setLayout(self.create_rigging_tab())
        
        tmp_tab = QtWidgets.QWidget()
        tmp_tab.setLayout(self.create_tmp_tab())
        
        post_tab = QtWidgets.QWidget()
        post_tab.setLayout(self.create_post_tab())
        
        main_tab = QtWidgets.QTabWidget()
        main_tab.addTab(pre_tab, 'Pre')
        # main_tab.addTab(rigging_tab, 'Rig')
        main_tab.addTab(tmp_tab, 'Rig')
        main_tab.addTab(post_tab, 'Post')

        # WINDOW
        main_win = QtWidgets.QVBoxLayout()
        main_win.addWidget(main_tab)
        
        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_win)
        self.setCentralWidget(widget)
    
    
    def create_pre_tab(self):
        
        # Font
        nfont = QtGui.QFont()
        nfont.setPointSize(11)
        nfont.setBold(True)
        
        # WIDGET
        self.sceneM_btn = QtWidgets.QPushButton("Scene Manager", self, fixedHeight=40, font=nfont, styleSheet="background: rgb(95,125,135);")
        self.AVS5_btn = QtWidgets.QPushButton("Run `AdvancedSkeleton9Fix`", self, fixedHeight=40, styleSheet="background: rgb(120,100,110);")
        self.GSbiped_btn = QtWidgets.QPushButton("Import `GS_biped.ma`", self)
        self.separator1 = QtWidgets.QFrame(styleSheet="background-color: gray;")
        self.separator1.setFrameShape(QtWidgets.QFrame.HLine)
        self.biped_btn = QtWidgets.QPushButton("Import `biped.ma`", self)
        self.fitSetup_btn = QtWidgets.QPushButton("Fit Setup", self)
        self.autoOrient_btn = QtWidgets.QPushButton("Auto-Orient", self)
        self.toggleOreint_cb = QtWidgets.QCheckBox("freeOreint", self)
        self.jointAxis_cb = QtWidgets.QCheckBox("joint-axis", self)
        self.poleVector_cb = QtWidgets.QCheckBox("pole-vector(미완)", self)
        self.crtvGuide_btn = QtWidgets.QPushButton("Corrective Guides", self) # minimumWidth=163.5
        self.crtvGuideDel_btn = QtWidgets.QPushButton("Delete", self, maximumWidth=100)
        self.asymmetry_btn = QtWidgets.QPushButton("Asymmetry", self)
        self.asymmetryDel_btn = QtWidgets.QPushButton("Delete", self, maximumWidth=100)
        self.fitBuild_btn = QtWidgets.QPushButton("Build AdvancedSkeleton", self, fixedHeight=40, styleSheet="background: rgb(130,90,100);")
        self.fitToggle_btn = QtWidgets.QPushButton("Toggle Fit", self)
        self.fitReBuild_btn = QtWidgets.QPushButton("ReBuild", self)
        self.preRigAll_cb = QtWidgets.QCheckBox("All", self, checked=1)
        self.preHier_cb = QtWidgets.QCheckBox("Milki Hierarchy", self, visible=False)
        self.preIKSub_cb = QtWidgets.QCheckBox("Add IKSub", self, visible=False)
        self.preOnoff_cb = QtWidgets.QCheckBox("OnoffCtrl", self, visible=False)
        self.editMain_cb = QtWidgets.QCheckBox("Edit MainCtrl Name", self, visible=False)
        self.ikLocalArm_cb = QtWidgets.QCheckBox("IKLocalArm Rotate Fix", self, visible=False)
        self.preRig_btn = QtWidgets.QPushButton("Pre Rig", self, fixedHeight=40, styleSheet="background: rgb(140,80,90);")
        self.pubCheck_btn = QtWidgets.QPushButton("Pub Check", self, fixedHeight=40, styleSheet="background: rgb(140,80,90);")
        # self.Milki_btn = QtWidgets.QPushButton("Milki", self, fixedHeight=40, font=nfont, styleSheet="background: rgb(95,125,135);")
        self.Milki_btn = QtWidgets.QPushButton("  Milki", self, font=nfont, icon=QtGui.QIcon(icon_path+"GS_icons/milki_menu_icon_resized.png"), iconSize=QtCore.QSize(31,31), styleSheet="background: rgb(95,125,135);")
        
        # CONNECT
        self.sceneM_btn.clicked.connect(partial(core.GSsceneManger))
        self.AVS5_btn.clicked.connect(partial(core.AdvancedSekelton5))
        self.GSbiped_btn.clicked.connect(partial(core.importGSBiped))
        self.biped_btn.clicked.connect(partial(core.importBiped))
        self.fitSetup_btn.clicked.connect(partial(core.fitSetup))
        self.autoOrient_btn.clicked.connect(partial(core.autoOrientSetup))
        self.toggleOreint_cb.clicked.connect(self.toggleFreeOrientHier)
        self.jointAxis_cb.toggled.connect(self.displayJointAxis)
        self.poleVector_cb.toggled.connect(self.displayPoleVector)
        self.crtvGuide_btn.clicked.connect(partial(crtv.importCrtvGuide))
        self.crtvGuideDel_btn.clicked.connect(partial(crtv.deleteCrtvGuide))
        self.asymmetry_btn.clicked.connect(partial(core.asymmetrySetup))
        self.asymmetry_btn.clicked.connect(partial(crtv.mirrorGuide))
        self.asymmetryDel_btn.clicked.connect(partial(core.delAsymmetrySetup))
        self.fitBuild_btn.clicked.connect(partial(core.fitBuild))
        self.fitBuild_btn.clicked.connect(partial(crtv.main))
        self.fitBuild_btn.clicked.connect(self.preRigRun)
        self.fitToggle_btn.clicked.connect(partial(core.fitToggleAVS))
        self.fitToggle_btn.clicked.connect(partial(crtv.toggleCrtvGuide))
        self.fitReBuild_btn.clicked.connect(partial(core.fitReBuild))
        self.fitReBuild_btn.clicked.connect(partial(crtv.ReBuildMain))
        self.preRigAll_cb.toggled.connect(self.preRigCheck)
        self.preRig_btn.clicked.connect(self.preRigRun)
        self.pubCheck_btn.clicked.connect(partial(core.pubCheck))
        self.Milki_btn.clicked.connect(partial(core.GSMilki))

        # LAYOUT
        AVS5_layout = QtWidgets.QVBoxLayout()
        # AVS5_layout.setAlignment(QtCore.Qt.AlignCenter)
        AVS5_layout.addWidget(self.sceneM_btn)
        AVS5_layout.addWidget(self.AVS5_btn)

        display_layout = QtWidgets.QHBoxLayout()
        display_layout.addWidget(self.jointAxis_cb)
        display_layout.addWidget(self.poleVector_cb)

        orient_layout = QtWidgets.QHBoxLayout()
        orient_layout.addWidget(self.autoOrient_btn)
        orient_layout.addWidget(self.toggleOreint_cb)
    
        fit_layout = QtWidgets.QVBoxLayout()
        fit_layout.addWidget(self.GSbiped_btn)
        fit_layout.addWidget(self.fitSetup_btn)
        fit_layout.addLayout(orient_layout)
        fit_layout.addLayout(display_layout)
        
        asym_layout = QtWidgets.QHBoxLayout()
        asym_layout.addWidget(self.asymmetry_btn)
        asym_layout.addWidget(self.asymmetryDel_btn)
                
        crtv_layout = QtWidgets.QHBoxLayout()
        crtv_layout.addWidget(self.crtvGuide_btn)
        crtv_layout.addWidget(self.crtvGuideDel_btn)
        
        extra_layout = QtWidgets.QVBoxLayout()
        extra_layout.addLayout(crtv_layout)
        extra_layout.addLayout(asym_layout)
             
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
        self.preSec_layout.addWidget(self.editMain_cb)
        self.preSec_layout.addWidget(self.ikLocalArm_cb)
        
        pre_layout = QtWidgets.QHBoxLayout()
        pre_layout.addLayout(self.preSec_layout)
        pre_layout.addWidget(self.preRig_btn)
        
        post_layout = QtWidgets.QHBoxLayout()
        post_layout.addWidget(self.pubCheck_btn)
        post_layout.addWidget(self.Milki_btn)
        
        # GROUPBOX
        AVS5_gb = QtWidgets.QGroupBox()
        AVS5_gb.setLayout(AVS5_layout)
        
        fit_gb = QtWidgets.QGroupBox('Fit Setup')
        fit_gb.setLayout(fit_layout)
        
        extra_gb = QtWidgets.QGroupBox('Extra Setup')
        extra_gb.setLayout(extra_layout)
        
        build_gb = QtWidgets.QGroupBox()
        build_gb.setLayout(build_layout)
        
        pre_gb = QtWidgets.QGroupBox('After Build')
        pre_gb.setLayout(pre_layout)
        
        post_gb = QtWidgets.QGroupBox('Pub')
        post_gb.setLayout(post_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(AVS5_gb)
        main_layout.addWidget(fit_gb)
        main_layout.addWidget(extra_gb)
        main_layout.addWidget(build_gb)
        main_layout.addWidget(pre_gb)
        main_layout.addWidget(post_gb)
        main_layout.addStretch(1)
        
        return main_layout
    
    
    def create_rigging_tab(self):
        
        # WIDGET
        self.switchFKIK_btn = QtWidgets.QPushButton("Switch FKIK", self)
        self.setCtrlZero_btn = QtWidgets.QPushButton("Ctrl = 0", self)
        self.osGrp_btn = QtWidgets.QPushButton("OffsetGrp", self)
        self.rename_btn = QtWidgets.QPushButton("Rename Tool", self)
        self.colorMaker_btn = QtWidgets.QPushButton("Color Maker", self)
        self.skinHelp_btn = QtWidgets.QPushButton("Skin Help Tool", self)
        self.JH_btn = QtWidgets.QPushButton("JHRigTool", self)
        self.folSub_btn = QtWidgets.QPushButton("FolSubRig Tool", self)
        self.simpleRig_btn = QtWidgets.QPushButton("Bin Simple Rig Tool", self)
        self.HIKsetup_btn = QtWidgets.QPushButton("HIKsetup Tool", self)
        
        # CONNECT
        self.switchFKIK_btn.clicked.connect(partial(core.switchFKIKBlend))
        self.setCtrlZero_btn.clicked.connect(partial(core.setCtrlZero))
        # self.osGrp_btn.clicked.connect(partial(core.makeOffsetGrp_Sangsu))
        self.osGrp_btn.clicked.connect(self.osGrpUI_run)
        self.rename_btn.clicked.connect(partial(core.RunRenameTool))
        self.colorMaker_btn.clicked.connect(partial(core.RunColorTool))
        self.skinHelp_btn.clicked.connect(partial(core.RunSkinHelpTool))
        self.JH_btn.clicked.connect(partial(core.RunJHRigTool))
        self.folSub_btn.clicked.connect(partial(core.RunFolSubRigTool))
        self.simpleRig_btn.clicked.connect(partial(core.RunBinSimpleRigTool))
        self.HIKsetup_btn.clicked.connect(partial(core.RunHIKsetupTool))
        
        # LAYOUT
        rigHelpScript_layout = QtWidgets.QVBoxLayout()
        rigHelpScript_layout.addWidget(self.switchFKIK_btn)
        rigHelpScript_layout.addWidget(self.setCtrlZero_btn)
        rigHelpScript_layout.addWidget(self.osGrp_btn)
        
        rigHelpTool_layout = QtWidgets.QVBoxLayout()
        rigHelpTool_layout.addWidget(self.rename_btn)
        rigHelpTool_layout.addWidget(self.skinHelp_btn)
        rigHelpTool_layout.addWidget(self.JH_btn)
        rigHelpTool_layout.addWidget(self.colorMaker_btn)
        
        rigSub_layout = QtWidgets.QVBoxLayout()
        rigSub_layout.addWidget(self.simpleRig_btn)
        rigSub_layout.addWidget(self.folSub_btn)

        otherTool_layout = QtWidgets.QVBoxLayout()
        otherTool_layout.addWidget(self.HIKsetup_btn)
        
        # GROUPBOX
        rigHelpScript_gb = QtWidgets.QGroupBox('')
        rigHelpScript_gb.setLayout(rigHelpScript_layout)
        
        rigHelpTool_gb = QtWidgets.QGroupBox('Rig Tools')
        rigHelpTool_gb.setLayout(rigHelpTool_layout)
        
        rigSub_gb = QtWidgets.QGroupBox('Sub / Prop')
        rigSub_gb.setLayout(rigSub_layout)
        
        otherTool_gb = QtWidgets.QGroupBox('Others')
        otherTool_gb.setLayout(otherTool_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(rigHelpScript_gb)
        main_layout.addWidget(rigHelpTool_gb)
        main_layout.addWidget(rigSub_gb)
        main_layout.addWidget(otherTool_gb)
        main_layout.addStretch(1)
        
        return main_layout
    
    
    def create_tmp_tab(self):
        
        # SETTING
        size = QtCore.QSize(27,27)
        cnst_rgb="background: rgb(95,90,105);"
        nfont = QtGui.QFont()
        nfont.setPointSize(20)
        
        # WIDGET
        self.driver_label = QtWidgets.QLabel("[    driver    ]", self, alignment=QtCore.Qt.AlignCenter)
        self.driver_list = QtWidgets.QListWidget(self, minimumHeight=200, minimumWidth=140)
        self.driver_replace_btn = QtWidgets.QPushButton("Add", self)
        self.driver_remove_btn = QtWidgets.QPushButton("Remove", self)
        self.to_label = QtWidgets.QLabel(">>", self)
        self.driven_label = QtWidgets.QLabel("[    driven    ]", self, alignment=QtCore.Qt.AlignCenter)
        self.driven_list = QtWidgets.QListWidget(self, minimumHeight=200, minimumWidth=140)
        self.driven_replace_btn = QtWidgets.QPushButton("Add", self)
        self.driven_remove_btn = QtWidgets.QPushButton("Remove", self)
        
        self.maintainOs_cb = QtWidgets.QCheckBox("Maintain Offset", self)
        self.prntCnst_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/parentConstraint.png"), iconSize=size, styleSheet=cnst_rgb)
        self.pntCnst_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/posConstraint.png"), iconSize=size, styleSheet=cnst_rgb)
        self.oriCnst_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/orientConstraint.png"), iconSize=size, styleSheet=cnst_rgb)
        self.scaCnst_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/scaleConstraint.png"), iconSize=size, styleSheet=cnst_rgb)
        self.connect_btn = QtWidgets.QPushButton("↦", self, font=nfont, styleSheet="background: rgb(175,140,50);")
        self.disconnect_btn = QtWidgets.QPushButton("↛", self, font=nfont, styleSheet="background: rgb(175,170,130);")
        self.lock_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/lockGeneric.png"), iconSize=size, styleSheet="background: rgb(90,110,120);")
        self.unlock_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/unlockGeneric.png"), iconSize=size, styleSheet="background: rgb(120,125,130);")
        
        self.osGrp_btn = QtWidgets.QPushButton("OffsetGrp", self)
        self.parent_btn = QtWidgets.QPushButton("Parent", self)
        self.switchFKIK_btn = QtWidgets.QPushButton("Switch FKIK", self)
        self.setCtrlZero_btn = QtWidgets.QPushButton("Ctrl = 0", self)
        
        self.rename_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path+"/maya_icons/RenameTool.png"), iconSize=QtCore.QSize(35,40))
        self.colorMaker_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path+"/maya_icons/ColorMarker.png"), iconSize=QtCore.QSize(45,40))
        self.skinHelp_btn = QtWidgets.QPushButton("  Skin Help Tool", self, icon=QtGui.QIcon(":/paintSkinWeights.png"), iconSize=QtCore.QSize(35,40))
        self.folSub_btn = QtWidgets.QPushButton("FolSubRig Tool", self)
        self.simpleRig_btn = QtWidgets.QPushButton("Bin Simple Rig Tool", self)
        self.propRig_btn = QtWidgets.QPushButton("Prop Rig Tool", self)
        self.HIKsetup_btn = QtWidgets.QPushButton("HIKsetup Tool", self)
        
        self.separator1 = QtWidgets.QFrame(styleSheet="background-color: gray;")
        self.separator1.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator2 = QtWidgets.QFrame(styleSheet="background-color: gray;", fixedHeight=2)
        self.separator2.setFrameShape(QtWidgets.QFrame.HLine)
        
        # CONNECT
        self.driver_replace_btn.clicked.connect(partial(core.ReplaceItemList, self.driver_list))
        self.driver_remove_btn.clicked.connect(partial(core.RemoveItemList, self.driver_list))
        self.driven_replace_btn.clicked.connect(partial(core.ReplaceItemList, self.driven_list))
        self.driven_remove_btn.clicked.connect(partial(core.RemoveItemList, self.driven_list))
        
        # self.prntCnst_btn.clicked.connect(partial(core.ConstraintCmd_2, self.driver_list, self.driven_list, self.maintainOs_cb.checkState(), self.))
        # self.pntCnst_btn.clicked.connect(partial(core.ConstraintCmd_2, self.driver_list, self.driven_list))
        # self.oriCnst_btn.clicked.connect(partial(core.ConstraintCmd_2, self.driver_list, self.driven_list))
        # self.scaCnst_btn.clicked.connect(partial(core.ConstraintCmd_2, self.driver_list, self.driven_list))
        
        self.switchFKIK_btn.clicked.connect(partial(core.switchFKIKBlend))
        self.setCtrlZero_btn.clicked.connect(partial(core.setCtrlZero))
        self.osGrp_btn.clicked.connect(partial(core.makeOffsetGrp))
        self.rename_btn.clicked.connect(partial(core.RunRenameTool))
        self.colorMaker_btn.clicked.connect(partial(core.RunColorTool))
        self.skinHelp_btn.clicked.connect(partial(core.RunSkinHelpTool))
        self.folSub_btn.clicked.connect(partial(core.RunFolSubRigTool))
        self.simpleRig_btn.clicked.connect(partial(core.RunBinSimpleRigTool))
        self.propRig_btn.clicked.connect(partial(core.RunPropRigTool))
        self.HIKsetup_btn.clicked.connect(partial(core.RunHIKsetupTool))
        
        # LAYOUT
        driverAdd_layout = QtWidgets.QHBoxLayout()
        driverAdd_layout.addWidget(self.driver_replace_btn)
        driverAdd_layout.addWidget(self.driver_remove_btn)
        
        driver_layout = QtWidgets.QVBoxLayout()
        driver_layout.addWidget(self.driver_label)
        driver_layout.addWidget(self.driver_list)
        driver_layout.addLayout(driverAdd_layout)
        
        drivenAdd_layout = QtWidgets.QHBoxLayout()
        drivenAdd_layout.addWidget(self.driven_replace_btn)
        drivenAdd_layout.addWidget(self.driven_remove_btn)
        
        driven_layout = QtWidgets.QVBoxLayout()
        driven_layout.addWidget(self.driven_label)
        driven_layout.addWidget(self.driven_list)
        driven_layout.addLayout(drivenAdd_layout)
        
        listWidget_layout = QtWidgets.QHBoxLayout()
        listWidget_layout.addLayout(driver_layout)
        listWidget_layout.addWidget(self.to_label)
        listWidget_layout.addLayout(driven_layout)
        
        cnst_layout = QtWidgets.QHBoxLayout()
        cnst_layout.addWidget(self.prntCnst_btn)
        cnst_layout.addWidget(self.pntCnst_btn)
        cnst_layout.addWidget(self.oriCnst_btn)
        cnst_layout.addWidget(self.scaCnst_btn)
        
        connection_layout = QtWidgets.QHBoxLayout()
        connection_layout.addWidget(self.connect_btn)
        connection_layout.addWidget(self.disconnect_btn)
        
        lock_layout = QtWidgets.QHBoxLayout()
        lock_layout.addWidget(self.lock_btn)
        lock_layout.addWidget(self.unlock_btn)
        
        etc_layout = QtWidgets.QHBoxLayout() # alignment=QtCore.Qt.AlignCenter
        etc_layout.addWidget(self.osGrp_btn)
        etc_layout.addWidget(self.parent_btn)
        etc_layout.addWidget(self.switchFKIK_btn)
        etc_layout.addWidget(self.setCtrlZero_btn)
        
        rigHelp_layout = QtWidgets.QVBoxLayout()
        rigHelp_layout.addLayout(listWidget_layout)
        rigHelp_layout.addWidget(self.separator1)
        rigHelp_layout.addWidget(self.maintainOs_cb)
        rigHelp_layout.addLayout(cnst_layout)
        rigHelp_layout.addWidget(self.separator2)
        rigHelp_layout.addLayout(connection_layout)
        rigHelp_layout.addLayout(lock_layout)

        rigHelpTool1_layout = QtWidgets.QHBoxLayout()
        rigHelpTool1_layout.addWidget(self.rename_btn)
        rigHelpTool1_layout.addWidget(self.colorMaker_btn)
        
        rigHelpTool_layout = QtWidgets.QVBoxLayout()
        rigHelpTool_layout.addLayout(rigHelpTool1_layout)
        rigHelpTool_layout.addWidget(self.skinHelp_btn)
        
        otherTool_con = Container.Main("Other Tools")
        otherTool_layout = QtWidgets.QVBoxLayout()
        otherTool_layout.addWidget(otherTool_con)
        container_lay1 = QtWidgets.QGridLayout(otherTool_con.contentWidget)
        container_lay1.addWidget(self.simpleRig_btn)
        container_lay1.addWidget(self.propRig_btn)
        container_lay1.addWidget(self.folSub_btn)
        container_lay1.addWidget(self.HIKsetup_btn)
        
        # GROUPBOX
        rigHelp_gb = QtWidgets.QGroupBox('Rig Help(미완성)')
        rigHelp_gb.setLayout(rigHelp_layout)
        
        rigHelp2_gb = QtWidgets.QGroupBox('')
        rigHelp2_gb.setLayout(etc_layout)
        
        rigHelpTool_gb = QtWidgets.QGroupBox('Rig Tools')
        rigHelpTool_gb.setLayout(rigHelpTool_layout)
        
        otherTool_gb = QtWidgets.QGroupBox('')
        otherTool_gb.setLayout(otherTool_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(rigHelp_gb)
        main_layout.addWidget(rigHelp2_gb)
        main_layout.addWidget(rigHelpTool_gb)
        main_layout.addWidget(otherTool_gb)
        main_layout.addStretch(1)
        
        return main_layout
    
    
    def create_post_tab(self):
    
        # WIDGET
        self.deformerIssue_btn = QtWidgets.QPushButton("Fix Deformer Evaluation Inaccuracy", self)
        self.headSquash_btn = QtWidgets.QPushButton("Fix Head Squash", self)
        self.MTX2_btn = QtWidgets.QPushButton("MTX2: import shader", self)
        self.afterMTX_btn = QtWidgets.QPushButton("Import Shader & Generate Preview", self)

        # CONNECT        
        self.deformerIssue_btn.clicked.connect(partial(deformerIssue.deformerIssueRun))
        self.headSquash_btn.clicked.connect(partial(core.fixAVSHeadSquash))
        # self.pubCheck_btn.clicked.connect(partial(core.pubCheck))
        self.MTX2_btn.clicked.connect(partial(core.GS_MTX2))
        self.afterMTX_btn.clicked.connect(partial(core.RunAfterShader))
        
        # LAYOUT
        post_layout = QtWidgets.QVBoxLayout()
        post_layout.addWidget(self.deformerIssue_btn)
        post_layout.addWidget(self.headSquash_btn)
        
        check_layout = QtWidgets.QVBoxLayout()
        # check_layout.addWidget(self.pubCheck_btn)
        check_layout.addWidget(self.MTX2_btn)
        check_layout.addWidget(self.afterMTX_btn)
        
        # GROUPBOX
        post_gb = QtWidgets.QGroupBox('Post Rig')
        post_gb.setLayout(post_layout)
        
        check_gb = QtWidgets.QGroupBox('Shader')
        check_gb.setLayout(check_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(post_gb)
        main_layout.addWidget(check_gb)
        main_layout.addStretch(1)
        
        return main_layout
    
    
    ##########################################################################################


    def displayPoleVector(self):
        pass
    
    
    def preRigCheck(self):
        
        if self.preRigAll_cb.isChecked():
            self.preHier_cb.setVisible(0)
            self.preIKSub_cb.setVisible(0)
            self.preOnoff_cb.setVisible(0)
            self.editMain_cb.setVisible(0)
            self.ikLocalArm_cb.setVisible(0)

        else:
            self.preHier_cb.setChecked(1)
            self.preIKSub_cb.setChecked(1)
            self.preOnoff_cb.setChecked(1)
            self.editMain_cb.setChecked(1)
            self.ikLocalArm_cb.setChecked(1)
            
            self.preHier_cb.setVisible(1)
            self.preIKSub_cb.setVisible(1)
            self.preOnoff_cb.setVisible(1)
            self.editMain_cb.setVisible(1)
            self.ikLocalArm_cb.setVisible(1)
    
   
    def preRigRun(self):
        
        print("\n[ Pre-RIG ]")
        
        if self.preRigAll_cb.isChecked():
            with pm.UndoChunk():
                core.editMainName()
                core.milkiHierarchy()
                core.addIKSubPart()
                core.createOnOffCtrl()
                core.IKLocalArmSetup()
        
        else:
            if self.preHier_cb.isChecked():
                with pm.UndoChunk():
                    core.milkiHierarchy()
                
            if self.preIKSub_cb.isChecked():
                with pm.UndoChunk():
                    core.addIKSubPart()
                
            if self.preOnoff_cb.isChecked():
                with pm.UndoChunk():
                    core.createOnOffCtrl()
                    
            if self.editMain_cb.isChecked():
                with pm.UndoChunk():
                    core.editMainName()
              
            if self.ikLocalArm_cb.isChecked():
                with pm.UndoChunk():
                    core.IKLocalArmSetup()
    
     
    def colorPalette(self):
        for i in range(1, 32):
            r, g, b = pm.colorIndex(i, q=1)
            pm.canvas(rgbValue=(r, g, b), w=20, h=20) # , pc=partial(core.SetColor, i)
    
    
    def toggleFreeOrientHier(self):
        
        jntL = []
        for obj in pm.ls('Root', dag=True):
            if pm.nodeType(obj)=='joint':
                jntL.append(pm.PyNode(obj))
            
        if self.toggleOreint_cb.isChecked():
            [ pm.setAttr(jnt.freeOrient, 1) for jnt in jntL ]
            pm.displayInfo('freeOrient = 1')
        else:
            [ pm.setAttr(jnt.freeOrient, 0) for jnt in jntL ]
            pm.displayInfo('freeOrient = 0')
    
    
    def displayJointAxis(self):
        
        onoff = self.jointAxis_cb.isChecked()

        jntL = pm.listRelatives('Root', ad=True)
        for jnt in jntL:
            child = pm.listRelatives(jnt, c=True)
            if not child:
                continue
            pm.setAttr(jnt+'.displayLocalAxis', onoff)
            
            
    def osGrpUI_run(self):
        
        global win
        try:
            win.close()
            win.deleteLater()
        except:
            pass
        
        window = osGrpUI()
        window.show()


class osGrpUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)
        self.setWindowTitle("Group_Name")

        # qtRectangle = self.frameGeometry()
        # centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        # qtRectangle.moveCenter(centerPoint)
        # self.move(qtRectangle.topLeft())
    
        self.line_edit = QtWidgets.QLineEdit(self)
        self.ok_btn = QtWidgets.QPushButton("OK", self)
        
        self.ok_btn.clicked.connect(lambda: partial(core.makeOffsetGrp_Sangsu(self.line_edit.text())))

        self.osGrp_lay = QtWidgets.QVBoxLayout()
        self.osGrp_lay.addWidget(self.line_edit)
        self.osGrp_lay.addWidget(self.ok_btn)
        
        widget = QtWidgets.QWidget(self)
        widget.setLayout(self.osGrp_lay)
        self.setCentralWidget(widget)



