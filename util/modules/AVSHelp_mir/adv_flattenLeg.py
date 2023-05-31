# -*- coding: utf-8 -*-
from pymel.core import *
import re

def addNotes(node = None, default_text = "Input note here"):
    if not node:
        sel = ls(sl=1)
        if sel:
            node = sel[0]
        else:
            warning("Please select a node to apply the notes field too")

    if not attributeQuery("notes", n = node, ex = True):
        addAttr(node, ln = "notes", sn="nts", dt="string")
        setAttr("%s.notes"%node, default_text, type="string")
    else:
        setAttr("%s.notes"%node, default_text, type="string")

def legPoleMatching(side="L"):
    Pole = PyNode("PoleLeg_{}".format(side))
    IKLeg = PyNode("IKLeg_{}".format(side))

    Pole.follow.set(10)
    Pole.t.set(0,0,0)

    point1 = Pole.getTranslation(space="world")
    x1, y1, z1 = point1
    Pole.tx.set(1)
    point2 = Pole.getTranslation(space="world")
    x2, y2, z2 = point2
    Pole.tx.set(0)

    x0, y0, z0 = IKLeg.getTranslation(space="world")

    k = (x0-x1)/(x2-x1)
    x = x0
    y = k*(y2-y1)+y1
    z = k*(z2-z1)+z1

    offset = group(em=1, n=Pole+"_mod_offGRP")
    offset.t.set(x,y,z)
    parent(offset, "leg_org_space_GRP")
    return offset

def duplicateAndNoteLocalRot(transform_node, rot=True):
    dup = duplicate(transform_node, po=1, n=transform_node+"_duplicate_org")[0]
    if rot == True:
        addNotes(dup, str(getAttr(transform_node+'.r')))
    else:
        addNotes(dup, str(getAttr(transform_node+'.t')))
    return dup

def readNoteValues(node):
    vx, vy, vz = re.findall(r"[-+]?(?:\d*\.*\d+)", getAttr("{}.notes".format(node)))
    x,y,z = float(vx), float(vy), float(vz)
    return x,y,z

################################################################
def legFlatten():
    hip_r_offset = PyNode("FKOffsetHip_R")
    hip_l_offset = PyNode("FKOffsetHip_L")
    hip_r = PyNode("FKHip_R")
    hip_l = PyNode("FKHip_L")

    ankle_r_offset = PyNode("FKOffsetAnkle_R")
    ankle_l_offset = PyNode("FKOffsetAnkle_L")
    ankle_r = PyNode("FKAnkle_R")
    ankle_l = PyNode("FKAnkle_L")

    ik_leg_r_offset = PyNode("IKOffsetLeg_R")
    ik_leg_l_offset = PyNode("IKOffsetLeg_L")
    ik_leg_r = PyNode("IKLeg_R")
    ik_leg_l = PyNode("IKLeg_L")
    
    pole_leg_l_offset = PyNode("PoleOffsetLeg_L")
    pole_leg_r_offset = PyNode("PoleOffsetLeg_R")
    pole_leg_l = PyNode("PoleLeg_L")
    pole_leg_r = PyNode("PoleLeg_R")
    ######################################

    dup_hip_r_offset = duplicateAndNoteLocalRot(hip_r_offset)
    dup_hip_l_offset = duplicateAndNoteLocalRot(hip_l_offset)

    dup_ankle_r_offset = duplicateAndNoteLocalRot(ankle_r_offset)
    dup_ankle_l_offset = duplicateAndNoteLocalRot(ankle_l_offset)
    
    dup_pole_leg_r_offset = duplicateAndNoteLocalRot(pole_leg_r_offset, rot=False)
    dup_pole_leg_l_offset = duplicateAndNoteLocalRot(pole_leg_l_offset, rot=False)
    
    dup = [dup_ankle_l_offset, dup_ankle_r_offset, dup_hip_l_offset, dup_hip_r_offset, dup_pole_leg_r_offset, dup_pole_leg_l_offset]

    GRP = group(em=1, n="leg_org_space_GRP")
    parent(dup, GRP)

    #ankleSet
    hip_l_offset.r.set(180,0,hip_l_offset.rz.get())
    hip_r_offset.r.set(0,180,hip_r_offset.rz.get())

    matchTransform(ankle_l_offset, dup_ankle_l_offset, rot=1, pos=0)
    matchTransform(ankle_r_offset, dup_ankle_r_offset, rot=1, pos=0)

    matchTransform(ik_leg_l_offset, ankle_l_offset, pos=1, rot=0)
    matchTransform(ik_leg_r_offset, ankle_r_offset, pos=1, rot=0)
    
    mod_pole_leg_l_offset = legPoleMatching(side="L")
    mod_pole_leg_r_offset = legPoleMatching(side="R")
    
    matchTransform(pole_leg_l_offset, mod_pole_leg_l_offset)
    matchTransform(pole_leg_r_offset, mod_pole_leg_r_offset)
    
    parentConstraint("PoleOffsetLeg_RStatic", "PoleOffsetLeg_RFollow", "PoleOffsetLeg_R_parentConstraint1", e=1, mo=1)
    parentConstraint("PoleOffsetLeg_LStatic", "PoleOffsetLeg_LFollow", "PoleOffsetLeg_L_parentConstraint1", e=1, mo=1)

    matchTransform(hip_l, dup_hip_l_offset, rot=1, pos=0)
    matchTransform(hip_r, dup_hip_r_offset, rot=1, pos=0)
    matchTransform(ankle_l, dup_ankle_l_offset, rot=1, pos=0)
    matchTransform(ankle_r, dup_ankle_r_offset, rot=1, pos=0)
    matchTransform(ik_leg_l, dup_ankle_l_offset, rot=0, pos=1)
    matchTransform(ik_leg_r, dup_ankle_r_offset, rot=0, pos=1)
    matchTransform(pole_leg_l, dup_pole_leg_l_offset, rot=0, pos=1)
    matchTransform(pole_leg_r, dup_pole_leg_r_offset, rot=0, pos=1)
    
    addNotes(ik_leg_l, str(ik_leg_l.t.get())) #t
    addNotes(ik_leg_r, str(ik_leg_r.t.get()))#t
    addNotes(hip_l, str(hip_l.r.get()))#r
    addNotes(hip_r, str(hip_r.r.get()))#r
    addNotes(ankle_l, str(ankle_l.r.get()))#r
    addNotes(ankle_r, str(ankle_r.r.get()))#r
    addNotes(pole_leg_l, str(pole_leg_l.t.get()))#t
    addNotes(pole_leg_r, str(pole_leg_r.t.get()))#t
    
    root_ty = ik_leg_l.ty.get()
    setAttr("RootOffsetX_M.ty", root_ty)
    setAttr("RootX_M.ty", -1*root_ty)
    
