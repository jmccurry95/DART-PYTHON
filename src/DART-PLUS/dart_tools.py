#############################################################
import os
import sys
import glob
import numpy as np
import datetime as DT

# This flag adds an k/j/i index to the DART file, which is the index locations of the gridded data
_write_grid_indices = False


#=========================================================================================
# DART obs definitions (handy for writing out DART files)
def Oerror_LookUp(name,special_oerror='no'):
          if (special_oerror=='no'): 
                Look_Up_Oerror={ 'LAND_SFC_TEMPERATURE': 6.25,
                      "LAND_SFC_V_WIND_COMPONENT": 12.25,
                      "LAND_SFC_U_WIND_COMPONENT": 12.25,
                       "LAND_SFC_SPECIFIC_HUMIDITY": 0.2,
                      "LAND_SFC_ALTIMETER": 1.00,
                      "ACARS_U_WIND_COMPONENT": 6.25,
                      "ACARS_V_WIND_COMPONENT": 6.25,
                      "ACARS_TEMPERATURE": 1.00,
                       "METAR_U_10_METER_WIND": 12.25,
                       "METAR_V_10_METER_WIND": 12.25,
                      "METAR_ALTIMETER": 1.00,
                      "METAR_TEMPERATURE_2_METER": 6.25,
                      "METAR_SPECIFIC_HUMIDITY_2_METER": 1.2433972081762647E-005,
                      "ACARS_SPECIFIC_HUMIDITY": 0.2, 
                      "RADAR_REFLECTIVITY": 25.00,
                      "DOPPLER_RADIAL_VELOCITY": 9.00,
                      "RADAR_CLEARAIR_REFLECTIVITY": 25.00,
                      "RADIOSONDE_U_WIND_COMPONENT":  6.25,
                      "RADIOSONDE_V_WIND_COMPONENT":  6.25,
                      "RADIOSONDE_TEMPERATURE": 1.00     ,
                      "RADIOSONDE_SPECIFIC_HUMIDITY": 0.2, 
                      "RADIOSONDE_SURFACE_ALTIMETER": 4.00,
                         }
          elif (special_oerror=='yes'):
                Look_Up_Oerror={ 'LAND_SFC_TEMPERATURE': 1.00,
                      "LAND_SFC_V_WIND_COMPONENT": 6.25,
                      "LAND_SFC_U_WIND_COMPONENT": 6.25,
                       "LAND_SFC_SPECIFIC_HUMIDITY": 0.2,
                      "LAND_SFC_ALTIMETER": 1.00,
                      "ACARS_U_WIND_COMPONENT": 6.25,
                      "ACARS_V_WIND_COMPONENT": 6.25,
                      "ACARS_TEMPERATURE": 1.00,
                       "METAR_U_10_METER_WIND": 6.25,
                       "METAR_V_10_METER_WIND": 6.25,
                      "METAR_ALTIMETER": 1.00,
                      "METAR_TEMPERATURE_2_METER": 1.00,
                      "METAR_SPECIFIC_HUMIDITY_2_METER": 1.2433972081762647E-005,
                      "ACARS_SPECIFIC_HUMIDITY": 0.2, 
                      "RADAR_REFLECTIVITY": 25.00,
                      "DOPPLER_RADIAL_VELOCITY": 9.00,
                      "RADAR_CLEARAIR_REFLECTIVITY": 25.00,
                      "RADIOSONDE_U_WIND_COMPONENT":  6.25,
                      "RADIOSONDE_V_WIND_COMPONENT":  6.25,
                      "RADIOSONDE_TEMPERATURE": 1.00     ,
                      "RADIOSONDE_SPECIFIC_HUMIDITY": 0.2, 
                      "RADIOSONDE_SURFACE_ALTIMETER": 4.00,
                         }



          return Look_Up_Oerror[name]
        
def Tuned_Oerror_LookUp(name,representation_error='yes'):
          if (representation_error=='yes'):
                Look_Up_Oerror={ 'LAND_SFC_TEMPERATURE': 1.10,
                      "LAND_SFC_V_WIND_COMPONENT": 9.00,
                      "LAND_SFC_U_WIND_COMPONENT": 9.00,
                       "LAND_SFC_SPECIFIC_HUMIDITY": 0.0125,
                      "LAND_SFC_ALTIMETER": 1.00,
                      "ACARS_U_WIND_COMPONENT": 6.25,
                      "ACARS_V_WIND_COMPONENT": 6.25,
                      "ACARS_TEMPERATURE": 1.00,
                       "METAR_U_10_METER_WIND": 9.00,
                       "METAR_V_10_METER_WIND": 9.00,
                      "METAR_ALTIMETER": 1.00,
                      "METAR_TEMPERATURE_2_METER": 1.10,
                      "METAR_SPECIFIC_HUMIDITY_2_METER": 0.0125, 
                      "ACARS_SPECIFIC_HUMIDITY": 0.0125,
                      "RADAR_REFLECTIVITY": 6.25,
                      "DOPPLER_RADIAL_VELOCITY": 2.25,
                      "RADAR_CLEARAIR_REFLECTIVITY": 25.00,
                      "RADIOSONDE_U_WIND_COMPONENT":  6.25,
                      "RADIOSONDE_V_WIND_COMPONENT":  6.25,
                      "RADIOSONDE_TEMPERATURE": 1.00     ,
                      "RADIOSONDE_SPECIFIC_HUMIDITY": 0.0125,
                      "RADIOSONDE_SURFACE_ALTIMETER": 4.00,
                         }
          elif (representation_error=='no'):
                Look_Up_Oerror={ 'LAND_SFC_TEMPERATURE': 1.0,
                      "LAND_SFC_V_WIND_COMPONENT": 6.25,
                      "LAND_SFC_U_WIND_COMPONENT": 6.25,
                       "LAND_SFC_SPECIFIC_HUMIDITY": 0.0125,
                      "LAND_SFC_ALTIMETER": 1.00,
                      "ACARS_U_WIND_COMPONENT": 6.25,
                      "ACARS_V_WIND_COMPONENT": 6.25,
                      "ACARS_TEMPERATURE": 1.00,
                       "METAR_U_10_METER_WIND": 6.25,
                       "METAR_V_10_METER_WIND": 6.25,
                      "METAR_ALTIMETER": 1.00,
                      "METAR_TEMPERATURE_2_METER": 1.0,
                      "METAR_SPECIFIC_HUMIDITY_2_METER": 0.0125, 
                      "ACARS_SPECIFIC_HUMIDITY": 0.0125,
                      "RADAR_REFLECTIVITY": 6.25,
                      "DOPPLER_RADIAL_VELOCITY": 2.25,
                      "RADAR_CLEARAIR_REFLECTIVITY": 25.00,
                      "RADIOSONDE_U_WIND_COMPONENT":  6.25,
                      "RADIOSONDE_V_WIND_COMPONENT":  6.25,
                      "RADIOSONDE_TEMPERATURE": 1.00     ,
                      "RADIOSONDE_SPECIFIC_HUMIDITY": 0.0125,
                      "RADIOSONDE_SURFACE_ALTIMETER": 4.00
                         }
          return Look_Up_Oerror[name]
