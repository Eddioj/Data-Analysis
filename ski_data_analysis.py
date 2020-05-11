# -*- coding: utf-8 -*-
"""Final Ski Data Analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BaIRk6Dpkr-TahmTdGWBRBY2YRJYziHv

Hello this is the start of the data analysis - first get the file from git hub into pandas
"""

# Imports for analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

"""Next get the URL from github The easiest way to upload a CSV file is from your GitHub repository. Click on the dataset in your repository, then click on View Raw. Copy the link to the raw dataset and store it as a string variable called url in Colab as shown below (a cleaner method but it’s not necessary). The last step is to load the url into Pandas read_csv to get the dataframe.

See also other methods https://towardsdatascience.com/3-ways-to-load-csv-files-into-colab-7c14fcbdcb92
"""

url = 'https://raw.githubusercontent.com/Eddioj/Data-Analysis/master/Velocity%20Data.csv'
df1 = pd.read_csv(url)
# Dataset is now stored in a Pandas Dataframe df1

"""Lets's see what we loaded looks - data has been fixed"""

#print(df1.shape)
#df1.describe()

# Check what we got 
df1.head()

#print(ss[0:20:1])
#df1.hist('Time')
#df1.hist('Velocity')

"""Plot the raw Velocity data"""

y = df1['Velocity']
  x = list(range(0, len(y)*30, 30))  # intervals are 30ms
  fig = plt.figure(figsize=(20, 2))
  ax = fig.add_subplot(111)
  plt.xlabel("Time ms")
  plt.ylabel("V m/s")
  ax.plot(x,y)
  plt.title('Ski Raw Data ')
  plt.savefig('ski.png')
  plt.show()

"""Create a new series where we flag zero values as start of kick

Note calculating local min and max would be better see https://stackoverflow.com/questions/48023982/pandas-finding-local-max-and-min
"""

#print(type(ts))
#print(type(ss))

# Variables to determine Velocity events in ms
KICK_THRESHOLD = 0.6 
PUSH_THRESHOLD = 1.0 

# series for Velocity
ss = df1['Velocity']

# kick is where Velocity approaches zero
ks = ss.apply(lambda val: val < KICK_THRESHOLD)
#print(ks)

# add back into dataframe
df1['Kick'] = ks

# push is where Velocity exceeds threshold
ps = ss.apply(lambda val: val > PUSH_THRESHOLD)
#print(ps)

# add back into dataframe
df1['Push'] = ps

# check what we got
df1.head()

"""Here we use signal processing to find the local minima and maxima make sure the comparison size n is big enough to take out noise"""

compare_points = 2 
# number of points to be checked before and after 
# Find local peaks
df1['min'] = df1.iloc[argrelextrema(df1.Velocity.values, np.less_equal, order=compare_points)[0]]['Velocity']
df1['max'] = df1.iloc[argrelextrema(df1.Velocity.values, np.greater_equal, order=compare_points)[0]]['Velocity']

# Plot results
plt.figure(figsize=(20, 8))
plt.scatter(df1.index, df1['min'], c='r')
plt.scatter(df1.index, df1['max'], c='g')
plt.plot(df1.index, df1['Velocity'])
plt.show()

df1.head()

"""Just looking at how these series are indexed"""

df1['Push'].index
df1['Kick'].index

"""Now we are going to loop over the time and look for a pulse, this will be a True value in the Kick, then we keep going till we hit a True value in the pulse then we keep going till hit a True value in the kick again."""

# Check the data state
# df1.head()
# df1.iloc[[0],[1]]

# setup indicies, series and results
start = 0
end = 0
kick = False
push = False
spd = df1['Velocity']
results = []

for i in range(0,spd.size,1):

  # Look for the first Kick in the series
  if df1.loc[[i],['Kick']].bool() and start == 0:
    kick = True
    start = i # start index of the kick
  

  # Start of first Push after a Kick
  if df1.loc[[i],['Push']].bool() and kick and not push:
    # print ('push = True')
    push = True

  # Next Kick after a Push 
  if df1.loc[[i],['Kick']].bool() and push:
    kick = True
    end = i
    #print ('start = ',start)
    #print('end =',end)

    # save the series from kick to kick
    impulse = spd[start:end:1]
    impulse.reset_index(drop=True, inplace=True)
    results.append(impulse)

    # print('Impulse =',impulse)

    # reset index
    start = i
    end = start
    push = False

