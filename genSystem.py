import re;
import math;
import sys, traceback
import copy
import os
execfile('epicsParse.py')

"""
execfile('genSystem.py')
"""


print "Loading epics-spreadsheet python generator functions"

helpscreen = """

#Supply a tab delimited spreadsheet
#open a python shell as below
xterm &
#in the xterm
python


#Examples to generate the dig driver if digtizer ss is updated

#In the python shell
#set is_do_screenss to 1 to gen screens
is_do_screenss=1
#tell where your working copy of carlware is. No '/'on the end!!
code_location='/global/devel'
genDGSDigitizerDriver('MDRM.csv') or genDGSMasterTrigger('ss.csv') or genDGSRouterTrigger('ss.csv')
genDGSDigitizerDriver('/home/dgs/MDRM.csv')
genDGSDigitizerDriver('/home/dgs/specialSpreadsheet.csv')


For DGS, after python generation, you must run make on con5
From a unix prompt (not python):

ssh con5
#it may be devel or develbuild... depending on where you are building from
cd /global/devel/gretTop/9-22/dgsDrivers
make
cd ..
cd dgsIoc
make

#For help do this in python:
print helpscreen

"""

print helpscreen

#Debugging stuff
# for pv in findAsyn(master,'param','MASK'): pv.getPvName();pv.getAsynSpec()['param'];pv.getAsynSpec()['mask']
#master = readEpicsDb('Master.template')
#trigger = readEpicsDb('Trigger.template')
#master.extend(trigger)
#len(master)


#
#
# Global variables
#
#
#
# set to 0 for no screen generation.
# set to 1 for css screen generation.
# set to 2 for edm screen generation.
is_do_screens = 2

#tell where the runtime is. it is generatlly either /global/devel, 
#or /globel/develbuid
#Set to None for not copying files to build area, but only local copues 
# in the script directory.

code_location = '/global/devel'
#code_location = '/global/develbuild'
#code_location = None

#spread sheet column delimiter. 
ss_delimiter='\t'
#ss_delimiter=','

###################################################################################
#
#generate C code, st.cmd files, epics dbs, guis
#
#
#####################################################################################


