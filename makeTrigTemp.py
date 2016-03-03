


import os;
#import io;


is_gretina_dev = 1;


def boRecords(st_address,ed_address) :
  tfile = open('trigDbgBo.template','w+');

  tfile.write("# This is pyuthon gen file for Trigger");

  #st_address = 0x800
  #ed_address = 0x810

  pvbase_bo = 'Trig$(T)_DbgWrAddr_'
  pvbase_bi = 'Trig$(T)_DbgRdAddr_'

  st_bit =0;
  ed_bit = 15;

  bits = range(st_bit,ed_bit+1);
  addresses = range(st_address,ed_address+1);


  for adr in addresses :
    for bit in bits :
     tfile.write(" ");
     tfile.write("\n");  
     tfile.write(" ");  
     tfile.write("\n");  
     pvname="%s0x%x_%i" % (pvbase_bo,adr,bit)
     print "Making " + pvname
     strx = "record(bo, \"%s\") {" % (pvname)
     tfile.write(strx);  
     tfile.write("\n");  
     strx = "  field(DESC, \"Debugging\")"
     tfile.write(strx); 
     tfile.write("\n");  
     strx = "field(PINI, \"YES\")"
     tfile.write(strx);  
     tfile.write("\n");  
     strx = "field(DTYP, \"Gretina Trigger\")"
     tfile.write(strx);  
     tfile.write("\n");  
     strx = "field(DOL, \"0\")"
     tfile.write(strx);  
     tfile.write("\n");  
     strx = "field(OUT, \"#C$(C) S0x%x @%i\")" % (adr,bit)
     tfile.write(strx);  
     tfile.write("\n");  
     strx = "field(ZNAM, \"Off\")"
     tfile.write(strx);  
     tfile.write("\n");  
     strx = "field(ONAM, \"On\")"
     tfile.write(strx);  
     tfile.write("\n");  
     strx = "}"
     tfile.write(strx);  
     tfile.write("\n");  
  
  tfile.close();

#location for db files...edit vme32.cmd in iocBoot/iocArray
#/global/devel_tjm/gretTop/9-22/tcDet/db


def aRecords1(st_address,ed_address,ioc,slot,filenumber) :
  lfile = open('aRecList%i_%i_%i.txt'%(filenumber,ioc,slot),'w+');
  tfile = open('Trig%i_%i_%i_Dbg.db'%(filenumber,ioc,slot),'w+');

  tfile.write("# This is pyuthon gen file for Trigger");

  #st_address = 0x800
  #ed_address = 0x810

  pvbase_ai = 'Trig%i_aiAddr_' %(slot)
  pvbase_ao = 'Trig%i_aoAddr_' %(slot)

  addresses = range(st_address,ed_address+1,4);


  for adr in addresses :
    tfile.write(" ");
    tfile.write("\n");  
    tfile.write(" ");  
    tfile.write("\n");  
    pvname="%s0x%x" % (pvbase_ai,adr)
    print "Making " + pvname
    strx = "record(ai, \"%s\") {" % (pvname)
    tfile.write(strx);  
    tfile.write("\n");  
    strx = "  field(DESC, \"Debugging\")"
    tfile.write(strx);  
    tfile.write("\n");  
    
    strx="  field(PINI, \"YES\")"
    tfile.write(strx);  
    tfile.write("\n");  
    
    if (is_gretina_dev==1) :
      strx = "  field(DTYP, \"Gretina Trigger\")"
      tfile.write(strx);  
      tfile.write("\n");
      strx = "  field(INP, \"#C%i S0x%x @\")" % (slot,adr)
      tfile.write(strx);  
      tfile.write("\n");

  
    if (is_gretina_dev==0) :      
      strx = "  field(INP, \"%s0x%x\")" % (pvbase_ao,adr)
      tfile.write(strx);  
      tfile.write("\n");

        
    strx = "  field(SCAN, \"passive\")"
    tfile.write(strx);  
    tfile.write("\n");
    strx = "}"
    tfile.write(strx);  
    tfile.write("\n");  


  for adr in addresses :
    tfile.write(" ");
    tfile.write("\n");  
    tfile.write(" ");  
    tfile.write("\n");  
    pvname="%s0x%x" % (pvbase_ao,adr)
    print "Making " + pvname
    strx = "record(ao, \"%s\") {" % (pvname)
    tfile.write(strx);  
    tfile.write("\n");  
    strx = "  field(DESC, \"Debugging\")"
    tfile.write(strx);  
    tfile.write("\n");  
    
    if (is_gretina_dev==1) :
      strx = "  field(DTYP, \"Gretina Trigger\")"
      tfile.write(strx);  
      tfile.write("\n");  
      strx = "  field(OUT, \"#C%i S0x%x @\")" % (slot,adr)
      tfile.write(strx);  
      tfile.write("\n");  
      
    strx = "}"
    tfile.write(strx);  
    tfile.write("\n");  

  tfile.close();

  print "caput(\"Trig1_aoDbgWrAddr_0x804\",int(0xff))"
  print "hex(int(caget(\"Trig1_aoDbgWrAddr_0x804\")))"
  print "dbgf \"Trig1_aoDbgWrAddr_0x804\""
  print "dbpf \"Trig1_aoDbgWrAddr_0x804\",\"43211\""




  for adr in addresses :
    pvname="%s0x%x" % (pvbase_ai,adr)
    print "Making " + pvname
    strx = "0x%x ai %s %i %i\n" % (adr,pvname,ioc,slot)
    lfile.write(strx);  


  for adr in addresses :
    pvname="%s0x%x" % (pvbase_ao,adr)
    print "Making " + pvname
    strx = "0x%x ao %s %i %i\n" % (adr,pvname,ioc,slot)
    lfile.write(strx);  

  tfile.close();



