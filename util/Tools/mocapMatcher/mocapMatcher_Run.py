#-*- coding: utf-8 -*-

def MocapMatcher_Run():
    
    import sys, imp
    path = r'/gstepasset/WorkLibrary/1.Animation_team/Script/TeamScript/module/mocapMatcher/'
    if path not in sys.path:
        sys.path.append(path)
        
    import mocapMatcher_Core as ui
    imp.reload(ui)

    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass

    win = ui.MainUI()
    