def ObType_LookUp(name,DART_name=False,Print_Table=False,reverse=False):
      """ObType_LookUp returns the DART kind number for an input variable type.  There seems
         to be several ways observations names are written in the observation inputs
         and output files, e.g., in the DART ascii files and in the ***.obs.nc files,
         so this function is designed to handle the variety of cases and return the
         integer corresponding to the DART definitionp.
      
         Exampled:   REFLECTIVITY is sometimes stored as REFL
                     T_2M         is sometimes stored as TEMP2m
                     TD_2M        is sometimes stored as DEWPT2m
      
         If you come across a variable that is not defined, you can add it to the lookup
         table (dictionary) below - just make sure you know the official DART definition
         
         You can add any unique variable name or reference on the left column, and then use
         the pyDART INTERNAL definition on the right - so that you can refer to more than
         one type of data in different ways internally in this code
      
         Usage:  variable_kind = ObType_Lookup(variable_name)   where type(variable_name)=str
      
         If you need the return the actual DART_name as well, set the input flag to be True"""

# Create local dictionary for observation kind definition - these can include user abbreviations

#                      user's observation type            kind   DART official name

      Look_Up_Table={ "DOPPLER_VELOCITY":                 [164,   "DOPPLER_RADIAL_VELOCITY"] ,
                      "UNFOLDED VELOCITY":                [164,   "DOPPLER_RADIAL_VELOCITY"] ,
                      "VELOCITY":                         [164,   "DOPPLER_RADIAL_VELOCITY"] ,
                      "DOPPLER_RADIAL_VELOCITY":          [164,   "DOPPLER_RADIAL_VELOCITY"] ,
                      "REFLECTIVITY":                     [165,   "RADAR_REFLECTIVITY"],
                      "RADAR_REFLECTIVITY":               [165,   "RADAR_REFLECTIVITY"],
                      "RADAR_CLEARAIR_REFLECTIVITY":      [166,   "RADAR_CLEARAIR_REFLECTIVITY"],  
                      "CLEARAIR_REFLECTIVITY":            [166,   "RADAR_CLEARAIR_REFLECTIVITY"],
                      "METAR_U_10_METER_WIND":            [93,    "METAR_U_10_METER_WIND"],
                      "METAR_V_10_METER_WIND":            [94,    "METAR_V_10_METER_WIND"],
                      "METAR_TEMPERATURE_2_METER":        [95,    "METAR_TEMPERATURE_2_METER"],
                      "METAR_DEWPOINT_2_METER":           [96,    "METAR_DEWPOINT_2_METER"],
                      "VR":                               [164,   "DOPPLER_RADIAL_VELOCITY"],
                      "DBZ":                              [165,   "RADAR_REFLECTIVITY"],
                      "0DBZ":                             [166,   "RADAR_CLEARAIR_REFLECTIVITY"],
                      "U10M":                             [93,    "METAR_U_10_METER_WIND"],
                      "V10M":                             [94,    "METAR_V_10_METER_WIND"],
                      "T2M":                              [95,    "METAR_TEMPERATURE_2_METER"],
                      "TD2M":                             [96,    "METAR_DEWPOINT_2_METER"],
                      "U_10M":                            [93,    "METAR_U_10_METER_WIND"],
                      "V_10M":                            [94,    "METAR_V_10_METER_WIND"],
                      "T_2M":                             [95,    "METAR_TEMPERATURE_2_METER"],
                      "TD_2M":                            [96,    "DEW_POINT_2_METER"],
                      "TEMP2M":                           [95,    "METAR_TEMPERATURE_2_METER"],
                      "DEWPT2M":                          [96,    "DEW_POINT_2_METER"],
                      "REFL":                             [165,   "REFLECTIVITY"],
                      "METAR_ALTIMETER":                  [24,    "METAR_ALTIMETER"],
                      "LAND_SFC_ALTIMETER":               [23,    "LAND_SFC_ALTIMETER"],
                      "LAND_SFC_TEMPERATURE":             [194,   "LAND_SFC_TEMPERATURE"],
                      "LAND_SFC_U_WIND_COMPONENT":        [192,   "LAND_SFC_U_WIND_COMPONENT"],
                      "LAND_SFC_V_WIND_COMPONENT":        [193,   "LAND_SFC_V_WIND_COMPONENT"],
                      "LAND_SFC_SPECIFIC_HUMIDITY":       [195,   "LAND_SFC_SPECIFIC_HUMIDITY"],
                      "ACARS_U_WIND_COMPONENT":           [183,   "ACARS_U_WIND_COMPONENT"],
                      "ACARS_V_WIND_COMPONENT":           [184,   "ACARS_V_WIND_COMPONENT"],
                      "ACARS_TEMPERATURE":                [185,   "ACARS_TEMPERATURE"],
                      "ACARS_SPECIFIC_HUMIDITY":          [186,   "ACARS_SPECIFIC_HUMIDITY"],
                      "RADIOSONDE_U_WIND_COMPONENT":      [1,     "RADIOSONDE_U_WIND_COMPONENT"],
                      "RADIOSONDE_V_WIND_COMPONENT":      [2,     "RADIOSONDE_V_WIND_COMPONENT"],
                      "RADIOSONDE_TEMPERATURE":           [5,     "RADIOSONDE_TEMPERATURE"],
                      "RADIOSONDE_SPECIFIC_HUMIDITY":     [6,     "RADIOSONDE_SPECIFIC_HUMIDITY"],
                      "RADIOSONDE_SURFACE_ALTIMETER":     [71,     "RADIOSONDE_SURFACE_ALTIMETER"],
                    }
      Reverse_Look_Up_Table={'164':         [164,   "DOPPLER_RADIAL_VELOCITY"] ,
                      '165':                     [165,   "RADAR_REFLECTIVITY"],
                      '166':      [166,   "RADAR_CLEARAIR_REFLECTIVITY"],  
                      '93':            [93,    "METAR_U_10_METER_WIND"],
                      '94':            [94,    "METAR_V_10_METER_WIND"],
                      '95':        [95,    "METAR_TEMPERATURE_2_METER"],
                      '96':           [96,    "METAR_SPECIFIC_HUMIDITY_2_METER"],
                      '24':                  [24,    "METAR_ALTIMETER"],
                      '23':               [23,    "LAND_SFC_ALTIMETER"],
                      '194':             [194,   "LAND_SFC_TEMPERATURE"],
                      '192':        [192,   "LAND_SFC_U_WIND_COMPONENT"],
                      '193':        [193,   "LAND_SFC_V_WIND_COMPONENT"],
                     '195':       [195,   "LAND_SFC_SPECIFIC_HUMIDITY"],
                      '183':           [183,   "ACARS_U_WIND_COMPONENT"],
                      '184':           [184,   "ACARS_V_WIND_COMPONENT"],
                      '185':                [185,   "ACARS_TEMPERATURE"],
                      '186':          [186,   "ACARS_SPECIFIC_HUMIDITY"],
                       '36':         [36,   "DOPPLER_RADIAL_VELOCITY"] ,
                      '37':                     [37,   "RADAR_REFLECTIVITY"],
                      '38':      [38,   "RADAR_CLEARAIR_REFLECTIVITY"],  
                      '40':            [40,    "METAR_U_10_METER_WIND"],
                      '41':            [41,    "METAR_V_10_METER_WIND"],
                      '42':        [42,    "METAR_TEMPERATURE_2_METER"],
                      '43':           [43,    "METAR_SPECIFIC_HUMIDITY_2_METER"],
                      '75':                  [75,    "METAR_ALTIMETER"],
                      '74':               [74,    "LAND_SFC_ALTIMETER"],
                      '27':             [27,   "LAND_SFC_TEMPERATURE"],
                      '25':        [25,   "LAND_SFC_U_WIND_COMPONENT"],
                      '26':        [26,   "LAND_SFC_V_WIND_COMPONENT"],
                     '28':       [28,   "LAND_SFC_SPECIFIC_HUMIDITY"],
                      '16':           [16,   "ACARS_U_WIND_COMPONENT"],
                      '17':           [17,   "ACARS_V_WIND_COMPONENT"],
                      '18':                [18,   "ACARS_TEMPERATURE"], 
                      '19':          [19,   "ACARS_SPECIFIC_HUMIDITY"],
                      '1':      [1,     "RADIOSONDE_U_WIND_COMPONENT"],
                      '2':      [2,     "RADIOSONDE_V_WIND_COMPONENT"],
                      '5':           [5,     "RADIOSONDE_TEMPERATURE"],
                      '6':     [6,     "RADIOSONDE_SPECIFIC_HUMIDITY"],
                      '71':     [71,     "RADIOSONDE_SURFACE_ALTIMETER"],
                      '168':     [1,     "RADIOSONDE_U_WIND_COMPONENT"],
                      '169':     [2,     "RADIOSONDE_V_WIND_COMPONENT"],
                      '172':     [5,     "RADIOSONDE_TEMPERATURE"],
                      '173':     [6,     "RADIOSONDE_SPECIFIC_HUMIDITY"],
                       '20':     [71,     "RADIOSONDE_SURFACE_ALTIMETER"],
                      

                    }     

      if Print_Table:
            print()
            print("VALID INPUT VARIABLE NAME              KIND  DART NAME")
            print("==========================================================================")
            for key in list(Look_Up_Table.keys()):
                  print("%35s    %3d    %s" % (key, Look_Up_Table[key][0], Look_Up_Table[key][1]))
            return
      
      name2 = name.upper().strip()
      
      if (reverse==False):
          if name2 in Look_Up_Table:
                if DART_name == True:
                      return Look_Up_Table[name2][0], Look_Up_Table[name2][1]
                else:
                     return Look_Up_Table[name2][0]
          else:
                print("ObType_LookUp cannot find variable:  ", name, name2)
                raise SystemExit
      else:
          if name2 in Reverse_Look_Up_Table:
                if DART_name == True:
                      return Reverse_Look_Up_Table[name2][0], Reverse_Look_Up_Table[name2][1]
                else:
                     return Reverse_Look_Up_Table[name2][0]        
          else:
                print("ObType_LookUp cannot find variable:  ", name, name2)
                raise SystemExit

