# pyEpicsDb

Python Functions for manipulating Epics Databases

History

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

How this software can be used.

pyEpicsDb can be used for the following purposes:
1. Programmatically generating EPICS databases.
2. parsing EPICS template files into python objects fr programmacic manipulation
3. Documenting EPICS databases by generating an HTML table of EPICS PVs
4. Reformatting EPICS template files for uniform white space usage.
5. Given a list of PVs in a spread sheet, one can generate:
	a) EPICS template files.
	b) Control System Studio GUI screens
	c) asynDriver C++ code to support the PVs in software
	d) IOC startup files
6. given an EPICS template file, one can generate GUIs and C++ asynDriver code.
7. Parsing EDM GUI files and generating OPI Control System Studio files.
8. Generating EPICS database template files,C++ code, startup files from Control
   System Studio opi files. One can draw a GUI, save it, gen generate much of the
   IOC code and databases needed to host the PVs.
   
   
   
   
   
   
   

