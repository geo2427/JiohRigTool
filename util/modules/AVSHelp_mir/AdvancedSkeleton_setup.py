#20221028 edited by SANG BIN LEE

from operator import mod
import pymel.core as pm
import maya.cmds as mc


#--- list of curve shape changing ---#
rotCtlList = ['FKNeck1_M', 'FKNeck0_M']
#--- list of will be changed rotate value of the offset groups ---#
rotList = ['FKRoot_M', 'FKSpine1_M', 'FKSpine2_M', 'FKSpine3_M', 'FKChest_M']
headRotateOrderList = ['FKHead_M','FKNeck1_M','FKNeck0_M']


fkShoulderFollowList = ['FollowShoulder_L', 'FollowShoulder_R']

#--- list of ik arm controls' follow targets ('Scapula' is default targets so no need to add)---#

IkArmFollowList = ['RootX_M', 'Head_M', 'Chest_M'] #20221028 edited - Root_M =>RootX_M
IkArmFollowTargets = ['IKOffsetArm_LStatic', 'IKOffsetArm_RStatic']
IkArmFollowConst = ['IKOffsetArm_L', 'IKOffsetArm_R']
IkArmOriParents = ['FKOffsetShoulder_L', 'FKOffsetShoulder_R']

#--- Main Cotroller / World Controller's name assign ---#
Main = 'Main'
World = 'World'
Root = 'RootX_M'
HipSwinger = 'HipSwinger_M' #20221028 edited

SpineIKH = 'IKSpineHandle_M'

# --- for ikTransCTL command ---#
IKRoot = ('IKXShoulder_L', 'IKXShoulder_R', 'IKXHip_L', 'IKXHip_R')
IKctrlList = ('IKArm_L', 'IKArm_R', 'IKLeg_L', 'IKLeg_R')

#20221028 edited - change funtionOrder
##########################################################
############ ---- spine control shape fix ----############
##########################################################
## --- Change Center CTLs rotation ---##
#--- Change its shape only to 90 degrees in z Axis ---#
def centerCtlRot(List):
    for a in List:
        aShp = pm.listRelatives(a, s=1)[0]
        pm.rotate(aShp.cv[:], 0, 0, 90, r=1, os=1, fo=1)

def centerCtlRot_reverse(List):
    for a in List:
        aShp = pm.listRelatives(a, s=1)[0]
        pm.rotate(aShp.cv[:], 0, 0, -90, r=1, os=1, fo=1)

#--- Change its offset group's rotate values ---#
def spineOrientRot(List):
    for a in List:
        aPrnt = pm.listRelatives(a, p=1, type='transform')[0] #ExtraGRP
        aGPrnt = pm.listRelatives(aPrnt, p=1, type='transform')[0] #offGRP
        aChldrn = pm.listRelatives(a, c=1, type='transform') #JNT+extra
        
        aFixGRP = pm.group(em=1, n = aChldrn[0].replace('FK', 'FKFix')) #FixGRP
        pm.matchTransform(aFixGRP, aGPrnt)
        pm.parent(aFixGRP, aGPrnt)
        pm.parent(aChldrn, aFixGRP)
        
        aPrnt.rotateX.set(-90)
        aPrnt.rotateY.set(-90)
        pm.parent(aFixGRP, a)

#--- Change its offset group's rotate values to origin ---#
def spineOrientRot_reverse(List):
    for a in List:
        # aPrnt = pm.listRelatives(a, p=1)[0] #Extra
        # aGPrnt = pm.listRelatives(aPrnt, p=1)[0] #offGRP
        # aFixGRP = pm.listRelatives(a, c=1)[0] #FixGRP
        # aChldrn = aFixGRP.listRelatives(c=1,type='transform') #JNT+extra

        # pm.parent(aChldrn, aGPrnt)
        # pm.delete(aFixGRP)
        # aPrnt.rotateX.set(0)
        # aPrnt.rotateY.set(0)
        # pm.parent(aChldrn, a)
        
        aPrnt = pm.listRelatives(a, p=1, type='transform')[0] #Extra
        aGPrnt = pm.listRelatives(aPrnt, p=1, type='transform')[0] #offGRP
        aFixGRP = pm.listRelatives(a, c=1, type='transform')[0] #FixGRP
        aChldrn = aFixGRP.listRelatives(c=1, type='transform') #JNT+extra

        pm.parent(aFixGRP, aGPrnt)
        aPrnt.rotateX.set(0)
        aPrnt.rotateY.set(0)
        
        pm.parent(aChldrn, a)
        pm.delete(aFixGRP)

#--- create Neck CTL, Head CTL ---# 20221028 edited (added)
def createAndChange_Neck0_CTL():
    pointTuple = ([0.8688758948095611, -3.907985046680551e-14, -1.1731017506250592], 
                  [1.3791441845219611e-14, -3.5527136788004994e-15, -1.821589375587486], 
                  [-0.8688758948095463, -3.907985046680551e-14, -1.1731017506250438], 
                  [-1.3906246703447254, 0.532186685750067, -0.11121956958123701], 
                  [-0.98332013449844, -1.7763568394002505e-15, 0.9506626114625607], 
                  [-1.0162927942596152e-14, -1.7763568394002524e-15, 1.39050861247433], 
                  [0.9833201344984233, -1.776356839400253e-15, 0.9506626114625465], 
                  [1.3906246703447251, 0.5321866857500683, -0.11121956958125966])
    pm.select(cl=1)
    neck0Ctl = pm.curve(n='FKNeck0_M1', d=3, p=pointTuple)
    neck0CtlShp = pm.listRelatives(neck0Ctl, s=1)[0]
    pm.closeCurve(neck0Ctl, ch=0, ps=0, rpo=1, bb=0.5, bki=0, p=0.1)
    neck0CtlShp.overrideEnabled.set(1)
    neck0CtlShp.overrideColor.set(18)

    CTL = 'FKNeck0_M'
    CTL_shape = pm.listRelatives(CTL, s=1)[0]
    pm.delete(CTL_shape)
    pm.parent(neck0CtlShp, CTL, r=1, s=1)
    pm.delete(neck0Ctl)
    mc.rename(str(neck0CtlShp), str(CTL_shape))

