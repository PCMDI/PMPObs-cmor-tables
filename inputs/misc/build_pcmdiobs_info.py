#!/bin/env python

# PJG 10212014 NOW INCLUDES SFTLF FROM
# /obs AND HARDWIRED TEST CASE WHICH
# NEEDS FIXIN

import cdms2
import gc
import glob
import json
import os
import sys
import time
import datetime

ver = datetime.datetime.now().strftime('v%Y%m%d')


###############################################################
datatype = 'clim'  #'timeSeries'
datatype = 'timeSeries'
datatype = 'monthly'
#datatype = 'day'
#datatype = '3hr'



if len(sys.argv) > 1:
    data_path = sys.argv[1]
else:
#   data_path = '/work/gleckler1/processed_data/obs'
    data_path = '/p/user_pub/PCMDIobs/PCMDIobs2'

if datatype == 'clim': comb = data_path + '/atmos/mon/*/*/*/*/climo/*AC.nc'

if datatype == 'timeSeries': comb = data_path + '/atmos/mon/*/*/gn/*/*.nc'
if datatype == 'timeSeries': comb = data_path + '/atmos/*/pr/*/*/*/*.nc'
if datatype == 'monthly': comb = data_path + '/atmos/mon/*/*/*/*/*.nc'
if datatype == 'day': comb = data_path + '/atmos/day/*/*/*/*/*.nc'
if datatype == '3hr': comb = data_path + '/atmos/3hr/*/*/*/*/*.nc'

pathout = '/p/user_pub/PCMDIobs/catalogue/'

#lst = glob.glob(os.path.join(data_path, '/atmos/mon/rlut/*/gn/*/ac/*.nc'))

lst = glob.glob(comb)



# FOR MONTHLY MEAN OBS
obs_dic_in = {'rlut': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rst': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rsut': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rsds': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rlds': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rsdt': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rsdscs': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rldscs': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rlus': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rsus': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rlutcs': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rsutcs': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rstcre': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'rltcre': {'default': 'CERES-EBAF-4-1','alternate1': 'CERES-EBAF-4-0'},
              'pr': {'default': 'GPCP-2-3',
                     'alternate1': 'TRMM-3B43v-7',
                     'alternate2': 'CMAP-V1902'},
              'prw': {'default': 'REMSS-PRW-v07r01'},
              'tas': {'default': 'ERA-INT',
                      'alternate2': 'JRA25',
                      'alternate1': 'ERA-40'},
              'psl': {'default': 'ERA-INT',
                      'alternate2': 'JRA25',
                      'alternate1': 'ERA-40'},
              'ua':  {'default': 'ERA-5',
                     'alternate1': 'ERA-INT',
                     'alternate3': 'JRA25',
                     'alternate2': 'ERA-40'},
              'va': {'default': 'ERA-INT',
                     'alternate2': 'JRA25',
                     'alternate1': 'ERA-40'},
              'uas': {'default': 'ERA-INT',
                      'alternate2': 'JRA25',
                      'alternate1': 'ERA-40'},
              'hus': {'default': 'ERA-INT',
                      'alternate2': 'JRA25',
                      'alternate1': 'ERA-40'},
              'vas': {'default': 'ERA-INT',
                      'alternate2': 'JRA25',
                      'alternate1': 'ERA-40'},
              'ta': {'default': 'ERA-INT',
                     'alternate2': 'JRA25',
                     'alternate1': 'ERA-40'},
              'zg': {'default': 'ERA-INT',
                     'alternate2': 'JRA25',
                     'alternate1': 'ERA-40'},
              'tauu': {'default': 'ERA-INT',
                       'alternate2': 'JRA25',
                       'alternate1': 'ERA-40'},
              'tauv': {'default': 'ERA-INT',
                       'alternate2': 'JRA25',
                       'alternate1': 'ERA-40'},
              'tos': {'default': 'UKMETOFFICE-HadISST-v1-1'},
              'zos': {'default': 'CNES-AVISO-L4'},
              'sos': {'default': 'NODC-WOA09'},
              'ts': {'default': 'HadISST1'},
              'thetao': {'default': 'WOA13v2',
                         'alternate1': 'UCSD',
                         'alternate2': 'Hosoda-MOAA-PGV',
                         'alternate3': 'IPRC'}
              }

obs_dic = {}

