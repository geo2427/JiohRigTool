#-*- coding: utf-8 -*-
import os, sys, imp
import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm


GSpath = "/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/"

################################################################################### AVS commands


def AdvancedSekelton5():
    avs_path = 'source "/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/util/modules/AdvancedSekeltonFix_9/AdvancedSkeleton5.mel"'
    mel.eval(avs_path)
    mel.eval(avs_path+';AdvancedSkeleton5;')


def importBiped():
    biped = GSpath + "util/modules/AdvancedSekeltonFix_9/AdvancedSkeleton5Files/fitSkeletons/GS_biped.ma"
    pm.importFile(biped)
    

def oldFitSetup():
    mel.eval('asFitSkeletonImport;')


def fitBuild():

    if pm.objExists('*.Asymmetry'):
        ifAsymmetryBuild('g_FitSkeleton')

    mel.eval('''
            optionMenu -e -v "Y" asPrimaryAxisOptionMenu;
            optionMenu -e -v "X" asSecondaryAxisOptionMenu;
            asAxisChanged;
            ''')
    
    mel.eval('asReBuildAdvancedSkeleton;')
       
       
def fitToggleAVS():
    mel.eval('asToggleFitAdvancedSkeleton;')


def fitReBuild():
    mel.eval('asReBuildAdvancedSkeleton;')


# def getJntList(jnt):
    
#     ArmL = [ "Shoulder", "Elbow", "Wrist" ]
#     LegL = [ "Hip", "Knee", "Ankle" ]
    
#     LegJntL = []
#     for jnt in pm.ls('Root', dag=True):
#         for arm in List:
#             if arm in str(jnt):
#                 LegJntL.append(jnt)

                    
################################################################################### Fit Setup


def fitSetup():
    
    with pm.UndoChunk():
        
        Root = pm.PyNode('Root')
        LegPartL = [ "Hip", "Knee", "Ankle" ]
        ArmPartL = [ "Shoulder", "Elbow", "Wrist" ]
        
        # All
        All = pm.ls(Root, dag=True)
        # [ pm.addAttr(jnt, sn='freeOrient', at='bool', dv=0, k=1) for jnt in All ]
        for jnt in All:
            if not pm.objExists(jnt+'.freeOrient'):
                pm.addAttr(jnt, sn='freeOrient', at='bool', dv=0, k=1)
                pm.setAttr(jnt+'.freeOrient', k=1)
            else:
                pm.setAttr(jnt+'.freeOrient', k=1)
                
        # Spine
        spine01 = pm.PyNode("Spine1")
        spine02 = pm.duplicate(spine01, po=1)[0]
        pm.setAttr(spine02.tx, 0.355)
        pm.parent(spine01, spine02)
        pm.parent(spine02, Root)
        pm.rename(spine01, "Spine2")
        pm.rename(spine02, "Spine1")

        pm.setAttr(Root.numMainExtras, 2)
        pm.setAttr(Root.inbetweenJoints, 0)
        pm.setAttr(spine01.inbetweenJoints, 1)
        pm.setAttr(spine02.inbetweenJoints, 1)

        # Arm
        for i in range(2):
            jnt = pm.PyNode(ArmPartL[i])
            pm.setAttr(jnt.bendyJoints, 1)
            pm.setAttr(jnt.twistJoints, 3)
        
        Shoulder = pm.PyNode(ArmPartL[0])
        pm.addAttr(Shoulder, sn='ikLocal', at='enum', k=1, en='addCtrl:noneZero:localOrient', dv=0)
        pm.addAttr(Shoulder, sn='global', at='double', k=1, dv=10, min=0, max=10)
        pm.addAttr(Shoulder, sn='globalTranslate', at='bool', k=1, dv=1)

        Wrist = pm.PyNode(ArmPartL[2])
        pm.addAttr(Wrist, sn='ikLocal', at='enum', k=1, en='addCtrl:noneZero:localOrient') 
        pm.setAttr(Wrist.ikLocal, 0)
        pm.select('Chest', 'Wrist')
        pm.addAttr(Wrist, sn='ikFollow', at='enum', k=1, en='Chest')
        pm.select(cl=1)

        # Leg
        Hip = pm.PyNode(LegPartL[0])
        pm.addAttr(Hip, sn='ikLocal', at='enum', k=1, en='addCtrl:noneZero:localOrient', dv=0)
        pm.addAttr(Hip, sn='global', at='double', k=1, dv=10, min=0, max=10)
        pm.addAttr(Hip, sn='globalTranslate', at='bool', k=1, dv=1)
        pm.setAttr(Hip.bendyJoints, 1)
        pm.setAttr(Hip.twistJoints, 3)

        Knee = pm.PyNode(LegPartL[1])
        pm.addAttr(Knee, sn='bendyJoints', at='bool', k=1, dv=1)
        pm.addAttr(Knee, sn='twistJoints', at='long', k=1, dv=3, min=0, max=10)

        Ankle = pm.PyNode(LegPartL[2])
        # pm.addAttr(Ankle, sn='ikLocal', at='enum', k=1, en='addCtrl:noneZero:localOrient') 
        pm.setAttr(Ankle.worldOrient, 4)

        pm.select(cl=1)
        pm.displayInfo('FitSkeleton Attribute Setup Completed')
        
        
