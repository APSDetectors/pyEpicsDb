# Class to build edm windows 

class edmMaker:


	def __init__(self):
		#widget widths, for several cols of widgets
		self.xw=[160,85,85]
		self.height=20
		#total step for next widget
		self.ystep=30
		#def width
		self.width = 20
		
		#space between widgets in x
		self.xstep=5
		
		#every thouhsan d rows we insert a space... set to 10 for an empty row every 10, for say 10 crates
		self.empty_row_every=1000
		
		#where all the widgets start on the screen
		self.ybase=30
		self.xbase=0
		
		#true to put title on screen
		self.is_title = True
		self.twidth=1000
		
	##############################################################################
	# pass in list of epicspv objects
	# makes screen - grops of 3 widgets, label, control, readback control
	# if PV is R only a text widget is inserted in place of control widget
	# xw is self.width of 3 widgets as  list
	# self.height and self.width is def. self.width and hwight of widtets. 
	# self.ystep self.xstep is space between rows and widgets
	##############################################################################


	def dbToRegister(self,epicsdb,mytitle,yrows,scr):

		nwidgets=1000

		ylist=range(self.ybase,self.ybase+ yrows*self.ystep,self.ystep)
		ystep = 30

		xtabs=[]
		for xx in self.xw:
			xtabs.append(xx +self.xstep)	

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

        # This is so header is in scr[0]. Replace with w and h at end.
		if scr==None:
			scr=[]
			scr.append(edm_Register_Header)

		title = edm_Register_Title
		title = title.replace('%%TITLE',mytitle)
		scr.append(title)
        
		nw=0

		
#  generate widgets by looping through PV's

		try:

			# first loop through RW PVs
			x = self.xbase
			y = self.ybase
			nrows = 1
			for pv in epicsdb:

				is_add_widget=False

				if (pv.getExtra('row')['Field Mode']=='RW'):
					#print 'WR W---------------------'
					#print pv.getPvName()
					#print pv.getRecType()
					print "is chan %d"%(pv.isChanPv())
					pvbase = pv.getPvName().lstrip('$(P)$(R)reg').lstrip('_')
					addr = pv.getExtra('row')['Address']
					#print addr

					if (pv.getRecType()=='longout'):
						# make label widget
						wlabel = edm_Register_Label
						xl = str(x)
						yl = str(y)
						wlabel = wlabel.replace("%%XLABEL",xl)
						wlabel = wlabel.replace("%%YLABEL",yl)
						wlabel = wlabel.replace("%%WLABEL",str(self.xw[0]))
						wlabel = wlabel.replace("%%REGNAME",pvbase)
						wlabel = wlabel.replace("%%REGADDR",addr) 
						scr.append(wlabel)
						# make control widget
						xc = x + xtabs[0]
						yc = y + 3
						wcntrl = edm_Register_Control
						wcntrl = wcntrl.replace("%%XCNTRL",str(xc))
						wcntrl = wcntrl.replace("%%YCNTRL",str(yc))
						wcntrl = wcntrl.replace("%%WCNTRL",str(self.xw[1]))
						wcntrl = wcntrl.replace("%%PVCNTRL",pv.getPvName())
						scr.append(wcntrl)
						# make RBV widget
						xrbv = x + xtabs[1]+xtabs[0]
						yrbv = y + 3
						wRBV = edm_Register_RBV
						wRBV = wRBV.replace("%%XRBV",str(xrbv))
						wRBV = wRBV.replace("%%YRBV",str(yrbv))
						wRBV = wRBV.replace("%%WRBV",str(self.xw[2]))
						wRBV = wRBV.replace("%%PVRBV",pv.getPvName()+"_RBV")
						scr.append(wRBV)

						print nrows,x,y
						nrows = nrows + 1
						y = y + ystep
						if (nrows > yrows):
							nrows = 1
							y = self.ybase
							x = x + xtabs[2]+xtabs[1]+xtabs[0]
		except:
			print "Parsing error"
								
			print " "
			traceback.print_exc(file=sys.stdout)
			return pv

		try:

			# first loop through RW PVs
			x = x + xtabs[2]+xtabs[1]+xtabs[0]
			y = self.ybase
			nrows = 1
					
			# secondly loop through R PVs
			for pv in epicsdb:

				if (pv.getExtra('row')['Field Mode']=='R'):
					#print 'R---------------------'
					#print pv.getPvName()
					#print pv.getRecType()
					pvbase = pv.getPvName().lstrip('$(P)$(R)reg').lstrip('_')
					pvbase = pvbase.rstrip('_RBV')
					#print "is chan %d"%(pv.isChanPv())
					addr = pv.getExtra('row')['Address']
					#print addr
					
					if (pv.getRecType()=='longin'):
						# make label widget
						wlabel = edm_Register_Label
						xl = str(x)
						yl = str(y)
						wlabel = wlabel.replace("%%XLABEL",xl)
						wlabel = wlabel.replace("%%YLABEL",yl)
						wlabel = wlabel.replace("%%WLABEL",str(self.xw[0]))
						wlabel = wlabel.replace("%%REGNAME",pvbase)
						wlabel = wlabel.replace("%%REGADDR",addr) 
						scr.append(wlabel)
						# make RBV widget
						xrbv = x + xtabs[0]
						yrbv = y + 3
						wRBV = edm_Register_RBV
						wRBV = wRBV.replace("%%XRBV",str(xrbv))
						wRBV = wRBV.replace("%%YRBV",str(yrbv))
						wRBV = wRBV.replace("%%WRBV",str(self.xw[2]))
						wRBV = wRBV.replace("%%PVRBV",pv.getPvName())
						scr.append(wRBV)

						print nrows,x,y
						nrows = nrows + 1
						y = y + ystep
						if (nrows > yrows):
							nrows = 1
							y = self.ybase
							x = x + xtabs[1]+xtabs[0]					

		except:
			print "Parsing error"
								
			print " "
			traceback.print_exc(file=sys.stdout)
			return pv
				

		# Calculate width and length of display area
		ylen = str( yrows*self.ystep + self.ybase )
		scr[0] = scr[0].replace("%%HHEAD",ylen)
		if (nrows == 1) :
			xlen = x
		else:
			xlen = x + xtabs[1]+xtabs[0]
		scr[0] = scr[0].replace("%%WHEAD",str(xlen))
		
		# Find x-Position of Title and Width
		scr[1] = scr[1].replace("%%WTITLE",str(xlen))

		print nrows,x,y,xlen,ylen

		return(scr)

	###########################################################
	#
	# Version to generate register screens for digitizers
	#
	###########################################################
	
	def dbToRegister2(self,epicsdb,mytitle,yrows,mode,ofile):

		nwidgets=1000
		edlfile = ofile

		ylist=range(self.ybase,self.ybase+ yrows*self.ystep,self.ystep)
		ystep = 30

		xtabs=[]
		for xx in self.xw:
			xtabs.append(xx +self.xstep)	

        # This is so header is in scr[0]. Replace with w and h at end.

        
		nw=0
		nrmax = 0
		
		# Determine whether to extract channel info or not
		if mode == 'XXX':
			loop = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
		else :
			loop = [0]
		validtype = ['RW','R']