#record(longout, "$(P)$(R)reg_jta_diag1")
#{
#   field(DTYP, "asynInt32")
#   field(OUT,  "@asyn($(PORT),$(ADDR),$(TIMEOUT))reg_jta_diag1")
#}

def asynLongOut(param_list,filename) :
	tfile = open(filename,'w+');
	tfile.write("# This is pyuthon gen file for asyn");
	pvfile = open('pv_out.txt','w+');
	
	indices = range(0,len(param_list)-1);

	for ii in indices :
		param=param_list[ii];
		
		tfile.write(" ");
		tfile.write("\n");  
		tfile.write(" ");  
		tfile.write("\n");  
		pvname="$(P)$(R)%s" % (param)
		pvfile.write(pvname+"\n");
		print "Making " + pvname
		strx = "record(longout, \"%s\") {" % (pvname)
		tfile.write(strx);  
		tfile.write("\n");  
		strx = "  field(DTYP, \"asynUInt32Digital\")"
		tfile.write(strx);  
		tfile.write("\n");  

		strx = "  field(OUT,  \"@asynMask($(PORT),$(ADDR),0xaaaa2000,$(TIMEOUT))%s\")" % (param)
		tfile.write(strx);  
		tfile.write("\n");  
		
		tfile.write("}\n\n");
	
	tfile.close();
	pvfile.close();






#record(longin, "$(P)$(R)reg_jta_diag1_RBV")
#{
#   field(PINI, "1")
#   field(DTYP, "asynInt32")
#   field(INP,  "@asyn($(PORT),$(ADDR),$(TIMEOUT))reg_jta_diag1")
#   field(SCAN, "I/O Intr")
#}


def asynLongIn(param_list,filename) :
	tfile = open(filename,'w+');
	tfile.write("# This is pyuthon gen file for asyn");
	pvfile = open('pv_in.txt','w+');
	
	indices = range(0,len(param_list)-1);

	for ii in indices :
		param=param_list[ii];
		
		tfile.write(" ");
		tfile.write("\n");  
		tfile.write(" ");  
		tfile.write("\n");  
		pvname="$(P)$(R)%s_RBV" % (param)
		pvfile.write(pvname+"\n");
		print "Making		" + pvname
		strx = "record(longin, \"%s\") {" % (pvname)
		tfile.write(strx);  
		tfile.write("\n");  
		tfile.write("  field(PINI, \"1\")\n");  
		
		tfile.write("  field(DTYP, \"asynUInt32Digital\")\n");  
		

		strx = "  field(INP,  \"@asynMask($(PORT),$(ADDR),0xaaaa2000,$(TIMEOUT))%s\")" % (param)
		tfile.write(strx);  
		tfile.write("\n");  
		
		tfile.write("  field(SCAN, \"1 second\")\n");
		
		tfile.write("}\n\n");
	
	tfile.close();
	pvfile.close();