def autoOrientSetup():
    
    with pm.UndoChunk():
        
        jntL = pm.ls('Root', dag=True)

        [ pm.setAttr(jnt.freeOrient, 0) for jnt in jntL if jnt.freeOrient == 0 ]
        
        mel.eval('''
                optionMenu -e -v "Y" asPrimaryAxisOptionMenu;
                optionMenu -e -v "Z" asSecondaryAxisOptionMenu;
                asAxisChanged;
                ''')

        # pm.makeIdentity("EyeEnd", apply=True)
        # pm.parent("Hip", w=1)
        # pm.joint("Hip", oj='yzx', sao='zup', e=True, ch=True, zso=True)
        # pm.joint("Root", oj='yzx', sao='zup', e=True, ch=True, zso=True)
        # pm.parent("Hip", "Root")
        pm.joint("Wrist*", oj='yzx', sao='xup', e=True, ch=True, zso=True)

        [ pm.setAttr(jnt.freeOrient, 1) for jnt in jntL]

        pm.select(cl=1)
        pm.displayInfo('Auto-Oreint Complete')


################################################################################### Asymmetry

def getAsymmetryJnt():
    
    # asymmetryJntL = [ 'Scapula', 'Hip', 'Eye' ]
    
    asymmetryJntL = []
    for jnt in pm.ls('Root', dag=True):
        for arm in [ 'Scapula', 'Hip', 'Eye' ]:
            if arm in str(jnt):
                asymmetryJntL.append(jnt)
    asymmetryJntL.remove('EyeEnd')
    
    return asymmetryJntL


def asymmetrySetup():
    
    with pm.UndoChunk():
        
        if not pm.objExists('*.Asymmetry'):
            
            asymmetryJntL = getAsymmetryJnt()
            for jnt in asymmetryJntL:
                
                jnt = pm.PyNode(jnt)
                pm.addAttr(jnt, sn='Asymmetry', at='bool', dv=1, k=1)
                
                R_jnts = pm.ls(jnt, dag=True)
                [ pm.rename(j, 't_'+j) for j in R_jnts ]

                L_jnt = pm.mirrorJoint(jnt, myz=1, mb=1, sr=('t_', 'g_'))
                [ pm.rename(j, j+'_L') for j in pm.ls(L_jnt, dag=True) ]
                [ pm.rename(str(j), str(j)[2:]) for j in R_jnts]

            pm.select(cl=1)
            pm.displayInfo('Asymmetry Joints Mirrored')
            
        else:
            pm.warning('Asymmetry Joints Already Exists')
        

def delAsymmetrySetup():
    
    with pm.UndoChunk():
        
        if pm.objExists('g_Corrective_L'):
            pm.delete('g_Corrective_L')
        
        asymmetryJntL = getAsymmetryJnt()
        for jnt in asymmetryJntL:
            if pm. objExists(jnt+'.Asymmetry'):
                pm.delete('g_'+jnt+'_L')
                pm.deleteAttr(jnt+'.Asymmetry')

        pm.displayInfo('Asymmetry Guide Deleted')


def ifAsymmetryBuild(grp):
    
    with pm.UndoChunk():
        
        for part in [ 'Scapula', 'Hip', 'Eye' ]:
            jnt = 'g_'+part+'*_L'
            
            if not pm.objExists(grp):
                pm.group(n=grp, w=1, em=True)
            
            pm.parent(pm.ls(jnt, dag=True), grp)
            
        pm.hide(grp)