def createAndChange_Neck1_CTL():
    pointTuple = ([0.6808782209244918, -1.7763568394002503e-15, -1.001751895293739], 
                  [1.4155343563970746e-15, -1.7763568394002503e-15, -1.6505820078777163], 
                  [-0.6808782209244821, -1.7763568394002505e-15, -1.0017518952937337], 
                  [-1.0800233803649935, 0.3133039327957632, -0.23806003918801977], 
                  [-0.7636918561057164, -1.7763568394002505e-15, 0.5256318169176947], 
                  [-3.6914915568786455e-15, -1.77635683940025e-15, 0.8419633411769729], 
                  [0.7636918561057131, -1.77635683940025e-15, 0.525631816917692], 
                  [1.0800233803649943, 0.3133039327957641, -0.238060039188023])
    pm.select(cl=1)
    neck1Ctl = pm.curve(n='FKNeck0_M1', d=3, p=pointTuple)
    neck1CtlShp = pm.listRelatives(neck1Ctl, s=1)[0]
    pm.closeCurve(neck1Ctl, ch=0, ps=0, rpo=1, bb=0.5, bki=0, p=0.1)
    neck1CtlShp.overrideEnabled.set(1)
    neck1CtlShp.overrideColor.set(18)

    CTL = 'FKNeck1_M'
    CTL_shape = pm.listRelatives(CTL, s=1)[0]
    pm.delete(CTL_shape)
    pm.parent(neck1CtlShp, CTL, r=1, s=1)
    pm.delete(neck1Ctl)
    mc.rename(str(neck1CtlShp), str(CTL_shape))

def createAndChange_Head_CTL():
    pointTuple = ([0.8681892512761962, 1.6563899092776453, -0.6285825240913313], 
                  [2.661517544896219e-10, 1.6563899092776453, -0.8853502598873165],
                  [-0.8681892512761816, 1.6563899092776444, -0.6285825240913313],
                  [-1.0975528097316591, 0.4423766662972387, -0.008690374605471039],
                  [-0.733735641173711, -0.5918153217460878, 0.5277102936973374],
                  [2.661517544896219e-10, -0.909355891323457, 1.3052341985297746],
                  [0.7337356411737279, -0.5918153217460871, 0.5277102936973374],
                  [1.0975528097316758, 0.4423766662972397, -0.008690374605470296])
    pm.select(cl=1)
    headCtl = pm.curve(n='FKHead_M1', d=3, p=pointTuple)
    headCtlShp = pm.listRelatives(headCtl, s=1)[0]
    pm.closeCurve(headCtl, ch=0, ps=0, rpo=1, bb=0.5, bki=0, p=0.1)
    headCtlShp.overrideEnabled.set(1)
    headCtlShp.overrideColor.set(18)
    
    CTL = 'FKHead_M'
    CTL_shape = pm.listRelatives(CTL, s=1)[0]
    pm.delete(CTL_shape)
    pm.parent(headCtlShp, CTL, r=1, s=1)
    pm.delete(headCtl)
    mc.rename(str(headCtlShp), str(CTL_shape))

def headRotateOrderFix(RotateOrderList):
    for x in RotateOrderList:
        pm.setAttr("{}.rotateOrder".format(x), 3)

def headRotateOrderRollBack(RotateOrderList):
    for x in RotateOrderList:
        pm.setAttr("{}.rotateOrder".format(x), 5)

####--- Definitions for UI execute buttons ---####
#--- center controls rotate edit ---# 20221028 edited (added)
def rotSpine():
    spineOrientRot(rotList)
    centerCtlRot(rotList)
    createAndChange_Neck0_CTL()
    createAndChange_Neck1_CTL()
    createAndChange_Head_CTL()
    headRotateOrderFix(headRotateOrderList)

def rotSpine_rollBack():
    headRotateOrderRollBack(headRotateOrderList)
    centerCtlRot_reverse(rotList)
    spineOrientRot_reverse(rotList)

#####################################################
############ ---- mirror ik Controls ----############
######################################################
#### 20221028_IKsubCTL is added####

#--- making offset groups of each ---#
def offGRP(Sel, Suffix):
    offGrpList = []
    for a in Sel:
        aParent = pm.listRelatives(a, p=1)
        if aParent == []:
            GRP = pm.group(em=1, n='{}_{}'.format(a, Suffix))
        else:
            GRP = pm.group(em=1, n='{}_{}'.format(a, Suffix), parent=aParent[0])

        pos = pm.xform(a, q=1, m=1, ws=1)
        pm.xform(GRP, m=pos, ws=1)
        pm.parent(a, GRP)
        offGrpList.append(GRP)
    return offGrpList

