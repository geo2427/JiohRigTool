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
imp.reload(core)
imp.reload(crtv)
imp.reload(deformerIssue)


class GSRigUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    TITLE = 'GSRigTool'
    VERSION  = '230424'
    # ICON = '/home/jioh.kim/Desktop/pipe/wip/A/GSRigTool/util/resources/GSLogo.png'

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        self.setWindowTitle("{}_v{}".format(self.TITLE, self.VERSION))
        # self.setWindowIcon(QtGui.QIcon(self.ICON))
        self.setGeometry(2400,500,370,400)
        self.setMinimumWidth(350)
        
        # TAB
        pre_tab = QtWidgets.QWidget()
        pre_tab.setLayout(self.create_pre_tab())
        
        rigging_tab = QtWidgets.QWidget()
        rigging_tab.setLayout(self.create_rigging_tab())
        
        post_tab = QtWidgets.QWidget()
        post_tab.setLayout(self.create_post_tab())
        
        main_tab = QtWidgets.QTabWidget()
        main_tab.addTab(pre_tab, 'Pre')
        main_tab.addTab(rigging_tab, 'Rig')
        main_tab.addTab(post_tab, 'Post')

        # WINDOW
        main_win = QtWidgets.QVBoxLayout()
        main_win.addWidget(main_tab)
        
        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_win)
        self.setCentralWidget(widget)
    
    
    def create_pre_tab(self):
        
        # WIDGET
        self.AVS5_btn = QtWidgets.QPushButton("Run `AdvancedSkeleton9Fix`", self, fixedHeight=40, styleSheet="background: rgb(120,100,110);")
        self.biped_btn = QtWidgets.QPushButton("Import `biped.ma`", self)
        self.fitSetup_btn = QtWidgets.QPushButton("Fit Setup", self)
        self.autoOrient_btn = QtWidgets.QPushButton("Auto-Orient", self)
        self.jointAxis_cb = QtWidgets.QCheckBox("joint-axis", self)
        self.poleVector_cb = QtWidgets.QCheckBox("pole-vector(미완)", self)
        self.crtvGuide_btn = QtWidgets.QPushButton("Corrective Guides", self) # minimumWidth=163.5
        # self.crtvGuide_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, singleStep=1, minimum=1, maximum=100, value=30) # fixedWidth = 163
        self.crtvGuideDel_btn = QtWidgets.QPushButton("Delete", self, maximumWidth=100)
        self.asymmetry_btn = QtWidgets.QPushButton("Asymmetry", self)
        self.asymmetryDel_btn = QtWidgets.QPushButton("Delete", self, maximumWidth=100)
        self.fitBuild_btn = QtWidgets.QPushButton("Build AdvancedSkeleton", self, fixedHeight=40, styleSheet="background: rgb(130,90,100);")
        self.fitToggle_btn = QtWidgets.QPushButton("Toggle Fit", self)
        self.fitReBuild_btn = QtWidgets.QPushButton("ReBuild", self)
        self.preRigAll_cb = QtWidgets.QCheckBox("All", self, checked=1)
        self.preHier_cb = QtWidgets.QCheckBox("Milki Hierarchy", self, visible=False)
        self.preIKSub_cb = QtWidgets.QCheckBox("IKSubArm", self, visible=False)
        self.preOnoff_cb = QtWidgets.QCheckBox("OnoffCtrl", self, visible=False)
        self.editMain_cb = QtWidgets.QCheckBox("Edit MainCtrl Name", self, visible=False)
        self.preRig_btn = QtWidgets.QPushButton("Pre Rig", self)

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

        # LAYOUT
        AVS5_layout = QtWidgets.QVBoxLayout()
        # AVS5_layout.setAlignment(QtCore.Qt.AlignCenter)
        AVS5_layout.addWidget(self.AVS5_btn)

        display_layout = QtWidgets.QHBoxLayout()
        display_layout.addWidget(self.jointAxis_cb)
        display_layout.addWidget(self.poleVector_cb)

        fit_layout = QtWidgets.QVBoxLayout()
        fit_layout.addWidget(self.biped_btn)
        fit_layout.addWidget(self.fitSetup_btn)
        fit_layout.addWidget(self.autoOrient_btn)
        fit_layout.addLayout(display_layout)
        
        asym_layout = QtWidgets.QHBoxLayout()
        asym_layout.addWidget(self.asymmetry_btn)
        asym_layout.addWidget(self.asymmetryDel_btn)
                
        crtv_layout = QtWidgets.QHBoxLayout()
        crtv_layout.addWidget(self.crtvGuide_btn)
        crtv_layout.addWidget(self.crtvGuideDel_btn)
        # crtv_layout.addWidget(self.crtvGuide_slider)
        
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
        
        pre_layout = QtWidgets.QHBoxLayout()
        pre_layout.addLayout(self.preSec_layout)
        pre_layout.addWidget(self.preRig_btn)
        
        # GROUPBOX
        AVS5_gb = QtWidgets.QGroupBox()
        AVS5_gb.setLayout(AVS5_layout)
        
        fit_gb = QtWidgets.QGroupBox('Fit Setup')
        fit_gb.setLayout(fit_layout)
        
        extra_gb = QtWidgets.QGroupBox('Extra Setup')
        extra_gb.setLayout(extra_layout)
        
        build_gb = QtWidgets.QGroupBox()
        build_gb.setLayout(build_layout)
        
        pre_gb = QtWidgets.QGroupBox('Pre Rig')
        pre_gb.setLayout(pre_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(AVS5_gb)
        main_layout.addWidget(fit_gb)
        main_layout.addWidget(extra_gb)
        main_layout.addWidget(build_gb)
        main_layout.addWidget(pre_gb)
        main_layout.addStretch(1)
        
        return main_layout
    
    
    def create_rigging_tab(self):
        
        # WIDGET
        self.driver_label = QtWidgets.QLabel("[    driver    ]", self, alignment=QtCore.Qt.AlignCenter)
        self.driver_list = QtWidgets.QListWidget(self, minimumHeight=200, minimumWidth=160)
        self.driver_add_btn = QtWidgets.QPushButton("Add", self)
        self.driver_remove_btn = QtWidgets.QPushButton("Remove", self)
        self.to_label = QtWidgets.QLabel(">>", self)
        self.driven_label = QtWidgets.QLabel("[    driven    ]", self, alignment=QtCore.Qt.AlignCenter)
        self.driven_list = QtWidgets.QListWidget(self, minimumHeight=200, minimumWidth=160)
        self.driven_add_btn = QtWidgets.QPushButton("Add", self)
        self.driven_remove_btn = QtWidgets.QPushButton("Remove", self)
        
        # self.maintainOs_btn = QtWidgets.QCheckBox("MaintainOffset", self)
        self.prntCnst_btn = QtWidgets.QPushButton("Parent", self)
        self.pntCnst_btn = QtWidgets.QPushButton("Point", self)
        self.oriCnst_btn = QtWidgets.QPushButton("Orient", self)
        self.scaCnst_btn = QtWidgets.QPushButton("Scale", self)
        self.connect_btn = QtWidgets.QPushButton("Connect", self)
        self.disconnect_btn = QtWidgets.QPushButton("disConnect", self)
        self.lock_btn = QtWidgets.QPushButton("Lock", self)
        self.unlock_btn = QtWidgets.QPushButton("UnLock", self)
        self.osGrp_btn = QtWidgets.QPushButton("OffsetGrp", self)
        self.parent_btn = QtWidgets.QPushButton("Parent", self)
        
        # self.color_pal = QtGui.QDialog
        
        self.separator1 = QtWidgets.QFrame(styleSheet="background-color: gray;")
        self.separator1.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator2 = QtWidgets.QFrame(styleSheet="background-color: gray;")
        self.separator2.setFrameShape(QtWidgets.QFrame.HLine)
        
        self.rename_btn = QtWidgets.QPushButton("Rename Tool", self)
        self.colorMaker_btn = QtWidgets.QPushButton("Color Maker", self)
        self.skinHelp_btn = QtWidgets.QPushButton("Skin Help Tool", self)
        self.folSub_btn = QtWidgets.QPushButton("FolSubRig Tool", self)
        self.simpleRig_btn = QtWidgets.QPushButton("Bin Simple Rig Tool", self)
        self.HIKsetup_btn = QtWidgets.QPushButton("HIKsetup Tool", self)
        
        # CONNECT
        self.osGrp_btn.clicked.connect(partial(core.makeOffsetGrp))

        self.rename_btn.clicked.connect(self.RunRenameTool)
        self.colorMaker_btn.clicked.connect(self.RunColorTool)
        self.skinHelp_btn.clicked.connect(self.skinHelpTool)
        self.folSub_btn.clicked.connect(self.RunFolSubRigTool)
        self.simpleRig_btn.clicked.connect(self.RunBinSimpleRigTool)
        self.HIKsetup_btn.clicked.connect(self.RunHIKsetupTool)
        
        # LAYOUT
        driverAdd_layout = QtWidgets.QHBoxLayout()
        driverAdd_layout.addWidget(self.driver_add_btn)
        driverAdd_layout.addWidget(self.driver_remove_btn)
        
        driver_layout = QtWidgets.QVBoxLayout()
        driver_layout.addWidget(self.driver_label)
        driver_layout.addWidget(self.driver_list)
        driver_layout.addLayout(driverAdd_layout)
        
        drivenAdd_layout = QtWidgets.QHBoxLayout()
        drivenAdd_layout.addWidget(self.driven_add_btn)
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
        
        etc_layout = QtWidgets.QHBoxLayout() # alignment=QtCore.Qt.AlignCenter
        etc_layout.addWidget(self.lock_btn)
        etc_layout.addWidget(self.unlock_btn)
        etc_layout.addWidget(self.osGrp_btn)
        etc_layout.addWidget(self.parent_btn)
        
        rigHelp_layout = QtWidgets.QVBoxLayout()
        rigHelp_layout.addLayout(listWidget_layout)
        rigHelp_layout.addWidget(self.separator1)
        rigHelp_layout.addLayout(cnst_layout)
        rigHelp_layout.addLayout(connection_layout)
        rigHelp_layout.addWidget(self.separator2)
        rigHelp_layout.addLayout(etc_layout)
        
        rigHelpTool_layout = QtWidgets.QVBoxLayout()
        rigHelpTool_layout.addWidget(self.rename_btn)
        rigHelpTool_layout.addWidget(self.skinHelp_btn)
        rigHelpTool_layout.addWidget(self.colorMaker_btn)
        
        rigSub_layout = QtWidgets.QVBoxLayout()
        rigSub_layout.addWidget(self.simpleRig_btn)
        rigSub_layout.addWidget(self.folSub_btn)

        otherTool_layout = QtWidgets.QVBoxLayout()
        otherTool_layout.addWidget(self.HIKsetup_btn)
        
        # GROUPBOX
        rigHelp_gb = QtWidgets.QGroupBox('Rig Help')
        rigHelp_gb.setLayout(rigHelp_layout)
        
        rigHelpTool_gb = QtWidgets.QGroupBox('Rig Tools')
        rigHelpTool_gb.setLayout(rigHelpTool_layout)
        
        rigSub_gb = QtWidgets.QGroupBox('Sub / Prop')
        rigSub_gb.setLayout(rigSub_layout)
        
        otherTool_gb = QtWidgets.QGroupBox('Others')
        otherTool_gb.setLayout(otherTool_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(rigHelp_gb)
        main_layout.addWidget(rigHelpTool_gb)
        main_layout.addWidget(rigSub_gb)
        main_layout.addWidget(otherTool_gb)
        main_layout.addStretch(1)
        
        return main_layout
            
    
    def create_post_tab(self):
    
        # WIDGET
        self.deformerIssue_btn = QtWidgets.QPushButton("Fix Deformer Evaluation Inaccuracy", self)
        self.headSquash_btn = QtWidgets.QPushButton("Fix Head Squash", self)
        self.pubCheck_btn = QtWidgets.QPushButton("Pub Check", self)
        self.MTX2_btn = QtWidgets.QPushButton("MTX2: import shader", self)
        self.afterMTX_btn = QtWidgets.QPushButton("Import Shader & Generate Preview", self)

        # CONNECT        
        self.deformerIssue_btn.clicked.connect(partial(deformerIssue.deformerIssueRun))
        self.headSquash_btn.clicked.connect(partial(core.fixAVSHeadSquash))
        self.pubCheck_btn.clicked.connect(partial(core.pubCheck))
        self.MTX2_btn.clicked.connect(partial(core.GS_MTX2))
        self.afterMTX_btn.clicked.connect(partial(core.RunAfterShader))
        
        # LAYOUT
        post_layout = QtWidgets.QVBoxLayout()
        post_layout.addWidget(self.deformerIssue_btn)
        post_layout.addWidget(self.headSquash_btn)
        
        check_layout = QtWidgets.QVBoxLayout()
        check_layout.addWidget(self.pubCheck_btn)
        check_layout.addWidget(self.MTX2_btn)
        check_layout.addWidget(self.afterMTX_btn)
        
        # GROUPBOX
        post_gb = QtWidgets.QGroupBox('Post Rig')
        post_gb.setLayout(post_layout)
        
        check_gb = QtWidgets.QGroupBox('Pub Check')
        check_gb.setLayout(check_layout)
        
        # FINAL
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(post_gb)
        main_layout.addWidget(check_gb)
        main_layout.addStretch(1)
        
        return main_layout

    
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
            self.editMain_cb.setVisible(0)

        else:
            self.preHier_cb.setChecked(1)
            self.preIKSub_cb.setChecked(1)
            self.preOnoff_cb.setChecked(1)
            self.editMain_cb.setChecked(1)
            
            self.preHier_cb.setVisible(1)
            self.preIKSub_cb.setVisible(1)
            self.preOnoff_cb.setVisible(1)
            self.editMain_cb.setVisible(1)
    
            
    def crtvSlider(self, var):
        val = self.crtvGuide_slider.value()
        realVal = float(val) / 10
        print(realVal)
        return realVal
    
    
    def crtvSlider_2(self):
        # self.crtvSlider(var)
        pass
    
    
    def preRigRun(self):
        
        print("\n[ Pre-RIG ]")
        
        if self.preRigAll_cb.isChecked():
            with pm.UndoChunk():
                core.milkiHierarchy()
                core.addIKSubArm()
                core.createOnOffCtrl()
                core.editMainName()
        
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
                    
            if self.editMain_cb():
                core.editMainName()
              
    
    def colorPalette(self):
        for i in range(1, 32):
            r, g, b = pm.colorIndex(i, q=1)
            pm.canvas(rgbValue=(r, g, b), w=20, h=20) # , pc=partial(core.SetColor, i)
    
    # QtGui.QPalette()
            
                        
    ##########################################################################################
    
    
    def RunRenameTool(self):
        
        rename_path = 'source "/home/jioh.kim/Desktop/pipe/wip/A/GSRigTool/util/modules/Quick_rename_tool.mel"'
        mel.eval(rename_path)
        mel.eval("Quick_rename_tool")

    
    def RunFolSubRigTool(self):
        
        from util.modules import folSubRigTool as fol
        fol.MainUI()
        
    
    def JHRigTool(self):
        
        from util.modules.JHTool import JHRun
        JHRun.JH_edit_run()
        
    
    def RunHIKsetupTool(self):
        
        from util.modules.HIKsetupTool import HIK_Run
        HIK_Run.HIK_Tool_run()
        
    
    def RunBinSimpleRigTool(self):
        
        from util.modules import simpleRigTool
        imp.reload(simpleRigTool)
        simpleRigTool.winshow()
        
        
    def RunBinSkinTool(self):
        
        from util.modules import skinningTool
        imp.reload(skinningTool)
        skinningTool.winshow()
        

    def RunCtrlCtl(self):
        
        path = 'source "/home/jioh.kim/Desktop/pipe/wip/A/GSRigTool/util/modules/ctrlctl.mel"'
        mel.eval(path)
        
    
    def skinHelpTool(self):
        
        from util.modules.skinHelpTool import skinHelpTool_Run as run
        imp.reload(run)
        run.skinHelpTool_Run()


    def RunColorTool(self):
        
        path = 'source "/home/jioh.kim/Desktop/pipe/wip/A/GSRigTool/util/modules/ColorMarker_v3_01/ColorMarker_v3_01.mel"'
        mel.eval(path)
    
    
# if __name__ == '__main__':
#     win = GSRigUI()
#     win.show(dockable=True, floating=False, area='right')

