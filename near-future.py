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

# A Model of Climate Chanhge Today
# https://www.coursera.org/learn/global-warming-model/home/week/5

import math,matplotlib.pyplot as plt

co2_at_equilibrium         = 280.0    # ppm
co2_initial                = 290.0    # ppm
co2_growth_exponent        = 0.0225   # per year
time_response              = 20       # Years
watts_m2_sx                = 4        # radiative forcing due to doubled CO2 

# Calculate radiative forcing from CO2
#
# Input:   CO2 ppm
# Output: Radiative Forcing W/(m*m)

def get_rf(co2):            # CO2 ppm
    # A function to determine the number of doubleins of CO2 compared to equilibrium
    def number_of_doublings_of_co2():
        return  math.log( co2/co2_at_equilibrium ) / math.log(2.0)
    return watts_m2_sx * number_of_doublings_of_co2()

# Calculate aerosol coefficient
#
# Given a year and a target, work out what aerosol_coefficient we
# need to use if the RF masking scaled is to match the target in the
# specified year
#

def get_aerosol_coefficient(years,             # The years used in the simulation
                            co2,               # CO2 ppm for each year
                            aerosol_Wm2_now,   # The masking effect for the target year
                            year=2015):        # The target year
    index = years.index(year)
    return aerosol_Wm2_now/((co2[index]-co2[index-1])/(years[index] - years[index-1]))  
    
#  Compute business as usual scenario
#
#  Inputs:
#       start       First year
#       end         Last Year
#       co2_initial CO2 ppm at start of first year
#
# Return (years,co2,rfco2,temp_eq,temp_trans)
#
# We can caluclate the CO2 and the radiative forcing in one loop, but the
# rf masking and temperatures depend on the aerosol_coefficient, which reqires
# the CO2, so there will be two loops

def business_as_usual(start=1900,
                      end=2100,
                      co2_initial=co2_initial,
                      climate_sensitivity_2x = 3.0,
                      aerosol_Wm2_now=-0.75,
                      time_step=5):
    years=[year for year in range(start,end+1,time_step)]
    
    co2 = [co2_initial]  # Initialize CO2 ppm
    rfco2 = [0]          # Initialize radiative forcing

    for year in years[1:]:
        co2.append(co2_at_equilibrium + (co2[-1]-co2_at_equilibrium) * (1 + co2_growth_exponent)**time_step)
        rfco2.append(get_rf(co2[-1]))

    aerosol_coefficient = get_aerosol_coefficient(years,co2,aerosol_Wm2_now)
    
    temp_eq=[0]
    temp_trans=[0]
    climateSensitivityWM2      = climate_sensitivity_2x/watts_m2_sx
    for i in range(1,len(years)):
        rfmask=max(((co2[i]-co2[i-1])/time_step)*aerosol_coefficient,aerosol_Wm2_now)
        rf_total=rfco2[i]+rfmask
        temp_eq.append(climateSensitivityWM2*rf_total)
        temp_trans.append(temp_trans[-1]+(temp_eq[-1]-temp_trans[-1])*time_step/time_response)
        
    return (years,co2,rfco2,temp_eq,temp_trans)

# This function is used by world_without_us to find where the CO2 crosses a specific threshold
def find_index_threshold_crossing(values,        # Values to search - e.g. CO2
                                  threshold):    # We want to find the index
                                                 # of the first position in values
                                                 # that exceeds thrshold
    for i in range(len(values)):
        if values[i]>=threshold:
            return i

# This function is used by world_without_us to decide how much to relax CO2

def relax_co2(co2,
              time_step,
              target_for_relaxing_co2=340,
              timescale_for_relaxing_co2 = 100):
    return ( target_for_relaxing_co2 - co2 ) * ( time_step / timescale_for_relaxing_co2)

# Calculate values for World without Us. It is meant to be executed after
# Business as Usual
#

