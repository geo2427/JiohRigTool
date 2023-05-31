#-*- coding: utf-8 -*-
import os, sys, imp
import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm

import GSRigTool_UI as GSUI
imp.reload(GSUI)

# 해당 스크립트는 최신 버전이 아닐 수 있습니다. 아래 경로의 제일 최신 스크립트로 업데이트 후 사용하는 걸 추천드립니다.
# /home/jioh.kim/Desktop/pipe/wip/A/CorrectiveRig/


partL = [ 'Wrist', 'Elbow', 'ShoulderPart2', 'Shoulder', 'Scapula1', 'Chest', 'Hip', 'Knee', 'Ankle' ]
xyzL = [ 'X', 'Y', 'Z' ]
pmL = [ '_P', '_M' ]
preL = [ 'Pos', 'Rot', 'Sca' ]


def addExtraAttr(driver, driven):

    for i, pre in enumerate(preL):
        for xyz in xyzL:
            attr = pre + xyz

            pm.addAttr(driver, sn=attr, dv=0, k=1, at='double')
            pm.connectAttr(driver+'.'+attr, driven[i].input2+xyz)


def setExtraAttr(guideL):

    valL = [[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0],
            [-1.2000000000000002, -0.09999999999999998, 0.0, -0.2, -0.3, 0.20000000000000004, 0.0, -0.7000000000000002, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.7000000000000001, 0.0, 0.6000000000000001, -0.30000000000000004, -0.1, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-0.6000000000000001, -1.0, 0.0, 0.0, 0.0, -0.4, 0.0, 0.0, 0.0],
            [-0.7000000000000001, -1.5, 0.30000000000000004, 0.1, 0.10000000000000003, -0.20000000000000004, 1.1, -1.7000000000000002, 0.0]],
            
            [[0.10000000000000009, 1.4, 0.30000000000000004, -1.2000000000000002, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-3.1999999999999997, 1.3, 1.6, -1.6, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-0.30000000000000004, 0.0, 0.0, 0.0, 0.0, -0.7000000000000001, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-0.10000000000000003, 0.6000000000000001, -0.9, -1.2000000000000002, 1.8, -0.4, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.8, 0.5, 0.0, -0.30000000000000004, 0.20000000000000007, -3.9000000000000004, 0.0, 0.0, 0.0],
            [-0.30000000000000004, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[-0.10000000000000009, -0.40000000000000013, 1.0, -0.7000000000000001, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-0.20000000000000004, -0.5, 0.0, -0.9, 0.2, 0.0, 0.0, 0.4, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-0.5, 0.0, -0.1, -0.1, 0.0, -0.8000000000000002, -0.09999999999999998, 0.0, 0.8999999999999999]],
            
            [[0.0, 0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.4, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, -0.30000000000000004, 0.1, -0.30000000000000004, 0.0, -0.30000000000000004, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, -0.6, 0.20000000000000004, -0.9, 0.0, 0.0, 0.0, -0.5, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.4, 0.0, 0.2, 0.0, -0.9, -1.3],
            [0.0, -0.2, 0.2, -1.3, 0.0, 0.0, 0.0, -0.29999999999999993, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
            
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]]
    
    for g, guide in enumerate(guideL):
        name = guide.split('_')
        prefix = name[1] + '_R_' + name[2]

        for i, xyz in enumerate(xyzL):
            for j, PM in enumerate(pmL):
                obj = '_Rot' + xyz + PM
                
                for m, pre in enumerate(preL):
                    for n, xyz2 in enumerate(xyzL):
                        attr = '.'+pre+xyz2

                        driven = prefix+obj+attr
                        vals = valL[g][i*2+j][m*3+n]
                                            
                        # print('# ' + driven, '=', vals)
                        pm.setAttr(driven, vals)


def setMirrorL(guideL):

    for guide in guideL:
        nameL = guide.split('_')
        part = nameL[1]
        crtv = '_'+nameL[2]
        side = '_'+nameL[3]

        for XYZ in xyzL:
            for PM in pmL:
                name = part + side + crtv + '_Rot' + XYZ + PM

                driver = pm.PyNode(part + '_R' + crtv + '_Rot' + XYZ + PM)
                driven = pm.PyNode(name)

                mirrorMD = pm.createNode('multiplyDivide', n=name+'_mirror_md')
                revMaxMD = pm.createNode('multiplyDivide', n=name+'_maxTransLimit_md')
                revMinMD = pm.createNode('multiplyDivide', n=name+'_minTransLimit_md')
                pm.setAttr(mirrorMD.input2, -1,-1,-1)
                pm.setAttr(revMaxMD.input2, -1,-1,-1)
                pm.setAttr(revMinMD.input2, -1,-1,-1)
                
                for xyz in xyzL:
                    
                    # Extra
                    for pre in preL:
                        attr = pre + xyz

                        if pre == 'Pos':
                            pm.connectAttr(driver+'.'+attr, mirrorMD.input1+xyz)
                            pm.connectAttr(mirrorMD.output+xyz, driven+'.'+attr)
                        else:
                            pm.connectAttr(driver+'.'+attr, driven+'.'+attr)

                    # Limit
                    for pre in [ 'Trans', 'Rot', 'Scale' ]:
                        for lim in [ 'Limit', 'LimitEnable' ]:
                            for mm in [ '.min', '.max' ]:
                                attr = mm + pre + xyz + lim
                                pm.connectAttr(driver+attr, driven+attr)

                    # Reverse Limit
                    if not xyz == 'Y':
                        if pm.isConnected(driver+attr, driven+attr):
                            pm.disconnectAttr(driven+'.maxTrans'+xyz+'Limit')
                            pm.disconnectAttr(driven+'.maxTrans'+xyz+'LimitEnable')
                            pm.disconnectAttr(driven+'.minTrans'+xyz+'Limit')
                            pm.disconnectAttr(driven+'.minTrans'+xyz+'LimitEnable')
                        
                        pm.connectAttr(driver+'.minTrans'+xyz+'Limit', revMaxMD.input1+xyz)
                        pm.connectAttr(revMaxMD.output+xyz, driven+'.maxTrans'+xyz+'Limit')
                        pm.connectAttr(driver+'.minTrans'+xyz+'LimitEnable', driven+'.maxTrans'+xyz+'LimitEnable')

                        pm.connectAttr(driver+'.maxTrans'+xyz+'Limit', revMinMD.input1+xyz)
                        pm.connectAttr(revMinMD.output+xyz, driven+'.minTrans'+xyz+'Limit')
                        pm.connectAttr(driver+'.maxTrans'+xyz+'LimitEnable', driven+'.minTrans'+xyz+'LimitEnable')
                        

def setCrtvNodes(name, driver, driven):
    
    cns = 'Cns_'+name
    cnt = 'Cnt_'+name
    
    xyz = name.split('_')[3][-1]
    PM = name.split('_')[4]

    # CNS_CONDITION
    CON = pm.createNode('condition', n=cns+'_con')
    pm.connectAttr(driver.rotate+xyz, CON.firstTerm)
    if 'P' in PM:
        pm.setAttr(CON.operation, 2) # Greater Than
    else:
        pm.setAttr(CON.operation, 4) # Less Than
    pm.setAttr(CON.colorIfTrueR, 1.0)
    pm.setAttr(CON.colorIfFalseR, 0.0)

    # CNS_MD
    MD = pm.createNode('multiplyDivide', n=cns+'_md')
    pm.connectAttr(driver.rotate+xyz, MD.input1X)
    pm.connectAttr(driver.rotate+xyz, MD.input1Y)
    pm.connectAttr(driver.rotate+xyz, MD.input1Z)
    pm.connectAttr(CON.outColorR, MD.input2X)
    pm.connectAttr(CON.outColorR, MD.input2Y)
    pm.connectAttr(CON.outColorR, MD.input2Z)

    # CNT_TRANSLATE
    tMD01 = pm.createNode('multiplyDivide', n=cnt+'_trans_md01')
    pm.connectAttr(MD.output, tMD01.input1)

    tMD02 = pm.createNode('multiplyDivide', n=cnt+'_trans_md02')
    pm.connectAttr(tMD01.output, tMD02.input1)
    pm.setAttr(tMD02.input2, 0.01,0.01,0.01)
    pm.connectAttr(tMD02.output, driven.t)

    # CNT_ROTATE
    rMD01 = pm.createNode('multiplyDivide', n=cnt+'_rotate_md01')
    pm.connectAttr(MD.output, rMD01.input1)
    pm.connectAttr(rMD01.output, driven.r)

    # CNT_SCALE
    sMD01 = pm.createNode('multiplyDivide', n=cnt+'_scale_md01')
    pm.connectAttr(MD.output, sMD01.input1)

    sMD02 = pm.createNode('multiplyDivide', n=cnt+'_scale_md02')
    pm.connectAttr(sMD01.output, sMD02.input1)
    pm.setAttr(sMD02.input2, 0.01,0.01,0.01)

    sPMA = pm.createNode('plusMinusAverage', n=cnt+'_scale_pma')
    pm.connectAttr(sMD02.output, sPMA.input3D[0])
    pm.connectAttr(sPMA.output3D, driven.s)
    tf = pm.createNode('transform')
    pm.setAttr(tf.t, 1,1,1)
    pm.connectAttr(tf.t, sPMA.input3D[1])
    pm.delete(tf)

    cntL = [ tMD01, rMD01, sMD01 ]
    return cntL


def setCrtvRig(guideL, side):

    sideAllGrp = pm.group(n='Corrective'+side+'_RigGrp', em=True, p='CorrectiveRigGrp')
    sideJntSet = pm.sets(n='Corrective'+side+'_JntSet', em=True)
    
    for part in partL:
        
        if pm.objExists(part):
            print(part)
            
            ################################ grp01, grp02
            
            if part == 'Chest':
                p_side = '_M'
                prntJnt = pm.PyNode(part+p_side)
                
                if not pm.objExists('Cns_Chest_M_Corrective'):
                    MAllGrp = pm.group(n='Corrective'+p_side+'_RigGrp', em=True, p='CorrectiveRigGrp')
                    grp02 = pm.group(n='Cns_'+part+p_side+'_Corrective', em=True)
                    pm.delete(pm.parentConstraint(prntJnt, grp02, mo=0))
                    pm.parentConstraint(prntJnt, grp02, mo=1)
                    pm.scaleConstraint(prntJnt, grp02, mo=1)
                    pm.parent(grp02, MAllGrp)
                else:
                    grp02 = pm.PyNode('Cns_Chest_M_Corrective')

            else:
                p_side = side
                prntJnt = pm.PyNode(part+p_side)
                gPrntJnt = pm.pickWalk(prntJnt, d='up')[0]

                grp01 = pm.group(n='Cns_'+part+p_side+'_Corrective', em=True)
                pm.delete(pm.parentConstraint(prntJnt, grp01, mo=0))
                pm.parentConstraint(gPrntJnt, grp01, mo=1)
                pm.scaleConstraint(gPrntJnt, grp01, mo=1)
                pm.parent(grp01, sideAllGrp)

                grp02 = pm.group(n='Grp_'+part+p_side+'_Corrective', em=True)
                pm.parent(grp02, grp01)
                pm.makeIdentity(grp02, apply=True)
                pm.parentConstraint(prntJnt, grp02, mo=1)

            ################################ grp03, jnt, loc

            for guide in guideL:
                name = guide.split('_')
                crtv = '_'+name[2]

                if part == name[1]:

                    crtvJnt = pm.joint(n=part+side+crtv, rad=0.5)
                    sideJntSet.add(crtvJnt)
                    pm.parent(crtvJnt, prntJnt)
                    pm.delete(pm.pointConstraint(guide, crtvJnt, mo=0))
                    pm.delete(pm.orientConstraint(prntJnt, crtvJnt, mo=0))
                    pm.makeIdentity(crtvJnt, apply=True)

                    grp03 = pm.group(n='Cnt_'+part+side+crtv, em=True)
                    pm.delete(pm.parentConstraint(crtvJnt, grp03, mo=0))
                    pm.parent(grp03, grp02)

                    for xyz in xyzL:
                        for PM in pmL:
                            name = part + side + crtv + '_Rot' + xyz + PM

                            # LOCATOR
                            loc = pm.spaceLocator(n=name)
                            pm.setAttr(loc.localScale, 0.1,0.1,0.1)

                            if pm.listRelatives(grp03) == []:
                                pm.parent(loc, grp03, s=True)
                            else:
                                # pm.select(grp03, hi=1)
                                # pm.parent(loc, pm.selected()[-2])
                                pm.parent(loc, pm.ls(grp03, dag=True)[-2])
                            
                            # Corrective NODES / EXTRA ATTR
                            suffix = side + '_Corrective'
                            if part == 'ShoulderPart2':
                                driver = 'Grp_Elbow'+suffix
                            elif part == 'Scapula':
                                if '1' in crtv:
                                    driver = 'Grp_Shoulder'+suffix
                                else:
                                    driver = 'Grp_Scapula'+suffix
                            elif part == 'Chest':
                                if '1' in crtv:
                                    driver = 'Grp_Scapula'+suffix
                                else:
                                    driver = 'Grp_Shoulder'+suffix
                            else:
                                driver = grp02

                            cntL = setCrtvNodes(name, pm.PyNode(driver), loc)
                            addExtraAttr(loc, cntL)

                    endLoc = pm.ls(grp03, dag=True)[-2]
                    pm.parentConstraint(endLoc, crtvJnt, mo=1)
                    pm.scaleConstraint(endLoc, crtvJnt, mo=1)


def setCrtvGuide(side):
    
    guide = 'g_Corrective'+side
    
    if not pm.objExists(guide):
        L_guide = pm.duplicate('g_Corrective_R', n=guide)[0]
        pm.setAttr(L_guide.s, -1, 1, 1)
        [pm.rename(g, g.name().replace('_R', side)) for g in pm.ls(L_guide, dag=True)]

    grp = pm.listRelatives(guide)
    loc = pm.pickWalk(grp, d='down')
    
    return loc


def main():
    
    if pm.objExists('g_Corrective_R'):
    
        allSet = pm.sets(n='CorrectiveJntSet', em=True)
        Grp = pm.group(n='CorrectiveRigGrp', em=True)
        allGrp = pm.group(n='g_Corrective', em=True, p=Grp)
        pm.hide(allGrp)
        
        for side in [ '_R', '_L' ]:
            
            guideL = setCrtvGuide(side)
            setCrtvRig(guideL, side)
            
            if side == '_R':
                # setExtraAttr(guideL)
                pass
            else:
                setMirrorL(guideL)
            
            allSet.add('Corrective'+side+'_JntSet')
            pm.parent('g_Corrective'+side, allGrp)

        pm.select(cl=1)
        pm.displayInfo('Corrective Rig Completed')
    
    else:
        pm.displayInfo('Corrective Rig Skipped')


################################################################################### for GSRigTool


def ReBuildMain():
    
    if pm.objExists('CorrectiveRigGrp'):
        pm.parent('g_Corrective_R', w=1)
        pm.delete('CorrectiveRigGrp')
        pm.delete('Corrective*JntSet')
    
    main()
    
    
def importCrtvGuide():
    
    with pm.UndoChunk():
    
        if not pm.objExists('g_Corrective_R'):

            locGrp = pm.group(n='g_Corrective_R', em=True)
            Fit = pm.getAttr('FitSkeleton.scaleX')
            crtvNumL = [ 2, 2, 2, 4, 2, 2, 4, 2, 2 ]
            
            for i, part in enumerate(partL):
                
                locL = []
                
                for j in range((crtvNumL[i])):
                    name = 'g_' + part + '_crtv' + str(j+1).zfill(2) + '_R'
                    
                    s = Fit/10
                    loc = pm.spaceLocator(n=name)
                    locL.append(loc)
                    pm.setAttr(loc.localScale, s,s,s)
                    
                    locG = pm.group(n=name+'_grp', em=True)
                    pm.parent(loc, locG)
                    pm.parent(locG, locGrp)
                    
                    if part == 'ShoulderPart2':
                        pm.delete(pm.parentConstraint('Shoulder', 'Elbow', locG, mo=0))
                        pm.parentConstraint('Shoulder', locG, mo=1)
                    else:
                        pm.delete(pm.parentConstraint(part, locG, mo=0))
                        pm.parentConstraint(part, locG, mo=1)

                # 보류
                # uiVal = GSUI.GSRigUI.crtvSlider(GSUI.GSRigUI)
                # realVal = float(uiVal) / 10
                # pos = Fit/3 * realVal
                
                pos = Fit*2
                if part == 'Ankle':
                    pm.move(locL[0], 0,0,pos, r=True, os=True, wd=True)
                    pm.move(locL[1], 0,0,-pos, r=True, os=True, wd=True)
                elif part == 'Scapula':
                    pm.move(locL[0], pos,0,0, r=True, os=True, wd=True)
                    pm.move(locL[1], 0,0,-pos, r=True, os=True, wd=True)
                elif part == 'Chest':
                    pm.move(locL[0], 0,0,pos, r=True, os=True, wd=True)
                    pm.move(locL[1], -pos,0,0, r=True, os=True, wd=True)
                elif part == 'Hip':
                    pm.move(locL[0], 0,0,pos, r=True, os=True, wd=True)
                    pm.move(locL[1], pos,0,0, r=True, os=True, wd=True)
                    pm.move(locL[2], 0,0,-pos, r=True, os=True, wd=True)
                    pm.move(locL[3], -pos,0,0, r=True, os=True, wd=True)
                else:
                    if len(locL) == 4:
                        pm.move(locL[0], pos,0,0, r=True, os=True, wd=True)
                        pm.move(locL[1], 0,0,pos, r=True, os=True, wd=True)
                        pm.move(locL[2], -pos,0,0, r=True, os=True, wd=True)
                        pm.move(locL[3], 0,0,-pos, r=True, os=True, wd=True)
                    elif len(locL) == 2:
                        pm.move(locL[0], 0,0,pos, r=True, os=True, wd=True)
                        pm.move(locL[1], 0,0,-pos, r=True, os=True, wd=True)
                
                for loc in locL:
                    pm.makeIdentity(loc, apply=True)
                    
            pm.displayInfo('Corrective Guides Completed')
                    
        else:
            pm.warning('Corrective Guides Already Exists')
            
        pm.select(cl=1)


def deleteCrtvGuide():
    
    with pm.UndoChunk():

        guide = 'g_Corrective_R'
        
        if pm.objExists(guide):
            pm.delete(guide)
            pm.displayInfo('Corrective Guide Deleted')
        else:
            pass
            pm.warning('Corrective Guide Already Deleted')


def mirrorGuide():
    
    with pm.UndoChunk():
        
        if pm.objExists('g_Corrective_R'):
        
            if not pm.objExists('g_Corrective_L'):
                side = '_L'

                L_guide = pm.duplicate('g_Corrective_R', n='g_Corrective'+side)[0]
                pm.setAttr(L_guide.s, -1, 1, 1)
                [pm.rename(g, g.name().replace('_R', side)) for g in pm.ls(L_guide, dag=True)]

                for guide in pm.listRelatives(L_guide):
                    part = guide.split('_')[1]
                    driver = 'g_' + part + side
                    
                    pm.delete(guide + '_parentConstraint1')

                    if part == 'ShoulderPart2':
                        pm.parentConstraint('g_Shoulder'+side, guide, mo=1)
                    elif part == 'Chest':
                        pm.parentConstraint('Chest', guide, mo=1)
                    else:
                        pm.parentConstraint(driver, guide, mo=1)

                pm.select(cl=1)
                pm.displayInfo('R Corrective Guide Mirrored')
                
            else:
                pm.warning('L Corrective Guide Already Exists')


def toggleCrtvGuide():
    
    grp = 'CorrectiveRigGrp'
    
    if pm.objExists(grp):
        for obj in pm.listRelatives(grp):
            if obj == 'g_Corrective':
                pm.setAttr(obj+'.v', 1)
            else:
                pm.setAttr(obj+'.v', 0)
        pm.hide('g_Corrective_L')


