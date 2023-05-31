#-*- coding: utf-8 -*-
import maya.cmds as mc
import subprocess
import pymel.core as pm
import maya.mel as mel
import os, imp, sys


if mc.window('BinSkin_tools', exists=True):
    mc.deleteUI('BinSkin_tools')
    
    
def S_Geo(*arg):
    skingeo = mc.ls(sl=1)
    skingeo = skingeo[0]
    skingeoShape = mc.listRelatives(skingeo, s=1)
    skingeoShape = skingeoShape[0]
    
    skingeoSkin = mc.listConnections(skingeoShape+'.inMesh', type = 'skinCluster')
    skingeoSkin = skingeoSkin[0]
    global Bingeo
    Bingeo = skingeo
    global Binskin
    Binskin = skingeoSkin
    global Binjnt
    Binjnt = mc.listConnections(skingeoSkin+'.matrix')
    
    
def AL(*arg):
    for x in Binjnt:
        mc.setAttr(x+'.liw', 1)
    mel.eval('setToolTo $gSelect')
    mel.eval('ArtPaintSkinWeightsTool')
    
    
def AUL(*arg):
    for x in Binjnt:
        mc.setAttr(x+'.liw', 0)
    mel.eval('setToolTo $gSelect')
    mel.eval('ArtPaintSkinWeightsTool')


def JD(*arg):   
    mel.eval('setObjectPickMask "Surface" false;')
    mel.eval('setObjectPickMask "Curve" false;')
    mel.eval('setObjectPickMask "Joint" true;')
    mel.eval('setObjectPickMask "Marker" false;')
    mel.eval('setObjectPickMask "Deformer" false;')
    mel.eval('setObjectPickMask "Dynamic" false;')
    mel.eval('setObjectPickMask "Rendering" false;')
    mel.eval('setObjectPickMask "Other" false;')
    mel.eval('modelEditor -e -allObjects 0 modelPanel4;')
    mel.eval('modelEditor -e -j 1 modelPanel4;')
    mel.eval('setToolTo $gSelect')
    mc.select(Bingeo)


def SL(*arg):
    selBinjnt = mc.ls(sl=1)
    for x in selBinjnt:
        mc.setAttr(x+'.liw', 1)
    mc.select(Bingeo)
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('setObjectPickMask "Surface" true;')
    mel.eval('setObjectPickMask "Curve" true;')
    mel.eval('setObjectPickMask "Joint" true;')
    mel.eval('setObjectPickMask "Marker" false;')
    mel.eval('setObjectPickMask "Deformer" false;')
    mel.eval('setObjectPickMask "Dynamic" false;')
    mel.eval('setObjectPickMask "Rendering" false;')
    mel.eval('setObjectPickMask "Other" false;')
    mel.eval('modelEditor -e -allObjects 0 modelPanel4;')
    mel.eval('modelEditor -e -j 1 modelPanel4;')
    mel.eval('modelEditor -e -pm 1 modelPanel4;')
    mel.eval('modelEditor -e -nc 1 modelPanel4;')
    
    
def SUL(*arg):  
    selBinjnt = mc.ls(sl=1)
    for x in selBinjnt:
        mc.setAttr(x+'.liw', 0)
    mc.select(Bingeo)
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('setObjectPickMask "Surface" true;')
    mel.eval('setObjectPickMask "Curve" true;')
    mel.eval('setObjectPickMask "Joint" true;')
    mel.eval('setObjectPickMask "Marker" false;')
    mel.eval('setObjectPickMask "Deformer" false;')
    mel.eval('setObjectPickMask "Dynamic" false;')
    mel.eval('setObjectPickMask "Rendering" false;')
    mel.eval('setObjectPickMask "Other" false;')
    mel.eval('modelEditor -e -allObjects 0 modelPanel4;')
    mel.eval('modelEditor -e -j 1 modelPanel4;')
    mel.eval('modelEditor -e -pm 1 modelPanel4;')
    mel.eval('modelEditor -e -nc 1 modelPanel4;')


