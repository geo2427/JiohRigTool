# coding:utf-8
import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm
import pymel.core as core


def constraint(TypeName, ConsName, x):
    selList = pm.ls(sl=1)
    Moffset = pm.checkBox('MaintainOffset', q=1, v=1)

    if TypeName == 'Constraint':
        for i in range(len(selList) - 1):
            eval('pm.%sConstraint(selList[i], selList[-1], mo=Moffset)' % ConsName)
    elif TypeName == 'OneToAll':
        for i in range(len(selList) - 1):
            eval('pm.%sConstraint(selList[0], selList[i+1], mo=Moffset)' % ConsName)
    elif TypeName == 'Each':
        for i in range(len(selList)):
            if i % 2 == 0:
                eval('pm.%sConstraint(selList[i], selList[i+1], mo=Moffset)' % ConsName)
            else:
                continue
    elif TypeName == 'AllToAll':
        ListHarfLen = len(selList) / 2
        for i in range(ListHarfLen):
            eval('pm.%sConstraint(selList[i], selList[i+ListHarfLen], mo=Moffset)' % ConsName)


def CtrlShapeChage(tslpanel, z):
    tslOldShape = core.uitypes.TextScrollList(tslpanel[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tslpanel[1]).getAllItems()
    if (len(tslOldShape) or len(tslNewShape)) > 1:
        print ('Select one by one')
    else:
        pm.parent(pm.PyNode(tslNewShape[0]).getShape(), tslOldShape[0], r=1, s=1)
        pm.delete(tslNewShape[0], pm.PyNode(tslOldShape[0]).getShape())
        core.uitypes.TextScrollList(tslpanel[0]).removeItem(tslOldShape)
        core.uitypes.TextScrollList(tslpanel[1]).removeItem(tslNewShape)


def MeshChangeOneToOneConnect(tslpanel, x):
    tslOldShape = core.uitypes.TextScrollList(tslpanel[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tslpanel[1]).getAllItems()
    if len(tslNewShape) == len(tslOldShape):
        for num in range(len(tslOldShape)):
            pm.connectAttr((pm.PyNode(tslNewShape[num]).getShapes()[-1]).outMesh,
                           (pm.PyNode(tslOldShape[num]).getShapes()[-1]).inMesh, f=1)
            print ('Mesh Change' + tslOldShape[num] + '->' + tslNewShape[num])
    else:
        print ('OldShapeList And NewShapeList is not Same. Check Your List')


def MeshChangeOnToAllConnec(tslpanel, x):
    tslOldShape = core.uitypes.TextScrollList(tslpanel[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tslpanel[1]).getAllItems()
    for ChangeObj in tslOldShape:
        print (tslNewShape[0], ChangeObj)
        pm.connectAttr((pm.PyNode(tslNewShape[0]).getShapes()[-1]).outMesh,
                       (pm.PyNode(ChangeObj).getShapes()[-1]).inMesh, f=1)
        print ('Mesh Change' + ChangeObj + '->' + tslNewShape[0])


def MeshChangeOneToOneDisConnec(tslpanel, x):
    tslOldShape = core.uitypes.TextScrollList(tslpanel[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tslpanel[1]).getAllItems()
    if len(tslNewShape) == len(tslOldShape):
        for num in range(len(tslOldShape)):
            pm.disconnectAttr((pm.PyNode(tslNewShape[num]).getShapes()[-1]).outMesh,
                              (pm.PyNode(tslOldShape[num]).getShapes()[-1]).inMesh)
            print ('Mesh DisConnect' + tslOldShape[num] + '->' + tslNewShape[num])
    else:
        print ('OldShapeNum And NewShapeNum is not Same. Check Your List')


def MeshChangeOnToAllDisConnec(tslpanel, x):
    tslOldShape = core.uitypes.TextScrollList(tslpanel[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tslpanel[1]).getAllItems()
    for ChangeObj in tslOldShape:
        pm.disconnectAttr((pm.PyNode(tslNewShape[0]).getShapes()[-1]).outMesh,
                          (pm.PyNode(ChangeObj).getShapes()[-1]).inMesh)
        print ('Mesh DisConnect' + ChangeObj + '->' + tslNewShape[0])


def CopySkinOneToOne(tslpanel, z):
    tslOldShape = core.uitypes.TextScrollList(tslpanel[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tslpanel[1]).getAllItems()

    # 두 리스트의 갯수가 같을때만 작동하시오
    if len(tslOldShape) == len(tslNewShape):
        for i in range(len(tslNewShape)):
            # 스킨과 조인트들을 알아내고
            # GoodSkin = mel.eval('findRelatedSkinCluster ' + tslNewShape[i])
            GoodSkin = pm.listHistory(pm.PyNode(tslNewShape[i]), groupLevels=True, pruneDagObjects=True, il=2,
                                      type='skinCluster')
            # GoodFindJntList = cmds.listConnections(GoodSkin + '.influenceColor', t='joint')
            GoodFindJntList = [x.name() for x in GoodSkin[0].getInfluence()]
            GoodBindJntlist = []
            # 조인트가 레퍼런스라면 네임을 빼시오
            if ':' in GoodFindJntList[0]:
                GoodBindJntlist = [x.split(':')[1] for x in GoodFindJntList]
            else:
                GoodBindJntlist = GoodFindJntList
            # 올드리스트 메쉬에 스킨이 있는지 없는지 파악하시오
            # BadSkin = pm.PyNode(tslOldShape[i]).getShape().inputs(type='skinCluster')
            BadSkin = pm.listHistory(pm.PyNode(tslOldShape[i]), groupLevels=True, pruneDagObjects=True, il=2,
                                     type='skinCluster')
            if BadSkin:
                # 스킨이있으면
                # 조인트 리스트가 서로 같은지 파악하시오
                BadFindJntList = [x.name() for x in BadSkin[0].getInfluence()]
                # 같지않다면 조인트들을 더하고 카피하시오
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
                    print ('JntList is not same Add Joint And Finished Copy  ' + tslNewShape[i] + ' -> ' + tslOldShape[i])
                # 같다면 스킨을 카피하시오
                else:
                    pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
                    print ('Finished Copy  ' + tslNewShape[i] + ' -> ' + tslOldShape[i])
            else:
                # 스킨이없으면 바인드를 하고 카피하시오
                newJntList = [x for x in GoodBindJntlist if pm.objExists(x)]
                pm.skinCluster(newJntList, tslOldShape[i], tsb=1)
                # BadSkin = pm.PyNode(tslOldShape[i]).getShape().inputs(type='skinCluster')
                BadSkin = pm.listHistory(pm.PyNode(tslOldShape[i]), groupLevels=True, pruneDagObjects=True, il=2,
                                         type='skinCluster')
                pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
                print ('OldSkin is not exist bind Jnt And Finished Copy  ' + tslNewShape[i] + ' -> ' + tslOldShape[i])
    else:
        print ('OldObj numberList and NewObj numberList is not Same Check Your List')


def CopySkinOneToAll(tslpanel, z):
    tslOldShape = core.uitypes.TextScrollList(tslpanel[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tslpanel[1]).getAllItems()

    # 뉴리스트의 스킨과 조인트들을 알아내고
    # GoodSkin = pm.PyNode(tslNewShape[0]).getShape().inputs(type='skinCluster')
    GoodSkin = pm.listHistory(pm.PyNode(tslNewShape[0]), groupLevels=True, pruneDagObjects=True, il=2,
                              type='skinCluster')
    GoodFindJntList = [x.name() for x in GoodSkin[0].getInfluence()]
    GoodBindJntlist = []
    # 조인트가 레퍼런스라면 네임을 빼시오
    if ':' in GoodFindJntList[0]:
        GoodBindJntlist = [x.split(':')[1] for x in GoodFindJntList]
    else:
        GoodBindJntlist = GoodFindJntList
    # 올드리스트 메쉬에 스킨이 있는지 없는지 파악하시오
    for changeObjs in tslOldShape:
        # BadSkin = pm.PyNode(changeObjs).getShape().inputs(type='skinCluster')
        BadSkin = pm.listHistory(pm.PyNode(changeObjs), groupLevels=True, pruneDagObjects=True, il=2,
                                 type='skinCluster')
        if BadSkin:
            # 스킨이있으면
            # 조인트 리스트를 비교해서
            BadFindJntList = [x.name() for x in BadSkin[0].getInfluence()]
            # 모자란 조인트들 중에서 존재하는 조인트만을 더하고 스킨 카피하시오
            addJntList = [x for x in GoodBindJntlist if not (x in BadFindJntList) * (pm.objExists(x))]
            if addJntList:
                pm.skinCluster(changeObjs, edit=1, ai=addJntList, lw=1, dr=4, tsb=1)
            pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
            print ('Finished Copy And Bind ' + tslNewShape[0] + ' -> ' + changeObjs)
        else:
            # 스킨이없으면 바인드를 하고 카피하시오
            newJntList = [x for x in GoodBindJntlist if pm.objExists(x)]
            pm.skinCluster(GoodBindJntlist, changeObjs, tsb=1)
            # BadSkin = pm.PyNode(changeObjs).getShape().inputs(type='skinCluster')
            BadSkin = pm.listHistory(pm.PyNode(changeObjs), groupLevels=True, pruneDagObjects=True, il=2,
                                     type='skinCluster')
            pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
            print ('OldSkin is not exist bind Jnt And Finished Copy And Bind ' + tslNewShape[0] + ' -> ' + changeObjs)


# 조인트-> 스킨 옮기기
# 조인트 왼 오 목록 부르기
def MoveSkin(tslpanel, z):
    tslOldShape = core.uitypes.TextScrollList(tslpanel[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tslpanel[1]).getAllItems()
    for i in range(len(tslNewShape)):
        SkinClur = pm.listConnections(tslNewShape[i], type='skinCluster')
        # 조인트 버텍스 선택
        getVerx = pm.skinCluster(SkinClur[0], selectInfluenceVerts=tslNewShape[i], e=1)
        pm.skinPercent(SkinClur[0], tmw=(tslNewShape[i], tslOldShape[i]))
        print ('MoveJointSkin ' + tslNewShape[i] + ' -> ' + tslOldShape[i])


def CleanUpSkin(tslpanel, z):
    print (tslpanel)
    tslOldShape = core.uitypes.TextScrollList(tslpanel[0]).getAllItems()
    print (tslOldShape)
    for i in range(len(tslOldShape)):
        pm.select(tslOldShape[i], r=1)
        mel.eval('removeUnusedInfluences')


def SetColor(i):
    selList = core.general.selected()
    for j in range(len(selList)):
        oldName = selList[j].getShape().name()
        newName = pm.rename(oldName, selList[j] + 'Shape')
        pm.setAttr(newName + '.overrideEnabled', 1)
        pm.setAttr(newName + '.overrideColor', i)


def CreatSets(*args):
    SetSelList = pm.ls(sl=1)
    pm.sets(SetSelList)


def ReplaceTsl(tsl, x):
    tsl.removeAll()

    sel = pm.general.selected()
    if sel[0].getShape() == None and pm.nodeType(sel) == 'transform':
        for i in sel:
            shape = i.getChildren(ad=1, type='mesh')
            obj = pm.pickWalk(shape, d='up')
            tsl.append(obj)
    else:
        tsl.append(sel)


def addToTsl(tsl, x):
    sel = core.general.selected()
    tslList = core.uitypes.TextScrollList(tsl).getAllItems()
    for i in sel:
        if i not in tslList:
            tsl.append(i)


def RemoveAllTsl(tsl, x):
    tsl.removeAll()


def RemoveSelTsl(tsl, x):
    delItem = core.uitypes.TextScrollList(tsl).getSelectItem()
    core.uitypes.TextScrollList(tsl).removeItem(delItem)


def MakeGroup():
    goupNameList = ['Grp', 'Group']
    selList = []
    selList = cmds.ls(sl=1)
    if len(selList) == 0:
        pm.group(em=True, name='Grp')

    elif goupNameList[0] in selList[0]:
        pm.group(selList[0], name=selList[0].split('Grp')[0] + goupNameList[1])

    elif goupNameList[0] and goupNameList[1] not in selList[0]:
        pm.group(selList[0], name=selList[0] + goupNameList[0])


def UnLockHideAll(Type, x):
    selList = pm.ls(sl=1)
    Attrlist = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
    for att in Attrlist:
        if Type == 'lock':
            for obj in selList:
                pm.setAttr(obj + '.' + att, lock=0)
        else:
            for obj in selList:
                pm.setAttr(obj + '.' + att, channelBox=1)
                pm.setAttr(obj + '.' + att, keyable=1)


def UnLockCheck(*args):
    selList = pm.ls(sl=1)
    Attrlist = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
    for att in Attrlist:
        getCheckBox = pm.checkBox(att, q=1, v=1)
        if getCheckBox == 1:
            for obj in selList:
                pm.setAttr(obj + '.' + att, lock=0)
        else:
            continue


def UnHideCheck(*args):
    selList = pm.ls(sl=1)
    Attrlist = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
    for att in Attrlist:
        getCheckBox = pm.checkBox(att, q=1, v=1)
        if getCheckBox == 1:
            for obj in selList:
                pm.setAttr(obj + '.' + att, channelBox=1)
                pm.setAttr(obj + '.' + att, keyable=1)
        else:
            continue


def CheckLockHide(*args):
    selList = cmds.ls(sl=1)
    Attrlist = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
    for Att in Attrlist:
        Lock = pm.getAttr(selList[0] + '.' + Att, lock=1)
        Hide = pm.getAttr(selList[0] + '.' + Att, keyable=1)
        if Lock == 1 or Hide == 0:
            pm.checkBox(Att, e=1, value=1)
        else:
            pm.checkBox(Att, e=1, value=0)


def getItemType(item):
    if item.type() == 'transform':
        if item.getShape():
            return item.getShape().type()
        else:
            return False
    else:
        return item.type()


def Move(type, x):
    selList = pm.ls(sl=1)
    cmd = 'pm.xform("{0}", ws=1, {1}={2})'
    cmdSub = 'pm.xform("{0}", q=1, ws=1, {1}=1)'
    cmdDic = {'TrsRot': 'm', 'Trs': 't', 'Rot': 'ro'}
    ex = ['clusterHandle']
    selType = getItemType(selList[0])
    for sel in selList[1:]:
        if selType in ex:
            attr = sel.name(), 't', selList[0].getPivots()[-1]
        else:
            attr = sel.name(), cmdDic[type], cmdSub.format(selList[0].name(), cmdDic[type])
        eval(cmd.format(attr[0], attr[1], attr[2]))


'''
def Move(type,x):
    selList = pm.ls(sl=1)
    if type == 'TrsRot':
        #TrsRot
        pm.xform(selList[1], ws=1, m=pm.xform(selList[0], q=1, m=1, ws=1))
    elif type == 'Trs':
        #Trs
        pm.xform(selList[1], ws=1, t=pm.xform(selList[0], q=1, t=1, ws=1))
    else:
        #Rot
        pm.xform(selList[1], ws=1, ro=pm.xform(selList[0], q=1, ro=1, ws=1))
'''


def MakeGroup(x):
    selList = pm.ls(sl=1)
    for sel in selList:
        shape = sel.getShape()
        if shape:
            shape.rename(sel.name() + 'Shape')
    for sel in selList:
        gp = pm.group(n=sel.name() + 'Grp', em=1)
        pm.xform(gp, ws=1, m=pm.xform(sel, q=1, ws=1, m=1))
        pm.parent(sel, gp)


def ConnecOneToAll(tsl, value, x):
    tslOldShape = core.uitypes.TextScrollList(tsl[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tsl[1]).getAllItems()
    # 뭐랑 트랜스할지 정보를 가져오고
    Attrlist = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
    checkAttrList = []
    for att in Attrlist:
        getCheckBox = pm.checkBox(att, q=1, v=1)
        if getCheckBox:
            checkAttrList.append(att)
    # 커넥 디스커넥 구분
    for i in range(len(tslOldShape)):
        tslOldShape[i]
        for at in checkAttrList:
            if value:
                pm.connectAttr(tslNewShape[0] + '.' + at, tslOldShape[i] + '.' + at)
            else:
                pm.disconnectAttr(tslNewShape[0] + '.' + at, tslOldShape[i] + '.' + at)


def ConnecOneToOne(tsl, value, x):
    tslOldShape = core.uitypes.TextScrollList(tsl[0]).getAllItems()
    tslNewShape = core.uitypes.TextScrollList(tsl[1]).getAllItems()
    # 뭐랑 트랜스할지 정보를 가져오고
    Attrlist = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
    checkAttrList = []
    for att in Attrlist:
        getCheckBox = pm.checkBox(att, q=1, v=1)
        if getCheckBox:
            checkAttrList.append(att)
    # 커넥 디스커넥 구분
    for i in range(len(tslOldShape)):
        for at in checkAttrList:
            if value:
                pm.connectAttr(tslNewShape[i] + '.' + at, tslOldShape[i] + '.' + at)
            else:
                pm.disconnectAttr(tslNewShape[i] + '.' + at, tslOldShape[i] + '.' + at)


def CheckBoxEdit(key, x):
    for at in ['t', 'r', 's']:
        for sd in ['x', 'y', 'z']:
            pm.checkBox(at + sd, e=1, value=key)
