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
# https://www.coursera.org/learn/global-warming-model/home/week/4
# 
# Based on shallow_template.py


#    ----V(00)-------V(01)--------V(02)----
#     |           |            |           |
#   U(00) H(00) U(01) H(01)  U(02) H(02) [U(03)]
#     |           |            |           |
#     ----V(10)-------V(11)--------V(12)----
#     |           |            |           |
#   U(10) H(10) U(11) H(11)  U(12) H(12) [U(13)]
#     |           |            |           |  
#     ----V(20)-------V(21)--------V(22)----
#     |           |            |           |
#   U(20) H(20) U(21) H(21)  U(22) H(22) [U(23)]
#     |           |            |           |  
#     ---[V(30)]-----[V(31)]------[V(32)]---


import numpy,math,matplotlib.pyplot as plt, matplotlib.ticker as tkr

# First we have some functions that implement rotation calculations

# Easier First Method: Loop over all rows and columns, and calculate

# rotU[irow,icol] = rotConst[irow] * U[irow,icol]

def easy_rotation():
  for i in range(nrow):
    for j in range(ncol):    
      rotU[i,j] = rotConst[i] * U[i,j]
      rotV[i,j] = -rotConst[i] * V[i,j]

# Interpolated rotation
def full_rotation():
  # interpolate the U and V values onto the cell centers.
  U_centre = numpy.zeros((nrow, ncol+1)) # Temporary - TODO just do this once when we initialize
  V_centre = numpy.zeros((nrow, ncol+1)) # Temporary - TODO just do this once when we initialize
  for i in range(nrow):
    for j in range(ncol):
      U_centre[i,j] = 0.5 *(U[i,j]+U[i,j+1])
      V_centre[i,j] = 0.5 *(V[i,j]+V[i+1,j])
      
# calculate the rotational transformation of U and V as gridded
# on the H points, by multiplying each array by rotConst[]. 
  rotU_centre = numpy.zeros((nrow, ncol+1)) # Temporary - TODO just do this once when we initialize
  rotV_centre = numpy.zeros((nrow, ncol+1)) # Temporary - TODO just do this once when we initialize
  for i in range(nrow):
    for j in range(ncol):    
      rotU_centre [i,j] = rotConst[i] * U_centre[i,j]
      rotV_centre [i,j] = -rotConst[i] * V_centre[i,j]
      
# Finally, the rotated velocities, placed at the cell centers,
# need to be back-interpolated to the grid locations where the
# velocities are. 
  for i in range(nrow):
    for j in range(ncol):
      rotU[i,j] = 0.5 *(rotU_centre[i,j]+rotU_centre[i,j+1])
      rotV[i,j] = 0.5 *(rotV_centre[i,j]+rotV_centre[i+1,j])  
      

# This is the rotation calculator to use if we want to ignore rotation altogether

def trivial_rotation():
  pass

"""
This is the work-horse subroutine.  It steps forward in time, taking ntAnim steps of
duration dT.  
"""

