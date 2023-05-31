# coding:utf-8
import pymel.all as pm
from functools import partial
import HIK_Tool as core
import imp
imp.reload(core)


def winshow():
    winName = 'HIKSetup'
    if pm.window(winName, exists=1):
        pm.deleteUI(winName)
    
    with pm.window(winName, title='HIKsetupTool', widthHeight=(230, 800) , sizeable=1) as win:
        with pm.rowColumnLayout(nc=1, columnWidth=[(1, 230)], rowSpacing=(1, 5)) as layTypes:
            with pm.frameLayout('Edit_v230125', bgc=[.3, .3, .3]):

                with pm.frameLayout('Setting', cll=1, cl=0, bgc=[.4, .4, .5]):
                    pm.text('1. Pre')
                    btnCreateSet = pm.button('(option) create AVS Set', w=230, c=partial(core.CreateADVSet))
                    btnCreateHIK = pm.button('create HIK', w=230,  bgc=[.5, .6, .7], c=partial(core.CreateHIK, core.CHNameField))
                    
                    pm.separator()
                    pm.text('2. Pose')
                    btnSaveBPose = pm.button('Save  B', w=110, c=partial(core.savePose, 'Bpose'))
                    btnSetTpose = pm.button('Set T pose', w=230, c=partial(core.SetTposeFK))
                    btnSaveTPose = pm.button('Save  T', w=110, c=partial(core.savePose, 'Tpose'))
                    
                    pm.separator()
                    pm.text('3. HIK')
                    btnLoadCustomHIK = pm.button('Load Skeleton Definition', w=230, bgc=[.5, .6, .7], c=partial(core.LoadCostomHIK))
                    
                    pm.separator()
                    pm.text('4. Check Primary Axis')
                    with pm.rowLayout(nc=4, cat=[(1, 'left', 15), (3, 'right', 10), (4, 'right', 10)]):
                        checkArmX = pm.checkBox('x')
                        checkArmY = pm.checkBox('y', v=1)
                        checkArmZ = pm.checkBox('z')
                        btnArmEditRotLimit = pm.button('Set ForeArm', w=100, c=partial(core.RotLimitSetting, 'ForeArm'))

                    with pm.rowLayout(nc=4, cat=[(1, 'left', 15), (3, 'right', 10), (4, 'right', 10)]):
                        checkLegX = pm.checkBox('x')
                        checkLegY = pm.checkBox('y', v=1)
                        checkLegZ = pm.checkBox('z')
                        btnLegEditRotLimit = pm.button('Set Leg', w=100, c=partial(core.RotLimitSetting, 'Leg'))

                pm.text('')
                with pm.frameLayout('Load Pose', cll=1, cl=0, bgc=[.4, .4, .5]):
                    with pm.rowColumnLayout(nc=2, rowSpacing=(1, 5), columnSpacing=(2,10)) as layTypes:
                        btnLoadBPose = pm.button('Load  B', w=110, h=30, c=partial(core.loadPose, 'Bpose'))
                        btnLoadTPose = pm.button('Load  T', w=110, h=30, c=partial(core.loadPose, 'Tpose'))
