import math
from math import pi


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
		K = .5  #the paper uses .5, assume need of 10hrs use.54
		return (- K )
	else:
		if Rt < 2880:
			return sleep_intensity(Rc,Rt,minute, peaks)
		else:
			return 0 

def sleep_intensity(Rc, Rt, minute,peaks):
	f = 0.0026564  #from the paper  # f = 0.00261  #trying new constant, this should be for a sleep need of about 9 hours
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


def set_sleep_schedule(time_in_minutes, sleep_hours):
	sleep_start = sleep_hours[0] * 60
	sleep_end = sleep_hours[1] * 60
	minutes_in_day = 24 * 60
	is_asleep = []
	for t in time_in_minutes:
		if sleep_hours[0] < sleep_hours[1]: #if bed time is same calendar day early in the morning
			asleep = ((t % minutes_in_day) > sleep_start) and ((t % minutes_in_day) < sleep_end)
		else:
			asleep = ((t % minutes_in_day) > sleep_start) or ((t % minutes_in_day) < sleep_end)
		is_asleep.append(asleep)

	return is_asleep


def set_circadian_peaks(to_sleep_time, wake_time):
	if to_sleep_time > wake_time: #if this is true, the sleep time is before midnight
		to_sleep_time -= 24 #subtract 24

	duration = wake_time - to_sleep_time
	Tmin = to_sleep_time + duration / 2 + 1.5
	p = Tmin + 14.5
	p2 = 3

	return {'p':p, 'p2': p2}



