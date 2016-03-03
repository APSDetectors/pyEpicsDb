




class screenMaker:


	def __init__(self):
		#widget widths, for several cols of widgets
		self.xw=[300,100,100]
		self.height=20
		#total step for next widget
		self.ystep=25
		#def width
		self.width = 20
		
		#space between widgets in x
		self.xstep=20
		
		#every thouhsan d rows we insert a space... set to 10 for an empty row every 10, for say 10 crates
		self.empty_row_every=1000
		
		#where all the widgets start on the screen
		self.ybase=100
		self.xbase=20
		
		#true to put title on screen
		self.is_title = True
		self.twidth=1000
		
	##############################################################################
	#pass in list of epicspv objects
	# makes screen - grops of 3 widgets, label, pv control, readback control
	#pass in epicsdb or list of epicspv().
	# pass in string mytitle fopr window title
	#ischans is True to include only channel pvs or False for only Board pvs
	# isonechan is True if we incl channel pvs and want to gen a single window with macros
	#yrows is how many rows of widgerts we make before starting a new col
	#some global pvs needed:
	#xw is self.width of 3 widgets as  list
	# self.height and self.width is def. self.width and hwight of widtets. 
	#self.ystep self.xstep is space between rows and widgets
	##############################################################################


	def dbToScreen1(self,epicsdb,mytitle,ischans,isonechan,yrows,scr):


		nwidgets=1000

		ylist=range(self.ybase,self.ybase+ yrows*self.ystep,self.ystep)

		xtabs=[]
		for xx in self.xw:
			xtabs.append(xx+self.xstep)	

		x=self.xbase
		xlist=[]

		for c in range(50):
			for t in xtabs:
				xlist.append(x)
				x=x+t

		yind=0
		xind=0

		y=ylist[yind]
		x=xlist[xind]


		if scr==None:
			scr=cssScreen()

		nw=0

		try:
			for pv in epicsdb:

				is_add_widget=False
				
				if (re.search(r'(LONGOUT)|(LONGIN)',pv.getPvName())==None):
 				    if (pv.isChanPv()==False and ischans==False) or  (ischans==True and pv.isChanPv()==True and isonechan==False) or (ischans==True and pv.isChanPv()==True and isonechan==True and re.search('.*0',pv.getPvName())!=None):

					if pv.isOutRec() and (re.search(r'.*LONGOUT',pv.getPvName())==None):
						#print 'WR W---------------------'
						#print pv.getPvName()
						#print pv.getRecType()
						#print "is chan %d"%(pv.isChanPv())

						label=cssWidget()
						label.setType('label')
						ctrl=cssWidget()
						is_add_widget=True


						if  (pv.getRecType()=='longout') or   pv.getRecType()=='ao':
							ctrl.setType('textinput')
							ctrl.setField('width','%d'%(self.xw[1]))
							if (pv.getExtra('row')['EPICS type']=='h'):
								ctrl.setField('format_type','3')


						elif pv.getRecType()=='bo':
							if (pv.getExtra('row')['EPICS type']=='bm'):
								ctrl.setType('actionbutton')
								ctrl.setField('width','%d'%(self.xw[1]))

							else:
								ctrl.setType('boolbutton')							
								ctrl.setField('width','%d'%(self.width))


						elif pv.getRecType()=='mbbo':
							ctrl.setType('combo')
							ctrl.setField('width','%d'%(self.xw[1]))

						else:
							ctrl.setType('textinput')
							ctrl.setField('width','%d'%(self.xw[1]))


						n=pv.getPvName()
						if isonechan:
							n=pv.makeChanName('$(CH)')


						#if momentary button add action...
						if ctrl.getType()=='actionbutton':
							ctrl.addPvAction(n,'1')
							ctrl.setField('text',pv.getExtra('row')['Human field name'])



						ctrl.setField('pv_name',n)
						label.setField('text',pv.getExtra('row')['Human field name'])
						label.setField('width','%d'%(self.xw[0]))


						label.setField('height','%d'%(self.height))
						ctrl.setField('height','%d'%(self.height))


						label.setField('x','%d'%(xlist[xind]))
						ctrl.setField('x','%d'%(xlist[xind+1]))

						label.setField('y','%d'%(ylist[yind]))
						ctrl.setField('y','%d'%(ylist[yind]))



						scr.addWidget(ctrl)
						scr.addWidget(label)


						#see if there is a pv in the list with same name with _RBV. this is the correspondingh readback
						#pt it next to this one.




						if (pv.getExtra('row')['Field Mode']=='RW'):
							#print "Add RBV"


							ctrl_rbv=cssWidget()
							ctrl_rbv.setType('textupdate')
							ctrl_rbv.setField('pv_name',n+'_RBV')
							ctrl_rbv.setField('width','%d'%(self.xw[2]))
							ctrl_rbv.setField('height','%d'%(self.height))

							ctrl_rbv.setField('x','%d'%(xlist[xind+2]))

							ctrl_rbv.setField('y','%d'%(ylist[yind]))

							if (pv.getExtra('row')['EPICS type']=='h'):
								ctrl_rbv.setField('format_type','3')

							scr.addWidget(ctrl_rbv)
						else:
							#we dont have RBV pv. but for little buttons, we 
							#should readback the value ...
							if ctrl.getType()=='boolbutton':
								ctrl_rbv=cssWidget()
								ctrl_rbv.setType('textupdate')
								ctrl_rbv.setField('pv_name',n)
								ctrl_rbv.setField('width','%d'%(self.xw[2]))
								ctrl_rbv.setField('height','%d'%(self.height))

								ctrl_rbv.setField('x','%d'%(xlist[xind+2]))

								ctrl_rbv.setField('y','%d'%(ylist[yind]))

								if (pv.getExtra('row')['EPICS type']=='h'):
									ctrl_rbv.setField('format_type','3')

								scr.addWidget(ctrl_rbv)






					elif (pv.getExtra('row')['Field Mode']=='R'):



						is_add_widget=True


						#print 'R---------------------'
						#print pv.getPvName()
						#print pv.getRecType()
						#print "is chan %d"%(pv.isChanPv())

						label=cssWidget()
						label.setType('label')
						ctrl=cssWidget()

						if  (pv.getRecType()=='longin' and re.search(r'.*LONGIN',pv.getPvName())==None) or  pv.getRecType()=='ai':
							ctrl.setType('textupdate')
							ctrl.setField('width','%d'%(self.xw[1]))
							if (pv.getExtra('row')['EPICS type']=='h'):
								ctrl.setField('format_type','3')

						elif  pv.getRecType()=='bi':			
							ctrl.setType('led')
							ctrl.setField('width','%d'%(self.width))
						elif  pv.getRecType()=='mbbi':			
							ctrl.setType('textupdate')
							ctrl.setField('width','%d'%(self.xw[1]))
						else:
							ctrl.setType('textupdate')
							ctrl.setField('width','%d'%(self.xw[1]))
							if (pv.getExtra('row')['EPICS type']=='h'):
								ctrl.setField('format_type','3')


						n=pv.getPvName()
						if isonechan:
							n=pv.makeChanName('$(CH)')


						ctrl.setField('pv_name',n)
						label.setField('text',pv.getExtra('row')['Human field name'])
						label.setField('width','%d'%(self.xw[0]))


						label.setField('height','%d'%(self.height))
						ctrl.setField('height','%d'%(self.height))


						label.setField('x','%d'%(xlist[xind]))
						ctrl.setField('x','%d'%(xlist[xind+1]))

						label.setField('y','%d'%(ylist[yind]))
						ctrl.setField('y','%d'%(ylist[yind]))



						scr.addWidget(ctrl)
						scr.addWidget(label)





					if is_add_widget:
						if yind<(len(ylist)-1):
							yind=yind+1	
						else:
							yind = 0
							xind=xind+len(xtabs)


						nw=nw+1
						if (nw>nwidgets):
							break



		except:
				print "Parsing error"
				
				
				print " "
				traceback.print_exc(file=sys.stdout)
				return pv
				
				
		print "Num widgt Groups  %d "%(nw)


		#add title
		if (self.is_title):
			title=cssWidget()
			title.setType('label')	
			title.setField('text',mytitle)


			title.setField('height','40')

			title.setField('width','1000')

			title.setField('x','20')

			title.setField('y','20')
			title.setFont('Sans','20')
			scr.addWidget(title)	

		return(scr)







	##############################################################################
	#pass in list of epicspv objects
	# nake screen with row heading, col heading
	#pass in epicsdb as list of epicspvs ordered in the list as col1, col2 etc.
	# num rows and cols is derived from len of headings lists
	#
	# pass in mytitle for window tiotle
	#yrows is how many rows of widgerts we make before starting a new col
	#use gliobals self.width,self.height for wig size, use self.xstep ysetp for space
	#use global  rhself.width, chself.width for row and col heading self.widthn
	#pass in a screen, so we can add stuff to a screen as opposed to starting a new one
	#put none for scr for make new screen
	##############################################################################



	def dbToScreen2(self,epicsdb,mytitle,rheading,cheading,scr):


		nwidgets=1000

		nrows = len(rheading)

		ncols=len(cheading)

		#start at 100, leave room for col headings, self.height+self.ystep
		ystart=self.ybase+self.ystep

		ylist=[]	
		y=ystart
		rowcount = 0	
		for r in range(nrows):
			ylist.append(y)
			y = y + self.ystep
			
			rowcount=rowcount+1
			
			if (rowcount==self.empty_row_every):
				y = y + self.ystep
				rowcount=0
				
			
		
		#ylist=range(ystart,ystart+ nrows*self.ystep,self.ystep)

		#start at 20, add room for row headings, rhself.width
		xstart=self.xbase+self.width+self.xstep

		xtabs=[]
		for xx in self.xw:
			xtabs.append(xx+self.xstep)	

		x=xstart
		xlist=[]

		
		for t in xtabs:
			xlist.append(x)
			x=x+t

		
		



		yind=0
		xind=0

		y=ylist[yind]
		x=xlist[xind]


		if (scr==None):
			scr=cssScreen()

		nw=0

		for pv in epicsdb:

			is_add_widget=False

			

			if pv.isOutRec() :
				#print 'WR W---------------------'
				#print pv.getPvName()
				#print pv.getRecType()
				#print "is chan %d"%(pv.isChanPv())


				ctrl=cssWidget()
				is_add_widget=True


				if  (pv.getRecType()=='longout') or   pv.getRecType()=='ao':
					ctrl.setType('textinput')
					ctrl.setField('width','%d'%(self.xw[xind]))


				elif pv.getRecType()=='bo':
					ctrl.setType('boolbutton')
					ctrl.setField('width','%d'%(self.xw[xind]))


				elif pv.getRecType()=='mbbo':
					ctrl.setType('combo')
					ctrl.setField('width','%d'%(self.xw[xind]))

				else:
					ctrl.setType('textinput')
					ctrl.setField('width','%d'%(self.xw[xind]))


				n=pv.getPvName()
				

				ctrl.setField('pv_name',n)
				ctrl.setField('height','%d'%(self.height))
				ctrl.setField('x','%d'%(xlist[xind]))
				ctrl.setField('y','%d'%(ylist[yind]))
				scr.addWidget(ctrl)

			else:



				is_add_widget=True


				#print 'R---------------------'
				#print pv.getPvName()
				#print pv.getRecType()
				#print "is chan %d"%(pv.isChanPv())

				ctrl=cssWidget()

				if  (pv.getRecType()=='longin' and re.search(r'.*LONGIN',pv.getPvName())==None) or  pv.getRecType()=='ai':
					ctrl.setType('textupdate')
					ctrl.setField('width','%d'%(self.xw[xind]))

				elif  pv.getRecType()=='bi':			
					ctrl.setType('led')
					ctrl.setField('width','%d'%(self.xw[xind]))
				elif  pv.getRecType()=='mbbi':			
					ctrl.setType('textupdate')
					ctrl.setField('width','%d'%(self.xw[xind]))
				else:
					ctrl.setType('textupdate')
					ctrl.setField('width','%d'%(self.xw[xind]))


				n=pv.getPvName()
				

				ctrl.setField('pv_name',n)
				ctrl.setField('height','%d'%(self.height))
				ctrl.setField('x','%d'%(xlist[xind]))
				ctrl.setField('y','%d'%(ylist[yind]))
				scr.addWidget(ctrl)





			if is_add_widget:
				if yind<(len(ylist)-1):
					yind=yind+1	
				else:
					yind = 0
					xind=xind+1


				nw=nw+1
				if (nw>nwidgets):
					break




		print "Num widgt Groups  %d "%(nw)


		#add col headings

		x=self.xbase+self.xstep+self.width
		y=self.ybase


		xind=0
		for h in cheading:
			x=xlist[xind]
			head=cssWidget()
			head.setType('label')	
			head.setField('text',h)
			head.setField('height','%d'%(self.height))
			head.setField('width','%d'%(self.xw[xind]))
			head.setField('x','%d'%(x))
			head.setField('y','%d'%(y))
			
			scr.addWidget(head)
			xind=xind+1	

		x=self.xbase
		y=self.ybase


		yind = 0

		for h in rheading:
			y=ylist[yind]
			head=cssWidget()
			head.setType('label')	
			head.setField('text',h)
			head.setField('height','%d'%(self.height))
			head.setField('width','%d'%(self.width))
			head.setField('x','%d'%(x))
			head.setField('y','%d'%(y))
			y=y+self.ystep
			scr.addWidget(head)
			yind=yind+1	

		#add title

		if (self.is_title):
			title=cssWidget()
			title.setType('label')	
			title.setField('text',mytitle)


			title.setField('height','40')

			title.setField('width','%d'%(self.twidth))

			title.setField('x','20')

			title.setField('y','20')
			title.setFont('Sans','20')
			scr.addWidget(title)	

		return(scr)



	def makeEvtRateScreen(self,fname):
		
		pv=makeSoftAo('EvtRate'," ","0")
		pvl=[]
		pvl.append(pv)
		
		vmecrates=['$(DN)']
		brds=['1', '3']
		chans=['0','1','2','3','4','5','6','7','8','9']
		
		gdb=makeGlobalEpicsDb(pvl,'EvtRate','Cry$(P)_$(R)_DV_Rate$(CH)',vmecrates,brds,chans)
		cheadings=['Brd1', 'Brd3']
		rheadings=chans

		self.twidth=300
		self.width=150
		
		self.xw=[75,75,75,75]
		scr = self.dbToScreen2(gdb,'Event Rates Crate $(DN)',rheadings,cheadings,None)
		scr.writeXML(fname)
		
		
		#Cry$(DN)_DV_Ratea1



	def makeEvtRateScreenDFMA(self,fname):
		
		pv=makeSoftAo('EvtRate'," ","0")
		pvl=[]
		pvl.append(pv)
		
		vmecrates=['$(DN)']
		brds=['1','2', '3','4']
		chans=['0','1','2','3','4','5','6','7','8','9']
		
		gdb=makeGlobalEpicsDb(pvl,'EvtRate','Cry$(P)_$(R)_DV_Rate$(CH)',vmecrates,brds,chans)
		cheadings=['Brd1','Brd2', 'Brd3','Brd4']
		rheadings=chans

		self.twidth=300
		self.width=150
		
		self.xw=[75,75,75,75]
		scr = self.dbToScreen2(gdb,'Event Rates Crate $(DN)',rheadings,cheadings,None)
		scr.writeXML(fname)
		
		
		#Cry$(DN)_DV_Ratea1


	def makeDigCountScreen(self,epicsdb,fname):


		#make global screen for all event counters in system
		#1st we make a pvlist for all the d window ovs, and replace macros with all boards, crates chanes

		#11 crates, 2 boards, 10 channels, 4 counters
		#have 4 crates down, 80 channes, then 4 crates down, then 3 crates down.




		#make dbase with 4 crates, make one col. 
		vmecrates=['VME01:','VME02:','VME03:','VME04:']
		brds=['DIG1:', 'DIG3:']
		chans=['0','1','2','3','4','5','6','7','8','9']

		dec=makeGlobalEpicsDb(epicsdb,'dropped_event_count0_RBV','$(P)$(R)dropped_event_count$(CH)_RBV',vmecrates,brds,chans)
		aec=makeGlobalEpicsDb(epicsdb,'accepted_event_count0_RBV','$(P)$(R)accepted_event_count$(CH)_RBV',vmecrates,brds,chans)
		ahc=makeGlobalEpicsDb(epicsdb,'ahit_count0_RBV','$(P)$(R)ahit_count$(CH)_RBV',vmecrates,brds,chans)
		dc=makeGlobalEpicsDb(epicsdb,'disc_count0_RBV','$(P)$(R)disc_count$(CH)_RBV',vmecrates,brds,chans)

		newdb = interleaveEpicsDb([dec,aec,ahc,dc],80)

		cheadings=['DrpEvCnt', 'AcEvCnt','AcHtCnt','DscCnt']

		rheadings=[]
		for v in vmecrates:
			for b in brds:
				for c in chans:
					rheadings.append('%s%s%s'%(v,b,c))



		self.width=200
		self.empty_row_every=10
		self.xw=[75,75,75,75]
		scr = self.dbToScreen2(newdb,'Digitizer Counters',rheadings,cheadings,None)


		#make dbase with 4 crates, make 2nd col, add to screen.
		vmecrates=['VME05:','VME06:','VME07:','VME08:']
		brds=['DIG1:', 'DIG3:']
		chans=['0','1','2','3','4','5','6','7','8','9']
		
		dec=makeGlobalEpicsDb(epicsdb,'dropped_event_count0_RBV','$(P)$(R)dropped_event_count$(CH)_RBV',vmecrates,brds,chans)
		aec=makeGlobalEpicsDb(epicsdb,'accepted_event_count0_RBV','$(P)$(R)accepted_event_count$(CH)_RBV',vmecrates,brds,chans)
		ahc=makeGlobalEpicsDb(epicsdb,'ahit_count0_RBV','$(P)$(R)ahit_count$(CH)_RBV',vmecrates,brds,chans)
		dc=makeGlobalEpicsDb(epicsdb,'disc_count0_RBV','$(P)$(R)disc_count$(CH)_RBV',vmecrates,brds,chans)

		newdb = interleaveEpicsDb([dec,aec,ahc,dc],len(dec))

		cheadings=['DrpEvCnt', 'AcEvCnt','AcHtCnt','DscCnt']

		rheadings=[]
		for v in vmecrates:
			for b in brds:
				for c in chans:
					rheadings.append('%s%s%s'%(v,b,c))



		
		self.empty_row_every=10
		self.xw=[75,75,75,75]
		self.xbase=800
		self.is_title = False
		
		scr = self.dbToScreen2(newdb,'Digitizer Counters',rheadings,cheadings,scr)


		#make dbase with 4 crates, make 2nd col, add to screen.
		vmecrates=['VME09:','VME10:','VME11:']
		brds=['DIG1:', 'DIG3:']
		chans=['0','1','2','3','4','5','6','7','8','9']
		
		dec=makeGlobalEpicsDb(epicsdb,'dropped_event_count0_RBV','$(P)$(R)dropped_event_count$(CH)_RBV',vmecrates,brds,chans)
		aec=makeGlobalEpicsDb(epicsdb,'accepted_event_count0_RBV','$(P)$(R)accepted_event_count$(CH)_RBV',vmecrates,brds,chans)
		ahc=makeGlobalEpicsDb(epicsdb,'ahit_count0_RBV','$(P)$(R)ahit_count$(CH)_RBV',vmecrates,brds,chans)
		dc=makeGlobalEpicsDb(epicsdb,'disc_count0_RBV','$(P)$(R)disc_count$(CH)_RBV',vmecrates,brds,chans)

		newdb = interleaveEpicsDb([dec,aec,ahc,dc],len(dec))

		cheadings=['DrpEvCnt', 'AcEvCnt','AcHtCnt','DscCnt']

		rheadings=[]
		for v in vmecrates:
			for b in brds:
				for c in chans:
					rheadings.append('%s%s%s'%(v,b,c))



		
		self.empty_row_every=10
		self.xw=[75,75,75,75]
		self.xbase=1600
		self.is_title = False
		scr = self.dbToScreen2(newdb,'Digitizer Counters',rheadings,cheadings,scr)

		self.xbase=20
		self.is_title = True



		scr.writeXML(fname)





	def makeDigCountScreenDFMA(self,epicsdb,fname):


		#make global screen for all event counters in system
		#1st we make a pvlist for all the d window ovs, and replace macros with all boards, crates chanes

		#11 crates, 2 boards, 10 channels, 4 counters
		#have 4 crates down, 80 channes, then 4 crates down, then 3 crates down.




		#make dbase with 4 crates, make one col. 
		vmecrates=['VME01:','VME02:','VME03:','VME04:']
		brds=['DIG1:', 'DIG2:', 'DIG3:', 'DIG4:']

		chans=['0','1','2','3','4','5','6','7','8','9']

		dec=makeGlobalEpicsDb(epicsdb,'dropped_event_count0_RBV','$(P)$(R)dropped_event_count$(CH)_RBV',vmecrates,brds,chans)
		aec=makeGlobalEpicsDb(epicsdb,'accepted_event_count0_RBV','$(P)$(R)accepted_event_count$(CH)_RBV',vmecrates,brds,chans)
		ahc=makeGlobalEpicsDb(epicsdb,'ahit_count0_RBV','$(P)$(R)ahit_count$(CH)_RBV',vmecrates,brds,chans)
		dc=makeGlobalEpicsDb(epicsdb,'disc_count0_RBV','$(P)$(R)disc_count$(CH)_RBV',vmecrates,brds,chans)

		newdb = interleaveEpicsDb([dec,aec,ahc,dc],len(dec))

		cheadings=['DrpEvCnt', 'AcEvCnt','AcHtCnt','DscCnt']

		rheadings=[]
		for v in vmecrates:
			for b in brds:
				for c in chans:
					rheadings.append('%s%s%s'%(v,b,c))



		self.width=200
		self.empty_row_every=10
		self.xw=[75,75,75,75]
		scr = self.dbToScreen2(newdb,'Digitizer Counters',rheadings,cheadings,None)


		#make dbase with 4 crates, make 2nd col, add to screen.
		vmecrates=['VME05:','VME06:','VME07:','VME08:']
		
		brds=['DIG1:', 'DIG2:', 'DIG3:', 'DIG4:']
		chans=['0','1','2','3','4','5','6','7','8','9']
		
		dec=makeGlobalEpicsDb(epicsdb,'dropped_event_count0_RBV','$(P)$(R)dropped_event_count$(CH)_RBV',vmecrates,brds,chans)
		aec=makeGlobalEpicsDb(epicsdb,'accepted_event_count0_RBV','$(P)$(R)accepted_event_count$(CH)_RBV',vmecrates,brds,chans)
		ahc=makeGlobalEpicsDb(epicsdb,'ahit_count0_RBV','$(P)$(R)ahit_count$(CH)_RBV',vmecrates,brds,chans)
		dc=makeGlobalEpicsDb(epicsdb,'disc_count0_RBV','$(P)$(R)disc_count$(CH)_RBV',vmecrates,brds,chans)

		newdb = interleaveEpicsDb([dec,aec,ahc,dc],len(dec))

		cheadings=['DrpEvCnt', 'AcEvCnt','AcHtCnt','DscCnt']

		rheadings=[]
		for v in vmecrates:
			for b in brds:
				for c in chans:
					rheadings.append('%s%s%s'%(v,b,c))



		
		self.empty_row_every=10
		self.xw=[75,75,75,75]
		self.xbase=800
		self.is_title = False
		
		scr = self.dbToScreen2(newdb,'Digitizer Counters',rheadings,cheadings,scr)


		#make dbase with 4 crates, make 2nd col, add to screen.
		vmecrates=['VME10:']
		brds=['DIG1:', 'DIG2:', 'DIG3:', 'DIG4:']
		chans=['0','1','2','3','4','5','6','7','8','9']
		
		dec=makeGlobalEpicsDb(epicsdb,'dropped_event_count0_RBV','$(P)$(R)dropped_event_count$(CH)_RBV',vmecrates,brds,chans)
		aec=makeGlobalEpicsDb(epicsdb,'accepted_event_count0_RBV','$(P)$(R)accepted_event_count$(CH)_RBV',vmecrates,brds,chans)
		ahc=makeGlobalEpicsDb(epicsdb,'ahit_count0_RBV','$(P)$(R)ahit_count$(CH)_RBV',vmecrates,brds,chans)
		dc=makeGlobalEpicsDb(epicsdb,'disc_count0_RBV','$(P)$(R)disc_count$(CH)_RBV',vmecrates,brds,chans)

		newdb = interleaveEpicsDb([dec,aec,ahc,dc],len(dec))

		cheadings=['DrpEvCnt', 'AcEvCnt','AcHtCnt','DscCnt']

		rheadings=[]
		for v in vmecrates:
			for b in brds:
				for c in chans:
					rheadings.append('%s%s%s'%(v,b,c))



		
		self.empty_row_every=10
		self.xw=[75,75,75,75]
		self.xbase=1600
		self.is_title = False
		scr = self.dbToScreen2(newdb,'Digitizer Counters',rheadings,cheadings,scr)

		self.xbase=20
		self.is_title = True



		scr.writeXML(fname)





	def makeGloEvtRateScreen(self,fname):

		#make dbase with 4 crates, make one col. 
		vmecrates=range(1,12)
		brds=[1,3]
		chans=range(10)

		epicsdb=[]
		for v in vmecrates:
			for b in brds:
				for c in chans:
					pv=makeSoftLongin('Cry%d_%d_DV_Rate%d'%(v,b,c),'%d:%d:%d'%(v,b,c))
					epicsdb.append(pv)

	
		self.xw=[75,75,1]
		scr = self.dbToScreen1(epicsdb,'Global Event Rates',True,False,50,None)

		scr.writeXML(fname)






	def makeGloEvtRateScreenDFMA(self,fname):

		#make dbase with 4 crates, make one col. 
		vmecrates=[1,2,3,4,5,6,7,8,10]
		brds=[1,2,3,4]
		chans=range(10)

		epicsdb=[]
		for v in vmecrates:
			for b in brds:
				for c in chans:
					pv=makeSoftLongin('Cry%d_%d_DV_Rate%d'%(v,b,c),'%d:%d:%d'%(v,b,c))
					epicsdb.append(pv)

	
		self.xw=[75,75,1]
		scr = self.dbToScreen1(epicsdb,'Global Event Rates',True,False,50,None)

		scr.writeXML(fname)



	def makeReplaceList1(self,pre,post):
		vme=range(1,12)
		brd=[1,2,3,4]
		dig=1
		
		fr=dict()
		
		for v in vme:
			for b in brd:
				fr['%s%d%s'%(pre,dig,post)]='%s%d_%d%s'%(pre,v,b,post)
				dig=dig+1
		
		return(fr)
	
	
	
	
	
	def makeReplaceList2(self):
		fr={ '$(ID1)':'$(CR)_1', '$(ID2)':'$(CR)_2', '$(ID3)':'$(CR)_3', '$(ID4)':'$(CR)_4'}
		return(fr)
		

	# a =gui.makeReplaceList3('CV_LiveTS')
	# scr = gui.substPvScreen('dssd_LiveTS.opi','textinput',a,None);
	#scr.writeXML('dssd_LiveTS.opi')
	def makeReplaceList3(self,post):
		vme=range(1,12)
		brd=[1,2,3,4]
		dig=1
		
		fr=dict()
		
		for v in vme:
			for b in brd:
				fr['Dig%d_%s'%(dig,post)]='VME%02d:DIG%d:%s'%(v,b,post)
				dig=dig+1
		
		return(fr)
	
	
	def substPvScreen(self,fname,ftype, findreplace,scr):
		
		if scr==None:
			scr=cssScreen()
	
		scr2=cssScreen()
		scr.readXML(fname)
		#fname = '/home/dgs/CSS-Workspaces/Default/CSS/DigEnable.opi'

		wl=scr.getWidgets()
		#for w in wl: w.getType()


		for w in wl:
			if w.getType()==ftype:
				pvname=w.getField('pv_name')
				
				for fr in findreplace:
					pvname=pvname.replace(fr,findreplace[fr])
				w.setField('pv_name',pvname)
			
			
			scr2.addWidget(w)
		return(scr2)
				

	# set all texinputs to decimal.
	# scr= gui.setScreenFormat('dssd_LiveTS.opi','textinput','0',None)
	# scr.writeXML('dssd_LiveTS.opi')
	def setScreenFormat(self,fname,ftype,format, scr):
		
		if scr==None:
			scr=cssScreen()
	
		scr2=cssScreen()
		scr.readXML(fname)
		#fname = '/home/dgs/CSS-Workspaces/Default/CSS/DigEnable.opi'

		wl=scr.getWidgets()
		#for w in wl: w.getType()


		for w in wl:
			if w.getType()==ftype:
				
				
				
				w.setField('format_type',format)
			
			
			scr2.addWidget(w)
		return(scr2)
		
		

	def makeVmeSummaryScreen(self):
		#generate screen for VME Summary

		daqdir='/global/develbuild/gretTop/9-22/dgsData/gretDataApp/Db/'
		drvdir='/global/develbuild/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/'

		#load the database from the DAQ system.
		daqcrate = readEpicsDb(daqdir+ 'daqCrate.template')
		#alter pv names

		vmecrates=['1','2','3','4','5','6','7','8','9','10','11']
		sendrate=makeGlobalEpicsDb(daqcrate,'SendRate','DAQC$(P)_CV_SendRate',vmecrates,None,None)
		buffavail=makeGlobalEpicsDb(daqcrate,'BuffersAvail','DAQC$(P)_CV_BuffersAvail',vmecrates,None,None)

		sendbuff=makeGlobalEpicsDb(daqcrate,'NumSendBuffers','DAQC$(P)_CV_NumSendBuffers',vmecrates,None,None)

		#DAQC$(DN)_CV_NotAAAErrors
		notaaa=makeGlobalEpicsDb(daqcrate,'NotAAAErrors','DAQC$(P)_CV_NotAAAErrors',vmecrates,None,None)

		onmon = readEpicsDb(daqdir+ 'onMon.template')
		rcvrIP=makeGlobalEpicsDb(onmon,'RcvrIP','OnMon$(P)_CS_RcvrIP',vmecrates,None,None)
		att=makeGlobalEpicsDb(onmon,'CV_AttStat','OnMon$(P)_CV_AttStat',vmecrates,None,None)
		count=makeGlobalEpicsDb(onmon,'CV_Count','OnMon$(P)_CV_Count',vmecrates,None,None)
		#PercentToSend
		percent=makeGlobalEpicsDb(onmon,'CS_PercentToSend','OnMon$(P)_CS_PercentToSend',vmecrates,None,None)

		#put pvs in interleaved order so we can have cols of different tuype of pvs
		#order of pvs in cols is below in the list. we have 11 crates, so interleave by 11
		newdb = interleaveEpicsDb([sendrate,buffavail,sendbuff,notaaa,percent,rcvrIP,att,  count  ],11)

		self.width=100
		self.xw=[100,100,100,100,100,200,100,100]
		scr = self.dbToScreen2(newdb,'Sender Summary',vmecrates,['TCP', 'Buffs', 'SndBuffs','AAA Err','MonPercent','Sendto', 'Stat', 'UDP'],None)
		scr.writeXML('vmesummary.opi')
		return(scr)
				
		


	def makeDAQDbgScreen(self):
		#generate screen for VME Summary

		daqdir='/global/develbuild/gretTop/9-22/dgsData/gretDataApp/Db/'
		drvdir='/global/develbuild/gretTop/9-22/dgsDrivers/dgsDriverApp/Db/'

		#load the database from the DAQ system.
		daqcrate = readEpicsDb(daqdir+ 'daqCrate.template')
		#alter pv names

		vmecrates=['1','2','3','4','5','6','7','8','9','10','11']
		
		
		fftr=makeGlobalEpicsDb(daqcrate,'CV_ReadFIFOTrace','DAQC$(P)_CV_ReadFIFOTrace',vmecrates,None,None)
		cstr=makeGlobalEpicsDb(daqcrate,'CV_CeSortTrace','DAQC$(P)_CV_CeSortTrace',vmecrates,None,None)
		sdtr=makeGlobalEpicsDb(daqcrate,'CV_SenderTrace','DAQC$(P)_CV_SenderTrace',vmecrates,None,None)
		octm=makeGlobalEpicsDb(daqcrate,'CV_OutputClearTime','DAQC$(P)_CV_OutputClearTime',vmecrates,None,None)
		

		#put pvs in interleaved order so we can have cols of different tuype of pvs
		#order of pvs in cols is below in the list. we have 11 crates, so interleave by 11
		newdb = interleaveEpicsDb([fftr,cstr,sdtr,octm  ],11)

		self.width=100
		self.xw=[100,100,100,100]
		scr = self.dbToScreen2(newdb,'DAQ Debug',vmecrates,['FIFO Tr', 'Sort Tr', 'Send Tr','OutTime'],None)
		scr.writeXML('daqdebug.opi')
		return(scr)
				
		

#####################################################################
# pass in a cssScreen
# list through all widgets, for monitors like leds textmonitor,bytemonotr
#  add _RBV if needed to the pv name. return a new cssScreen
# skips pvs with a . like pv.DESC 
#######################################################################
	def screenAddRBV(self,scr):
		wlist=scr.getWidgets()
		newscr=cssScreen()
		
		for w in wlist:
			if w.getType()=='led' or w.getType()=='bytemonitor' or w.getType=='textupdate':
				if re.search('(_RBV)|(\.)',w.getField('pv_name')) == None:
					pv=w.getField('pv_name')+'_RBV'
					w.setField('pv_name',pv)
					
			newscr.addWidget(w)
		return(newscr)
		
		
