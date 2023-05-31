#-*- coding: utf-8 -*-
import os, sys, imp, re
import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm


def AvSm():
    
    # path = '/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/util/plugin/averageVertexSkinWeight/'
    path = '/home/jioh.kim/maya/2023/plug-ins/averageVertexSkinWeight/'
    if path not in sys.path:
        sys.path.append(path)
    
    import averageVertexSkinWeightBrush
    imp.reload(averageVertexSkinWeightBrush)
    averageVertexSkinWeightBrush.paint()


def SmSkin():
    
    mel.eval('brSmoothWeightsToolCtx;')
    

def ngSkin():
    
    # path = '/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/ngskintools-2.0.22-win64.msi'
    import ngSkinTools2;
    ngSkinTools2.open_ui()
    
    
############################################################################### Commands


def sortScrollList_TEST():

    for x in pm.ls(sl=1):
        y = re.findall(r'\d+', x.name())
        print(y)
        aa = x.name().split(y[0])
        print(aa)


def CopySkinOneToOne(driver, driven):
    
    tslNewShape = driver
    tslOldShape = driven
    
    if len(tslNewShape) == len(tslOldShape):

        for i in range(len(tslNewShape)):
            
            GoodSkin = pm.listHistory(pm.PyNode(tslNewShape[i]), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
            GoodFindJntList = [x.name() for x in GoodSkin[0].getInfluence()]
            GoodBindJntlist = []
            
            if ':' in GoodFindJntList[0]:
                GoodBindJntlist = [x.split(':')[1] for x in GoodFindJntList]
            else:
                GoodBindJntlist = GoodFindJntList
                
            BadSkin = pm.listHistory(pm.PyNode(tslOldShape[i]), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
            if BadSkin:
                BadFindJntList = [x.name() for x in BadSkin[0].getInfluence()]

                if not set(GoodBindJntlist) == set(BadFindJntList):
                    for Gjnt in GoodBindJntlist:
                        if Gjnt in BadFindJntList:
                            continue
                        else:
                            try:
                                pm.skinCluster(tslOldShape[i], edit=1, ai=Gjnt, lw=1, dr=4, tsb=1)
                            except:
                                pass
                    pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
                    pm.displayInfo('AddJnt & Copy Skin: ' + tslNewShape[i] + ' >> ' + tslOldShape[i])
                    
                else:
                    pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
                    pm.displayInfo('Copy Skin: ' + tslNewShape[i] + ' >> ' + tslOldShape[i])
                    
            else:
                newJntList = [x for x in GoodBindJntlist if pm.objExists(x)]
                pm.skinCluster(newJntList, tslOldShape[i], tsb=1)
                BadSkin = pm.listHistory(pm.PyNode(tslOldShape[i]), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
                pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
                pm.displayInfo('Bind & Copy Skin: ' + tslNewShape[i] + ' >> ' + tslOldShape[i])
                
    else:
        pm.warning('Driver Index and Driven Index is Different')

    
def CopySkinOneToAll(driver, driven):
    
    tslNewShape = driver
    tslOldShape = driven

    GoodSkin = pm.listHistory(pm.PyNode(tslNewShape[0]), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
    GoodFindJntList = [x.name() for x in GoodSkin[0].getInfluence()]
    GoodBindJntlist = []

    if ':' in GoodFindJntList[0]:
        GoodBindJntlist = [x.split(':')[1] for x in GoodFindJntList]
    else:
        GoodBindJntlist = GoodFindJntList

    for changeObjs in tslOldShape:
        BadSkin = pm.listHistory(pm.PyNode(changeObjs), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')

        if BadSkin:
            BadFindJntList = [x.name() for x in BadSkin[0].getInfluence()]
            addJntList = [x for x in GoodBindJntlist if not (x in BadFindJntList) * (pm.objExists(x))]
            if addJntList:
                pm.skinCluster(changeObjs, edit=1, ai=addJntList, lw=1, dr=4, tsb=1)
            pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
            pm.displayInfo('Bind & Copy Skin: ' + tslNewShape[0] + ' >> ' + changeObjs)

        else:
            newJntList = [x for x in GoodBindJntlist if pm.objExists(x)]
            pm.skinCluster(GoodBindJntlist, changeObjs, tsb=1)
            BadSkin = pm.listHistory(pm.PyNode(changeObjs), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
            pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
            pm.displayInfo('Bind & Copy Skin: ' + tslNewShape[0] + ' >> ' + changeObjs)


def artToInteractive():

    # Normalize
            # EnableWeightNrm;
    mel.eval('''
            doNormalizeWeightsArgList 1 {"2"};
            ''')

    # Interactive
            # NormalizeWeights;
    mel.eval('''
            doNormalizeWeightsArgList 1 {"4"};
            ''')


def artToPost():
    
    # Post
            # EnableWeightPostNrm;
    mel.eval('''
            doNormalizeWeightsArgList 1 {"3"};
            ''')


def artflood(*arg):
    mel.eval('artAttrSkinPaintCtx -e -clear `currentCtx`;')
    
    
def Re(*arg):
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Replace;')


def Sm(*arg):
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Smooth;')
    
    
def P0(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 1.0 `currentCtx`;')
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
    
    
def AvP0(*arg):
    mel.eval('artSkinSetSelectionValue 0 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')
    
def AvP1(*arg):
    mel.eval('artSkinSetSelectionValue 0.1 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')
    

def AvP2(*arg):
    mel.eval('artSkinSetSelectionValue 0.25 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')

def AvP3(*arg):
    mel.eval('artSkinSetSelectionValue 0.5 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')

def AvP4(*arg):
    mel.eval('artSkinSetSelectionValue 0.75 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')

def AvP5(*arg):
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')



    
    