def genDGSMasterTrigger(ssname):
	
	global code_location
	global is_do_screens
	global ss_delimiter

	global e_pvnamestr
	global e_pvnamestrrbv

	# These are the wild cards P and R, the %s will contain the pv name i.e. led_threshold

	e_pvnamestr='$(P)$(R)%s'
	e_pvnamestrrbv='$(P)$(R)%s_RBV'

	#	
	# Initialize Gui object for screen generation
	#


	if is_do_screens==2:
		gui=edmMaker()
	elif is_do_screens!=2:
		gui=screenMaker()

	#
	# Create SS object and readin spreadsheet
	#

	ss=spreadsheet()
	ss.delimiter=ss_delimiter
	ss.read(ssname)

	#
	# Generate register level pvs, one pv per reg. longouts and longins.
	# 

	rawdb = ssToRawEpicsDB(ss,'dgsMTrigRegisters.template')
	#for debugging
	#for a in find(rawdb,"disc",None,None,None): print a.getPvName()

	#
	#Generate  c code for dig. asyn driver
	#

	ssToAsynC(ss,'asynMTrigParams.c','asynMTrigParams.h')

	#
	# Generate the IOC startup comand file
	#

	makeTrigStCmd('DGS')

	#
	# Generate some screens
	#

	if (is_do_screens==1):
		

		#generate board level pvs	
		gui.xw=[300,100,100]
		scr = gui.dbToScreen1(rawdb,'DGS MTrigger Registers for $(P)$(R)',False,False,32,None)

		scr.writeXML('dgsMTrigRegisters.opi')

	if (is_do_screens==2):
    
        # generate register screen
		gui.xw=[240,85,85]
		scr = gui.dbToRegister(rawdb,'DGS MTrigger Registers for $(P)$(R)',31,None)
		writelist(scr,'dgsMTrigRegisters.edl')

	#
	# Generate User PVs and create template file
	#

	epicsdb = ssToUserPvs(ss,None)
	writeEpicsDb(epicsdb,'dgsMTrigUser.template')

	# Generate Screens for User PVs

	if (is_do_screens==1):
		#make sure master2.opi has RBV on readback pvs
		mst=cssScreen()
		mst.readXML('master2.opi')

		ser=cssScreen()
		ser.readXML('serdes.opi')

		mdiag=cssScreen()
		mdiag.readXML('MasterDiag.opi')

		lnk=cssScreen()
		lnk.readXML('links.opi')


		tl=cssScreen()
		tl.readXML('TrigLock.opi')

		tl=gui.screenAddRBV(tl);

		mst=gui.screenAddRBV(mst);
		ser=gui.screenAddRBV(ser);
		mdiag=gui.screenAddRBV(mdiag);
		lnk=gui.screenAddRBV(lnk);
		
		tl.writeXML('TrigLockR.opi')

		mst.writeXML('master2R.opi')
		ser.writeXML('serdesR.opi')
		mdiag.writeXML('MasterDiagR.opi')
		lnk.writeXML('linksR.opi')
		
		
		allwidgets=mst.getWidgets()
		allwidgets = allwidgets + ser.getWidgets()
		allwidgets = allwidgets + mdiag.getWidgets()
		allwidgets = allwidgets + lnk.getWidgets()
		

		#epics database to gen where pv has no dispay. need new widgets
		scrdb=[]
		
		for pv in epicsdb:
			found = 0
			for w in allwidgets:
				
				
				if pv.getPvName() == w.getField('pv_name'):
					found=1
			
			if found==0:
				scrdb.append(pv)
				
				gui.xw=[300,100,100]

		newscr = gui.dbToScreen1(scrdb,'Master Trigger $(T)',False,False,32,None)
	
		newscr.writeXML('master3.opi')
		

	# copy genarated files to proper areas if requested

	if code_location!=None:
	
		if is_do_screens==1: 
			os.system('cp TrigLockR.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp dgsMTrigRegisters.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp linksR.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp master3.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp master2R.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp MasterDiagR.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp serdesR.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
	
	
		os.system('cp asynMTrigParams.c %s/gretTop/9-22/dgsDrivers/dgsDriverApp/src/.'%(code_location))
		os.system('cp asynMTrigParams.h %s/gretTop/9-22/dgsDrivers/dgsDriverApp/src/.'%(code_location))


		os.system('cp dgsMTrigUser.template %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsMTrigRegisters.template %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))

		os.system('cp vme32.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))

		if is_do_screens==1: 
			os.system('cp dgsMTrigRegisters.opi /home/dgs/CSS-Workspaces/Default/CSS/.')


###################################################################################
#
#
#
#####################################################################################

def genDGSRouterTrigger(ssname):

	#gen screen for dig. board. use macros for use with any board.
	gui=screenMaker()

	e_pvnamestr='$(P)$(R)%s'
	e_pvnamestrrbv='$(P)$(R)%s_RBV'

	#generate register level pvs, one pv per reg. longouts and longins.
	#pv namessname is $(P)$(R)reg_%s , $(P)$(R)reg_%s_RBV


	ss=spreadsheet()
	ss.delimiter=ss_delimiter
	ss.read(ssname)

	rawdb = ssToRawEpicsDB(ss,'dgsRTrigRegisters.template')

	
#for debugging
#for a in find(rawdb,"disc",None,None,None): print a.getPvName()


	#
	#Generate  c code for dig. asyn driver
	#
	
	ssToAsynC(ss,'asynRTrigParams.c','asynRTrigParams.h')


	if (is_do_screens==1):
		gui=screenMaker()

		#generate board level pvs	
		gui.xw=[300,100,100]
		scr = gui.dbToScreen1(rawdb,'DGS Router Registers $(P)$(R)',False,False,32,None)

		scr.writeXML('dgsRTrigRegisters.opi')

	if (is_do_screens==2):
		gui=edmMaker()
		    
        # generate register screen
		gui.xw=[180,85,85]
		scr = gui.dbToRegister(rawdb,'DGS Router Registers for $(P)$(R)',31,None)
		writelist(scr,'dgsRTrigRegisters.edl')

	epicsdb = ssToUserPvs(ss,None)

#	for pv in epicsdb: 
#		pv.setPvName(pv.getPvName().replace('$(P)$(R)',''))


	writeEpicsDb(epicsdb,'dgsRTrigUser.template')

	if (is_do_screens==1):
		#make sure master2.opi has RBV on readback pvs
		rtr=cssScreen()
		rtr.readXML('Router2.opi')

		rdiag=cssScreen()
		rdiag.readXML('RouterDiag.opi')
	
		ser=cssScreen()
		ser.readXML('serdes.opi')

	

		lnk=cssScreen()
		lnk.readXML('links.opi')


		rtr=gui.screenAddRBV(rtr);
		rdiag=gui.screenAddRBV(rdiag);
		
		
		rtr.writeXML('Router2R.opi')
		rdiag.writeXML('RouterDiagR.opi')
		
		
		allwidgets=rtr.getWidgets()
		allwidgets = allwidgets + ser.getWidgets()
		allwidgets = allwidgets + rdiag.getWidgets()
		allwidgets = allwidgets + lnk.getWidgets()
		

		#epics database to gen where pv has no dispay. need new widgets
		scrdb=[]
		
		for pv in epicsdb:
			found = 0
			for w in allwidgets:
				
				
				if pv.getPvName() == w.getField('pv_name'):
					found=1
			
			if found==0:
				scrdb.append(pv)
				
				gui.xw=[300,100,100]

		newscr = gui.dbToScreen1(scrdb,'Router Trigger $(T)',False,False,32,None)
	
		newscr.writeXML('router3.opi')
		


	#if (is_do_screens==1): 
	#	os.system('cp dgsMTrigRegisters.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
	
	
		###
	

	# copy c code to proper area

	if code_location!=None:
	
		if is_do_screens==1: 
			os.system('cp dgsRTrigRegisters.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp Router2R.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp RouterDiagR.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp router3.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			
	
		os.system('cp asynRTrigParams.c %s/gretTop/9-22/dgsDrivers/dgsDriverApp/src/.'%(code_location))
		os.system('cp asynRTrigParams.h %s/gretTop/9-22/dgsDrivers/dgsDriverApp/src/.'%(code_location))



		os.system('cp dgsRTrigUser.template %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsRTrigRegisters.template %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))

###################################################################################
#
#generate C code, st.cmd files, epics dbs, guis
#
#
#####################################################################################


def genDGSDigitizerDriver(ssname):
	
	
	global code_location
	global is_do_screens
	global ss_delimiter
	global e_pvnamestr
	global e_pvnamestrrbv
	
	# These are the wild cards P and R, the %s will contain the pv name i.e. led_threshold

	e_pvnamestr='$(P)$(R)%s'
	e_pvnamestrrbv='$(P)$(R)%s_RBV'

	# make object of GUi which gen screen for dig. board. use macros for use with any board.


	
	#
	# Read in specified spreadsheet
    #

	ss=spreadsheet()
	ss.delimiter=ss_delimiter
	ss.read(ssname)
	
	#
	# Generate register level pvs, one pv per reg. longouts and longins.
    #

	rawdb = ssToRawEpicsDB(ss,'dgsDigRegisters.template')
	#for debugging
	#for a in find(rawdb,"disc",None,None,None): print a.getPvName()
	

	#
	# Generate board level screens for the regsiter PVs.
	#

	if (is_do_screens==1):
		gui=screenMaker()
		
		gui.xw=[300,100,100]
		scr = gui.dbToScreen1(rawdb,'DGS Digitizer Board Registers $(P)$(R)',False,False,32,None)	
		
		#add a related screen button.
		button=cssWidget()
		button.setType('dispbutton')
		button.addDisp('digEngChanRegisters.opi',"Channels",{'A':'A'})
		button.setField('height','50')
		button.setField('width','200')
		button.setField('x','600')
		button.setField('y','100')
		button.setField('label',"Channels")
	
		scr.addWidget(button)
		scr.writeXML('digitizer3.opi')								
	
		#generate board level pvs	
		gui.xw=[200,100,100]
		scr = gui.dbToScreen1(rawdb,'DGS Digitizer Chan Registers $(P)$(R)',True,False,30,None)
		
		scr.writeXML('digEngChanRegisters.opi')
		
	if (is_do_screens==2):
		gui=edmMaker()
		    
        # generate register screen
		gui.xw=[180,85,85]
		scr = gui.dbToRegister2(rawdb,'Digitizer Registers for $(P)$(R)',31,'Dig','DigRegisters.edl')
		#writelist(scr,'DigRegisters.edl')
		#scr = gui.dbToRegister2(rawdb,'Digitizer Registers for $(P)$(R) CH %%CH',31,'Chan','DigChan%%CHRegisters.edl')
		scr = gui.dbToRegister2(rawdb,'Digitizer Channel Registers for $(P)$(R)',30,'Chan','DigChanRegisters.edl')
		#writelist(scr,'DigChanRegisters.edl')

	#
	# Generate st cmd files for 11 dig crates
	#
	vmelist = [1,2,3,4,5,6,7,8,9,10,11]
	boardlist=[1,2,3,4]
	vmecrates=['VME01','VME02','VME03','VME04','VME05','VME06','VME07','VME08','VME09','VME10','VME11']
	brds=['MDIG1','SDIG1','MDIG2','SDIG2']
	chans=['0','1','2','3','4','5','6','7','8','9']

	# Note: vmelist and boardlist need to be replaced by vmecrates and brds.

	#makeDigStCmd(vmelist,boardlist, 'DGS')	
	makeDigStCmd(vmelist,brds, 'DGS')
	
	#
	#Generate  c code for dig. asyn driver
	#

	ssToAsynC(ss,'asynDigParams.c','asynDigParams.h')
	
	#
	# Generate user pvs for a digitizer- $(P)$(R) is included in pv names.
	#

	epicsdb = ssToUserPvs(ss,None)
		
	
	#win comp max and min need to read back as signed 16 bit- use calcout rec to reintreprt
	wcmin= find(epicsdb,"win_comp_min_RBV$",None,None,None)[0]	
	wcminl= find(epicsdb,"win_comp_min_RBVLONGIN$",None,None,None)[0]
	wcminc = makeSignShort('$(P)$(R)win_comp_min_RBVCALC',wcminl.getPvName(),wcmin.getPvName()+' PP')
	wcmin.setField('INP',wcminc.getPvName())
	epicsdb.append(wcminc)
		
		
	#win comp max and min need to read back as signed 16 bit- use calcout rec to reintreprt
	wcmax= find(epicsdb,"win_comp_max_RBV$",None,None,None)[0]	
	wcmaxl= find(epicsdb,"win_comp_max_RBVLONGIN$",None,None,None)[0]
	wcmaxc = makeSignShort('$(P)$(R)win_comp_max_RBVCALC',wcmaxl.getPvName(),wcmax.getPvName()+' PP')
	wcmax.setField('INP',wcmaxc.getPvName())
	epicsdb.append(wcmaxc)	

	#add timestamp pv. Digxxx_CV_LiveTS		
	epicsdb.append(makePvLiveTS())	
	epicsdb.append(makeCVRunning())

	
	# Write out template file
	writeEpicsDb(epicsdb,'dgsDigUser.template')
	

	# Generate user PV screens
	
	if (is_do_screens==1):
	
		#make user screen for dig board
		gui.xw=[300,100,100]
		scr = gui.dbToScreen1(epicsdb,'DGS Digitizer Board $(P)$(R)',False,False,24,None)
		
	
		#add a related screen button.
		button=cssWidget()
		button.setType('dispbutton')
	
		button.setField('height','50')
		button.setField('width','200')
		button.setField('x','600')
		button.setField('y','100')
		button.setField('label',"Channels")
	
		for c in range(10):
			button.addDisp('segment.opi',"Chan %d"%c,{'CH':'%d'%c})
	
		scr.addWidget(button)
		scr.writeXML('Digitizer.opi')

		#genearte screen for dig channel, a single channel using macros
		
		scr = gui.dbToScreen1(epicsdb,'DGS Digitizer Channel $(P)$(R) $(CH)',True,True,24,None)
		scr.writeXML('segment.opi')

	#
	# Generate Global PV db files
	#
	
	

	#generate global pvs for digitizers and all channges. all pvs live on the trigger mod or softioc
	#glo_db=ssToDigGlobalPVsDist(ssname, vmelist,boardlist,None)
	glo_db=ssToDigGlobalPVsDist(ssname, vmelist,brds,None)
	
	#add a global timedelay pv. for inLoop.st to tell how fast it runs
	glo_db.append(makeSoftAo('GLBL:DAQ:DAQTimeDelayA','DAQ RdTime','0.02','GLBL'))
	
	glo_db.append(makeSoftAo('GLBL:DAQ:DAQTimeDelayB','DAQ RdTime Full','0.01','GLBL'))
	
	glo_db.append(makeSoftAo('GLBL:DAQ:BuildSendDelay','Send/Sort DlyTime','0.01','GLBL'))
	glo_db.append(makeSoftBo('GLBL:DAQ:BuildSendEna','SendSort Ena','1','Disabled','Enabled','GLBL'))

	
	saveEpicsDbByCrates(glo_db,'DGS')
	
        #
	# Generate global PV's
	#

	if (is_do_screens==1):
	
		
		#make dig global screen
		#make a database excluding dfanouts, and channel pvs. just real globals are included
		gloscr=[]
		for d in glo_db:
			if d.getRecType()!='dfanout' and d.isChanPv()==False:
				gloscr.append(d)
		
		scr = gui.dbToScreen1(gloscr,'Digitizer Global Screen',False,False,24,None)
		scr.writeXML('DGTL_Global.opi')

		#copy opis to proper area.
		
		if code_location!=None:
			os.system('cp DGTL_Global.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp Digitizer.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp segment.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp digitizer3.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
			os.system('cp digEngChanRegisters.opi /home/dgs/CSS-Workspaces/Default/CSS/.')
		
		###
	

	# copy c code to proper area

	if code_location!=None:
		os.system('cp asynDigParams.c %s/gretTop/9-22/dgsDrivers/dgsDriverApp/src/.'%(code_location))
		os.system('cp asynDigParams.h %s/gretTop/9-22/dgsDrivers/dgsDriverApp/src/.'%(code_location))

		os.system('cp dgsGlobals_DGS_VME01.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME02.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME03.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME04.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME05.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME06.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME07.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME08.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME09.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME10.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_VME11.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsGlobals_DGS_GLBL.db %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))



		os.system('cp dgsDigUser.template %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))
		os.system('cp dgsDigRegisters.template %s/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/.'%(code_location))


		os.system('cp vme01.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme02.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme03.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme04.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme05.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme06.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme07.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme08.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme09.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme10.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme11.DGS.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp cdCommands_DGS %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))

		
	#gui.makeDigCountScreen(epicsdb,'digCounters.opi')
	return()

###################################################################################
#
#generate C code, st.cmd files, epics dbs, guis
#
#
#####################################################################################

def genDFMADig(ssname):
	
	
	global code_location
	global is_do_screens
	global ss_delimiter
	global e_pvnamestr
	global e_pvnamestrrbv
	
	
	e_pvnamestr='$(P)$(R)%s'
	e_pvnamestrrbv='$(P)$(R)%s_RBV'

	#this is the spreadsheet (ss)
	#ssname = 'MDRM.csv'
	#gen screen for dig. board. use macros for use with any board.
	gui=screenMaker()
	
	ss=spreadsheet()
	ss.delimiter=ss_delimiter
	ss.read(ssname)
	
	#generate st cmd files for 11 dig crates
		
	vmelist = [1,2,3,4,5,6,7,8,10]
	boardlist=[1,2,3,4]
	
	vmecrates=['VME01','VME02','VME03','VME04','VME05','VME06','VME07','VME08','VME10']
	brds=['MDIG1', 'MDIG2','MDIG3', 'MDIG4']
	chans=['0','1','2','3','4','5','6','7','8','9']

        # generate startup command files
	user_package_start=200
	makeDigStCmd(vmelist,brds, 'DFMA')

	#generate globak ovs for digitizers and all channges. all pvs live on the trigger mod or softioc
	glo_db=ssToDigGlobalPVsDist(ssname, vmelist,boardlist,None)
	
	#add a global timedelay pv. for inLoop.st to tell how fast it runs
	glo_db.append(makeSoftAo('GLBL:DAQ:DAQTimeDelayA','DAQ RdTime','0.02','GLBL'))
	
	glo_db.append(makeSoftAo('GLBL:DAQ:DAQTimeDelayB','DAQ RdTime Full','0.01','GLBL'))
	
	glo_db.append(makeSoftAo('GLBL:DAQ:BuildSendDelay','Send/Sort DlyTime','0.01','GLBL'))
	glo_db.append(makeSoftBo('GLBL:DAQ:BuildSendEna','SendSort Ena','1','Disabled','Enabled','GLBL'))

	
	saveEpicsDbByCrates(glo_db,'DFMA')
	
		
	if code_location!=None:

		os.system('cp dgsGlobals_DFMA_GLBL.db %s/gretTop/9-22/dgsIoc/db/.'%(code_location))

		for crate in vmecrates:
			os.system('cp dgsGlobals_DFMA_%s.db %s/gretTop/9-22/dgsIoc/db/.'%(crate,code_location))
	


			os.system('cp %s.DFMA.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(crate.lower(),code_location))
		

	#gui.makeDigCountScreen(epicsdb,'digCounters.opi')
	return()


###################################################################################
#
#generate C code, st.cmd files, epics dbs, guis
#
#
#####################################################################################


def genDFMAMasterTrig(ssname):

	
	global code_location
	global is_do_screens
	global ss_delimiter

	global e_pvnamestr
	global e_pvnamestrrbv

	
	ss=spreadsheet()
	ss.delimiter=ss_delimiter
	ss.read(ssname)


	makeTrigStCmd5('DFMA')


	e_pvnamestr='%s'
	e_pvnamestrrbv='%s_RBV'

	epicsdb = ssToUserPvs(ss,None)
	writeEpicsDb(epicsdb,'dfmaMTrigUser.template')

	if code_location!=None:
		os.system('cp vme32.DFMA.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))


		os.system('cp dfmaMTrigUser.template %s/gretTop/9-22/dgsIoc/db/.'%(code_location))

	





###################################################################################
#
#generate C code, st.cmd files, epics dbs, guis
#
#
#####################################################################################


def genDFMARouterTrig(ssname):

	
	global code_location
	global is_do_screens
	global ss_delimiter

	global e_pvnamestr
	global e_pvnamestrrbv

	

	ss=spreadsheet()
	ss.delimiter=ss_delimiter
	ss.read(ssname)

	epicsdb = ssToUserPvs(ss,None)

	for pv in epicsdb: 
		pv.setPvName(pv.getPvName().replace('$(P)$(R)',''))


	writeEpicsDb(epicsdb,'dfmaRTrigUser.template')

	if code_location!=None:
		os.system('cp dfmaRTrigUser.template %s/gretTop/9-22/dgsIoc/db/.'%(code_location))



###################################################################################
#
#generate C code, st.cmd files, epics dbs, guis
#
#
#####################################################################################

def genCloDig(ssname):
	
	
	global code_location
	global is_do_screens
	global ss_delimiter
	global e_pvnamestr
	global e_pvnamestrrbv
	
	
	e_pvnamestr='$(P)$(R)%s'
	e_pvnamestrrbv='$(P)$(R)%s_RBV'

	#this is the spreadsheet (ss)
	#ssname = 'MDRM.csv'
	#gen screen for dig. board. use macros for use with any board.
	gui=screenMaker()
	
	ss=spreadsheet()
	ss.delimiter=ss_delimiter
	ss.read(ssname)

	


	
	#generate st cmd files for 11 dig crates
	vmelist = [1,2,3,4,5]
	boardlist=[1,2,3,4]
	
	makeDigStCmd(vmelist,boardlist, 'CLO')
	
	
	

	
	
	
	
	
	vmecrates=['VME01','VME02','VME03','VME04','VME05']
	brds=['DIG1', 'DIG2','DIG3', 'DIG4']
	chans=['0','1','2','3','4','5','6','7','8','9']


	#generate global db
	vmelist = [1,2,3,4,5]
	boardlist=[1,2,3,4]





	#generate globak ovs for digitizers and all channges. all pvs live on the trigger mod or softioc
	glo_db=ssToDigGlobalPVsDist(ssname, vmelist,boardlist,None)
	
	#add a global timedelay pv. for inLoop.st to tell how fast it runs
	glo_db.append(makeSoftAo('GLBL:DAQ:DAQTimeDelayA','DAQ RdTime','0.02','GLBL'))
	
	glo_db.append(makeSoftAo('GLBL:DAQ:DAQTimeDelayB','DAQ RdTime Full','0.01','GLBL'))
	


	glo_db.append(makeSoftAo('GLBL:DAQ:BuildSendDelay','Send/Sort DlyTime','0.01','GLBL'))
	glo_db.append(makeSoftBo('GLBL:DAQ:BuildSendEna','SendSort Ena','1','Disabled','Enabled','GLBL'))

	
	saveEpicsDbByCrates(glo_db,'CLO')
	
	
	
	if code_location!=None:

		os.system('cp dgsGlobals_CLO_GLBL.db %s/gretTop/9-22/dgsIoc/db/.'%(code_location))

		os.system('cp dgsGlobals_CLO_VME01.db %s/gretTop/9-22/dgsIoc/db/.'%(code_location))
		os.system('cp dgsGlobals_CLO_VME02.db %s/gretTop/9-22/dgsIoc/db/.'%(code_location))
		os.system('cp dgsGlobals_CLO_VME03.db %s/gretTop/9-22/dgsIoc/db/.'%(code_location))
		os.system('cp dgsGlobals_CLO_VME04.db %s/gretTop/9-22/dgsIoc/db/.'%(code_location))
		os.system('cp dgsGlobals_CLO_VME05.db %s/gretTop/9-22/dgsIoc/db/.'%(code_location))



		os.system('cp vme01.CLO.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme02.CLO.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme03.CLO.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme04.CLO.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp vme05.CLO.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))
		os.system('cp cdCommands_CLO %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))



	



	

	

	#gui.makeDigCountScreen(epicsdb,'digCounters.opi')
	return()





###################################################################################
#
#generate C code, st.cmd files, epics dbs, guis
#
#
#####################################################################################


def genCLOTrig():

	
	global code_location
	global is_do_screens
	global ss_delimiter

	global e_pvnamestr
	global e_pvnamestrrbv

	

	makeTrigStCmd('CLO')



	if code_location!=None:
		os.system('cp vme32.CLO.cmd %s/gretTop/9-22/dgsIoc/iocBoot/iocArray/.'%(code_location))



	




###################################################################################
#
#generate C code, st.cmd files, epics dbs, guis
#
#
#####################################################################################

def genDSSDSt():

	global dig_st_template
	global user_package_start	
	
	
	
	#generate st cmd files for 11 dig crates
	vmelist = [1,2,3,4,5,6,7,8,10]
	boardlist=[1,2,3,4]
	user_package_start=200
	
	makeDigStCmd(vmelist,boardlist, 'DFMA')
	
	os.system('cp *.DFMA.cmd /global/develbuild/gretTop/9-22/dgsIoc/iocBoot/iocArray/.')


def genDSSDSystem():
	
	
	global dig_st_template
	global user_package_start	
	
	ssname = 'MDRM.csv'
	#gen screen for dig. board. use macros for use with any board.
	gui=screenMaker()
	


	
	
	#generate st cmd files for 11 dig crates
	vmelist = [1,2,3,4,5,6,7,8,10]
	boardlist=[1,2,3,4]
	user_package_start=200
	
	makeDigStCmd(vmelist,boardlist, 'DFMA')
	
	


	
	
	
	
	vmecrates=['VME01','VME02','VME03','VME04','VME05','VME06','VME07','VME08','VME10']
	brds=['DIG1', 'DIG2','DIG3', 'DIG4']
	chans=['0','1','2','3','4','5','6','7','8','9']


	#generate st cmd files for 11 dig crates
	vmelist = [1,2,3,4,5,6,7,8,10]
	boardlist=[1,2,3,4]





	#generate globak ovs for digitizers and all channges. all pvs live on the trigger mod or softioc
	glo_db=ssToDigGlobalPVsDist(ssname, vmelist,boardlist,None)
	
	#add a global timedelay pv. for inLoop.st to tell how fast it runs
	glo_db.append(makeSoftAo('GLBL:DAQ:DAQTimeDelayA','DAQ RdTime','0.02','GLBL'))
	
	glo_db.append(makeSoftAo('GLBL:DAQ:DAQTimeDelayB','DAQ RdTime Full','0.01','GLBL'))
	


	glo_db.append(makeSoftAo('GLBL:DAQ:BuildSendDelay','Send/Sort DlyTime','0.01','GLBL'))
	glo_db.append(makeSoftBo('GLBL:DAQ:BuildSendEna','SendSort Ena','1','Disabled','Enabled','GLBL'))

	
	dbpath = '/global/develbuild/gretTop/9-22/dgsIoc/db/'
	saveEpicsDbByCrates2(glo_db,'DFMA',dbpath)
	
	dbpath = ''
	saveEpicsDbByCrates2(glo_db,'DFMA',dbpath)
	
	


	
	
	if is_do_screens:
	
		#make dig global screen
		#make a database excluding dfanouts, and channel pvs. just real globals are included
		gloscr=[]
		for d in glo_db:
			if d.getRecType()!='dfanout' and d.isChanPv()==False:
				gloscr.append(d)
		
		
		
		scr = gui.dbToScreen1(gloscr,'Digitizer Global Screen',False,False,24,None)
		scr.writeXML('DGTL_Global.opi')
	


	#generate user pvs for a digitizer- $(P)$(R) is included in pv names.
	#this is just ot make a screen
	epicsdb = ssToUserPvs(ssname,None)
		

	
	if is_do_screens:
	
		gui.makeDigCountScreenDFMA(epicsdb,'digCounters.opi')
		gui.makeEvtRateScreenDFMA('eventRates2.opi')
		gui.makeGloEvtRateScreenDFMA('gloEvtRates.opi')
	
		gui.makeDAQDbgScreen()
	
		#copy opis to proper area.
	
	
		os.system('cp *.opi /home/dgs/CSS_Workspaces/Default/CSS/.')
	
	# copy c code to proper area


	#os.system('cp dgsGlobals.db /global/develbuild/gretTop/9-22/dgsIoc/db/.')


	os.system('cp *.DFMA.cmd /global/develbuild/gretTop/9-22/dgsIoc/iocBoot/iocArray/.')


	

	

	return()








###################################################################################
#
#generate screens that work with older names
#
#####################################################################################


def makeOldDGSScreens():


	daqdir='/global/develbuild/gretTop/9-22/dgsData/gretDataApp/Db/'
	drvdir='/global/develbuild/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/'
	
	gui=screenMaker()
	

	#generate screen for VME Summary
	#load the database from the DAQ system.
	daqcrate = readEpicsDb(daqdir+ 'daqCrate.template')
	#alter pv names
	
	
	vmecrates=['1','2','3','4','5','6','7','8','9','10','11']
	sendrate=makeGlobalEpicsDb(daqcrate,'SendRate','DAQC$(P)_CV_SendRate',vmecrates,None,None)
	buffavail=makeGlobalEpicsDb(daqcrate,'BuffersAvail','DAQC$(P)_CV_BuffersAvail',vmecrates,None,None)
	
	
	
	onmon = readEpicsDb(daqdir+ 'onMon.template')
	rcvrIP=makeGlobalEpicsDb(onmon,'RcvrIP','OnMon$(P)_CS_RcvrIP',vmecrates,None,None)
	att=makeGlobalEpicsDb(onmon,'CV_AttStat','OnMon$(P)_CV_AttStat',vmecrates,None,None)
	count=makeGlobalEpicsDb(onmon,'CV_Count','OnMon$(P)_CV_Count',vmecrates,None,None)

	#put pvs in interleaved order so we can have cols of different tuype of pvs
	#order of pvs in cols is below in the list. we have 11 crates, so interleave by 11
	newdb = interleaveEpicsDb([sendrate,buffavail,rcvrIP,att,  count  ],11)
	
	gui.width=100
	gui.xw=[50,50,200,50,50]
	scr = gui.dbToScreen2(newdb,'Sender Summary',vmecrates,['TCP', 'Buffs', 'Sendto', 'Stat', 'UDP'],None)
	scr.writeXML('vmesummary.opi')


	#
	#Generate dig board screen.
	#
	gretBoard = readEpicsDb(drvdir+ 'gretBoard.template')
	
	pvNameReplace(gretBoard,'Dig$(DB)','Dig1')
		
	#gen screen for dig. board. use macros for use with any board.
	gui=screenMaker()
	
	gui.xw=[300,100,100]
	scr = gui.dbToScreen1(gretBoard,'DGS Digitizer Board $(P)$(R)',False,False,24,None)
	scr.writeXML('digBoardtest.opi')
	
def writelist(list,filename):

	#write header file
	fileobj=open(filename,'w')
	
	for item in list:
		fileobj.write(item)