#  generate widgets by looping through PV's

		try:
			
			for ch in loop:
				nrmax = 0
				x = self.xbase
				y = self.ybase
				nrows = 1
				
				# now create scr list and write header, title and chanbutton
				scr=[]
				scr.append(edm_Register_Header)

				title = edm_Register_Title
				title = title.replace('%%TITLE',mytitle)
				scr.append(title)
        
                # Now add Channel Button only for registers for digitizer
				if (mode=='Dig'):
					scr.append(edm_Register_ChanButton)

				for a in validtype:
					for pv in epicsdb:
	
						add_widget = False
						if (mode == 'Trig'):
							add_widget=True
						if (mode == 'Dig' and not pv.isChanPv()): 
							add_widget=True
						if (mode == 'Chan' and pv.isChanPv()):
							add_widget=True	
				
						if (pv.getExtra('row')['Field Mode']==a and add_widget):
							#print 'WR W---------------------'
							#print pv.getPvName()
							#print pv.getRecType()
							#print "is chan %d"%(pv.isChanPv())
							pvbase = pv.getPvName().lstrip('$(P)$(R)reg').lstrip('_')
							addr = pv.getExtra('row')['Address']
							processPV = False
							if (a=='RW' and pv.getRecType()=='longout'):
								processPV = True
							if (a=='R' and pv.getRecType()=='longin'):
								processPV = True

							if (processPV):
								print pv.getPvName()
								# make label widget
								wlabel = edm_Register_Label
								xl = str(x)
								yl = str(y)
								wlabel = wlabel.replace("%%XLABEL",xl)
								wlabel = wlabel.replace("%%YLABEL",yl)
								wlabel = wlabel.replace("%%WLABEL",str(self.xw[0]))
								wlabel = wlabel.replace("%%REGNAME",pvbase)
								wlabel = wlabel.replace("%%REGADDR",addr) 
								scr.append(wlabel)
								if a == 'RW':
									# make control widget
									xc = x + xtabs[0]
									yc = y + 3
									wcntrl = edm_Register_Control
									wcntrl = wcntrl.replace("%%XCNTRL",str(xc))
									wcntrl = wcntrl.replace("%%YCNTRL",str(yc))
									wcntrl = wcntrl.replace("%%WCNTRL",str(self.xw[1]))
									wcntrl = wcntrl.replace("%%PVCNTRL",pv.getPvName())
									scr.append(wcntrl)
								# make RBV widget
								xrbv = x + xtabs[1]+xtabs[0]
								if a == 'R':
									xrbv = x + xtabs[0]
								yrbv = y + 3
								wRBV = edm_Register_RBV
								wRBV = wRBV.replace("%%XRBV",str(xrbv))
								wRBV = wRBV.replace("%%YRBV",str(yrbv))
								wRBV = wRBV.replace("%%WRBV",str(self.xw[2]))
								if a=='RW':
									wRBV = wRBV.replace("%%PVRBV",pv.getPvName()+"_RBV")
								if a=='R':
									wRBV = wRBV.replace("%%PVRBV",pv.getPvName())
								scr.append(wRBV)

								print nrows,yrows,x,y
								if nrows > nrmax :
									nrmax = nrows
								nrows = nrows + 1
								y = y + ystep
								if (nrows > yrows):
									nrows = 1
									y = self.ybase
									x = x + xtabs[2]+xtabs[0]
									if a=='RW':
										x = x + xtabs[1]
					if (nrows>1):
						x = x + xtabs[2]+xtabs[1]+xtabs[0]
						y = self.ybase
						nrows = 1
					#end of valid type loop
			
				# now lets calculate some final things and write out file
				ylen = str( nrmax*self.ystep + self.ybase )
				scr[0] = scr[0].replace("%%HHEAD",ylen)
				if (nrows == 1) :
					xlen = x
				else:
					xlen = x + xtabs[1]+xtabs[0]
				scr[0] = scr[0].replace("%%WHEAD",str(xlen))
		
				# Find x-Position of Title and Width
				scr[1] = scr[1].replace("%%WTITLE",str(xlen))

				# write list to file
				fileobj=open(edlfile,'w')
	
				for item in scr:
					fileobj.write(item)
			
				fileobj.close()

				print nrows,x,y,xlen,ylen
				# end of ch loop
				
		except:
			print "Parsing error"
								
			print " "
			traceback.print_exc(file=sys.stdout)
			return pv

		return(scr)

