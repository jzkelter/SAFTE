import math
from math import pi

#circadian component
def Ct(T):
	"""Returns the circadian component of alertness for an hour in the day T"""
	p = 18 #the time of the peak of the 24 hour rhythm
	p2 = 3 #the realtive time of the 12 hour peak
	B = 0.5 #The relative amplitude of the 12 hour rhythm

	return math.cos(2 * pi * (T -p) / 24) + B * math.cos(4 * pi * ( T - p - p2) / 24)


def Ct_adjusted(m,Rt,Rc):
	"""Returns the circadian component of alertness for aa minute in the day m modified by 
	current reservoir level Rt and reservoir capacity Rc"""
	a1 = 7
	a2 = 5
	T = m / 60.0
	return Ct(T) * (a1 + a2 * (Rc - Rt) / Rc)


def update_res(is_asleep, Rt, Rc, minute):

	if not is_asleep:
		K = 0.5
		return (- K )
	else:
		if Rt < 2880:
			return sleep_intensity(Rc,Rt,minute)
		else:
			return 0 

def sleep_intensity(Rc, Rt, minute):
	f = 0.0026564
	a = 0.55
	T = minute / 60.0
	SI = (-a) * Ct(T) + f * (Rc - Rt)
	max_SI = 4.4
	if SI <= max_SI:
		return SI
	else:
		return max_SI
	
def update_res_capacity(Rt,Rc,t):
	k1 = 0.22 # down-regulation time constant
	k2 = 0.5 #the reference level for Sleep intensity regulation
	k3 = 0.0015 #recovery time constant
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


def set_sleep_schedule(start_time, days, sleep_hours):
	return
