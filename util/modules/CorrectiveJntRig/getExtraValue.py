import pymel.all as pm


xyzL = [ 'X', 'Y', 'Z' ]
pmL = [ '_P', '_M' ]
preL = [ '.Pos', '.Rot', '.Sca' ]

valL = []

guideL = pm.listRelatives('g_Slide_R')
for g, guide in enumerate(guideL):
	name = guide.split('_')
	prefix = name[1] + '_R_' + name[2]

	partVL = []
	for i, xyz in enumerate(xyzL):
		for j, PM in enumerate(pmL):
			obj = '_Rot' + xyz + PM
			
			attrVL = []
			for m, pre in enumerate(preL):
				for n, xyz2 in enumerate(xyzL):
					attr = pre+xyz2
					
					val = pm.getAttr(prefix+obj+attr)
					attrVL.append(val)
					
					# print(prefix+obj+attr, '>>>>>>', val)
			
			partVL.append(attrVL)
			
	valL.append(partVL)


