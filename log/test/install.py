import os
import pymel.all as pm
import maya.mel as mel


def onMayaDroppedPythonFile():
    
    PATH = "/gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/"
    script_name = "GSRigTool_Run"
    file_path = os.path.join(PATH, script_name+".py")
    icon_path = os.path.join(PATH, "util/resources/GSLogo.png")

    fp = open(file_path)
    runCommand = fp.read()

    current_shelf = mel.eval("string $currentShelf=`tabLayout -query -selectTab $gShelfTopLevel`;")
    pm.setParent(current_shelf)
    pm.shelfButton(label=script_name, 
                    annotation=script_name, 
                    image1=icon_path, 
                    command=runCommand
                    )
    pm.saveShelf(pm.shelfLayout(), current_shelf)

    fp.close()