def aRecords2(addr_list,name_list,ioc,slot,fnumber) :
  lfile = open('aRecList%i_%i_%i.txt'%(fnumber,ioc,slot),'w+');
  tfile = open('Trig%i_%i_%i_Dbg.db'%(fnumber,ioc,slot),'w+');

  tfile.write("# This is pyuthon gen file for Trigger");

  #st_address = 0x800
  #ed_address = 0x810

  pvbase_ai = 'Trig%i_%i_ai_' %(ioc,slot)
  pvbase_ao = 'Trig%i_%i_ao_' %(ioc,slot)

  indices = range(0,len(addr_list)-1);


  for ii in indices :
    adr=addr_list[ii];
    name = name_list[ii];
    tfile.write(" ");
    tfile.write("\n");  
    tfile.write(" ");  
    tfile.write("\n");  
    pvname="%s%s" % (pvbase_ai,name)
    print "Making		" + pvname
    strx = "record(ai, \"%s\") {" % (pvname)
    tfile.write(strx);  
    tfile.write("\n");  
    strx = "  field(DESC, \"Debugging\")"
    tfile.write(strx);  
    tfile.write("\n");  
    
    strx="  field(PINI, \"YES\")"
    tfile.write(strx);  
    tfile.write("\n");  
    
    if (is_gretina_dev==1) :
      strx = "  field(DTYP, \"Gretina Trigger\")"
      tfile.write(strx);  
      tfile.write("\n");
      strx = "  field(INP, \"#C%i S0x%x @\")" % (slot,adr)
      tfile.write(strx);  
      tfile.write("\n");

  
    if (is_gretina_dev==0) :      
      strx = "  field(INP, \"%s0x%x\")" % (pvbase_ao,adr)
      tfile.write(strx);  
      tfile.write("\n");

        
    strx = "  field(SCAN, \"passive\")"
    tfile.write(strx);  
    tfile.write("\n");
    strx = "}"
    tfile.write(strx);  
    tfile.write("\n");  


  for ii in indices :
    adr=addr_list[ii];
    name = name_list[ii];
    tfile.write(" ");
    tfile.write("\n");  
    tfile.write(" ");  
    tfile.write("\n");  
    pvname="%s%s" % (pvbase_ao,name)
    print "Making " + pvname
    strx = "record(ao, \"%s\") {" % (pvname)
    tfile.write(strx);  
    tfile.write("\n");  
    strx = "  field(DESC, \"Debugging\")"
    tfile.write(strx);  
    tfile.write("\n");  
    
    if (is_gretina_dev==1) :
      strx = "  field(DTYP, \"Gretina Trigger\")"
      tfile.write(strx);  
      tfile.write("\n");  
      strx = "  field(OUT, \"#C%i S0x%x @\")" % (slot,adr)
      tfile.write(strx);  
      tfile.write("\n");  
      
    strx = "}"
    tfile.write(strx);  
    tfile.write("\n");  

  tfile.close();

  print "caput(\"Trig1_aoDbgWrAddr_0x804\",int(0xff))"
  print "hex(int(caget(\"Trig1_aoDbgWrAddr_0x804\")))"
  print "dbgf \"Trig1_aoDbgWrAddr_0x804\""
  print "dbpf \"Trig1_aoDbgWrAddr_0x804\",\"43211\""



  for ii in indices :
    adr=addr_list[ii];
    name = name_list[ii];
    pvname="%s%s" % (pvbase_ai,name)
    print "Making " + pvname
    strx = "0x%x ai %s %i %i\n" % (adr,pvname,ioc,slot)
    lfile.write(strx);  

  for ii in indices :
    adr=addr_list[ii];
    name = name_list[ii];
    pvname="%s%s" % (pvbase_ao,name)
    print "Making " + pvname
    strx = "0x%x ao %s %i %i\n" % (adr,pvname,ioc,slot)
    lfile.write(strx);  

  lfile.close();



