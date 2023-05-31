## Custom : T pose for AVS HIK ##
import pymel.core as pm


def mirrorArm(direction):
    ctl = ['PoleArm_%s' % direction, 'FKScapula_%s' % direction, 'IKArm_%s' % direction]
    t = pm.group(n='temp', em=1)
    tG = pm.group(n='tempGrp')
    for i in range(3):
        if direction == "L":
            other = "R"
        else:
            other = "L"
        otherDirection = ctl[i].replace(direction, other)
        pm.setAttr(tG + '.scaleX', 1)
        if not i:
            pm.delete(pm.pointConstraint(ctl[i], t, mo=0))
        else:
            pm.delete(pm.parentConstraint(ctl[i], t, mo=0))
        pm.setAttr(tG + '.scaleX', -1)
        if not i:
            pm.delete(pm.pointConstraint(t, otherDirection, mo=0))
        else:
            pm.delete(pm.parentConstraint(t, otherDirection, mo=0))
    pm.delete(tG)

def setTpose():
    AToB=pm.datatypes.Vector.zero
    armJoint=[['Shoulder_L', 'Elbow_L'], ['Elbow_L', 'Wrist_L']]
    ikHandCtl='IKArm_L'
    wrist=pm.PyNode(ikHandCtl)
    for items in armJoint:
        aRev=pm.datatypes.Vector(pm.xform(items[0], q=1, t=1, ws=1)).__neg__()
        b=pm.datatypes.Vector(pm.xform(items[1], q=1, t=1, ws=1))
        AToB+=pm.datatypes.Vector.length(aRev+b)
    sholderPoint=pm.datatypes.Vector(pm.xform(armJoint[0][0], q=1, t=1, ws=1))
    goalPoint=sholderPoint+(AToB.x, 0, 0)
    pm.xform(ikHandCtl, t=goalPoint, ws=1)
    ElbowHigh=pm.datatypes.Vector(0, pm.xform(armJoint[0][1], q=1, t=1, ws=1)[1], 0)
    polPos=pm.datatypes.Vector(pm.xform(wrist, q=1, t=1, ws=1))
    wristRo=pm.xform(armJoint[1][1], q=1, os=1, ro=1)

    pm.xform(wrist, t=(polPos.x, ElbowHigh.y, polPos.z), ws=1)
    pm.xform(wrist, os=1, ro=(0, wristRo[1]*-1, wristRo[2]*-1))

    mirrorArm('L')

    pm.setAttr('PoleArm_L.follow', 10)
    pm.setAttr('PoleArm_R.follow', 10)
    pm.setAttr('FKIKSpine_M.FKIKBlend', 10)

# run
setTpose()