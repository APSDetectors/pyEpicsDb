#########################################################################################################
#
#
#
#########################################################################################################



def analAddresses():

	ssname = 'MTRM.csv'

	ss=spreadsheet()
	ss.readTabText(ssname);
	mycols = [1,2,3,4]
	addr_rows=ss.getColsD(mycols)

	mycols = range(5,21)
	pv_rows=ss.getColsD(mycols)

	cfile=[]

	cfile.append('asynTrigCommonDriver.cpp')
	cfile.append('asynTrigMasterDriver.cpp')
	cfile.append('asynTrigRouterDriver.cpp')

	addr2reg=dict()


	#create map from address to regname in the current trig driver
	for ff in cfile:
		print 'Searching file %s '%(ff)
		for r in addr_rows:
			ss_addr=r['Address']
			ss_reg=r['Register Name']

			c_reg=findRegAddress(ff,ss_addr)
			#find address in the c code
			#print 'For ss addr %s found driver reg %s '%(ss_addr,c_reg)

			if c_reg!=0:
				if ss_addr not in addr2reg:
					addr2reg[ss_addr]=c_reg
				else:
					print "WARNING-in asyn cpp files doubly defined addr %s"%(ss_addr)	





	#create map from address to regname in ss
	#also make map from regname to addr, in ss
	addr2ssreg=dict()
	ssreg2addr=dict()
	for r in addr_rows:
		ss_addr=r['Address']
		ss_reg=r['Register Name']

		#see if there are white space in the ss regname
		if ' ' in ss_reg:
			print 'WARNING- Whitespace in ss regname %s'%(ss_reg)

		if ss_addr not in addr2ssreg:
			addr2ssreg[ss_addr]=ss_reg
		else:
			print 'ERROR- duplicate address in ss %s'%(ss_addr)
	
		if ss_reg not in ssreg2addr:
			ssreg2addr[ss_reg]=ss_addr
		else:
			print 'ERROR- duplicate regname in ss %s'%(ss_reg)	




	#create a map from driver regnames to newer ss regnames
	drReg2ssReg=dict()
	ssReg2drReg=dict()
	for k in addr2reg.keys():
		drreg = addr2reg[k];
		ssreg = addr2ssreg[k];
		drReg2ssReg[drreg]=ssreg
		ssReg2drReg[ssreg]=drreg




	#create a list of changed reg names, where ss reg name is different from current driver reg name
	regnames_changed=dict()
	regnames_unchanged=dict()

	for k in drReg2ssReg.keys():
	
		if drReg2ssReg[k] != k:
			regnames_changed[k] = drReg2ssReg[k]
		else:
			regnames_unchanged[k]=drReg2ssReg[k]







	#create list of addresses that the ss has, but current driver lacks

	addr_missing=[]

	for r in addr_rows:
		ss_addr=r['Address']
		if ss_addr not in addr2reg:
			addr_missing.append(ss_addr)



	#report on teh ss and driver

	print "\n\n--List of changed reg names  driver--> ss  --"

	for r in regnames_changed.keys():
		print "%s --> %s"%(r,regnames_changed[r])



#report on teh ss and driver

	print "\n\n--List of UN-changed reg names  driver--> ss  --"

	for r in regnames_unchanged.keys():
		print "%s"%(regnames_unchanged[r])





	print "\n\n---Missing or New registers----"
	for a in addr_missing:
		print "%s  ,  %s "%(a,addr2ssreg[a])

		


	print "\n\nnum regnames that change %d"%(len(regnames_changed))
	print "num regnames that stay the same %d"%(len(drReg2ssReg)-len(regnames_changed))
	print "num addresses not impl in driver %d"%(len(addr_missing))




#########################################################################################################
#
#
#
#########################################################################################################

