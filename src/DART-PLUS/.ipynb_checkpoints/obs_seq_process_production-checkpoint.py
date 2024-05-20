import matplotlib.pyplot as plt
from pylab import *
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FormatStrFormatter
import sys
import os
import subprocess
import scipy.interpolate
from scipy.interpolate import interp1d
import math
from netCDF4 import Dataset as netcdf_dataset
import copy
from pathlib import Path

#wrf-python libs
import wrf
from wrf import to_np, vertcross, CoordPair
from matplotlib.cm import get_cmap


#########
#written by JMC
#plot obs from obs_sequence file 
#for diagnostic purposes
########


class obs_seq:
   def __init__(self,timestamp,obs_seq,custom='no',perfect_obs='no'):
      self.scriptsdir = (Path(__file__) / Path('../../../shell_scripts')).resolve()
      if (custom=='no'):
        procname = '{}/obs_seq.processed.{}.{}'.format(os.getcwd(),obs_seq,timestamp)
        path='/glade/scratch/jmccurry/WOF/realtime/OBSGEN/OBS_SEQ_OSSE/obs_seq.{}.{}'.format(obs_seq,timestamp)
      else:
        procname = '{}'.format(custom[0])
        path ='{}'.format(custom[1])
      if (perfect_obs=='no'):
        subprocess.call(['{}/process_obs_seq.sh'.format(self.scriptsdir),'{}'.format(path),'{}'.format(procname)])
      else:
        subprocess.call(['{}/process_obs_seq_truth.sh'.format(self.scriptsdir),'{}'.format(path),'{}'.format(procname)])
      self.data = np.loadtxt(procname,delimiter=',')     
      self.varnames = dict([('obs_type',0),('value',1),('vals',1),('X_loc',2),('Y_loc',3),('Z_loc',4),('QC',5),('obs_num',6),('radar_xloc',7),('radar_yloc',8),('second',10),('day',11),('oerror',12),('value2',13)])
      self.radar_locs = dict([('KVNX',[4.57053374392750,0.6412447157008800]),('KOAX',[4.601266986004480,0.7211764997633801]),('KEAX',[4.637959886345540,0.6773666343042200]),('KDVN',[4.702251524537250,0.7262606074423900])])
   def filter_data_type(self,obs_type_list):
      data_int = self.data.astype(int)
      if isinstance(obs_type_list,list):
        self.data =  self.data[np.where(np.isin(data_int[:,0],obs_type_list))] 
      else:
        self.data =  self.data[data_int[:,0]!=obs_type_list]
      return self 
   def filter_outliers(self,z,low_thresh,high_thresh):
      self.data[:,self.varnames[str(z)]][self.data[:,self.varnames[str(z)]]< low_thresh] = 'NaN'  
      self.data[:,self.varnames[str(z)]][self.data[:,self.varnames[str(z)]]> high_thresh] = 'NaN' 
      self.data = self.data[~np.isnan(self.data[:,self.varnames[str(z)]])]
      return self 
   def filter_radar_location(self,radar):
      self.data[:,self.varnames['radar_xloc']][self.data[:,self.varnames['radar_xloc']]!=self.radar_locs[radar][0]] = 'NaN'  
      self.data[:,self.varnames['radar_yloc']][self.data[:,self.varnames['radar_yloc']]!=self.radar_locs[radar][1]] = 'NaN'  
      self.data = self.data[~np.isnan(self.data[:,self.varnames['radar_xloc']])]
      self.data = self.data[~np.isnan(self.data[:,self.varnames['radar_yloc']])]
      return self 
        
class obs_seq_final:
   def __init__(self,timestamp,obs_seq,rundir='',forecast='no',outputmem='',member='no',custom='no'):
      self.iscopy = False
      self.scriptsdir = (Path(__file__) / Path('../../../shell_scripts')).resolve() 
      procname = '{}'.format(custom[0])
      path ='{}'.format(custom[1])
      subprocess.call(['{}/process_obs_final.sh'.format(self.scriptsdir),'{}'.format(path),'{}'.format(procname)])
      self.data = np.loadtxt(procname,delimiter=',')
      self.varnames = dict([('obs_type',0),('value',1),('vals',1),('X_loc',2),('Y_loc',3),('Z_loc',4),('QC',5),('obs_num',6),('prior',7),('post',8),('prior_sp',9),('post_sp',10),('obs_err',11),('priorA',7),('priorB',8),('priorC',9),('priorD',10),('priorE',11),('priorF',12),('priorG',13),('priorH',14),('priorI',15),('priorJ',16),('priorK',17),('priorL',18),('priorM',19),('priorN',20),('priorO',21),('priorP',22),('priorQ',23),('priorR',24),('priorS',25),('priorT',26)])
   def filter_data_QC(self,obs_type_list):
      return_obs = copy.deepcopy(self)
      return_obs.iscopy = True

      if self.iscopy==True:
          self.data=None
      data_int = return_obs.data.astype(int)
      if isinstance(obs_type_list,list):
        return_obs.data =  return_obs.data[np.where(np.isin(data_int[:,5],obs_type_list))]
        
      else:
        return_obs.data =  return_obs.data[data_int[:,5]==obs_type_list]
      return return_obs 
   def filter_data_type(self,obs_type_list):
      return_obs = copy.deepcopy(self)
      return_obs.iscopy = True

      if self.iscopy==True:
          self.data=None
      data_int = return_obs.data.astype(int)
      if isinstance(obs_type_list,list):
        return_obs.data =  return_obs.data[np.where(np.isin(data_int[:,0],obs_type_list))]

      else:
        return_obs.data =  return_obs.data[data_int[:,0]==obs_type_list]
      return return_obs
   def filter_outliers(self,z,low_thresh,high_thresh):
      return_obs = copy.deepcopy(self)
      return_obs.iscopy = True

      if self.iscopy==True:
          self.data=None
      return_obs.data[:,return_obs.varnames[str(z)]][return_obs.data[:,return_obs.varnames[str(z)]]< low_thresh] = 'NaN'  
      return_obs.data[:,return_obs.varnames[str(z)]][return_obs.data[:,return_obs.varnames[str(z)]]> high_thresh] = 'NaN'  
      return_obs.data = return_obs.data[~np.isnan(return_obs.data[:,return_obs.varnames[str(z)]])]
      return return_obs 
   def RMSE(self,mode):
     RMSE_out =np.sqrt(np.nanmean((self.data[:,self.varnames['value']]-self.data[:,self.varnames[str(mode)]])**2))
     return RMSE_out
   def TOT_ERR(self,mode):
      pass

def main():
   pass
if __name__ == "__main__":
    main()
