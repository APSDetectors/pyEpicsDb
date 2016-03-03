

import re;
import math;
import sys, traceback
import copy




##############################################################################
#
#
#
#
##############################################################################

#take spread sheet, gen c code for all registers.
#gen c code for h and cpp files. give out filenames
def ssToAsynC(ssname,cfilename,hfilename):
	



	#read spreadsheet into softchan pvs
	epicsdb = ssEpicsSoftChan(ssname)
	
	#write header file
	fileobj=open(hfilename,'w');

	fileobj.write("\n\n");

	nparams=0
	
	for pv in epicsdb:
		param = pv.getExtra('param')
		fileobj.write("// %s\n"%(pv.getField('DESC')))
		fileobj.write("int %s;\n"%(param))
		nparams=nparams+1
		
	fileobj.write("\n\n");
	fileobj.write("enum {num_params = %d};\n"%(nparams))	
	
	fileobj.write("\n\n");
		
	fileobj.close();


	fileobj=open(cfilename,'w');
	for pv in epicsdb:
		param = pv.getExtra('param')
		fileobj.write("// %s\n"%(pv.getField('DESC')))
		fileobj.write("createParam(\"%s\",asynParamUInt32Digital,&%s);\n"%(param,param))


			
	fileobj.write("\n\n");
	
	for pv in epicsdb:
		param = pv.getExtra('param')
		fileobj.write("setUIntDigitalParam(%s,1,0xffffffff );\n"%(param))
	
		

	fileobj.write("\n\n");
	
	for pv in epicsdb:
		param = pv.getExtra('param')
		fileobj.write("setAddress(%s,%s);\n"%(param,pv.getExtra('vmeaddr')))
	


	fileobj.close();



user_package_start=100

##############################################################################
#
# 
# board list is 1,2,3,4
# logical slot is boardlist -1
# so for slots 0, 2m then we number 1,3
##############################################################################

