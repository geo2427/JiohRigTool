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
from util.modules.golaemSetting import golaemSetting_Core as golaem
from util.ui_commands import Container
imp.reload(core)
imp.reload(crtv)
imp.reload(deformerIssue)
imp.reload(golaem)
imp.reload(Container)

        
server_path = "/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/"
icon_path = server_path + "/util/resources/"


class GSRigUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        self.setWindowTitle("GSRigTool")
        self.setGeometry(2400,500,375,400)
        self.setMinimumWidth(375)
        
        # TAB
        pre_tab = QtWidgets.QWidget()
        pre_tab.setLayout(self.GS_Pre_Tab())
        
        tmp_tab = QtWidgets.QWidget()
        tmp_tab.setLayout(self.GS_Rig_Tab())
        
        post_tab = QtWidgets.QWidget()
        post_tab.setLayout(self.GS_Other_Tab())
        
        main_tab = QtWidgets.QTabWidget()
        main_tab.addTab(pre_tab, 'Pre')
        main_tab.addTab(tmp_tab, 'Rig')
        main_tab.addTab(post_tab, 'Other')

        # WINDOW
        main_win = QtWidgets.QVBoxLayout()
        main_win.addWidget(main_tab)
        
        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_win)
        self.setCentralWidget(widget)
    
    
    def GS_Pre_Tab(self):
        
        # Font
        nfont = QtGui.QFont()
        nfont.setPointSize(11)
        nfont.setBold(True)
        
        # WIDGET
        self.sceneM_btn = QtWidgets.QPushButton("Scene Manager", self, fixedHeight=40, font=nfont, styleSheet="background: rgb(95,125,135);")
        self.AVS5_btn = QtWidgets.QPushButton("  AdvancedSkeleton", self, icon=QtGui.QIcon(icon_path+"/maya_icons/AS5.png"), iconSize=QtCore.QSize(31,31), styleSheet="background: rgb(130,90,100);")
        self.GSbiped_btn = QtWidgets.QPushButton("  import 'GS_biped'", self, icon=QtGui.QIcon(icon_path+"/maya_icons/asBiped.png"), iconSize=QtCore.QSize(31,31), styleSheet="background: rgb(130,90,100);")
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
        self.pubCheck_btn = QtWidgets.QPushButton("Pub Check", self, fixedHeight=40, styleSheet="background: rgb(140,80,90);")
        self.Milki_btn = QtWidgets.QPushButton("  Milki", self, font=nfont, icon=QtGui.QIcon(icon_path+"GS_icons/milki_menu_icon_resized.png"), iconSize=QtCore.QSize(31,31), styleSheet="background: rgb(95,125,135);")
        
        self.rename_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path+"/maya_icons/RenameTool.png"), iconSize=QtCore.QSize(35,40))
        self.colorMaker_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path+"/maya_icons/ColorMarker.png"), iconSize=QtCore.QSize(45,40))
        self.skinHelp_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/paintSkinWeights.png"), iconSize=QtCore.QSize(35,40))
        self.propRig_btn = QtWidgets.QPushButton("  Prop", self, icon=QtGui.QIcon(icon_path+"/maya_icons/PropRigTool.png"), iconSize=QtCore.QSize(35,40))
        self.mocap_btn = QtWidgets.QPushButton("MocapMatcher", self)
        self.folSub_btn = QtWidgets.QPushButton("FolSubRig Tool", self)
        self.simpleRig_btn = QtWidgets.QPushButton("Bin Simple Rig Tool", self)
        self.HIKsetup_btn = QtWidgets.QPushButton("HIKsetup Tool", self)
        
        self.GSbiped_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.GSbiped_btn.customContextMenuRequested.connect(self.popupFitSetup)
        self.fitSetup_menu = QtWidgets.QMenu()
        self.fitSetup_item = QtWidgets.QAction('Fit Setup')
        self.fitSetup_menu.addAction(self.fitSetup_item)
        self.fitBuild_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.fitBuild_btn.customContextMenuRequested.connect(self.popupPreRig)
        self.preRig_menu = QtWidgets.QMenu()
        self.preRig_item = QtWidgets.QAction('Pre Rig')
        self.preRig_menu.addAction(self.preRig_item)
        
        self.separator1 = QtWidgets.QFrame(styleSheet="background-color: gray;")
        self.separator1.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator2 = QtWidgets.QFrame(styleSheet="background-color: gray;")
        self.separator2.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator3 = QtWidgets.QFrame(styleSheet="background: rgb(50,50,50);", fixedHeight=5)
        self.separator3.setFrameShape(QtWidgets.QFrame.HLine)
        
        # CONNECT
        self.sceneM_btn.clicked.connect(partial(core.GSsceneManger))
        self.AVS5_btn.clicked.connect(partial(core.AdvancedSekelton5))
        self.GSbiped_btn.clicked.connect(partial(core.importGSBiped))
        self.fitSetup_item.triggered.connect(partial(core.fitSetup))
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
        self.fitBuild_btn.clicked.connect(partial(crtv.Build))
        self.preRig_item.triggered.connect(partial(core.RunPreRig))
        self.fitToggle_btn.clicked.connect(partial(core.fitToggleAVS))
        self.fitToggle_btn.clicked.connect(partial(crtv.toggleCrtvGuide))
        self.fitReBuild_btn.clicked.connect(partial(core.fitReBuild))
        self.fitReBuild_btn.clicked.connect(partial(crtv.Rebuild))
        self.pubCheck_btn.clicked.connect(partial(core.pubCheck))
        self.Milki_btn.clicked.connect(partial(core.GSMilki))
        
        self.rename_btn.clicked.connect(partial(core.RunRenameTool))
        self.colorMaker_btn.clicked.connect(partial(core.RunColorTool))
        self.skinHelp_btn.clicked.connect(partial(core.RunSkinHelpTool))
        self.propRig_btn.clicked.connect(partial(core.RunPropRigTool))
        self.mocap_btn.clicked.connect(partial(core.RunMocapMatcher))
        self.folSub_btn.clicked.connect(partial(core.RunFolSubRigTool))
        self.simpleRig_btn.clicked.connect(partial(core.RunBinSimpleRigTool))
        self.HIKsetup_btn.clicked.connect(partial(core.RunHIKsetupTool))
        
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
        
        AVS_layout = QtWidgets.QVBoxLayout()
        AVS_layout.addLayout(fit_layout)
        AVS_layout.addWidget(self.separator1)
        AVS_layout.addLayout(extra_layout)
        AVS_layout.addWidget(self.separator2)
        AVS_layout.addLayout(build_layout)
        
        post_layout = QtWidgets.QHBoxLayout()
        post_layout.addWidget(self.pubCheck_btn)
        post_layout.addWidget(self.Milki_btn)
        
        tool1_lay = QtWidgets.QHBoxLayout()
        tool1_lay.addWidget(self.rename_btn)
        tool1_lay.addWidget(self.colorMaker_btn)
        
        tool2_lay = QtWidgets.QHBoxLayout()
        tool2_lay.addWidget(self.skinHelp_btn)
        tool2_lay.addWidget(self.propRig_btn)
        
        tool_layout = QtWidgets.QVBoxLayout()
        tool_layout.addLayout(tool1_lay)
        tool_layout.addLayout(tool2_lay)
        
        otherTool_con = Container.Main("Other Tools")
        otherTool_layout = QtWidgets.QVBoxLayout()
        otherTool_layout.addWidget(otherTool_con)
        container_lay1 = QtWidgets.QGridLayout(otherTool_con.contentWidget)
        container_lay1.addWidget(self.simpleRig_btn)
        container_lay1.addWidget(self.folSub_btn)
        container_lay1.addWidget(self.HIKsetup_btn)
        container_lay1.addWidget(self.mocap_btn)
        
        # GROUPBOX
        AVS5_gb = QtWidgets.QGroupBox()
        AVS5_gb.setLayout(AVS5_layout)
        
        AVS_gb = QtWidgets.QGroupBox('AVS')
        AVS_gb.setLayout(AVS_layout)
        
        post_gb = QtWidgets.QGroupBox('Pub')
        post_gb.setLayout(post_layout)
        
        tool_gb = QtWidgets.QGroupBox('Rig Tools')
        tool_gb.setLayout(tool_layout)
        
        otherTool_gb = QtWidgets.QGroupBox('')
        otherTool_gb.setLayout(otherTool_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(AVS5_gb)
        main_layout.addWidget(AVS_gb)
        main_layout.addWidget(post_gb)
        main_layout.addWidget(self.separator3)
        main_layout.addWidget(tool_gb)
        main_layout.addWidget(otherTool_gb)
        main_layout.addStretch(1)
        
        return main_layout
    
    
    def GS_Rig_Tab(self):
        
        # SETTING
        size = QtCore.QSize(27,27)
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
        self.prntCnst_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/parentConstraint.png"), iconSize=size, styleSheet="background: rgb(95,90,105);")
        self.pntCnst_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/posConstraint.png"), iconSize=size, styleSheet="background: rgb(95,90,105);")
        self.oriCnst_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/orientConstraint.png"), iconSize=size, styleSheet="background: rgb(95,90,105);")
        self.scaCnst_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/scaleConstraint.png"), iconSize=size, styleSheet="background: rgb(95,90,105);")
        self.connect_btn = QtWidgets.QPushButton("↦", self, font=nfont, styleSheet="background: rgb(175,140,50);")
        self.disconnect_btn = QtWidgets.QPushButton("↛", self, font=nfont, styleSheet="background: rgb(175,170,130);")
        self.lock_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/lockGeneric.png"), iconSize=size, styleSheet="background: rgb(90,110,120);")
        self.unlock_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(":/unlockGeneric.png"), iconSize=size, styleSheet="background: rgb(120,125,130);")
        
        self.osGrp_btn = QtWidgets.QPushButton("OffsetGrp", self)
        self.parent_btn = QtWidgets.QPushButton("Parent", self)
        self.switchFKIK_btn = QtWidgets.QPushButton("Switch FKIK", self)
        self.setCtrlZero_btn = QtWidgets.QPushButton("Ctrl = 0", self)
        
        # self.separator1 = QtWidgets.QFrame(styleSheet="background-color: gray;")
        # self.separator1.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator2 = QtWidgets.QFrame(styleSheet="background-color: gray;", fixedHeight=2)
        self.separator2.setFrameShape(QtWidgets.QFrame.HLine)
        
        # CONNECT
        self.driver_replace_btn.clicked.connect(partial(core.ReplaceItemList, self.driver_list))
        self.driver_remove_btn.clicked.connect(partial(core.RemoveItemList, self.driver_list))
        self.driven_replace_btn.clicked.connect(partial(core.ReplaceItemList, self.driven_list))
        self.driven_remove_btn.clicked.connect(partial(core.RemoveItemList, self.driven_list))
        
        # self.prntCnst_btn.clicked.connect(partial(core.ConstraintCmd2, self.driver_list, self.driven_list, self.maintainOs_cb.checkState(), self.))
        # self.pntCnst_btn.clicked.connect(partial(core.ConstraintCmd2, self.driver_list, self.driven_list))
        # self.oriCnst_btn.clicked.connect(partial(core.ConstraintCmd2, self.driver_list, self.driven_list))
        # self.scaCnst_btn.clicked.connect(partial(core.ConstraintCmd2, self.driver_list, self.driven_list))
        
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
        
        etc_layout = QtWidgets.QHBoxLayout()
        etc_layout.addWidget(self.osGrp_btn)
        etc_layout.addWidget(self.parent_btn)
        etc_layout.addWidget(self.switchFKIK_btn)
        etc_layout.addWidget(self.setCtrlZero_btn)
        
        rigHelp_layout = QtWidgets.QVBoxLayout()
        rigHelp_layout.addLayout(listWidget_layout)
        rigHelp_layout.addWidget(self.separator2)
        rigHelp_layout.addWidget(self.maintainOs_cb)
        rigHelp_layout.addLayout(cnst_layout)
        rigHelp_layout.addLayout(connection_layout)
        rigHelp_layout.addLayout(lock_layout)
        
        # GROUPBOX
        rigHelp_gb = QtWidgets.QGroupBox('')
        rigHelp_gb.setLayout(rigHelp_layout)
        
        rigHelp2_gb = QtWidgets.QGroupBox('')
        rigHelp2_gb.setLayout(etc_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(rigHelp_gb)
        main_layout.addWidget(rigHelp2_gb)
        main_layout.addStretch(1)
        
        return main_layout
    
    
    def GS_Other_Tab(self):
    
        # WIDGET
        self.golaemSet_btn = QtWidgets.QPushButton("Golaem Setting", self)
        self.deformerIssue_btn = QtWidgets.QPushButton("Fix DeformIssue", self) #Fix Deformer Evaluation Inaccuracy
        self.headSquash_btn = QtWidgets.QPushButton("Fix Head Squash", self)
        self.MTX2_btn = QtWidgets.QPushButton("MTX2: import shader", self)
        self.afterMTX_btn = QtWidgets.QPushButton("Import Shader & Generate Preview", self)

        # CONNECT
        self.golaemSet_btn.clicked.connect(partial(golaem.golaemSettingRun))
        self.deformerIssue_btn.clicked.connect(partial(deformerIssue.deformerIssueRun))
        self.headSquash_btn.clicked.connect(partial(core.fixAVSHeadSquash))
        self.MTX2_btn.clicked.connect(partial(core.GS_MTX2))
        self.afterMTX_btn.clicked.connect(partial(core.RunAfterShader))
        
        # LAYOUT
        post_layout = QtWidgets.QVBoxLayout()
        post_layout.addWidget(self.golaemSet_btn)
        post_layout.addWidget(self.deformerIssue_btn)
        post_layout.addWidget(self.headSquash_btn)
        
        check_layout = QtWidgets.QVBoxLayout()
        check_layout.addWidget(self.MTX2_btn)
        check_layout.addWidget(self.afterMTX_btn)
        
        # GROUPBOX
        post_gb = QtWidgets.QGroupBox('Fix')
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

    
    def popupFitSetup(self, position):
        
        self.fitSetup_menu.exec_(self.GSbiped_btn.mapToGlobal(position))
        

    def popupPreRig(self, position):
        
        self.preRig_menu.exec_(self.fitBuild_btn.mapToGlobal(position))
        
    
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
            
            
    def displayPoleVector(self):
        pass
    
            
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