def correctAsymmetryPV():
    
    with pm.UndoChunk():
    
        if pm.objExists('g_FitSkeleton'):
            pm.displayInfo('correct PoleVector')
            
        
################################################################################### Pre Rig


def editMainName():
    
    pm.rename('Main', 'Main')
    pm.rename('MainExtra1', 'Globe')
    pm.rename('MainExtra2', 'World')
    

def milkiHierarchy():
    
    filePath = cmds.file(q=True, sn=True)
    fileName = os.path.basename(filePath)
    ChName = fileName.split('_')[0]
    
    if not pm.objExists(ChName+'_rig'):
        
        allGrp = pm.group(n=ChName+'_rig', em=True)
        geoGrp = pm.group(n='geo', em=True, p=allGrp)
        rigGrp = pm.group("Group", n='rig', p=allGrp)
        subRigGrp = pm.group(n='SubRigGrp', em=True, p=rigGrp)
    
        geo = ChName+'_GRP'
        if pm.objExists(geo):
            pm.parent(geo, geoGrp)
        else:
            pass
        
        if pm.objExists('CorrectiveRigGrp'):
            pm.parent('CorrectiveRigGrp', 'SubRigGrp')
        
        pm.select(cl=1)
        pm.displayInfo('Milki Hierarchy Completed')
    
    else:
        pm.warning('Milki Hierarchy Already Done')


def addIKSubArm():
    
    if not pm.objExists('IKSubArm*'):

        for dir in [ '_L', '_R' ]:

            ctrl = pm.PyNode('IKArm'+dir)
            pm.addAttr(ctrl, sn='Twist', at='double', dv=0, k=1)
            pm.connectAttr(ctrl.Twist, 'IKArmHandle'+dir+'.twist')

            # IKlist = pm.listRelatives(ctrl)
            IKlist = [ 'IKArmHandle'+dir, 'IKFKAlignedOffsetArm'+dir, 'IKLocalOffsetArm'+dir, 'IKmessureConstrainToArm'+dir ]
            tmpGrp = pm.group(IKlist)
            pm.parent(tmpGrp, w=1)

            name = 'IKSubArm'+dir
            SubGrp = pm.duplicate(pm.pickWalk(ctrl, d='up'), n='IKExtraArmSub'+dir)[0]
            Sub = pm.rename(pm.pickWalk(SubGrp, d='down'), name)
            
            shape = pm.PyNode(name+'Shape')
            pm.scale(shape+'.cv[:]', 0.8,0.8,0.8)
            pm.setAttr(shape+'.overrideEnabled', 1)
            pm.setAttr(shape+'.overrideColor', 20)

            pm.parent(SubGrp, ctrl)
            pm.parent(IKlist, Sub)
            pm.delete(tmpGrp)
            
            [pm.deleteAttr(Sub, at=attr) for attr in ['stretchy', 'antiPop', 'Lenght1', 'Lenght2', 'Fatness1', 'Fatness2', 'volume', 'ikFollow', 'Twist', 'follow']]

        pm.select(cl=1)
        pm.displayInfo('IKSubArm Add Completed')
        
    else:
        pm.warning('IKSubArm Already Exists')


