# coding:utf-8
import pymel.all as pm


armL = [ 'Shoulder', 'Elbow', 'Wrist' ]
prefix = 'VisPV_'
armLocL = []

for arm in armL:
	jnt = pm.PyNode(arm)
	loc = pm.spaceLocator(n=prefix+arm)
	pm.delete(pm.pointConstraint(jnt, loc, mo=0))
	pm.pointConstraint(jnt, loc, mo=1)
	armLocL.append(loc)

sh = armLocL[0]
el = armLocL[1]
wr = armLocL[2]

sh_dis = pm.createNode('distanceBetween', n=prefix+'sh_dis')
pm.connectAttr(sh.worldMatrix[0], sh_dis.inMatrix1)
pm.connectAttr(el.worldMatrix[0], sh_dis.inMatrix2)

wr_dis = pm.createNode('distanceBetween', n=prefix+'wr_dis')
pm.connectAttr(wr.worldMatrix[0], wr_dis.inMatrix1)
pm.connectAttr(el.worldMatrix[0], wr_dis.inMatrix2)

el_vec = pm.spaceLocator(n=prefix+'Arm_vec')
pm.delete(pm.pointConstraint(sh, wr, el_vec, mo=0))
pm.delete(pm.pointConstraint(el, el_vec, mo=0, sk='z'))
pm.delete(pm.orientConstraint('Shoulder', 'Elbow', el_vec, mo=0))
pm.rotate(el_vec, -180,0,0, r=True, os=True)
#pm.makeIdentity(el_vec, t=1, r=0, s=0, apply=True)

aim_pnt = pm.pointConstraint(armL[0], armL[2], el_vec, mo=1)
aimCnst = pm.aimConstraint(armL[1], el_vec, mo=1, aim=(1,0,0), u=(0,0,1), wut='objectrotation', wu=(0,0,1), wuo=armL[0])

#pm.setAttr(aim_pnt.offset, 0,0,0)
#pm.setAttr(aimCnst.offset, 0,0,0)
pm.disconnectAttr(aim_pnt.ShoulderW0)
pm.disconnectAttr(aim_pnt.WristW1)
pm.connectAttr(wr_dis.distance, aim_pnt.ShoulderW0)
pm.connectAttr(sh_dis.distance, aim_pnt.WristW1)

disA = pm.createNode('distanceBetween', n=prefix+'pv_disA')
pm.connectAttr(sh.worldMatrix[0], disA.inMatrix1)
pm.connectAttr(wr.worldMatrix[0], disA.inMatrix2)

disB = pm.createNode('distanceBetween', n=prefix+'pv_disB')
pm.connectAttr(el.worldMatrix[0], disB.inMatrix1)
pm.connectAttr(el_vec.worldMatrix[0], disB.inMatrix2)

pma = pm.createNode('plusMinusAverage', n=prefix+'Arm_PMA')
pm.connectAttr(disA.distance, pma.input1D[0])
pm.connectAttr(disB.distance, pma.input1D[1])

vec = pm.spaceLocator(n=prefix+'Arm')
pm.parent(vec, el_vec)
pm.setAttr(vec.t, 0,0,0)
pm.setAttr(vec.r, 0,0,0)
pm.connectAttr(pma.output1D, vec.tz)

tmpP = (0,0,0)
poly = pm.polyCreateFacet(n=prefix+'poly', p=[tmpP, tmpP, tmpP, tmpP])
pm.parent(sh, el, wr, el_vec, poly)

poly = pm.PyNode(str(poly[0])+'Shape')
shP = pm.PyNode(str(sh)+'Shape')
vecP = pm.PyNode(str(vec)+'Shape')
wrP = pm.PyNode(str(wr)+'Shape')
elP = pm.PyNode(str(el)+'Shape')
pntL = [ shP, vecP, wrP, elP ]

for i in range(4):
	pm.connectAttr(pntL[i].worldPosition[0], poly.pnts[i])