# --- Scapula_L CTRL reverse --- NOW : not considering shapeORG Connections // only Y rotate # 20221028 edited (added)
def reverseShape(ctrl):
    temp = pm.duplicate(ctrl, rc=1)[0]
    org_shape = pm.listRelatives(ctrl, c=1,s=1)[0]
    mod_shape = pm.listRelatives(temp, c=1,s=1)[0]
    org_shapeName = str(org_shape)
    mod_shapeName = str(mod_shape)
    temp.ry.set(180)
    temp.sy.set(-1) #20221104 added
    pm.makeIdentity(temp, apply=1, t=1, r=1, s=1, n=0, pn=1)
    pm.delete(org_shape)
    pm.parent(mod_shape, ctrl, r=1,s=1)
    pm.rename(mod_shapeName,org_shapeName)
    pm.delete(temp)

#--- parent ikCtrls to its parent offset group that just made ---#
def mirrorIkCtrl(Sel):
    Dic = {'mirror': [], 'ikCtrl': [], 'children': [], 'parent': []}
    for a in Sel:
        Prnt = pm.listRelatives(a, p=1, type='transform')[0]
        Child = pm.listRelatives(a, c=1, type='transform')

        offGrp = offGRP([a], 'mirrorGRP')[0]
        pm.parent(Child, Prnt)

        Dic['mirror'].append(offGrp)
        Dic['ikCtrl'].append(a)
        Dic['children'].append(Child)
        Dic['parent'].append(Prnt)

    return Dic


####--- Definitions for UI execute buttons ---####
#--- set the attribute values for mirror setting ---#
def mirrorSetup(IkCTL):
    # --- mirror ik Controls ---#
    mirrorGRP = mirrorIkCtrl(IkCTL)
    mirrorGRP['mirror'][0].rotateX.set(180)
    mirrorGRP['mirror'][0].scaleX.set(-1)

    mirrorGRP['mirror'][1].scaleX.set(-1)

    mirrorGRP['mirror'][2].rotateY.set(180)
    mirrorGRP['mirror'][2].scaleZ.set(-1)

    mirrorGRP['mirror'][3].rotateY.set(180)
    mirrorGRP['mirror'][3].scaleZ.set(-1)
    
    #20221028 edited
    #R_toes Roll inside even reverse
    REV = pm.group(em=1, n='RollToes_R_reverseGRP')
    pm.matchTransform('RollToes_R_reverseGRP', 'RollToes_R')
    pm.parent(REV, mirrorGRP['ikCtrl'][3])
    REV.rotateY.set(180)
    REV.scaleZ.set(-1)
    
    mirrorGRP['mirror'][4].rotateY.set(180)
    mirrorGRP['mirror'][4].scaleZ.set(-1)

    mirrorGRP['mirror'][5].rotateX.set(180)
    mirrorGRP['mirror'][5].scaleX.set(-1)

    [pm.parent(mirrorGRP['children'][a], mirrorGRP['ikCtrl'][a]) for a in range(len(IkCTL))]
    
    #20221028 edited
    #R_toes Roll inside even reverse
    pm.parent(mirrorGRP['children'][3], REV)
    #FKXScapula_L revesre transform name
    pm.rename(pm.listRelatives('FKXScapula_L', p=1, type='transform')[0], 'FKXScapula_L_reverseGRP')
    reverseShape('FKScapula_L')

    return mirrorGRP

#--- rolling back the mirror setting ---#
def rollBack(IkCTL):
    # --- rollback ---#
    for a in IkCTL:
        prnt = pm.listRelatives(a, p=1)[0]
        if 'mirrorGRP' in prnt[:]:
            
            #MAIN COMMAND
            children = pm.listRelatives(a, c=1, type='transform')
            grandPrnt = pm.listRelatives(prnt, p=1)[0]
            pm.parent(children, grandPrnt)

            prnt.rotateX.set(0)
            prnt.rotateY.set(0)
            prnt.rotateZ.set(0)
            prnt.scaleX.set(1)
            prnt.scaleY.set(1)
            prnt.scaleZ.set(1)

            pm.parent(children, a)
            pm.parent(a, grandPrnt)

            pm.delete(prnt)

            #20221031 edited
            # toes exception
            if a == 'RollToes_R':
                REV = pm.listRelatives('RollToes_R', c=1, type='transform')[0]
                reverse_children = pm.listRelatives(REV, c=1, type='transform')
                reverse_parent = pm.listRelatives(REV, p=1, type='transform')[0]
                pm.parent(reverse_children, reverse_parent)
                pm.delete(REV)
            
            #20221028 edited
            #Scapula_L exception
            if a == 'FKScapula_L':
                if mc.listRelatives('FKXScapula_L', p=1, type='transform')[0] == u'FKXScapula_L_reverseGRP':
                    child = pm.listRelatives('FKXScapula_L_reverseGRP', c=1)
                    pm.parent(child, 'FKScapula_L')
                    pm.delete('FKXScapula_L_reverseGRP')
                    reverseShape('FKScapula_L')

        else:
            print ( 'no mirror setup' )

##########################################################
##################### edit follow options ################ Arm
##########################################################

