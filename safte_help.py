import math
from math import pi
import basic_math as bm

#circadian component
def Ct(T, peaks):
	"""Returns the circadian component of alertness for an hour in the day T"""

	p = peaks['p'] #the time of the peak of the 24 hour rhythm
	p2 = peaks['p2'] #the realtive time of the 12 hour peak
	B = 0.5 #The relative amplitude of the 12 hour rhythm

	return math.cos(2 * pi * (T -p) / 24) + B * math.cos(4 * pi * ( T - p - p2) / 24)


def Ct_adjusted(m,Rt,Rc, peaks):
	"""Returns the circadian component of alertness for aa minute in the day m modified by 
	current reservoir level Rt and reservoir capacity Rc"""
	a1 = 7
	a2 = 5
	T = m / 60.0
	return Ct(T, peaks) * (a1 + a2 * (Rc - Rt) / Rc)


def update_res(is_asleep, Rt, Rc, minute, peaks):

	if not is_asleep:
		K = .50  #the paper uses .5, assume need of 10hrs use.54
		return (- K )
	else:
		if Rt < 2880:
			return sleep_intensity(Rc,Rt,minute, peaks)
		else:
			return 0 

def sleep_intensity(Rc, Rt, minute,peaks):
	f = 0.0026564  #from the paper 0.0026564 # trying new constant, this should be for a sleep need of about 9 hours, f = 0.00261  
	a = 0.55
	T = minute / 60.0
	SI = (-a) * Ct(T,peaks) + f * (Rc - Rt)
	max_SI = 4.4
	if SI <= max_SI:
		return SI
	else:
		return max_SI
	
def update_res_capacity(Rt,Rc,t):
	k1 = 0.22 # down-regulation time constant
	k2 = 0.5 #the reference level for Sleep intensity regulation
	k3 = 0.0015 #recovery time constant; from the paper
	f = 0.00312
	SD = f * (Rc - Rt)
	t = t % (24 * 60)

	new_Rc = Rc +  (k1 * (1 - (SD / k2)) + k3 * ( 2880 - Rc))

	if new_Rc < 2880:
		return new_Rc
	else:
		return 2880

def inertia(ta,SI):
	Imax = -5 #in %reaction time
	i = 0.04 #inertia time constant
	return Imax * math.exp(-(i * ta / SI))


def set_1_night_sleep_schedule(time_in_minutes, sleep_hours):
	if sleep_hours[0] < 0:
		sleep_hours[0] +=24
		
	sleep_start = sleep_hours[0] * 60
	sleep_end = sleep_hours[1] * 60
	minutes_in_day = 24 * 60
	is_asleep = []
	for t in time_in_minutes:
		if sleep_hours[0] < sleep_hours[1]: #if bed time is after midnight
			asleep = ((t % minutes_in_day) > sleep_start) and ((t % minutes_in_day) < sleep_end)
		else:  # if bed time is before midnight
			asleep = ((t % minutes_in_day) > sleep_start) or ((t % minutes_in_day) < sleep_end)
		is_asleep.append(asleep)

	return is_asleep


def set_sleep_schedule(start_t, sleep_times):
	"""
	Outputs an array with the sleep schedule. 
	Each cell of the array represents a minute: 1 if sleeping, 0 i awake.
	Inputs: a list of lists with sleep start and end times.
	"""
	end_t = int(24 * 60 + start_t )

	time_in_minutes = range(start_t,end_t)
	sleep_schedule = []

	for s in sleep_times:
		sleep_schedule += set_1_night_sleep_schedule(time_in_minutes, s)

	return sleep_schedule



def set_circadian_peaks(to_sleep_time, wake_time):
	if to_sleep_time > wake_time: #if this is true, the sleep time is before midnight
		to_sleep_time -= 24  # subtract 24 to make the to sleep time "negative" i.e. 11pm becomes -1am

	duration = wake_time - to_sleep_time
	Tmin = to_sleep_time + duration / 2 + 1
	p = Tmin + 14 
	p2 = 3

	return {'p':p, 'p2': p2}