def combineHepDrvSS():

	ssname = 'MTRM.csv'

	hepss=spreadsheet()

	#load the hep trig ss
	hepss.readTabText(ssname)

	#generate a ss based on existing trig driver/dbs
	drvss = makeSsFromDriver()


	#get dict of ss for reg/addresses

	hep_reg=hepss.getRegColsD()
	#rows for user pvs from hep ss
	hep_pvs=hepss.getUserColsD()


	#get dict of user pvs from drv
	drv_pvs=drvss.getUserColsD()


	#generate map from addr to regnames in hep ss


	# we want to make new ss that will take address/regs from hep, and import pv names etc from driver.

	#make blank ss.
	newss=spreadsheet()

	#step through the reg rows in hepss, and add rows to new ss, for pvs and regs

	for regrow in hep_reg:

		print regrow['Address']
		addr = regrow['Address']

		#step thru all the rows in the driver ss, to find rows that have target address
		for r in drv_pvs:
			if r['Address']==addr:
				#found a pv row that has correct addr.
				#update the regname 
				r['Register Name']=regrow['Register Name']
				#add row to new ss
				newss.addUserRowD(r)



	
		#step thru all the rows in the hep ss, to find rows that have target address
		for r in hep_pvs:
			if r['Address']==addr:
			
				#add row to new ss
				newss.addUserRowD(r)



		newss.addRegRowD(regrow)


	return(newss)







#########################################################################################################
#
#
#
#########################################################################################################




def makeAddrRegMaps(addr_rows):
	#create map from address to regname in ss
	#also make map from regname to addr, in ss
	addr2ssreg=dict()
	ssreg2addr=dict()
	for r in addr_rows:
		ss_addr=r['Address']
		ss_reg=r['Register Name']

		#see if there are white space in the ss regname
		if ' ' in ss_reg:
			print 'WARNING- Whitespace in ss regname %s'%(ss_reg)

		if ss_addr not in addr2ssreg:
			addr2ssreg[ss_addr]=ss_reg
		else:
			print 'ERROR- duplicate address in ss %s'%(ss_addr)
	
		if ss_reg not in ssreg2addr:
			ssreg2addr[ss_reg]=ss_addr
		else:
			print 'ERROR- duplicate regname in ss %s'%(ss_reg)	

	return((addr2ssreg,ssreg2addr))


#########################################################################################################
#
#
#
#########################################################################################################



def analUserDbs1():



	ssname = 'MTRM.csv'

	ss=spreadsheet()
	ss.readTabText(ssname);
	mycols = [1,2,3,4]
	addr_rows=ss.getColsD(mycols)

	mycols = range(5,21)
	pv_rows=ss.getColsD(mycols)

	#create map from address to regname in ss
	#also make map from regname to addr, in ss
	addr2ssreg=dict()
	ssreg2addr=dict()
	for r in addr_rows:
		ss_addr=r['Address']
		ss_reg=r['Register Name']

		#see if there are white space in the ss regname
		if ' ' in ss_reg:
			print 'WARNING- Whitespace in addr ss regname %s'%(ss_reg)

		if ss_addr not in addr2ssreg:
			addr2ssreg[ss_addr]=ss_reg
		else:
			print 'ERROR- duplicate address in addr ss %s'%(ss_addr)

		if ss_reg not in ssreg2addr:
			ssreg2addr[ss_reg]=ss_addr
		else:
			print 'ERROR- duplicate regname in addr ss %s'%(ss_reg)	



	#create map from address to regname in ss- pv area
	#also make map from regname to addr, in ss - pv area
	pvaddr2ssreg=dict()
	pvssreg2addr=dict()
	for r in pv_rows:
		ss_addr=r['Address']
		ss_reg=r['Register Name']

	
		#see if there are white space in the ss regname
		if ' ' in ss_reg:
			print 'WARNING- Whitespace in ss pv regname %s'%(ss_reg)

		if len(ss_reg)>0:	
			if ss_addr not in pvaddr2ssreg:
				pvaddr2ssreg[ss_addr]=ss_reg
			elif pvaddr2ssreg[ss_addr]!=ss_reg:
				print "ERROR: two pv addresses have same registername %s %s"%(ss_reg, ss_addr)
	
			if ss_reg not in pvssreg2addr:
				pvssreg2addr[ss_reg]=ss_addr
			elif pvssreg2addr[ss_reg] != ss_addr:
				print "ERROR: two pv regnames have same addr %s %s"%(ss_reg, ss_addr)
	

	#list regs in the addrss that have no pvs defined, or not in the pvss

	regs_without_pvs=[]

	for r in addr_rows:
		ss_addr=r['Address']
		ss_reg=r['Register Name']

		if ss_reg not in pvssreg2addr:
			if ss_reg not in regs_without_pvs:
				regs_without_pvs.append(ss_reg);



	#make sure you can find the regname in pv area in the addr area of ss
	pvregs_no_addrreg=[]

	for r in pv_rows:
		ss_addr=r['Address']
		ss_reg=r['Register Name']

		if (len(ss_reg)>0) & (ss_reg not in ssreg2addr):
			if ss_reg not in pvregs_no_addrreg:
				pvregs_no_addrreg.append(ss_reg)
				print "ERROR: pvreg not in addr reglist %s"%(ss_reg)







	#read in epics dbs
	trigdb = readEpicsDb('Trigger.template')
	mastdb = readEpicsDb('Master.template')
	routdb = readEpicsDb('Router.template')


