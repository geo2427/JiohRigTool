import maya.cmds as mc
import math as math
# this is 100% made and copyrighted by korean SANG BIN LEE
# I'm finding a job now(2022/07). Rigging TA / CFX Artist / Character TD is good for me.
# my github : https://github.com/SANG-BIN-LEE
# my linkedin : https://www.linkedin.com/in/sangbin-lee-981a7215a
# my youtube : https://www.youtube.com/playlist?list=PLKIoBfXktlaalLuyrsqxT3QgzhQ-08yeE
# maintenance work is needed, yet.

class BinIKSetting():
    def __init__(self):
        pass
    def ikPVT(self, ikList=mc.ls(sl=1, type='joint')):
        self.ikList = ikList
        if not len(self.ikList) == 3:
            mc.error('please select 3 joint.')
            return
        ikRoot, ikMiddle, ikTip = self.ikList

        #calculate pos
        space1 = mc.xform (ikRoot, q=1, ws=1, t=1)
        space2 = mc.xform (ikMiddle, q=1, ws=1, t=1)
        space3 = mc.xform (ikTip, q=1, ws=1, t=1)
        x1,y1,z1 = space1
        x2,y2,z2 = space2
        x3,y3,z3 = space3
        
        #calculate PV
        #ua dot product
        ua = (x3-x1)*(x3-x2)+(y3-y1)*(y3-y2)+(z3-z1)*(z3-z2)
        u = math.sqrt((x3-x1)**2+(y3-y1)**2+(z3-z1)**2)
        d = ua/u
        uVec = ((x3-x1),(y3-y1),(z3-z1))
        mx,my,mz = ((x3-x1)*(u-d)/u, (y3-y1)*(u-d)/u, (z3-z1)*(u-d)/u)
        pos1 = ((x1+mx),(y1+my),(z1+mz))
        self.poseH = pos1
        x4,y4,z4 = pos1
        a = math.sqrt((x3-x2)**2+(y3-y2)**2+(z3-z2)**2)
        h = math.sqrt(a**2 - d**2)
        hVec = ((x2-x4),(y2-y4),(z2-z4))
        #uh vector product
        UH = (uVec[1]*hVec[2]-uVec[2]*hVec[1], uVec[2]*hVec[0]-uVec[0]*hVec[2], uVec[0]*hVec[1]-uVec[1]*hVec[0])
        #uh length
        uh = math.sqrt(UH[0]**2+UH[1]**2+UH[2]**2)
        
        posPV = (pos1[0]+3*hVec[0], pos1[1]+3*hVec[1], pos1[2]+3*hVec[2])

        X = [uVec[0]/u, uVec[1]/u, uVec[2]/u, 0]
        Y = [UH[0]/uh, UH[1]/uh, UH[2]/uh, 0]
        Z = [-hVec[0]/h, -hVec[1]/h, -hVec[2]/h, 0]
        T = [posPV[0], posPV[1], posPV[2], 1]
        PVmt = []
        for x in X:
            PVmt.append(x)
        for y in Y:
            PVmt.append(y)
        for z in Z:
            PVmt.append(z)
        for t in T:
            PVmt.append(t)
        self.PVmt = PVmt
        self.posPV = posPV

        return posPV
    def ikRPSet(self, n='name', s=5, aim=(1,0,0)):
        if not len(self.ikList) == 3:
            mc.error('please select 3 joint.')
            return

        ikRoot, ikMiddle, ikTip = self.ikList

        #createController_Hand
        mc.select(cl=1)
        Tipmaster = mc.group(em=1, n=n+'_MCTL')
        Tipmain = BinCTL.cube_CTL(n=n+'_CTL', s=s*1.2, c=17)
        mc.setAttr(Tipmain+'.v', lock=1, keyable=0, cb=0)
        mc.setAttr(Tipmain+'.sx', lock=1, keyable=0, cb=0)
        mc.setAttr(Tipmain+'.sy', lock=1, keyable=0, cb=0)
        mc.setAttr(Tipmain+'.sz', lock=1, keyable=0, cb=0)
        Tipnull = BinCTL.cube_CTL(n=n+'_n_CTL', s =s*1, c=21)
        mc.setAttr(Tipnull+'.v', lock=1, keyable=0, cb=0)
        mc.setAttr(Tipnull+'.sx', lock=1, keyable=0, cb=0)
        mc.setAttr(Tipnull+'.sy', lock=1, keyable=0, cb=0)
        mc.setAttr(Tipnull+'.sz', lock=1, keyable=0, cb=0)
        mc.parent(Tipnull,Tipmain)
        mc.parent(Tipmain,Tipmaster)
        ro = mc.getAttr(ikTip+'.rotateOrder')
        mc.setAttr(Tipmaster+'.rotateOrder', ro)
        mc.setAttr(Tipmain+'.rotateOrder', ro)
        mc.setAttr(Tipnull+'.rotateOrder', ro)
        mc.matchTransform(Tipmaster, ikTip)

        #createController_PV
        mc.select(cl=1)
        PVmaster = mc.group(em=1, n=n+'_MPVCTL')
        PVmain = BinCTL.halfdia_CTL(n=n+'_PV_CTL', s=s*0.5, c=17)
        mc.setAttr(PVmain+'.v', lock=1, keyable=0, cb=0)
        mc.setAttr(PVmain+'.sx', lock=1, keyable=0, cb=0)
        mc.setAttr(PVmain+'.sy', lock=1, keyable=0, cb=0)
        mc.setAttr(PVmain+'.sz', lock=1, keyable=0, cb=0)
        mc.setAttr(PVmain+'.rx', lock=1, keyable=0, cb=0)
        mc.setAttr(PVmain+'.ry', lock=1, keyable=0, cb=0)
        mc.setAttr(PVmain+'.rz', lock=1, keyable=0, cb=0)
        mc.parent(PVmain, PVmaster)
        mc.setAttr(PVmaster+'.offsetParentMatrix', self.PVmt, type='matrix')

        RP = mc.ikHandle(sol='ikRPsolver', n=n+'_ikRPsolver', sj=ikRoot, ee=ikTip)
        RPsolver = RP[0]
        mc.rename(RP[1], n+'_ikRPee')
        mc.parent(RPsolver, Tipnull)
        mc.poleVectorConstraint(PVmain, RPsolver)
        dMt = mc.createNode('decomposeMatrix', n='IKdMt_'+ikTip)
        lR = mc.listRelatives(ikTip, p=1)[0] or ''
        if not lR == '':
            multMt = mc.createNode('multMatrix', n='multMt'+ikTip)
            mc.connectAttr(Tipnull+'.worldMatrix', multMt+'.matrixIn[0]')
            mc.connectAttr(lR+'.worldInverseMatrix', multMt+'.matrixIn[1]')
            mc.connectAttr(multMt+'.matrixSum', dMt+'.inputMatrix')
        else:
            mc.connectAttr(Tipnull+'.worldMatrix', dMt+'.inputMatrix')
        mc.connectAttr(dMt+'.outputRotate', ikTip+'.jointOrient')

        self.RPsolver = RPsolver
        self.Tipmain = Tipmain
        self.Tipnull = Tipnull
        self.PVmain = PVmain
        return RPsolver, Tipmain, Tipnull, PVmain
    def ikSpline(self, j = mc.ls(sl=1, type='joint'), d=3, n = 'spline'):
        self.splineJoint = j
        ev = []
        for x in self.Joint:
            point = mc.xform(x,q=1,ws=1,t=1)
            ev.append(tuple(point))
        mc.select(cl=1)
        mc.curve(d=3, ep=ev, n=n+'_ikCurve')
        mc.ikHandle(sj=self.Joint[0], ee=self.Joint[-1], c=n+'_ikCurve', n=n+'_ikHandle', sol='ikSplineSolver', ccv=0, scv=0, pcv=0)
    def help(self):
        print("""
        ikPVT(ikList = mc.ls(sl=1))
        ikRPSet(n=stringName, s=3 scale) -needed PVT first, color is fixed
        ikSpline(j=joints, d=3 degree, n=name)
        """ )
