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

class Earth:
    def __init__(self):
        self.a=1.0
        self.longitude_of_perihelion=102.94719
        self.e=0.017
        self.obliquity=23.4
        
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
        return math.sin(self.obliquity) * math.sin(true_longitude)
     
    def cos_zenith_angle(self,true_longitude,latitude,T):
        '''
        Cosine of zenith angle
        Appelbaum & Flood equation (6)
        See also Derivation of the solar geometric 
        relationships using vector analysis by Alistair Sproul

        Renewable Energy 32 (2007) 1187-1205
        '''
        sin_declination=self.sin_declination(true_longitude)
        cos_declination=math.sqrt(1-sin_declination*sin_declination)
        return math.sin(latitude)*sin_declination +            \
            math.cos(latitude)*cos_declination *  math.cos(self.hour_angle(T))
    
    def hour_angle(self,T):
        '''
        Hour angle
        Appelbaum & Flood equation (8)
        Parameters:
             T     Time in Planetary hours
        '''
        return math.radians(15*T-180)   

    
if __name__=='__main__':
    import math, matplotlib.pyplot as plt,  kepler.solar as s, kepler.kepler as k, matplotlib.cm as cm, numpy as np
    from scipy.integrate import quad       

    earth = Earth()
    solar = s.Solar(earth)
    def surface_irradience(true_longitude,latitude):
        return sum([solar.surface_irradience(math.radians(true_longitude),math.radians(latitude),T) for T in range(0,23)]) 

    x = np.linspace(-90, 270,num=360) 
    y = np.linspace(-90,90,num=180) 
    X, Y = np.meshgrid(x, y) 
    Z = (np.vectorize(surface_irradience))(X,Y) 
    fig, ax = plt.subplots()
    cax=plt.pcolormesh(X, Y, Z, cmap = cm.jet) 
    cbar = fig.colorbar(cax)
    plt.ylim([-90,90])
    plt.title('Surface Irradiance')
    plt.show() 