########################################################################

def beam_elv(sfc_range, z):

########################################################################
#
#     PURPOSE:
#
#     Calculate the elevation angle (elvang) and the along
#     ray-path distance (range) of a radar beam
#     crossing through the given height and along-ground
#     distance.
#
#     This method assumes dn/dh is constant such that the
#     beam curves with a radius of 4/3 of the earth's radius.
#     This is dervied from Eq. 2.28 of Doviak and Zrnic',
#     Doppler Radar and Weather Observations, 1st Ed.
#
########################################################################
#
#     AUTHOR: Keith Brewster
#     10/10/95
#
#     MODIFICATION HISTORY: adapted to python by Lou Wicker (thanks Keith)
#
########################################################################
#
#     INPUT:
#       sfc_range:    Distance (meters) along ground from radar 
#       z        :    Height above radar
#
#     OUTPUT
#       elvang   Elevation angle (degrees) of radar beam
#
########################################################################
    eradius=6371000.
    frthrde=(4.*eradius/3.)
    eighthre=(8.*eradius/3.)
    fthsq=(frthrde*frthrde)

    if sfc_range > 0.0:
        hgtdb = frthrde + z
        rngdb = sfc_range/frthrde

        elvrad = np.arctan((hgtdb*np.cos(rngdb) - frthrde)/(hgtdb * np.sin(rngdb)))

        return np.rad2deg(elvrad)

    else:

        return -999.

####################################################################################### 
#
# write_DART_ascii is a program to dump radar data to DART ascii files.
#
# Usage: 
#
#   obs:  a gridded data object (described below)
#
#   fsuffix:  a string containing a label for the radar fields
#             the string "obs_seq" will be prepended, and
#             the filename will have ".txt" appended after fsuffix.
#             If fsuffix is not supplied, data will be write to
#             "obs_seq.txt".
#
#   obs_error:  the observation error for the field (2 m/s, 5 dbz)
#               this is NOT the variance, the stddev!
#               YOU MUST SPECIFY the obs_error, or program will quit.
#
#   obs object spec:  The obs object must have the following  attributes...
#
#       obs.data:       3D masked numpy array of radar data on a grid.
#                       missing data are filled with  np.nan, and mask=True
#                       for those points.
#
#       obs.data.mask:  the 3D mask for data array (part of np.ma.array)
#
#       obs.field:  string name of field (valid:  "reflectivity", "velocity") 
#
#       obs.lats/lons:  2D numpy arrays of lats and lons of horizontal grid 
#                       locations in degrees.
#
#       obs.hgts:  3D array of heights in meters AGL.
#
#       obs.radar_hgt:  height of radar in meters above MSL
#
#       obs.time:  a dictorary having {'data': an array containing time in seconds, size could be=1  
#                                      'units': a calender reference for datatime calcs}
#                  example:  data: array([   0.535,    0.56 ,    0.582,...])
#                            units: 'seconds since 2013-05-31T23:55:56Z'
# 
#  -->  for radial velocity, more metadata is needed
#
#        obs.nyquist:  a 1D array of dimension z, containing nyquist velo for each tilt
#
#        obs.radar_lat:  latitude of radar
#        obs.radar_lon:  longitude of radar
#
#        obs.xg:  1D array of x-distance of grid point from radar
#        obs.yg:  1D array of y-distance of grid point from radar
#
#
########################################################################################  
def write_DART_ascii(obs, filename=None, obs_error=None, zero_dbz_obtype=True, grid_dict=None):

  if filename == None:
      print(("\n write_DART_ascii:  No output file name is given, writing to %s" % "obs_seq.txt"))
      filename = "obs_seq.out"
  else:
      dirname = os.path.dirname(filename)
      basename = "%s_%s.out" % ("obs_seq", os.path.basename(filename))
      filename =  os.path.join(dirname, basename)
      
  if obs_error == None:
      print("write_DART_ascii:  No obs error defined for observation, exiting")
      raise SystemExit

