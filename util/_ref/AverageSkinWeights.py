''' 
Average Skin Weights v.1.0 by vjurat.
Tested on version Maya 2018.
That script allows making hard surface objects look non deformable without assigning separate 
joints to them. It works with single mesh selection (by transform or shape), multiple selection 
or mesh components selection. If selected one mesh or it's components that allows each joint 
weight adjustment separately.
However, it is not recommended to run script with multiple shells of single mesh selected. 
They all will have the same weights. Maybe I'll add support of that case later.
'''


from functools import partial
import maya.cmds as cmds


class AverageSkinWeights(object):
    
    def __init__(self):

        # Check if window or window preferences already exists.  
        if cmds.window('ASW', exists=1):
            cmds.deleteUI('ASW')
        if cmds.windowPref('ASW', exists=1):
            cmds.windowPref('ASW', remove=1)

        # Create main UI.  
        note = str("Script allows you to make hard surface objects look non deformable \n" + 
                   "without assigning separate joints to them.\n\n" + 
                   "Select skinned mesh/meshes or it's components and press 'Execute'\n" + 
                   "Single selection of mesh or it's components " + 
                   "allows each joint weight adjustment separately.")

        mainW = cmds.window('ASW', title='Average skin weights', width=500, height=115)
        self.__mainL = cmds.columnLayout(adjustableColumn=1, rowSpacing=10, parent=mainW)
        self.__execB = cmds.button(label='Execute', parent=self.__mainL, height=30, command=partial(self.__exec_button))
        self.__noteL = cmds.rowLayout(parent=self.__mainL, numberOfColumns=3, columnWidth3=(35, 15, 150), adjustableColumn=3, columnAttach=[(1, 'left', -60), (2, 'left', -60), (3, 'left', -50)])
        cmds.text(label='lock: ', parent=self.__noteL)
        self.__mainChB = cmds.checkBox(label='', parent=self.__noteL, enableKeyboardFocus=1, value=0, changeCommand=self.__UI_switch_all_chB)
        self.__noteT = cmds.text(label=note, parent=self.__noteL)
        cmds.showWindow('ASW')

        # Variables  
        self.__vtxList = list(())
        self.__jntList = list(())
        self.__SCname = str('')
        self.__allData = dict()            # index : (joint name, awerage weight, lock state)  
        self.__UInames = dict()            # index : (joint name, slider name, checkbox name)  
        self.__UIslider = list(('', 0.0))  # joint name, input joint weight  
        self.__UIcheckBox = dict()         # joint name : lock state  


    def __exec_button(self, *args):

        selection = self.__check_selection()

        if len(selection) == 1:
            self.__get_data(selection[0])
            choice = self.__check_max_influences()
            if choice:
                self.__set_average_weights()
                self.__UI_extend()
            cmds.select(selection[0])

        else:
            for i in selection:
                self.__get_data(i)
                self.__set_average_weights()
            cmds.select(*selection)


    def __exec_slider(self, jntIndex, inputWeight):
        self.__UI_get_data(jntIndex, inputWeight)
        self.__set_exact_weights()
        self.__UI_update()


    def __check_selection(self):
        ''' Check selection and generate the list of objects to further operations.
        '''
        tempDict = dict()
        selection = cmds.ls(sl=1, long=1, flatten=0)

        if not selection:
            raise Exception ("Select several meshes, one mesh or mesh components.")

        elif not '.' in selection[0] and len(selection) == 1:
            # Check if selection is a transform mesh or a shape mesh. 
            if cmds.listRelatives(selection, shapes=1, type='mesh'):
                tempDict[selection[0]] = selection
            elif cmds.nodeType(selection) == 'mesh':
                tempDict[selection[0]] = cmds.listRelatives(selection, parent=1, fullPath=1)
            else:
                raise Exception ("Selected object must be a mesh.")

        else:
            # Check each element of multiple selection.  
            for i in selection:
                # If transform mesh  
                if cmds.listRelatives(i, shapes=1, type='mesh'):
                    tempDict[i] = [i]
                # If mesh component  
                elif '.' in i:
                    name = i.split('.')[0]
                    tempDict.setdefault(name, [x for x in selection if x.split('.')[0] == name])
                # If shape mesh  
                elif cmds.nodeType(i) == 'mesh':
                    tempDict[i] = cmds.listRelatives(i, parent=1, fullPath=1)

        return [tempDict.get(x) for x in tempDict]


    def __get_data(self, obj):
        ''' Get the data about object: 
        influenced vertices, skin cluster & joints that have influence.
        '''
        self.__vtxList = []
        self.__jntList = []
        self.__SCname = ''
        self.__allData = {}

        cmds.select(cl=1)

        # Check if object is a mesh or list of components.  
        if not '.' in obj[0] and len(obj) == 1:
            cmds.select(obj)
            objName = obj[0]
        else:
            for i in obj:
                cmds.select(i, add=1)
            objName = obj[0].split('.')[0]

        cmds.ConvertSelectionToVertices()

        self.__vtxList = cmds.ls(selection=1, flatten=0)

        # Get skin cluster.  
        objShapes = cmds.listRelatives(objName, fullPath=1, shapes=1)

        if cmds.listConnections(objShapes, type='skinCluster'):
            self.__SCname = cmds.listConnections(objShapes, type='skinCluster')[0]
        else:
            # Check if skinCluster connected via skinClusterSet.  
            for i in cmds.listConnections(objShapes, type='objectSet'):
                if (cmds.listConnections(i, type = 'skinCluster')):
                    self.__SCname = cmds.listConnections(i, type = 'skinCluster')[0]
                if self.__SCname: break

        if not self.__SCname:
            raise Exception ("{} No skin cluster found".format(objName))

        # Get influencing joints and lock joints that have no influence at all.  
        allJntList = cmds.skinPercent(self.__SCname, self.__vtxList, q=1, t=None)
        for j in allJntList:
            if cmds.skinPercent(self.__SCname, self.__vtxList, q=1, t=j) > 0.0:
                self.__jntList.append(j)
            else:
                cmds.setAttr(j + '.liw', True)

        self.__calculate_data()

        cmds.select(cl=1)


    def __check_max_influences(self):
        ''' Check if object's max influence lesser than amount of influencing joints.
        Let user choose to proceed or stop the script execution, if so.
        In that case joints with lowest influence will be excluded from influence
        to make amount of influencing joints equal to max influence.
        '''
        choiceB = True
        jntsAmount = len(self.__jntList)
        maxInflTrue = cmds.getAttr(self.__SCname + '.maintainMaxInfluences')
        maxInfl = cmds.getAttr(self.__SCname + '.maxInfluences')
        note = ('The max influence of selected is lesser than amount of influencing joints.' + 
               '\nIf proceed, joints with lowest influence will be excluded from influence.')

        if maxInflTrue and jntsAmount > maxInfl:

            choiceCD = cmds.confirmDialog(title='Cofirm', message=note, button=['Yes','No'], 
                                        icon='warning', defaultButton='Yes', cancelButton='No', 
                                        dismissString='No')

            if choiceCD == 'Yes':
                # Exclude joints with lowest influence.  
                weightsList = list(())
                for i, (j, w, l) in self.__allData.items():
                    weightsList.append(w)
                for count in range(jntsAmount-maxInfl):
                    for i, (j, w, l) in self.__allData.items()[:]:
                        if min(weightsList) == w:
                            cmds.skinPercent(self.__SCname, self.__vtxList, tv=[(j, 0)])
                            cmds.setAttr(j + '.liw', True)
                            self.__allData.pop(i)
                    weightsList.remove(min(weightsList))

            else: choiceB = False

        return choiceB


    def __calculate_data(self):
        ''' Get average weight of vertices for each joint, 
        joints lock state and collect it in single variable.
        '''
        for j in self.__jntList:
            index = self.__jntList.index(j)
            self.__allData[index] = (j, 
                                     cmds.skinPercent(self.__SCname, self.__vtxList, q=1, t=j), 
                                     cmds.getAttr(j + '.liw'))


    def __set_average_weights(self):
        ''' Lock joints with 0.0 influence. Unlock influencing joints, 
        set average weight to vertices and lock influencing joints.
        '''
        allJntList = cmds.skinPercent(self.__SCname, self.__vtxList, q=1, t=None)
        for j in allJntList:
            if cmds.skinPercent(self.__SCname, self.__vtxList, q=1, t=j) == 0.0:
                cmds.setAttr(j + '.liw', True)

        for i, (j, w, l) in self.__allData.items():
            cmds.setAttr(j + '.liw', False)

        for i, (j, w, l) in self.__allData.items():
            cmds.skinPercent(self.__SCname, self.__vtxList, transformValue=[(j, w)])
            cmds.setAttr(j + '.liw', True)


    def __set_exact_weights(self):
        ''' Lock/unlock joints according to checkboxes & set weight gotten from slider.
        '''
        # amucb = (self.__UIcheckBox.values()).count(False)  # This Only Work in Python3.7~
        amucb = list(self.__UIcheckBox.values()).count(False) # Amount of unlocked checkboxes.  
        jntName = self.__UIslider[0]
        weightSet = self.__UIslider[1]
        scbsl = self.__UIcheckBox[jntName]
        # scbsl is lock/unlock state of checkbox corresponding to input slider.  

        for j, l in self.__UIcheckBox.items():
            cmds.setAttr(j + '.liw', l)

        # Prevent weird Maya bug that allows set sum interactive weight less than 1.0.  
        if amucb == 0 or len(self.__allData) == 1 or (amucb == 1 and not scbsl):
            pass
        else:
            cmds.skinPercent(self.__SCname, self.__vtxList, 
                             transformValue=[(jntName, weightSet)])

            # Set average weight to other unlocked joints just for sure.  
            self.__calculate_data()
            for i, (j, w, l) in self.__allData.items():
                if not l:
                    cmds.skinPercent(self.__SCname, self.__vtxList, transformValue=[(j, w)])
                    cmds.setAttr(j + '.liw', True)

            for j, l in self.__UIcheckBox.items():
                cmds.setAttr(j + '.liw', l)


    def __UI_extend(self):
        ''' Edit UI controls. Add sliders corresponding to joints.
        '''
        u, v = cmds.window('ASW', q=1, topLeftCorner=1)  # Window coordinates.  

        cmds.button(self.__execB, e=1, command=self.__UI_update, label='Update UI values', statusBarMessage='Update UI values if Undo/Redo commands were called.')
        cmds.rowLayout(self.__noteL, e=1, columnAttach=[(1, 'right', 0), (2, 'left', 0), (3, 'right', 50)])
        cmds.text(self.__noteT, e=1, label='Adjust weights if needed')

        for i, (j, w, l) in self.__allData.items(): 
            sliderL = cmds.rowLayout(parent=self.__mainL, numberOfColumns=3, columnWidth3=(35, 15, 150), adjustableColumn=3, columnAttach=[(1, 'right', 0)])
            cmds.text(label='lock: ', parent=sliderL)
            checkBox = cmds.checkBox(label='', parent=sliderL, value=l, enableKeyboardFocus=1)
            slider = cmds.floatSliderGrp(label=j, parent = sliderL, field=1, min=0.0, max=1.0, step=0.0001, value=w, columnWidth3=[150,45,200], changeCommand=partial(self.__exec_slider,i))

            # Collect UI controls names.  
            self.__UInames[i] = (j, slider, checkBox)
        
        cmds.window('ASW', e=1, topLeftCorner=[(u+1), (v+1)])


    def __UI_get_data(self, jntIndex, inputWeight):
        ''' Get input slider data & lock state of checkboxes.
        '''
        self.__UIslider[0] = self.__UInames[jntIndex][0]  # Get joint name.  
        self.__UIslider[1] = inputWeight

        for i, (j, s, chb) in self.__UInames.items():
            jntN = self.__UInames[i][0]
            self.__UIcheckBox[jntN] = cmds.checkBox(chb, q=1, v=1)


    def __UI_switch_all_chB(self, *args):
        ''' Switch states of all checkboxes in one main checkbox.
        '''
        if cmds.checkBox(self.__mainChB, q=1, value=1):
            for i, (j, s, chb) in self.__UInames.items():
                cmds.checkBox(chb, e=1, value=1)
        else:
            for i, (j, s, chb) in self.__UInames.items():
                cmds.checkBox(chb, e=1, value=0)


    def __UI_update(self, *args):

        # Recalculate awerage weights.  
        self.__calculate_data() 

        # Set average weight to corresponding slider.  
        for i, (j, s, chb) in self.__UInames.items():
            cmds.floatSliderGrp(s, e=1, v=self.__allData[i][1])


AverageSkinWeights()
