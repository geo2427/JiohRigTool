# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm
from pymel.core import *

import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import xml.etree.ElementTree as ET
import imp

path = "/gstepasset/WorkLibrary/1.Animation_team/Animator/sangbin/v00_published/"

if not path in sys.path:
    sys.path.append(path)

import AdvancedSkeleton_setup
imp.reload(AdvancedSkeleton_setup)

import adv_flattenLeg
imp.reload(adv_flattenLeg)

import faceCommand
imp.reload(faceCommand)

import variable as var
imp.reload(var)

import ctlCommand as ctlCommand
import bsCommand as bsCommand
imp.reload(ctlCommand)
imp.reload(bsCommand)


##!--------------------------------------------------------------------------------------------------------------------------
# [UI]

def maya_main_win():
    """

    Returns: the Maya main window widget as a Python object

    """
    main_win_ptr = omui.MQtUtil.mainWindow()
    # return wrapInstance(long(main_win_ptr), QtWidgets.QWidget)
    return wrapInstance(main_win_ptr, QtWidgets.QWidget)

class TESTAdvancedSetup_win(QtWidgets.QDialog):
    def __init__(self, parent = maya_main_win()):
        super(TESTAdvancedSetup_win, self).__init__(parent)  # maya main window parent

        self.ui_path = "/gstepasset/WorkLibrary/1.Animation_team/Animator/sangbin/v00_published/advanced_UI_v07.ui"

        # Parent widget under Maya main window
        self.setParent(maya_main_win())
        self.setWindowFlags(Qt.Window)

        # Remove previous window
        # TODO: Delete window without title.
        doc = ET.parse(self.ui_path)
        root = doc.getroot()
        result = {}
        for child in root:
            result[child.tag] = child.attrib
        get_window = result.get('widget').get('name')

        if cmds.window(get_window, exists=True):
            cmds.deleteUI(get_window)

        # ui file load
        ui_loader = QUiLoader()
        ui_file = QFile(self.ui_path)
        ui_file.open(QFile.ReadOnly)

        # create widget from ui file
        self.ui = ui_loader.load(ui_file, parentWidget=self) #--- Parent Widget!!!! ---#
        ui_file.close()

        self.ui.setAttribute(Qt.WA_DeleteOnClose, True)
        self.ui.show()

        # ----------------------------------------------------------------------------------------------

        self.ui.rotate_Btn.clicked.connect(self.rotateSpinShape)
        self.ui.rotate_rollBack_Btn.clicked.connect(self.rotateSpinShape_rollBack)

        self.ui.mirror_Btn.clicked.connect(self.mirror)
        self.ui.mirror_rollBack_Btn.clicked.connect(self.mirrorRollback)

        self.ui.edit_follow_Btn.clicked.connect(self.editFollow)
        self.ui.edit_follow_rollback_Btn.clicked.connect(self.editFollowRollBack)

        # 2023_01_27_ temperally deleted
        # self.ui.edit_leg_follow_Btn.clicked.connect(self.editLegFollow)
        # self.ui.edit_leg_follow_rollback_Btn.clicked.connect(self.editLegFollowRollBack)
        
        self.ui.addWorldCtl_Btn.clicked.connect(self.editWorld)

        self.ui.rollback_Btn.clicked.connect(self.rollBack)

        # if self.ui.DQ_namespace_cbox.isChecked() == True:
        #     self.ui.nonRigid_On_Btn.clicked.connect(self.DQ_nonRigid_ON_cboxChecked)
        #     self.ui.nonRigid_Off_Btn.clicked.connect(self.DQ_nonRigid_OFF_cboxChecked)
        # else:
        #     self.ui.nonRigid_On_Btn.clicked.connect(self.DQ_nonRigid_ON_cboxUnChecked)
        #     self.ui.nonRigid_Off_Btn.clicked.connect(self.DQ_nonRigid_OFF_cboxUnChecked)

        # 2023_01_27_ namespace option temperally deleted
        self.ui.nonRigid_On_Btn.clicked.connect(self.DQ_nonRigid_ON_cboxChecked)
        self.ui.nonRigid_Off_Btn.clicked.connect(self.DQ_nonRigid_OFF_cboxChecked)
            
        self.ui.subCTL_Btn.clicked.connect(self.editSubCTL)
        self.ui.subCTL_rollBack_Btn.clicked.connect(self.editSubCTL_rollBack)
        
        self.ui.transCTL_Btn.clicked.connect(self.editTranseCTL)
        self.ui.transCTL_rollBack_Btn.clicked.connect(self.editTranseCTL_rollBack)
        
        self.ui.allAtOnce_Btn.clicked.connect(self.allAtOnce)
        self.ui.allAtOnce_rollBack_Btn.clicked.connect(self.allAtOnce_rollBack)
                
        ########## Tap 2 #############
        self.ui.legFlatten_Btn.clicked.connect(self.legFlatten)
        self.ui.legFlattenRollBack_Btn.clicked.connect(self.legFlatten_rollBack)
        
        self.ui.legGoToBuildPose_Btn.clicked.connect(self.legGotoBuildPose)
        
        
        ######### Tap 3 ##########
        self.ui.BS_Connect_Btn.clicked.connect(self.bsConnectBtnCommand)
        
        self.ui.headRIG_FIX_head_Btn.clicked.connect(self.headRIGFixBtnCommand_head)
        self.ui.headRIG_FIX_body_Btn.clicked.connect(self.headRIGFixBtnCommand_body)
        
        self.ui.attacher_rig_Head_Btn.clicked.connect(self.attacherRigBtnCommand_head)
        self.ui.attacher_rig_Body_Btn.clicked.connect(self.attacherRigBtnCommand_body)
        
    def rotateSpinShape(self):
        AdvancedSkeleton_setup.rotSpine()

    def rotateSpinShape_rollBack(self):
        AdvancedSkeleton_setup.rotSpine_rollBack()

    def mirror(self):
        # --- mirror ik Controls ---#
        ikCtrl = ('IKArm_R', 'IKLeg_R', 'RollToesEnd_R', 'RollToes_R', 'RollHeel_R', 'FKScapula_L') #20221028 edited - 'FKScapula_L' added, value edited
        AdvancedSkeleton_setup.mirrorSetup(ikCtrl)

    def mirrorRollback(self):
        ikCtrl = ('IKArm_R', 'IKLeg_R', 'RollToesEnd_R', 'RollToes_R', 'RollHeel_R', 'FKScapula_L') #20221028 edited - 'FKScapula_L' added, value edited
        AdvancedSkeleton_setup.rollBack(ikCtrl)

    def editFollow(self):
        main = ('Main')
        ikCtrl = ('IKArm_L', 'IKArm_R')
        AdvancedSkeleton_setup.editFollow(ikCtrl, main)

    def editFollowRollBack(self):
        ikCtrl = ('IKArm_L', 'IKArm_R')
        AdvancedSkeleton_setup.editFollowRollBack(ikCtrl)

    def editLegFollow(self):
        AdvancedSkeleton_setup.editLegFollow()
    
    def editLegFollowRollBack(self):
        AdvancedSkeleton_setup.editLegFollowRollBack()

    def editWorld(self):
        main = ('Main')
        world = ('World')
        AdvancedSkeleton_setup.editAfterBuild(main, world)

    def rollBack(self):
        main = ('Main')
        world = ('World')
        AdvancedSkeleton_setup.rollbackEdit(main, world)

    def DQ_nonRigid_ON_cboxChecked(self):
        AdvancedSkeleton_setup.DQ_nonRigid_ON(ref=True)

    def DQ_nonRigid_ON_cboxUnChecked(self):
        AdvancedSkeleton_setup.DQ_nonRigid_ON(ref=False)

    def DQ_nonRigid_OFF_cboxChecked(self):
        AdvancedSkeleton_setup.DQ_nonRigid_OFF(ref=True)

    def DQ_nonRigid_OFF_cboxUnChecked(self):
        AdvancedSkeleton_setup.DQ_nonRigid_OFF(ref=False)
    
    def editSubCTL(self):
        AdvancedSkeleton_setup.editSubCTL()
    
    def editSubCTL_rollBack(self):
        AdvancedSkeleton_setup.editSubCTL_rollBack()
    
    def editTranseCTL(self):
        AdvancedSkeleton_setup.makeIkTransCTL()
    
    def editTranseCTL_rollBack(self):
        AdvancedSkeleton_setup.makeIkTransCTL_rollBack()
    
    #20221031_added
    def allAtOnce(self):
        AdvancedSkeleton_setup.rotSpine()
        
        ikCtrl = ('IKArm_R', 'IKLeg_R', 'RollToesEnd_R', 'RollToes_R', 'RollHeel_R', 'FKScapula_L')
        AdvancedSkeleton_setup.mirrorSetup(ikCtrl)
        
        main = ('Main')
        world = ('World')
        AdvancedSkeleton_setup.editAfterBuild(main, world)
        
        main = ('Main')
        ikArm = ('IKArm_L', 'IKArm_R')
        AdvancedSkeleton_setup.editFollow(ikArm, main)
        
        # AdvancedSkeleton_setup.editLegFollow()
        
        AdvancedSkeleton_setup.DQ_nonRigid_ON(ref=True)
        
        AdvancedSkeleton_setup.editSubCTL()
        
        AdvancedSkeleton_setup.makeIkTransCTL()
        
    def allAtOnce_rollBack(self):
        AdvancedSkeleton_setup.makeIkTransCTL_rollBack()
        
        AdvancedSkeleton_setup.editSubCTL_rollBack()
        
        # AdvancedSkeleton_setup.editLegFollowRollBack()
        
        ikArm = ('IKArm_L', 'IKArm_R')
        AdvancedSkeleton_setup.editFollowRollBack(ikArm)
        
        ikCtrl = ('IKArm_R', 'IKLeg_R', 'RollToesEnd_R', 'RollToes_R', 'RollHeel_R', 'FKScapula_L')
        AdvancedSkeleton_setup.rollBack(ikCtrl)
        
        main = ('Main')
        world = ('World')
        AdvancedSkeleton_setup.rollbackEdit(main, world)
                
        AdvancedSkeleton_setup.rotSpine_rollBack()
        
    def legFlatten(self):
        adv_flattenLeg.legFlatten()
    
    def legFlatten_rollBack(self):
        adv_flattenLeg.legFlattenRollback()
    
    def legGotoBuildPose(self):
        adv_flattenLeg.legGoToBuildPose()
        
    #############################################################################
    def bsConnectBtnCommand(self):
        # Main Script 0 #
        AS_MESH, AS_BS, MOD_MESH, MOD_BS, matching_DICT = faceCommand.defineVariable()

        # Main Script 1 # connect to ctrlBox Controller#
        for ctl, attrs in var.userdefine_attr_dict.items():
            faceCommand.connectBStoCtl(MOD_MESH, ctl, attrs)

        # Main Script 2 # connect selected AS_mesh's blendshape to SDK
        faceCommand.connectBStoFacialCtl(AS_MESH,AS_BS,MOD_MESH,MOD_BS,matching_DICT)

        # Main Script 4 # make MOD_MESH as a target to AS_MESH and auto set 1
        faceCommand.MODtoAS_autoTarget(AS_MESH,AS_BS,matching_DICT)

    def headRIGFixBtnCommand_head(self):
        # Main Script # 3 controller Cleaning r/s/v lock and delete Emotions and visCtrl
        faceCommand.controllerCleaning(head=True, body=False)
        # Main Script 5 # fix EyeCTL for Animator
        faceCommand.eyeFix(head=True, body=False)
    
    def headRIGFixBtnCommand_body(self):
        # Main Script # 3 controller Cleaning r/s/v lock and delete Emotions and visCtrl
        faceCommand.controllerCleaning(head=False, body=True)
        # Main Script 5 # fix EyeCTL for Animator
        faceCommand.eyeFix(head=False, body=True)
        # if body == True: 추가작업 자동화 필요
        if objExists("headRIG_Head_M"):
            headRIG_head = PyNode("headRIG_Head_M")
            body_head = PyNode("Head_M")
            parentConstraint(body_head, headRIG_head, mo=0)
            body_head.s>>headRIG_head.s
            connectAttr("MainScaleMultiplyDivide.output", "MainAndHeadScaleMultiplyDivide.input1")
            
    #rotation피봇을 위한 orientConstriant 추가필요
    def attacherRigBtnCommand_head(self):
        # Main Script 6 # ctrl_attacher 
        le = self.ui.attacher_rig_lineEdit.text()
        faceCommand.attacher_rig(name=le ,head=True)
        
    def attacherRigBtnCommand_body(self):
        # Main Script 6 # ctrl_attacher 
        le = self.ui.attacher_rig_lineEdit.text()
        faceCommand.attacher_rig(name=le ,head=False)
        