def createOnOffCtrl():
    
    posL = pm.xform('Wrist_L', q=1, ws=1, rp=1)
    f_posL = [float(item) for item in posL]
    posX = f_posL[0] 
    posY = f_posL[1] - f_posL[1]/2.5
    pos = ( posX, posY, 0 )

    if not pm.objExists("onoffCtrl"):
        
        onoff = pm.curve(n='onoffCtrl', d=1, p=[(-0.45800349939820273, 0.3670367720320906, 0.0), (-0.49026301228499386, 0.5181642615814636, 0.0), (-0.5657577509362233, 0.8177956482622923, 0.0), (-0.6628684028114601, 1.1350232564928775, 0.0), (-0.6887643953479796, 1.28068906433991, 0.0), (-0.6822903972138494, 1.4134065359870402, 0.0), (-0.6499204065431992, 1.523465184130536, 0.0), (-0.5819429162373703, 1.6043906707046236, 0.0), (-0.49451283768131327, 1.639727244820618, 0.0), (-0.40066994868680117, 1.6141018378716416, 0.0), (-0.33269245838097145, 1.5655463419682019, 0.0), (-0.2591237724169555, 1.4636814061389658, 0.0), (-0.2127693338996275, 1.3169590907466004, 0.0), (-0.1981192998966555, 1.1621613592516145, 0.0), (-0.18268062448275244, 0.8513186870647866, 0.0), (-0.1692659020691439, 0.7050845135112553, 0.0), (-0.14818266172915898, 0.630048682577593, 0.0), (-0.09507208181430767, 0.5683585679340828, 0.0), (-0.03812401358566301, 0.5944415228740564, 0.0), (0.006157691740651018, 0.6588487111372094, 0.0), (0.02146324992329523, 0.8134727375628047, 0.0), (0.01053247600880539, 1.1215752207782894, 0.0), (0.0030055532088553187, 1.430080183058665, 0.0), (0.04036722249546215, 1.579740187706748, 0.0), (0.0881194599273368, 1.6691309919775668, 0.0), (0.17551894463555626, 1.7371084822833969, 0.0), (0.2664615368550404, 1.7619445679581576, 0.0), (0.334132748750849, 1.7371084822833969, 0.0), (0.3948469196483318, 1.6815198006936811, 0.0), (0.43124340062608485, 1.6173386669728864, 0.0), (0.455286085846917, 1.5412925591972875, 0.0), (0.46453902515965073, 1.3869816098145673, 0.0), (0.40346826596903546, 1.0839410486896737, 0.0), (0.32709446408993187, 0.7829336187194286, 0.0), (0.29619433784206856, 0.6366283994525854, 0.0), (0.30176275808019853, 0.5588343631705203, 0.0), (0.33072085485364394, 0.49454139193929486, 0.0), (0.3988730700237918, 0.5167532053328534, 0.0), (0.4533141423879466, 0.5744195491224021, 0.0), (0.578915824959637, 0.8532552776329211, 0.0), (0.6132448416868371, 1.0032045641088942, 0.0), (0.6777291944328698, 1.1432135694907104, 0.0), (0.7355230125884095, 1.2224227412010957, 0.0), (0.8293964954307592, 1.2645038990387643, 0.0), (0.9336895629833927, 1.2597288792545613, 0.0), (0.9815363014119229, 1.203000746798707, 0.0), (1.0068115787689769, 1.125291693427302, 0.0), (0.9936470460443534, 0.9749378882965845, 0.0), (0.9295923668946205, 0.8331585189198858, 0.0), (0.7885921208428582, 0.5589152669014692, 0.0), (0.7134006012168658, 0.25967582140460704, 0.0), (0.6541392981600378, -0.20009940171504922, 0.0), (0.5697046972389478, -0.4965136753299079, 0.0), (0.48717609303815534, -0.6268336091014789, 0.0), (0.3748664175570797, -0.7326590884991449, 0.0), (0.24196708248113638, -0.8110870972947384, 0.0), (0.0958461061646051, -0.8608405123068504, 0.0), (-0.057388619637509596, -0.8787654477550426, 0.0), (-0.2102113482887411, -0.857998683774358, 0.0), (-0.35226776195419346, -0.7979252840232564, 0.0), (-0.4769614871083854, -0.7069238836295951, 0.0), (-0.6774715262477469, -0.47262973818618925, 0.0), (-0.8186869490293015, -0.19823045754379967, 0.0), (-0.8708311032841191, -0.0532598099059712, 0.0), (-0.948394325980831, 0.07983804524927565, 0.0), (-1.0763915068382237, 0.16517210529679796, 0.0), (-1.2124029161025613, 0.23854567049793732, 0.0), (-1.3165453939375036, 0.3508805009205689, 0.0), (-1.3555899424114435, 0.43259054972587735, 0.0), (-1.3685379386797047, 0.5232272034669837, 0.0), (-1.3491159442773124, 0.5944415228740564, 0.0), (-1.2940864502397433, 0.6656558422811296, 0.0), (-1.1969761382961506, 0.6947890038505367, 0.0), (-1.1128134826891745, 0.6915518348176499, 0.0), (-1.0278666047826215, 0.6715336003140638, 0.0), (-0.8989278132751083, 0.5879559670640766, 0.0), (-0.7902849804232197, 0.47586792701400393, 0.0), (-0.6965308135874367, 0.3568860732511376, 0.0), (-0.6369720703432971, 0.2869247418788449, 0.0), (-0.5742240884278825, 0.2707620120661133, 0.0), (-0.5010174296632808, 0.3063470762128781, 0.0), (-0.45800349939820273, 0.3670367720320906, 0.0)] )
        onoffShape = 'onoffCtrlShape' 
        pm.setAttr(onoffShape+'.overrideEnabled', 1)
        pm.setAttr(onoffShape+'.overrideColor', 6)
        sca = pm.getAttr('FitSkeleton.scaleX')/1.5
        pm.scale(onoffShape+'.cv[:]', sca,sca,sca)
        
        for srt in [ 's', 'r', 't' ]:
            for xyz in [ 'x', 'y', 'z' ]:
                attr = srt+xyz
                pm.setAttr(str(onoff)+'.'+attr, lock=True, keyable=False, channelBox=False)
        
        pm.addAttr(onoff, sn='Main', at='bool', k=1, dv=1)
        pm.addAttr(onoff, sn='Finger', at='bool', k=1, dv=0)
        pm.addAttr(onoff, sn='Bend', at='bool', k=1, dv=0)
        
        main = pm.PyNode('Main')
        pm.connectAttr(onoff.Main, main.fkVis)
        pm.connectAttr(onoff.Main, main.ikVis)
        pm.connectAttr(onoff.Main, main.fkIkVis)
        pm.connectAttr(onoff.Finger, main.fingerVis)
        pm.connectAttr(onoff.Finger, main.drvSysVis)
        pm.connectAttr(onoff.Bend, main.bendVis)
        
        onoffGrp = pm.group(onoff, n='onoffCtrl_grp')
        pm.setAttr(onoffGrp.t, pos)
        pm.parentConstraint(main, onoffGrp, mo=1)
        pm.scaleConstraint(main, onoffGrp, mo=1)
        pm.parent(onoffGrp, 'SubRigGrp')
            
        pm.select(cl=1)
        pm.displayInfo('onoffCtrl Completed')
        
    else:
        pm.warning('onoffCtrl Already Exists')
        

