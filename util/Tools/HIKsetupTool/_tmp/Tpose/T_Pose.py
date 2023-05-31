import maya.cmds as cmds

FKIKCon_List = ['FKIKArm_L', 'FKIKArm_R', 'FKIKLeg_L', 'FKIKLeg_R']

leg_getAttrList = {'Hip_L' : ['FKHip_L', 'FKKnee_L', 'FKAnkle_L'],
                   'Hip_R' : ['FKHip_R', 'FKKnee_R', 'FKAnkle_R']}
                   
arm_getAttrList = {'Scapula_L' : ['FKScapula_L', 'FKShoulder_L', 'FKElbow_L','FKWrist_L'],
                   'Scapula_R' : ['FKScapula_R', 'FKShoulder_R', 'FKElbow_R','FKWrist_R']}

finger_getAttrList = {'IndexFinger1_L' : ['FKIndexFinger1_L', 'FKIndexFinger2_L', 'FKIndexFinger3_L'],
                      'MiddleFinger1_L' : ['FKMiddleFinger1_L', 'FKMiddleFinger2_L', 'FKMiddleFinger3_L'],
                      'RingFinger1_L' :['FKRingFinger1_L', 'FKRingFinger2_L', 'FKRingFinger3_L'],
                      'PinkyFinger1_L' : ['FKPinkyFinger1_L', 'FKPinkyFinger2_L', 'FKPinkyFinger3_L'],
                      'IndexFinger1_R' : ['FKIndexFinger1_R', 'FKIndexFinger2_R', 'FKIndexFinger3_R'],
                      'MiddleFinger1_R' : ['FKMiddleFinger1_R', 'FKMiddleFinger2_R', 'FKMiddleFinger3_R'],
                      'RingFinger1_R' :['FKRingFinger1_R', 'FKRingFinger2_R', 'FKRingFinger3_R'],
                      'PinkyFinger1_R' : ['FKPinkyFinger1_R', 'FKPinkyFinger2_R', 'FKPinkyFinger3_R']}

leg_getAttrDict = {'Hip_L' : {'FKHip_L':[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0,-1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                              'FKKnee_L':[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0,-1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                              'FKAnkle_L':[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0,-1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0]}, 
                   'Hip_R' : {'FKHip_R':[0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                              'FKKnee_R':[0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0,-1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                              'FKAnkle_R':[0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0,-1.0, 0.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0]}, 
                   }
                            
                
arm_getAttrDict = {'Scapula_L' : {'FKScapula_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                       'FKShoulder_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                       'FKElbow_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                       'FKWrist_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    }, 
                                    
                   'Scapula_R' : {'FKScapula_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                       'FKShoulder_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                       'FKElbow_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                       'FKWrist_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0]},
                   }

finger_getAttrDict = {'IndexFinger1_L' : {'FKIndexFinger1_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                          'FKIndexFinger2_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                          'FKIndexFinger3_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    }, 
                      'MiddleFinger1_L' : {'FKMiddleFinger1_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKMiddleFinger2_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKMiddleFinger3_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    }, 
                      'RingFinger1_L' : {'FKRingFinger1_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                         'FKRingFinger2_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                         'FKRingFinger3_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    }, 
                      'PinkyFinger1_L' : {'FKPinkyFinger1_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                          'FKPinkyFinger2_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                          'FKPinkyFinger3_L':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,-1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    }, 

                      'IndexFinger1_R' : {'FKIndexFinger1_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                          'FKIndexFinger2_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                          'FKIndexFinger3_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    }, 
                      'MiddleFinger1_R' : {'FKMiddleFinger1_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKMiddleFinger2_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                           'FKMiddleFinger3_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    }, 
                      'RingFinger1_R' : {'FKRingFinger1_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                         'FKRingFinger2_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                         'FKRingFinger3_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    }, 
                      'PinkyFinger1_R' : {'FKPinkyFinger1_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                          'FKPinkyFinger2_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                          'FKPinkyFinger3_R':[-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 5.0 , 5.0, 1.0],
                                    }, 
                     }

thumb_getAttrDict = {'FKThumbFinger2_L' : 'FKThumbFinger3_L',
                     'FKThumbFinger2_R' : 'FKThumbFinger3_R'}


for i in FKIKCon_List:
    cmds.setAttr('%s.FKIKBlend'%i, 0)

for i in leg_getAttrDict.items():
    j_getMat = cmds.xform(i[0], q=True ,m=True , ws=True)
    for x in leg_getAttrList[i[0]]:
        ctr_getMat = cmds.xform(x, q=True ,m=True , ws=True)
        i[1][x][12] = j_getMat[12]
        i[1][x][13] = ctr_getMat[13]
        i[1][x][14] = ctr_getMat[14]
        cmds.xform(x, m=i[1][x] , ws=True)
        
for i in arm_getAttrDict.items():
    j_getMat = cmds.xform(i[0], q=True ,m=True , ws=True)
    for x in arm_getAttrList[i[0]]:
        ctr_getMat = cmds.xform(x, q=True ,m=True , ws=True)
        i[1][x][12] = ctr_getMat[12]
        i[1][x][13] = ctr_getMat[13]
        i[1][x][14] = ctr_getMat[14]
        cmds.xform(x, m=i[1][x] , ws=True)

for i in finger_getAttrDict.items():
    j_getMat = cmds.xform(i[0], q=True ,m=True , ws=True)
    for x in finger_getAttrList[i[0]]:
        ctr_getMat = cmds.xform(x, q=True ,m=True , ws=True)
        i[1][x][12] = ctr_getMat[12]
        i[1][x][13] = ctr_getMat[13]
        i[1][x][14] = ctr_getMat[14]
        cmds.xform(x, m=i[1][x] , ws=True)

for i in thumb_getAttrDict.items():
    j_getMat = cmds.xform(i[0], q=True ,m=True , ws=True)
    ctr_getMat = cmds.xform(i[1], q=True ,m=True , ws=True)
    cmds.xform(i[1], m=[j_getMat[0], j_getMat[1], j_getMat[2], ctr_getMat[3], j_getMat[4], j_getMat[5], j_getMat[6], ctr_getMat[7], j_getMat[8], j_getMat[9], j_getMat[10], ctr_getMat[11], ctr_getMat[12], ctr_getMat[13], ctr_getMat[14], ctr_getMat[15]] , ws=True)