# Open ASCII file for DART obs to be written into.  We will add header info afterward
  
  fi = open(filename, "w")
  
# This is why I love python - they think of everything.  Here Numpy has an interator over 
#      an array, and it will extract the indices for you automatically..so create a single 
#      loop over a MD array is very simple....

  print(("\n Writing %s to file...." % obs.field.upper()))
    
  data       = obs.data
  lats       = np.radians(obs.lats)
  lons       = np.radians(obs.lons)
  hgts       = obs.zg + obs.radar_hgt
  vert_coord = 3
  kind       = ObType_LookUp(obs.field.upper())
  truth      = 1.0  # dummy variable

# Fix the negative lons...

  lons       = np.where(lons > 0.0, lons, lons+(2.0*np.pi))

# extra information

  if kind == ObType_LookUp("VR"):
      platform_nyquist    = obs.nyquist
      platform_lat        = np.radians(obs.radar_lat)
      platform_lon        = np.radians(obs.radar_lon)
      platform_hgt        = obs.radar_hgt
      platform_key        = 1
      platform_vert_coord = 3
  else:
      try:
          nz, ny, nx        = data.shape
          new_data          = np.ma.zeros((nz+2, ny, nx), dtype=np.float32)
          new_hgts          = np.ma.zeros((nz+2, ny, nx), dtype=np.float32)
          new_data[0:nz]    = data[0:nz]
          new_hgts[0:nz]    = hgts[0:nz]
          new_data[nz]      = obs.zero_dbz
          new_data[nz+1]    = obs.zero_dbz
          new_hgts[nz:nz+2] = obs.zero_dbz_zg[0:2]
          data = new_data
          hgts = new_hgts
          print("\n write_DART_ascii:  0-DBZ separate type added to reflectivity output\n")
      except AttributeError:
          print("\n write_DART_ascii:  No 0-DBZ separate type found\n")

# Set up the time stamping for dat
      
  vol_time = DT.datetime.strptime(obs.time['units'], "seconds since %Y-%m-%dT%H:%M:%SZ")
  dt_time  = vol_time - DT.datetime(1601,1,1,0,0,0)
  
# Print the number of value gates

#  mask_check = data.mask && numpy.isnan().any()

  data_length = np.sum(data.mask[:]==False)
  print(("\n Number of good observations:  %d" % data_length))
  
# Create a multidimension iterator to move through 3D array creating obs
 
  it = np.nditer(data, flags=['multi_index'])
  nobs = 0
  nobs_clearair = 0

  while not it.finished:
      k = it.multi_index[0]
      j = it.multi_index[1]
      i = it.multi_index[2]
      
      if data.mask[k,j,i] == True:   # bad values
          pass
      else:          
          nobs += 1

# time of observations is the mean time of each sweep
          
          try:
              sw_time = dt_time + DT.timedelta(seconds=obs.sweep_time[k])
          except:
              sw_time = dt_time + DT.timedelta(seconds=obs.sweep_time.max())

          days    = sw_time.days
          seconds = sw_time.seconds
  
          if _write_grid_indices:
              fi.write(" OBS            %d     %d     %d    %d\n" % (nobs,k,j,i) )
          else:
              fi.write(" OBS            %d\n" % (nobs) )
              
          fi.write("   %20.14f\n" % data[k,j,i]  )
          fi.write("   %20.14f\n" % truth )
            
          if nobs == 1: 
              fi.write(" %d %d %d\n" % (-1, nobs+1, -1) ) # First obs.
          elif nobs == data_length:
              fi.write(" %d %d %d\n" % (nobs-1, -1, -1) ) # Last obs.
          else:
              fi.write(" %d %d %d\n" % (nobs-1, nobs+1, -1) ) 
      
          fi.write("obdef\n")
          fi.write("loc3d\n")

          fi.write("    %20.14f          %20.14f          %20.14f     %d\n" % 
                  (lons[i], lats[j], hgts[k,j,i], vert_coord))
      
          fi.write("kind\n")

# If we created zeros, and 0dbz_obtype == True, write them out as a separate data type
# IF MRMS_zeros == True, we assume that is what you want anyway.

          if (kind == ObType_LookUp("REFLECTIVITY") and data[k,j,i] <= 0.1) and \
             (grid_dict['0dbz_obtype'] or grid_dict['MRMS_zeros'][0]):
             
              fi.write("     %d     \n" % ObType_LookUp("RADAR_CLEARAIR_REFLECTIVITY") )
              nobs_clearair += 1
              o_error = obs_error[1]
          else:     
              fi.write("     %d     \n" % kind )
              o_error = obs_error[0]

# If this GEOS cloud pressure observation, write out extra information (NOTE - NOT TESTED FOR HDF2ASCII LJW 04/13/15)
# 
#       if kind == ObType_LookUp("GOES_CWP_PATH"):
#           fi.write("    %20.14f          %20.14f  \n" % (row["satellite"][0], row["satellite"][1]) )
#           fi.write("    %20.14f  \n" % (row["satellite"][2]) )

