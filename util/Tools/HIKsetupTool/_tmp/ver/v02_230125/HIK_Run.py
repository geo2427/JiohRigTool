# coding:utf-8

def HIK_Tool_run():
    import sys
    Path = r'/home/jioh.kim/maya/scripts/HIKsetupTool/'
    if Path not in sys.path:
        sys.path.append(Path)

    import HIK_UI as ui
    import imp
    imp.reload(ui)

    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass
    win = ui.winshow()
    

HIK_Tool_run()