for filePath in lst:
    subp = filePath.split('/')
    template = filePath.split(data_path)[1]
    realm = subp[5]
    var = subp[7]
    product = subp[8]
    # Assign tableId
    if realm == 'atmos':
        tableId = 'Amon'
    elif realm == 'ocn':
        tableId = 'Omon'
    elif realm == 'fx':
        tableId = 'fx'
    print('tableId:', tableId)
    print('subp:', subp)
    print('var:', var)
    print('product:', product)

    fileName = subp[len(subp)-1]
    print('Filename:', fileName)
    # Fix rgd2.5_ac issue
    fileName = fileName.replace('rgd2.5_ac', 'ac')
    if '-clim' in fileName:
        period = fileName.split('_')[-1]
    # Fix durack1 formatted files
    elif 'sftlf_pcmdi-metrics_fx' in fileName:
        period = fileName.split('_')[-1]
        period = period.replace('.nc', '')
    else:
        period = fileName.split('_')[-1]
    period = period.replace('-clim.nc', '')  # .replace('ac.nc','')
    period = period.replace('.nc','')
    print('period:', period)

    # TRAP FILE NAME FOR OBS DATA
    if var not in list(obs_dic.keys()):
        obs_dic[var] = {}
    if product not in list(obs_dic[var].keys()) and os.path.isfile(filePath):
        obs_dic[var][product] = {}
        obs_dic[var][product]['template'] = template 
        obs_dic[var][product]['filename'] = fileName
#       obs_dic[var][product]['CMIP_CMOR_TABLE'] = tableId
        obs_dic[var][product]['period'] = period
        obs_dic[var][product]['RefName'] = product
        obs_dic[var][product]['RefTrackingDate'] = time.ctime(
            os.path.getmtime(filePath.strip()))
        md5 = os.popen('md5sum ' + filePath)
        md5 = md5.readlines()[0].split()[0]
        obs_dic[var][product]['MD5sum'] = md5
        f = cdms2.open(filePath)
        d = f(var)
        shape = d.shape
        f.close()
        shape = repr(d.shape)
        obs_dic[var][product]['shape'] = shape
        print('md5:', md5)
        print('')
        del(d, fileName)
        gc.collect()

    try:
        for r in list(obs_dic_in[var].keys()):
            # print '1',r,var,product
            # print obs_dic_in[var][r],'=',product
            if obs_dic_in[var][r] == product:
                # print '2',r,var,product
                obs_dic[var][r] = product
    except BaseException:
        pass
#del(filePath, lst, md5, period, product, r, realm, shape, subp, tableId, var)
#del(filePath, lst, md5, period, product, realm, shape, subp, tableId, var)

gc.collect()
# pdb.set_trace()

# ADD SPECIAL CASE SFTLF FROM TEST DIR
#product = 'UKMETOFFICE-HadISST-v1-1'
#var = 'sftlf'
#obs_dic[var][product] = {}
#obs_dic[var][product]['CMIP_CMOR_TABLE'] = 'fx'
#obs_dic[var][product]['shape'] = '(180, 360)'
#obs_dic[var][product]['filename'] = \
#    'sftlf_pcmdi-metrics_fx_UKMETOFFICE-HadISST-v1-1_198002-200501-clim.nc'
#obs_dic[var][product]['RefName'] = product
#obs_dic[var][product]['MD5sum'] = ''
#obs_dic[var][product]['RefTrackingDate'] = ''
#obs_dic[var][product]['period'] = '198002-200501'
#del(product, var)
#gc.collect()

# Save dictionary locally and in doc subdir
if datatype == 'clim':  json_name = pathout + 'pcmdiobs2_clims_catalogue_' + ver + '.json'
if datatype == 'timeSeries':  json_name = pathout + 'pcmdiobs_timeSeries_catalogue_' + ver + '.json'
if datatype == 'monthly':  json_name = pathout + 'pcmdiobs_monthly_catalogue_' + ver + '.json'
if datatype == 'day':  json_name = pathout + 'pcmdiobs_day_catalogue_' + ver + '.json'
if datatype == '3hr':  json_name = pathout + 'pcmdiobs_3hr_catalogue_' + ver + '.json'


json.dump(obs_dic, open(json_name, 'w'), sort_keys=True, indent=4,
          separators=(',', ': '))
#json.dump(obs_dic, open('../../../../doc/' + json_name, 'wb'), sort_keys=True,
#          indent=4, separators=(',', ': '))