def aClient(st_address,ed_address,ioc) :
  tfile = open('trigClient.py','w+');

  tfile.write("# This is pyuthon gen file for Trigger\n\n");

  tfile.write("from CaChannel import CaChannel\n");
  tfile.write("from CaChannel import CaChannelException\n");
  tfile.write("import ca\n");

  tfile.write("import time\n");
  tfile.write("import datetime\n");
  tfile.write("import io\n");
  tfile.write("import os\n");
  tfile.write("import sys\n\n\n");

  #st_address = 0x800
  #ed_address = 0x810

  pvbase_ai = 'Trig%i_aiAddr_' % (ioc)

  pvbase_ao = 'Trig%i_aoAddr_' % (ioc)

  addresses = range(st_address,ed_address+1);

  tfile.write("\nprint \"Creating and Connecting EPICS channels\"\n");  

  print "Copy/Paste to get/put"

  for adr in addresses :
    
    tfile.write("\n");  
     
    tfile.write("\n");  
    pvname="%s0x%x" % (pvbase_ao,adr)
    print "%s.putw(intval)\n" % (pvname) 
    
    tfile.write("try:\n");
    tfile.write("  %s = CaChannel()\n" % (pvname))
    tfile.write("  %s.searchw(\"%s\")\n" % (pvname,pvname))
    tfile.write("except CaChannelException, status:\n");
    tfile.write("  print \"Could not connect %s\" \n"% (pvname));
    tfile.write("  print ca.message(status)\n\n\n");


  for adr in addresses :
    
    tfile.write("\n");  
     
    tfile.write("\n");  
    pvname="%s0x%x" % (pvbase_ai,adr)
    print "%s.getw()\n" % (pvname) 

    tfile.write("try:\n");
    tfile.write("  %s = CaChannel()\n" % (pvname))
    tfile.write("  %s.searchw(\"%s\")\n" % (pvname,pvname))
    tfile.write("except CaChannelException, status:\n");
    tfile.write("  print \"Could not connect %s\" \n"% (pvname));
    tfile.write("  print ca.message(status)\n\n\n");

    

  print "run execfile(\"trigClient.py\")"
  tfile.close();





def aRecordList(st_address,ed_address,ioc) :
  tfile = open('aRecList%i.txt'%(ioc),'w+');


  #st_address = 0x800
  #ed_address = 0x810

  pvbase_ai = 'Trig%i_aiAddr_' %(ioc)
  pvbase_ao = 'Trig%i_aoAddr_' %(ioc)

  addresses = range(st_address,ed_address+1);


  for adr in addresses :
    pvname="%s0x%x" % (pvbase_ai,adr)
    print "Making " + pvname
    strx = "0x%x ai %s\n" % (adr,pvname)
    tfile.write(strx);  


  for adr in addresses :
    pvname="%s0x%x" % (pvbase_ao,adr)
    print "Making " + pvname
    strx = "0x%x ao %s\n" % (adr,pvname)
    tfile.write(strx);  

  tfile.close();