def SIV(*arg):  
    selBinjnt = mc.ls(sl=1)
    mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[0] + ' ' + Binskin+';')
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('setObjectPickMask "Surface" true;')
    mel.eval('setObjectPickMask "Curve" true;')
    mel.eval('setObjectPickMask "Joint" true;')
    mel.eval('setObjectPickMask "Marker" false;')
    mel.eval('setObjectPickMask "Deformer" false;')
    mel.eval('setObjectPickMask "Dynamic" false;')
    mel.eval('setObjectPickMask "Rendering" false;')
    mel.eval('setObjectPickMask "Other" false;')
    mel.eval('modelEditor -e -allObjects 0 modelPanel4;')
    mel.eval('modelEditor -e -j 1 modelPanel4;')
    mel.eval('modelEditor -e -pm 1 modelPanel4;')
    mel.eval('modelEditor -e -nc 1 modelPanel4;')


def SIV2(*arg): 
    selBinjnt = mc.ls(sl=1)
    y = len(selBinjnt)
    if y == 1:
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[0] + ' ' + Binskin+';')
    elif y == 2:
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[0] + ' ' + Binskin+';')
        S1 = mc.ls(sl=1, fl=1)
        s1 = set(S1)
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[1] + ' ' + Binskin+';')
        S2 = mc.ls(sl=1, fl=1)
        s2 = set(S2)
        mc.select(s1&s2)
    elif y == 3:
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[0] + ' ' + Binskin+';')
        S1 = mc.ls(sl=1, fl=1)
        s1 = set(S1)
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[1] + ' ' + Binskin+';')
        S2 = mc.ls(sl=1, fl=1)
        s2 = set(S2)
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[2] + ' ' + Binskin+';')
        S3 = mc.ls(sl=1, fl=1)
        s3 = set(S3)
        mc.select(s1&s2&s3)
    elif y == 4:
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[0] + ' ' + Binskin+';')
        S1 = mc.ls(sl=1, fl=1)
        s1 = set(S1)
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[1] + ' ' + Binskin+';')
        S2 = mc.ls(sl=1, fl=1)
        s2 = set(S2)
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[2] + ' ' + Binskin+';')
        S3 = mc.ls(sl=1, fl=1)
        s3 = set(S3)
        mel.eval('skinCluster -e -selectInfluenceVerts ' +selBinjnt[3] + ' ' + Binskin+';')
        S4 = mc.ls(sl=1, fl=1)
        s4 = set(S4)
        mc.select(s1&s2&s3&s4)
    else:
        print("you need select within 4 joints")
        
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('setObjectPickMask "Surface" true;')
    mel.eval('setObjectPickMask "Curve" true;')
    mel.eval('setObjectPickMask "Joint" true;')
    mel.eval('setObjectPickMask "Marker" false;')
    mel.eval('setObjectPickMask "Deformer" false;')
    mel.eval('setObjectPickMask "Dynamic" false;')
    mel.eval('setObjectPickMask "Rendering" false;')
    mel.eval('setObjectPickMask "Other" false;')
    mel.eval('modelEditor -e -allObjects 0 modelPanel4;')
    mel.eval('modelEditor -e -j 1 modelPanel4;')
    mel.eval('modelEditor -e -pm 1 modelPanel4;')
    mel.eval('modelEditor -e -nc 1 modelPanel4;')


def MD(*arg):
    mel.eval('setObjectPickMask "Surface" true;')
    mel.eval('setObjectPickMask "Curve" true;')
    mel.eval('setObjectPickMask "Joint" true;')
    mel.eval('setObjectPickMask "Marker" false;')
    mel.eval('setObjectPickMask "Deformer" false;')
    mel.eval('setObjectPickMask "Dynamic" false;')
    mel.eval('setObjectPickMask "Rendering" false;')
    mel.eval('setObjectPickMask "Other" false;')
    mel.eval('modelEditor -e -allObjects 0 modelPanel4;')
    mel.eval('modelEditor -e -j 1 modelPanel4;')
    mel.eval('modelEditor -e -pm 1 modelPanel4;')
    mel.eval('modelEditor -e -nc 1 modelPanel4;')
    mc.select(Bingeo)
    mel.eval('ArtPaintSkinWeightsTool')
        
        
def artflood(*arg):
    mel.eval('artAttrSkinPaintCtx -e -clear `currentCtx`;')


