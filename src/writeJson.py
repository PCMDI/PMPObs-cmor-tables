#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 15:53:01 2018

Paul J. Durack 24th January 2018

This script generates all json files residing in this subdirectory

PJD 24 Jan 2018     - Started, copied from https://github.com/PCMDI/obs4MIPs-cmor-tables
PJD 25 Jan 2018     - First pass at complete tables etc, with institution_id and source_id entries to start
PJD 29 Jan 2018     - Updated product, realm and region format

@author: durack1
"""

#%% Import statements
import copy,gc,json,os,re,shutil,ssl,sys
import shutil 

#from durolib import readJsonCreateDict ; #getGitInfo

#from jsonFcns_py2 import readJsonCreateDict

#######################################################################
def readJsonCreateDict_dep(buildList):
    """
    Documentation for readJsonCreateDict(buildList):
    -------
    The readJsonCreateDict() function reads web-based json files and writes
    their contents to a dictionary in memory
    Author: Paul J. Durack : pauldurack@llnl.gov
    The function takes a list argument with two entries. The first is the
    variable name for the assigned dictionary, and the second is the URL
    of the json file to be read and loaded into memory. Multiple entries
    can be included by generating additional embedded lists
    Usage:
    ------

    Taken from Durolib to be used in PCMDIObs.  NEEDS TO BE CONVERTED TO PY3

        >>> from durolib import readJsonCreateDict
        >>> tmp = readJsonCreateDict([['Omon','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_Omon.json']])
        >>> Omon = tmp.get('Omon')
    Notes:
    -----
        ...
    """

    import os, json, ssl  #, urllib2   # urllib.request this is for PY3

#   import urllib2  # PY2
    import urllib.request  # PY3
    from urllib.request import urlopen #PY3

    # Test for list input of length == 2
    if len(buildList[0]) != 2:
        print('Invalid inputs, exiting..')
        sys.exit()
    # Create urllib2 context to deal with lab/LLNL web certificates
    ctx                 = ssl.create_default_context()
    ctx.check_hostname  = False
    ctx.verify_mode     = ssl.CERT_NONE
    # Iterate through buildList and write results to jsonDict
    jsonDict = {}
    for count,table in enumerate(buildList):
        #print 'Processing:',table[0]
        # Read web file
#       jsonOutput = urllib2.urlopen(table[1], context=ctx) # Py2
        jsonOutput = urlopen(table[1], context=ctx) # Py3
        tmp = jsonOutput.read()
        vars()[table[0]] = tmp
        jsonOutput.close()
        # Write local json
        tmpFile = open('tmp.json','w')
        tmpFile.write(eval(table[0]))
        tmpFile.close()
        # Read local json
        vars()[table[0]] = json.load(open('tmp.json','r'))
        os.remove('tmp.json')
        jsonDict[table[0]] = eval(table[0]) ; # Write to dictionary

    return jsonDict

def readJsonCreateDict(buildList):

    import os, json, ssl  #, urllib2   # urllib.request this is for PY3

#   import urllib2  # PY2
    import urllib.request  # PY3
    from urllib.request import urlopen #PY3

    # Test for list input of length == 2
    if len(buildList[0]) != 2:
        print('Invalid inputs, exiting..')
        sys.exit()
    # Create urllib2 context to deal with lab/LLNL web certificates
    ctx                 = ssl.create_default_context()
    ctx.check_hostname  = False
    ctx.verify_mode     = ssl.CERT_NONE
    # Iterate through buildList and write results to jsonDict
    jsonDict = {}
    for count,table in enumerate(buildList):
        print('Processing:',table[0])
        # Read web file
#       jsonOutput = urllib2.urlopen(table[1], context=ctx) # Py2
        jsonOutput = urlopen(table[1], context=ctx) # Py3
        tmp = jsonOutput.read()

#       vars()[table[0]] = tmp
#       jsonOutput.close()
#       # Write local json
#       tmpFile = open('tmp.json','w')
#       tmpFile.write(eval(table[0]))
#       tmpFile.close()
#       # Read local json
#       vars()[table[0]] = json.load(open('tmp.json','r'))
#       res = urllib.request.urlopen(pth)
#       res_body = res.read()
#       j = json.loads(res_body.decode("utf-8"))
#       os.remove('tmp.json')
 
        jsonDict[table[0]] = tmp #eval(table[0]) ; # Write to dictionary

    return jsonDict



#######################################################################





#%% Determine path
homePath = os.path.join('/','/'.join(os.path.realpath(__file__).split('/')[0:-1]))
#homePath = '/export/durack1/git/obs4MIPs-cmor-tables/' ; # Linux
#homePath = '/sync/git/PMPObs-cmor-tables/src' ; # OS-X
os.chdir(homePath)

#%% Create urllib2 context to deal with lab/LLNL web certificates
ctx                 = ssl.create_default_context()
ctx.check_hostname  = False
ctx.verify_mode     = ssl.CERT_NONE

#%% List target tables
masterTargets = [
 'Amon',
 'Aday',
 'A3hr',
 'Lmon',
 'Omon',
 'SImon',
 'fx',
 'coordinate',
 'formula_terms',
 'frequency',
 'grid_label',
 'grids',
 'institution_id',
 'license_',
 'nominal_resolution',
 'product',
 'realm',
 'region',
 'required_global_attributes',
 'source_id',
 'source_type',
 'table_id'
 ] ;

#%% Tables
tableSource = [
 ['coordinate','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_coordinate.json'],
 ['formula_terms','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_formula_terms.json'],
 ['frequency','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_frequency.json'],
 ['fx','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_fx.json'],
 ['grid_label','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_grid_label.json'],
 ['grids','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_grids.json'],
 ['nominal_resolution','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_nominal_resolution.json'],
 ['product','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/obs4MIPs_product.json'],
 ['nominal_resolution','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_nominal_resolution.json'],
 ['realm','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/obs4MIPs_realm.json'],
 ['region','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/obs4MIPs_region.json'],
 ['Amon','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_Amon.json'],
 ['Aday','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_Aday.json'],
 ['A3hr','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_A3hr.json'],
 ['Lmon','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_Lmon.json'],
 ['Omon','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_Omon.json'],
 ['SImon','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_SImon.json']
 ] ;

#%% Loop through tables and create in-memory objects
# Loop through tableSource and create output tables


tmp = readJsonCreateDict(tableSource)
tmpy = tmp
print(type(tmp))
print(tmp.keys())

#w = sys.stdin.readline()

for count,table in enumerate(tmp.keys()):
    #print('table:', table)
#   if table in ['frequency','grid_label','nominal_resolution','product',
#                'realm','region']:
#       vars()[table] = tmp[table].get(table)
#   else:
#       vars()[table] = tmp[table]
        vars()[table] = tmp[table]

del(tmp,count,table) ; gc.collect()

# Cleanup table_id values
'''
for table in ['Amon','Aday','A3hr','Lmon','Omon','SImon','fx']:
    eval(table)['Header']['table_id']  = ''.join(['Table PMPObs_',table]) ; # Cleanup from upstream
'''

#%% Coordinate

#%% Frequency

#%% Grid

#%% Grid label

#%% Institution
tmp = [['institution_id','https://raw.githubusercontent.com/PCMDI/PMPObs-cmor-tables/master/PMPObs_institution_id.json']
      ] ;
institution_id = readJsonCreateDict(tmp)
institution_id = institution_id.get('institution_id')

# Fix issues
#execfile('institution_ids.py')

exec(open("./institution_ids.py").read())


'''
List from https://goo.gl/GySZ56 to be updated
ERA-40/ECMWF
JRA-25/MRI
AIRS/?
MLS/?
CERES/?
GPCP/UofMD
TRMM/?
RSS/REMSS
ISCCP/?
MODIS/?
CALIPSO/?
WOA13v2/NOAA-NCEI
Hosoda/?
IPRC/?
UCSD/?
ERSSTv3b/NOAA-NCEI
GISTEMP/NASA-GISS
HadCRUT4.5/MOHC
Kaplan_Extended_V2/?
NOC1.1/NOC
OAFluxV3/WHOI
Aquarius/REMSS
SMOS/?
'''
#==============================================================================
# Example new institution_id entry
#institution_id['institution_id']['NOAA-NCEI'] = 'NOAA\'s National Centers for Environmental Information, Asheville, NC 28801, USA'
#institution_id['institution_id']['RSS'] = 'Remote Sensing Systems, Santa Rosa, CA 95401, USA'

#%% License
license_ = ('Data in this file produced by <Your Centre Name> is licensed under'
            ' a Creative Commons Attribution-ShareAlike 4.0 International License'
            ' (https://creativecommons.org/licenses/). Use of the data must be'
            ' acknowledged following guidelines found at <a URL maintained by you>.'
            ' Further information about this data, including some limitations,'
            ' can be found via <some URL maintained by you>.)')

#%% Nominal resolution

#%% Product

#%% Realm

#%% Region (taken from http://cfconventions.org/Data/cf-standard-names/docs/standardized-region-names.html)

#%% Required global attributes - # indicates source
required_global_attributes = [
 'Conventions',
 'activity_id',
 'contact',
 'creation_date',
 'data_specs_version',
 'frequency',
 'grid',
 'grid_label',
 'institution',
 'institution_id',
 'license',
 'nominal_resolution',
 'product',
 'realm',
 'source_id',
 'table_id',
 'tracking_id',
 'variable_id',
 'variant_label' # Not likely required
] ;

#%% Source ID
tmp = [['source_id','https://raw.githubusercontent.com/PCMDI/PMPObs-cmor-tables/master/PMPObs_source_id.json']
      ] ;
source_id = readJsonCreateDict(tmp)
source_id = source_id.get('source_id')

# Enter fixes or additions below

#execfile('source_ids.py')
exec(open("./source_ids.py").read())

'''
List from https://goo.gl/GySZ56 to be updated
ERA-40/ECMWF
ERA-Interim/ECMWF
JRA-25/MRI
AIRS/
MLS/
CERES/
GPCP/UofMD
TRMM/
RSS/REMSS
ISCCP/
MODIS/
CALIPSO/
WOA13v2/NOAA-NCEI
Hosoda/
IPRC
UCSD
ERSSTv3b
ERSSTv4
ERSSTv5
GISTEMP
HadCRUT4.5
HadISST1.1
HadSST3.1
Kaplan_Extended_V2
CMAP/UofMD
NOC1.1/NOC
OAFluxV3/WHOI
Aquarius/REMSS
SMOS
'''
#==============================================================================
# Example new source_id entry
#key = 'CMSAF-SARAH-2-0'
#source_id['source_id'][key] = {}
#source_id['source_id'][key]['source_description'] = 'Surface solAr RAdiation data set - Heliosat, based on MVIRI/SEVIRI aboard METEOSAT'
#source_id['source_id'][key]['institution_id'] = 'DWD'
#source_id['source_id'][key]['release_year'] = '2017'
#source_id['source_id'][key]['source_id'] = key
#source_id['source_id'][key]['source_label'] = 'CMSAF-SARAH'
#source_id['source_id'][key]['source_name'] = 'CMSAF SARAH'
#source_id['source_id'][key]['source_type'] = 'satellite_retrieval'
#source_id['source_id'][key]['region'] = list('africa','atlantic_ocean','europe')
#source_id['source_id'][key]['source_variables'] = list('rsds')
#source_id['source_id'][key]['source_version_number'] = '2.0'

key = "REMSS-PRW-v07r01"
source_id['source_id'][key] = {}
source_id['source_id'][key]['source_description'] = 'Monthly Average Precipitable Water over Ice-Free Oceans'
source_id['source_id'][key]['institution_id'] = 'RSS'
source_id['source_id'][key]['release_year'] = '2019'
source_id['source_id'][key]['source_id'] = key
source_id['source_id'][key]['source_label'] = 'REMSS-PRW'
source_id['source_id'][key]['source_name'] = 'REMSS PRW'
source_id['source_id'][key]['source_type'] = 'satellite_retrieval'
source_id['source_id'][key]['region'] = ['global_ocean']
source_id['source_id'][key]['source_variables'] = list('prw')
source_id['source_id'][key]['source_version_number'] = 'v07r01'


# Example rename source_id entry
#key = 'CMSAF-SARAH-2-0'
#source_id['source_id'][key] = {}
#source_id['source_id'][key] = source_id['source_id'].pop('CMSAF-SARAH-2.0')

# Example remove source_id entry
#key = 'CMSAF-SARAH-2.0'
#source_id['source_id'].pop(key)

# Test invalid chars
#key = 'CMSAF-SARAH-2 0' ; # Tested ".", “_”, “(“, “)”, “/”, and " "
#source_id['source_id'][key] = {}
#source_id['source_id'][key] = source_id['source_id'].pop('CMSAF-SARAH-2-0')

#%% Source type
source_type = {}
source_type['gridded_insitu'] = 'gridded product based on measurements collected from in-situ instruments'
source_type['reanalysis'] = 'gridded product generated from a model reanalysis based on in-situ instruments and possibly satellite measurements'
source_type['satellite_blended'] = 'gridded product based on both in-situ instruments and satellite measurements'
source_type['satellite_retrieval'] = 'gridded product based on satellite measurements'

#%% Table ID
table_id = [
  'PMPObs_Amon',
  'PMPObs_Aday',
  'PMPObs_A3hr',
  'PMPObs_Lmon',
  'PMPObs_Omon',
  'PMPObs_SImon',
  'PMPObs_fx'
] ;

#%% Validate entries
def entryCheck(entry,search=re.compile(r'[^a-zA-Z0-9-]').search):
    return not bool(search(entry))

# source_id
for key in source_id['source_id'].keys():
    # Validate source_id format
    if not entryCheck(key):
        print('Invalid source_id format for entry:',key,'- aborting')
        sys.exit()
    # Sort variable entries
    vals = source_id['source_id'][key]['source_variables']
    if not isinstance(vals,list):
        vals = list(vals); vals.sort()
    else:
        vals.sort()
    # Validate source_label format
    val = source_id['source_id'][key]['source_label']
    if not entryCheck(key):
        print('Invalid source_label format for entry:',key,'- aborting')
        sys.exit()
    # Validate source_type
    val = source_id['source_id'][key]['source_type']
    if val not in source_type:
        print('Invalid source_type for entry:',key,'- aborting')
        sys.exit()
    # Validate region
    vals = source_id['source_id'][key]['region']
    for val in vals:
        if val not in eval(region)['region']: #['region']:
            print('Invalid region for entry:',key,'- aborting')
            sys.exit()

Amon = eval(Amon)
Aday = eval(Aday)
A3hr = eval(A3hr)
Lmon = eval(Lmon)
Omon = eval(Omon)
SImon = eval(SImon)
fx = eval(fx)

for table in [Amon,Aday,A3hr,Lmon,Omon,SImon,fx]:
    if table == Amon: tname = 'Amon'
    if table == Aday: tname = 'Aday'
    if table == A3hr: tname = 'A3hr'
    if table == Lmon: tname = 'Lmon'
    if table == Omon: tname = 'Omon'
    if table == SImon: tname = 'SImon'
    if table == fx: tname = 'fx'

    table['Header']['table_id']  = ''.join(['Table PMPObs_',tname]) 


# Add new variables
# Variable sponsor - NOAA-NCEI; Jim Baird (JimBiardCics)
Amon['variable_entry'][u'rltcre'] = {}
Amon['variable_entry']['rltcre']['cell_measures'] = ''
Amon['variable_entry']['rltcre']['cell_methods'] = 'time: mean'
Amon['variable_entry']['rltcre']['comment'] = ''
Amon['variable_entry']['rltcre']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['rltcre']['frequency'] = 'mon'
Amon['variable_entry']['rltcre']['long_name'] = 'Top of Atmosphere Longwave CRE'
Amon['variable_entry']['rltcre']['ok_max_mean_abs'] = ''
Amon['variable_entry']['rltcre']['ok_min_mean_abs'] = ''
Amon['variable_entry']['rltcre']['out_name'] = 'rltcre'
Amon['variable_entry']['rltcre']['positive'] = ''
Amon['variable_entry']['rltcre']['standard_name'] = 'TOA_LW_cloud_forcing'
Amon['variable_entry']['rltcre']['type'] = 'real'
Amon['variable_entry']['rltcre']['units'] = 'W m-2'
Amon['variable_entry']['rltcre']['valid_max'] = ''
Amon['variable_entry']['rltcre']['valid_min'] = ''

# Add new variables
# Variable sponsor - NOAA-NCEI; Jim Baird (JimBiardCics)
Amon['variable_entry'][u'rstcre'] = {}
Amon['variable_entry']['rstcre']['cell_measures'] = ''
Amon['variable_entry']['rstcre']['cell_methods'] = 'time: mean'
Amon['variable_entry']['rstcre']['comment'] = ''
Amon['variable_entry']['rstcre']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['rstcre']['frequency'] = 'mon'
Amon['variable_entry']['rstcre']['long_name'] = 'Top of Atmosphere Shortwave CRE'
Amon['variable_entry']['rstcre']['ok_max_mean_abs'] = ''
Amon['variable_entry']['rstcre']['ok_min_mean_abs'] = ''
Amon['variable_entry']['rstcre']['out_name'] = 'rstcre'
Amon['variable_entry']['rstcre']['positive'] = ''
Amon['variable_entry']['rstcre']['standard_name'] = 'TOA_SW_cloud_forcing'
Amon['variable_entry']['rstcre']['type'] = 'real'
Amon['variable_entry']['rstcre']['units'] = 'W m-2'
Amon['variable_entry']['rstcre']['valid_max'] = ''
Amon['variable_entry']['rstcre']['valid_min'] = ''

# Add new variables
# Variable sponsor - NOAA-NCEI; Jim Baird (JimBiardCics)
Amon['variable_entry'][u'rt'] = {}
Amon['variable_entry']['rt']['cell_measures'] = ''
Amon['variable_entry']['rt']['cell_methods'] = 'time: mean'
Amon['variable_entry']['rt']['comment'] = ''
Amon['variable_entry']['rt']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['rt']['frequency'] = 'mon'
Amon['variable_entry']['rt']['long_name'] = 'Top of Atmosphere Net Radation'
Amon['variable_entry']['rt']['ok_max_mean_abs'] = ''
Amon['variable_entry']['rt']['ok_min_mean_abs'] = ''
Amon['variable_entry']['rt']['out_name'] = 'rt'
Amon['variable_entry']['rt']['positive'] = ''
Amon['variable_entry']['rt']['standard_name'] = 'Net_TOA_Radiation'
Amon['variable_entry']['rt']['type'] = 'real'
Amon['variable_entry']['rt']['units'] = 'W m-2'
Amon['variable_entry']['rt']['valid_max'] = ''
Amon['variable_entry']['rt']['valid_min'] = ''

# Add new variables
# Variable sponsor - PCMDI; PjG 
Amon['variable_entry'][u'hfns'] = {}
Amon['variable_entry']['hfns']['cell_measures'] = ''
Amon['variable_entry']['hfns']['cell_methods'] = 'time: mean'
Amon['variable_entry']['hfns']['comment'] = ''
Amon['variable_entry']['hfns']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['hfns']['frequency'] = 'mon'
Amon['variable_entry']['hfns']['long_name'] = 'Net Surface Energy'
Amon['variable_entry']['hfns']['ok_max_mean_abs'] = ''
Amon['variable_entry']['hfns']['ok_min_mean_abs'] = ''
Amon['variable_entry']['hfns']['out_name'] = 'hfns'
Amon['variable_entry']['hfns']['positive'] = ''
Amon['variable_entry']['hfns']['standard_name'] = 'Net_Surface_Energy'
Amon['variable_entry']['hfns']['type'] = 'real'
Amon['variable_entry']['hfns']['units'] = 'W m-2'
Amon['variable_entry']['hfns']['valid_max'] = ''
Amon['variable_entry']['hfns']['valid_min'] = ''

# Add new variables

Amon['variable_entry']['uaplev37_ERA5'] = {}
Amon['variable_entry']['uaplev37_ERA5']['cell_measures'] = ''
Amon['variable_entry']['uaplev37_ERA5']['cell_methods'] = 'time: mean'
Amon['variable_entry']['uaplev37_ERA5']['comment'] = ''
Amon['variable_entry']['uaplev37_ERA5']['dimensions'] = 'longitude latitude plev37_ERA5 time'
Amon['variable_entry']['uaplev37_ERA5']['frequency'] = 'mon'
Amon['variable_entry']['uaplev37_ERA5']['long_name'] = 'Eastward Wind'
Amon['variable_entry']['uaplev37_ERA5']['ok_max_mean_abs'] = ''
Amon['variable_entry']['uaplev37_ERA5']['ok_min_mean_abs'] = ''
Amon['variable_entry']['uaplev37_ERA5']['out_name'] = 'ua'
Amon['variable_entry']['uaplev37_ERA5']['positive'] = ''
Amon['variable_entry']['uaplev37_ERA5']['standard_name'] = 'eastward_wind'
Amon['variable_entry']['uaplev37_ERA5']['type'] = 'real'
Amon['variable_entry']['uaplev37_ERA5']['units'] = 'm s-1'
Amon['variable_entry']['uaplev37_ERA5']['valid_max'] = ''
Amon['variable_entry']['uaplev37_ERA5']['valid_min'] = ''

# Add new variables

Amon['variable_entry']['vaplev37_ERA5'] = {}
Amon['variable_entry']['vaplev37_ERA5']['cell_measures'] = ''
Amon['variable_entry']['vaplev37_ERA5']['cell_methods'] = 'time: mean'
Amon['variable_entry']['vaplev37_ERA5']['comment'] = ''
Amon['variable_entry']['vaplev37_ERA5']['dimensions'] = 'longitude latitude plev37_ERA5 time'
Amon['variable_entry']['vaplev37_ERA5']['frequency'] = 'mon'
Amon['variable_entry']['vaplev37_ERA5']['long_name'] = 'Northward Wind'
Amon['variable_entry']['vaplev37_ERA5']['ok_max_mean_abs'] = ''
Amon['variable_entry']['vaplev37_ERA5']['ok_min_mean_abs'] = ''
Amon['variable_entry']['vaplev37_ERA5']['out_name'] = 'va'
Amon['variable_entry']['vaplev37_ERA5']['positive'] = ''
Amon['variable_entry']['vaplev37_ERA5']['standard_name'] = 'northward_wind'
Amon['variable_entry']['vaplev37_ERA5']['type'] = 'real'
Amon['variable_entry']['vaplev37_ERA5']['units'] = 'm s-1'
Amon['variable_entry']['vaplev37_ERA5']['valid_max'] = ''
Amon['variable_entry']['vaplev37_ERA5']['valid_min'] = ''

# Add new variables

Amon['variable_entry']['zgplev37_ERA5'] = {}
Amon['variable_entry']['zgplev37_ERA5']['cell_measures'] = ''
Amon['variable_entry']['zgplev37_ERA5']['cell_methods'] = 'time: mean'
Amon['variable_entry']['zgplev37_ERA5']['comment'] = ''
Amon['variable_entry']['zgplev37_ERA5']['dimensions'] = 'longitude latitude plev37_ERA5 time'
Amon['variable_entry']['zgplev37_ERA5']['frequency'] = 'mon'
Amon['variable_entry']['zgplev37_ERA5']['long_name'] = 'Geopotential Height'
Amon['variable_entry']['zgplev37_ERA5']['ok_max_mean_abs'] = ''
Amon['variable_entry']['zgplev37_ERA5']['ok_min_mean_abs'] = ''
Amon['variable_entry']['zgplev37_ERA5']['out_name'] = 'zg'
Amon['variable_entry']['zgplev37_ERA5']['positive'] = ''
Amon['variable_entry']['zgplev37_ERA5']['standard_name'] = 'geopotential_height'
Amon['variable_entry']['zgplev37_ERA5']['type'] = 'real'
Amon['variable_entry']['zgplev37_ERA5']['units'] = 'm'
Amon['variable_entry']['zgplev37_ERA5']['valid_max'] = ''
Amon['variable_entry']['zgplev37_ERA5']['valid_min'] = ''

# Add new variables

Amon['variable_entry']['taplev37_ERA5'] = {}
Amon['variable_entry']['taplev37_ERA5']['cell_measures'] = ''
Amon['variable_entry']['taplev37_ERA5']['cell_methods'] = 'time: mean'
Amon['variable_entry']['taplev37_ERA5']['comment'] = ''
Amon['variable_entry']['taplev37_ERA5']['dimensions'] = 'longitude latitude plev37_ERA5 time'
Amon['variable_entry']['taplev37_ERA5']['frequency'] = 'mon'
Amon['variable_entry']['taplev37_ERA5']['long_name'] = 'Temperature'
Amon['variable_entry']['taplev37_ERA5']['ok_max_mean_abs'] = ''
Amon['variable_entry']['taplev37_ERA5']['ok_min_mean_abs'] = ''
Amon['variable_entry']['taplev37_ERA5']['out_name'] = 'ta'
Amon['variable_entry']['taplev37_ERA5']['positive'] = ''
Amon['variable_entry']['taplev37_ERA5']['standard_name'] = 'air_temperature'
Amon['variable_entry']['taplev37_ERA5']['type'] = 'real'
Amon['variable_entry']['taplev37_ERA5']['units'] = 'K'
Amon['variable_entry']['taplev37_ERA5']['valid_max'] = ''
Amon['variable_entry']['taplev37_ERA5']['valid_min'] = ''

'''
coordinate['plev37_ERA5'] = {}
coordinate['plev37_ERA5']['axis'] = 'Z'
coordinate['plev37_ERA5']['out_name'] = 'plev'
coordinate['plev37_ERA5']['standard_name']='air_pressure'
coordinate['plev37_ERA5']['long_name']='pressure'
coordinate['plev37_ERA5']['stored_direction']='decreasing'
coordinate['plev37_ERA5']['positive']='down'
coordinate['plev37_ERA5']['units']='Pa'
coordinate['plev37_ERA5']['bounds_values']= ''
coordinate['plev37_ERA5']['climatology']= ''
coordinate['plev37_ERA5']['generic_level_name']= ''
coordinate['plev37_ERA5']['must_have_bounds']= 'no'
coordinate['plev37_ERA5']['forumula']= ''
coordinate['plev37_ERA5']["requested_bounds"]=""
coordinate['plev37_ERA5']["standard_name"]="air_pressure"
coordinate['plev37_ERA5']["stored_direction"]="decreasing"
coordinate['plev37_ERA5']["tolerance"]=""
coordinate['plev37_ERA5']["type"]="double"
coordinate['plev37_ERA5']["units"]="Pa"
coordinate['plev37_ERA5']["valid_max"]=""
coordinate['plev37_ERA5']["valid_min"]=""
coordinate['plev37_ERA5']["value"]=""
coordinate['plev37_ERA5']["z_bounds_factors"]=""
coordinate['plev37_ERA5']["z_factors"]=""
coordinate['plev37_ERA5']['requested'] = [ "100000.", "97500.", "95000.", "92500.", "90000.", "87500.", "85000.", "82500.", "80000.", "77500.", "75000.", "70000.", "65000.", "60000.", "55000.", "50000.", "45000.", "40000.", "35000.", "30000.", "25000.", "22500.", "20000.", "17500.", "15000.", "12500.", "10000.", "7000.", "5000.", "3000.", "2000.", "1000.", "700.", "500.", "300.", "200.", "100."]
'''
 
#%% Write variables to files
for jsonName in masterTargets:
    # Clean experiment formats
    if jsonName  in []:  #['coordinate','grids']: #,'Amon','Lmon','Omon','SImon']:
        dictToClean = eval(jsonName)
        for key, value1 in dictToClean.iteritems():
            for value2 in value1.iteritems():
                string = dictToClean[key][value2[0]]
                if not isinstance(string, list) and not isinstance(string, dict):
                    string = string.strip() ; # Remove trailing whitespace
                    string = string.strip(',.') ; # Remove trailing characters
                    string = string.replace(' + ',' and ')  ; # Replace +
                    string = string.replace(' & ',' and ')  ; # Replace +
                    string = string.replace('   ',' ') ; # Replace '  ', '   '
                    string = string.replace('  ',' ') ; # Replace '  ', '   '
                    string = string.replace('anthro ','anthropogenic ') ; # Replace anthro
                    string = string.replace('decidous','deciduous') ; # Replace decidous
                dictToClean[key][value2[0]] = string
        vars()[jsonName] = dictToClean
    # Write file
    if jsonName in ['Aday', 'Amon','A3hr', 'Lmon', 'Omon', 'SImon', 'coordinate',
                    'formula_terms', 'fx', 'grids', 'monNobs', 'monStderr']:
        outFile = ''.join(['../Tables/PMPObs_',jsonName,'.json'])
    elif jsonName == 'license_':
        outFile = ''.join(['../PMPObs_license.json'])
    else:
        outFile = ''.join(['../PMPObs_',jsonName,'.json'])
    # Check file exists
    if os.path.exists(outFile):
        print('File existing, purging:',outFile)
        os.remove(outFile)
    if not os.path.exists('../Tables'):
        os.mkdir('../Tables')
    # Create host dictionary
    if jsonName == 'license_':
        jsonDict = {}
        jsonDict[jsonName.replace('_','')] = eval(jsonName)
    elif jsonName not in ['coordinate','formula_terms','fx','grids',
                          'institution_id','source_id','Aday','Amon','A3hr','Lmon',
                          'Omon','SImon']: #,'product','realm','region']:
        jsonDict = {}
        jsonDict[jsonName] = eval(jsonName)
    else:
        jsonDict = eval(jsonName)
    fH = open(outFile,'w')
    if jsonName in ['coordinate','formula_terms','grids']: jsonDict = eval(jsonDict)
    if jsonName in ['frequency']: jsonDict['frequency']  = eval(jsonDict['frequency'])
    if jsonName in ['grid_label']: jsonDict['grid_label']  = eval(jsonDict['grid_label'])
    if jsonName in ['nominal_resolution']: jsonDict['nominal_resolution']  = eval(jsonDict['nominal_resolution'])
    if jsonName in ['product']: jsonDict['product']  = eval(jsonDict['product'])
    if jsonName in ['realm']: jsonDict['realm']  = eval(jsonDict['realm'])
    if jsonName in ['region']: jsonDict['region']  = eval(jsonDict['region'])


    print('starting ', fH,' ', jsonDict.keys(),' ' ,type(jsonDict))

#   if jsonName in ['frequency']: jsonDict['frequency']
#   print('dumping ', fH,' ', jsonDict.keys())
#   json.dump(jsonDict,fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
    json.dump(jsonDict,fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'))
    print(fH,' ','DONE------------------')
    fH.close()

del(jsonName,outFile) ; gc.collect()

# Validate - only necessary if files are not written by json module

#%% Generate files for download and use
demoPath = os.path.join('/','/'.join(os.path.realpath(__file__).split('/')[0:-2]),'demo')
outPath = os.path.join(demoPath,'Tables')
if os.path.exists(outPath):
    shutil.rmtree(outPath) ; # Purge all existing
    os.makedirs(outPath)
else:
    os.makedirs(outPath)
os.chdir(demoPath)

# Integrate all controlled vocabularies (CVs) into master file - create obs4MIPs_CV.json
# List all local files
inputJson = ['frequency','grid_label','institution_id','license',
             'nominal_resolution','product','realm','region',
             'required_global_attributes','source_id','source_type','table_id', # These are controlled vocabs
             'coordinate','grids','formula_terms', # These are not controlled vocabs - rather lookup tables for CMOR
             'Amon','Lmon','Omon','SImon','fx' # Update/add if new tables are generated
            ]
tableList = ['Amon', 'Lmon', 'Omon', 'SImon', 'coordinate',
             'formula_terms', 'fx', 'grids']

# Load dictionaries from local files
CVJsonList = copy.deepcopy(inputJson)
CVJsonList.remove('coordinate')
CVJsonList.remove('grids')
CVJsonList.remove('formula_terms')
CVJsonList.remove('Amon')
CVJsonList.remove('Lmon')
CVJsonList.remove('Omon')
CVJsonList.remove('SImon')
CVJsonList.remove('fx')
for count,CV in enumerate(inputJson):
    if CV in tableList:
        path = '../Tables/'
    else:
        path = '../'
    vars()[CV] = json.load(open(''.join([path,'PMPObs_',CV,'.json'])))

# Build CV master dictionary


PMPObs_CV = {}
PMPObs_CV['CV'] = {}
for count,CV in enumerate(CVJsonList):
    # Create source entry from source_id
    if CV == 'source_id':
        source_id_ = source_id['source_id']
        PMPObs_CV['CV']['source_id'] = {}
        for key,values in source_id_.items():
            PMPObs_CV['CV']['source_id'][key] = {}
            string = ''.join([source_id_[key]['source_label'],' ',
                              source_id_[key]['source_version_number'],' (',
                              source_id_[key]['release_year'],'): ',
                              source_id_[key]['source_description']])
            PMPObs_CV['CV']['source_id'][key]['source_label'] = values['source_label']
            PMPObs_CV['CV']['source_id'][key]['source_type'] = values['source_type']
            PMPObs_CV['CV']['source_id'][key]['source_version_number'] = values['source_version_number']
            PMPObs_CV['CV']['source_id'][key]['region'] = ', '.join(str(a) for a in values['region'])
            PMPObs_CV['CV']['source_id'][key]['source'] = string
    # Rewrite table names
    elif CV == 'table_id':
        PMPObs_CV['CV']['table_id'] = []
        for value in table_id['table_id']:
            PMPObs_CV['CV']['table_id'].append(value)
    # Else all other CVs
    elif CV not in tableList:
        PMPObs_CV['CV'].update(eval(CV))
# Add static entries to obs4MIPs_CV.json
PMPObs_CV['CV']['activity_id'] = 'PMPObs'

# Dynamically update "data_specs_version": "2.0.0", in rssSsmiPrw-input.json
#print os.getcwd()
#versionInfo = getGitInfo('../demo/rssSsmiPrw-input.json')
#tagTxt = versionInfo[2]
#tagInd = tagTxt.find('(')
#tagTxt = tagTxt[0:tagInd].replace('latest_tagPoint: ','').strip()

# Write demo PMPObs_CV.json

for p in PMPObs_CV['CV'].keys():
  print(p,'  ',type(PMPObs_CV['CV'][p]))
# PMPObs_CV['CV'][p] = eval(PMPObs_CV['CV'][p])

if os.path.exists('Tables/PMPObs_CV.json'):
    print('File existing, purging:','PMPObs_CV.json')
    os.remove('Tables/PMPObs_CV.json')
fH = open('Tables/PMPObs_CV.json','w')
#json.dump(PMPObs_CV,fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
json.dump(PMPObs_CV,fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'))
fH.close()

# Write ../Tables obs4MIPs_CV.json
if os.path.exists('../Tables/PMPObs_CV.json'):
    print('File existing, purging:','PMPObs_CV.json')
    os.remove('../Tables/PMPObs_CV.json')
fH = open('../Tables/PMPObs_CV.json','w')
#json.dump(PMPObs_CV,fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
json.dump(PMPObs_CV,fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'))
fH.close()

# Loop and write all other files
os.chdir('Tables')
#tableList.extend(lookupList)
for count,CV in enumerate(tableList):
    outFile = ''.join(['PMPObs_',CV,'.json'])
    if os.path.exists(outFile):
        print('File existing, purging:',outFile)
        os.remove(outFile)
    fH = open(outFile,'w')
#   json.dump(eval(CV),fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
    json.dump(eval(CV),fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'))
    fH.close()

# Cleanup
del(coordinate,count,formula_terms,frequency,grid_label,homePath,institution_id,
    nominal_resolution,PMPObs_CV,product,realm,inputJson,tableList,
    required_global_attributes,table_id)


inpath = os.getcwd()
inpath = inpath.replace('demo/','')
outpath = inpath.replace('input','Tables')
shutil.copyfile(inpath + '/PMPObs_coordinate-AddNewLevsHere.json',outpath + '/PMPObs_coordinate.json')


#%% Generate zip archive
# Add machine local 7za to path - solve for @gleckler1
'''
env7za = os.environ.copy()
if os.environ.get('USER') == 'gleckler1':
    if 'oceanonly' in os.environ.get('HOSTNAME'):
        env7za['PATH'] = env7za['PATH'] + ':/export/durack1/bin/downloads/p7zip9.38.1/150916_build/p7zip_9.38.1/bin'
    elif 'crunchy' in os.environ.get('HOSTNAME'):
        env7za['PATH'] = env7za['PATH'] + ':/export/durack1/bin/downloads/p7zip9.20.1/130123_build/p7zip_9.20.1/bin'
    else:
        print 'No 7za path found'

# Cleanup rogue files
os.chdir(demoPath)
if os.path.exists('.DS_Store'):
    os.remove('.DS_Store')
if os.path.exists('demo.zip'):
    os.remove('demo.zip')
if os.path.exists('demo/demo.zip'):
    os.remove('demo/demo.zip')
if os.path.exists('../demo/demo.zip'):
    os.remove('../demo/demo.zip')
# Jump up one directory
os.chdir(demoPath.replace('/demo',''))
# Zip demo dir
p = subprocess.Popen(['7za','a','demo.zip','demo','tzip','-xr!demo/demo'],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         cwd=os.getcwd(),env=env7za)
stdout = p.stdout.read() ; # Use persistent variables for tests below
stderr = p.stderr.read()
# Move to demo dir
shutil.move('demo.zip', 'demo/demo.zip')
'''