def animStep(calculate_rotation=trivial_rotation):    

    global stepDump, itGlobal
    
    # Time Loop
    for it in range(ntAnim):
    
        # Longitudinal Derivatives

        # Calculate dH/dX (variable dHdX), making sure to put the value in each
        # index [irow, icol] so that it applies to the horizontal velocity
        # at that index location (U[irow, icol]).
       
        for i in range(nrow):
            for j in range(ncol+1):     
                dHdX[i,j] = (H[i,j]-H[i,j-1])/dX

        # If the variable horizontalWrap is set to True, the flow out the 
        # right-hand side of the domain (U[:,ncol]) will equal the flow in 
        # from the left side (U[:,0]). (The colon means, in this case, "all rows")

        # Assume that there is are "ghost cells" at the right-hand end of the
        # U and H arrays. U[:,ncol] = U[:,0], and H[:,ncol] = H[:,0].

        # For example, if ncol = 3, the H values that are in the domain will have
        # indices 0, 1, and 2. For convenience, we'll set up an H[:,3] set of
        # cells, which equal the H[:,0] cells, so we can take a difference for
        # dHdX[:,3] from H[:,2] and our ghost H[:,3], which are on either side of U[:,2].

        # Or, if horizontalWrap is set to False, the U velocities at the
        # left and right sides of the domain will be set to zero.

        # Also calculate dU/dx (dUdX), again making sure that the result that
        # has index [irow, icol] applies to the elevation H[irow, icol]. Assume
        # that the ghost cells U[:,ncol] are already set, if it's wrapped, or
        # that the boundary velocities U[:,0] and U[:,ncol-1] = 0, if it's a wall. 
        # (There can be flow along the wall (V) but not through it (U)).
        for i in range(nrow):
            for j in range(ncol):         
                dUdX[i,j] = (U[i,j+1]-U[i,j])/dX
 
        #print ('U')
        #print (U)  
        #print ('H')
        #print (H)
        #print ('dHdX')        
        #print (dHdX) 
        #print ('dUdX')
        #print (dUdX) 
        
        # Encode Latitudinal Derivatives Here
        
        # Within a loop over all grid cells, calculate dHdY, remembering that
        # dHdy[irow, icol] should be comprised of H values that straddle a
        # particular V[irow, icol].
        
        for i in range(1,nrow):
            for j in range(ncol):
                dHdY[i,j] = (H[i,j]-H[i-1,j])/dY    #FIXME
        
                #The northern and southern boundaries of the domains are always walls.
                # This means that the flows at the north boundary (V[0,:]), and the
                # south (a ghost cell would be V[ncol,:]) are both set to zero. Assume
                # that this will be true going into this loop, and that the ghost cell exists.
        
                # The gradient in the surface elevation, dHdY, should be set to zero
                # at the top boundary. dHdY[0,:] would be used to calculate V[0,:],
                # which is going to be zero anyway. 
        
                dVdY[i,j] = (V[i+1,j]-V[i,j])/dY
       
        #print ('dHdY')        
        #print (dHdY)
        #print ('V')
        #print (V)
        #print ('dVdY')
        #print (dVdY)         
        # Rotation

        # The effect of Earth's rotation is to transfer velocity between the U
        # and V directions. There are two ways to calculate this effect:
        # an easy but somewhat biased way which will mostly work but lead to
        # some weird flow patterns, and a better way.
        # You don't have to do either one to pass the Code Check, but there
        # are optional code checkers for both schemes if you want to try your
        # hand. The two formulations diverge in longer simulations, where the
        # simpler method will generate diagonal "stripes" of water level 
        # (waves) across the grid, as an artifact of its less-accurate method.

        calculate_rotation()

        # Assemble the Time Derivatives Here
        # Encode the equations for dU/dT, dV/dT, and dH/dT, given above, by 
        # looping over the grid and calculating values to put in arrays dUdT,
        # dVdT, and dHdT. Be sure that the indices of the arrays correspond to
        # those of the arrays U, V, and H that they are going to update.
        # It's very easy to make a mistake of this type, and the flow results 
        #you get will be strange and non-physical.
       
        for i in range(nrow):
            for j in range(ncol):
                dUdT[i,j] = rotU[i,j] - flowConst * dHdX[i,j] - dragConst * U[i,j] + windU[i]
                dVdT[i,j] = rotV[i,j] - flowConst * dHdY[i,j] - dragConst * V[i,j]
                dHdT[i,j] = - ( dUdX[i,j] + dVdY[i,j] ) * HBackground / dX

        # Step Forward One Time Step
        # Step forward in time by looping over the grid, updating each variable
        # U, V, and H by adding the time derivative multiplied by the time step.           
        for i in range(nrow):
            for j in range(ncol):
                U[i,j]+=(dUdT[i][j]*dT)
                V[i,j]+=(dVdT[i][j]*dT)
                H[i,j]+=(dHdT[i][j]*dT)
                
        # Update the Boundary and Ghost Cells
        # At the end of each time step, do any maintenance that needs doing
        # for the ghost cells, which are cells at the edges that mirror other#
        # cells in the grid to make it easier to calculate spatial derivatives at the edges.

        #The velocities at the north wall should be zeroed.

        if horizontalWrap:
            # If the horizontal flow wraps around the grid (meaning: you should 
            # write to code to see if the variable horizontalWrap is set to a 
            # value of True, and if it is), set the ghost cells for U and H, for
            # indices [:, ncol], to equal their values at indices[:,0]. 
            # Your code should calculate new values for U and H in the leftmost
            # grid cell (column 0), while you need to update the ghost cell.
            # This is in column ncols, because the numbering of the columns starts
            # at 0. Columns numbered 0 to (ncols-1) are in the computational grid, 
            # and column number ncols is an "extra" ghost cell.            
            H[:, ncol] =  H[:, 0]
            U[:, ncol] =  U[:, 0]
        else:
            # If the flow doesn't wrap, set U = zero at the eastern and western
            # boundaries (indices [:,0] and [:,ncol]).
            U[:, 0] =  0
            U[:, ncol] =  0

        