def P0(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 1 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 0 false artAttrSkinPaintCtx artAttrSkin;')


def P1(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 0.05 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')


def P2(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')
    
    
def P3(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 0.3 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')
    
    
def P4(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 0.5 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')


def P5(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 1 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')


def Re(*arg):
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Replace;')


def Sm(*arg):
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Smooth;')


def AvP0(*arg):
    mel.eval('artUserPaintCtx -e -opacity 0.1 `currentCtx`;')
    
    
def AvP1(*arg):
    mel.eval('artUserPaintCtx -e -opacity 1 `currentCtx`;')


def AvSm(*arg):
    
    path = '/home/jioh.kim/Desktop/pipe/wip/A/GSRigTool/util/plugin/averageVertexSkinWeight/'
    if path not in sys.path:
        sys.path.append(path)
    
    from util.plugin.averageVertexSkinWeight import averageVertexSkinWeightBrush
    imp.reload(averageVertexSkinWeightBrush)
    
    averageVertexSkinWeightBrush.paint()

    
mc.window('BinSkin_tools', s=True)
mc.columnLayout(columnAlign='center', rowSpacing=10)


mc.button(label='SelectSkinGeo',bgc=[0,0.9,0], h=30, w = 240, command = S_Geo)
mc.text (l='All lock/unlock')
mc.setParent('..')


mc.rowColumnLayout(numberOfColumns = 2)
mc.button(label='A_Lock',bgc=[0.3,0.3,0], h=30, w = 120, command = AL)
mc.button(label='A_UnLock',bgc=[1,1,0.2], h=30, w = 120, command = AUL)
mc.setParent('..')


mc.columnLayout(columnAlign='center', rowSpacing=10)
mc.separator( w=180, h=5)
mc.text ( l='Selected lock/unlock/influence')
mc.button(label='Display_Joint',bgc=[0.9,0.9,0.4], h=30, w = 240, command = JD)
mc.setParent('..')


mc.rowColumnLayout(numberOfColumns = 2)
mc.button(label='S_Lock',bgc=[0.3,0.3,0], h=30, w = 120, command = SL)
mc.button(label='S_UnLock',bgc=[1,1,0.2], h=30, w = 120, command = SUL)
mc.setParent('..')


mc.rowColumnLayout(numberOfColumns = 2)
mc.button(label='S_I_Vertex',bgc=[0.9,0.9,0.4], h=30, w = 120, command = SIV)
mc.button(label='S_I_Vertex_n',bgc=[0.9,0.9,0.4], h=30, w = 120, command = SIV2)
mc.setParent('..')


mc.columnLayout(columnAlign='center', rowSpacing=10)
mc.button(label='DisplayMesh',bgc=[0.9,0.9,0.4], h=20, w = 240, command = MD)
mc.separator( w=180, h=5)
mc.setParent('..')


mc.text ( l='paintWeight')
mc.setParent('..')
mc.columnLayout(columnAlign='center', rowSpacing=10)
mc.button(label='Flood',bgc=[1,0.3,0.3], h=30, w = 240, command = artflood)
mc.setParent('..')
mc.rowColumnLayout(numberOfColumns = 6)
mc.button(label='0',bgc=[0,0,0], h=30, w = 40, command = P0)
mc.button(label='0.05',bgc=[0.2,0.2,0.2], h=30, w = 40, command = P1)
mc.button(label='0.1',bgc=[0.4,0.4,0.4], h=30, w = 40, command = P2)
mc.button(label='0.3',bgc=[0.6,0.6,0.6], h=30, w = 40, command = P3)
mc.button(label='0.5',bgc=[0.8,0.8,0.8], h=30, w = 40, command = P4)
mc.button(label='1',bgc=[1,1,1], h=30, w = 40, command = P5)
mc.setParent('..')
mc.rowColumnLayout(numberOfColumns = 2)
mc.button(label='Replace',bgc=[0.9,0.9,0.4], h=30, w = 120, command = Re)
mc.button(label='Smooth',bgc=[0.9,0.9,0.4], h=30, w = 120, command = Sm)
mc.setParent('..')
mc.columnLayout(columnAlign='center', rowSpacing=10)
mc.button(label='AvgSmooth',bgc=[0.9,0.9,0.4], h=30, w = 240, command = AvSm)
mc.setParent('..')
mc.rowColumnLayout(numberOfColumns = 2)
mc.button(label='0.1',bgc=[0.25,0.25,0.25], h=30, w = 120, command = AvP0)
mc.button(label='1',bgc=[1,1,1], h=30, w = 120, command = AvP1)
mc.setParent('..')


mc.showWindow()

