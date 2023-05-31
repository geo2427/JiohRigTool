#-*- coding: utf-8 -*-
import maya.mel as mel
import pymel.all as pm
import pymel.core as core
from functools import partial
import maya.api.OpenMaya as OM


def createFollicleFromPoint(mesh, postion):
    mSel = OM.MGlobal.getSelectionListByName(mesh)
    dMesh = mSel.getDagPath(0)
    dMesh.extendToShape()
    fnMesh = OM.MFnMesh(dMesh)
    mPoint = OM.MPoint(postion)
    uvVal = fnMesh.getUVAtPoint(mPoint, OM.MSpace.kWorld, uvSet=fnMesh.getUVSetNames()[0])

    follicleNode = pm.createNode("follicle")
    follicleTransForm = pm.listRelatives(follicleNode, parent=True)[0]

    folName = follicleNode.getParent()
    folName.rename('SkirtFollicle' + str(1).zfill(2))
    folName.getShape().rename(folName.name() + 'Shape')

    pm.connectAttr(mesh + ".outMesh", follicleNode + ".inputMesh")
    pm.connectAttr(mesh + ".worldMatrix", follicleNode + ".inputWorldMatrix")
    pm.connectAttr(follicleNode + ".outTranslate", follicleTransForm + ".translate")
    pm.connectAttr(follicleNode + ".outRotate", follicleTransForm + ".rotate")
    pm.setAttr(follicleNode + ".parameterU", uvVal[0])
    pm.setAttr(follicleNode + ".parameterV", uvVal[1])

    return {"node": follicleNode, "transform": follicleTransForm}