# Check to see if its radial velocity and add platform informationp...need BETTER CHECK HERE!
      
          if kind == ObType_LookUp("VR"):
          
              R_xy            = np.sqrt(obs.xg[i]**2 + obs.yg[j]**2)
              elevation_angle = beam_elv(R_xy, obs.zg[k,j,i])

              platform_dir1 = (obs.xg[i] / R_xy) * np.cos(np.deg2rad(elevation_angle))
              platform_dir2 = (obs.yg[j] / R_xy) * np.cos(np.deg2rad(elevation_angle))
              platform_dir3 = np.sin(np.deg2rad(elevation_angle))
              
              fi.write("platform\n")
              fi.write("loc3d\n")

              if platform_lon < 0.0:  platform_lon = platform_lon+2.0*np.pi

              fi.write("    %20.14f          %20.14f        %20.14f    %d\n" % 
                      (platform_lon, platform_lat, platform_hgt, platform_vert_coord) )
          
              fi.write("dir3d\n")
          
              fi.write("    %20.14f          %20.14f        %20.14f\n" % (platform_dir1, platform_dir2, platform_dir3) )
              fi.write("    %20.14f     \n" % obs.nyquist[k] )
              fi.write("    %d          \n" % platform_key )

    # Done with special radial velocity obs back to dumping out time, day, error variance info
      
          fi.write("    %d          %d     \n" % (seconds, days) )

    # Logic for command line override of observational error variances

          fi.write("    %20.14f  \n" % o_error**2 )

          if nobs % 1000 == 0: print((" write_DART_ascii:  Processed observation # %d" % nobs))
  
      it.iternext()
      
  fi.close()
  
# To write out header information AFTER we know how big the observation data set is, we have
# to read back in the entire contents of the obs-seq file, store it, rewrite the file
# with header information first, and then dump the contents of obs-seq back inp.  Yuck.

  with open(filename, 'r') as f: f_obs_seq = f.read()

  fi = open(filename, "w")
  
  fi.write(" obs_sequence\n")
  fi.write("obs_kind_definitions\n")

# Deal with case that for reflectivity, 2 types of observations might have been created


  if kind == ObType_LookUp("REFLECTIVITY") and zero_dbz_obtype and nobs_clearair > 0:
      fi.write("       %d\n" % 2)
      akind, DART_name = ObType_LookUp(obs.field.upper(), DART_name=True)
      fi.write("    %d          %s   \n" % (akind, DART_name) )
      akind, DART_name = ObType_LookUp("RADAR_CLEARAIR_REFLECTIVITY", DART_name=True) 
      fi.write("    %d          %s   \n" % (akind, DART_name) )
  else:
      fi.write("       %d\n" % 1)
      akind, DART_name = ObType_LookUp(obs.field.upper(), DART_name=True)
      fi.write("    %d          %s   \n" % (akind, DART_name) )

  fi.write("  num_copies:            %d  num_qc:            %d\n" % (1, 1))
  
  fi.write(" num_obs:       %d  max_num_obs:       %d\n" % (nobs, nobs) )
      
  fi.write("observations\n")
  fi.write("QC radar\n")
          
  fi.write("  first:            %d  last:       %d\n" % (1, nobs) )

# Now write back in all the actual DART obs data

  fi.write(f_obs_seq)
  
  fi.close()
  
  print(("\n write_DART_ascii:  Created ascii DART file, N = %d written" % nobs))
  
  if kind == ObType_LookUp("REFLECTIVITY") and zero_dbz_obtype and nobs_clearair > 0:
      print((" write_DART_ascii:  Number of clear air obs:             %d" % nobs_clearair))
      print((" write_DART_ascii:  Number of non-zero reflectivity obs: %d" % (nobs - nobs_clearair)))

  return
  
#####################################################################################################
def insert_DART_ascii_direct_conventional(data,truth,lats,lons,z,days_in,seconds_in,kind,oerror,obnum_insert,obnum_last,infile,outfile,zero_dbz_obtype=True, grid_dict=None,conventional=True):
    

  dirname = os.path.dirname(outfile)
  temp_basename = "%s_%s" % (os.path.basename(outfile),"temp")
  step1 = os.path.join(dirname,temp_basename)

  
      

# Open ASCII file for DART obs to be written into.  We will add header info afterward
  
  fi = open(step1, "w")
  
# This is why I love python - they think of everything.  Here Numpy has an interator over 
#      an array, and it will extract the indices for you automatically..so create a single 
#      loop over a MD array is very simple....

    
  
  #lats       = np.radians(lats)
  #lons       = np.radians(lons)
  vert_coord = -1   
  QC = 1.0 #dummy variable

# Fix the negative lons...

  lons       = np.where(lons > 0.0, lons, lons+(2.0*np.pi))

# extra information

# Set up the time stamping for dat
      
  
# Print the number of value gates

#  mask_check = data.mask && numpy.isnan().any()

  data_length = np.size(data)
  print(("\n Number of good observations:  %d" % data_length))
  
# Create a multidimension iterator to move through 3D array creating obs
 
  nobs = obnum_insert

  for i in range(data.shape[0]):
   
      
          nobs += 1

# time of observations is the mean time of each sweep
          
          
          
          #sw_time = dt_time + DT.timedelta(seconds=time[i])

          days    = days_in[i]
          seconds = seconds_in[i]
  

          fi.write(" OBS            %d\n" % (nobs) )
              
          fi.write("   %20.14f\n" % data[i]  )
          fi.write("   %20.14f\n" % truth[i] )
          fi.write("   %20.14f\n" % (QC)) 
          if nobs == 1: 
              fi.write(" %d %d %d\n" % (-1, nobs+1, -1) ) # First obs.
          else:
              fi.write(" %d %d %d\n" % (nobs-1, nobs+1, -1) ) 
      
          fi.write("obdef\n")
          fi.write("loc3d\n")
          if int(kind[i]) in [16,17,18,183,184,185]:
              fi.write("    %20.14f          %20.14f          %20.14f     %d\n" % 
                  (lons[i], lats[i], z[i], 2))
          else:
              fi.write("    %20.14f          %20.14f          %20.14f     %d\n" % 
                  (lons[i], lats[i], z[i], vert_coord))
      
          fi.write("kind\n")

# If we created zeros, and 0dbz_obtype == True, write them out as a separate data type
# IF MRMS_zeros == True, we assume that is what you want anyway.

          fi.write("     %d     \n" % int(kind[i]) )
          

