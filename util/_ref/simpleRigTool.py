import maya.cmds as mc
import subprocess
import pymel.core as pm
import maya.mel as mel
import os


# this is made and copyrighted by korean SANG BIN LEE
# You need "https://www.highend3d.com/maya/plugin/average-vertex-skin-weight-brush-for-maya" for last 3 command
# I'm finding a job now(2022/07). Rigging TA / CFX Artist / Character TD is good for me.
# my github : https://github.com/SANG-BIN-LEE
# my linkedin : https://www.linkedin.com/in/sangbin-lee-981a7215a
# my youtube : https://www.youtube.com/playlist?list=PLKIoBfXktlaalLuyrsqxT3QgzhQ-08yeE



if mc.window('BinSimpleRig_tools', exists=True):
    mc.deleteUI('BinSimpleRig_tools')
    
    
def Se_joint(*arg):
    jnt = []
    mc.select( hi = True )
    a = mc.ls ( sl = True)
    for x in a:
        if mc.nodeType(x) == 'joint':
            jnt.append(x)
    mc.select (jnt)


def Se_not_joint(*arg):
    jnt = []
    mc.select( hi = True )
    a = mc.ls ( sl = True)
    for x in a:
        if not mc.nodeType(x) == 'joint':
            jnt.append(x)
    mc.select (jnt)
    
    
def Se_crv(*arg):
    crv = []


    mc.select( hi = True )
    a = mc.ls ( sl = True)


    for x in a:
        if mc.nodeType(x) == 'nurbsCurve':
            crv.append(x)
   
    mc.select (crv)
    mc.pickWalk( direction='up' )
    
    
def Se_mesh(*arg):
    mesh = []


    mc.select( hi = True )
    a = mc.ls ( sl = True)


    for x in a:
        if mc.nodeType(x) == 'mesh':
            mesh.append(x)
   
    mc.select (mesh)
    mc.pickWalk( direction='up' )


def Se_shp(*arg):
    crv = []


    mc.select( hi = True )
    a = mc.ls ( sl = True)


    for x in a:
        if mc.nodeType(x) == 'nurbsCurve':
            crv.append(x)
   
    mc.select (crv)


def par_in_crv(*arg):
    crv = mc.ls(sl=1)
    incrv = []
    for x in crv:
        c_list = mc.listRelatives(x)
        for y in c_list:
            if not mc.nodeType(y) == 'nurbsCurve':
                incrv.append(y)
        mc.select(cl=1)
        mc.group(em=1, n ='ingrp_'+x)
        k = 'ingrp_'+x
        mc.connectAttr (x+'.rotatePivot', k+'.rotatePivot', f=1)
        mc.connectAttr (x+'.scalePivot', k+'.scalePivot', f=1)
        mc.disconnectAttr (x+'.rotatePivot', k+'.rotatePivot')
        mc.disconnectAttr (x+'.scalePivot', k+'.scalePivot')
        mc.parent(k,x, r=1)
    for y in incrv:
        mc.parent(y,k)


def Se_fol(*arg):
    fol = []


    mc.select( hi = True )
    a = mc.ls ( sl = True)


    for x in a:
        if mc.nodeType(x) == 'follicle':
            fol.append(x)
   
    mc.select (fol)
    mc.pickWalk( direction='up' )
    
    
def par_in_fol(*arg):
    fol = mc.ls(sl=1)
    infol = []
    for x in fol:
        c_list = mc.listRelatives(x)
        for y in c_list:
            if not mc.nodeType(y) == 'follicle':
                infol.append(y)
        mc.select(cl=1)
        mc.group(em=1, n ='ingrp_'+x)
        k = 'ingrp_'+x
        mc.connectAttr (x+'.rotatePivot', k+'.rotatePivot', f=1)
        mc.connectAttr (x+'.scalePivot', k+'.scalePivot', f=1)
        mc.disconnectAttr (x+'.rotatePivot', k+'.rotatePivot')
        mc.disconnectAttr (x+'.scalePivot', k+'.scalePivot')
        mc.parent(k,x, r=1)
    for y in infol:
        mc.parent(y,k)
        
        
