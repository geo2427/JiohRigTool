###############################################
lock_dict = {'AimEye_L': ['sx', 'sy', 'sz'],
            'AimEye_M': ['sy', 'sz'],
            'AimEye_R': ['sx', 'sy', 'sz'],
            'SmilePull_L': ['rx', 'ry', 'rz', 'sx', 'sy', 'sz'],
            'SmilePull_R': ['rx', 'ry', 'rz', 'sx', 'sy', 'sz'],
            'lowerInnerLidOuter_L': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'lowerInnerLidOuter_R': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'lowerInnerLid_L': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'lowerInnerLid_R': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'lowerLipA_L': ['ry', 'rz', 'sx', 'sy', 'sz'],
            'lowerLipA_R': ['ry', 'rz', 'sx', 'sy', 'sz'],
            'lowerLipB_L': ['ry', 'rz', 'sx', 'sy', 'sz'],
            'lowerLipB_R': ['ry', 'rz', 'sx', 'sy', 'sz'],
            'lowerOuterLidOuter_L': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'lowerOuterLidOuter_R': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'lowerOuterLid_L': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'lowerOuterLid_R': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'upperInnerLidOuter_L': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'upperInnerLidOuter_R': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'upperInnerLid_L': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'upperInnerLid_R': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'upperLipA_L': ['ry', 'rz', 'sx', 'sy', 'sz'],
            'upperLipA_R': ['ry', 'rz', 'sx', 'sy', 'sz'],
            'upperLipB_L': ['ry', 'rz', 'sx', 'sy', 'sz'],
            'upperLipB_R': ['ry', 'rz', 'sx', 'sy', 'sz'],
            'upperOuterLidOuter_L': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'upperOuterLidOuter_R': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'upperOuterLid_L': ['rx', 'ry', 'sx', 'sy', 'sz'],
            'upperOuterLid_R': ['rx', 'ry', 'sx', 'sy', 'sz']}

faceCTRL_userdefine_attr_dict = {'Cheek_L': {'ud_attr': ['Cheek_L.followJawFollow_L'], 
                                            'value': [5.0]},
                                'EyeBrowCenter_M': {'ud_attr': ['EyeBrowCenter_M.follow'],
                                                    'value': [0.0]},
                                'FrownBulge_L': {'ud_attr': ['FrownBulge_L.followCheek_L'],
                                                'value': [0.0]},
                                'FrownBulge_R': {'ud_attr': ['FrownBulge_R.followCheek_R'],
                                                'value': [0.0]},
                                'SmileBulge_L': {'ud_attr': ['SmileBulge_L.followCheek_L'],
                                                'value': [0.0]},
                                'SmileBulge_R': {'ud_attr': ['SmileBulge_R.followCheek_R'],
                                                'value': [0.0]},
                                'ctrlBox': {'ud_attr': ['ctrlBox.limits'] ,
                                            'value': [True]},
                                'lowerLipB_L': {'ud_attr': ['lowerLipB_L.followlowerLip_M'],
                                                'value': [2.0]},
                                'lowerLipB_R': {'ud_attr': ['lowerLipB_R.followlowerLip_M'],
                                                'value': [2.0]},
                                'upperLipB_L': {'ud_attr': ['upperLipB_L.followupperLip_M'],
                                                'value': [2.0]},
                                'upperLipB_R': {'ud_attr': ['upperLipB_R.followupperLip_M'],
                                                'value': [2.0]},
                                'NoseCorner_L': {'ud_attr': ['NoseCorner_L.followLip_L'], 
                                            'value': [1.0]},# 20221221 added
                                'NoseCorner_R': {'ud_attr': ['NoseCorner_R.followLip_R'], 
                                            'value': [1.0]}# 20221221 added
                                }

eye_main_aim_curves = ['lowerLidMainCurve1_R',  'upperLidMainCurve1_R', 'lowerLidMainCurve1_L',  'upperLidMainCurve1_L']
eye_outer_aim_curves = ['upperLidOuterCurve1_R', 'lowerLidOuterCurve1_R', 'upperLidOuterCurve1_L', 'lowerLidOuterCurve1_L']

userdefine_attr_dict = {
    'ctrlPhonemes_M': ['Ah', 'Ee', 'St', 'Oh', 'Uw','L', 'BMP','FV','Th'],
    'ctrlMouth_M':  ['Angry_L', 'Angry_R', 'Roll_U', 'Roll_D', 'Cheek_L', 'Cheek_R'] 
                    #  'mouth_lower_L', 'mouth_narrow_L', 'mouth_raiser_L', 'mouth_wide_L' 
                    #  'mouth_lower_R', 'mouth_narrow_R', 'mouth_raiser_R', 'mouth_wide_R'
}