# If this GEOS cloud pressure observation, write out extra information (NOTE - NOT TESTED FOR HDF2ASCII LJW 04/13/15)
# 
#       if kind == ObType_LookUp("GOES_CWP_PATH"):
#           fi.write("    %20.14f          %20.14f  \n" % (row["satellite"][0], row["satellite"][1]) )
#           fi.write("    %20.14f  \n" % (row["satellite"][2]) )


    # Done with special radial velocity obs back to dumping out time, day, error variance info
      
          fi.write("    %d          %d     \n" % (seconds, days) )

    # Logic for command line override of observational error variances
          fi.write("    %20.14f  \n" % oerror[i] )

          if nobs % 1000 == 0: print((" write_DART_ascii:  Processed observation # %d" % nobs))
  
      
      
  fi.close()
  #PT 2
  with open(infile, 'r') as input_file, open(outfile, 'w') as output_file, open(step1, 'r') as insert_file:
    flag=0
    humidity_definitions=0
    for linenumber, line in enumerate(input_file):
        if 'SPECIFIC_HUMIDITY' in line.strip():
           humidity_definitions+=1
        if 'num_copies' in line.strip():
             if (humidity_definitions==0):
                akind, DART_name = ObType_LookUp(str(28), DART_name=True,reverse=True)
                output_file.write("    %d          %s   \n" % (akind, DART_name) ) 
                akind, DART_name = ObType_LookUp(str(43), DART_name=True,reverse=True)
                output_file.write("    %d          %s   \n" % (akind, DART_name) ) 
                akind, DART_name = ObType_LookUp(str(19), DART_name=True,reverse=True)
                output_file.write("    %d          %s   \n" % (akind, DART_name) ) 
                akind, DART_name = ObType_LookUp(str(1), DART_name=True,reverse=True)
                output_file.write("    %d          %s   \n" % (akind, DART_name) ) 
                akind, DART_name = ObType_LookUp(str(2), DART_name=True,reverse=True)
                output_file.write("    %d          %s   \n" % (akind, DART_name) ) 
                akind, DART_name = ObType_LookUp(str(5), DART_name=True,reverse=True)
                output_file.write("    %d          %s   \n" % (akind, DART_name) ) 
                akind, DART_name = ObType_LookUp(str(6), DART_name=True,reverse=True)
                output_file.write("    %d          %s   \n" % (akind, DART_name) ) 
        if linenumber==2:
                num_otypes = int(line.strip().split()[0])
                line='{}'.format(num_otypes)+'\n'

        if line.strip().startswith('num_obs'):
            line=' num_obs:     {}  max_num_obs:     {}'.format(obnum_last+np.shape(lats)[0],obnum_last+np.shape(lats)[0])+ '\n'
        if line.strip().startswith('first'):
            line=' first:       1  last:        {}'.format(obnum_last+np.shape(lats)[0])+ '\n'
        if ('OBS' in line.strip()) and flag<2:
            index_number = int(line.strip().split()[1])
            if index_number==obnum_insert:
                flag=2
                print('found obnum insert: {}'.format(obnum_insert))
            else:
                flag=1
            current_entry_lines = ['blank']
        elif ('OBS' in line.strip()) and flag==2:
            output_file.write(insert_file.read())
            current_entry_lines = ['blank']
            index_number = int(line.strip().split()[1])
            flag=3
            print('index flag 2: {}'.format(index_number))
        if ('OBS' in line.strip()) and flag==3:
            index_number = int(line.strip().split()[1])
            line='OBS            {}'.format(index_number+np.shape(lats)[0])+'\n'      
            current_entry_lines = ['blank']
        elif flag>0 and len(current_entry_lines) <= 4:
            if len(current_entry_lines) == 4:
                if index_number==obnum_last:
                    line='{} {} {}'.format(index_number+np.shape(lats)[0]-1,-1,-1)+ '\n'

                elif index_number>obnum_insert:
                    line='{} {} {}'.format(index_number+np.shape(lats)[0]-1,index_number+np.shape(lats)[0]+1,-1)+ '\n'
            current_entry_lines.append('blank') 

        output_file.write(line)
  os.remove(step1)

    

def write_DART_ascii_direct_conventional(data,lats,lons,z,days_in,seconds_in,kind,oerror,filename=None, zero_dbz_obtype=True, grid_dict=None,conventional=True):

  if filename == None:
    print(("\n write_DART_ascii:  No output file name is given, writing to %s" % "obs_seq.txt"))
    filename = "obs_seq.out"
  else:
    dirname = os.path.dirname(filename)
    basename = "%s_%s.out" % ("obs_seq", os.path.basename(filename))
    filename =  os.path.join(dirname, basename)
      

# Open ASCII file for DART obs to be written into.  We will add header info afterward
  
  fi = open(filename, "w")
  
# This is why I love python - they think of everything.  Here Numpy has an interator over 
#      an array, and it will extract the indices for you automatically..so create a single 
#      loop over a MD array is very simple....

    
  
  lats       = np.radians(lats)
  lons       = np.radians(lons)
  vert_coord = -1   
  truth      = 1.0  # dummy variable

# Fix the negative lons...

  lons       = np.where(lons > 0.0, lons, lons+(2.0*np.pi))

# extra information

# Set up the time stamping for dat
      
  
# Print the number of value gates

#  mask_check = data.mask && numpy.isnan().any()

  data_length = np.size(data)
  print(("\n Number of good observations:  %d" % data_length))
  
# Create a multidimension iterator to move through 3D array creating obs
 
  nobs = 0
  nobs_clearair = 0

  for i in range(data.shape[0]):
   
      
          nobs += 1

# time of observations is the mean time of each sweep
          
          
          
          #sw_time = dt_time + DT.timedelta(seconds=time[i])

          days    = days_in[i]
          seconds = seconds_in[i]
  

          fi.write(" OBS            %d\n" % (nobs) )
              
          fi.write("   %20.14f\n" % data[i]  )
          fi.write("   %20.14f\n" % truth )
            
          if nobs == 1: 
              fi.write(" %d %d %d\n" % (-1, nobs+1, -1) ) # First obs.
          elif nobs == data_length:
              fi.write(" %d %d %d\n" % (nobs-1, -1, -1) ) # Last obs.
          else:
              fi.write(" %d %d %d\n" % (nobs-1, nobs+1, -1) ) 
      
          fi.write("obdef\n")
          fi.write("loc3d\n")
          if int(kind[i]) in [16,17,18,183,184,185]:
              fi.write("    %20.14f          %20.14f          %20.14f     %d\n" % 
                  (lons[i], lats[i], z[i], 2))
          else:
              fi.write("    %20.14f          %20.14f          %20.14f     %d\n" % 
                  (lons[i], lats[i], z[i], vert_coord))
      
          fi.write("kind\n")

# If we created zeros, and 0dbz_obtype == True, write them out as a separate data type
# IF MRMS_zeros == True, we assume that is what you want anyway.

          fi.write("     %d     \n" % int(kind[i]) )
          

# If this GEOS cloud pressure observation, write out extra information (NOTE - NOT TESTED FOR HDF2ASCII LJW 04/13/15)
# 
#       if kind == ObType_LookUp("GOES_CWP_PATH"):
#           fi.write("    %20.14f          %20.14f  \n" % (row["satellite"][0], row["satellite"][1]) )
#           fi.write("    %20.14f  \n" % (row["satellite"][2]) )


    # Done with special radial velocity obs back to dumping out time, day, error variance info
      
          fi.write("    %d          %d     \n" % (seconds, days) )

    # Logic for command line override of observational error variances
          fi.write("    %20.14f  \n" % oerror[i] )

          if nobs % 1000 == 0: print((" write_DART_ascii:  Processed observation # %d" % nobs))
  
      
      
  fi.close()
  
