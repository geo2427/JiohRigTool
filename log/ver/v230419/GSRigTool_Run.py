# coding:utf-8
import sys, imp
import maya.mel as mel


def GSRigTool_Run():

    path = r'/home/jioh.kim/Desktop/pipe/wip/A/GSRigTool/'
    if path in sys.path:
        pass
    else:
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
    win.show()


GSRigTool_Run()
