# Copyright (C) 2016-2019 Greenweaves Software Limited

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

# A Simple 1-D Ice Sheet Flow Model
# https://www.coursera.org/learn/global-warming-model/

# My goal is to have a single program that will:
# 1. Pass the grader
# 2. Satisfy the code tricks quiz
# 3. Allow me to explore the model
# By having a single program, I can accurately record which code
# was actually tested.

# I have therefore used the 'getopt' module to allow the program
# to run from the command line with optional argument supplied by the user.
# If there are no command line argument, the program expects that it
# is being executed by the grader.
# If the program is run with a single argument, '-r', it will do
# what is required by the code review: python ice-sheet.py -r

import sys, getopt, os, re

# Parameters

nX          = 10       # number of grid points
domainWidth = 1e6      # meters
timeStep    = 100      # years
nYears      = 50000    # years
flowParam   = 1e4      # m horizontal / yr
snowFall    = 0.5      # m / y

plotLimit   = 4000


def create_grid():
  return [0 for i in range(nX+2)]

def get_flow(elevation,ix,dX):
  return ( elevation[ix] - elevation[ix+1] ) / dX * flowParam  *  ( elevation[ix]+elevation[ix+1] ) / 2 / dX

def get_snow(flow,ix):
  return ( snowFall + flow[ix-1] - flow[ix] ) * timeStep

def step(elevation,dX):
  flow=[get_flow(elevation,ix,dX) for ix in range(nX+1)]
  for ix in range(1,nX+1):
    elevation[ix]+=get_snow(flow,ix)
  return elevation


  
def iterate(mustPlot=False):
  dX = domainWidth/nX 
  elevation=create_grid()
  fig,ax=(None,None)
  
  if mustPlot:
    fig, ax=initialize_dynamic_plots(elevation)
  
  for year in range(0,int(nYears+timeStep),timeStep):
    elevation=step(elevation,dX)
    if mustPlot:
      print (year)
      plot(elevation,fig,ax)
      
  return elevation

def initialize_dynamic_plots(elevation):
  fig,ax = plt.subplots()
  ax.plot(elevation)
  ax.set_ylim([0,plotLimit])
  plt.show(block=False)    
  return (fig,ax)

def plot(elevation,fig,ax):
  dX = domainWidth/nX
  ax.clear()
  xs=[i * dX for i in range(nX+2) ]
  ax.plot( xs, elevation )
  plt.title('Ice Sheet Flow Model')
  plt.xlabel('Distance')
  plt.ylabel('Height')  
  ax.set_ylim([0,plotLimit])
  plt.show( block=False )
  plt.pause(0.001)
  fig.canvas.draw() 
  
# Provide command level help

def help():
  print ('Iterative Relaxation to Consistent T and Albedo Given L ')
  print ('Global Warming II: Create Your Own Models in Python')
  print ('Usage:')
  print ('   a. To pass grader:')
  print ('      python {0}'.format(__file__))
  print ('   b. For code review:')
  print ('      python {0} -r'.format(__file__))
  print ('   c. Additional arguments')
  print ('      -h --help      To get usage instructions')
  print ('      -v --version   To find version of model')
  print ('      -r --review    Demonstrate functionality for code review')

  

# Main program - decode command line argments and drive iteration

if __name__=='__main__':
  must_plot=False
  try:
      opts, args = getopt.getopt( \
            sys.argv[1:],\
            'hrp',\
            ['help','review','plot'])
  except getopt.GetoptError as e:
    print (e)
    help()
    sys.exit(2)  

  if len(opts)==0:   # This is for the grader
    nYears    = float( input('') )
    elevation = iterate()
    print(elevation[5])
  else:               # This is for all other cases
    # Default values for parameters
 
    for opt, arg in opts:
      if opt in ['-h','--help']:
        help()
        sys.exit()
      elif opt in ['-r','--review']:
        nYears    = 20000
        must_plot = True
      elif opt in ['-p','--plot']:
        must_plot = True  
    
    # run model
    
    if must_plot:
      import  matplotlib.pyplot as plt # grader gets upset by plot library 

    iterate(must_plot)
    if must_plot:
      plt.show()