def world_without_us(years,           # The years used for the Business as Usual Calculation
                     co2_bau,         # The Carbon dioxide PPM from Business
                                      # as Usual Calculation
                     rfco2_bau,       # Radiative forcing from CO2,
                                      # from the Business as Usual Calculation
                     temp_eq_bau,     # Equilibrium temperatures from
                                      # the Business as Usual Calculation
                     temp_trans_bau,  # Transient temperatures from the 
                                      # Business as Usual Calculation
                     threshold=400,   # W=orld Without Us begins to diverge
                                      # from Business as Usual after
                                      # CP2 ppm exceeds thrshold
                     climate_sensitivity_2x = 3.0): # Degrees per doubling
    time_step = years[1]-years[0]
    index = find_index_threshold_crossing(co2_bau,threshold)

    co2 = co2_bau[:index]                # Initialize for years before we cross threshold
    rfco2 = rfco2_bau[:index]            # Initialize for years before we cross threshold
    temp_eq = temp_eq_bau[:index]        # Initialize for years before we cross threshold
    temp_trans = temp_trans_bau[:index]  # Initialize for years before we cross threshold
    
    # Now calculate data after threshold crossing
    climateSensitivityWM2      = climate_sensitivity_2x/watts_m2_sx
    
    while (len(co2)<len(years)):
        co2.append(co2[-1]+relax_co2(co2[-1],time_step))
        rfco2.append(get_rf(co2[-1]))
        temp_eq.append(climateSensitivityWM2*rfco2[-1])
        temp_trans.append(temp_trans[-1]+(temp_eq[-1]-temp_trans[-1])*time_step/time_response) 
        
    return (co2,rfco2,temp_eq,temp_trans)

# get_climate_sensitivity_2x
#
# Helper funtion used by code tricks 1 and 3
#
# This function accepts a valus for aerosol_Wm2_now and determines the value
# of climate_sensitivity_2x which would give a specified target tmperature in a specified year.


def get_climate_sensitivity_2x(target_temp=0.8,
                               target_year=2015,
                               aerosol_Wm2_now=-0.75):
    # Equation solver
    # Good old fashioned, but reliable, binary search will do (performance is acceptable).
    # The solver assumes that xmin<= xmax, and the solution is within the range
    # It isn't bulletproof (may run forever if assumption violated) but, I haven't
    # seen this behaviour - and I don't expect it, given the physics!
    
    def solve(f,                        # solve f(x)==0
              xmin,                     # Assume solution>xmin
              xmax):                    # Assume solution<xmax
        x=0.5*(xmin+xmax)               # Mid point
        if xmax<xmin: return x          # Endpoints of range have converged
        y=f(x)
        if y<0: return solve(f,x,xmax)  # Solution is in top half of range
        if y>0: return solve(f,xmin,x)  # Solution is in lower half of range
        return x   
    
    # This is the function we are going to save for. Notice that we've subtracted the target_temperature,
    # so equation solver can use standard form (f(x)==0)
    def get_transient_temperature(climate_sensitivity_2x):
        (_,_,_,_,temp_trans)=business_as_usual(climate_sensitivity_2x=climate_sensitivity_2x,aerosol_Wm2_now=aerosol_Wm2_now)
        return temp_trans[index_target]-target_temp

    (years,_,_,_,_)=business_as_usual(climate_sensitivity_2x=0,aerosol_Wm2_now=aerosol_Wm2_now)
    index_target=years.index(target_year)
    return solve(get_transient_temperature,0,10)
 

# Code Trick https://www.coursera.org/learn/global-warming-model/exam/GQC5B/code-trick-aerosol-masking-and-our-future
# Question 1
# I am still confused by this - which units?

def code_trick1(target_temp=0.8,target_year=2015,aerosol_Wm2_now=-0.75):
    global figure_number
    (years,co2_bau,rfco2_bau,temp_eq_bau,temp_trans_bau)=business_as_usual()
    index_target=years.index(target_year)
    print ('Transient temperature in {0} is {1:.3f} C'.format(target_year,temp_trans_bau[index_target]))
    plt.plot(years, temp_trans_bau, 'b',label='BAU')
    plt.figure(figure_number)
    figure_number+=1
    plt.xlabel('Year')
    plt.ylabel('T Trans')
    plt.title('Code Trick 1')    
    return get_climate_sensitivity_2x(target_temp,target_year,aerosol_Wm2_now)

# Code Trick https://www.coursera.org/learn/global-warming-model/exam/GQC5B/code-trick-aerosol-masking-and-our-future
# Question 2

