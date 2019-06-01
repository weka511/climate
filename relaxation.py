# (C) 2016-2019 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>

# Time-Stepping Naked Planet Model
# https://www.coursera.org/learn/global-warming-model/supplement/m29aQ/model-formulation

# My goal is to have a single program that will:
# 1. Pass the grader
# 2. Satisfy the code tricks/quiz
# 3. Allow me to explore the model
# By having a single program, I can accurately record which code
# was actually tested

# I have therefore used the 'getopt' module to allow the program
# to run from the command line with opional argument supplied by the user.
# If there are no command line argument, the program expects that it
# is being executed by the grader.
# If the program is run with the following arguments, it will do
# what is required by the code review: python relaxation.py -f 1150 -l 1350 -p

import sys, getopt, os, re
from scipy import constants

# Constants

epsilon             = 1


# clip
#
# Used to restrict a value to be within a specified range
# clip (0.5,0,1)==0.5
# clip (-0.5,0,1)==0
# clip (1.5,0,1)==1.0

def clip(x,low,high):
  return low if x<low else high if x>high else x

# Find T from L and albedo
#
# Use energy balance; heat in=heat radiated out

def get_T(L,albedo):
  return (L*(1-albedo)/(4*epsilon*constants.sigma))**0.25

# get_latitudu
#
# Get ice latitude from Temperatue
#
# Use regression from data in
# https://www.coursera.org/learn/global-warming-model/supplement/
# fqAsP/parameterized-relationship-between-t-ice-latitude-and-albedo

def get_latitudu(T):
  return 1.5*clip(T,215,265) - 322.5

# get_albedo
#
# Get albedo from latitude
#
# Use regression from data in
# https://www.coursera.org/learn/global-warming-model/supplement/
# fqAsP/parameterized-relationship-between-t-ice-latitude-and-albedo
# NB: the regression gives -0.0067 as the slope to 4 decimal places,
# which doesn't track the data in the spreadsheet very well. I tried 8
# decimal places, and it looks as if the value should really be -2/300
# I check and found that 2/300 works better.

def get_albedo(latitude):
  return -2*clip(latitude,0,75)/300 + 0.65

# step_albedo
#
# Refine albedo and calculate corresponding temperature

def step_albedo(L,albedo):
  T=get_T(L,albedo)
  latitude=get_latitudu(T)
  albedo=get_albedo(latitude)
  return (T,albedo)

# get_albedo_from_L
#
# Determina albedo and temperature by iterating
# 1. Calculate T given L & trial albedo.
# 2. Calcualte new albedo fot T
#
# Iteration continues until values agree within specified tolerance

def get_albedo_from_L(L,albedo,tolerance):
  previous_albedo=albedo
  T,albedo=step_albedo(L,albedo)  
  while abs(albedo-previous_albedo)>tolerance:
    previous_albedo=albedo
    T,albedo=step_albedo(L,albedo)    
  return (T,albedo)

# evolve_model
#
# Vary luminosity within specified range, and calculate Temperature
# For each luminosity, use previously calculated value of albedo as
# starting point for iterations

def evolve_model(first,last,step,tolerance):
  print ('From {0:d} to {1:d} by {2:d}. Tolerance={3}'.\
         format(first,last,step,tolerance))
  step=10
  albedo=0.15
  Ls=[]
  Ts=[]
  if last<first:
    step=-step
  for L in range(first,last+step,step):
    T,albedo=get_albedo_from_L(L,albedo,tolerance)
    print ('{0:d}, {1:0.1f}'.format(L,T))
    Ls.append(L)
    Ts.append(T)
  return (Ls,Ts)
 
# plot
#
# Plot temperature against luminosity

def plot(Ls1,Ts1,Ls2,Ts2,name,tolerance):
  plt.plot(Ls1,Ts1,'b-',label='Descending Luminosity')
  plt.plot(Ls2,Ts2,'r-',label='Ascending Luminosity')
  plt.plot([1200,1600],[273.16,273.16],'g--',label='Water<-->Ice')
  plt.legend(loc='lower right')
  plt.title('Temperature vs. Luminosity, tolerance={0:.2e}'.format(tolerance))
  plt.grid(True)   
  plt.xlabel('Luminosity')
  plt.ylabel('Temperature K')
  plt.savefig(name)
  plt.show()  

# Provide command level help

def help():
  print ('Iterative Relaxation to Consistent T and Albedo Given L ')
  print ('Global Warming II: Create Your Own Models in Python')
  print ('Usage:')
  print ('   a. To pass grader:')
  print ('      python relaxation.py')
  print ('   b. For code review:')
  print ('      python relaxation.py -p')
  print ('   c. Additional arguments')
  print ('      -h --help      To get usage instructions')
  print ('      -v --version   To find version of model')
  print ('      -t --tolerance Tolerance for iterating to determine albedo from L')
  print ('      -n --name      File name for saving plot')
  print ('      -p --plot      Species that output is to be plotted')
  print ('      -f --fromL     Starting Luminosity')
  print ('      -t --toL       Final Luminosity')
  print ('      -s --step      Step size for iterating across luminosities')
  
# Determine revision number from subversion

def version(tag='$LastChangedRevision: 890 $'):
  re_number=re.compile('.* ([0-9]+) .*')
  match=re_number.match(tag)
  return int(match.group(1))

# Main program - decode command line argmengts and drive iteration

if __name__=='__main__':
  must_plot = False
  try:
      opts, args = getopt.getopt( \
            sys.argv[1:],\
            'hvt:n:pf:l:s:',\
            ['help','version','tolerance','name','plot','fromL','toL','step'])
  except getopt.GetoptError as e:
    print (e)
    help()
    sys.exit(2)  

  if len(opts)==0:   # This is for the grader
    L, albedo, nIters = input("").split()
    L, albedo, nIters = [ float(L), float(albedo), int(nIters) ]
   
    for i in range(nIters):
      T,albedo=get_albedo_from_L(L,albedo,2.0)
    print (T,albedo)
  else:               # This is for all other cases
    # Default values for parameters
    fromL     = 1150
    toL       = 1350
    step      = 10
    tolerance = 1.0e-9    # allowable error in iteration  
    name      = 'relaxation.png'    
    for opt, arg in opts:
      if opt in ['-h','--help']:
        help()
        sys.exit()
      elif opt in ['-v','--version']:
        print ('{0} revision {1}'.format(os.path.basename(sys.argv[0]), version()))
        sys.exit()
      elif opt in ['-t','--tolerance']:
        tolerance=float(arg)
      elif opt in ['-n','--name']:
        name=arg
      elif opt in ['-p','--plot']:
        must_plot=True          
      elif opt in ['-f','--fromL']:
        fromL=int(arg)     
      elif opt in ['-l','--toL']:
        toL=int(arg)
      elif opt in ['-n','--name']:
        name=arg      
      elif opt in ['-s','--step']:
        step=int(arg)     

    
    Ls1,Ts1=evolve_model(toL,fromL,step,tolerance)
    Ls2,Ts2=evolve_model(fromL,toL,step,tolerance)
  
    if must_plot:
      import  matplotlib.pyplot as plt # grader gets upset by plot library 
      plot(Ls1,Ts1,Ls2,Ts2,name,tolerance)