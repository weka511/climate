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
        Appelbaum & Flood equations (2) & (3)
        Parameters:
             true_longitude
        '''
        f = k.true_anomaly_from_true_longitude(true_longitude,PERH=self.longitude_of_perihelion)
        return k.get_distance_from_focus(f,self.a,e=self.e) 
    
    def sin_declination(self,true_longitude):
        '''
        Sine of declination
        Appelbaum & Flood equation (7)
        Parameters:
             true_longitude        
        '''
        return s.sin_declination(self.obliquity,true_longitude)# math.sin(self.obliquity) * math.sin(true_longitude)
     
    def cos_zenith_angle(self,true_longitude,latitude,T):
        '''
        Cosine of zenith angle
        Appelbaum & Flood equation (6)
        See also Derivation of the solar geometric 
        relationships using vector analysis by Alistair Sproul

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

days=list(itertools.accumulate([31,28,31,30,31,30,31,31,30,31,30,31])) 
earth = Earth()
solar = s.Solar(earth)

fig, ax = plt.subplots()
plt.figure(1,figsize=(20,20))
ax1=plt.subplot(221)

xs=list(range(0,366))
ys=[m.degrees(declination(day)) for day in xs]
plt.plot(xs,ys)
plt.title('Solar declination of Earth')
plt.ylabel('Declination - degrees')
ax1.set_xticks([i for i in days])
ax1.set_xticklabels(['JFMAMJJASOND'[i] for i in range(0,12)])        
plt.savefig('declination.png')

ax2=plt.subplot(222)

def day_length(day,latitude):
    phi=true_longitude(day)
    ha1=solar.ha_sunrise_sunset(phi,m.radians(latitude),sunset=False)
    ha2=solar.ha_sunrise_sunset(phi,m.radians(latitude))
    print ('{0:7.2f}, {1:7.2f}, {2:7.2f}'.format(phi,latitude,m.degrees(ha2-ha1)/15))
    return m.degrees(ha2-ha1)/15

x = np.linspace(0, 366) 
y = np.linspace(-90,  90) 

X, Y = np.meshgrid(x, y) 
Z = (np.vectorize(day_length))(X,Y) 

cax=plt.pcolormesh(X, Y, Z, cmap = cm.jet) 
cbar = fig.colorbar(cax)
#plt.xlim(-90,271)
#plt.ylim([-90,90])
ax2.set_xticks([i for i in days])
ax2.set_xticklabels(['JFMAMJJASOND'[i] for i in range(0,12)])    
ax2.set_yticks([i for i in range(-90,90,30)])
ax2.set_yticklabels([lat(i) for i in range(-90,91,30)])
plt.title('Length of Day')
plt.savefig('length-of-day.png')
#plt.show()     
 
 
 #for latitude in range(-90,90,10):
     #for longitude in range(-90,271,12):
         #print (longitude,latitude,solar.ha_sunrise_sunset(longitude,latitude))
         
 #def surface_irradience(true_longitude,latitude):
     #return sum([solar.surface_irradience(math.radians(true_longitude),math.radians(latitude),T) for T in range(0,23)]) 

 #x = np.linspace(-90, 270,num=360) 
 #y = np.linspace(-90,90,num=180) 

 #X, Y = np.meshgrid(x, y) 
 #Z = (np.vectorize(surface_irradience))(X,Y) 
 #fig, ax = plt.subplots()
 #cax=plt.pcolormesh(X, Y, Z, cmap = cm.jet) 
 #cbar = fig.colorbar(cax)
 #plt.xlim(-90,271)
 #plt.ylim([-90,90])
 #ax.set_xticks([i for i in range(-90,271,30)])
 #ax.set_xticklabels(['JFMAMJJASOND'[i] for i in range(0,12)])    
 #ax.set_yticks([i for i in range(-90,91,30)])
 #ax.set_yticklabels([lat(i) for i in range(-90,91,30)])
 #plt.title('Surface Irradiance')
 #plt.savefig('surface.png')
 #plt.show() 