##--- Change ik arm Controls' follow option ---##
def ikArmFollow(CtlList, FollowList, FollowTargets, ConstGrp):
    for a in range(len(CtlList)):
        Const = pm.listConnections('{}.parentInverseMatrix'.format(IkArmFollowConst[a]), type='constraint')[0]
        Side = CtlList[a].split('_')[-1]

        rootStatic = pm.duplicate(FollowTargets[a], n=FollowTargets[a] + '_Root')
        headStatic = pm.duplicate(FollowTargets[a], n=FollowTargets[a] + '_Head')
        chestStatic = pm.duplicate(FollowTargets[a], n=FollowTargets[a] + '_Chest')

        pm.parentConstraint(FollowList[0], rootStatic, mo=1)
        pm.parentConstraint(FollowList[1], headStatic, mo=1)
        pm.parentConstraint(FollowList[2], chestStatic, mo=1)

        pm.parentConstraint(rootStatic, headStatic, chestStatic, ConstGrp[a])

        pm.deleteAttr(CtlList[a], attribute="follow")
        pm.addAttr(CtlList[a], ln='follow', at='enum', en='Scapula:Head:Chest:Root:World', k=1)
        pm.setAttr('{}.follow'.format(CtlList[a]), k=1)

        Cond0 = pm.createNode('condition', n='{}_Follow_0_COND'.format(CtlList[a]))
        Cond1 = pm.createNode('condition', n='{}_Follow_1_COND'.format(CtlList[a]))
        Cond2 = pm.createNode('condition', n='{}_Follow_2_COND'.format(CtlList[a]))
        Cond3 = pm.createNode('condition', n='{}_Follow_3_COND'.format(CtlList[a]))
        Cond4 = pm.createNode('condition', n='{}_Follow_4_COND'.format(CtlList[a]))

        Ctl = pm.ls(CtlList[a])[0]
        Ctl.follow >> Cond0.firstTerm
        Ctl.follow >> Cond1.firstTerm
        Ctl.follow >> Cond2.firstTerm
        Ctl.follow >> Cond3.firstTerm
        Ctl.follow >> Cond4.firstTerm

        Cond0.colorIfTrueR.set(1)
        Cond0.colorIfFalseR.set(0)

        Cond1.colorIfTrueR.set(1)
        Cond1.colorIfFalseR.set(0)
        Cond1.secondTerm.set(1)

        Cond2.colorIfTrueR.set(1)
        Cond2.colorIfFalseR.set(0)
        Cond2.secondTerm.set(2)

        Cond3.colorIfTrueR.set(1)
        Cond3.colorIfFalseR.set(0)
        Cond3.secondTerm.set(3)

        Cond4.colorIfTrueR.set(1)
        Cond4.colorIfFalseR.set(0)
        Cond4.secondTerm.set(4)

        Cond0.outColorR >> '{}.IKOffsetArm_{}FollowW1'.format(Const, Side)
        Cond1.outColorR >> '{}.IKOffsetArm_{}Static_HeadW3'.format(Const, Side)
        Cond2.outColorR >> '{}.IKOffsetArm_{}Static_ChestW4'.format(Const, Side)
        Cond3.outColorR >> '{}.IKOffsetArm_{}Static_RootW2'.format(Const, Side)
        Cond4.outColorR >> '{}.IKOffsetArm_{}StaticW0'.format(Const, Side)

#--- finding original setrange ---#
def OriSetRangeExists(Name):
    if pm.objExists(Name):
        return pm.PyNode(Name) #20221031 error Fix
    else:
        srng = pm.createNode('setRange', n=Name)
        srng.minY.set(1)
        srng.maxX.set(1)
        srng.oldMaxX.set(10)
        srng.oldMaxY.set(10)
        return srng #20221031 error Fix

#--- rollback ik Follow option ---#
def ikArmFollowRollBack(CtlList, FollowTargets):
    for a in range(len(CtlList)):
        Const = pm.listConnections('{}.parentInverseMatrix'.format(IkArmFollowConst[a]), type='constraint')[0]
        Side = CtlList[a].split('_')[-1]
        OriCnts = OriSetRangeExists('IKArm_{}SetRangeFollow'.format(Side))
        Ctl = pm.ls(CtlList[a])[0]

        rootStatic = pm.ls(FollowTargets[a] + '_Root')
        headStatic = pm.ls(FollowTargets[a] + '_Head')
        chestStatic = pm.ls(FollowTargets[a] + '_Chest')

        pm.delete(rootStatic, headStatic, chestStatic)

        pm.deleteAttr(Ctl, attribute="follow")
        pm.addAttr(Ctl, ln='follow', at='float', min=0, max=10, k=1)
        pm.setAttr('{}.follow'.format(Ctl), k=1)

        Ctl.follow >> OriCnts.valueX
        Ctl.follow >> OriCnts.valueY

        Cond0 = pm.ls('{}_Follow_0_COND'.format(Ctl))
        Cond1 = pm.ls('{}_Follow_1_COND'.format(Ctl))
        Cond2 = pm.ls('{}_Follow_2_COND'.format(Ctl))
        Cond3 = pm.ls('{}_Follow_3_COND'.format(Ctl))
        Cond4 = pm.ls('{}_Follow_4_COND'.format(Ctl))

        pm.delete(Cond0, Cond1, Cond2, Cond3, Cond4)

        OriCnts.outValueX >> '{}.IKOffsetArm_{}FollowW1'.format(Const, Side)
        OriCnts.outValueY >> '{}.IKOffsetArm_{}StaticW0'.format(Const, Side)

## --- Change FK Shoulder follow setup ---##
#--- Change the target of orient Constraint to main CTL ---#
def fkShoulderFollow(List, Main):
    for a in List:
        OriConst = pm.listConnections('{}.parentInverseMatrix'.format(a), type='constraint')[0]
        pm.delete(OriConst)
        pm.orientConstraint(Main, a, mo=1)

#--- Change the target of orient Constraint to deafualt (Chest) target ---#
def fkShoulderFollowRollBack(List):
    for a in List:
        OriConst = pm.listConnections('{}.parentInverseMatrix'.format(a), type='constraint')[0]
        pm.delete(OriConst)
        pm.orientConstraint('Chest_M', a, mo=1)