#   Now you're done

    itGlobal = itGlobal + ntAnim

def createRotation(nrow,rotationScheme):   
    latitude = []
    rotConst = []

    for irow in range(0,nrow):
      if rotationScheme == "WithLatitude":
        latitude.append( meanLatitude + (irow - nrow/2) * dxDegrees )
        rotConst.append( -7.e-5 * math.sin(math.radians(latitude[-1]))) # s-1
      elif rotationScheme == "PlusMinus":
        rotConst.append( -3.5e-5 * (1. - 0.8 * ( irow - (nrow-1)/2 ) / nrow )) # rot 50% +-
      elif rotationScheme == "Uniform":
        rotConst.append( -3.5e-5 ) 
      else:
        rotConst.append( 0 )
    return (latitude,rotConst)

def createWind(nrow,windScheme):    
    windU = []
    for irow in range(0,nrow):
        if windScheme == "Curled":
            windU.append( 1e-8 * math.sin( (irow+0.5)/nrow * 2 * 3.14 ) ) 
        elif windScheme == "Uniform":
            windU.append( 1.e-8 )
        else:
            windU.append( 0 )
    return windU

def firstFrame():
    global fig, ax, hPlot
    fig, ax = plt.subplots()
    ax.set_title("H")   
    hh = H[:,0:ncol]
    loc = tkr.IndexLocator(base=1, offset=1)
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)
    grid = ax.grid(which='major', axis='both', linestyle='-')
    hPlot = ax.imshow(hh, interpolation='nearest', clim=(-0.5,0.5))   
    plotArrows()
    plt.show(block=False) 

def plotArrows():
    global quiv, quiv2
    xx = []
    yy = []
    uu = []
    vv = []
    for irow in range( 0, nrow ):
        for icol in range( 0, ncol ):
            xx.append(icol - 0.5)
            yy.append(irow )
            uu.append( U[irow,icol] * arrowScale )
            vv.append( 0 )
    quiv = ax.quiver( xx, yy, uu, vv, color='red', scale=1)
    for irow in range( 0, nrow ):
        for icol in range( 0, ncol ):
            xx.append(icol)
            yy.append(irow - 0.5)
            uu.append( 0 )
            vv.append( -V[irow,icol] * arrowScale )
    quiv2 = ax.quiver( xx, yy, uu, vv, color='red', scale=1)

def updateFrame():
    global fig, ax, hPlot, quiv, quiv2
    hh = H[:,0:ncol]
    hPlot.set_array(hh)
    quiv.remove()    
    quiv2.remove()
    plotArrows()
    plt.show( block=False )
    plt.pause(0.001)    
    fig.canvas.draw()
    print("Time: ", math.floor( itGlobal * dT / 86400.*10)/10, "days")
    
def textDump():
    print("time step ", itGlobal)    
    print("H", H)
    print("dHdX" )
    print( dHdX)
    print("dHdY" )
    print( dHdY)
    print("U" )
    print( U)
    print("dUdX" )
    print( dUdX)
    print("rotV" )
    print( rotV)
    print("V" )
    print( V)
    print("dVdY" )
    print( dVdY)
    print("rotU" )
    print( rotU)
    print("dHdT" )
    print( dHdT)
    print("dUdT" )
    print( dUdT)
    print("dVdT" )
    print( dVdT)

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
  print ('      -p --plot      Species that output is to be plotted')

  