def makeDigStCmd(vmelist,boardlist, dgsDssd):

	global user_package_start
	global code_location
	
	boardID=[1,2,3,4]      # this is a trick for now
	
	cdcmd = cdcommands_template
	
	if code_location!=None:
		cdcmd = cdcmd.replace('%%CODELOCATION',code_location)
	
	fname = "cdCommands_%s"%(dgsDssd)
	f=open(fname,'w')
	f.write(cdcmd)
	f.close()
	
	for vme in vmelist:
	
		fname = "vme%02d.%s.cmd"%(vme,dgsDssd)
		f=open(fname,'w')
		
		stcmd=dig_st_template
		
		dbstr=''
		
		for brd in boardlist:
			#load reg pvs for registers
			#dbstr=dbstr + 'dbLoadRecords(\"db/dgsDigRegisters.template\",\"P=VME%02d:,R=DIG%d:,PORT=DIG%d\")\n'%(vme,brd,brd)
			dbstr=dbstr + 'dbLoadRecords(\"db/dgsDigRegisters.template\",\"P=VME%02d:,R=%s:,PORT=%s\")\n'%(vme,brd,brd)
		
		#load debugging pvs
		dbstr=dbstr + 'dbLoadRecords(\"db/asynDebug.template",\"P=VME%02d:,R=DBG:,PORT=DBG,ADDR=0,TIMEOUT=1\")\n'%(vme)
		
		#load user pvs
		for brd in boardlist:
			
			#dbstr=dbstr + 'dbLoadRecords(\"db/dgsDigUser.template\",\"P=VME%02d:,R=DIG%d:,PORT=DIG%d\")\n'%(vme,brd,brd)
			dbstr=dbstr + 'dbLoadRecords(\"db/dgsDigUser.template\",\"P=VME%02d:,R=%s:,PORT=%s\")\n'%(vme,brd,brd)
			
		#load daq pvs
		dbstr=dbstr + 'dbLoadRecords(\"db/daqCrate.template",\"DN=%d\")\n'%(vme)
		dbstr=dbstr + 'dbLoadRecords(\"db/onMon.template",\"DN=%d\")\n'%(vme)


		#load vme pvs
		log_brdnum=0
		for brd in boardID:
			
			dbstr=dbstr + 'dbLoadRecords(\"db/gretVME.template\",\"  DB=%d_%d, DC=%d \")\n'%(vme,brd,log_brdnum)
			dbstr=dbstr + 'dbLoadRecords(\"db/daqBoard.template\",\"  DB=%d_%d, DC=%d \")\n'%(vme,brd,log_brdnum)
			log_brdnum=log_brdnum+1	

		#load daq segments--- need to change driver??? or change names??
		log_brdnum=0
		for brd in boardID:
			for k in range(10):
				dbstr=dbstr + 'dbLoadRecords(\"db/daqSegment.template\",\"  DN=%d_%d, SN=%d,  DC=%d, CP=%d  \")\n'%(vme,brd,k,log_brdnum,k+1)
			log_brdnum=log_brdnum+1




		dbstr=dbstr + 'dbLoadRecords(\"db/dgsGlobals_%s_VME%02d.db\")\n'%(dgsDssd,vme)
		
		stcmd = stcmd.replace('%%LOADDATABASE',dbstr)
		
		
		#set where the stuff goes-- devel or develbuild
		
		if code_location!=None:		
			stcmd = stcmd.replace('%%CODELOCATION',code_location)
		
		
		stcmd = stcmd.replace('%%CDCOMMANDS','cdCommands_%s'%(dgsDssd))
		
		
		#now put in where the drivers are started
		drstr = ''
		
		log_brdnum=0
		brdID = 1
		
		for brd in boardlist:
			#drstr = drstr + 'asynDigitizerConfig(\"DIG%d\",%d,%d,2)\n'%(brd,log_brdnum,brd+2)
			drstr = drstr + 'asynDigitizerConfig(\"%s\",%d,%d,2)\n'%(brd,log_brdnum,brdID+2)
			log_brdnum=log_brdnum+1
			brdID = brdID+1
		
		
		
		drstr = drstr + "\nasynDebugConfig(\"DBG\",0)\n"
		stcmd = stcmd.replace('%%STARTDRIVERS',drstr)
		
		
		#start the inloop stuff
		
		seqstr=''
		
		
		log_brdnum=0
		brdID=1
		for brd in boardlist:
			PVAcqEna='DAQB%d_%d_CS_Ena'%(vme,brdID)
			PVMLE='VME%02d:%s:master_logic_enable'%(vme,brd)
			PVRun='VME%02d:%s:CV_Running'%(vme,brd)	
		
			seqstr = seqstr + 'seq &inLoop,\"bdno=%d, PVAcqEna=%s,PVMLE=%s, PVRun=%s\"\n'%(log_brdnum,PVAcqEna,PVMLE,PVRun)
			
			magic_number=user_package_start+(vme-1)*4+(brdID)
			
			seqstr = seqstr + 'dbpf \"VME%02d:%s:user_package_data\",\"%d\"\n\n'%(vme,brd,magic_number)
			seqstr = seqstr + 'dbpf \"DAQC%d_CV_OutputClearTime\",\"0.10\"\n\n'%(vme)
			log_brdnum=log_brdnum+1
			brdID=brdID+1
		
		seqstr = seqstr + "seq &TrigCon, \"CN=%d\"\n"%(vme)
		seqstr = seqstr + "seq &BuildSend, \"CN=%d,priority=5\"\n"%(vme)
		
		
		stcmd = stcmd.replace('%%STARTSEQUENCERS',seqstr)
		
		
		
		
		f.write(stcmd)
		f.close()
		


##############################################################################
#
# 
##############################################################################

def makeTrigStCmd(dgsDssd):

	global user_package_start
	global code_location
	
	cdcmd = cdcommands_template
	
	if code_location!=None:
		cdcmd = cdcmd.replace('%%CODELOCATION',code_location)
	
	fname = "cdCommands_%s"%(dgsDssd)
	f=open(fname,'w')
	f.write(cdcmd)
	f.close()
	
	stcmd = trig_st_template
	
	
	stcmd = stcmd.replace('%%SYSTEM',dgsDssd)
		
	dbstr='dbLoadDatabase("db/OnlineCon.db")\n'
	dbstr=dbstr + 'dbLoadDatabase("db/daqGlobal.db")'
	
	if dgsDssd=='CLO':
		stcmd = stcmd.replace('%%ONLINE',dbstr)
	else:
		stcmd = stcmd.replace('%%ONLINE','#oneline db on softioc')
		
	if code_location!=None:
		stcmd = stcmd.replace('%%CODELOCATION',code_location)
		stcmd = stcmd.replace('%%CDCOMMANDS','cdCommands_%s'%(dgsDssd))
	
	fname = "vme32.%s.cmd"%(dgsDssd)
	f=open(fname,'w')
	f.write(stcmd)
	f.close()
	


