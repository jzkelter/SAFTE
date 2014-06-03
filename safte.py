import matplotlib.pyplot as plt
import math
from math import pi
from safte_help import *

#CONSTANTS
Rc = 2880  #reservoir capacity (this will be variable later)
start_t = 8 #assume zero sleep debt starting at 
num_days = 6
ta = 0
SI_inertia = 1
I = 0
Rt = 2880 #reservoir starts out full

times = [i / 60.0 for i in range(0,60*24)]
circadian = [7 * Ct(t) for t in times]

R_array = []
E_array = []
C_array = []
minutes_in_day = range(start_t * 60, (24 * num_days + start_t) * 60)
is_asleep = [((m % (24*60))< (6.5 * 60)) for m in minutes_in_day]
#set_sleep_schedule(start_t,[[0,6],[0,8]])
#[0 * m + 1 for m in minutes_in_day]
#

for m in minutes_in_day:
	sleeping = is_asleep[m- start_t * 60]
	Rt += update_res(sleeping, Rt, Rc, m)

	if sleeping:
		Rc = update_res_capacity(Rt,Rc,m)

	R_array.append(100* Rt/Rc )

	C_array.append( 100 + Ct_adjusted(m,Rt,Rc))

	#for inertia term:
	"""something is wrong. sleep inertia should start high and decrease"""
	if not sleeping and is_asleep[m - start_t * 60 - 1]: #if just awoke, initialize intertia stuff
		SI_inertia = sleep_intensity(Rc,Rt,m)
		ta = 0
	ta = ta + (ta<120)
	if ta < 120:
		I = inertia(ta,SI_inertia)
		print ta, I
	else:
		I = 0

	E = 100 * (Rt / Rc) + Ct_adjusted(m,Rt,Rc) + I
	E_array.append(E)




#plt.plot(R_array)
plt.plot(E_array)
#plt.plot(R_array)
#plt.plot(C_array)
plt.show()


# c2 = [Ct_adjusted(t,1000,Rc) for t in times]
# plt.plot(times,c2)
# plt.xlabel('hour of day')
# plt.ylabel('alertness')
# plt.show()