# print(results)

# plot out results
n = 0
for imp in results:
  # print(type(imp))
  n += 1
  y = imp
  x = list(range(0, len(y)*30, 30))  # intervals are 30ms
  fig = plt.figure()
  ax = fig.add_subplot(111)
  plt.xlabel("Time ms")
  plt.ylabel("Velocity ms")
  ax.plot(x,y)
  plt.title('Ski Impulse '+ str(n))
  plt.savefig('ski.png')
  plt.show()

"""Now do some analysis on the results - for example impulse length, max Velocity,"""

# Basic analysis and diagnostics

# factors for various skills
print("Select skill level")
print("1 Beginner")
print("2 Intermediate")
print("3 Expert")

level = 0
while level < 1 or level > 3:
  val = input("Enter Level :")
  level = int(val)

arguments = ['beginner','intermediate', 'expert']

#1
beginner =  {'total_kick_time':{'min':50.0, 'max':400.0}, 
                'ground_time':{'min':40.0, 'max':80.0}, 
                'max_Velocity':{'min':4.0, 'max':100.0}, 
                'min_Velocity':{'min':-2, 'max':1.0}, 
                'glide_time': {'min':500.0, 'max':2000.0}, 
                'terminal_Velocity':{'min':0.5, 'max':3}, 
                'recovery_time':{'min':10.0,'max':400.0}, 
                'total_cycle_time':{'min':1200.0, 'max':2500.0} }   
#2
intermediate = {'total_kick_time':{'min':150.0, 'max':200.0}, 
                'ground_time':{'min':50.0, 'max':70.0}, 
                'max_Velocity':{'min':5.0, 'max':100.0}, 
                'min_Velocity':{'min':-1.0, 'max':1.0}, 
                'glide_time': {'min':1000.0, 'max':1500.0}, 
                'terminal_Velocity':{'min':1.5, 'max':2.5}, 
                'recovery_time':{'min':10.0,'max':250.0}, 
                'total_cycle_time':{'min':1600.0, 'max':1900.0} }      
#3
expert = {'total_kick_time':{'min':100.0, 'max':150.0}, 
                'ground_time':{'min':30.0, 'max':50.0}, 
                'max_Velocity':{'min':6.0, 'max':100.0}, 
                'min_Velocity':{'min':-0.5, 'max':1.0}, 
                'glide_time': {'min':1200.0, 'max':1500.0}, 
                'terminal_Velocity':{'min':1.8, 'max':2.2}, 
                'recovery_time':{'min':10.0,'max':200.0}, 
                'total_cycle_time':{'min':1500.0, 'max':1750.0} }       

user_limits = {'intermediate':intermediate, 'expert':expert, 'beginner':beginner }

parameters = user_limits[arguments[level - 1]]


SAMPLE_NOISE = 4

#threshold percentage to feedback error to user 
ERROR_GATE = 0.6

low_glide = 0
high_glide = 0
sample = len(results)
#print(sample)

kicks = []
glides = []
recoveries = []

# Store out of range values
bad_total_kick_times = []
bad_max_Velocitys = []
bad_min_Velocitys = []
bad_glide_times = []
bad_terminal_Velocitys = []
bad_recovery_times = []
bad_total_cycle_times = []

# Store in range values
good_total_kick_times = []
good_max_Velocitys = []
good_min_Velocitys = []
good_glide_times = []
good_terminal_Velocitys = []
good_recovery_times = []
good_total_cycle_times = []

#number of impulses , used to calculate averages
sample_size = len(results)