####--- Definitions for UI execute buttons ---####
#--- ik arm follow options change ---#
def editFollow(IkArmCtl, Main):
    ikArmFollow(IkArmCtl, IkArmFollowList, IkArmFollowTargets, IkArmFollowConst)
    fkShoulderFollow(fkShoulderFollowList, Main)

def editFollowRollBack(IkArmCtl):
    ikArmFollowRollBack(IkArmCtl, IkArmFollowTargets)
    fkShoulderFollowRollBack(fkShoulderFollowList)

##########################################################
##################### edit follow options ################ leg
##########################################################

##--- Change ik arm Controls' follow option ---##
def ikLegFallow(controller, followList):
    enumList = ["World:Root:Pelvis"]
    controller = pm.PyNode(controller)
    
    pm.addAttr(controller, ln='follow', at='enum', en=enumList, k=1)
    
    side = controller.split('_')[-1]
    offset = pm.PyNode('IKOffsetLeg_{}'.format(side))
    
    for x in range(len(followList)):
        const = pm.parentConstraint(followList[x], offset, mo=1)
        condition = pm.createNode('condition', n = '{}_to_{}_condition'.format(controller, followList[x]))
        controller.follow>>condition.firstTerm
        condition.secondTerm.set(x)
        condition.colorIfTrueR.set(1)
        condition.colorIfFalseR.set(0)
        
        weight = [w for w in pm.listAttr(const, m=1) if 'W'+str(x) in w][0]
        
        pm.connectAttr('{}.outColorR'.format(condition), '{}.{}'.format(const, weight))
            
def deleteFollow(controller):
    side = controller.split('_')[-1]
    offset = 'IKOffsetLeg_{}'.format(side)
    pm.deleteAttr(controller, at='follow')
    const = pm.listConnections('{}.parentInverseMatrix'.format(offset), type='constraint')[0]
    if pm.objExists(const):
        pm.delete(const)
    
####--- Definitions for UI execute buttons ---####
#--- ik leg follow options change ---#

def editLegFollow():
    legSide = ['L', 'R']
    for lr in legSide:
        controller = 'IKLeg_{}'.format(lr)
        legFallowList = ['World', 'RootX_M', 'Root_M']
        ikLegFallow(controller, legFallowList)
    
def editLegFollowRollBack():
    legSide = ['L', 'R']
    for lr in legSide:
        controller = 'IKLeg_{}'.format(lr)
        deleteFollow(controller)
       
#########################################################
##################### add main control ##################
#########################################################
## --- change connections between main CTL & Groups ---##
#--- Create a main Control for curve shape---#
def createMainCtl(Name):
    mainCtl = pm.curve(n=Name, d=3, p=([2.537816701040911, 0.002442294850725167, -2.5380324880347036],
                                       [-4.094636743949884e-16, 0.002442294850725186, -3.5892305844227983],
                                       [-2.537816701040911, 0.002442294850725167, -2.5380324880347036],
                                       [-3.589014797429009, 0.002442294850725112, -0.00021578699379121784],
                                       [-2.688265080130336, 0.002442294850725074, 2.1743863968123938],
                                       [-1.3722810870597535, 0.0024422948507250588, 3.0002883215588296],
                                       [-0.6463858784437456, 0.0024422948507250544, 3.1969052309404065],
                                       [-0.17401882757282375, 0.0024422948507250544, 3.4327100802313417],
                                       [-0.014180722362863413, 0.0024422948507250544, 3.8104691078712047],
                                       [0.17881032135486344, 0.0024422948507250544, 3.420657738688963],
                                       [0.5598239079634361, 0.0024422948507250544, 3.2117043866002324],
                                       [1.317027873329351, 0.0024422948507250588, 3.0288956709438977],
                                       [2.662061383032138, 0.0024422948507250722, 2.2376477177311633],
                                       [3.589014797429009, 0.002442294850725112, -0.00021578699378822737]))
    mainCtlShp = pm.listRelatives(mainCtl, s=1)[0]
    pm.closeCurve(mainCtl, ch=0, ps=0, rpo=1, bb=0.5, bki=0, p=0.1)
    mainCtlShp.overrideEnabled.set(1)
    mainCtlShp.overrideColor.set(13)
    return mainCtl

#--- Create a world Control ---#
def createWorldCtl(World):
    worldCtl = pm.circle(n=World, r=3, ch=0, nr=(0, 1, 0))
    worldCtlShp = pm.listRelatives(worldCtl, s=1)[0]
    worldCtlShp.overrideEnabled.set(1)
    worldCtlShp.overrideColor.set(17)
    return worldCtl

# --- for rollback Main restore main shape ---- #
def createMainOrigShapeCtl():
    mainCtl = pm.circle(r=3.3, ch=0, nr=(0, 1, 0))
    mainCtlShp = pm.listRelatives(mainCtl, s=1)[0]
    pm.parent(mainCtlShp, 'Main', r=1, s=1)
    mainCtlShp.overrideEnabled.set(1)
    mainCtlShp.overrideColor.set(29)
    pm.rename(mainCtlShp, 'MainShape')
    pm.delete(mainCtl)
    
#--- Change the Scale related connections from main CTL to world CTL ---#
def changeScale(From, To):
    scaleInfo = pm.listConnections('{}.scale'.format(From), p=1, type='multiplyDivide')
    scaleMULT = pm.createNode('multiplyDivide', n='main_world_MULT')

    FromNode = pm.ls(From)[0]
    ToNode = pm.ls(To)[0]
    FromNode.scale >> scaleMULT.input1
    ToNode.scale >> scaleMULT.input2
    scaleMULT.output >> scaleInfo[0]

