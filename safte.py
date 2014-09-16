
#uncomment these to export the figure as an svg
# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import math
from math import pi
from safte_help import *
import sys



num_days = 1 #number of days to calculate for

#Get the to bed times and wake times from the inputs. If none are provided, defaults are used
if len(sys.argv) > 1:
	to_sleep_time = int(sys.argv[1])
	wake_time = int(sys.argv[2])
else:
	to_sleep_time = 0
	wake_time = 8

circadian_peaks = set_circadian_peaks(to_sleep_time, wake_time) #get circadian peaks
print "sleep and wake times: ", to_sleep_time, wake_time
print "circadian peak: ", circadian_peaks['p']

start_t = wake_time - 3 #assume zero sleep debt starting at 
Rt = 2880 - ( .8 * 60 * (wake_time - start_t))#initial reservoir set so that it will be full on wake


#CONSTANTS
Rc = 2880  #reservoir capacity (this will be variable later)
ta = 0
SI_inertia = 1
end_t = num_days * 24 + start_t
I = 0


R_array = []
E_array = []
C_array = []

minutes_in_day = range(start_t * 60, (24 * num_days + start_t) * 60)
hours_in_day = [m / 60.0 for m in minutes_in_day]

is_asleep = set_sleep_schedule(minutes_in_day, [to_sleep_time, wake_time])


for m in minutes_in_day:
	sleeping = is_asleep[m - start_t * 60]
	Rt += update_res(sleeping, Rt, Rc, m, circadian_peaks)
	#print "T: ", (m/60.0), "   Rt: ", Rt
	if sleeping:
		Rc = update_res_capacity(Rt,Rc,m)

	R_array.append(100* Rt/Rc )

	C_array.append( 100 + Ct_adjusted(m,Rt,Rc,circadian_peaks))

	#for inertia term:
	if not sleeping and is_asleep[m - start_t * 60 - 1]: #if just awoke, initialize intertia stuff
		SI_inertia = sleep_intensity(Rc,Rt,m,circadian_peaks)
		ta = 0
	ta = ta + (ta<120)
	if ta < 120:
		I = inertia(ta,SI_inertia)
	else:
		I = 0

	E = 100 * (Rt / Rc) + Ct_adjusted(m,Rt,Rc,circadian_peaks) + I
	E_array.append(E)



#plotting functions
plt.plot(hours_in_day,E_array,linewidth=2.5)
plt.ylabel("alertness")


xticks = range(start_t, end_t)
#xtick_labels =[]
xtick_labels = [t % 24 for t in xticks]
plt.xticks(xticks,xtick_labels)

# yticks = range(70,95,5)
# plt.yticks(yticks,[])
plt.xlim([start_t,end_t])

plt.show()

#save fig

plt.savefig('camp_practice.svg',figsize=(10,5))



