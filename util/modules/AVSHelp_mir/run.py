import sys, imp

path = r'/home/jioh.kim/Desktop/pipe/wip/A/GSRigTool/util/modules/AVSHelp_mir/'

if not path in sys.path:
    sys.path.append(path)

import Advanced_setup
imp.reload(Advanced_setup)

Advanced_setup.TESTAdvancedSetup_win()
