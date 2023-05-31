# coding:utf-8
import sys, imp

def JH_edit_run():
    
    Path = r'/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/util/_ref/JHTool'
    if Path not in sys.path:
        sys.path.append(Path)

    import JHUI as ui
    imp.reload(ui)

    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass
    win = ui.winshow()


JH_edit_run()
