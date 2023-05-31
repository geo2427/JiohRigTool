# -*- coding: utf-8 -*-
from pymel.core import *
import imp
import maya.mel as mel

import variable as var
import ctlCommand as ctlCommand
import bsCommand as bsCommand
imp.reload(ctlCommand)
imp.reload(bsCommand)
imp.reload(var)

CTL = ctlCommand.ctlCommand()
BS = bsCommand.bsCommand()

# Main Script 0 # 
def defineVariable():
    sels = ls(sl=1)
    
    AS_MESH = sels
    AS_BS = BS.finding_AS_BS(sels)
    MOD_MESH = BS.finding_MOD_MESH()
    MOD_BS = BS.finding_MOD_BS()

    matching_DICT = BS.matching_MESH_LIST(AS_MESH, MOD_MESH)
    
    return AS_MESH, AS_BS, MOD_MESH, MOD_BS, matching_DICT

# Main Script 1 # connect to ctrlBox Controller#
def connectBStoCtl(Meshes, Ctl, tgtList):
    if objExists(Ctl):
        Ctl = PyNode(Ctl)
        ctl_dict = {}
        for tgt_alias in tgtList:
            ctl_attr = ctlCommand.floatAttr(Ctl, tgt_alias)
            ctl_dict[tgt_alias] = ctl_attr
            
            entire_userdefine_attrs = listAttr(Ctl, ud=True)
            unused_userdefine_attrs = list(set(entire_userdefine_attrs) - set(tgtList))
            
            for attr in unused_userdefine_attrs:
                attr = PyNode('{}.{}'.format(Ctl, attr))
                if not attr.isLocked():
                    attr.lock()
                    attr.setKeyable(0)
            
        for obj in Meshes:
            blendshapes = BS.findingBS(obj)
            if not blendshapes: return None
            
            for _BS in blendshapes:
                bs_aliases = BS.createAliasesDict(_BS)
                for tgt_alias, ctl_attr in ctl_dict.items():
                    if tgt_alias.lower() in bs_aliases.keys():
                        unit = createNode('unitConversion', n = '{}_{}_UNIT'.format(_BS, tgt_alias))
                        unit.conversionFactor.set(0.1)

                        BS_tgt_alias = bs_aliases[tgt_alias.lower()]['weight']

                        ctl_attr >> unit.input
                        unit.output >> BS_tgt_alias

# Main Script 2 # connect selected AS_mesh's blendshape to SDK
def connectBStoFacialCtl(AS_MESH,AS_BS,MOD_MESH,MOD_BS,matching_DICT):
    for as_mesh in AS_MESH:
        as_face_bs = AS_BS[AS_MESH.index(as_mesh)]
        face_bs = MOD_BS[MOD_MESH.index(matching_DICT[as_mesh])]

        afb_w_dict = BS.createAliasesDict(as_face_bs)
        fb_w_dict = BS.createAliasesDict(face_bs)

        for afb_key in afb_w_dict.keys():
            for fb_key in fb_w_dict.keys():
                # match_afb = afb_key
                # if match_afb.startswith('cheek_out_'):
                #     org = 'cheek_out_'
                #     new = 'cheek_'
                #     match_afb = match_afb.replace(org, new)
                
                if fb_key == afb_key:
                    animcrv = afb_w_dict[afb_key]['cns']
                    afb_w = afb_w_dict[afb_key]['weight']
                    fb_w = fb_w_dict[fb_key]['weight']
                    
                    if animcrv:
                        animcrv // afb_w
                        animcrv >> fb_w

# Main Script # 3 controller Cleaning r/s/v lock and delete Emotions and visCtrl
# 20221104 set_faceCTRL_userdefine_attr Updated
def controllerCleaning(head = True, body = True):
    if head ==True:
        CTL.Lock_lock_dict(var.lock_dict)
        CTL.deleteEmotions()
        CTL.RegionFix()
        CTL.set_faceCTRL_userdefine_attr(var.faceCTRL_userdefine_attr_dict)
        CTL.visAllLock(body=False)
    
    if body == True:
        CTL.FKHead_M_vis_setting()
        CTL.visAllLock(head=False)
        
# Main Script 4 # make MOD_MESH as a target to AS_MESH and auto set 1
def MODtoAS_autoTarget(AS_MESH,AS_BS,matching_DICT):
    for i in range(len(AS_MESH)):
        mod_mesh = matching_DICT[AS_MESH[i]]
        if mod_mesh:
            as_bs = AS_BS[i]
            select(mod_mesh)
            index = mel.eval('doBlendShapeAddSelectionAsTarget '+str(as_bs)+' 1 2 "" 0 1;')
            as_bs.w[int(index[0])].set(1)
            select(cl=1)


# Main Script 5 # faceSelection to Curve

# CTL.makeCurveFromFaceSelection_v02(mirror=1, rebuild=1)
# sels = ls(sl=1)
# CTL.switchCurve_worldCurve_v02(sels, mirror=1)


# Main Script 5 # fix EyeCTL for mirAnimator

def eyeFix(head=True, body=True):
    if head == True:
        CTL.eyeRigFix()
        #20221229 added
        setAttr("LidWireWS_scaleConstraint1.Head_MW0", 0)
        setAttr("LidWireWS_parentConstraint1.Head_MW0", 0)
    
    if body == True:    
        CTL.eyeCurveGuideSetUp()
        CTL.eyeCurveVis(var.eye_main_aim_curves, main=True)
        CTL.eyeCurveVis(var.eye_outer_aim_curves, main=False)

# Main Script 6 # ctrl_attacher 
# (select joint -> will make ctrl, and attachCurve)
# all you need to do is 
# 1. "wrap" the attachCurve for translate following,
# and 2. parentCosntraint 'follow_~GRP' for orient following
def attacher_rig(name = 'upperCheek', head=True):
    attacher_rig_name = name
    _offGRP = CTL.layering_CTL(attacher_rig_name, head)
    CTL.attacherCurve(attacher_rig_name, _offGRP)