# -*- coding: utf-8 -*-
from pymel.core import *

class bsCommand:
    def __init__(self):
        pass
    
    def findingBS(self, obj):
        shp = [f for f in obj.getShapes() if f.intermediateObject.get() == 0]
        if shp:
            shp = shp[0]
            inmesh_cns = [f for f in shp.inMesh.listHistory() if f.type()=='blendShape']
            return inmesh_cns

    #-- find AS's BS --#
    def finding_AS_BS(self, sels):
        AS_BS = [self.findingBS(sel)[0] for sel in sels if self.findingBS(sel)]
        return AS_BS

    #-- find modeler's Mesh --#
    def finding_MOD_MESH(self, groupName='*BS_GRP'):
        if not objExists(groupName):
            print('there is no '+groupName+' in the scene.')
            return
        else:
            GRP = PyNode(groupName)
            AD = listRelatives(GRP, ad=1, type='transform')
            
            MOD_MESH = [decendent for decendent in AD if self.findingBS(decendent)]
            return MOD_MESH

    #-- find modeler's BS --#
    def finding_MOD_BS(self, groupName='*BS_GRP'):
        if not objExists(groupName):
            print('there is no '+groupName+' in the scene.')
            return
        else:
            GRP = PyNode(groupName)
            AD = listRelatives(GRP, ad=1, type='transform')
            
            MOD_BS = [self.findingBS(decendent)[0] for decendent in AD if self.findingBS(decendent)]
            return MOD_BS

    #-- find set --#
    def matching_MESH_LIST(self, MESH_LIST_A, MESH_LIST_B):
        matching_dict = {}
        
        for numA in range(len(MESH_LIST_A)):
            for numB in range(len(MESH_LIST_B)):
                A_list = MESH_LIST_A[numA].split('_')
                B_list = MESH_LIST_B[numB].split('_')
                #20221130 list->set->list erazed
                
                A_list.remove('oneMesh')
                B_list.remove('BS')
                
                if A_list == B_list:
                    matching_dict[MESH_LIST_A[numA]] = MESH_LIST_B[numB]

        return matching_dict

    # find bsTargetName or userDefine ## nowhere used : converted with createAliasesDict ##
    # def findUserDefineAttrs(ctl, bs=False):
    #     attr_dict = {}
    #     if bs:
    #         attrs = listAttr(ctl.w, m=True)
    #     else:
    #         attrs = ctl.listAttr(ud=True)

    #     for attr in attrs:
    #         if bs: 
    #             attrname = attr.lower()
    #             attr = PyNode('{}.{}'.format(ctl, attr))
    #         else: attrname = attr.name().split('.')[-1].lower()
    #         attr_dict[attrname] = attr    
    #     return attr_dict

    # blendshape Target Dictionary converted with lower (keys)#lower_target (keys in values):# weight #cns 
    def createAliasesDict(self, blendshape):
        alias_dict = {}
        for attr in listAttr(blendshape.w, m=True):
            bs_attr = PyNode('{}.{}'.format(blendshape, attr))
            if bs_attr.connections(p=True):
                connection = bs_attr.connections(p=True)[0]
            else:
                connection = None
            
            alias_dict[attr.lower()] = {
                'weight': bs_attr,
                'cns': connection
            }
        return alias_dict