def Se_constA(*arg):
    const = []


    mc.select( hi = True )
    a = mc.ls ( sl = True)


    for x in a:
        if mc.nodeType(x) == 'pointConstraint':
            const.append(x)
        if mc.nodeType(x) == 'orientConstraint':
            const.append(x)
        if mc.nodeType(x) == 'parentConstraint':
            const.append(x)
        if mc.nodeType(x) == 'scaleConstraint':
            const.append(x)
       
    mc.select (const)
    
    
def Se_constS(*arg):
    const = []


    mc.select( hi = True )
    a = mc.ls ( sl = True)


    for x in a:
        if mc.nodeType(x) == 'scaleConstraint':
            const.append(x)
       
    mc.select (const)


def sl_name(*arg):
    a = mc.ls(sl=True)
    print(a)
    
    
def m_trans(*arg):
    a = mc.ls( sl = True )


    for x in a:
        tx = mc.getAttr(x+'.tx')
        ty = mc.getAttr(x+'.ty')
        tz = mc.getAttr(x+'.tz')
        mc.select (cl = 1)
        mc.CreateEmptyGroup()
        k = mc.ls(sl=1)
        if 'c_' in x:
            t = x.split("c_")
            mc.rename(k, "cm_"+t[0]+t[1])
            y = "cm_"+t[0]+t[1]
        else:
            mc.rename(k, "m_"+x)
            y = "m_"+x
        if tx==0 and ty==0 and tz==0:
            mc.pointConstraint(y,x,n='tempPoconstrint', mo=0)
            tx = mc.getAttr(x+'.tx')
            ty = mc.getAttr(x+'.ty')
            tz = mc.getAttr(x+'.tz')
            mc.delete('tempPoconstrint')
            mc.select(x)
            mc.makeIdentity(apply=True, t=1, r=0, s=0, n=0, pn=1)
            mc.setAttr(x+'.tx', -tx)
            mc.setAttr(x+'.ty', -ty)
            mc.setAttr(x+'.tz', -tz)
        mc.parent(y,x)
        mc.setAttr(y+'.translateX', 0)
        mc.setAttr(y+'.translateY', 0)
        mc.setAttr(y+'.translateZ', 0)
        mc.setAttr(y+'.rotateX', 0)
        mc.setAttr(y+'.rotateY', 0)
        mc.setAttr(y+'.rotateZ', 0)
        mc.parent(y, w=1)
        mc.parent(x,y)
        mc.connectAttr (x+'.rotatePivot', y+'.rotatePivot')
        mc.connectAttr (x+'.scalePivot', y+'.scalePivot')
        mc.disconnectAttr (x+'.rotatePivot', y+'.rotatePivot')
        mc.disconnectAttr (x+'.scalePivot', y+'.scalePivot')    


def n_trans(*arg):
    a = mc.ls( sl = True )


    for x in a:
        mc.select (cl = 1)
        mc.CreateEmptyGroup()
        k = mc.ls(sl=1)
        mc.rename(k, "n_"+x)
        y = "n_"+x
        mc.connectAttr (x+'.rotatePivot', y+'.rotatePivot', f=1)
        mc.connectAttr (x+'.scalePivot', y+'.scalePivot', f=1)
        mc.disconnectAttr (x+'.rotatePivot', y+'.rotatePivot')
        mc.disconnectAttr (x+'.scalePivot', y+'.scalePivot')
        mc.parent(y,x, r=1, s=1)


def Se_hi(*arg):
    mc.select(hi=1)


def arc(*arg):
    mel.eval('arclen -ch 1;')
    
    
