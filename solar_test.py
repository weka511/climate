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
    def rrr(true_longitude,latitude):
        return max([solar.surface_irradience(true_longitude,latitude,T) for T in (0,23)]) 

    x = np.linspace(0, 2*math.pi, num=360) 
    y = np.linspace(-math.pi/2,math.pi/2,num=20) 
    X, Y = np.meshgrid(x, y) 
    zz=np.vectorize(rrr)
    Z = zz(X,Y) 

    plt.pcolormesh(X, Y, Z, cmap = cm.gist_rainbow) 
    plt.show() 
    # Mean beam irradience at top of atmosphere   
    #beam_irradience_top=solar.beam_irradience(earth.a)
    #print ('Mean beam irradience at top of atmosphere = {0:6.2f} W/m2'.\
          #format(beam_irradience_top))
    

    ## Instananeous beam irradience at top of atmosphere
    #xs=[]
    #ys=[]
    #d0=-1
    #d1=-1

 
        
        #d2=earth.instantaneous_distance(i)
        #ys.append(solar.beam_irradience(d2))
        ##if d0>-1 and d1>-1:
            ##if d0>d1 and d1<d2:
                ##x=utilities.extremum(i-2,i-2,i,d0,d1,d2)
                ##d=earth.instantaneous_distance(x)
                ##irr=solar.beam_irradience(d)
                ##print ('Perihelion day={0:.3f}, distance={1:.3f}, irradiance={2:.2f}'.format(x,d,irr))
            ##if d0<d1 and d1>d2:
                ##x=utilities.extremum(i-2,i-2,i,d0,d1,d2)
                ##d=earth.instantaneous_distance(x) 
                ##irr=solar.beam_irradience(d)
                ##print ('Aphelion day={0:.3f}, distance={1:.3f}, irradiance={2:.2f}'.format(x,d,irr))
        ##d0=d1
        ##d1=d2
    #plt.figure(1,figsize=(12,12))
    #plt.subplot(221)

    #plt.title('Beam irradience at top of Mars atmosphere')
    #plt.xlabel('Areocentric longitude - degrees')
    #plt.ylabel('Beam irradience at top of Mars atmosphere - W/m2')
    ##add_text(min(ys),xs,ys)
    ##add_text(max(ys),xs,ys)
    #plt.grid(True)
    #plt.plot(xs,ys)

    ## Variation of solar declination angle  
    
    #x=[]
    #y=[]
    #for i in range(360):
        #x.append(i)
        #y.append(math.degrees(math.asin(earth.sin_declination(i))))

    #plt.subplot(222)
    #plt.title('Variation of solar declination angle')
    #plt.axis([0, 360, -25, 25])
    #plt.xlabel('Areocentric longitude - degrees')
    #plt.ylabel('Solar Declination Angle - degrees')
    #plt.grid(True)     
    #plt.plot(x,y)

    ## Diurnal Variation of Beam Irradience on a horizontal surface

    #plt.subplot(223)
    #plt.title('Diurnal Variation of Beam Irradience on a horizontal surface')
    #plt.xlabel('Solar Time - Hours')
    #plt.ylabel('Beam Irradiance - W/m2')
    #plot_irradiance(69,'r')
    #plot_irradiance(120,'g')
    #plot_irradiance(153,'b')
    #plot_irradiance(249,'c')
    #plot_irradiance(299,'m')
    #plt.axis([12, 20, 0, 600])
    #plt.legend(loc='upper right',title=r'$L_S$')
    #plt.grid(True)
    #plt.savefig('solar')
    #plt.show()    