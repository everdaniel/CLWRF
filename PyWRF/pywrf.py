##!/usr/local/bin/python
#!/disk5/chl/anaconda2/bin/python
# ==============================================================================
#  Author: Liang Chen
#  Email: chenliang@tea.ac.cn
#  Date: 2016-09-11
# ------------------------------------------------------------------------------
#  Usage:
#
#  - WPS
#  ./pywrf.py wps -t make_namelist \
#                 -s <start_time> -e <end_time> -r <running_hours>
#  ./pywrf.py wps -t geogrid
#  ./pywrf.py wps -t ungrib
#  ./pywrf.py wps -t metgrid
#
#  - WRF
#  ./pywrf.py wrf -t make_namelist \
#                 -s <start_time> -e <end_time> -r <running_hours>
#  ./pywrf.py wrf -t real
#  ./pywrf.py wrf -t wrf
# ==============================================================================

import argparse
import settings
import environment_vars
import wps
import wrf

def main():
    parser = argparse.ArgumentParser(description='Run WRF in Python')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s V1.0')
    subparsers = parser.add_subparsers(help='running mode')
    subparsers.required = True
    subparsers.dest = 'mode'
    parser_wps = subparsers.add_parser('wps', help='run WPS')
    parser_wrf = subparsers.add_parser('wrf', help='run WRF')

    # ============================================
    #  WPS
    # ============================================
    parser_wps.add_argument(
        '-t',
        '--task',
        required=True,
        choices=[
            'make_new_run',
            'make_namelist',
            'geogrid',
            'ungrib',
            'metgrid'
        ],
        help='running task'
    )
    parser_wps.add_argument('-o','--workdir',help='work directory')
    # below are just for make_namelist task
    parser_wps.add_argument('-s', '--start', help='start time')
    wps_run_length = parser_wps.add_mutually_exclusive_group()
    wps_run_length.add_argument('-e', '--end', help='end time')
    wps_run_length.add_argument('-r', '--run', help='running hours')
    # other parameters
    parser_wps.add_argument('-i','--interval_seconds',help='interval seconds')
    parser_wps.add_argument('--spec_bdy_width',help='boundary width')
    parser_wps.add_argument('--relax_zone',help='relax zone')

    # ============================================
    #  WRF
    # ============================================
    parser_wrf.add_argument(
        '-t',
        '--task',
        required=True,
        choices=[
            'make_new_run',
            'make_namelist',
            'make_real_srun',
            'make_wrf_srun',
            'real',
            'wrf'
        ],
        help='running task'
    )
    parser_wrf.add_argument('-o','--workdir',help='work directory')
    
    # below are just for make_namelist task
    parser_wrf.add_argument('-s','--start',help='start time')
    wrf_run_length = parser_wrf.add_mutually_exclusive_group()
    wrf_run_length.add_argument('-e','--end',help='end time')
    wrf_run_length.add_argument('-r','--run',help='running hours')

    # other parameters
    parser_wrf.add_argument('-i','--interval_seconds',help='interval seconds')
    parser_wrf.add_argument('--history_interval',help='history interval')
    parser_wrf.add_argument('--spec_bdy_width',help='boundary width')
    parser_wrf.add_argument('--relax_zone',help='relax zone')
    parser_wrf.add_argument('--damp_opt',help='relax zone')

    # parse the input command line
    args = parser.parse_args()
    # ============================================
    # initial
    # ============================================
    settings.init(args)

    if args.mode == 'wps':
        wps.run(args)

    elif args.mode == 'wrf':
        wrf.run(args)

if __name__ == '__main__':
    main()    