def legFlattenRollback():
    setAttr("RootOffsetX_M.ty", 0)
    setAttr("RootX_M.ty", 0)

    hip_r_offset = PyNode("FKOffsetHip_R")
    hip_l_offset = PyNode("FKOffsetHip_L")
    hip_r = PyNode("FKHip_R")
    hip_l = PyNode("FKHip_L")

    ankle_r_offset = PyNode("FKOffsetAnkle_R")
    ankle_l_offset = PyNode("FKOffsetAnkle_L")
    ankle_r = PyNode("FKAnkle_R")
    ankle_l = PyNode("FKAnkle_L")

    ik_leg_r_offset = PyNode("IKOffsetLeg_R")
    ik_leg_l_offset = PyNode("IKOffsetLeg_L")
    ik_leg_r = PyNode("IKLeg_R")
    ik_leg_l = PyNode("IKLeg_L")

    pole_leg_l_offset = PyNode("PoleOffsetLeg_L")
    pole_leg_r_offset = PyNode("PoleOffsetLeg_R")
    pole_leg_l = PyNode("PoleLeg_L")
    pole_leg_r = PyNode("PoleLeg_R")

    dup_hip_r_offset = PyNode(hip_r_offset+"_duplicate_org")
    dup_hip_l_offset = PyNode(hip_l_offset+"_duplicate_org")

    dup_ankle_r_offset = PyNode(ankle_r_offset+"_duplicate_org")
    dup_ankle_l_offset = PyNode(ankle_l_offset+"_duplicate_org")

    dup_pole_leg_r_offset = PyNode(pole_leg_r_offset+"_duplicate_org")
    dup_pole_leg_l_offset = PyNode(pole_leg_l_offset+"_duplicate_org")

    hip_l_offset.r.set(readNoteValues(dup_hip_l_offset))
    hip_r_offset.r.set(readNoteValues(dup_hip_r_offset))
    hip_l.r.set(0,0,0)
    hip_r.r.set(0,0,0)
    ankle_l_offset.r.set(readNoteValues(dup_ankle_l_offset))
    ankle_r_offset.r.set(readNoteValues(dup_ankle_r_offset))
    ankle_l.r.set(0,0,0)
    ankle_r.r.set(0,0,0)

    matchTransform(ik_leg_l_offset, dup_ankle_l_offset, rot=0, pos=1)
    matchTransform(ik_leg_r_offset, dup_ankle_r_offset, rot=0, pos=1)
    ik_leg_l.t.set(0,0,0)
    ik_leg_r.t.set(0,0,0)
    pole_leg_l.t.set(0,0,0)
    pole_leg_r.t.set(0,0,0)

    setAttr('PoleLeg_R.follow', 10)
    setAttr('PoleLeg_L.follow', 10)
    matchTransform(pole_leg_l_offset, dup_pole_leg_l_offset)
    matchTransform(pole_leg_r_offset, dup_pole_leg_r_offset)
    parentConstraint("PoleOffsetLeg_RStatic", "PoleOffsetLeg_RFollow", "PoleOffsetLeg_R_parentConstraint1", e=1, mo=1)
    parentConstraint("PoleOffsetLeg_LStatic", "PoleOffsetLeg_LFollow", "PoleOffsetLeg_L_parentConstraint1", e=1, mo=1)
    delete("leg_org_space_GRP")