param_name_list=[
	'regin_fbus_status',
	'regin_latched_timestamp_lsb',
	'regin_latched_timestamp_msb',
	'regin_live_timestamp_lsb',
	'regin_live_timestamp_msb',
	'regin_master_logic_status',
	'regin_sd_read',
	'reg_board_id',
	'reg_programming_done',
	'reg_external_window',
	'reg_pileup_window',
	'reg_noise_window',
	'reg_ext_trig_length',
	'reg_collection_time',
	'reg_egration_time',
	'reg_hardware_status',
	'reg_user_package_data',
	'reg_control_status_0',
	'reg_control_status_1',
	'reg_control_status_2',
	'reg_control_status_3',
	'reg_control_status_4',
	'reg_control_status_5',
	'reg_control_status_6',
	'reg_control_status_7',
	'reg_control_status_8',
	'reg_control_status_9',
	'reg_led_threshold_0',
	'reg_led_threshold_1',
	'reg_led_threshold_2',
	'reg_led_threshold_3',
	'reg_led_threshold_4',
	'reg_led_threshold_5',
	'reg_led_threshold_6',
	'reg_led_threshold_7',
	'reg_led_threshold_8',
	'reg_led_threshold_9',
	'reg_cfd_parameters_0',
	'reg_cfd_parameters_1',
	'reg_cfd_parameters_2',
	'reg_cfd_parameters_3',
	'reg_cfd_parameters_4',
	'reg_cfd_parameters_5',
	'reg_cfd_parameters_6',
	'reg_cfd_parameters_7',
	'reg_cfd_parameters_8',
	'reg_cfd_parameters_9',
	'reg_raw_data_length_0',
	'reg_raw_data_length_1',
	'reg_raw_data_length_2',
	'reg_raw_data_length_3',
	'reg_raw_data_length_4',
	'reg_raw_data_length_5',
	'reg_raw_data_length_6',
	'reg_raw_data_length_7',
	'reg_raw_data_length_8',
	'reg_raw_data_length_9',
	'reg_raw_data_window_0',
	'reg_raw_data_window_1',
	'reg_raw_data_window_2',
	'reg_raw_data_window_3',
	'reg_raw_data_window_4',
	'reg_raw_data_window_5',
	'reg_raw_data_window_6',
	'reg_raw_data_window_7',
	'reg_raw_data_window_8',
	'reg_raw_data_window_9',
	'reg_ge_d_window',
	'reg_ge_k_window',
	'reg_ge_m_window',
	'reg_jta_diag1',
	'reg_bgo_d_window',
	'reg_bgo_k_window',
	'reg_bgo_m_window',
	'reg_channel_pulsed_control',
	'REG_0194',
	'REG_0198',
	'REG_019C',
	'REG_01A0',
	'REG_01A4',
	'REG_01A8',
	'REG_01AC',
	'REG_01B0',
	'REG_01B4',
	'REG_01B8',
	'REG_01BC',
	'REG_01C0',
	'REG_01C4',
	'REG_01C8',
	'REG_01CC',
	'REG_01D0',
	'REG_01D4',
	'REG_01D8',
	'REG_01DC',
	'REG_01E0',
	'REG_01E4',
	'REG_01E8',
	'REG_01EC',
	'REG_01F0',
	'REG_01F4',
	'REG_01F8',
	'reg_diag_channel_input',
	'reg_dac',
	'reg_fbus_status',
	'reg_fbus_sdata_send_0',
	'reg_fbus_sdata_send_1',
	'reg_fbus_sdata_send_2',
	'reg_fbus_sdata_send_3',
	'reg_fbus_sdata_send_4',
	'reg_fbus_sdata_send_5',
	'reg_fbus_sdata_send_6',
	'reg_fbus_sdata_send_7',
	'reg_fbus_sdata_send_8',
	'reg_fbus_sdata_send_9',
	'reg_fbus_sdata_send_10',
	'reg_fbus_unused',
	'reg_fbus_sdata_receive_0',
	'reg_fbus_sdata_receive_1',
	'reg_fbus_sdata_receive_2',
	'reg_fbus_sdata_receive_3',
	'reg_fbus_sdata_receive_4',
	'reg_fbus_sdata_receive_5',
	'reg_fbus_sdata_receive_6',
	'reg_fbus_sdata_receive_7',
	'reg_fbus_sdata_receive_8',
	'reg_fbus_sdata_receive_9',
	'reg_fbus_sdata_receive_10',
	'reg_master_logic_status',
	'reg_ccled_timer',
	'reg_deltat_X55',
	'reg_deltat_X5A',
	'reg_deltat_XA5',
	'reg_snapshot',
	'reg_xtal_id',
	'reg_get_hit_pattern_time',
	'reg_fbus_command',
	'reg_test_dig_rx_ttcl',
	'reg_fbus_mdata_send_0',
	'reg_fbus_mdata_send_1',
	'reg_fbus_mdata_send_2',
	'reg_fbus_mdata_send_3',
	'reg_fbus_mdata_send_4',
	'reg_fbus_mdata_send_5',
	'reg_fbus_mdata_send_6',
	'reg_fbus_mdata_send_7',
	'reg_fbus_mdata_send_8',
	'reg_fbus_mdata_send_9',
	'reg_fbus_mdata_send_10',
	'reg_fbus_mdata_receive_0',
	'reg_fbus_mdata_receive_1',
	'reg_fbus_mdata_receive_2',
	'reg_fbus_mdata_receive_3',
	'reg_fbus_mdata_receive_4',
	'reg_fbus_mdata_receive_5',
	'reg_fbus_mdata_receive_6',
	'reg_fbus_mdata_receive_7',
	'reg_fbus_mdata_receive_8',
	'reg_fbus_mdata_receive_9',
	'reg_fbus_mdata_receive_10',
	'reg_debug_data_buffer_addr',
	'reg_debug_data_buffer_data',
	'reg_led_flag_window',
	'reg_ADC_clock_control',
	'reg_aux_io_read',
	'reg_aux_io_write',
	'reg_aux_io_config',
	'reg_fb_read',
	'reg_fb_write',
	'reg_fb_config',
	'reg_sd_read',
	'reg_sd_write',
	'reg_sd_config',
	'reg_adc_config',
	'reg_self_trigger_enable',
	'reg_self_trigger_period',
	'reg_self_trigger_count'
]