def setCtrlCrvsShape():
    
    shape_path = 'source "'+ GSpath + 'util/AdvancedSekeltonFix_9/ctrlCrvs.mel"'
    mel.eval(shape_path)


################################################################################### Post Rig


def pubCheck():
    
    with pm.UndoChunk():

        for side in [ '_L', '_R' ]:
            
            for part in [ 'Shoulder', 'Hip' ]:
                ctrl = 'FK' + part + side
                pm.setAttr(ctrl+'.Global', 0)
                pm.setAttr(ctrl+'.GlobalTranslate', 0)

            for part in [ 'Arm', 'Leg' ]:
                ctrl = 'FKIK' + part + side
                if part == 'Arm':
                    pm.setAttr(ctrl+'.FKIKBlend', 0)
                else:
                    pm.setAttr(ctrl+'.FKIKBlend', 10)

        main = pm.PyNode('Main')
        pm.setAttr(main.jointVis, 0)

        onoff = pm.PyNode('onoffCtrl')
        pm.setAttr(onoff.Finger, 0)
        pm.setAttr(onoff.Bend, 0)
        
        subs = pm.listRelatives('SubRigGrp')
        for sub in subs:
            if sub == onoff:
                pass
            else:
                pm.hide(sub)

        # OPTIMIZE SCENE SIZE
        pm.mel.source('cleanUpScene')
        pm.mel.scOpt_performOneCleanup({
            'setsOption',
            'displayLayerOption'
            'renderLayerOption',
            'animationCurveOption',
            'unusedSkinInfsOption',
            'referencedOption',
            'referencedOption',
            'brushOption',
            'unknownNodesOption',
            'shadingNetworksOption'
            }
        )

        pm.displayInfo("Pub Check Complete")