##############################################################################
#
# 
##############################################################################

def makeTrigStCmd5(dgsDssd):

	global user_package_start
	global code_location
	
	cdcmd = cdcommands_template
	
	if code_location!=None:
		cdcmd = cdcmd.replace('%%CODELOCATION',code_location)
	
	fname = "cdCommands_%s"%(dgsDssd)
	f=open(fname,'w')
	f.write(cdcmd)
	f.close()
	

	stcmd = trig_st_template5
	
	
	stcmd = stcmd.replace('%%SYSTEM',dgsDssd)
	
	
	dbstr='dbLoadDatabase("db/OnlineCon.db")\n'
	dbstr=dbstr + 'dbLoadDatabase("db/daqGlobal.db")'
	
	if dgsDssd=='CLO':
		stcmd = stcmd.replace('%%ONLINE',dbstr)
	else:
		stcmd = stcmd.replace('%%ONLINE','#oneline db on softioc')
	
	
	if code_location!=None:
		stcmd = stcmd.replace('%%CODELOCATION',code_location)
		stcmd = stcmd.replace('%%CDCOMMANDS','cdCommands_%s'%(dgsDssd))
	


	if dgsDssd=='DFMA':
		stcmd = stcmd.replace('dgsMTrigUser','dfmaMTrigUser')
		stcmd = stcmd.replace('dgsRTrigUser','dfmaRTrigUser')

	fname = "vme32.%s.cmd"%(dgsDssd)
	f=open(fname,'w')
	f.write(stcmd)
	f.close()
	

##############################################################################
#
# 
##############################################################################


cdcommands_template = """

startup = "%%CODELOCATION/gretTop/9-22/dgsIoc/iocBoot/iocArray"
putenv("ARCH=vxWorks-ppc604_long")
putenv("IOC=iocArray")
top = "%%CODELOCATION/gretTop/9-22/dgsIoc"
putenv("TOP=%%CODELOCATION/gretTop/9-22/dgsIoc")
topbin = "%%CODELOCATION/gretTop/9-22/dgsIoc/bin/vxWorks-ppc604_long"
sncseq = "%%CODELOCATION/supTop/31410/sncseq-2.0.12"
putenv("SNCSEQ=%%CODELOCATION/supTop/31410/sncseq-2.0.12")
sncseqbin = "%%CODELOCATION/supTop/31410/sncseq-2.0.12/bin/vxWorks-ppc604_long"
asyn = "%%CODELOCATION/synApps/asyn/asyn4-17"
putenv("ASYN=%%CODELOCATION/synApps/asyn/asyn4-17")
asynbin = "%%CODELOCATION/synApps/asyn/asyn4-17/bin/vxWorks-ppc604_long"
epics_base = "%%CODELOCATION/base/base-3.14.12.1"
putenv("EPICS_BASE=%%CODELOCATION/base/base-3.14.12.1")
epics_basebin = "%%CODELOCATION/base/base-3.14.12.1/bin/vxWorks-ppc604_long"
vxstats = "%%CODELOCATION/supTop/31410/vxStats"
putenv("VXSTATS=%%CODELOCATION/supTop/31410/vxStats")
vxstatsbin = "%%CODELOCATION/supTop/31410/vxStats/bin/vxWorks-ppc604_long"
gretvme = "%%CODELOCATION/gretTop/9-22/dgsIoc/../gretVME"
putenv("GRETVME=%%CODELOCATION/gretTop/9-22/dgsIoc/../gretVME")
gretvmebin = "%%CODELOCATION/gretTop/9-22/dgsIoc/../gretVME/bin/vxWorks-ppc604_long"
gretdig = "%%CODELOCATION/gretTop/9-22/dgsIoc/../dgsDrivers"
putenv("GRETDIG=%%CODELOCATION/gretTop/9-22/dgsIoc/../dgsDrivers")
gretdigbin = "%%CODELOCATION/gretTop/9-22/dgsIoc/../dgsDrivers/bin/vxWorks-ppc604_long"
trigger = "%%CODELOCATION/gretTop/9-22/dgsIoc/../dgsDrivers"
putenv("TRIGGER=%%CODELOCATION/gretTop/9-22/dgsIoc/../dgsDrivers")
triggerbin = "%%CODELOCATION/gretTop/9-22/dgsIoc/../dgsDrivers/bin/vxWorks-ppc604_long"
gretdata = "%%CODELOCATION/gretTop/9-22/dgsIoc/../dgsData"
putenv("GRETDATA=%%CODELOCATION/gretTop/9-22/dgsIoc/../dgsData")
gretdatabin = "%%CODELOCATION/gretTop/9-22/dgsIoc/../dgsData/bin/vxWorks-ppc604_long"
autosaverestore = "%%CODELOCATION/supTop/31410/asr4"
putenv("AUTOSAVERESTORE=%%CODELOCATION/supTop/31410/asr4")
autosaverestorebin = "%%CODELOCATION/supTop/31410/asr4/bin/vxWorks-ppc604_long"


"""






