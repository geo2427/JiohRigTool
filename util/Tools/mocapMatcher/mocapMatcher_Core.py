# coding:utf-8
import pymel.all as pm
from functools import partial

partML = [ 'Root', 'Spine1', 'Spine2', 'Chest', 'Neck', 'Head' ]
partL = [ 'Shoulder', 'Elbow', 'Wrist', 'Scapula1', 'Shoulder1', 'Elbow1', 'Wrist1', 'Hip', 'Knee', 'Ankle', 'Toes']
sideL = [ '_R', '_L' ]


def connectMocapRig(*args):
    
    rig = pm.textField("RigNS", q=1, text=1)
    
    if pm.nodeType(pm.listRelatives(rig+':RootX_M')[-1])=='ParentConstraint':
        pm.displayInfo(rig+': Mocap Already Connected')

    else:
        switchToFK()
        org = pm.getCurrentTime()
        pm.setCurrentTime(990)
        
        mocap = pm.textField("MocapNS", q=1, text=1)
        rig = pm.textField("RigNS", q=1, text=1)

        for part in partL:
            for side in sideL:
                driver = mocap+':'+part+side
                driven = rig+':FK'+part+side

                if pm.objExists(driven):
                    if pm.objExists(driver):
                        pm.parentConstraint(driver, driven, mo=1, n=driven+'_parentConstraint')
                        
        for part in partML:
            driver = mocap+':'+part+'_M'

            if part == 'Root':
                driven = rig+':RootX_M'
                pm.parentConstraint(driver, driven, mo=1, n=driven+'_parentConstraint')
            else:
                driven = rig+':FK'+part+'_M'
                pm.parentConstraint(driver, driven, mo=1, n=driven+'_parentConstraint')

        pm.setCurrentTime(org)
        pm.displayInfo('Connect: '+mocap+'  >>>>  '+rig)
    

def deleteConstraint(*args):
    
    rig = pm.textField("RigNS", q=1, text=1)
    
    if pm.nodeType(pm.listRelatives(rig+':RootX_M')[-1])=='ParentConstraint':
        pm.displayInfo(rig+': Mocap Already Disconnected')

    else:
        org = pm.getCurrentTime()
        pm.setCurrentTime(990)
        
        for part in partL:
            for side in sideL:
                driven = rig+':FK'+part+side
                if pm.objExists(driven):
                    cnst = driven+'_parentConstraint'
                    pm.delete(cnst)
                    
        for part in partML:
            if part == 'Root':
                pm.delete(rig+':RootX_M_parentConstraint')
            else:
                cnst = rig+':FK'+part+'_M_parentConstraint'
                pm.delete(cnst)
                
        pm.setCurrentTime(org)
        pm.displayInfo(rig+': Mocap Disconnected')


def switchToFK(*args):
    
    rig = pm.textField("RigNS", q=1, text=1)
    
    for obj in pm.ls(rig+':FKIK*', dag=True):
        FKIK = obj+'.FKIKBlend'
        if pm.objExists(FKIK):
            if FKIK == 10:
                pm.setAttr(FKIK, 0)
            else:
                pm.setAttr(FKIK, 0)
                
                
############################################################### UI


def addTsl(tsl, x):
    aa = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    for item in [ 'UI', 'shared' ]:
        if item:
            aa.remove(item)
    tsl.removeAll()
    tsl.append(aa)


def removeTsl(tsl, x):
    tsl.removeAll()
    
    
def addMocapName(x):
    sel = pm.textScrollList('tslName', q=1, si=1)[0]
    pm.textField("MocapNS", edit=True, text=sel)
    return sel


def addRigName(x):
    sel = pm.textScrollList('tslName', q=1, si=1)[0]
    pm.textField("RigNS", edit=True, text=sel)
    return sel


############################################################### Window

    
def MainUI():
    MainWin = "MainWinName"
    if pm.window(MainWin, ex=1):
        pm.deleteUI(MainWin)

    with pm.window(MainWin, title='GS Mocap Matcher', w=300, h=200):
        pm.frameLayout(l='Edit_v230519_ ⁽⁽◝( ˙ ꒳ ˙ )◜⁾⁾ ', bgc=(0.5, 0.5, 0.5))

        with pm.rowLayout(nc=2):
            with pm.rowColumnLayout(co=(1, 'both', 10), ro=[(1, 'top', 5), (2, 'both', 5), (3, 'bottom', 5)]):
                pm.text('[ NameSpace ]')
                tslName = pm.textScrollList('tslName', ams=1, w=250, h=175)

                with pm.rowColumnLayout(nc=2, co=[(1, 'left', 30), (2, 'left', 7)]):
                    pm.button(l='Get', w=85, c=partial(addTsl, tslName))
                    pm.button(l='Remove', w=85, c=partial(removeTsl, tslName))

            with pm.rowColumnLayout(co=(1, 'both', 10), ro=[(1, 'top', 5), (6, 'bottom', 5)]):
                with pm.rowColumnLayout(nc=2, ro=[(1, 'bottom', 10), (2, 'bottom', 10)]):
                    pm.textField("MocapNS", ed=0, w=180, h=30)
                    pm.button(l='  Mocap  ', h=30, c=addMocapName)
                    pm.textField("RigNS", ed=0, w=180, h=30)
                    pm.button(l='  Rig  ', h=30, c=addRigName)
                pm.separator(h=25)

                with pm.rowColumnLayout(nc=2, co=[(1, 'left', 10), (2, 'left', 7)]):
                    pm.button(l='Apply', w=100, h=30, bgc=(0.65, 0.6, 0.77), c=connectMocapRig)
                    pm.button(l='Disconnect', w=100, h=30, c=deleteConstraint)