BinIK = BinIKSetting()
class BinIKFKSwitch():
    def __init__(self):
        pass
    def FKtoIK(self, FKJoints, PV_CTL, IKRP_CTL):
        tx, ty, tz = BinIK.ikPVT(ikList=FKJoints)
        mc.group(em=1, n='temp')
        mc.setAttr('temp.tx', tx)
        mc.setAttr('temp.ty', ty)
        mc.setAttr('temp.tz', tz)
        mc.matchTransform(PV_CTL, 'temp', rot=0, scl=0)
        mc.matchTransform(IKRP_CTL, FKJoints[2])
        mc.delete('temp')
    def IKtoFK(self, IKJoints, FK_CTLs):
        mc.matchTransform(FK_CTLs[0], IKJoints[0])
        mc.matchTransform(FK_CTLs[1], IKJoints[1])
        mc.matchTransform(FK_CTLs[2], IKJoints[2])
    def help(self):
        print("""
        FKtoIK = FKJoints, PV_CTL, IKRP_CTL
        IKtoFK = IKJoints, FK_CTLs
        """)

# keep this py file to maya script folder

# example
# from IKFKSW import BinIKSetting as BinIK
# from IKFKSW import BinIKFKSwitch
# BinSwitch = BinIKFKSwitch()
# BinSwitch.FKtoIK(['fkjoint1Name', 'fkjoint2Name', 'fkjoint3Name'], 'ikPVName', 'ikCTLName')
# BinSwitch.IKtoFK(['ikjoint1Name', 'ikjoint2Name', 'ikjoint3Name'],['fkCTL1Name', 'fkCTL2Name', 'fkCTLName'])