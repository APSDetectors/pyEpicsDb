# pyEpicsDb

Python Functions for manipulating Epics Databases

##History

This software, called pyEpicsDb, was design for the Digital Gammasphere project in the Pysics Division
Argonne National Laboratory. Digital Gammasphere (DGS) is a new digital data 
acquision system used in Gamma ray experiments at the Atlas Accelerator at Argonne.
The digital DAQ hardware is FPGA based. As the experiments developed at Atlas, 
firmware needed to be routinely changed in the DAQ hardware. For every change in the
firmware, considerable software changes were necessary such as altertering the
EPICS database, editing the GUI, editing the C++ code used to configure the FPGA.
Because so many changes to the firmware were necessary, softwarwe was designed for 
automatic generation of EPICS databases, C++ code, and GUIs based on the FPGA
firmware. Given a text comma-delimited spreadsheet detailing the FPGA firmware
registers, python scripts can reqad this spreadsheet and automatically generate
EPICS databases, C code and GUIs. In this way, every change in the FPGA firmware
allowed automatic updating of the software drivers and user interfaces. 

##How this software can be used.

pyEpicsDb can be used for the following purposes:
1. Programmatically generating EPICS databases.
2. parsing EPICS template files into python objects fr programmacic manipulation
3. Documenting EPICS databases by generating an HTML table of EPICS PVs
4. Reformatting EPICS template files for uniform white space usage.
5. Given a list of PVs in a spread sheet, one can generate:
	* EPICS template files.
	* Control System Studio GUI screens
	* asynDriver C++ code to support the PVs in software
	* IOC startup files
6. given an EPICS template file, one can generate GUIs and C++ asynDriver code.
7. Parsing EDM GUI files and generating OPI Control System Studio files.
8. Generating EPICS database template files,C++ code, startup files from Control
   System Studio opi files. One can draw a GUI, save it, gen generate much of the
   IOC code and databases needed to host the PVs.
   
   
The heart of pyEpicsDb is the epicspv class, in epicsclass.py. This class represents
a single epics PV with all its fields and asynDriver definitions. An entire database
is represented as a python list of these objects. epicspv, given a file handle, can
parse or write to an epics template file. All fields can be programmatically changed,
deleted or added. Also PVs can be entirely programmacitalkly created and written 
to an EPICS template file. 
   
   
##Examples:

###Reformat db files

To reformat a template file for nice white space usage:

```
execfile('epicsDb2Docs.py')

fn = 'D:/Madden/GitHub/areaDetector-R2-4/ADPCO/pcoApp/Db/pco_metarecs.template'

#read EPICS database template into a python list of epicspv objects.

db =readDb(fn)
#write database
writeDb(db,fn)
#now white space is nicer.
```

###HTML docs
To generate an HTML table of an epics database it is easiest to have PV names
and asynDriver parameter strings the same. Otherwise one must have some
set of rules of how params, param strings and PVs are named. pvEpicsDb is written
such that PVs, params, param strings are all identical.
To generate a table:
```
#read EPICS database template into a python list of epicspv objects.

fn = 'D:/Madden/GitHub/areaDetector-R2-4/ADPCO/pcoApp/Db/pco_metarecs.template'
db =readDb(fn)
#Generate an html table for documentation
dbToHtmlDoc(db,filename='table.html')

```

###Find PV object in a database
```
pv = findPv(db,'$(P)$(R)mypv')
```

### Grouping PVs

To associate write PVs with corresponding readback PVs, we name the write PV
$(P)$(R)mypv, and the readback pv as $(P)$(R)mypv_RBV
we can group these PVs as tuples from a list of pv objects.

```
fn = 'D:/Madden/GitHub/areaDetector-R2-4/ADPCO/pcoApp/Db/pco_metarecs.template'
#read EPICS database template into a python list of epicspv objects.
db =readDb(fn)
dbgr = groupDbRBV(db)
#now dbgr contains tuples of pvs and corresponding RBV pvs. pvs without their 
# read or write compliment are in tuples by themselves.
```
          



###Generation CSS screen programmatically

The the file guiClass.py has two classes defined:
1) cssScreen which defines a CSS boy screen.
2) cssWidget which defines a button or widget on the cssScreen.
All data in the cssWidget is stored as XML. When the widget is accessed programmatically,
XML generation and parsing takes place under the hood. No python variables store the
state of the widget, but only XML.
Below is an example for generatioon a css screen.

```
execfile('guiClass.py')
c=cssWidget()
c.setType('boolbutton')
c.setField('x','100')
c.setField('y','200')
c.setField('width','20')
c.setField('height','20')
c.setField('pv_name','maddog')

c.listFields()

d=cssWidget()
d.setType('combo')
d.setField('x','1000')
d.setField('y','2000')
d.setField('width','200')
d.setField('height','20')
d.setField('pv_name','birddy')

d.listFields()

s=cssScreen()
s.addWidget(c)
s.addWidget(d)
s.listWidgets()

c.setField('AAA','timmadden')
print c.getXML()

```

