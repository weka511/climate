# Copyright (C) 2015-2017 Greenweaves Software Pty Ltd

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

'''
Model for solar irradiation, based on Solar Radiation on Mars, 
 Joseph Appelbaum & Dennis Flood, Lewis Research Center, NASA 
'''

import math as m, kepler.solar as s, kepler.kepler as k,matplotlib.pyplot as plt
import kepler.solar as s, kepler.kepler as k, matplotlib.cm as cm
import numpy as np,itertools
from scipy.integrate import quad 

class Earth:
    def __init__(self):
        self.a=1.0
        self.longitude_of_perihelion=102.94719
        self.e=0.017
        self.obliquity=m.radians(23.4)
        
    def instantaneous_distance(self,true_longitude):
        '''
        Instantaneaous Distance from Sun in AU
        
        Parameters:
             true_longitude
        '''
        f = k.true_anomaly_from_true_longitude(true_longitude,PERH=self.longitude_of_perihelion)
        return k.get_distance_from_focus(f,self.a,e=self.e) 
    
    def sin_declination(self,true_longitude):
        '''
        Sine of declination
        
        Parameters:
             true_longitude        
        '''
        return s.sin_declination(self.obliquity,true_longitude)# math.sin(self.obliquity) * math.sin(true_longitude)
     
    def cos_zenith_angle(self,true_longitude,latitude,T):
        '''
        Cosine of zenith angle

        Renewable Energy 32 (2007) 1187-1205
        '''
        return s.cos_zenith_angle(self.obliquity,true_longitude,latitude,T)

def lat(i):
    if i<0:
        return '{0}S'.format(i)
    if i>0:
        return '{0}N'.format(i)
    return '0'

def true_longitude(day):
    M=2*m.pi*(day-2)/365 #perihelion Jan 3
    E=k.get_eccentric_anomaly(M,0.017)
    true_anomaly=k.get_true_anomaly(E,0.017)
    return k.true_longitude_from_true_anomaly(true_anomaly)
    
def declination(day): #Jan 1 is day zero
    return m.asin(s.sin_declination(m.radians(23.4),true_longitude(day)))

def lengths_of_months():
    return list(itertools.accumulate([31,28,31,30,31,30,31,31,30,31,30,31]))

earth = Earth()
solar = s.Solar(earth)

fig, ax = plt.subplots()
plt.figure(1,figsize=(40,40))
ax1=plt.subplot(221)

# Plot Solar declination of Earth

xs=list(range(0,366))
ys=[m.degrees(declination(day)) for day in xs]
plt.plot(xs,ys)
plt.title('Solar declination of Earth')
plt.ylabel('Declination - degrees')
ax1.set_xticks([i for i in lengths_of_months()])
ax1.set_xticklabels(['JFMAMJJASOND'[i] for i in range(0,12)])        


# Plot Length of Day

def day_length(day,latitude):
    return solar.length_of_day(true_longitude(day),m.radians(latitude))

ax2=plt.subplot(222)

x = np.linspace(0, 366) 
y = np.linspace(-90,  91) 

X, Y = np.meshgrid(x, y) 
Z = (np.vectorize(day_length))(X,Y) 

cax=plt.pcolormesh(X, Y, Z, cmap = cm.jet) 
cbar = fig.colorbar(cax)
#plt.xlim(-90,271)
#plt.ylim([-90,90])
ax2.set_xticks([i for i in lengths_of_months()])
ax2.set_xticklabels(['JFMAMJJASOND'[i] for i in range(0,12)])    
ax2.set_yticks([i for i in range(-90,91,30)])
ax2.set_yticklabels([lat(i) for i in range(-90,91,30)])
plt.title('Length of Day')


# Plot zenith angle at noon

def za_noon(day,latitude):
    return m.degrees(
        m.acos(
            s.cos_zenith_angle(m.radians(23.4),
                               true_longitude(day),
                               m.radians(latitude),
                               12)))

ax3=plt.subplot(223)

x = np.linspace(0, 366) 
y = np.linspace(-90,  90) 

X, Y = np.meshgrid(x, y) 
Z = (np.vectorize(za_noon))(X,Y) 

cax=plt.pcolormesh(X, Y, Z, cmap = cm.jet) 
cbar = fig.colorbar(cax)
#plt.xlim(-90,271)
#plt.ylim([-90,90])
ax3.set_xticks([i for i in lengths_of_months()])
ax3.set_xticklabels(['JFMAMJJASOND'[i] for i in range(0,12)])    
ax3.set_yticks([i for i in range(-90,90,30)])
ax3.set_yticklabels([lat(i) for i in range(-90,91,30)])
plt.title('Zenith Angle Noon')

     
 
 
# Surface Irradiance
 
         
def surface_irradience(day,latitude):
    return solar.surface_irradience_daily(true_longitude(day),m.radians(latitude))

ax4=plt.subplot(224)

x = np.linspace(0,366) 
y = np.linspace(-90,90) 

X, Y = np.meshgrid(x, y) 
Z = (np.vectorize(surface_irradience))(X,Y) 
#fig, ax = plt.subplots()
cax=plt.pcolormesh(X, Y, Z, cmap = cm.jet) 
cbar = fig.colorbar(cax)
#plt.xlim(-90,271)
#plt.ylim([-90,90])
ax4.set_xticks([i for i in lengths_of_months()])
ax4.set_xticklabels(['JFMAMJJASOND'[i] for i in range(0,12)])    
ax4.set_yticks([i for i in range(-90,91,30)])
ax4.set_yticklabels([lat(i) for i in range(-90,91,30)])
plt.title('Surface Irradiance')

plt.savefig('solar-tests.png')

plt.show() 