def SAFTE(num_days, to_sleep_time, wake_time):
	"""outputs SAFTE model for the given number of days with the given sleep and wake times."""
	#set start time and initial reservoir
	start_t = int(60 * (wake_time - 3)) #assume zero sleep debt starting at 
	Rt = 2880 - ( .85 * (60 * wake_time - start_t)) #initial reservoir set so that it will be full on wake

	#Constants
	Rc = 2880  #reservoir capacity (this will be variable later)
	ta = 0  # time since awakening (used for sleep intertia)
	SI_inertia = 1
	end_t = int(num_days * 24 * 60 + start_t )
	I = 0

	#set circadian peaks 
	#TO CHANGE: Right now this is based only on last nights sleep. It should be based on historical sleep and shift slowly over time
	circadian_peaks = set_circadian_peaks(to_sleep_time, wake_time) 

	print "circadian peak: ", circadian_peaks['p']

	#get the minutes and hours of the range
	minutes_in_day = range( start_t , end_t)
	hours_in_day = [m / 60.0 for m in minutes_in_day]
	is_asleep = set_1_night_sleep_schedule(minutes_in_day, [to_sleep_time, wake_time])


	#initialize arrays
	R_array = []
	E_array = []
	C_array = []

	#fill arrays
	for m in minutes_in_day:
		sleeping = is_asleep[m - start_t]  # bool: asleep or not
		Rt += update_res(sleeping, Rt, Rc, m, circadian_peaks)

		if sleeping:
			Rc = update_res_capacity(Rt,Rc,m)

		R_array.append(100* Rt/Rc )

		C_array.append( 100 + Ct_adjusted(m,Rt,Rc,circadian_peaks))

		#for inertia term:
		if not sleeping and is_asleep[m - start_t - 1]: #if just awoke, initialize intertia stuff
			SI_inertia = sleep_intensity(Rc,Rt,m,circadian_peaks)
			ta = 0
		ta = ta + (ta<120)
		if ta < 120:  # if withing 2 hours of waking, set inertia
			I = inertia(ta,SI_inertia)
		else:  # if more than 2 hrs after waking, intertia is 0
			I = 0


		E = 100 * (Rt / Rc) + Ct_adjusted(m,Rt,Rc,circadian_peaks) + I
		E_array.append(E)

	return hours_in_day, E_array 


def SAFTE_1(sleep_times, params):
	#parameters to input: Rt, Rc, SI, I 

	"""outputs SAFTE model for 1 of day with the given sleep and wake times."""
	#set start time and initial reservoir
	start_t = 60 * 4  #units: minutes. For now, days start at 4am (b.c. most people are assleep then)
	end_t = int(start_t + 24 * 60)  # end time is a day after start time
	Rt = params['Rt']  # initialize the reservoir
	Rc = params['Rc']  #initial reservoir capacity (this )
	ta = params['ta']  # time since awakening (used to calculate sleep intertia)
	#Variables
	SI= params['SI']  # sleep intensity (this changes as reservoir changes, and also effects inertial)
	I = params['I']  # initial sleep inertia is zero

	#set circadian peaks
	circadian_peaks = set_circadian_peaks(sleep_times[0], sleep_times[1]) #get circadian peaks

	print "circadian peak: ", circadian_peaks['p']

	#get the minutes and hours of the range
	minutes_in_day = range( start_t , end_t)
	hours_in_day = [m / 60.0 for m in minutes_in_day]
	is_asleep = set_1_night_sleep_schedule(minutes_in_day, sleep_times)

	#initialize arrays
	R_array = []
	E_array = []
	C_array = []

	#fill arrays
	for m in minutes_in_day:
		sleeping = is_asleep[m - start_t ]
		Rt += update_res(sleeping, Rt, Rc, m, circadian_peaks)
		#print "T: ", (m/60.0), "   Rt: ", Rt
		if sleeping:
			Rc = update_res_capacity(Rt,Rc,m)

		R_array.append(100* Rt/Rc )

		C_array.append( 100 + Ct_adjusted(m,Rt,Rc,circadian_peaks))

		#if just woke up, reset inertia term
		if not sleeping and is_asleep[m - start_t - 1]: #if just awoke, initialize intertia stuff
			SI = sleep_intensity(Rc,Rt,m,circadian_peaks)
			ta = 0

		#adjust interia term
		ta = ta + (ta<120)
		if ta < 120:
			I = inertia(ta,SI)
		else:
			I = 0

		E = 100 * (Rt / Rc) + Ct_adjusted(m,Rt,Rc,circadian_peaks) + I
		E_array.append(E)

	parameters = {  # get the parameters for the next run
    'Rt': Rt,
    'Rc': Rc,
    'SI': SI,
    'I': I,
    'ta':ta
    }
	return hours_in_day, E_array, parameters


