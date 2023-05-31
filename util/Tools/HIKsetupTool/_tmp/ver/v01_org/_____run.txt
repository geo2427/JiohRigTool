# coding:utf-8
import sys
HIK_ToolPath='G:/Animation_Unit/_Rigging_Team/___script/T_Pose'
if not HIK_ToolPath in sys.path:
    sys.path.append(HIK_ToolPath)
import HIK_Tool
reload(HIK_Tool)

def HIK_Tool_run():
    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass
    win=HIK_Tool.winshow()
    

HIK_Tool_run()
