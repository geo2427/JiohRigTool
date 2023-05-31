#-*- coding: utf-8 -*-
import sys, imp


def skinHelpTool_Run():

    path = r'/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/util/Tools/skinHelpTool'
    if path not in sys.path:
        sys.path.append(path)

    import skinHelpTool_UI as ui
    imp.reload(ui)

    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass
    
    win = ui.SkinWindow()
    win.show()


skinHelpTool_Run()