##############################################################################
#
# 
##############################################################################



dig_st_template = """
## vxWorks startup file

cd "%%CODELOCATION/gretTop/9-22/dgsIoc/iocBoot/iocArray/"


# array uses default EPICS ports 5065 and 5068
putenv("EPICS_CA_CONN_TMO = 40")
putenv("EPICS_CA_BEACON_PERIOD = 2")

< %%CDCOMMANDS
< ../nfsCommands

cd topbin

ld < gretDet.munch

cd top

dbLoadDatabase("dbd/gretDet.dbd",0,0)
gretDet_registerRecordDeviceDriver(pdbbase)

cd top

#mpc putenv("EPICS_TS_MIN_WEST = 480")
putenv("EPICS_TS_MIN_WEST = 360")


%%LOADDATABASE


# Do AutoSaveRestore

#set_requestfile_path(gretdig, "/db")
#set_requestfile_path(top, "/db")

#set_savefile_path("/global/devel/boot/autosave/", "vme1");

#set_pass1_restoreFile("vme1.sav")

#reboot_restoreDatedBU = 1


%%STARTDRIVERS


initMsDelay

cd startup

#save_restoreDebug = 3

asSetFilename("../../db/RunProtect.asf")


iocInit()

#devGDigSetRestFile "vme1.sav"

dumpFIFO = 0

#create_monitor_set("vme1.req",30,"")

setupFIFOReader()



## readout sequencers

%%STARTSEQUENCERS



"""




##############################################################################
#
# trig st cmd with 5 routers
##############################################################################



