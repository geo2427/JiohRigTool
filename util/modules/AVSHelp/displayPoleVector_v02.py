# coding:utf-8
import pymel.all as pm


partL = [ 'Arm', 'Leg' ]
prefix01 = 'VisPV_'

for part in partL:
	
	secPartL = []
	if part == 'Arm':
		armL = [ 'Shoulder', 'Elbow', 'Wrist' ]
		for arm in armL:
			secPartL.append(arm)
	else:
		legL = [ 'Hip', 'Knee', 'Ankle' ]
		for leg in legL:
			secPartL.append(leg)

	prefix = prefix01 + part
	locL = []
	for arm in secPartL:
		jnt = pm.PyNode(arm)
		loc = pm.spaceLocator(n=prefix+arm)
		pm.delete(pm.pointConstraint(jnt, loc, mo=0))
		pm.pointConstraint(jnt, loc, mo=1)
		locL.append(loc)

	pos01 = locL[0]
	pos02 = locL[1]
	pos03 = locL[2]

	disA = pm.createNode('distanceBetween', n=prefix+'_disA')
	pm.connectAttr(pos01.worldMatrix[0], disA.inMatrix1)
	pm.connectAttr(pos02.worldMatrix[0], disA.inMatrix2)

	disB = pm.createNode('distanceBetween', n=prefix+'_disB')
	pm.connectAttr(pos03.worldMatrix[0], disB.inMatrix1)
	pm.connectAttr(pos02.worldMatrix[0], disB.inMatrix2)

	el_vec = pm.spaceLocator(n=prefix+'_vec')
	pm.delete(pm.pointConstraint(pos01, pos03, el_vec, mo=0))
	pm.delete(pm.pointConstraint(pos02, el_vec, mo=0, sk='z'))
	pm.delete(pm.orientConstraint(secPartL[0], secPartL[1], el_vec, mo=0))
	pm.rotate(el_vec, -180,0,0, r=True, os=True)
	#pm.makeIdentity(el_vec, t=1, r=0, s=0, apply=True)

	pntCnst = pm.pointConstraint(secPartL[0], secPartL[2], el_vec, mo=1)
	aimCnst = pm.aimConstraint(secPartL[1], el_vec, mo=1, aim=(1,0,0), u=(0,0,1), wut='objectrotation', wu=(0,0,1), wuo=secPartL[0])

	#pm.setAttr(aim_pnt.offset, 0,0,0)
	pm.setAttr(aimCnst.offset, 0,0,0)
	pm.disconnectAttr(pntCnst+'.'+secPartL[0]+'W0')
	pm.disconnectAttr(pntCnst+'.'+secPartL[2]+'W1')
	pm.connectAttr(disB.distance, pntCnst+'.'+secPartL[0]+'W0')
	pm.connectAttr(disA.distance, pntCnst+'.'+secPartL[2]+'W1')

	disC = pm.createNode('distanceBetween', n=prefix+'_disC')
	pm.connectAttr(pos01.worldMatrix[0], disC.inMatrix1)
	pm.connectAttr(pos03.worldMatrix[0], disC.inMatrix2)

	disD = pm.createNode('distanceBetween', n=prefix+'_disD')
	pm.connectAttr(pos02.worldMatrix[0], disD.inMatrix1)
	pm.connectAttr(el_vec.worldMatrix[0], disD.inMatrix2)

	pma = pm.createNode('plusMinusAverage', n=prefix+'_PMA')
	pm.connectAttr(disC.distance, pma.input1D[0])
	pm.connectAttr(disD.distance, pma.input1D[1])

	vec = pm.spaceLocator(n=prefix)
	pm.parent(vec, el_vec)
	pm.setAttr(vec.t, 0,0,0)
	pm.setAttr(vec.r, 0,0,0)
	pm.connectAttr(pma.output1D, vec.tz)

	tmpP = (0,0,0)
	poly = pm.polyCreateFacet(n=prefix+'poly', p=[tmpP, tmpP, tmpP, tmpP])
	pm.parent(pos01, pos02, pos03, el_vec, poly)
	poly = pm.PyNode(str(poly[0])+'Shape')

	shP = pm.PyNode(str(pos01)+'Shape')
	vecP = pm.PyNode(str(vec)+'Shape')
	wrP = pm.PyNode(str(pos03)+'Shape')
	elP = pm.PyNode(str(pos02)+'Shape')
	pntL = [ shP, vecP, wrP, elP ]

	for i in range(4):
		pm.connectAttr(pntL[i].worldPosition[0], poly.pnts[i])