comm_trig_jta = [
'JVP_DIAG',
'MSM_STATE',
'CHAN_PIPE_STAT',
'MISC_STAT2',
'SYS_THROTTLE_MAP',
'FRAME_12_COUNT',
'FRAME_14_COUNT',
'FRAME_15_COUNT',
'FRAME_17_COUNT',
'MONARCH_TSTAMP_A',
'MONARCH_TSTAMP_B',
'MONARCH_TSTAMP_C',
'TRIG_RATE_A_LOW',
'TRIG_RATE_A_HIGH',
'TRIG_RATE_B_LOW',
'TRIG_RATE_B_HIGH',
'TRIG_RATE_C_LOW',
'TRIG_RATE_C_HIGH',
'TRIG_RATE_D_LOW',
'TRIG_RATE_D_HIGH',
'TRIG_RATE_E_LOW',
'TRIG_RATE_E_HIGH',
'TRIG_RATE_F_LOW',
'TRIG_RATE_F_HIGH',
'TRIG_RATE_G_LOW',
'TRIG_RATE_G_HIGH',
'TRIG_RATE_H_LOW',
'TRIG_RATE_H_HIGH',
'RAW_TRIG_RATE_A_LOW',
'RAW_TRIG_RATE_A_HIGH',
'RAW_TRIG_RATE_B_LOW',
'RAW_TRIG_RATE_B_HIGH',
'RAW_TRIG_RATE_C_LOW',
'RAW_TRIG_RATE_C_HIGH',
'RAW_TRIG_RATE_D_LOW',
'RAW_TRIG_RATE_D_HIGH',
'RAW_TRIG_RATE_E_LOW',
'RAW_TRIG_RATE_E_HIGH',
'RAW_TRIG_RATE_F_LOW',
'RAW_TRIG_RATE_F_HIGH',
'RAW_TRIG_RATE_G_LOW',
'RAW_TRIG_RATE_G_HIGH',
'RAW_TRIG_RATE_H_LOW',
'RAW_TRIG_RATE_H_HIGH'
]