trig_st_template5="""

## GRETINA main trigger vxWorks startup file

cd "%%CODELOCATION/gretTop/9-22/dgsIoc/iocBoot/iocArray/"





# Array uses default epics ports 5064 and 5065
#putenv("EPICS_CA_SERVER_PORT = 5068")
#putenv("EPICS_CA_REPEATER_PORT = 5069")
putenv("EPICS_CA_CONN_TMO = 4")
putenv("EPICS_CA_BEACON_PERIOD = 2")


#< cdCommands

< %%CDCOMMANDS
< ../nfsCommands

cd topbin

ld < gretDet.munch

cd top

dbLoadDatabase("dbd/gretDet.dbd",0,0)
gretDet_registerRecordDeviceDriver(pdbbase)

cd top

putenv("EPICS_TS_MIN_WEST = 360")

## Load record instances


#deprecarted w/ autogen driver
#dbLoadRecords("db/dgs_vme32.db")

dbLoadRecords("db/dgsMTrigRegisters.template","P=VME32:,R=MTRG:,PORT=MTRG,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigRegisters.template","P=VME32:,R=RTR1:,PORT=RTR1,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigRegisters.template","P=VME32:,R=RTR2:,PORT=RTR2,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigRegisters.template","P=VME32:,R=RTR3:,PORT=RTR3,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigRegisters.template","P=VME32:,R=RTR4:,PORT=RTR4,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigRegisters.template","P=VME32:,R=RTR5:,PORT=RTR5,ADDR=0,TIMEOUT=1")


dbLoadRecords("db/dgsMTrigUser.template","P=VME32:,R=MTRG:,PORT=MTRG,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigUser.template","P=VME32:,R=RTR1:,PORT=RTR1,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigUser.template","P=VME32:,R=RTR2:,PORT=RTR2,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigUser.template","P=VME32:,R=RTR3:,PORT=RTR3,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigUser.template","P=VME32:,R=RTR4:,PORT=RTR4,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigUser.template","P=VME32:,R=RTR5:,PORT=RTR5,ADDR=0,TIMEOUT=1")


dbLoadRecords("db/gretVME.template","DB=125,DC=0")
dbLoadRecords("db/gretVME.template","DB=126,DC=1")
dbLoadRecords("db/gretVME.template","DB=127,DC=2")
dbLoadRecords("db/gretVME.template","DB=128,DC=3")
dbLoadRecords("db/gretVME.template","DB=129,DC=4")
dbLoadRecords("db/gretVME.template","DB=130,DC=5")

dbLoadRecords("db/asynDebug.template","P=VME32:,R=DBG:,PORT=DBG,ADDR=0,TIMEOUT=1")

dbLoadRecords("db/dgsGlobals_%%SYSTEM_GLBL.db")

%%ONLINE

#These pvs are for running a sender/sorter/fiforeader on trig crate
dbLoadRecords("db/daqCrate.template","DN=32")
dbLoadRecords("db/onMon.template","DN=32")
dbLoadRecords("db/tempTrigPvs.template","DB=32_1")
dbLoadRecords("db/daqBoard.template","  DB=32_1, DC=0 ")
#end sendersorter


# the Global.substitutions file should only be loaded once in the system
cd gretdig
dbLoadDatabase("db/gretGlobalBase.db")
dbLoadDatabase("db/gretGlobal.db")
dbLoadDatabase("db/gretEqual.db")


cd vxstats
                                                                                
dbLoadRecords("db/vxStats-template.db", "IOCNAME=iocVME32")

# Do AutoSaveRestore

set_requestfile_path(gretdig, "/db")
set_requestfile_path(top, "/db")

set_savefile_path("%%CODELOCATION/boot/autosave/", "vme32");

#set_pass1_restoreFile("vme32.sav")
set_pass1_restoreFile("vme32-tmp.sav")


reboot_restoreDatedBU = 1

#dgs master   (PortName,Card#,Slot#)
asynTrigMasterConfig1("MTRG",0,2)
#dgs routers
asynTrigRouterConfig1("RTR1",1,3)
asynTrigRouterConfig1("RTR2",2,4)
asynTrigRouterConfig1("RTR3",3,5)
asynTrigRouterConfig1("RTR4",4,6)
asynTrigRouterConfig1("RTR5",5,7)


asynDebugConfig("DBG",0)



cd startup

#save_restoreDebug = 3

asSetFilename("../../db/RunProtect.asf")


iocInit()

dumpFIFO = 0

# the following file does not save some skew PV's due to bug
create_monitor_set("vme32-tmp.req",30,"")


#seq &inLoopTrig,"bdno=1,PVAcqEna=DAQB32_1_CS_Ena,PVRun=TrigFifoRunning"
#seq &BuildSend, "CN=32,priority=5"
#dbpf "DAQB32_1_CS_Ena","Disable"



"""

##############################################################################
#
# 
##############################################################################



