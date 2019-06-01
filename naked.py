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

# Time-Stepping Naked Planet Model
# https://www.coursera.org/learn/global-warming-model/supplement/m29aQ/model-formulation

# The goal is to numerically simulate how the planetary temperature of a naked planet would
# change through time as it approaches equilibrium (the state at which it stops changing, 
# which we calculated before). The planet starts with some initial temperature. 
# The “heat capacity” (units of Joules / m2 K) of the planet is set by a layer of 
# water which absorbs heat and changes its temperature. If the layer is very thick, 
# it takes a lot more heat (Joules) to change the temperature.

import sys, getopt, re, os
from scipy import constants


# Other constants

Density_water       = 1000             # Kg/M3

# parameters

L                   = 1350             # Watts/m2
albedo              = 0.3
epsilon             = 1

# calculate heat radiated (Stefan Bolzmann)

def heat_flux_out_calc(T):
  return epsilon * constants.sigma * T*T*T*T

# Iterate through possible times. Compute heat from heat flux
# then next temperature

def iterate_naked_planet(number_of_steps,must_plot,name,y_time_step,water_depth):
  water_column  = water_depth * Density_water # Kg (1 square meter column)
  heat_capacity = water_column * constants.calorie /constants.gram # Kg * (J/(gram*degree)) *(gram/Kg)
  if debug:
    print ('Mass of water={0},heat capacity= {1}'.format(water_column,heat_capacity))
  time_list=[0]
  temperature_list=[initial_temperature]
  heat_stored_in_water = heat_capacity*initial_temperature
  for i in range(number_of_steps):
    heat_flux_in = L * (1 - albedo) /4 # J/sec
    heat_flux_out = heat_flux_out_calc(temperature_list[-1]) # J/sec
    heat_flux_nett = heat_flux_in - heat_flux_out # J/sec
    heat_gain = heat_flux_nett * y_time_step * constants.year #J==(J/s) * (y) * (s/y)
    heat_stored_in_water += heat_gain
    time_list.append(y_time_step*(i+1))
    temperature_list.append(heat_stored_in_water/heat_capacity)
    if debug:
      print ('{0}: T={6:5.2f}, flux in={1:.4f}, flux_out={2:.4f}, nett={3:.4f}, gain={4:.2e}, stored={5:.2e}'.\
             format(time_list[-2],heat_flux_in,heat_flux_out,heat_flux_nett,heat_gain,heat_stored_in_water,temperature_list[-1]))
    
  if must_plot:
    plot(time_list, temperature_list,name)
    
  return (temperature_list[-1],heat_flux_out_calc(temperature_list[-1]))

def plot(time_list, temperature_list,name):
  plt.plot( time_list, temperature_list)
  plt.xlabel('Time')
  plt.ylabel('Temperature K')
  plt.title('Naked Planet. Timestep = {0} years, depth = {1} metres'.
            format(y_time_step,water_depth))
  plt.savefig(name)
  plt.show()

# Provide command level help

def help():
  print ('Time-Dependent Energy Balance Model from ')
  print ('Global Warming II: Create Your Own Models in Python')
  print ('')
  print ('To pass the automated code check, enter:')
  print ('   python naked.py')
  print ('To specify number of steps and plot to a named file, enter:')
  print ('   python naked.py -p -s 600 -n foo.png')
  print ('To specify timesetp and water depth, use the -t and -w options')
  print ('   NB timestep may be a fraction of a year. e.g.')
  print ('   python naked.py -p -s 600 -n foo.png -t 0.05 -w 1')


# This is the main program. We use command line parameters to have a single
# program that will pass the grader and generate plots

if __name__=='__main__':
  y_time_step         = 100              # years
  water_depth         = 4000             # meters  
  number_of_steps     = -1               # default, force program to as grader
  must_plot           = False            # Grader doesn't like plotting!
  name                = 'naked.png'      # for saving plot
  initial_temperature = 0
  debug               = False
  
  try:
    opts, args = getopt.getopt( \
          sys.argv[1:],\
          'hps:n:t:w:k:d',\
          ['help','plot','steps=','name=','timestep=','waterdepth=','initialtemperature','debug'])
  except getopt.GetoptError:
    help()
    sys.exit(2)
        
  for opt, arg in opts:
    if opt in ['-h','--help']:
      help()
      sys.exit()
    elif opt in ['-s','--steps']:
      number_of_steps = int(arg)
    elif opt in ['-p','--plot']:
      must_plot=True          
      import  matplotlib.pyplot as plt # grader gets upset by plot library
    elif opt in ['-n','--name']:
      name=arg
    elif opt in ['-t','--timestep']:
      y_time_step = float(arg)  #Quiz question 1 requires time< 1 year
    elif opt in ['-w','--waterdepth']:
      water_depth = int(arg)
    elif opt in ['-k','initialtemperature']:
      initial_temperature = int(arg)
      print (initial_temperature)
    elif opt in ['-d','debug']:
        debug = True    
    
  print (water_depth)      
  if number_of_steps<0:
    number_of_steps = int(input(""))
    
  T,F=iterate_naked_planet(number_of_steps,must_plot,name,y_time_step,water_depth)
  print (T,F)