def legGoToBuildPose():
    hip_r = PyNode("FKHip_R")
    hip_l = PyNode("FKHip_L")
    hip_l_rx, hip_l_ry, hip_l_rz = re.findall(r"[-+]?(?:\d*\.*\d+)", str(hip_l.notes.get()))
    hip_r_rx, hip_r_ry, hip_r_rz = re.findall(r"[-+]?(?:\d*\.*\d+)", str(hip_r.notes.get()))
    hip_l.r.set(float(hip_l_rx), float(hip_l_ry), float(hip_l_rz))
    hip_r.r.set(float(hip_r_rx), float(hip_r_ry), float(hip_r_rz))
    
    ankle_r = PyNode("FKAnkle_R")
    ankle_l = PyNode("FKAnkle_L")
    ankle_l_rx, ankle_l_ry, ankle_l_rz = re.findall(r"[-+]?(?:\d*\.*\d+)", str(ankle_l.notes.get()))
    ankle_r_rx, ankle_r_ry, ankle_r_rz = re.findall(r"[-+]?(?:\d*\.*\d+)", str(ankle_r.notes.get()))
    ankle_l.r.set(float(ankle_l_rx), float(ankle_l_ry), float(ankle_l_rz))
    ankle_r.r.set(float(ankle_r_rx), float(ankle_r_ry), float(ankle_r_rz))
    
    ik_leg_r = PyNode("IKLeg_R")
    ik_leg_l = PyNode("IKLeg_L")
    ik_leg_l_tx, ik_leg_l_ty, ik_leg_l_tz = re.findall(r"[-+]?(?:\d*\.*\d+)", str(ik_leg_l.notes.get()))
    ik_leg_r_tx, ik_leg_r_ty, ik_leg_r_tz = re.findall(r"[-+]?(?:\d*\.*\d+)", str(ik_leg_r.notes.get()))
    ik_leg_l.t.set(float(ik_leg_l_tx), float(ik_leg_l_ty), float(ik_leg_l_tz))
    ik_leg_r.t.set(float(ik_leg_r_tx), float(ik_leg_r_ty), float(ik_leg_r_tz))
            
    pole_leg_l = PyNode("PoleLeg_L")
    pole_leg_r = PyNode("PoleLeg_R")
    pole_leg_l_tx, pole_leg_l_ty, pole_leg_l_tz = re.findall(r"[-+]?(?:\d*\.*\d+)", str(pole_leg_l.notes.get()))
    pole_leg_r_tx, pole_leg_r_ty, pole_leg_r_tz = re.findall(r"[-+]?(?:\d*\.*\d+)", str(pole_leg_r.notes.get()))
    pole_leg_l.t.set(float(pole_leg_l_tx), float(pole_leg_l_ty), float(pole_leg_l_tz))
    pole_leg_r.t.set(float(pole_leg_r_tx), float(pole_leg_r_ty), float(pole_leg_r_tz))
    
    setAttr("FKKnee_L.t", 0,0,0)
    setAttr("FKKnee_L.r", 0,0,0)
    setAttr("FKKnee_R.t", 0,0,0)
    setAttr("FKKnee_R.r", 0,0,0)
    
    root_ty = getAttr("RootOffsetX_M.ty")
    setAttr("RootX_M.t", 0, -1*root_ty, 0)
    setAttr("RootX_M.r", 0, 0, 0)
    