# To write out header information AFTER we know how big the observation data set is, we have
# to read back in the entire contents of the obs-seq file, store it, rewrite the file
# with header information first, and then dump the contents of obs-seq back inp.  Yuck.

  with open(filename, 'r') as f: f_obs_seq = f.read()
  fi = open(filename, "w")

  
  fi.write(" obs_sequence\n")
  fi.write("obs_kind_definitions\n")

# Deal with case that for reflectivity, 2 types of observations might have been created

  unique_kinds = np.unique(kind)
  fi.write("       %d\n" % int(unique_kinds.shape[0]))
  for uniq_kind in unique_kinds:
      akind, DART_name = ObType_LookUp(str(int(uniq_kind)), DART_name=True,reverse=True)
      fi.write("    %d          %s   \n" % (akind, DART_name) )

  fi.write("  num_copies:            %d  num_qc:            %d\n" % (1, 1))
  
  fi.write(" num_obs:       %d  max_num_obs:       %d\n" % (nobs, nobs) )
      
  fi.write("observations\n")
  fi.write("QC radar\n")
          
  fi.write("  first:            %d  last:       %d\n" % (1, nobs) )

# Now write back in all the actual DART obs data

  fi.write(f_obs_seq)
  
  fi.close()
  
  print(("\n write_DART_ascii:  Created ascii DART file, N = %d written" % nobs))
  
  return

    
  
#####################################################################################################
def write_netcdf_radar_file(ref, vel, filename=None):
    
   _time_units    = 'seconds since 1970-01-01 00:00:00'
   _calendar      = 'standard'

   if filename == None:
       print(("\n write_DART_ascii:  No output file name is given, writing to %s" % "obs_seq.nc"))
       filename = "obs_seq.nc"
   else:
       dirname = os.path.dirname(filename)
       basename = "%s_%s.nc" % ("obs_seq", os.path.basename(filename))
       filename =  os.path.join(dirname, basename)

   _stringlen     = 8
   _datelen       = 19
     
# Extract grid and ref data
        
   dbz        = ref.data
   lats       = ref.lats
   lons       = ref.lons
   hgts       = ref.zg + ref.radar_hgt
   kind       = ObType_LookUp(ref.field.upper())  
   R_xy       = np.sqrt(ref.xg[20]**2 + ref.yg[20]**2)
   elevations = beam_elv(R_xy, ref.zg[:,20,20])
 
# if there is a zero dbz obs type, reform the data array 
   try:
       nx1, ny1       = ref.zero_dbz.shape
       zero_data      = np.ma.zeros((2, ny1, nx1), dtype=np.float32)
       zero_hgts      = np.ma.zeros((2, ny1, nx1), dtype=np.float32)
       zero_data[0]   = ref.zero_dbz
       zero_data[1]   = ref.zero_dbz
       zero_hgts[0:2] = ref.zero_dbz_zg[0:2]
       cref           = ref.cref
       zero_flag = True
       print("\n write_DART_ascii:  0-DBZ separate type added to netcdf output\n")       
   except AttributeError:
       zero_flag = False
       print("\n write_DART_ascii:  No 0-DBZ separate type found\n")
     
# Extract velocity data
  
   vr                  = vel.data
   platform_lat        = vel.radar_lat
   platform_lon        = vel.radar_lon
   platform_hgt        = vel.radar_hgt

# Use the volume mean time for the time of the volume
      
   dtime   = ncdf.num2date(ref.time['data'].mean(), ref.time['units'])
   days    = ncdf.date2num(dtime, units = "days since 1601-01-01 00:00:00")
   seconds = np.int(86400.*(days - np.floor(days)))  
 
# create the fileput filename and create new netCDF4 file

#filename = os.path.join(path, "%s_%s%s" % ("Inflation", DT.strftime("%Y-%m-%d_%H:%M:%S"), ".nc" ))

   print("\n -->  Writing %s as the radar file..." % (filename))
   
   rootgroup = ncdf.Dataset(filename, 'w', format='NETCDF4')
     
# Create dimensions

   shape = dbz.shape
 
   rootgroup.createDimension('nz',   shape[0])
   rootgroup.createDimension('ny',   shape[1])
   rootgroup.createDimension('nx',   shape[2])
   rootgroup.createDimension('stringlen', _stringlen)
   rootgroup.createDimension('datelen', _datelen)
   if zero_flag:
       rootgroup.createDimension('nz2',   2)
 
# Write some attributes

   rootgroup.time_units   = _time_units
   rootgroup.calendar     = _calendar
   rootgroup.stringlen    = "%d" % (_stringlen)
   rootgroup.datelen      = "%d" % (_datelen)
   rootgroup.platform_lat = platform_lat
   rootgroup.platform_lon = platform_lon
   rootgroup.platform_hgt = platform_hgt

# Create variables

   R_type  = rootgroup.createVariable('REF', 'f4', ('nz', 'ny', 'nx'), zlib=True, shuffle=True )    
   V_type  = rootgroup.createVariable('VEL', 'f4', ('nz', 'ny', 'nx'), zlib=True, shuffle=True )
 
   if zero_flag:
       R0_type   = rootgroup.createVariable('0REF',  'f4', ('nz2', 'ny', 'nx'), zlib=True, shuffle=True )    
       Z0_type   = rootgroup.createVariable('0HGTS', 'f4', ('nz2', 'ny', 'nx'), zlib=True, shuffle=True )
       CREF_type = rootgroup.createVariable('CREF', 'f4', ('ny', 'nx'), zlib=True, shuffle=True )
     
   V_dates = rootgroup.createVariable('date', 'S1', ('datelen'), zlib=True, shuffle=True)
   V_xc    = rootgroup.createVariable('XC', 'f4', ('nx'), zlib=True, shuffle=True)
   V_yc    = rootgroup.createVariable('YC', 'f4', ('ny'), zlib=True, shuffle=True)
   V_el    = rootgroup.createVariable('EL', 'f4', ('nz'), zlib=True, shuffle=True)

   V_lat   = rootgroup.createVariable('LATS', 'f4', ('ny'), zlib=True, shuffle=True)
   V_lon   = rootgroup.createVariable('LONS', 'f4', ('nx'), zlib=True, shuffle=True)
   V_hgt   = rootgroup.createVariable('HGTS', 'f4', ('nz', 'ny', 'nx'), zlib=True, shuffle=True)