trig_st_template="""

## GRETINA main trigger vxWorks startup file

cd "%%CODELOCATION/gretTop/9-22/dgsIoc/iocBoot/iocArray/"

# Array uses default epics ports 5064 and 5065
#putenv("EPICS_CA_SERVER_PORT = 5068")
#putenv("EPICS_CA_REPEATER_PORT = 5069")
putenv("EPICS_CA_CONN_TMO = 4")
putenv("EPICS_CA_BEACON_PERIOD = 2")

#< cdCommands

< %%CDCOMMANDS
< ../nfsCommands

cd topbin

ld < gretDet.munch

cd top

dbLoadDatabase("dbd/gretDet.dbd",0,0)
gretDet_registerRecordDeviceDriver(pdbbase)

cd top

putenv("EPICS_TS_MIN_WEST = 360")

## Load record instances


#deprecarted w/ autogen driver
#dbLoadRecords("db/dgs_vme32.db")

dbLoadRecords("db/dgsMTrigRegisters.template","P=VME32:,R=MTRG:,PORT=MTRG,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigRegisters.template","P=VME32:,R=RTR1:,PORT=RTR1,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigRegisters.template","P=VME32:,R=RTR2:,PORT=RTR2,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigRegisters.template","P=VME32:,R=RTR3:,PORT=RTR3,ADDR=0,TIMEOUT=1")

dbLoadRecords("db/dgsMTrigUser.template","P=VME32:,R=MTRG:,PORT=MTRG,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigUser.template","P=VME32:,R=RTR1:,PORT=RTR1,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigUser.template","P=VME32:,R=RTR2:,PORT=RTR2,ADDR=0,TIMEOUT=1")
dbLoadRecords("db/dgsRTrigUser.template","P=VME32:,R=RTR3:,PORT=RTR3,ADDR=0,TIMEOUT=1")

dbLoadRecords("db/gretVME.template","DB=125,DC=0")
dbLoadRecords("db/gretVME.template","DB=126,DC=1")
dbLoadRecords("db/gretVME.template","DB=127,DC=2")
dbLoadRecords("db/gretVME.template","DB=128,DC=3")

#dbLoadRecords("db/link.template","T=0,PORT=MTRG")
#dbLoadRecords("db/link.template","T=1,PORT=RTR1")
#dbLoadRecords("db/link.template","T=2,PORT=RTR2")
#dbLoadRecords("db/link.template","T=3,PORT=RTR3")

dbLoadRecords("db/asynDebug.template","P=VME32:,R=DBG:,PORT=DBG,ADDR=0,TIMEOUT=1")

dbLoadRecords("db/dgsGlobals_%%SYSTEM_GLBL.db")

%%ONLINE

#These pvs are for running a sender/sorter/fiforeader on trig crate
dbLoadRecords("db/daqCrate.template","DN=32")
dbLoadRecords("db/onMon.template","DN=32")
dbLoadRecords("db/tempTrigPvs.template","DB=32_1")
dbLoadRecords("db/daqBoard.template","  DB=32_1, DC=0 ")
#end sendersorter

# the Global.substitutions file should only be loaded once in the system
cd gretdig
dbLoadDatabase("db/gretGlobalBase.db")
dbLoadDatabase("db/gretGlobal.db")
dbLoadDatabase("db/gretEqual.db")


##### Cannot get this to work #################################
#cd vxstats
#dbLoadRecords("db/vxStats-template.db", "IOCNAME=iocVME32")
###############################################################

# Do AutoSaveRestore 
# Looks at req-file in dgsIOC/db and stores in /global/devel/boot/autosave/vme32

set_requestfile_path(gretdig, "/db")
set_requestfile_path(top, "/db")

set_savefile_path("%%CODELOCATION/boot/autosave/", "vme32");

set_pass1_restoreFile("dgs_vme32.sav")

reboot_restoreDatedBU = 1

####### Now initialize Triggers #####################
#dgs master   (PortName,Card#,Slot#)
asynTrigMasterConfig1("MTRG",0,3)
#dgs routers
asynTrigRouterConfig1("RTR1",1,4)
asynTrigRouterConfig1("RTR2",2,5)
asynTrigRouterConfig1("RTR3",3,6)


asynDebugConfig("DBG",0)

cd startup

#save_restoreDebug = 3

asSetFilename("../../db/RunProtect.asf")

##################### Run the dreaded iocInit()
iocInit()

dumpFIFO = 0


# Limit set of PV's are saved - we may expand
create_monitor_set("dgs_vme32.req",30,"")

#seq &inLoopTrig,"bdno=1,PVAcqEna=DAQB32_1_CS_Ena,PVRun=TrigFifoRunning"
#seq &BuildSend, "CN=32,priority=5"
#dbpf "DAQB32_1_CS_Ena","Disable"

"""

##############################################################################
#
# 
##############################################################################

