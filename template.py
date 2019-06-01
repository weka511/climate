# $HeadURL: https://server/svn/sandbox/trunk/global-warming-model/template.py $
# $LastChangedDate: 2016-05-04 13:00:13 +1200 (Wed, 04 May 2016) $
# $LastChangedRevision: 832 $

# Copyright (C) 2016 Greenweaves Software Pty Ltd

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

# Code template for Global Warming Models
# https://www.coursera.org/learn/global-warming-model/

# My goal is to have a single program that will:
# 1. Pass the grader
# 2. Satisfy the code review
# 3. Allow me to explore the model

# I have therefore used the 'getopt' module to allow the program
# to run from the command line with opional argument supplied by the user.
# If there are no command line argument, the program expects that it
# is being executed by the grader.
# If the program is run with a single argument, '-r', it will do
# what is required by the code review: python template.py -r

import sys, getopt, os, re

# Constants

sigma               = 5.67E-8            # W/m2 K4
epsilon             = 1



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

  
# Determine revision number from subversion

def version(tag='$LastChangedRevision: 832 $'):
  re_number=re.compile('.* ([0-9]+) .*')
  match=re_number.match(tag)
  return int(match.group(1))

# Main program - decode command line argmengts and drive iteration

if __name__=='__main__':
  must_plot=False
  try:
      opts, args = getopt.getopt( \
            sys.argv[1:],\
            'hvrp',\
            ['help','version','review','plot'])
  except getopt.GetoptError as e:
    print (e)
    help()
    sys.exit(2)  

  if len(opts)==0:   # This is for the grader
    pass
  else:               # This is for all other cases
    # Default values for parameters
 
    for opt, arg in opts:
      if opt in ['-h','--help']:
        help()
        sys.exit()
      elif opt in ['-v','--version']:
        print ('{0} revision {1}'.format(os.path.basename(sys.argv[0]), version()))
        sys.exit()
      elif opt in ['-r','--review']:
        pass 
      elif opt in ['-p','--plot']:
        must_plot=True  
    
    # run model
    
    if must_plot:
      import  matplotlib.pyplot as plt # grader gets upset by plot library 
      # plot model