#--- Change main CTL's curve shape ---#
def changeShp(From, To):
    mainCtl = createMainCtl(From[0])
    mainCtlShp = pm.listRelatives(mainCtl, s=1)[0]
    MainShp = pm.listRelatives(From, s=1)

    pm.delete(MainShp)
    pm.parent(mainCtlShp, From, r=1, s=1)
    pm.parent(To, From)
    pm.delete(mainCtl)

#--- Change Constraint connections from main CTL to world CTL ---#
def changeConst(From, To):
    transConstInfo = pm.listConnections('{}.translate'.format(From), type='constraint')
    constTgtList = [pm.listConnections('{}.constraintTranslateX'.format(transConstInfo[a]), type='transform') for a in
                    range(len(transConstInfo))]

    prntConst = [pm.parentConstraint(To, constTgtList[a][0], mo=1) for a in range(len(constTgtList))]
    scaleConst = [pm.scaleConstraint(To, constTgtList[a][0], mo=1) for a in range(len(constTgtList))]

    cntListPrnt = [pm.listConnections(prntConst[a].target, c=1, p=1) for a in range(len(prntConst))]
    cntListScale = [pm.listConnections(scaleConst[a].target, c=1, p=1) for a in range(len(scaleConst))]

    prntDic = {'to': [], 'from': []}
    for a in cntListPrnt:
        for b in a:
            if b[1].split('.')[0] == From:
                prntDic['to'].append(b[0])
                prntDic['from'].append(b[1])

    scaleDic = {'to': [], 'from': []}
    for a in cntListScale:
        for b in a:
            if b[1].split('.')[0] == From:
                prntDic['to'].append(b[0])
                prntDic['from'].append(b[1])

    for a in range(len(prntDic['to'])):
        prntDic['from'][a] // prntDic['to'][a]

    for a in range(len(scaleDic['to'])):
        scaleDic['from'][a] // scaleDic['to'][a]

## --- Add Extra centered shape to any Ctl ---#
#20221028 function all.. is edited 
def addCenterShape(RootCtl):
    tempCenter = pm.circle(n='tempCircle', ch=0, nr=(0, 1, 0))[0]
    RootShp = pm.listRelatives(RootCtl, s=1)
    CenterShp = pm.listRelatives(tempCenter, s=1)[0]
    
    pm.setAttr('{}.dispGeometry'.format(CenterShp), 0)
    pm.parent(tempCenter, RootCtl)
    tempCenter.t.set(0,0,0)
    tempCenter.r.set(0,0,0)
    tempCenter.s.set(1,1,1)
    pm.parent(RootShp, tempCenter, s=1, r=1)
    pm.parent(CenterShp, RootCtl, s=1, r=1)
    pm.parent(RootShp, RootCtl, s=1, r=1)

    pm.rename(str(CenterShp), str(RootCtl)+'_centerShape_focus')
    pm.delete(tempCenter)

#20221028 edited - add function
## --- add Extra mirrored shape to any CTL --- ##
def addCenterShape_Mirrored(CTL):
    
    COPY = pm.duplicate(CTL, rc=1)[0]
    COPY_child = pm.listRelatives(COPY, c=1, type='transform')
    if COPY_child:
        pm.delete(COPY_child)
    
    COPY_shape = pm.listRelatives(COPY, s=1)[0]
    
    null = pm.group(em=1)
    pm.parent(COPY_shape, null, a=1, s=1)
    pm.delete(COPY)
    null.sx.set(-1)
    pm.makeIdentity(null, apply=1, t=1, r=1, s=1, n=0, pn=1)
    
    pm.parent(COPY_shape, CTL, a=1, s=1)
    pm.delete(null)

    TRASH = pm.listRelatives(COPY_shape, p=1, type='transform')[0]
    pm.makeIdentity(TRASH, apply=1, t=1, r=1, s=1, n=0, pn=1)
    pm.parent(COPY_shape, CTL, r=1, s=1)
    pm.setAttr('{}.dispGeometry'.format(COPY_shape), 0)
    pm.delete(TRASH)

    pm.rename(COPY_shape, str(CTL)+'_centerShape_focus')

#20221028 edited - add function
## for rollback(delete) centerShape
def deleteCenterShape(CTL):
    for x in pm.listRelatives(CTL, c=1, s=1):
        if '_centerShape_focus' in str(x):
            pm.delete(x)

####--- Definitions for UI execute buttons ---####
#--- main, world Controls edit ---#
def editAfterBuild(Main, World):
    worldCtl = createWorldCtl(World)[0]
    changeConst(Main, worldCtl)
    changeScale(Main, worldCtl)
    changeShp(Main, worldCtl)
    if pm.objExists('IKSpine1_M'):
        pm.setAttr('IKSpine1_M.FixedOrient', 10)
    if pm.objExists('IKSpine3_M'):
        pm.setAttr('IKSpine3_M.ikHybridVis', 0)

    addCenterShape(Root)
    addCenterShape_Mirrored(HipSwinger)


def rollbackEdit(Main, World):
    changeConst(World, Main)
    mainShp = pm.listRelatives(Main, s=1)[0]
    MainCtl = pm.ls(Main)[0]

    scaleInfo = pm.listConnections('{}.scale'.format(Main), type='multiplyDivide')
    scaleInfoOfInfo = pm.listConnections('{}.output'.format(scaleInfo[0]), p=1, type='multiplyDivide')[0]
    MainCtl.scale >> scaleInfoOfInfo

    pm.delete(scaleInfo)
    pm.delete(mainShp)
    pm.delete(World)

    deleteCenterShape(Root)
    deleteCenterShape(HipSwinger)
    createMainOrigShapeCtl()

