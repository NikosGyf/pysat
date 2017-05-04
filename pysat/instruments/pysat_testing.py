# -*- coding: utf-8 -*-
"""
Produces fake instrument data for testing.
"""

import pandas as pds
import numpy as np
import pysat

platform = 'pysat'
name = 'testing'

meta = pysat.Meta()
meta['uts'] = {'units':'s', 'long_name':'Universal Time'}
meta['mlt'] = {'units':'hours', 'long_name':'Magnetic Local Time'}
meta['slt'] = {'units':'hours', 'long_name':'Solar Local Time'}

        
def init(self):
    self.new_thing=True        
                
def load(fnames, tag=None, sat_id=None):
    # create an artifical satellite data set
    parts = fnames[0].split('/')
    yr = int('20'+parts[-1][0:2])
    month = int(parts[-3])
    day = int(parts[-2])
    date = pysat.datetime(yr,month,day)
    num = 86400 #int(tag)
    num_array = np.arange(num)
    uts = num_array
    data = pysat.DataFrame(uts, columns=['uts'])


    # need to create simple orbits here. Have start of first orbit 
    # at 2009,1, 0 UT. 14.84 orbits per day	
    time_delta = date  - pysat.datetime(2009,1,1) 
    uts_root = np.mod(time_delta.total_seconds(), 5820)
    mlt = np.mod(uts_root+num_array, 5820)*(24./5820.)
    data['mlt'] = mlt
    
    # fake orbit number, consistent with MLT
    fake_delta = date  - pysat.datetime(2008,1,1) 
    fake_uts_root = fake_delta.total_seconds()

    data['orbit_num'] = ((fake_uts_root+num_array)/5820.).astype(int)
    
    # create a fake longitude, resets every 6240 seconds
    # sat moves at 360/5820 deg/s, Earth rotates at 360/86400, takes extra time 
    # to go around full longitude
    longitude = np.mod(uts_root+num_array, 6240)*(360./6240.)
    data['longitude'] = longitude
    
    # do slt, 20 second offset from mlt
    uts_root = np.mod(time_delta.total_seconds()+20, 5820)
    data['slt'] = np.mod(uts_root+num_array, 5820)*(24./5820.)

    # create some fake data to support testing of averaging routines
    data['dummy1'] = data['mlt'].copy().astype(int)
    data['dummy2'] = (data['longitude']/15.).copy().astype(int)
    data['dummy3'] = data['mlt'].copy().astype(int) + (data['longitude']/15.).copy().astype(int)*1000.
    data['dummy4'] = num_array
    
        
    index = pds.date_range(date,date+pds.DateOffset(hours=23,minutes=59,seconds=59),freq='S')
    data.index=index
    data.index.name = 'time'
    return data, meta.copy()

def list_files(tag=None, sat_id=None, data_path=None, format_str=None):
    """Produce a fake list of files spanning a year"""
    
    index = pds.date_range(pysat.datetime(2008,1,1), pysat.datetime(2010,12,31)) 
    names = [ data_path+'/'+date.strftime('%D')+'.nofile' for date in index]
    return pysat.Series(names, index=index)
    
def download(date_array, tag, sat_id, data_path=None, user=None, password=None):
    pass