# Determine revision number from subversion

def version(tag='$LastChangedRevision: 1066 $'):
  re_number=re.compile('.* ([0-9]+) .*')
  match=re_number.match(tag)
  return int(match.group(1))

# Shallow.py is ineteded to be executed from the command line. Paramters can be specified
# to control execution. If the program is executed with no paramters at all, it will execute
# with default values that correspond to 
# https://www.coursera.org/learn/global-warming-model/programming/023Rg/code-check
# i.e. for the grader: python shallow.py 
#
# To run the 1st code trick, use these values
#
# python shallow.py -c 10 -n 200 -a 200 -H -i -r PlusMinus -p -w 30 -g easy
#
#
# For the 2nd code trick
#
# python shallow.py -c 5 -n 400 -a 1000  -i -r PlusMinus -p -w 30 -s Curled -u -

if __name__=='__main__':
  # Set up defasult values for grader
  ncol = 5           # grid size (number of cells)
  nrow = ncol
  nSlices = 400         # maximum number of frames to show in the plot
  ntAnim = 1000  # number of time steps for each frame
  
  horizontalWrap = False # determines whether the flow wraps around, connecting
                         # the left and right-hand sides of the grid, 
                         # or whether there's a wall there. 
  interpolateRotation = True
  rotationScheme = "PlusMinus"   # "WithLatitude", "PlusMinus", "Uniform"
  
  # Note: the rotation rate gradient is more intense than the real world, so that
  # the model can equilibrate quickly.
  
  windScheme = 'Curled' #"Uniform"  # "Curled", "Uniform"
  initialPerturbation = ""    # "Tower", "NSGradient", "EWGradient"

  arrowScale = 30

  textOutput = False
  plotOutput = True  
  dT = 600 # seconds
  G = 9.8e-4 # m/s2, hacked (low-G) to make it run faster
  HBackground = 4000 # meters
  
  dX = 10.0E3 # meters, small enough to respond quickly.  This is a very small ocean
              # on a very small, low-G planet.  
  dY = dX        #FIXME
  
  dxDegrees = dX / 110.e3
  dyDegrees = dY / 110.e3
  flowConst = G  # 1/s2
  dragConst = 1.E-6  # about 10 days decay time
  meanLatitude = 30 # degrees
  rotationAlgorithm = full_rotation
 
  latitude,rotConst=createRotation(nrow,rotationScheme)
  windU = createWind(nrow,windScheme)

  itGlobal = 0

  U = numpy.zeros((nrow, ncol+1))
  V = numpy.zeros((nrow+1, ncol))
  H = numpy.zeros((nrow, ncol+1))
  dUdT = numpy.zeros((nrow, ncol))
  dVdT = numpy.zeros((nrow, ncol))
  dHdT = numpy.zeros((nrow, ncol))
  dHdX = numpy.zeros((nrow, ncol+1))
  dHdY = numpy.zeros((nrow, ncol))
  dUdX = numpy.zeros((nrow, ncol))
  dVdY = numpy.zeros((nrow, ncol))
  rotV = numpy.zeros((nrow,ncol)) # interpolated to u locations
  rotU = numpy.zeros((nrow,ncol)) #              to v
      
  midCell = int(ncol/2)
  if initialPerturbation == "Tower":
      H[midCell,midCell] = 1
  elif initialPerturbation == "NSGradient":
      H[0:midCell,:] = 0.1
  elif initialPerturbation == "EWGradient":
      H[:,0:midCell] = 0.1    
  
  if textOutput is True:
      textDump()
  if plotOutput is True:
      firstFrame()
  for i_anim_step in range(0,nSlices):
      animStep()
      if textOutput:
          textDump()
      if plotOutput:
          updateFrame()

# If we are doing a Code Check, need to make sure that we produce the required output

  if len(opts)==0:
    print(H[iRowOut,iColOut],dHdT[iRowOut,iColOut],U[iRowOut,iColOut],\
        V[iRowOut,iColOut],rotU[iRowOut,iColOut])
  
  if plotOutput:
    plt.show()
