#-*- coding: utf-8 -*-
import maya.mel as mel
import pymel.all as pm


def getChildGeo(x):
    geoGrp = pm.PyNode(x)
    pm.select(geoGrp, hi=1)

    geo_list = []
    for geo in pm.selected():
        if geo.nodeType() == 'mesh':
            geo = pm.pickWalk(geo, d='up')[0]
            geo_list.append(geo)
    
    return(geo_list)


def getNameList(x):
    pm.select(x, hi=1)
    nameList = []
    for obj in pm.selected():
        obj = str(obj)
        nameList.append(obj)
    
    return(nameList)


def duplicateItem(x, pre):
    name = getNameList(x)
    dupX = pm.duplicate(x)
    pm.select(dupX, hi=1)
    for i in range(len(pm.selected())):
        pm.rename(pm.selected()[i], pre+name[i])
        
    return(dupX)


def setSubJoints():
    pass
    

def deformerIssueRun():

    chName = pm.pickWalk('geo', d='down')[0].split('_')[0]
    jntGrp = pm.PyNode('DeformationSystem')
    RootJnt = pm.pickWalk(jntGrp, d='down')

    # SUB JOINT

    # 서브조인트 모두 DeformationSystem 하위로 >> 수동으로 해야될듯
    # 조인트의 상위그룹이 1개 이상이면 connection이 안됨 ?
    # bs rig용 조인트들은 하위에 넣지 말 것

    # DeformationSystem에 있는 cnst 노드 모두 ConstraintSystem 하위로
    for cnst in pm.ls(jntGrp, dag=True):
        if cnst.nodeType() == 'parentConstraint':
            pm.parent(cnst, 'ConstraintSystem')
        elif cnst.nodeType() == 'scaleConstraint':
            pm.delete(cnst)
        else:
            pass


    # SET JOINT
    pm.select(jntGrp)
    MainRoot = pm.joint(n='MainRoot_M')
    pm.parent(RootJnt, MainRoot)

    duplicateItem(MainRoot, 'skin_')

    for jnt in pm.ls('Root_M', dag=True):
        if jnt.nodeType() == 'joint':
            pm.connectAttr(jnt+'.t', 'skin_'+jnt+'.t')
            pm.connectAttr(jnt+'.r', 'skin_'+jnt+'.r')


    # SET MODELING
    old_geoGrp = pm.PyNode(chName+'_GRP')
    duplicateItem(old_geoGrp, 'new_')
    new_geoGrp = pm.PyNode('new_'+chName+'_GRP')

    pm.select('skin_Root_M', hi=1)
    pm.select(new_geoGrp, add=1)
    mel.eval('SmoothBindSkin;')
    # pm.skinCluster('skin_Root_M', new_geoGrp, mi=5)

    old_geo_list = getChildGeo(old_geoGrp)
    new_geo_list = getChildGeo(new_geoGrp)

    for i in range(len(old_geo_list)):
        aa = pm.listHistory(pm.PyNode(old_geo_list[i]), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
        if aa == []:
            pass
            print(old_geo_list[i]+': Skin Copy Skipped')
        else:
            pm.copySkinWeights(old_geo_list[i], new_geo_list[i], ia='closestJoint', nm=1, sa='closestPoint')
            print(old_geo_list[i]+': Skin Copy Completed')


    # FINAL
    pm.parentConstraint('Main', MainRoot, mo=1)
    pm.parentConstraint('Main', new_geoGrp, mo=1)
    pm.setAttr(new_geoGrp+'.t', l=1)
    pm.setAttr(new_geoGrp+'.r', l=1)

    pm.disconnectAttr('Root_M.v')
    pm.setAttr('Root_M.v', 1)
    pm.connectAttr('Main.jointVis', 'DeformationSystem.v')
    pm.setAttr('Main.jointVis', 0)

    # 5. blendShape 확인 후 실행!!
    pm.select(old_geoGrp)
    mel.eval('DetachSkin;')
    pm.delete(old_geoGrp)

    for geo in pm.ls(new_geoGrp, dag=True):
        geo = str(geo)
        
        if 'Shape' in geo:
            pass
        else:
            pm.rename(geo, geo[4:])