# Write variables

   rootgroup.variables['date'][:] = ncdf.stringtoarr(dtime.strftime("%Y-%m-%d_%H:%M:%S"), _datelen)
 
   rootgroup.variables['REF'][:]  = dbz[:]
   rootgroup.variables['VEL'][:]  = vr[:]
   rootgroup.variables['XC'][:]   = ref.xg[:]
   rootgroup.variables['YC'][:]   = ref.yg[:]
   rootgroup.variables['EL'][:]   = elevations[:]
   rootgroup.variables['HGTS'][:] = ref.zg[:]
   rootgroup.variables['LATS'][:] = lats[:]
   rootgroup.variables['LONS'][:] = lons[:]
 
   if zero_flag:
      rootgroup.variables['0REF'][:]   = zero_data
      rootgroup.variables['0HGTS'][:]  = zero_hgts
      rootgroup.variables['CREF'][:]   = cref
 
   rootgroup.sync()
   rootgroup.close()
 
   return filename  

def write_DART_ascii_direct(data,lats,lons,z,days_in,seconds_in,kind,oerror,platform_loc,platform_dir,keep_crop,truth=None,filename=None, grid_dict=None,include_truth=False):

# Set default outfile if no outfile name specification given
  if filename == None:
    print(("\n write_DART_ascii:  No output file name is given, writing to %s" % "obs_seq.txt"))
    filename = "obs_seq.out"
      

# Open ASCII file for DART obs to be written into.  We will add header info afterward
  
  fi = open(filename, "w")
  
# This is why I love python - they think of everything.  Here Numpy has an interator over 
#      an array, and it will extract the indices for you automatically..so create a single 
#      loop over a MD array is very simple....

    
  
  lats       = np.radians(lats)
  lons       = np.radians(lons)
  
  if(include_truth==False):
      truth      = 1.0  # dummy variable
  QC = 1.0
  platform_key = 1 
  vr_nyquist = 33.2700004577637
  spread_factor = 1 
# Fix the negative lons...

  lons       = np.where(lons > 0.0, lons, lons+(2.0*np.pi))

# extra information

# Set up the time stamping for dat
      
  
# Print the number of value gates

#  mask_check = data.mask && numpy.isn:/an().any()

  data_length = np.sum(keep_crop)
  print(("\n Number of good observations:  %d" % data_length))
  
# Create a multidimension iterator to move through 3D array creating obs
 
  nobs = 0
  nobs_clearair = 0

  for i in range(data.shape[0]):
          if('RADAR' in ObType_LookUp(str(int(kind[i])), DART_name=True,reverse=True)[1]):
              vert_coord = 3
          elif('DOPPLER' in ObType_LookUp(str(int(kind[i])), DART_name=True,reverse=True)[1]):
              vert_coord = 3
          elif('ACARS' in ObType_LookUp(str(int(kind[i])), DART_name=True,reverse=True)[1]):
              vert_coord = 2 
          else:
              vert_coord = -1

          if (keep_crop[i]==0):
            continue
          else:
            nobs += 1

# time of observations is the mean time of each sweep
          
         # Logic for command line override of observational error variances
          akind, DART_name = ObType_LookUp(str(int(kind[i])), DART_name=True,reverse=True)
          

          days    = days_in[i]
          seconds = seconds_in[i]
  

          fi.write(" OBS            %d\n" % (nobs) )
          fi.write("   %20.14f\n" % (data[i]))
          if (include_truth==True): 
              fi.write("   %20.14f\n" % (truth[i]))
          fi.write("   %20.14f\n" % (QC))
            
          if nobs == 1: 
              fi.write(" %d %d %d\n" % (-1, nobs+1, -1) ) # First obs.
          elif nobs == data_length:
              fi.write(" %d %d %d\n" % (nobs-1, -1, -1) ) # Last obs.
          else:
              fi.write(" %d %d %d\n" % (nobs-1, nobs+1, -1) ) 
      
          fi.write("obdef\n")
          fi.write("loc3d\n")

          fi.write("    %20.14f          %20.14f          %20.14f     %d\n" % 
                  (lons[i], lats[i], z[i], vert_coord))
      
          fi.write("kind\n")

# If we created zeros, and 0dbz_obtype == True, write them out as a separate data type
# IF MRMS_zeros == True, we assume that is what you want anyway.

          fi.write("     %d     \n" % int(kind[i]) )
          
          if kind[i] == 36:
          
              
              fi.write("platform\n")
              fi.write("loc3d\n")


              fi.write("    %20.14f          %20.14f        %20.14f    %d\n" % 
                      (platform_loc[i,0], platform_loc[i,1], platform_loc[i,2], 3) )
          
              fi.write("dir3d\n")
          
              fi.write("    %20.14f          %20.14f        %20.14f\n" % (platform_dir[i,0], platform_dir[i,1], platform_dir[i,2]) )
              fi.write("    %20.14f     \n" % vr_nyquist )
              fi.write("    %d          \n" % platform_key )


# If this GEOS cloud pressure observation, write out extra information (NOTE - NOT TESTED FOR HDF2ASCII LJW 04/13/15)
# 
#       if kind == ObType_LookUp("GOES_CWP_PATH"):
#           fi.write("    %20.14f          %20.14f  \n" % (row["satellite"][0], row["satellite"][1]) )
#           fi.write("    %20.14f  \n" % (row["satellite"][2]) )


    # Done with special radial velocity obs back to dumping out time, day, error variance info
      
          fi.write("    %d          %d     \n" % (seconds, days) )


          fi.write("    %20.14f  \n" % oerror[i] )

          if nobs % 1000 == 0: print((" write_DART_ascii:  Processed observation # %d" % nobs))
  
      
      
  fi.close()
  
# To write out header information AFTER we know how big the observation data set is, we have
# to read back in the entire contents of the obs-seq file, store it, rewrite the file
# with header information first, and then dump the contents of obs-seq back inp.  Yuck.

  with open(filename, 'r') as f: f_obs_seq = f.read()
  fi = open(filename, "w")

  
  fi.write(" obs_sequence\n")
  fi.write("obs_kind_definitions\n")

# Deal with case that for reflectivity, 2 types of observations might have been created

  unique_kinds = np.unique(kind)
  fi.write("       %d\n" % int(unique_kinds.shape[0]))
  for uniq_kind in unique_kinds:
      akind, DART_name = ObType_LookUp(str(int(uniq_kind)), DART_name=True,reverse=True)
      fi.write("    %d          %s   \n" % (akind, DART_name) )
  if(include_truth==False):
      fi.write("  num_copies:            %d  num_qc:            %d\n" % (1, 1))
  else:
      fi.write("  num_copies:            %d  num_qc:            %d\n" % (2, 1))

  fi.write(" num_obs:       %d  max_num_obs:       %d\n" % (nobs, nobs) )
      
  fi.write("observations\n")
  if(include_truth==True):
     fi.write("truth\n")
  fi.write("QC radar\n")
          
  fi.write("  first:            %d  last:       %d\n" % (1, nobs) )

# Now write back in all the actual DART obs data

  fi.write(f_obs_seq)
  
  fi.close()
  f.close()
  
  print(("\n write_DART_ascii:  Created ascii DART file, N = %d written" % nobs))
  
  return