def code_trick2(target_year=2015,duration=2):
    global figure_number
    (years,co2_bau,rfco2_bau,temp_eq_bau,temp_trans_bau)=business_as_usual()
    (_,_,_,temp_trans_wwu)=world_without_us(years,co2_bau,rfco2_bau,temp_eq_bau,temp_trans_bau)
    index_target=years.index(target_year)
    bau2,=plt.plot(years[index_target:index_target+duration], temp_trans_bau[index_target:index_target+duration], 'b',label='BAU')
    wwu2,=plt.plot(years[index_target:index_target+duration], temp_trans_wwu[index_target:index_target+duration],'g',label='WWU')
    plt.figure(figure_number)
    figure_number+=1
    plt.legend([bau2,wwu2], ['Business as usual', 'World without us'])
    plt.xlabel('Year')
    plt.ylabel('T Trans')
    plt.title('Code Trick 2')

# Code Trick https://www.coursera.org/learn/global-warming-model/exam/GQC5B/code-trick-aerosol-masking-and-our-future
# Question 3

def code_trick3(target_temp=0.8,target_year=2015,aerosol_Wm2_now=-1.5):
    return get_climate_sensitivity_2x(target_temp,target_year,aerosol_Wm2_now)

# Code Trick https://www.coursera.org/learn/global-warming-model/exam/GQC5B/code-trick-aerosol-masking-and-our-future
# Question 4

def code_trick4():
    global figure_number
    aerosol_Wm2_now=-1.5
    climate_sensitivity_2x=code_trick1(aerosol_Wm2_now=aerosol_Wm2_now)
    (years,co2_bau,rfco2_bau,temp_eq_bau,temp_trans_bau)=business_as_usual(climate_sensitivity_2x=climate_sensitivity_2x,aerosol_Wm2_now=aerosol_Wm2_now,time_step=1)
    (_,_,_,temp_trans_wwu)=world_without_us(years,co2_bau,rfco2_bau,temp_eq_bau,temp_trans_bau,climate_sensitivity_2x=climate_sensitivity_2x)
    high_year=-1
    for year,tt1,tt2 in zip(years,temp_trans_bau,temp_trans_wwu):
        if year>=2015 and tt1<=tt2:
            print (year,tt1,tt2)
            high_year=year
    
    plt.figure(figure_number)
    figure_number+=1
    low=years.index(2014)-5
    high=years.index(high_year)+5
    bau2,=plt.plot(years[low:high], temp_trans_bau[low:high], 'b',label='BAU')
    wwu2,=plt.plot(years[low:high], temp_trans_wwu[low:high],'g',label='WWU')

    plt.legend([bau2,wwu2], ['Business as usual', 'World without us'])
    plt.xlabel('Year')
    plt.ylabel('T Trans')
    plt.title('Code Trick 4')

# Generate the plots required for code review

def plot_for_code_review():
    global figure_number
    (years,co2_bau,rfco2_bau,temp_eq_bau,temp_trans_bau)=business_as_usual()
    (co2_wwu,rfco2_wwu,temp_eq_wwu,temp_trans_wwu)=world_without_us(years,co2_bau,rfco2_bau,temp_eq_bau,temp_trans_bau)

    plt.figure(figure_number)
    figure_number+=1
    plt.subplot(211)    
    bau1,= plt.plot(years, co2_bau, 'b',label='BAU')
    wwu1,=plt.plot( years, co2_wwu,'g',label='WWU')
    plt.legend([bau1,wwu1], ['Business as usual', 'World without us'])
    plt.xlabel('Year')
    plt.ylabel(r'$CO_{2} ppm$')   
    plt.subplot(212)
    bau2,=plt.plot(years, temp_trans_bau, 'b',label='BAU')
    wwu2,=plt.plot(years, temp_trans_wwu,'g',label='WWU')
    plt.legend([bau2,wwu2], ['Business as usual', 'World without us'])
    plt.xlabel('Year')
    plt.ylabel('T Trans')
    plt.show()
    
if __name__=='__main__':
    figure_number = 1
    print ('Code Trick 1: Climate sensitivity 2X={0:.3f} degrees C for doubling CO2'.format(code_trick1()))
    code_trick2()
    print ('Code Trick 3: Climate sensitivity 2X={0:.3f} degrees C for doubling CO2'.format(code_trick3()))
    code_trick4()
    plot_for_code_review()