##############################################################################
# Write list out to file -- list contains the EDM commands
##############################################################################	
	def writescr(scr,filename):

	
		fileobj=open(filename,'w')
	
		for item in scr:
			fileobj.write(item)
			
		fileobj.close()
		
##############################################################################
# Header for Register edl file
##############################################################################
edm_Register_Header="""
4 0 1
beginScreenProperties
major 4
minor 0
release 1
x 17
y 85
w %%WHEAD
h %%HHEAD
font "courier-medium-r-10.0"
ctlFont "courier-medium-r-10.0"
btnFont "courier-medium-r-10.0"
fgColor index 14
bgColor index 55
textColor index 14
ctlFgColor1 index 14
ctlFgColor2 index 0
ctlBgColor1 index 0
ctlBgColor2 index 14
topShadowColor index 0
botShadowColor index 14
endScreenProperties
"""
##############################################################################
# Title Widget for Register edl file
##############################################################################
edm_Register_Title="""
# (Static Text) Title Widget
object activeXTextClass
beginObjectProperties
major 4
minor 1
release 0
x 0
y 1
w %%WTITLE
h 30
font "helvetica-bold-r-14.0"
fontAlign "center"
fgColor index 25
bgColor index 0
useDisplayBg
value {
  " %%TITLE "
}
#autoSize
endObjectProperties
"""
##############################################################################
# Label Widget for Register
##############################################################################
edm_Register_Label="""
# (Static Text) Label/Register Widget
object activeXTextClass
beginObjectProperties
major 4
minor 1
release 0
x %%XLABEL
y %%YLABEL
w %%WLABEL
h 28
font "helvetica-bold-r-12.0"
fontAlign "right"
fgColor index 14
bgColor index 0
useDisplayBg
value {
  "%%REGNAME"
  "%%REGADDR"
}
endObjectProperties
"""
##############################################################################
# Control Widget for Register
##############################################################################
edm_Register_Control="""
# (Text Control) Control Widget
object activeXTextDspClass
beginObjectProperties
major 4
minor 4
release 0
x %%XCNTRL
y %%YCNTRL
w %%WCNTRL
h 18
controlPv "%%PVCNTRL"
format "hex"
font "helvetica-medium-r-12.0"
fontAlign "right"
fgColor index 14
bgColor index 0
editable
autoHeight
#motifWidget
limitsFromDb
nullColor index 0
useHexPrefix
newPos
objType "controls"
noExecuteClipMask
endObjectProperties
"""
##############################################################################
# RBV Widget for Register
##############################################################################
edm_Register_RBV="""
# (Text Control) RBV Widget
object activeXTextDspClass
beginObjectProperties
major 4
minor 4
release 0
x %%XRBV
y %%YRBV
w %%WRBV
h 18
controlPv "%%PVRBV"
format "hex"
font "helvetica-medium-r-12.0"
fontAlign "right"
fgColor index 15
bgColor index 80
autoHeight
#motifWidget
limitsFromDb
nullColor index 0
useHexPrefix
newPos
objType "controls"
noExecuteClipMask
endObjectProperties
"""
##############################################################################
# Widget for Channel Button accessed via Main Digitzer Register Screen
##############################################################################
edm_Register_ChanButton="""
# (Related Display) Button for Channel Registers
object relatedDisplayClass
beginObjectProperties
major 4
minor 2
release 0
x 5
y 5
w 80
h 20
fgColor index 25
bgColor index 1
topShadowColor index 0
botShadowColor index 14
font "helvetica-bold-r-14.0"
buttonLabel "Channels"
numPvs 4
numDsps 1
displayFileName {
  0 "DigChanRegisters.edl"
}
endObjectProperties
"""
