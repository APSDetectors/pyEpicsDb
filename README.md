# pyEpicsDb

Python Functions for manipulating Epics Databases

This software was design for the Digital Gammasphere project in the Pysics Division
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