print ('Number of cycles:' , sample_size)
print ("")
n = 0
for imp in results:
  n += 1

  # Gather impulse/full cycle parameters
  total_cycle_time = len(imp) * 30
  p_min = parameters['total_cycle_time']['min']
  p_max = parameters['total_cycle_time']['max']

  if total_cycle_time < p_min or total_cycle_time > p_max:
    bad_total_cycle_times.append(total_cycle_time)
  else:
    good_total_cycle_times.append(total_cycle_time)  

  # Get kick
  kick_start = imp.idxmin()
  kick_end = imp.idxmax()
  kick = imp[kick_start:kick_end:1]
  kick.reset_index(drop=True, inplace=True )
  kicks.append(kick)

  # Gather Kick parameters
  total_kick_time = len(kick) * 30
  p_min = parameters['total_kick_time']['min']
  p_max = parameters['total_kick_time']['max']

  if total_kick_time < p_min or total_kick_time > p_max:
    bad_total_kick_times.append(total_kick_time)
  else:
    good_total_kick_times.append(total_kick_time)  

  max_Velocity = kick.max()
  p_min = parameters['max_Velocity']['min']
  p_max = parameters['max_Velocity']['max']

  if max_Velocity < p_min or max_Velocity > p_max:
    bad_max_Velocitys.append(max_Velocity)
  else:
    good_max_Velocitys.append(max_Velocity)  

  min_Velocity = kick.min()
  p_min = parameters['min_Velocity']['min']
  p_max = parameters['min_Velocity']['max']

  if min_Velocity < p_min or min_Velocity > p_max:
    bad_min_Velocitys.append(min_Velocity)
  else:
    good_min_Velocitys.append(min_Velocity)  

  # Get Recovery data
  min_val = 0
  recovery_end = imp.size
  for i in range(recovery_end - 1,0,-1):
    val = imp.iloc[i]
    if val > min_val:
      min_val = val
    elif recovery_end - i > SAMPLE_NOISE:
      # end of the upward gradient
      recovery_start = i
      break
      
  # Get Glide
  glide = imp[kick_end:recovery_start:1]
  glide.reset_index(drop=True, inplace=True )
  glides.append(glide) 

  #  Total time for glide
  glide_time = len(glide) * 30

  p_min = parameters['glide_time']['min']
  p_max = parameters['glide_time']['max']

  if glide_time < p_min or glide_time > p_max:
    bad_glide_times.append(glide_time)
  else:
    good_glide_times.append(glide_time)  
  
  #Getting terminal Velocity
  terminal_Velocity = glide[len(glide) - 1]

  p_min = parameters['terminal_Velocity']['min']
  p_max = parameters['terminal_Velocity']['max']

  if terminal_Velocity < p_min or terminal_Velocity > p_max:
    bad_terminal_Velocitys.append(terminal_Velocity)
  else:
    good_terminal_Velocitys.append(terminal_Velocity)  

# slice recovery
  recovery = imp[recovery_start:recovery_end:1]
  recovery.reset_index(drop=True, inplace=True )
  recoveries.append(recovery)

  # Gather recovery parameters
  recovery_time = len(recovery) * 30
  p_min = parameters['recovery_time']['min']
  p_max = parameters['recovery_time']['max']

  if recovery_time < p_min or recovery_time > p_max:
    bad_recovery_times.append(recovery_time)
  else:
    good_recovery_times.append(recovery_time)  




  #ANALYSIS

#KICK ANALYSIS 

  # -1- Kick time 
if len(bad_total_kick_times) / sample_size >= ERROR_GATE:
  print("%d/%d of kicks took too long - Pass Range %d - %d" % (len(bad_total_kick_times), sample_size, parameters['total_kick_time']['min'], parameters['total_kick_time']['max']))
  ds = pd.Series(np.array(bad_total_kick_times))
  mean = ds.mean()
  print("Mean total Kick time : %d ms" % mean)
  if mean < parameters['total_kick_time']['min']:
    print("Short Kicks")
  else:
    print("Your kicks are taking too Long")
print ("")
  # -2- Kick max Velocity - end of kick
if len(bad_max_Velocitys) / sample_size >= ERROR_GATE:
  print("%d/%d did not reach the required Velocity - Pass Range %d - %d" % (len(bad_max_Velocitys), sample_size, parameters['max_Velocity']['min'], parameters['max_Velocity']['max']))
  ds = pd.Series(np.array(bad_max_Velocitys))
  mean = ds.mean()
  print("Mean max Velocity : %d m/s" % mean)
  if mean < parameters['max_Velocity']['min']:
    print("Max peak Velocity too low")
  else:
    print("")
print ("")
  # -3- Kick min Velocity - slip
if len(bad_min_Velocitys) / sample_size >= ERROR_GATE:
  print("%d/%d of kicks slipped - Pass Range %d - %d" % (len(bad_min_Velocitys), sample_size, parameters['min_Velocity']['min'], parameters['min_Velocity']['max']))
  ds = pd.Series(np.array(bad_min_Velocitys))
  mean = ds.mean()
  print("Mean minimum Velocity : %d m/s" % mean)
  if mean < parameters['min_Velocity']['min']:
    print("You are sliping")
  else:
    print("You are not having full contact with the ground")