trigger_names = [
  'SANDBOX0',				
  'SANDBOX1',				
  'SANDBOX2',				
  'SANDBOX3',				
  'INPUT_LINK_MASK',			
  'LED_REGISTER',			
  'SKEW_CTL_A',  			
  'SKEW_CTL_B',  			
  'SKEW_CTL_C',  			
  'MISC_CLK_CTL',			
  'AUX_IO_CTL',  			
  'AUX_IO_DATA', 			
  'AUX_INPUT_SELECT',			
  'SERDES_TPOWER',			
  'SERDES_RPOWER',			
  'SERDES_LOCAL_LE',			        	  
  'SERDES_LINE_LE',			
  'LVDS_PREEMPHASIS',			
  'LINK_LRU_CTL',			
  'GENERIC_TEST_FIFO',			
  'DIAG_PIN_CTL_REG',			
  'REG_0858',				
  'REG_085C',				
  'REG_0884',				
  'REG_0888',				
  'REG_088C',				
  'REG_0890',				
  'REG_0894',				
  'REG_0898',				
  'REG_089C',				
  'MON2_FIFO_SEL',			
  'MON3_FIFO_SEL',			
  'MON4_FIFO_SEL',			
  'MON5_FIFO_SEL',			
  'MON6_FIFO_SEL',			
  'MON7_FIFO_SEL',			
  'MON8_FIFO_SEL',			
  'CHANNEL_FIFO_CTL',			 
  'REG_08D8',				
  'REG_08DC',				 
  'REG_08E8',				
  'REG_08EC',				
  'FIFO_RESETS', 			 
  'WO_REG_08FC', 			
  'LINK_LOCKED', 			
  'LINK_DEN',				
  'LINK_REN',				
  'LINK_SYNC',				
  'REG_0110',				
  'MISC_STAT',				
  'Diagnostic_A',			
  'Diagnostic_B',			
  'Diagnostic_C',			
  'Diagnostic_D',			
  'Diagnostic_E',			
  'Diagnostic_F',			
  'Diagnostic_G',			
  'Diagnostic_H',			
  'DIAG_STAT',				
  'REG_0150',				
  'REG_0154',				
  'CODE_DATE',				
  'CODE_REVISION',			
  'MON1_FIFO',				
  'MON2_FIFO',				
  'MON3_FIFO',				
  'MON4_FIFO',				
  'MON5_FIFO',				
  'MON6_FIFO',				
  'MON7_FIFO',				
  'MON8_FIFO',				
  'CHAN1_FIFO',  			
  'CHAN2_FIFO',  			
  'CHAN3_FIFO',  			
  'CHAN4_FIFO',  			
  'CHAN5_FIFO',  			
  'CHAN6_FIFO',  			
  'CHAN7_FIFO',  			
  'CHAN8_FIFO',  			
  'MON_FIFO_STAT',			
  'CHAN_FIFO_STAT',				   
  'DISC_BIT_MASK',			
  'FS_THRESH'
]

				
trigger_addresses=[
0x0930,
0x0934,
0x0938,
0x093C,
0x0800,
0x0804,
0x0808,
0x080C,
0x0810,
0x0814,
0x0818,
0x081C,
0x0820,
0x0828,
0x082C,
0x0830,
0x0834,
0x0838,
0x083C,
0x0848,
0x084C,
0x0858,
0x085C,
0x0884,
0x0888,
0x088C,
0x0890,
0x0894,
0x0898,
0x089C,
0x08A4,
0x08A8,
0x08AC,
0x08B0,
0x08B4,
0x08B8,
0x08BC,
0x08C0,
0x08D8,
0x08DC,
0x08E8,
0x08EC,
0x08F0,
0x08FC,
0x0100,
0x0104,
0x0108,
0x010C,
0x0110,
0x0128,
0x012C,
0x0130,
0x0134,
0x0138,
0x013C,
0x0140,
0x0144,
0x0148,
0x014C,
0x0150,
0x0154,
0x0158,
0x015C,
0x0160,
0x0164,
0x0168,
0x016C,
0x0170,
0x0174,
0x0178,
0x017C,
0x0180,
0x0184,
0x0188,
0x018C,
0x0190,
0x0194,
0x0198,
0x019C,
0x01A0,
0x01A4,       
0xA000,
0xE000
]