def m_crv(*arg):
    a = mc.ls( sl = True )


    for x in a:
        tx = mc.getAttr(x+'.tx')
        ty = mc.getAttr(x+'.ty')
        tz = mc.getAttr(x+'.tz')
        mc.select (cl = 1)
        mc.CreateEmptyGroup()
        k = mc.ls(sl=1)
        if 'c_' in x:
            t = x.split("c_")
            mc.rename(k, "cm_"+t[0]+t[1])
            y = "cm_"+t[0]+t[1]
        else:
            mc.rename(k, "m_"+x)
            y = "m_"+x
        if tx==0 and ty==0 and tz==0:
            mc.pointConstraint(y,x,n='tempPoconstrint', mo=0)
            tx = mc.getAttr(x+'.tx')
            ty = mc.getAttr(x+'.ty')
            tz = mc.getAttr(x+'.tz')
            mc.delete('tempPoconstrint')
            mc.select(x)
            mc.makeIdentity(apply=True, t=1, r=0, s=0, n=0, pn=1)
            mc.setAttr(x+'.tx', -tx)
            mc.setAttr(x+'.ty', -ty)
            mc.setAttr(x+'.tz', -tz)
        mc.parent(y,x)
        mc.setAttr(y+'.translateX', 0)
        mc.setAttr(y+'.translateY', 0)
        mc.setAttr(y+'.translateZ', 0)
        mc.setAttr(y+'.rotateX', 0)
        mc.setAttr(y+'.rotateY', 0)
        mc.setAttr(y+'.rotateZ', 0)
        mc.parent(y, w=1)
        mc.parent(x,y)
        mc.connectAttr (x+'.rotatePivot', y+'.rotatePivot')
        mc.connectAttr (x+'.scalePivot', y+'.scalePivot')
        mc.disconnectAttr (x+'.rotatePivot', y+'.rotatePivot')
        mc.disconnectAttr (x+'.scalePivot', y+'.scalePivot')
        mc.duplicate(x, n='tempX')
        mc.setAttr('tempX.scale', 1.15,1.15,1.15)
        mc.select('tempX')
        mel.eval('FreezeTransformations;')
        child = mc.listRelatives('tempX')
        sh = mc.listRelatives('tempX', s=1)
        dList = []
        for z in child:
            if not z in sh:
                dList.append(z)
        if dList:
            mc.delete(dList)
        for z in sh:
            mc.parent(z,y, r=1,s=1)
            mc.rename(z,y+'Shape')
        mc.delete('tempX')


def n_crv(*arg):
    a = mc.ls( sl = True )


    for x in a:
        mc.select (cl = 1)
        mc.duplicate(x, n='tempX')
        mc.setAttr('tempX.scale', 0.85,0.85,0.85)
        mc.select('tempX')
        mel.eval('FreezeTransformations;')
        child = mc.listRelatives('tempX')
        sh = mc.listRelatives('tempX', s=1)
        dList = []
        for z in child:
            if not z in sh:
                dList.append(z)
        if dList:
            mc.delete(dList)
        mc.CreateEmptyGroup()
        k = mc.ls(sl=1)
        mc.rename(k, "n_"+x)
        y = "n_"+x
        mc.connectAttr (x+'.rotatePivot', y+'.rotatePivot', f=1)
        mc.connectAttr (x+'.scalePivot', y+'.scalePivot', f=1)
        mc.disconnectAttr (x+'.rotatePivot', y+'.rotatePivot')
        mc.disconnectAttr (x+'.scalePivot', y+'.scalePivot')
        mc.parent(y,x, r=1, s=1)
        for z in sh:
            mc.parent(z,y, r=1,s=1)
            mc.rename(z,y+'Shape')
        mc.delete('tempX')


def SW(*arg):
    SwapList = mc.ls(sl=1)
    SwapTarget = SwapList[:-1]
    SwapSource = SwapList[-1]
    S_Sname = mc.listRelatives(SwapSource, s=1)
    
    for x in range(len(S_Sname)):
        mc.rename(S_Sname[x], SwapSource+'Shape'+str(x))


    for T_Tname in SwapTarget:
        T_Sname = mc.listRelatives(T_Tname, s=1)
        mc.delete(T_Sname)
        mc.duplicate(SwapSource, n = 'tempCRV')
        mc.rename('tempCRVShape', T_Tname+'Shape')
        mc.parent(T_Tname+'Shape', T_Tname, r=1, s=1)       
        mc.delete('tempCRV')