def fixAVSHeadSquash():
    
    if pm.objExists('FaceJoint_M'):

        # DELETE 'AVS HEADSQUASH RIG' IF IT EXIST
        if pm.objExists("SquashControls"):
            pm.mel('asDeleteHeadSquash;')

        # CHANGE HEAD PART SKINNING METHOD
        for jnt in pm.listConnections('FaceJoint_M'):
            if pm.nodeType(jnt) == 'joint':
                for faceSkin in pm.listConnections(jnt):
                    if pm.nodeType(faceSkin) == 'skinCluster':
                        pm.setAttr(faceSkin+'.skinningMethod', 0)

        # DISCONNECT FaceMotionSystem
        FaceMotion = pm.PyNode("FaceMotionSystem")
        pm.disconnectAttr(FaceMotion+'.scale')
        pm.delete('FaceMotionSystem_pointConstraint1')
        pm.delete('FaceMotionSystem_orientConstraint1')

        # CONNECT FaceOnControlSystem
        FaceOnControl = pm.group(n="FaceOnControlSystem")

        pm.parent(FaceOnControl, FaceMotion)
        pm.setAttr(FaceOnControl+'.translate', (0,0,0))
        pm.parent('ControlsSetup', 'ConstrainedSetup', FaceOnControl)

        pm.pointConstraint('Head_M', FaceOnControl, mo=1)
        pm.orientConstraint('Head_M', FaceOnControl, mo=1)

        # CONNECT SCALE
        LRA = ['X', 'Y', 'Z']
        HeadScale = pm.PyNode("MainAndHeadScaleMultiplyDivide.output")
        FaceDefrom = pm.PyNode("FaceDeformationFollowHead")

        pm.disconnectAttr(FaceDefrom+'.scale')
        for i in range(3):
            pm.connectAttr(HeadScale+LRA[i-1], FaceDefrom+'.scale'+LRA[i])
            pm.connectAttr(HeadScale+LRA[i-1], FaceOnControl+'.scale'+LRA[i])

        # AimEyeFollow_M, ctrlBoxOffset
        HeadScale >> pm.PyNode("AimEyeFollow_M").scale
        pm.parentConstraint('Head_M', 'ctrlBoxOffset', mo=1)
        pm.parent('Aimcontrols', 'ctrlBoxOffset', 'FaceMotionSystem')

        # TONGUE
        for i in range(4):
            tongue = 'Tongue'+str(i)
            pm.delete(tongue + "Joint_M_scaleConstraint1")
            pm.PyNode(tongue + "_M").scale >> pm.PyNode(tongue + "Joint_M").scale

        # LIP
        LipSetup = [pm.PyNode("LipFollicles"), pm.PyNode("LipRibbonJoints")]
        for j in range(len(LipSetup)):
            pm.delete(LipSetup[j]+"_scaleConstraint1")
            for i in range(3):
                pm.connectAttr(HeadScale+LRA[i-1], LipSetup[j]+'.scale'+LRA[i])

        pm.select(cl=1)
        pm.displayInfo("HeadSquash Edit Compelete")


def makeOffsetGrp():

    sel = pm.ls(sl=1)

    if sel:
        for x in sel:
            GRPName = '%s_grp'%x

            if not pm.ls(GRPName):
                pm.select(x)
                parentName = pm.pickWalk(d='up')
                groupName = pm.group(em=1)
                offGrp = pm.rename(groupName,GRPName)
                pm.delete(pm.parentConstraint(x,GRPName,mo=0))
                pm.parent(x,GRPName)

                if not x == parentName[0]:
                    print ( parentName,x )
                    pm.parent(GRPName,parentName)


def GS_MTX2():
    
    mtx_path = "/usersetup/linux/scripts/maya_sc/MTXassignSHD2"
    if mtx_path not in sys.path:
        sys.path.append(mtx_path)
        
    # import MTX2_engine_selected
    from . import MTX2_engine_selected
    imp.reload(MTX2_engine_selected)
    _engine = MTX2_engine_selected.MTX2()
    _engine.run()


def GeneratePreview(sel):
	
    for ch in sel:
        chName = ch.split('_')[0]
        nameSpaces = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
        
        for item in nameSpaces:
            
            if chName and '_anim' in item:
                pm.select(item+':*')
                
                for shader in pm.selected():
                    
                    if shader.nodeType() == 'file':
                        mel.eval('generateUvTilePreview ' + shader + ';')
                        pm.displayInfo(shader+'Generate Preview Completed')
                        

def RunAfterShader():
    
    if pm.objExists('CH'):
        ch_list = pm.listRelatives('CH')
        GeneratePreview(ch_list)
    else:
        pm.warning('CH 그룹이 없습니다. 캐릭터의 상위 그룹을 선택해주세요.')
        GeneratePreview(pm.selected())
    
    for file in pm.ls(type='reference'):
        if file.split('_')[1] == 'anim':
            ref = pm.referenceQuery(file, f=True)
            cmds.file(ref, importReference=True)
            pm.displayInfo('Import Referenced Shader')

