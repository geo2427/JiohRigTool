# coding:utf-8
import pymel.all as pm
from functools import partial

import JHCore as core
import imp
imp.reload(core)


def winshow():
    winName = 'windowName'
    if pm.window(winName, exists=1):
        pm.deleteUI(winName)

    with pm.window(winName, title='JHTool', rtf=1) as win:
        with pm.tabLayout('tab'):
            with pm.rowColumnLayout('RigTab'):
                pm.frameLayout(l='Edit_v220705', bgc=(0.3, 0.3, 0.3))


                # Constraint #
                with pm.columnLayout('constraintGrp'):
                    pm.frameLayout(label='Constraint', bgc=(0.4, 0.4, 0.5))

                    pm.checkBox('MaintainOffset')
                    pm.rowColumnLayout(nc=4, cw=[(1, 80), (2, 80), (3, 80), (4, 80)],
                                       co=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2), (4, 'both', 2)])
                    constraintType = ['parent', 'point', 'orient', 'scale']
                    for consType in constraintType:
                        pm.button(l=consType.title())
                        pm.popupMenu(button=1)
                        userSelType = ['Constraint', 'OneToAll', 'Each', 'AllToAll']
                        for userType in userSelType:
                            pm.menuItem(userType, c=partial(core.constraint, userType, consType))


                # Shape #
                pm.separator(h=10, vis=0)
                with pm.rowColumnLayout('ShapeGrp'):
                    pm.frameLayout(label='Shape', bgc=(0.4, 0.4, 0.5))

                    with pm.rowLayout(nc=3):
                        
                        with pm.rowColumnLayout(nc=1, ro=(2, 'both', 5)):
                            pm.text('[ dirven ]')
                            tslLtOld = pm.textScrollList(ams=1, w=100)
                            with pm.rowColumnLayout(nc=2, co=(1, 'right', 4)):
                                btnLtAdd = pm.button(l='Add', w=70)
                                pm.popupMenu(mm=1, b=1, p=btnLtAdd)
                                pm.menuItem('Replace', rp='NW', c=partial(core.ReplaceTsl, tslLtOld))
                                pm.menuItem('Add', rp='NE', c=partial(core.addToTsl, tslLtOld))
                                # pm.menuItem('Sort', rp='S')

                                btnLtRemove = pm.button(l='Remove', w=70)
                                pm.popupMenu(mm=1, b=1, p=btnLtRemove)
                                pm.menuItem('All', rp='NW', c=partial(core.RemoveAllTsl, tslLtOld))
                                pm.menuItem('Sel', rp='NE', c=partial(core.RemoveSelTsl, tslLtOld))

                        pm.text(' << ')

                        with pm.rowColumnLayout(nc=1, ro=(2, 'both', 5)):
                            pm.text('[ driver ]')
                            tslRtNew = pm.textScrollList(ams=1, w=100)
                            with pm.rowColumnLayout(nc=2, co=(1, 'right', 4)):
                                btnRtAdd = pm.button(l='Add', w=70)
                                pm.popupMenu(mm=1, b=1, p=btnRtAdd)
                                pm.menuItem('Replace', rp='NW', c=partial(core.ReplaceTsl, tslRtNew))
                                pm.menuItem('Add', rp='NE', c=partial(core.addToTsl, tslRtNew))
                                # pm.menuItem('Sort', rp='S')

                                btnRtRemove = pm.button(l='Remove', w=70)
                                pm.popupMenu(mm=1, b=1, p=btnRtRemove)
                                pm.menuItem('All', rp='NW', c=partial(core.RemoveAllTsl, tslRtNew))
                                pm.menuItem('Sel', rp='NE', c=partial(core.RemoveSelTsl, tslRtNew))

                    with pm.rowColumnLayout(nc=5, cw=[(1, 64), (2, 64), (3, 66), (4, 64), (5, 64)], co=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2), (4, 'both', 2), (5, 'both', 2)]):
                        
                        btnCtrlShape = pm.button(l='CtrlShape', w=60, c=partial(core.CtrlShapeChage, (tslLtOld, tslRtNew)))

                        btnMesh = pm.button(l='Mesh')
                        pm.popupMenu(mm=1, b=1, p=btnMesh)
                        pm.menuItem('OneToAll', rp='NW', c=partial(core.MeshChangeOnToAllConnec, (tslLtOld, tslRtNew)))
                        pm.menuItem('OneToOne', rp='NE', c=partial(core.MeshChangeOneToOneConnect, (tslLtOld, tslRtNew)))
                        pm.menuItem('DisOneToAll', rp='SW', c=partial(core.MeshChangeOnToAllDisConnec, (tslLtOld, tslRtNew)))
                        pm.menuItem('DisOneToOne', rp='SE', c=partial(core.MeshChangeOneToOneDisConnec, (tslLtOld, tslRtNew)))

                        btnCopySkin = pm.button(l='CopySkin')
                        pm.popupMenu(mm=1, b=1, p=btnCopySkin)
                        pm.menuItem('OneToAll', rp='NW', c=partial(core.CopySkinOneToAll, (tslLtOld, tslRtNew)))
                        pm.menuItem('OneToOne', rp='NE', c=partial(core.CopySkinOneToOne, (tslLtOld, tslRtNew)))
                        pm.menuItem('MoveSkin', rp='SW', c=partial(core.MoveSkin, (tslLtOld, tslRtNew)))
                        pm.menuItem('CleanUpSkin', rp='SE', c=partial(core.CleanUpSkin, (tslLtOld, tslRtNew)))

                        btnSets = pm.button(l='Sets')

                        btnGroup = pm.button(l='Group', w=60, c=core.MakeGroup)


                # Lock And Hide #
                pm.separator(h=10, vis=0)
                pm.frameLayout(label='Lock & Hide', bgc=(0.4, 0.4, 0.5), w=320)
                with pm.rowColumnLayout(nc=4, co=[(1, 'both', 2), [2, 'both', 2], [3, 'both', 2], [4, 'both', 2]], ro=[(1, 'both', 2), [2, 'both', 2], [3, 'both', 2], [4, 'both', 2]], cw=[(1, 80), (2, 80), (3, 80), (4, 80)]):

                    btnUnLock = pm.button('UnLock')
                    pm.popupMenu(markingMenu=1, b=1, p=btnUnLock)
                    pm.menuItem('All', rp='NW', c=partial(core.UnLockHideAll, 'lock'))
                    pm.menuItem('Check', rp='NE', c=core.UnLockCheck)

                    btnUnHide = pm.button('UnHide')
                    pm.popupMenu(markingMenu=1, b=1, p=btnUnHide)
                    pm.menuItem('All', rp='NW', c=partial(core.UnLockHideAll, 'hide'))
                    pm.menuItem('Check', rp='NE', c=core.UnHideCheck)

                    btnCheck = pm.button('Check', w=60, c=core.CheckLockHide)

                    btnMove = pm.button('Move')
                    pm.popupMenu(markingMenu=1, b=1, p=btnMove)
                    pm.menuItem('Trs', rp='NW', c=partial(core.Move, 'Trs'))
                    pm.menuItem('Rot', rp='NE', c=partial(core.Move, 'Rot'))
                    pm.menuItem('TrsRot', rp='S', c=partial(core.Move, 'TrsRot'))

                    btnCheckALL = pm.button(l='checkAll', w=60, c=partial(core.CheckBoxEdit, True))

                    btnCheckClr = pm.button(l='clearAll', w=60, c=partial(core.CheckBoxEdit, False))

                    btnConnect = pm.button('connect')
                    pm.popupMenu(markingMenu=1, b=1, p=btnConnect)
                    pm.menuItem('OneToAll', rp='NW', c=partial(core.ConnecOneToAll, (tslLtOld, tslRtNew), True))
                    pm.menuItem('OneToOne', rp='NE', c=partial(core.ConnecOneToOne, (tslLtOld, tslRtNew), True))

                    btnDisConnect = pm.button('disconnect')
                    pm.popupMenu(markingMenu=1, b=1, p=btnDisConnect)
                    pm.menuItem('OneToAll', rp='NW', c=partial(core.ConnecOneToAll, (tslLtOld, tslRtNew), False))
                    pm.menuItem('OneToOne', rp='NE', c=partial(core.ConnecOneToOne, (tslLtOld, tslRtNew), False))

                with pm.rowColumnLayout(nc=4, cal=[1, 'left'], cs=[1, 10]):
                    pm.text('Trans: ')
                    pm.checkBox('tx')
                    pm.checkBox('ty')
                    pm.checkBox('tz')
                    pm.text('Rotate: ')
                    pm.checkBox('rx')
                    pm.checkBox('ry')
                    pm.checkBox('rz')
                    pm.text('Scale: ')
                    pm.checkBox('sx')
                    pm.checkBox('sy')
                    pm.checkBox('sz')
                    pm.text('Vis: ')
                    pm.checkBox('v')


                # Color #
                pm.separator(h=15, vis=1)
                with pm.rowColumnLayout(nc=2, cs=(1, 15)):
                    pm.text(l='Set Color : ')
                    
                    with pm.rowColumnLayout(nc=11):
                        for i in range(1, 32):
                            r, g, b = pm.colorIndex(i, q=1)
                            pm.canvas(rgbValue=(r, g, b), w=20, h=20, pc=partial(core.SetColor, i))
                pm.separator(h=15, vis=0)
