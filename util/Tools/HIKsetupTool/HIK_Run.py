# coding:utf-8
import sys, imp


def HIK_Tool_run():
    Path = r'/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/util/Tools/HIKsetupTool'
    if Path not in sys.path:
        sys.path.append(Path)

    import HIK_UI as ui
    imp.reload(ui)

    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass
    win = ui.winshow()
    

HIK_Tool_run()
