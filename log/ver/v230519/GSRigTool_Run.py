#-*- coding: utf-8 -*-
import sys, imp
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI as OM


def mayaMainWindow():
    win_ptr = OM.MQtUtil.mainWindow()
    return wrapInstance(int(win_ptr), QtWidgets.QMainWindow)


def GSRigTool_Run():

    path = r'/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/'
    if path not in sys.path:
        sys.path.append(path)
        
    import GSRigTool_UI as ui
    imp.reload(ui)

    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass

    win = ui.GSRigUI()
    win.show(dockable=True) # , floating=False, area="left"
    win.raise_()
    

GSRigTool_Run()