#########################################################################################################
#
#
#
#########################################################################################################



def makeSsFromDriver():

	ss=spreadsheet()

	trigdb = readEpicsDb('Trigger.template')
	mastdb = readEpicsDb('Master.template')
	routdb = readEpicsDb('Router.template')
	linkdb = readEpicsDb('link.template')
	sumdb=trigdb+mastdb+routdb+linkdb;



	cfile=[]

	cfile.append('asynTrigCommonDriver.cpp')
	cfile.append('asynTrigMasterDriver.cpp')
	cfile.append('asynTrigRouterDriver.cpp')

	reg2addr=dict()
	addr2reg=dict()
	for f in cfile:
	
		(r2a,a2r)=getRegAddressList(f)
		reg2addr=dict(reg2addr.items() + r2a.items())
		addr2reg=dict(addr2reg.items() + a2r.items())

	print "---------------------"


	ss=spreadsheet()

	for regname in reg2addr.keys():
		pvs =findAsyn(sumdb,'param',regname)
		for p in pvs:
			r=ss.createUserRowD()
			r['Register Name']=regname;
			r['Address']=reg2addr[regname]
			r['Software field name']=p.getPvName()
			if p.isOutRec():	
				r['Field Mode']='W'
			else:
				r['Field Mode']='R'

		
			r['Bit']=getMaskBits(p.getAsynSpec()['mask'])
			r['EPICS type']=pvType2ssType(p.getRecType())
			r['Field Description for database']=p.getField('DESC')
			r['Human field name']=p.getPvName()
			r['Bitfield Sub-Descriptor']=pvBitFields2ssSubDesc(p)

			#r['Address']=reg2addr[regname]
			ss.addUserRowD(r)
		

		r=ss.createRegRowD()
		r['Register Name']=regname;
		r['Register Mode']='RW'
		r['Address']=reg2addr[regname]
		ss.addRegRowD(r)
	

	#ss.writeTabText(filename)


	return(ss)









#########################################################################################################
#
# alter spreaadsheet- has to be run once, then we forget about this
# 1st we alter ss pv names and fix bugs, alter epics databases reg name, then we genSystem as normal
#new epics db is then generated and old trigger.template etc goes away. new dbs have mostly same pvnames
# how do we analyse the bitspec of user pvs? need to analyse it as above 1st to see what to do.
#########################################################################################################

# list of regs to remove from databases

#remove pvs no longer needed

# list of regs to update names in the databases

#update databases- reg names in asyn spec

#list of all addresses that driver already has..list of regs in ss to update the pv names in ss

#go through ss user pvs- find reg/bitspec in epics, update ss pv name from epics db

#done... now we can generate the system w/ gen System



