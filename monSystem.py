

########################################################################################
#
#
#
#
#
#########################################################################################


import subprocess
import re

import time



#List of pvs that start with DigG
pv_list=[
'Online_CS_StartStop',
'Online_CS_SaveData',
'DAQG_CS_BuildEnable',
'DAQC4_CV_SendRate',
'DAQC5_CV_SendRate',
'DAQC6_CV_SendRate',
'DAQC7_CV_SendRate',
'DAQC8_CV_SendRate',
'DAQC9_CV_SendRate',
'DAQC10_CV_SendRate',
'DAQC11_CV_SendRate',
'DAQC4_CV_BuffersAvail',
'DAQC5_CV_BuffersAvail',
'DAQC6_CV_BuffersAvail',
'DAQC7_CV_BuffersAvail',
'DAQC8_CV_BuffersAvail',
'DAQC9_CV_BuffersAvail',
'DAQC10_CV_BuffersAvail',
'DAQC11_CV_BuffersAvail',
'DAQC4_CV_NumSendBuffers',
'DAQC5_CV_NumSendBuffers',
'DAQC6_CV_NumSendBuffers',
'DAQC7_CV_NumSendBuffers',
'DAQC8_CV_NumSendBuffers',
'DAQC9_CV_NumSendBuffers',
'DAQC10_CV_NumSendBuffers',
'DAQC11_CV_NumSendBuffers',
'DAQC4_CV_NotAAAErrors',
'DAQC5_CV_NotAAAErrors',
'DAQC6_CV_NotAAAErrors',
'DAQC7_CV_NotAAAErrors',
'DAQC8_CV_NotAAAErrors',
'DAQC9_CV_NotAAAErrors',
'DAQC10_CV_NotAAAErrors',
'DAQC11_CV_NotAAAErrors'

]



def monSystem(pvlist):

	logfile = 'syslog.txt'

	stime= 1.0
	
	f=open(logfile,'w')
	
	#headings
	f.write('Time\t')
	for p in pvlist:
		f.write('%s\t'%(p))
	f.write('\n')
	f.flush()
	f.close()
	
	while(True):
		time.sleep(stime)
		f=open(logfile,'a')
		f.write('%s\t'%(datetime.now().strftime("%A, %d. %B %Y %I:%M:%S%p ")))

		for p in pvlist:
			v=caget(p);
			
			f.write('%s\t'%(v))
			
		
		
		f.write('\n')
		f.flush()
		f.close()
		
	

		
		


########################################################################################
#
#
#
#
#
#########################################################################################


def caget(pvname):
  val=subprocess.Popen(['caget', '-tw5', pvname],stdout=subprocess.PIPE).communicate()[0]
  val=re.match('\S*',val).group(0)
  return(val)



########################################################################################
#
#
#
#
#
#########################################################################################


def caput(pvname,val):
  oval=subprocess.Popen(['caput','-w5' ,pvname, val],stdout=subprocess.PIPE).communicate()[0]



########################################################################################
#
#
#
#
#
#########################################################################################

def caput_fl(pvname,v):
  val="%f"%(v)
  oval=subprocess.Popen(['caput','-w5', pvname, val],stdout=subprocess.PIPE).communicate()[0]


########################################################################################
#
#
#
#
#
#########################################################################################


#return number from pv, not str- if enum it gets nuimber
def caget_fl(pvname):

  if isPvEnum(pvname)==1:
    val=subprocess.Popen(['caget', '-tnw5', pvname],stdout=subprocess.PIPE).communicate()[0]
  else:
    val=subprocess.Popen(['caget', '-tw5', pvname],stdout=subprocess.PIPE).communicate()[0]

  if (len(val)>0):
    vf=float(val)
  else:
    vf=-1000000;

  return(vf)








########################################################################################
#
#
#
#
#
#########################################################################################



def cainfo(pvname):
  val=subprocess.Popen(['cainfo',  pvname],stdout=subprocess.PIPE).communicate()[0]

  return(val)


########################################################################################
#
#
#
#
#
#########################################################################################


def isPvEnum(pvname) :
  strg=cainfo(pvname)
  if re.search('DBR_ENUM',strg)==None :
    is_enum=0
  else:
    is_enum=1

  return(is_enum)