#########################################################
##################### dualQuaternion ##################
#########################################################

#DQ Scale Error FIX

#all with namespace/ without namespace
def findDQ(ref):
    if ref == True:
        skinClusters_list = pm.ls('::*', type = 'skinCluster')
    else:
        skinClusters_list = pm.ls('*', type = 'skinCluster')

    DQ = []

    for skin in skinClusters_list:
        if not skin.skinningMethod.get() == 0:
            DQ.append(skin)

    return DQ

def DQ_nonRigid_ON(ref):
    DQ = findDQ(ref)
    if DQ :
        for skin in DQ:
            skin.dqsSupportNonRigid.set(1)
            pm.connectAttr('MainScaleMultiplyDivide.output', '{}.dqsScale'.format(skin))
    
def DQ_nonRigid_OFF(ref):
    DQ = findDQ(ref)
    if DQ:
        for skin in DQ:
            pm.disconnectAttr('MainScaleMultiplyDivide.output', '{}.dqsScale'.format(skin))
            skin.dqsSupportNonRigid.set(0)

##########################################################
############ IK subCTL ################################
#######################################################
# 20221031 edited (added)

# 20221216 added
def connectionRebuildSubToOrg(ctrl):
    x = ctrl
    y = ctrl+"_sub"

    _input_s, _output_s = pm.listConnections("{}.s".format(y), p=1, c=1)[0]
    _input_sx, _output_sx = pm.listConnections("{}.sx".format(y), p=1, c=1)[0]
    _input_sy, _output_sy = pm.listConnections("{}.sy".format(y), p=1, c=1)[0]
    _input_sz, _output_sz = pm.listConnections("{}.sz".format(y), p=1, c=1)[0]
    _new_input_s = pm.PyNode("{}.s".format(x))
    _new_input_sx = pm.PyNode("{}.sx".format(x))
    _new_input_sy = pm.PyNode("{}.sy".format(x))
    _new_input_sz = pm.PyNode("{}.sz".format(x))
    
    _input_s//_output_s
    _input_sx//_output_sx
    _input_sy//_output_sy
    _input_sz//_output_sz
    
    s_multiply = pm.createNode('multiplyDivide', n = "{}_{}_scale_mult".format(x,y))
    sx_multiply = pm.createNode('multDoubleLinear', n = "{}_{}_sx_mult".format(x,y))
    sy_multiply = pm.createNode('multDoubleLinear', n = "{}_{}_sy_mult".format(x,y))
    sz_multiply = pm.createNode('multDoubleLinear', n = "{}_{}_sz_mult".format(x,y))
    
    _new_input_s>>s_multiply.input1
    _input_s>>s_multiply.input2
    s_multiply.output>>_output_s
    
    _new_input_sx>>sx_multiply.input1
    _input_sx>>sx_multiply.input2
    sx_multiply.output>>_output_sx
    
    _new_input_sy>>sy_multiply.input1
    _input_sy>>sy_multiply.input2
    sy_multiply.output>>_output_sy
    
    _new_input_sz>>sz_multiply.input1
    _input_sz>>sz_multiply.input2
    sz_multiply.output>>_output_sz

def connectionRebuildOrgToSub(ctrl):
    x = ctrl
    y = ctrl+"_sub"

    _new_input_s = pm.PyNode("{}.s".format(y))
    _new_input_sx = pm.PyNode("{}.sx".format(y))
    _new_input_sy = pm.PyNode("{}.sy".format(y))
    _new_input_sz = pm.PyNode("{}.sz".format(y))
    s_multiply = pm.PyNode("{}_{}_scale_mult".format(x,y))
    sx_multiply = pm.PyNode("{}_{}_sx_mult".format(x,y))
    sy_multiply = pm.PyNode("{}_{}_sy_mult".format(x,y))
    sz_multiply = pm.PyNode("{}_{}_sz_mult".format(x,y))
    
    _new_input_s>>s_multiply.output.listConnections(p=1, d=1)[0]
    _new_input_sx>>sx_multiply.output.listConnections(p=1, d=1)[0]
    _new_input_sy>>sy_multiply.output.listConnections(p=1, d=1)[0]
    _new_input_sz>>sz_multiply.output.listConnections(p=1, d=1)[0]
    
    pm.delete(s_multiply)
    pm.delete(sx_multiply)
    pm.delete(sy_multiply)
    pm.delete(sz_multiply)

# --- making IKCTL subCTL --- 
def makeSubCTL(ctrl):
    
    org_shape = pm.listRelatives(ctrl, c=1, s=1)[0]
    org_name = str(ctrl)

    subCTL = pm.duplicate(ctrl, rc=1)[0]
    pm.rename(ctrl, ctrl+'_sub')
    pm.rename(subCTL, org_name)
    
    org = pm.PyNode(org_name+'_sub')
    subCTL = pm.PyNode(org_name)

    TRASH = pm.listRelatives(subCTL, c=1, type='transform')
    pm.delete(TRASH)

    pm.scale(org_shape.cv[:], 0.8,0.8,0.8, os=1)
    org_shape.overrideColor.set(9)
    pm.parent(org, subCTL)

    org_Attr = pm.listAttr(ctrl, ud=1)
    subCTL_Attr = pm.listAttr(subCTL, ud=1)

    for x in org_Attr:
        for y in subCTL_Attr:
            if y == x:
                if not x =='ikLocal':
                    pm.connectAttr(subCTL+'.'+y, org+'.'+x)
                    pm.setAttr(org+'.'+x, k=0, cb=0)

    pm.addAttr(subCTL, ln='visSUB', at='bool', k=1)
    pm.setAttr(subCTL.visSUB, k=0, cb=1)

    subCTL.visSUB>>org_shape.v
    
    connectionRebuildSubToOrg(ctrl)
    
