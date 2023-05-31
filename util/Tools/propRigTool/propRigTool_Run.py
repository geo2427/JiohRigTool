#-*- coding: utf-8 -*-
import sys, imp


def propRigTool_run():

    path = r'/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/util/Tools/propRigTool'
    if path not in sys.path:
        sys.path.append(path)

    import propRigTool_UI as ui
    imp.reload(ui)

    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass
    
    win = ui.PropUI()
    win.show()


propRigTool_run()