def folSubRig(tsl, x):
    num = core.uitypes.TextScrollList(tsl).getAllItems()
    origin = pm.PyNode(getTf("orgGeoField"))
    target = pm.PyNode(getTf("targetGeoField"))
    dummy = pm.PyNode(getTf("follicleGeoField"))

    # LOCATOR
    locs = []
    locGrps = []
    locSubGrp = pm.group(n='SkirtSubLocGrp', em=True)
    for i in range(len(num)):
        loc = pm.spaceLocator(n='SkirtSubLoc' + str(i+1).zfill(2))
        loc.getShape().rename(loc.name() + 'Shape')
        locs.append(loc)
        locGrp = pm.group(loc, n=loc.name() + 'Grp')
        locGrps.append(locGrp)
        pm.parent(locGrp, locSubGrp)
        pm.delete(pm.parentConstraint(num[i], locGrp, mo=False))

    # CTRL
    ctrls = []
    ctrlGrps = []
    ctrlSubGrp = pm.group(n='SkirtSubCtrlGrp', em=True)
    for i in range(len(num)):
        ctrl = pm.curve(n='SkirtSubCtrl' + str(i+1).zfill(2), d=3,
                        p=[(-2.0, 0.0, 0.0), (-2.0, 0.522408, 0.0), (-1.567224, 1.567224, 0.0), (-0.522408, 2.0, 0.0),
                           (0.0, 2.0, 0.0), (0.0, 2.0, 0.522408), (0.0, 1.567224, 1.567224), (0.0, 0.522408, 2.0),
                           (0.0, 0.0, 2.0), (0.522408, 0.0, 2.0), (1.567224, 0.0, 1.567224), (2.0, 0.0, 0.522408),
                           (2.0, 0.0, 0.0), (2.0, 0.522408, 0.0), (1.567224, 1.567224, 0.0), (0.522408, 2.0, 0.0),
                           (0.0, 2.0, 0.0), (0.0, 2.0, -0.522408), (0.0, 1.567224, -1.567224), (0.0, 0.522408, -2.0),
                           (0.0, 0.0, -2.0), (0.522408, 0.0, -2.0), (1.567224, 0.0, -1.567224), (2.0, 0.0, -0.522408),
                           (2.0, 0.0, 0.0), (2.0, -0.522408, 0.0), (1.567224, -1.567224, 0.0), (0.522408, -2.0, 0.0),
                           (0.0, -2.0, 0.0), (-0.522408, -2.0, 0.0), (-1.567224, -1.567224, 0.0), (-2.0, -0.522408, 0.0),
                           (-2.0, 0.0, 0.0), (-2.0, 0.0, -0.522408), (-1.567224, 0.0, -1.567224), (-0.522408, 0.0, -2.0),
                           (0.0, 0.0, -2.0), (0.0, -0.522408, -2.0), (0.0, -1.567224, -1.567224), (0.0, -2.0, -0.522408),
                           (0.0, -2.0, 0.0), (0.0, -2.0, 0.522408), (0.0, -1.567224, 1.567224), (0.0, -0.522408, 2.0),
                           (0.0, 0.0, 2.0), (-0.522408, 0.0, 2.0), (-1.567224, 0.0, 1.567224), (-2.0, 0.0, 0.522408),
                           (-2.0, 0.0, 0.0)],
                        k=[8.0, 8.0, 8.0, 9.0, 10.0, 10.0, 10.0, 11.0, 12.0, 12.0, 12.0, 13.0, 14.0, 14.0, 14.0, 15.0, 16.0,
                           16.0, 16.0, 17.0, 18.0, 18.0, 18.0, 19.0, 20.0, 20.0, 20.0, 21.0, 22.0, 22.0, 22.0, 23.0, 24.0, 24.0,
                           24.0, 25.0, 26.0, 26.0, 26.0, 27.0, 28.0, 28.0, 28.0, 29.0, 30.0, 30.0, 30.0, 31.0, 32.0, 32.0,
                           32.0])
        ctrl.getShape().overrideEnabled.set(True)
        ctrl.getShape().overrideColor.set(20)
        ctrl.getShape().rename(ctrl.name() + 'Shape')
        ctrls.append(ctrl)

        ctrlGrp = pm.group(ctrl, n=ctrl.name() + 'Grp')
        ctrlGrps.append(ctrlGrp)
        pm.parent(ctrlGrp, ctrlSubGrp)
        pm.delete(pm.parentConstraint(num[i], ctrlGrp, mo=False))

    # JOINT
    jnts = []
    jntSubGrp = pm.group(n='SkirtSubJntGrp', em=True)
    for i in range(len(num)):
        pm.select(cl=True)
        jnt = pm.joint(n='SkirtSubJnt' + str(i+1).zfill(2))
        jnts.append(jnt)
        pm.parent(jnt, jntSubGrp)
        pm.delete(pm.parentConstraint(num[i], jnt, mo=False))
        pm.parentConstraint(locs[i], jnt, mo=True)

    SubRootJnt = pm.joint(n='SkirtSubRootJnt')
    if pm.objExists('RootJnt'):
        pm.delete(pm.pointConstraint('RootJnt', SubRootJnt, mo=False))
    else:
        pm.delete(pm.pointConstraint('Root_M', SubRootJnt, mo=False))
    jnts.append(SubRootJnt)
    pm.parent(SubRootJnt, jntSubGrp)

    # FOLLICLE
    mesh = dummy.getChildren()[0].name()
    folSubGrp = pm.group(n='SkirtFollicleGrp', em=True)
    for i in ctrlGrps:
        follicle = createFollicleFromPoint(mesh, pm.xform(i, q=True, ws=True, rp=True))
        pm.parentConstraint(follicle["transform"], i, mo=1)
        follicle["transform"].setParent(folSubGrp)

    # CONNECTION
    for i in range(len(num)):
        var = ctrls[i].translate >> locs[i].translate
        var = ctrls[i].rotate >> locs[i].rotate

    # DEFORM
    originBindJnt = pm.skinCluster(origin, inf=1, q=1)
    pm.select(originBindJnt, dummy)
    mel.eval('SmoothBindSkin;')
    pm.select(origin, dummy)
    mel.eval('CopySkinWeights;')
    pm.select(jnts, target)
    mel.eval('SmoothBindSkin;')

    pm.blendShape(target, origin, foc=True, n='bs_' + getTf('newNameField') + 'Fol', w=[0, 1])

    # CLEANUP
    subGrp = pm.group(n=getTf('newNameField') + 'RigGrp', em=True)
    pm.hide(subGrp)
    pm.parent(target, dummy, ctrlSubGrp, folSubGrp, jntSubGrp, locSubGrp, subGrp)

    for item in subGrp.listRelatives(ad=True):
        item.rename(item.name().replace('Skirt', getTf('newNameField')))

    pm.parent(ctrlSubGrp, w=1)

    if pm.objExists('SubRigGrp'):
        pm.parent(subGrp, 'SubRigGrp')
    else:
        pm.group(n='SubRigGrp', em=True)
        pm.parent(subGrp, 'SubRigGrp')
        pm.parent('SubRigGrp', 'RigGrp')