def repeat_safte_1(sleep_times):
	"""Runs Safte_1 for multiple nights and outputs the results"""
    #parameters to input: Rt, Rc, SI, I 
	start_t = 60 * 4  # start at 4 am when most people are asleep

 	params = {
	'Rt': 2880 - ( .85 * (60 * sleep_times[0][1] - start_t)),
	'Rc': 2880,
    'SI': 1,
    'I': 0,
    'ta':0
    }


   	final_E_array = []
   	final_hours_in_day = []

   	i = 0  # counter variable
   	for s in sleep_times:
   	    hours_in_day, E_array, params = SAFTE_1(s, params)
   	    final_E_array += E_array
   	    final_hours_in_day += [h + (24 * i) for h in hours_in_day]
   	    i += 1

   	return final_hours_in_day, final_E_array

def SAFTE_mult(sleep_times):
	#TO DO: update circadian peaks
	"""outputs SAFTE model for multiple days give sleep times."""
	#set start time and initial reservoir
	num_days = len(sleep_times)
	first_wake = sleep_times[0][1] * 60
	start_t = 60 * 4  # start at 4 am when most people are asleep
	Rt = 2880 - ( .85 * (first_wake - start_t)) #initial reservoir set so that it will be full on wake

	#Constants
	Rc = 2880  #reservoir capacity (this will be variable later)
	ta = 0  # time since awakening (used for sleep intertia)
	SI = 1
	end_t = int(num_days * 24 * 60 + start_t )
	I = 0

	#set circadian peaks
	ave_sleep_times = bm.mean_sleep_times(sleep_times)
	circadian_peaks = set_circadian_peaks(ave_sleep_times[0], ave_sleep_times[1]) #get circadian peaks

	#get minutes/hours in day and sleep schedule
	minutes_in_day = range( start_t , end_t)
	hours_in_day = [m / 60.0 for m in minutes_in_day]
	is_asleep = set_sleep_schedule(start_t, sleep_times)


	#initialize arrays
	R_array = []
	E_array = []
	C_array = []

	#fill arrays
	for m in minutes_in_day:
		sleeping = is_asleep[m - start_t ]
		Rt += update_res(sleeping, Rt, Rc, m, circadian_peaks)
		#print "T: ", (m/60.0), "   Rt: ", Rt
		if sleeping:
			Rc = update_res_capacity(Rt,Rc,m)

		R_array.append(100* Rt/Rc )

		C_array.append( 100 + Ct_adjusted(m,Rt,Rc,circadian_peaks))

		#for inertia term:
		if not sleeping and is_asleep[m - start_t - 1]: #if just awoke, initialize intertia stuff
			SI = sleep_intensity(Rc,Rt,m,circadian_peaks)
			ta = 0
		ta = ta + (ta<120)
		if ta < 120:
			I = inertia(ta,SI)
		else:
			I = 0

		E = 100 * (Rt / Rc) + Ct_adjusted(m,Rt,Rc,circadian_peaks) + I
		E_array.append(E)




	return hours_in_day, E_array




