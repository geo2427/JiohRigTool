#HIK Setting Script
# coding:utf-8
import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm
import pymel.core as core
import json
from functools import partial



def getTextField(textFieldName):
    getText = pm.textFieldGrp(textFieldName, q=True, tx=True)
    return getText

#Definition 생성 
def CreateHIK(CHNameField, x):
    ChName = getTextField(CHNameField)
    print ChName
    mel.eval('hikCreateCharacter("%s")'%str(ChName))
    
def SetTpose(x):
    #Tpose 만들기
    leg_getAttrList = {'Hip_L' : ['IKLeg_L', 'PoleLeg_L'],
                       'Hip_R' : ['IKLeg_R', 'PoleLeg_R']}
                       
    arm_getAttrList = {'Scapula_L' : ['FKScapula_L', 'FKShoulder_L', 'FKElbow_L','FKWrist_L'],
                       'Scapula_R' : ['FKScapula_R', 'FKShoulder_R', 'FKElbow_R','FKWrist_R']}
    
    finger_getAttrList = {'IndexFinger1_L' : ['FKIndexFinger1_L', 'FKIndexFinger2_L', 'FKIndexFinger3_L'],
                          'MiddleFinger1_L' : ['FKMiddleFinger1_L', 'FKMiddleFinger2_L', 'FKMiddleFinger3_L'],
                          'RingFinger1_L' :['FKRingFinger1_L', 'FKRingFinger2_L', 'FKRingFinger3_L'],
                          'PinkyFinger1_L' : ['FKPinkyFinger1_L', 'FKPinkyFinger2_L', 'FKPinkyFinger3_L'],
                          'IndexFinger1_R' : ['FKIndexFinger1_R', 'FKIndexFinger2_R', 'FKIndexFinger3_R'],
                          'MiddleFinger1_R' : ['FKMiddleFinger1_R', 'FKMiddleFinger2_R', 'FKMiddleFinger3_R'],
                          'RingFinger1_R' :['FKRingFinger1_R', 'FKRingFinger2_R', 'FKRingFinger3_R'],
                          'PinkyFinger1_R' : ['FKPinkyFinger1_R', 'FKPinkyFinger2_R', 'FKPinkyFinger3_R']}
    
    leg_getAttrDict = {'Hip_L' : {'IKLeg_L':[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0,-1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    'PoleLeg_L':[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0,-1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0]}, 
                       'Hip_R' : {'IKLeg_R':[0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    'PoleLeg_R':[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0,-1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0]}
                       }
                                
                    
    arm_getAttrDict = {'Scapula_L' : {'FKScapula_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKShoulder_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKElbow_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKWrist_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                        }, 
                                        
                       'Scapula_R' : {'FKScapula_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKShoulder_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKElbow_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKWrist_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0]},
                       }
    
    finger_getAttrDict = {'IndexFinger1_L' : {'FKIndexFinger1_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                              'FKIndexFinger2_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                              'FKIndexFinger3_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                        }, 
                          'MiddleFinger1_L' : {'FKMiddleFinger1_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                               'FKMiddleFinger2_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                               'FKMiddleFinger3_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                        }, 
                          'RingFinger1_L' : {'FKRingFinger1_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                             'FKRingFinger2_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                             'FKRingFinger3_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                        }, 
                          'PinkyFinger1_L' : {'FKPinkyFinger1_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                              'FKPinkyFinger2_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                              'FKPinkyFinger3_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                        }, 
    
                          'IndexFinger1_R' : {'FKIndexFinger1_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                              'FKIndexFinger2_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                              'FKIndexFinger3_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                        }, 
                          'MiddleFinger1_R' : {'FKMiddleFinger1_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                               'FKMiddleFinger2_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                               'FKMiddleFinger3_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                        }, 
                          'RingFinger1_R' : {'FKRingFinger1_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                             'FKRingFinger2_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                             'FKRingFinger3_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                        }, 
                          'PinkyFinger1_R' : {'FKPinkyFinger1_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                              'FKPinkyFinger2_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                              'FKPinkyFinger3_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                        }, 
                         }
    
    thumb_getAttrDict = {'FKThumbFinger2_L' : 'FKThumbFinger3_L',
                         'FKThumbFinger2_R' : 'FKThumbFinger3_R'}
    
    for i in leg_getAttrDict.items(): 
        j_getMat = cmds.xform(i[0], q=True ,m=True , ws=True)
        for x in leg_getAttrList[i[0]]:       
            ctr_getMat = cmds.xform(x, q=True ,m=True , ws=True)
            i[1][x][12] = j_getMat[12]
            i[1][x][13] = ctr_getMat[13]
            i[1][x][14] = ctr_getMat[14]
            cmds.xform(x, m=i[1][x] , ws=True)
            
    for i in arm_getAttrDict.items(): 
        j_getMat = cmds.xform(i[0], q=True ,m=True , ws=True)
        for x in arm_getAttrList[i[0]]:       
            ctr_getMat = cmds.xform(x, q=True ,m=True , ws=True)
            i[1][x][12] = ctr_getMat[12]
            i[1][x][13] = ctr_getMat[13]
            i[1][x][14] = ctr_getMat[14]
            cmds.xform(x, m=i[1][x] , ws=True)
    
    for i in finger_getAttrDict.items(): 
        j_getMat = cmds.xform(i[0], q=True ,m=True , ws=True)
        for x in finger_getAttrList[i[0]]:       
            ctr_getMat = cmds.xform(x, q=True ,m=True , ws=True)
            i[1][x][12] = ctr_getMat[12]
            i[1][x][13] = ctr_getMat[13]
            i[1][x][14] = ctr_getMat[14]
            cmds.xform(x, m=i[1][x] , ws=True)
    
    for i in thumb_getAttrDict.items(): 
        j_getMat = cmds.xform(i[0], q=True ,m=True , ws=True)
        ctr_getMat = cmds.xform(i[1], q=True ,m=True , ws=True)
        cmds.xform(i[1], m=[j_getMat[0], j_getMat[1], j_getMat[2], ctr_getMat[3], j_getMat[4], j_getMat[5], j_getMat[6], ctr_getMat[7], j_getMat[8], j_getMat[9], j_getMat[10], ctr_getMat[11], ctr_getMat[12], ctr_getMat[13], ctr_getMat[14], ctr_getMat[15]] , ws=True)


def CheckCtrl(x):
    #SDK 그룹 네이밍 변경
    pm.select('SDKFK**Finger**')
    SDKGrpList = pm.ls(sl=1)
    
    for Gp in SDKGrpList:
        if Gp.nodeType() == 'transform':
            GpName = Gp.split('_')
            if  GpName[-1] == 'L':
                pm.rename(Gp.name(), GpName[0]+'_Right')
            else:
                pm.rename(Gp.name(), GpName[0]+'_Right')
        else:
            print Gp
    
    
    #ADVRig Root 락풀기
    Attrlist = ['sx', 'sy', 'sz']
    for att in Attrlist:
        pm.setAttr('RootX_M'+'.'+att, lock=0)
        pm.setAttr('RootX_M'+'.'+att, channelBox=1)
        pm.setAttr('RootX_M'+'.'+att, keyable=1)
    
    pm.select('Main')
    


def LoadCostomHIK(x):
    mel.eval('hikNameMatching()')
    
    
def LockHIK(x):
    mel.eval('hikToggleLockDefinition()')
    
def CreateADVSet(x):
    Control_Set = ['Main',
     'RootExtraX_M',
     'RootX_M',
     'FKExtraToes_R',
     'FKToes_R',
     'FKExtraAnkle_R',
     'FKAnkle_R',
     'FKExtraKnee_R',
     'FKKnee_R',
     'FKExtraHip_R',
     'FKHip_R',
     'FKExtraHead_M',
     'FKHead_M',
     'FKExtraNeck_M',
     'FKNeck_M',
     'FKExtraMiddleFinger3_R',
     'FKMiddleFinger3_R',
     'FKExtraMiddleFinger2_R',
     'FKMiddleFinger2_R',
     'FKExtraMiddleFinger1_R',
     'FKMiddleFinger1_R',
     'FKExtraMiddleFinger0_R',
     'FKMiddleFinger0_R',
     'FKExtraIndexFinger3_R',
     'FKIndexFinger3_R',
     'FKExtraIndexFinger2_R',
     'FKIndexFinger2_R',
     'FKExtraIndexFinger1_R',
     'FKIndexFinger1_R',
     'FKExtraIndexFinger0_R',
     'FKIndexFinger0_R',
     'FKExtraThumbFinger3_R',
     'FKThumbFinger3_R',
     'FKExtraThumbFinger2_R',
     'FKThumbFinger2_R',
     'FKExtraThumbFinger1_R',
     'FKThumbFinger1_R',
     'FKExtraRingFinger3_R',
     'FKRingFinger3_R',
     'FKExtraRingFinger2_R',
     'FKRingFinger2_R',
     'FKExtraRingFinger1_R',
     'FKRingFinger1_R',
     'FKExtraRingFinger0_R',
     'FKRingFinger0_R',
     'FKExtraPinkyFinger3_R',
     'FKPinkyFinger3_R',
     'FKExtraPinkyFinger2_R',
     'FKPinkyFinger2_R',
     'FKExtraPinkyFinger1_R',
     'FKPinkyFinger1_R',
     'FKExtraPinkyFinger0_R',
     'FKPinkyFinger0_R',
     'FKExtraWrist_R',
     'FKWrist_R',
     'FKExtraElbow_R',
     'FKElbow_R',
     'FKExtraShoulder_R',
     'FKShoulder_R',
     'FKExtraScapula_R',
     'FKScapula_R',
     'FKExtraChest_M',
     'FKChest_M',
     'FKExtraSpine4_M',
     'FKSpine4_M',
     'FKExtraSpine3_M',
     'FKSpine3_M',
     'FKExtraSpine2_M',
     'FKSpine2_M',
     'FKExtraSpine1_M',
     'FKSpine1_M',
     'FKExtraRoot_M',
     'FKRoot_M',
     'FKExtraToes_L',
     'FKToes_L',
     'FKExtraAnkle_L',
     'FKAnkle_L',
     'FKExtraKnee_L',
     'FKKnee_L',
     'FKExtraHip_L',
     'FKHip_L',
     'FKExtraMiddleFinger3_L',
     'FKMiddleFinger3_L',
     'FKExtraMiddleFinger2_L',
     'FKMiddleFinger2_L',
     'FKExtraMiddleFinger1_L',
     'FKMiddleFinger1_L',
     'FKExtraMiddleFinger0_L',
     'FKMiddleFinger0_L',
     'FKExtraIndexFinger3_L',
     'FKIndexFinger3_L',
     'FKExtraIndexFinger2_L',
     'FKIndexFinger2_L',
     'FKExtraIndexFinger1_L',
     'FKIndexFinger1_L',
     'FKExtraIndexFinger0_L',
     'FKIndexFinger0_L',
     'FKExtraThumbFinger3_L',
     'FKThumbFinger3_L',
     'FKExtraThumbFinger2_L',
     'FKThumbFinger2_L',
     'FKExtraThumbFinger1_L',
     'FKThumbFinger1_L',
     'FKExtraRingFinger3_L',
     'FKRingFinger3_L',
     'FKExtraRingFinger2_L',
     'FKRingFinger2_L',
     'FKExtraRingFinger1_L',
     'FKRingFinger1_L',
     'FKExtraRingFinger0_L',
     'FKRingFinger0_L',
     'FKExtraPinkyFinger3_L',
     'FKPinkyFinger3_L',
     'FKExtraPinkyFinger2_L',
     'FKPinkyFinger2_L',
     'FKExtraPinkyFinger1_L',
     'FKPinkyFinger1_L',
     'FKExtraPinkyFinger0_L',
     'FKPinkyFinger0_L',
     'FKExtraWrist_L',
     'FKWrist_L',
     'FKExtraElbow_L',
     'FKElbow_L',
     'FKExtraShoulder_L',
     'FKShoulder_L',
     'FKExtraScapula_L',
     'FKScapula_L',
     'IKExtraLeg_R',
     'IKLeg_R',
     'PoleExtraLeg_R',
     'PoleLeg_R',
     'IKExtraArm_R',
     'IKArm_R',
     'PoleExtraArm_R',
     'PoleArm_R',
     'IKExtracvSpine1_M',
     'IKcvSpine1_M',
     'IKExtracvSpine2_M',
     'IKcvSpine2_M',
     'IKExtracvSpine3_M',
     'IKcvSpine3_M',
     'IKExtracvSpine4_M',
     'IKcvSpine4_M',
     'IKExtraSpine1_M',
     'IKSpine1_M',
     'IKExtraSpine2_M',
     'IKSpine2_M',
     'IKExtraSpine3_M',
     'IKSpine3_M',
     'IKhybridExtraSpine1_M',
     'IKhybridSpine1_M',
     'IKhybridExtraSpine2_M',
     'IKhybridSpine2_M',
     'IKhybridExtraSpine3_M',
     'IKhybridSpine3_M',
     'IKExtraLeg_L',
     'IKLeg_L',
     'PoleExtraLeg_L',
     'PoleLeg_L',
     'IKExtraArm_L',
     'IKArm_L',
     'PoleExtraArm_L',
     'PoleArm_L',
     'FKIKLeg_R',
     'FKIKArm_R',
     'FKIKSpine_M',
     'FKIKLeg_L',
     'FKIKArm_L',
     'RollExtraToes_R',
     'RollToes_R',
     'RollExtraToesEnd_R',
     'RollToesEnd_R',
     'RollExtraHeel_R',
     'RollHeel_R',
     'IKExtraToes_R',
     'IKToes_R',
     'RollExtraToes_L',
     'RollToes_L',
     'RollExtraToesEnd_L',
     'RollToesEnd_L',
     'RollExtraHeel_L',
     'RollHeel_L',
     'IKExtraToes_L',
     'IKToes_L',
     'HipSwinger_M',
     'Fingers_R',
     'Fingers_L']
     
     
    Deformer_Set = ['Toes_R',
     'Ankle_R',
     'Knee_R',
     'Hip_R',
     'HipPart1_R',
     'HipPart2_R',
     'Head_M',
     'NeckPart2_M',
     'NeckPart1_M',
     'Neck_M',
     'MiddleFinger3_R',
     'MiddleFinger2_R',
     'MiddleFinger1_R',
     'MiddleFinger0_R',
     'IndexFinger3_R',
     'IndexFinger2_R',
     'IndexFinger1_R',
     'IndexFinger0_R',
     'ThumbFinger3_R',
     'ThumbFinger2_R',
     'ThumbFinger1_R',
     'RingFinger3_R',
     'RingFinger2_R',
     'RingFinger1_R',
     'RingFinger0_R',
     'PinkyFinger3_R',
     'PinkyFinger2_R',
     'PinkyFinger1_R',
     'PinkyFinger0_R',
     'Wrist_R',
     'Elbow_R',
     'ElbowPart1_R',
     'ElbowPart2_R',
     'Shoulder_R',
     'ShoulderPart1_R',
     'ShoulderPart2_R',
     'Scapula_R',
     'Chest_M',
     'Spine4_M',
     'Spine3_M',
     'Spine2_M',
     'Spine1_M',
     'Root_M',
     'Toes_L',
     'Ankle_L',
     'Knee_L',
     'Hip_L',
     'HipPart1_L',
     'HipPart2_L',
     'MiddleFinger3_L',
     'MiddleFinger2_L',
     'MiddleFinger1_L',
     'MiddleFinger0_L',
     'IndexFinger3_L',
     'IndexFinger2_L',
     'IndexFinger1_L',
     'IndexFinger0_L',
     'ThumbFinger3_L',
     'ThumbFinger2_L',
     'ThumbFinger1_L',
     'RingFinger3_L',
     'RingFinger2_L',
     'RingFinger1_L',
     'RingFinger0_L',
     'PinkyFinger3_L',
     'PinkyFinger2_L',
     'PinkyFinger1_L',
     'PinkyFinger0_L',
     'Wrist_L',
     'Elbow_L',
     'ElbowPart1_L',
     'ElbowPart2_L',
     'Shoulder_L',
     'ShoulderPart1_L',
     'ShoulderPart2_L',
     'Scapula_L']
     
    pm.select(cl=1)
     
    if pm.objExists('ControlSet'): 
        print 'Set is already exists'
    else:
        pm.sets(n='AllSet')
        
        pm.select(Control_Set)
        pm.sets(n='ControlSet')
        
        pm.select(Deformer_Set)
        pm.sets(n='DeformSet')
        
        mel.eval(('sets -edit -fe  %s %s %s;')%('AllSet', 'ControlSet', 'DeformSet'))

    pm.select(cl=1)


#팔꿈치, 무릎 락 세팅         
def RotLimitSetting(part,CHNameField,x):
    HIKNode = getTextField(CHNameField)
    pm.select(HIKNode)
    
    SideList = ['Left', 'Right']
    ValueList = ['Min', 'Max']
    AttrList = ['x', 'y', 'z']
    
    for side in SideList:
        for Valu in ValueList:
            SetValueName = HIKNode+'.'+side+part+Valu
            print SetValueName
            for att in AttrList:
                getCheckBox = pm.checkBox(part+'_'+att, q=1, v=1)
                if getCheckBox == 1:
                    pm.setAttr(SetValueName+'RLimitEnable'+att, 0)
                else:
                    pm.setAttr(SetValueName+'RLimitEnable'+att, 1)
                    pm.setAttr(SetValueName+'RLimit'+att, 0)

      
    print '---->>   Finished ' + part + ' rotation limit setting   <<----'



#포즈 저장
def savePose(poseName, x):
    #최상위 컨트롤러 이름
    allCtrl = pm.PyNode('Main')
    #최상위 컨트롤러에 포즈 어트리뷰트 추가
    try:
        allCtrl.addAttr(poseName, dt='string')
    except:
        allCtrl.setAttr(poseName, lock=0)
        #이전에 저장된 컨트롤러들 지우고 초기화
        allCtrl.setAttr(poseName, '')
        
    #컨트롤러들 가져오기
    ctrlSetList = pm.listRelatives('ControlSet', children=1)
    crvs = []
    for csl in ctrlSetList:
        if csl.type() ==  'nurbsCurve':
            crvs.append(csl)
        else:
            pass            
        
    ctrls = [crv.getParent() for crv in crvs]

    #컨트롤러 어트리뷰트 값 가져오기
    ctrlVale = {}
    for ctrl in ctrls:
        attrList = ctrl.listAttr(keyable=True)
        for attr in attrList:
            ctrlVale[attr.name()] = attr.get()

    #컨트롤러 값 저장
    poseValue = json.dumps(ctrlVale, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)

    allCtrl.setAttr(poseName, poseValue)
    allCtrl.setAttr(poseName, lock=1)


#저장된 포즈 불러오기    
def loadPose(poseName, x):
    allCtrl = pm.PyNode('Main')
    data = json.loads(allCtrl.attr(poseName).get())
    for key, value in data.iteritems():
        try:
            pm.setAttr(key, value)
        except:
            pass
    
##############################      Window     #####################################################################


def winshow():
    winName = 'HIKSetup'
    if pm.window(winName, exists=1):
        pm.deleteUI(winName)
    
    with pm.window(winName, title='HIK_Setup', widthHeight=(230, 800) , sizeable=1) as win:
        with pm.rowColumnLayout(nc=1, columnWidth=[(1, 230)], rowSpacing=(1, 5)) as layTypes:
            CHNameField = pm.textFieldGrp('CHNameTextField', label='CH_Name :  ', w=120, cw=[(1,60),(2,150)], editable=1)
            btnCreateHIK = pm.button('1.   Creat_HIK', w=230, c=partial(CreateHIK, CHNameField))
            btnSetTpose = pm.button('2.   Set_Tpose', w=230, c=partial(SetTpose) ) #, bgc=[ 0.3 , 0.4 , 0.4 ])
            tx01 = pm.text('Pose')#   -   Save  /  Load' )
            with pm.rowColumnLayout(nc=2, rowSpacing=(1, 5), columnSpacing=(2,10)) as layTypes:
                btnSaveBPose = pm.button('Save  B', w=110, c=partial(savePose, 'Bpose'), bgc=[.0 , .1 , .2] )
                btnSaveTPose = pm.button('Save  T', w=110, c=partial(savePose, 'Tpose'), bgc=[.0 , .2 , .1] )
                btnLoadBPose = pm.button('Load  B', w=110, c=partial(loadPose, 'Bpose'), bgc=[.2 , .6 , .8] )
                btnLoadTPose = pm.button('Load  T', w=110, c=partial(loadPose, 'Tpose'), bgc=[.2 , .8 , .6] )
            btnCtrlCheck = pm.button('3.   Ctrl_Check', w=230, c=partial(CheckCtrl))
            btnLoadCustomHIK = pm.button('4.   HIK  -  Definition  -  Get', w=230, c=partial(LoadCostomHIK))
            btnLockHIK = pm.button('5.   HIK  -  Definition  -  Lock', w=230, c=partial(LockHIK))
            btnArmEditRotLimit = pm.button('6.   HIK  -  Arm Rotate Limit  -  Set', w=230, c=partial(RotLimitSetting, 'ForeArm', CHNameField ) , bgc=[.5 , .2 , .2] )
            pm.text('Check your using axis', bgc=[.6 , .5 , .5])
            #armRotAxisCheck = pm.checkBoxGrp(cw4=[50,50,50,50], numberOfCheckBoxes=3, label='RotAxis:  ', labelArray3=['X', 'Y', 'Z'], cw3=[60,60,60])
            with pm.rowColumnLayout(nc=3, cw=[(1,75),(2,75),(3,75)], cal=[1,'left']):
                checkArmX = pm.checkBox('ForeArm_x', bgc=[.6 , .5 , .5])
                checkArmY = pm.checkBox('ForeArm_y', bgc=[.6 , .5 , .5])
                checkArmZ = pm.checkBox('ForeArm_z', bgc=[.6 , .5 , .5])
            btnLegEditRotLimit = pm.button('6.   HIK  -  Leg Rotate Limit  -  Set', w=230, c=partial(RotLimitSetting, 'Leg', CHNameField) , bgc=[.2 , .2 , .5] )
            pm.text('Check your using axis' , bgc=[.5 , .5 , .6] )
            #armRotAxisCheck = pm.checkBoxGrp(cw4=[50,50,50,50], numberOfCheckBoxes=3, label='RotAxis:  ', labelArray3=['X', 'Y', 'Z'], cw3=[60,60,60])
            with pm.rowColumnLayout(nc=4, cw=[(1,75),(2,75),(3,75)], cal=[1,'left']):
                checkLegX = pm.checkBox('Leg_x' , bgc=[.5 , .5 , .6] )
                checkLegY = pm.checkBox('Leg_y' , bgc=[.5 , .5 , .6] )
                checkLegZ = pm.checkBox('Leg_z' , bgc=[.5 , .5 , .6] )
            btnCreateSet = pm.button('7.   Ctrl  -  Set', w=230, c=partial(CreateADVSet))

            
