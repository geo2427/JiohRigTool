import pymel.all as pm


#### 0. pre

# Resample
# - Root > Chest > 4개
# * 조인트의 Radius나 scale 값이 바뀌지 않은 상태에서 진행


#### 1. FitSkeleton

Root = pm.PyNode('Root')
ArmPartL = [ "Shoulder", "Elbow", "Wrist" ]
LegPartL = [ "Hip", "Knee", "Ankle" ]


# All
pm.select(Root, hi=1)
for jnt in pm.select(Root, hi=1):
    pm.addAttr(jnt, sn='freeOrient', at='bool', dv=1, k=1)

# Root
pm.setAttr(Root.inbetweenJoints, 0)
pm.setAttr(Root.numMainExtras, 2)

# Spine
for i in range(2):
    jnt = pm.PyNode('Spine'+i)
    pm.addAttr(jnt, sn='inbetweenJoints', at='float', dv=1, k=1)

# Shoulder
for i in range(2):
    jnt = pm.PyNode(ArmPartL[i])
    pm.setAttr(jnt.bendyJoints, 1)
    pm.setAttr(jnt.twistJoints, 3)

# wrist
jnt = pm.PyNode(ArmPartL[3])
pm.addAttr(jnt, sn='ikLocal', at='enum', k=1, en='addCtrl:noneZero:localOrient') 
pm.setAttr(jnt.ikLocal, 0)
pm.select('Chest', 'Wrist')
pm.addAttr(jnt, sn='ikFollow', at='enum', k=1, en='Chest') 

# Hip
for part in LegPartL:
    jnt = pm.PyNode(LegPartL[i])
    pm.addAttr(jnt, sn='ikLocal', at='enum', k=1, en='addCtrl:noneZero:localOrient') 
    pm.setAttr(jnt.ikLocal, 0)
    pm.addAttr(jnt, sn='global', at='bool', k=1, dv=10)

for i in range(2):
    jnt = pm.PyNode(LegPartL[i])
    pm.setAttr(jnt.bendyJoints, 1)
    pm.setAttr(jnt.twistJoints, 3)

# Ankle
jnt = pm.PyNode(LegPartL[2])
pm.setAttr(jnt.worldOreint, 4)
# pm.addAttr(jnt, sn='ikLocal', at='enum', k=1, en='addCtrl:noneZero:localOrient') 
# pm.setAttr(jnt.ikLocal, 2)


# Finger
# - FreeOrient를 사용해서, 구부려질 때 +rX 여야 함
# - Auto-Orient: Y,Z


#### 2. Build시
# - 전체 freeOrient=0 > Y,Z 으로 세팅 > freeOrient=1
# - Auto-Orient: Y, X
# ㄴ fingerCtqrl.attribute 제대로 작동하려면



