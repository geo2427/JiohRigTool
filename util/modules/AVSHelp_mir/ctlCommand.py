# -*- coding: utf-8 -*-
from pymel.core import *

# making float Attr #
def floatAttr(Ctrl, LongName, Keyable = True, min=0, max=10):
    attr = '{}.{}'.format(Ctrl, LongName)
    if objExists(attr):
        PyNode(attr).delete()
    addAttr(Ctrl, ln=LongName, at='float', min=min, max=max, dv=0)
    if Keyable == False:
        setAttr(Ctrl + '.' + LongName, cb=1)
    elif Keyable == True:
        setAttr(Ctrl + '.' + LongName, k=1)
    return PyNode(attr)

# making bool Attr #
def boolAttr(Ctrl, LongName, Keyable = False):
    attr = '{}.{}'.format(Ctrl, LongName)
    if objExists(attr):
        PyNode(attr).delete()
    addAttr(Ctrl, ln=LongName, at='bool', dv=0)
    if Keyable == False:
        setAttr(Ctrl + '.' + LongName, cb=1)
    elif Keyable == True:
        setAttr(Ctrl + '.' + LongName, k=1)
    return PyNode(attr)

class ctlCommand():
    def __init__(self):
        pass
    # controllerCleaning Script
    #lock_v
    def visAllLock(self, body = True, head = True):
        if objExists('ControlSet'):
            ControlSet = PyNode('ControlSet')
            
            if body == True:
                body_CTRL = [x for x in ControlSet if x.listRelatives(c=1,s=1)]
                for x in body_CTRL:
                    x.v.lock()
                    x.v.setKeyable(0)
        
        else: print ('there is no "ControlSet" which is adv_body made, in the Scene')
        
        
        if objExists('FaceControlSet'):
            FaceControlSet = PyNode('FaceControlSet')
            
            if head == True:
                face_CTRL = [x for x in FaceControlSet if x.listRelatives(c=1,s=1)]
                for x in face_CTRL:
                    x.v.lock()
                    x.v.setKeyable(0)
            
        else: print ('there is no "FaceControlSet" which is adv_Face made, in the Scene')

    #lock_r/s
    def Lock_lock_dict(self, lock_dict):
        for ctl in lock_dict.keys():
            for attr in lock_dict[ctl]:
                _attr = PyNode('{}.{}'.format(ctl,attr))
                _attr.lock()
                _attr.setKeyable(0)

    #deleteEmotions
    def deleteEmotions(self):
        emotions = objExists('ctrlBoxEmotions_M')
        if emotions:
            delete('ctrlBoxEmotions_M')

    #RegionCTL_Fix
    def RegionFix(self):
        LayerScale = PyNode('OnFacecontrolsLayered')
        _scale = LayerScale.s.get()
        # _unscale = (1/_scale[0], 1/_scale[1], 1/_scale[2])
        
        side = ['L','R']
        
        for lr in side:
            Region = PyNode('EyeRegion_{}'.format(lr))
            Eye = PyNode('Eye_{}'.format(lr))
            scaleFactor = createNode('multiplyDivide', n = 'Region_{}_scaleConvert'.format(lr))
            scaleFactor.input2.set(_scale)
            # unscaleFactor = createNode('multiplyDivide', n = 'Region_{}_unscaleConvert'.format(lr))
            # unscaleFactor.input2.set(_unscale)
            if lr == 'L':
                Region.t>>scaleFactor.input1
                scaleFactor.output>>Eye.t
                Region.r>>Eye.r
                # Region.s>>unscaleFactor.input1
                # unscaleFactor.input1>>Eye.s
            if lr == 'R':
                Region.t>>scaleFactor.input1
                scale_input2Reverse = (_scale[0]*-1, _scale[1], _scale[2])
                scaleFactor.input2.set(scale_input2Reverse)
                scaleFactor.output>>Eye.t
                mirrorFactor = createNode('multiplyDivide', n = 'Region_{}_mirrorConvert'.format(lr))
                Region.r>>mirrorFactor.input1
                mirrorFactor.input2.set(1,-1,-1)
                mirrorFactor.output>>Eye.r
                # Region.s>>unscaleFactor.input1
                # unscaleFactor.output>>Eye.s

    #HeadCTL_visControl
    def FKHead_M_vis_setting(self):
        Head = PyNode('FKHead_M')
        Box = PyNode('ctrlBox')
        faceRigVis_1 = PyNode('ctrlBoxOffset')
        faceRigVis_2 = PyNode('OnFacecontrolsLayered')
        
        boolAttr(Head,'facialCtrlVis')
        boolAttr(Head,'RegionsCtrlVis')
        
        Head.RegionsCtrlVis>>Box.RegionsCtrlVis
        Box.limits.set(1)
        Head.facialCtrlVis>>faceRigVis_1.v
        Head.facialCtrlVis>>faceRigVis_2.v
        
    def set_faceCTRL_userdefine_attr(self, faceCTRL_userdefine_attr_dict):
        _dict = faceCTRL_userdefine_attr_dict
        for attr in _dict.keys():
            
            for x in range(len(_dict[attr]['ud_attr'])):
                ud_attr = _dict[attr]['ud_attr'][x]
                _value = _dict[attr]['value'][x]
                setAttr(ud_attr, _value)
    
    ## CTRL maker ##
    def makeCurveFromFaceSelection(self, rebuild=True):
        mel.eval('ConvertSelectionToEdgePerimeter')

        org_edges = ls(sl=1, fl=1)
        one_edge = org_edges[0]
        org_mesh = listRelatives(one_edge.split('.e')[0], p=1)[0]
        org_mesh_shape = listRelatives(org_mesh, s=1)[0]

        temp = duplicate(org_mesh, n = 'temp')[0]
        temp_shape = listRelatives(temp, s=1)[0]

        temp_edges = [PyNode(x.replace(str(org_mesh_shape), str(temp_shape))) for x in org_edges]
        select(temp_edges)
        polyExtrudeEdge(ltz=0.02)
        polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1)

        extruded_curve = ls(sl=1)[0]
        if rebuild == True:
            _curve = rebuildCurve(extruded_curve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=8, d=3, tol=0.01)[0]
        else:
            _curve = extruded_curve
        delete(_curve, constructionHistory = True)
        delete(temp)
        return _curve

    def makeCurveFromFaceSelection_v02(self, mirror=True, rebuild=True):
        selected_face = ls(sl=1)
        _curve = self.makeCurveFromFaceSelection(rebuild)
        if mirror:
            mel.eval('reflectionSetMode objectx;')
            select(selected_face, sym=1)
            select(selected_face, d=1)
            mel.eval('reflectionSetMode none')
            mirrored_curve = self.makeCurveFromFaceSelection(rebuild)
            rename(mirrored_curve, str(_curve)+'_mirrored')
            
    # two curve selection is needed (modification to original)
    def switchCurve_worldCurve(self, sels):
        mod = sels[0]
        mod_shape = listRelatives(mod, s=1)[0]
        org = sels[1]
        org_shape = listRelatives(org, s=1)[0]
        org_shape_name = str(org_shape)
        
        #color
        mod_shape.overrideEnabled.set(1)
        
        if org_shape.overrideRGBColors.get() == 0:
            color_index = org_shape.overrideColor.get()
            mod_shape.overrideColor.set(color_index)
        else:
            color_vector = org_shape.overrideColorRGB.get()
            mod_shape.overrideRGBColors.set(1)
            mod_shape.overrideColorRGB.set(color_vector)
            
        #swap
        parent(mod, org)
        makeIdentity(mod, apply=1)
        makeIdentity(mod)
        delete(org_shape)
        parent(mod_shape, org, r=1, s=1)
        rename(mod_shape, org_shape_name)
        delete(mod)

    def switchCurve_worldCurve_v02(self, sels, mirror=1):
        sels = ls(sl=1)
        self.switchCurve_worldCurve(sels)
        
        if mirror:
            #mirroring
            if '_L' in str(sels[1]):
                side = '_L'
                mirror_side = '_R'
            elif '_R' in str(sels[1]):
                side = '_R'
                mirror_side = '_L'
            
            mirrored_sels = [PyNode(sels[0]+'_mirrored'), PyNode(sels[1].replace(side, mirror_side))]
            self.switchCurve_worldCurve(mirrored_sels)
            
    def eyeCurveGuideSetUp(self):
        guide_group = 'eye_guide_curvesGRP'
        head = 'FKHead_M'
        
        group(em=1, n=guide_group)
        parent(guide_group, 'FaceGroup')

        boolAttr(head, 'eyeMainAimCrvVis')
        boolAttr(head, 'eyeOuterAimCrvVis')
        parentConstraint(head, guide_group, mo=1)
    
    def eyeCurveVis(self, curves, main=True):
        head = PyNode('FKHead_M')
        for x in curves:
            x_shape = listRelatives(x, s=1)[0]
            guide = duplicate(x, n=x+'_guideCRV')[0]
            guide_shape = listRelatives(guide, s=1)[0]
            x_shape.worldSpace>>guide_shape.create
            parent(guide, 'eye_guide_curvesGRP')
            guide.t.lock()
            guide.r.lock()
            guide.s.lock()
            guide.v.lock()
            if main == True:
                head.eyeMainAimCrvVis>>guide_shape.v
            else:
                head.eyeOuterAimCrvVis>>guide_shape.v
    
    def eyeRigFix(self):
        side = ['_L', '_R']
        upper_lower = ['upper', 'lower']

        for lr in side:
            for ul in upper_lower:
                lid_outer_CTL = PyNode('{}LidOuter{}'.format(ul, lr))
                floatAttr(lid_outer_CTL, 'lidOut')
                lid_main_aim_ends = ls('{}LidMain*AimEnd{}'.format(ul, lr))
                lid_outer_aim_ends = ls('{}LidOuter*AimEnd{}'.format(ul, lr))
                
                if 'upper' == ul:
                    del lid_main_aim_ends[-1]
                    del lid_outer_aim_ends[-1]
                    
                    del lid_main_aim_ends[0]
                    del lid_outer_aim_ends[0]
                    
                for source, target in zip(lid_main_aim_ends, lid_outer_aim_ends):
                    mult_float = source.tx.listConnections()[0].input1D[1].listConnections()[0].input1X.get()*0.1
                    target_org_value = target.tx.get()
                    num = str(source[source.index('Main')+4:source.index('Aim')])
                    
                    _mult = createNode('multiplyDivide', n = '{}LidOutMult{}{}'.format(ul,num,lr))
                    _mult.input1X.set(mult_float)
                    _plus = createNode('plusMinusAverage', n = '{}LidOut{}{}'.format(ul,num,lr))
                    _plus.input1D[0].set(target_org_value)
                    
                    lid_outer_CTL.lidOut>>_mult.input2X
                    _mult.outputX>>_plus.input1D[1]
                    _plus.output1D>>target.tx
                    
    def create_layered_CTL(self, name, color=1):
        pointTuple = ((-0.015305999997299584, 4.090074305739947e-15, -3.6658060582704184e-16),
                    (-0.014540699997434604, 0.004744859999167015, -3.6658060582704184e-16),
                    (-0.012397859997812668, 0.009030539998410926, -3.6658060582704184e-16),
                    (-0.009030539998406712, 0.01239785999781689, -3.6658060582704184e-16),
                    (-0.004744859999162775, 0.014540699997438842, -3.6658060582704184e-16),
                    (1.4793461562439361e-16, 0.015305999997303832, -3.6658060582704184e-16),
                    (0.004744859999163076, 0.014540699997438842, -3.6658060582704184e-16),
                    (0.009030539998406995, 0.01239785999781689, -3.6658060582704184e-16),
                    (0.01239785999781296, 0.009030539998410926, -3.6658060582704184e-16),
                    (0.01454069999743487, 0.004744859999167015, -3.6658060582704184e-16),
                    (0.015305999997299879, 4.090074305739947e-15, -3.6658060582704184e-16),
                    (0.01454069999743487, -0.004744859999158833, -3.6658060582704184e-16),
                    (0.01239785999781296, -0.009030539998402757, -3.6658060582704184e-16),
                    (0.009030539998406995, -0.012397859997808734, -3.6658060582704184e-16),
                    (0.004744859999163076, -0.01454069999743066, -3.6658060582704184e-16),
                    (1.4793461562439361e-16, -0.015305999997295709, -3.6658060582704184e-16),
                    (-0.004744859999162775, -0.01454069999743066, -3.6658060582704184e-16),
                    (-0.009030539998406712, -0.012397859997808734, -3.6658060582704184e-16),
                    (-0.012397859997812668, -0.009030539998402757, -3.6658060582704184e-16),
                    (-0.014540699997434604, -0.004744859999158833, -3.6658060582704184e-16),
                    (-0.015305999997299584, 4.090074305739947e-15, -3.6658060582704184e-16),
                    (-0.014540699997434604, 4.090074305739947e-15, 0.00474485999916258),
                    (-0.012397859997812668, 4.090074305739947e-15, 0.009030539998406457),
                    (-0.009030539998406712, 4.090074305739947e-15, 0.012397859997812476),
                    (-0.004744859999162775, 4.090074305739947e-15, 0.014540699997434445),
                    (1.4793461562439361e-16, 4.090074305739947e-15, 0.015305999997299436),
                    (0.004744859999163076, 4.090074305739947e-15, 0.014540699997434445),
                    (0.009030539998406995, 4.090074305739947e-15, 0.012397859997812476),
                    (0.01239785999781296, 4.090074305739947e-15, 0.009030539998406457),
                    (0.01454069999743487, 4.090074305739947e-15, 0.00474485999916258),
                    (0.015305999997299879, 4.090074305739947e-15, -3.6658060582704184e-16),
                    (0.01454069999743487, 4.090074305739947e-15, -0.004744859999163271),
                    (0.01239785999781296, 4.090074305739947e-15, -0.009030539998407227),
                    (0.009030539998406995, 4.090074305739947e-15, -0.012397859997813145),
                    (0.004744859999163076, 4.090074305739947e-15, -0.014540699997435047),
                    (1.4793461562439361e-16, 4.090074305739947e-15, -0.015305999997300025),
                    (1.4793461562439361e-16, 0.004744859999167015, -0.014540699997435047),
                    (1.4793461562439361e-16, 0.009030539998410926, -0.012397859997813145),
                    (1.4793461562439361e-16, 0.01239785999781689, -0.009030539998407227),
                    (1.4793461562439361e-16, 0.014540699997438842, -0.004744859999163271),
                    (1.4793461562439361e-16, 0.015305999997303832, -3.6658060582704184e-16),
                    (1.4793461562439361e-16, 0.014540699997438842, 0.00474485999916258),
                    (1.4793461562439361e-16, 0.01239785999781689, 0.009030539998406457),
                    (1.4793461562439361e-16, 0.009030539998410926, 0.012397859997812476),
                    (1.4793461562439361e-16, 0.004744859999167015, 0.014540699997434445),
                    (1.4793461562439361e-16, 4.090074305739947e-15, 0.015305999997299436),
                    (1.4793461562439361e-16, -0.004744859999158833, 0.014540699997434445),
                    (1.4793461562439361e-16, -0.009030539998402757, 0.012397859997812476),
                    (1.4793461562439361e-16, -0.012397859997808734, 0.009030539998406457),
                    (1.4793461562439361e-16, -0.01454069999743066, 0.00474485999916258),
                    (1.4793461562439361e-16, -0.015305999997295709, -3.6658060582704184e-16),
                    (1.4793461562439361e-16, -0.01454069999743066, -0.004744859999163271),
                    (1.4793461562439361e-16, -0.012397859997808734, -0.009030539998407227),
                    (1.4793461562439361e-16, -0.009030539998402757, -0.012397859997813145),
                    (1.4793461562439361e-16, -0.004744859999158833, -0.014540699997435047),
                    (1.4793461562439361e-16, 4.090074305739947e-15, -0.015305999997300025),
                    (-0.004744859999162775, 4.090074305739947e-15, -0.014540699997435047),
                    (-0.009030539998406712, 4.090074305739947e-15, -0.012397859997813145),
                    (-0.012397859997812668, 4.090074305739947e-15, -0.009030539998407227),
                    (-0.014540699997434604, 4.090074305739947e-15, -0.004744859999163271),
                    (-0.015305999997299584, 4.090074305739947e-15, -3.6658060582704184e-16))
        select(cl=1)
        ctl = curve(n=name, d=1, p=pointTuple)
        ctl_shp = listRelatives(ctl, s=1)[0]
        closeCurve(ctl, ch=0, ps=0, rpo=1, bb=0.5, bki=0, p=0.1)
        if color ==1:
            ctl_shp.overrideEnabled.set(1)
            ctl_shp.overrideColor.set(9)
        return PyNode(ctl)

    def find_or_make(self, name):
            if not objExists(name):
                output_name = group(em=1, n=name)
            else: output_name = PyNode (name)
            return output_name
        
        
    def layering_CTL(self, name, head=True):
        if head==True :
            if not objExists('MainAndHeadScaleMultiplyDivide'):
                print ('there is no MainAndHeadScaleMultiplyDivide. so stopped the function')
                return
            else: main = PyNode('MainAndHeadScaleMultiplyDivide')
        else:
            if not objExists('MainScaleMultiplyDivide'):
                print ('there is no MainScaleMultiplyDivide. so stopped the function')
                return
            else: main = PyNode('MainScaleMultiplyDivide')
            
        jnt = ls(sl=1)
        output = []
        
        _all = self.find_or_make('{}_layered_GRP'.format(name))
        world_rig = self.find_or_make('world_{}_layered_GRP'.format(name))
        follow_rig = self.find_or_make('follow_{}_layered_GRP'.format(name))
        parent(world_rig, _all)
        parent(follow_rig, _all)
        
        for x in jnt:
            world_offGRP = group(em=1, n='world_'+x+'_offGRP')
            world_CTL = self.create_layered_CTL(name='world_'+x+'_CTL', color=0)
            offGRP = group(em=1, n=x+'_offGRP')
            subtractGRP = group(em=1, n=x+'_subtractGRP')
            _CTL = self.create_layered_CTL(name=x+'_CTL')
            
            _all = [world_CTL, world_offGRP, offGRP, subtractGRP, _CTL]
            
            for y in _all:
                matchTransform(y, x)
            
            parent(world_CTL, world_offGRP)
            
            parent(_CTL, subtractGRP)
            parent(subtractGRP, offGRP)
            
            main.output>>offGRP.s
            subtracter = createNode('multiplyDivide', n=x+'stubtractMultiplyer')
            _CTL.t>>subtracter.input1
            subtracter.input2.set(-1,-1,-1)
            subtracter.output>>subtractGRP.t
            
            # multiplyer = createNode('multiplyDivide', n=x+'_multiply_Main')
            # _CTL.t>>multiplyer.input1
            # main.output>>multiplyer.input2
            # multiplyer.output>>world_CTL.t
            _CTL.t>>world_CTL.t #20230111_errorFix
            _CTL.r>>world_CTL.r
            _CTL.s>>world_CTL.s
            parentConstraint(world_CTL, x, mo=0)
            scaleConstraint(world_CTL, x, mo=0)
            
            parent(world_offGRP, world_rig)
            parent(offGRP,follow_rig)
            
            output.append(offGRP)
            
        world_rig.v.set(0)
        return output

    def attacherCurve(self, name, offGRP):
        master_grp = group(em=1, name=name+'_attacherGRP')
        points = [x.t.get() for x in offGRP]
        _name = [str(x.replace('_offGRP', '')) for x in offGRP]
        select(cl=1)
        att_curve = curve(n=name+'_attacherCRV', d=1, p=points)
        
        for x in range(len(offGRP)):
            poc = createNode('pointOnCurveInfo', n=_name[x]+'_POC')
            attacher = group(em=1, n=_name[x]+'_attGRP')
            parent(attacher, master_grp)
            
            att_curve.worldSpace>>poc.inputCurve
            poc.parameter.set(x)
            poc.position>>attacher.t
            pointConstraint(attacher, offGRP[x], mo=0)

###########################################################################    
    
###############################################
# just in case #

# lock_dict_maker - just used once
    # def checkLocked_dict(sels):
    #     dict = {}
    #     attr = ['rx', 'ry', 'rz', 'sx', 'sy', 'sz']

    #     for x in sels:
    #         valueList = []
    #         for y in attr:
    #             _attr = PyNode('{}.{}'.format(x,y))
    #             if _attr.isLocked():
    #                 valueList.append(y)
    #         if valueList:
    #             dict[str(x)] = valueList
        
    #     return dict

# def user_define_attrs_reader():
        
#     a = ls(sl=1)
#     user_define_attrs_dict = {}

#     for x in a:
#         name = str(x)
#         ud_attrs = listAttr(x, ud=1)
        
#         _dict = {}
#         _listA = []
#         _listB = []
        
#         for attr in ud_attrs:
#             ud_attr = '{}.{}'.format(x,attr)
#             value = getAttr(ud_attr)
#             _listA.append(ud_attr)
#             _listB.append(ud_attr_get)
            
#         _dict['ud_attr'] = _listA
#         _dict['value'] = _listB
#         user_define_attrs_dict[name] = _dict
        
#     print (user_define_attrs_dict)
#     return user_define_attrs_dict            

###############################################