def S_add(*arg):
    AddList = mc.ls(sl=1)
    AddTarget = AddList[:-1]
    AddSource = AddList[-1]
    S_Sname = mc.listRelatives(AddSource, s=1)
    
    for x in range(len(S_Sname)):
        mc.rename(S_Sname[x], AddSource+'Shape'+str(x))


    for T_Tname in AddTarget:
        mc.duplicate(AddSource, n = 'tempCRV')
        mc.rename('tempCRVShape', T_Tname+'ShapeAdd')
        mc.parent(T_Tname+'ShapeAdd', T_Tname, r=1, s=1)        
        mc.delete('tempCRV')


def SelectedCurvNaming(*arg):
    sel=mc.ls(sl=1)
    S_crv='Shape'
    for o in sel:
        history = mc.listRelatives( s=1 )
        if history != None:
            for x in history:
                if mc.nodeType( x ) == "nurbsCurve":
                    mc.rename(x, o + S_crv)


mc.window('BinSimpleRig_tools', s=True)
mc.columnLayout(columnAlign='center', rowSpacing=10)


mc.text (l='Selection', w=240)
mc.setParent('..')


mc.rowColumnLayout(numberOfColumns = 6)
mc.button(label='Hi',bgc=[0,0.6,0], h=30, w = 40, command = Se_hi)
mc.button(label='JNT',bgc=[0.5,0.5,0.8], h=30, w = 40, command = Se_joint)
mc.button(label='CRV',bgc=[0.2,0.8,1], h=30, w = 40, command = Se_crv)
mc.button(label='C_A',bgc=[1,0,0], h=30, w = 40, command = Se_constA)
mc.button(label='SHP',bgc=[0.2,0.6,1], h=30, w = 40, command = Se_shp)
mc.button(label='FOL',bgc=[1,0.5,0], h=30, w = 40, command = Se_fol)


mc.setParent('..')
mc.rowColumnLayout(numberOfColumns = 6)
mc.button(label='arclen',bgc=[0,0,0], h=30, w = 40, command = arc)
mc.button(label='JNT',bgc=[0.2,0.2,0.5], h=30, w = 40, command = Se_not_joint)
mc.button(label='Mesh',bgc=[0,0,0.5], h=30, w = 40, command = Se_mesh)
mc.button(label='C_S',bgc=[0.5,0,0], h=30, w = 40, command = Se_constS)
mc.button(label='pCRV',bgc=[0,0,0], h=30, w = 40, command = par_in_crv)
mc.button(label='pFOL',bgc=[0,0,0], h=30, w = 40, command = par_in_fol)
mc.setParent('..')


mc.columnLayout(columnAlign='center', rowSpacing=10)
mc.text ( l='SelectionInverse', w=240)
mc.separator( w=180, h=5)
mc.button(label='L i s t', h=30, w = 240, command = sl_name)
mc.setParent('..')


mc.rowColumnLayout(numberOfColumns = 2)
mc.button(label='M_', h=30, w = 120, command = m_trans)
mc.button(label='N_', h=30, w = 120, command = n_trans)
mc.setParent('..')


mc.columnLayout(columnAlign='center', rowSpacing=10)
mc.text ( l='Curve', w=240)
mc.setParent('..')


mc.rowColumnLayout(numberOfColumns = 2)
mc.button(label='crv_M', h=30, w = 120, command = m_crv)
mc.button(label='crv_N', h=30, w = 120, command = n_crv)
mc.button(label='CRV Swap', h=30, w = 120, command = SW)
mc.button(label='CRV Add', h=30, w = 120, command = S_add)
mc.setParent('..')


mc.columnLayout(columnAlign='center', rowSpacing=10)
mc.button(label='Selected CRV Naming', h=30, w = 240, command = SelectedCurvNaming)


mc.showWindow()