############################################################### 


def getTf(x):
    gettext = pm.textField(x, q=True, tx=True)
    return gettext


def addTsl(tsl, x):
    sel = core.general.selected()
    tsl.removeAll()
    tsl.append(sel)


def removeTsl(tsl, x):
    tsl.removeAll()


def addOrgGeo(*args):
    sel = pm.ls(sl=1)
    aa = pm.textField("orgGeoField", edit=True, text=sel[0])
    return aa


def addTgGeo(*args):
    sel = pm.ls(sl=1)
    bb = pm.textField("targetGeoField", edit=True, text=sel[0])
    return bb


def addFolGeo(*args):
    sel = pm.ls(sl=1)
    cc = pm.textField("follicleGeoField", edit=True, text=sel[0])
    return cc


def resetUI(tsl, *args):
    tsl.removeAll()
    pm.textField('newNameField', edit=True, text='')
    pm.textField("orgGeoField", edit=True, text='')
    pm.textField("targetGeoField", edit=True, text='')
    pm.textField("follicleGeoField", edit=True, text='')


############################################################### Window


def MainUI():
    MainWin = "MainWinName"
    if pm.window(MainWin, ex=1):
        pm.deleteUI(MainWin)

    with pm.window(MainWin, title='Follicle Sub Rig', rtf=1):
        pm.frameLayout(l='Edit_v220729', bgc=(0.5, 0.5, 0.5))

        with pm.rowLayout(nc=2):
            with pm.rowColumnLayout(co=(1, 'both', 10), ro=[(1, 'top', 5), (2, 'both', 5), (3, 'bottom', 5)]):
                pm.text('[ select guide Locator ]')
                tslLoc = pm.textScrollList('tslLoc', ams=1, w=150, h=150)

                with pm.rowColumnLayout(nc=2, co=(1, 'right', 7)):
                    pm.button(l='Add', w=70, c=partial(addTsl, tslLoc))
                    pm.button(l='Remove', w=70, c=partial(removeTsl, tslLoc))

            with pm.rowColumnLayout(co=(1, 'both', 10), ro=[(1, 'top', 5), (6, 'bottom', 5)]):
                with pm.rowColumnLayout(nc=2):
                    pm.text('Name : ')
                    pm.textField('newNameField', h=25, w=135)
                pm.separator(h=25)

                with pm.rowColumnLayout(nc=2, ro=[(1, 'bottom', 10), (2, 'bottom', 10)]):
                    pm.textField("orgGeoField", ed=0)
                    pm.button(l='  origin geo  ', c=addOrgGeo)
                    pm.textField("targetGeoField", ed=0)
                    pm.button(l='  target geo  ', c=addTgGeo)
                    pm.textField("follicleGeoField", ed=0)
                    pm.button(l='  follicle geo  ', c=addFolGeo)
                pm.separator(h=25)

                with pm.rowColumnLayout(nc=2, co=(1, 'right', 7)):
                    pm.button(l='Apply', w=120, bgc=(0.65, 0.6, 0.77), c=partial(folSubRig, tslLoc))
                    pm.button(l='Reset', w=50, c=partial(resetUI, tslLoc))