print ("")
#GLIDE ANALYSIS

  # -4- Total Glide time 
if len(bad_glide_times) / sample_size >= ERROR_GATE:
  print("%d/%d of glides took too long - Pass Range %d - %d" % (len(bad_glide_times), sample_size, parameters['glide_time']['min'], parameters['glide_time']['max']))
  ds = pd.Series(np.array(bad_glide_times))
  mean = ds.mean()
  print("Mean total glide time : %d ms" % mean)
  if mean < parameters['glide_time']['min']:
    print("Glide for longer")
  else:
    print("Gliding for to long")
print ("")

#RECOVERY ANALYSIS

  # -5- Terminal Velocity  
if len(bad_terminal_Velocitys) / sample_size >= ERROR_GATE:
  print("%d/%d of recoveries did not start at the right Velocity - Pass Range %d - %d" % (len(bad_terminal_Velocitys), sample_size, parameters['terminal_Velocity']['min'], parameters['terminal_Velocity']['max']))
  ds = pd.Series(np.array(bad_terminal_Velocitys))
  mean = ds.mean()
  print("Mean recovery start Velocity : %d m/s" % mean)
  if mean < parameters['terminal_Velocity']['min']:
    print("Start recovery sooner")
  else:
    print("Start Recovery earlier")
print ("")
  # -6- Recovery Velocity   
if len(bad_recovery_times) / sample_size >= ERROR_GATE:
  print("%d/%d of recoveries taking too long - Pass Range %d - %d" % (len(bad_recovery_times), sample_size, parameters['recovery_time']['min'], parameters['recovery_time']['max']))
  ds = pd.Series(np.array(bad_recovery_times))
  mean = ds.mean()
  print("Mean recovery time : %d ms" % mean)
  if mean < parameters['recovery_time']['min']:
    print("")
  else:
    print("Recovery taking too long")
print ("")

#FULL CYCLE ANALYSIS
  # -7- Total cycle time 
if len(bad_total_cycle_times) / sample_size >= ERROR_GATE:
  print("%d/%d of cycles were out of total time- Pass Range %d - %d" % (len(bad_total_cycle_times), sample_size, parameters['total_cycle_time']['min'], parameters['total_cycle_time']['max']))
  ds = pd.Series(np.array(bad_total_cycle_times))
  mean = ds.mean()
  print("Mean cycle time : %d ms" % mean)
  if mean < parameters['total_cycle_time']['min']:
    print("Your cycles are too short")
  else:
    print("Your cycles are taking too long")
print ("")
#DATA PRINT OUT

#print (bad_max_Velocitys)
#print (good_max_Velocitys)

#print (bad_min_Velocitys)
#print (good_min_Velocitys)

#print (bad_recovery_times)
#print (good_recovery_times)

#print (bad_glide_times)
#print (good_glide_times)

#print (bad_terminal_Velocitys)
#print (good_terminal_Velocitys)

#print (bad_total_cycle_times)
#print (good_total_cycle_times)

"""Now look for end of the push working back from the data end"""

n = 0
for d in kicks:
  n += 1
  y = d
  x = list(range(0, len(d)*30, 30))  # intervals are 30ms
  fig = plt.figure()
  ax = fig.add_subplot(111)
  plt.xlabel("Time ms")
  plt.ylabel("Velocity m/s")
  ax.plot(x,y)
  plt.title('Ski kicks '+ str(n))
  plt.savefig('ski_kick.png')
  plt.show()

n = 0
for d in glides:
  n += 1
  y = d
  x = list(range(0, len(d)*30, 30))  # intervals are 30ms
  fig = plt.figure()
  ax = fig.add_subplot(111)
  plt.xlabel("Time ms")
  plt.ylabel("Velocity m/s")
  ax.plot(x,y)
  plt.title('Ski Glides '+ str(n))
  plt.savefig('ski_kick.png')
  plt.show()

n = 0
for d in recoveries:
  n += 1
  y = d
  x = list(range(0, len(d)*30, 30))  # intervals are 30ms
  fig = plt.figure()
  ax = fig.add_subplot(111)
  plt.xlabel("Time ms")
  plt.ylabel("Velocity m/s")
  ax.plot(x,y)
  plt.title('Ski Recoveries '+ str(n))
  plt.savefig('ski_kick.png')
  plt.show()