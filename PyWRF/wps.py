##!/usr/local/bin/python
#!/disk5/chl/anaconda2/bin/python
#=======================================================================
# Running WPS Scripts
#
# 2016-09-16, Liang Chen, chenliang@tea.ac.cn
#
#=======================================================================
# Module importation
#=======================================================================
import os
import subprocess
import re
import environment_vars

def run(args):
    print('Start running WPS...')
    print('Task:', args.task)

    environment_vars.WORK_ROOT = os.path.join(environment_vars.WPS_ROOT, environment_vars.RUN_NAME)
    print('WORK_ROOT:', environment_vars.WORK_ROOT)

    os.chdir(environment_vars.WPS_ROOT)

    if not os.path.exists(environment_vars.WORK_ROOT):
        os.mkdir(environment_vars.WORK_ROOT)

    os.chdir(environment_vars.WORK_ROOT)
    
    if args.task == 'make_new_run':
        make_new_run()

    elif args.task == 'make_namelist':
        make_namelist()

    elif args.task == 'geogrid':
        run_geogrid()

    elif args.task == 'ungrib':
        run_ungrib()

    elif args.task == 'metgrid':
        run_metgrid()

def make_new_run():
    tmp_dirs = ['geogrid','metgrid',]
    for tmp_dir in tmp_dirs:
        if not os.path.lexists(tmp_dir):
            os.mkdir(tmp_dir)

    tmp_cmds = [
    'ln -sf ' + environment_vars.WPS_ROOT + '/geogrid/src/geogrid.exe .',
    'ln -sf ' + environment_vars.WPS_ROOT + '/geogrid/GEOGRID.TBL.ARW ./geogrid/GEOGRID.TBL',
    'ln -sf ' + environment_vars.WPS_ROOT + '/link_grib.csh .',
    'ln -sf ' + environment_vars.WPS_ROOT + '/ungrib/src/ungrib.exe .',
    'ln -sf ' + environment_vars.WPS_ROOT + '/ungrib/Variable_Tables/Vtable.ERA-interim.pl Vtable',
    'ln -sf ' + environment_vars.WPS_ROOT + '/metgrid/METGRID.TBL.ARW ./metgrid/METGRID.TBL',
    'ln -sf ' + environment_vars.WPS_ROOT + '/metgrid/src/metgrid.exe .',
    ]
    for tmp_cmd in tmp_cmds:
        subprocess.call(tmp_cmd, shell=True)

def make_namelist():
    start_time = str(environment_vars.START_TIME).replace(' ', '_')
    end_time = str(environment_vars.END_TIME).replace(' ', '_')

    max_dom = str(environment_vars.MAX_DOM)
    e_we = re.sub(r'\[|\]', '', str(environment_vars.E_WE))
    e_sn = re.sub(r'\[|\]', '', str(environment_vars.E_SN))
    e_vert = re.sub(r'\[|\]', '', str(environment_vars.E_VERT))
    i_parent_start = re.sub(r'\[|\]', '', str(environment_vars.I_PARENT_START))
    j_parent_start = re.sub(r'\[|\]', '', str(environment_vars.J_PARENT_START))
    dx = str(environment_vars.DX[0])
    dy = str(environment_vars.DY[0])

    ref_lat   = str(environment_vars.REF_LAT)
    ref_lon   = str(environment_vars.REF_LON)
    truelat1  = str(environment_vars.TRUELAT1)
    truelat2  = str(environment_vars.TRUELAT2)
    stand_lon = str(environment_vars.STAND_LON)

    interval_seconds = str(environment_vars.INTERVAL_SECONDS)

    namelist = open('namelist.wps', 'w')
    #=================== write namelist.wps ===================
    namelist.write("""
&share
 wrf_core = 'ARW',
 max_dom = """ + max_dom + """,
 start_date = '""" + start_time + """','""" + start_time + """',
 end_date   = '""" + end_time + """','""" + end_time + """',
 interval_seconds = """ + interval_seconds + """
 io_form_geogrid = 2,
 debug_level=10
/

&geogrid
 parent_id         =   1,   1,   1,
 parent_grid_ratio =   1,   3,   3,
 i_parent_start    =  """ + i_parent_start + """,
 j_parent_start    =  """ + j_parent_start + """,
 e_we              =  """ + e_we + """,
 e_sn              =  """ + e_sn + """
 geog_data_res     = 'default','default',
 dx = """ + dx + """,
 dy = """ + dy + """,
 map_proj = 'lambert',
 ref_lat   = """ + ref_lat + """,
 ref_lon   = """ + ref_lon + """,
 truelat1  = """ + truelat1 + """,
 truelat2  = """ + truelat2 + """,
 stand_lon = """ + stand_lon + """,
 geog_data_path = '""" + environment_vars.GEOG_DATA_PATH + """'
/

&ungrib
 out_format = 'WPS',
 prefix = 'FILE',
/

&metgrid
 fg_name = 'FILE',
 io_form_metgrid = 2
/

&mod_levs
 press_pa = 201300 , 200100 , 100000 ,
            975000 ,  95000 ,  90000 ,
            85000 ,  80000 ,
            75000 ,  70000 ,
            65000 ,  60000 ,
            55000 ,  50000 ,
            45000 ,  40000 ,
            35000 ,  30000 ,
            25000 ,  20000 ,
            15000 ,  10000 ,
            5000 ,   1000
/""")
    #=================== configuration-e ===================
    namelist.close()

def run_geogrid():
    if environment_vars.MPI_WPS == False:
        subprocess.call('./geogrid.exe', shell=True)
    else:
        subprocess.call('bsub -J geogrid -a intelmpi -n 18 -o geogrid.lsf mpirun.lsf geogrid.exe', shell=True)

def run_ungrib():
    subprocess.call('./link_grib.csh ' + environment_vars.ERAI_DATA_PATH + '/fnl*', shell=True)

    if environment_vars.MPI_WPS == False:
        subprocess.call('./ungrib.exe', shell=True)
    else:
        subprocess.call('./ungrib.exe', shell=True)

def run_metgrid():

    if environment_vars.MPI_WPS == False:
        subprocess.call('./metgrid.exe', shell=True)
    else:
        subprocess.call('bsub -J metgrid -a intelmpi -n 18 -o metgrid.lsf mpirun.lsf metgrid.exe', shell=True)

    subprocess.call('cp met_em* ' + environment_vars.RESULTS_WPS, shell=True)
    subprocess.call('cp namelist.wps ' + environment_vars.RESULTS_WPS, shell=True)
    #subprocess.call('ln -sf ' + environment_vars.RESULTS_WPS + '/met_em* .', shell=True)