def makeSubCTL_rollBack(ctrl):
    connectionRebuildOrgToSub(ctrl)
    
    org = pm.PyNode(ctrl+'_sub')
    subCTL = pm.PyNode(ctrl)
    org_p = pm.listRelatives(ctrl, p=1, type='transform')[0]
    org_shape = pm.listRelatives(ctrl, c=1, s=1)[0]

    org_Attr = pm.listAttr(org, ud=1)
    subCTL_Attr = pm.listAttr(subCTL, ud=1)

    for x in org_Attr:
        for y in subCTL_Attr:
            if x==y:
                if not x =='ikLocal':
                    pm.disconnectAttr(subCTL+'.'+y, org+'.'+x)
                    pm.setAttr(org+'.'+x, cb=1)
                    pm.setAttr(org+'.'+x, k=1)

    pm.parent(org, org_p)
    pm.delete(subCTL)
    pm.rename(org, subCTL)
    
    org = pm.PyNode(ctrl)
    org_shape = pm.listRelatives(ctrl, c=1, s=1)[0]
    
    org_shape.v.set(1)
    pm.scale(org_shape.cv[:], 1.25,1.25,1.25, os=1)
    org_shape.overrideColor.set(13)

####--- Definitions for UI execute buttons ---####
def editSubCTL():
    ctrlList = ('IKArm_L', 'IKArm_R', 'IKLeg_L', 'IKLeg_R')
    for x in ctrlList:
        makeSubCTL(x)
        
def editSubCTL_rollBack():
    ctrlList = ('IKArm_L', 'IKArm_R', 'IKLeg_L', 'IKLeg_R')
    for x in ctrlList:
        makeSubCTL_rollBack(x)

##########################################################
############ IK transCTL ################################
#######################################################
# 20230127 edited (added)

def makeIkTransCTL():
    for rootJNT,ikCTL in zip(IKRoot, IKctrlList):
        #make CTL upper rootJNT
        rootJNT = pm.PyNode(rootJNT)
        ikCTL = pm.PyNode(ikCTL)
        _parent = rootJNT.listRelatives(p=1)[0]
        pm.select(cl=1)
        _circle = pm.circle(r=1.2, nr = (1,0,0), n= rootJNT.replace("IKX", "IKTRANS"))
        CTL = _circle[0]
        shape = CTL.listRelatives(c=1, s=1)[0]
        pm.delete(_circle[1])
        offGRP = pm.group(em=1, n = CTL+"_offGRP")
        fixGRP = pm.group(em=1, n = CTL+"_fixGRP")
        pm.parent(fixGRP, CTL)
        pm.parent(CTL, offGRP)
        
        pm.parent(offGRP, _parent)
        offGRP.t.set(0,0,0)
        offGRP.r.set(0,0,0)
        offGRP.s.set(1,1,1)
        
        if "Shoulder" in rootJNT.name():
            _grandParent = _parent.listRelatives(p=1)[0]
            pm.matchTransform(offGRP, _grandParent, pos=0, rot=1, scl=0, piv=0)
            pm.matchTransform(fixGRP, rootJNT, pos=0, rot=1, scl=0, piv=0)

            if "_L" in rootJNT.name():
                offGRP.s.set(-1,-1,1)
                fixGRP.s.set(-1,-1,1)
        else:
            pm.move("{}.cv[:]".format(shape), 0,-1, 0, r=1)
        
        pm.parent(rootJNT, fixGRP)
        
        pm.setAttr("{}.rx".format(CTL), l=1)
        pm.setAttr("{}.ry".format(CTL), l=1)
        pm.setAttr("{}.rz".format(CTL), l=1)
        pm.setAttr("{}.sx".format(CTL), l=1)
        pm.setAttr("{}.sy".format(CTL), l=1)
        pm.setAttr("{}.sz".format(CTL), l=1)
        pm.setAttr("{}.v".format(CTL), l=1)
        
        pm.setAttr("{}.rx".format(CTL), k=0)
        pm.setAttr("{}.ry".format(CTL), k=0)
        pm.setAttr("{}.rz".format(CTL), k=0)
        pm.setAttr("{}.sx".format(CTL), k=0)
        pm.setAttr("{}.sy".format(CTL), k=0)
        pm.setAttr("{}.sz".format(CTL), k=0)
        pm.setAttr("{}.v".format(CTL), k=0)
        
        pm.addAttr(ikCTL, ln='visTransCTL', at='bool', k=1)
        pm.setAttr(ikCTL.visTransCTL, k=0, cb=1)
        
        ikCTL.visTransCTL>>shape.v
        shape.overrideEnabled.set(1)
        shape.overrideColor.set(6)

def makeIkTransCTL_rollBack():
    for rootJNT,ikCTL in zip(IKRoot, IKctrlList):
        rootJNT = pm.PyNode(rootJNT)
        offGRP = rootJNT.listRelatives(p=1)[0].listRelatives(p=1)[0].listRelatives(p=1)[0]
        orgGRP = rootJNT.listRelatives(p=1)[0].listRelatives(p=1)[0].listRelatives(p=1)[0].listRelatives(p=1)[0]
        
        pm.parent(rootJNT, orgGRP)
        pm.delete(offGRP)
        
        pm.deleteAttr("{}.visTransCTL".format(ikCTL))
    