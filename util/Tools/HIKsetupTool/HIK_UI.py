# coding:utf-8
import imp
import pymel.all as pm
from functools import partial
import HIK_Tool as core
imp.reload(core)


def winshow():
    winName = 'HIKSetup'
    if pm.window(winName, exists=1):
        pm.deleteUI(winName)
    
    with pm.window(winName, title='HIKsetupTool', wh=(230, 500) , s=1) as win:
        with pm.rowColumnLayout(nc=1, columnWidth=[(1, 230)], rowSpacing=(1, 5)) as layTypes:
            with pm.frameLayout('Edit_v230127', bgc=[.3, .3, .3]):

                with pm.frameLayout('Maya Setup', cll=1, cl=0, bgc=[.4, .4, .5]):
                    pm.text('1. Pre')
                    btnCreateSet = pm.button('(option) create AVS Set', c=partial(core.CreateADVSet))
                    btnCreateHIK = pm.button('create HIK', h=30, bgc=[.5, .6, .7], c=partial(core.CreateHIK, core.CHNameField))
                    
                    pm.separator()
                    pm.text('2. Pose')
                    btnSaveBPose = pm.button('Save  B', c=partial(core.savePose, 'Bpose'))
                    btnSetTpose = pm.button('Set T pose', c=partial(core.SetTposeFK))
                    btnSaveTPose = pm.button('Save  T', c=partial(core.savePose, 'Tpose'))
                    
                    pm.separator()
                    pm.text('3. HIK')
                    btnLoadCustomHIK = pm.button('Load Skeleton Definition', h=30, bgc=[.5, .6, .7], c=partial(core.LoadCostomHIK))
                    btnLoadBPose = pm.button('Load  B', c=partial(core.loadPose, 'Bpose'))
                
                with pm.frameLayout('Mobu Setup', cll=1, cl=1, bgc=[.4, .4, .5]):
                    btnLoadTPose = pm.button('Load  T', c=partial(core.loadPose, 'Tpose'))
                    btnMobuSet = pm.button('Set for Mobu', h=30, bgc=[.5, .6, .7], c=partial(core.MobuSetGrp, core.CHNameField))
                    btnSendMobu = pm.button('send to MotionBuilder', c=partial(core.SendToMobu))

                with pm.frameLayout('Load Pose', cll=1, cl=1, bgc=[.4, .4, .5]):
                    with pm.rowColumnLayout(nc=2, rowSpacing=(1, 5), columnSpacing=(2,10)) as layTypes:
                        btnLoadBPose = pm.button('Load  B', w=110, h=30, c=partial(core.loadPose, 'Bpose'))
                        btnLoadTPose = pm.button('Load  T', w=110, h=30, c=partial(core.loadPose, 'Tpose'))
