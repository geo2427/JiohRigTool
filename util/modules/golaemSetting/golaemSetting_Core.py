#-*- coding: utf-8 -*-
import maya.mel as mel
import pymel.all as pm


def check_plugins() -> None:
    un_nodes = pm.ls(type="unknown")
    un_plugins = pm.unknownPlugin(q=True, l=True)
    
    print(un_nodes)
    print(un_plugins)
    del_count = 0
    if un_plugins:
        for cur_plugin in un_plugins:
            pm.unknownPlugin(cur_plugin, r=True)
            del_count += 1
    pm.displayInfo("삭제 노드 개수: {0}".format(str(del_count)))
    
    
def golaemSettingRun():

    geoG = pm.pickWalk('geo', d='down')[0]
    jntG = pm.PyNode('DeformationSystem')
    name = geoG.split('_')[0]

    crowdGeo = pm.duplicate(geoG)[0]
    crowdJnt = pm.duplicate(jntG)[0]

    pm.select(geoG, jntG)
    mel.eval('PrefixHierarchyNames;') # Prees 'OK'

    pm.parent(crowdGeo, crowdJnt, w=1)
    pm.rename(crowdGeo, name+'_GRP')
    pm.rename(crowdJnt, 'DeformationSystem')

    jntL = []
    for jnt in pm.ls('Root_M', dag=True):
        if pm.nodeType(jnt)=='joint':
            if 'crtv' in str(jnt):
                jntL.append(jnt)
    pm.delete(jntL)

    pm.select('Root_M', hi=1)
    pm.select(crowdGeo, add=1)
    mel.eval('SmoothBindSkin;')

    sel = crowdGeo
    if sel.getShape()==None and pm.nodeType(sel)=='transform':
        
        for x in pm.ls(sel, dag=True):
            if x.listRelatives(c=1, s=1, type='mesh'):
                if x.intermediateObject.get() == 0:
                    x = str(x)
                    driver = 'prefix_'+x
                    driven = x
                    
                    pm.select(driver)
                    pm.select(driven, add=1)
                    try:
                        pm.copySkinWeights(nm=1, sa='closestPoint', ia='closestJoint')
                        print(driver, '>>>>>', driven)
                    except:
                        pass

    pm.delete('SubRigGrp')
    pm.delete('Group')
    pm.delete('prefix_'+name+'_GRP')

    pm.parent(crowdGeo, 'geo')
    pm.parent(crowdJnt, 'rig')
    pm.setAttr('Root_M.v', 1)

    setL = ['Sets', 'AllSet', 'DeformSet', 'ControlSet', 'CorrectiveJntSet']
    for obj in setL:
        if pm.objExists(obj):
            pm.delete(obj)
    
    mel.eval('cleanUpScene(1)')
    check_plugins()

    pm.informBox(title='Golaem Setting', message='가전제품 스키닝을 까먹지 마십시오')
