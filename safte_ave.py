
#uncomment these to export the figure as an svg
# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
from safte_help import SAFTE_1

sleep_times = [23,7.5]
init_reservoir = 2880 - ( .85 * (60 * sleep_times[1] - sleep_times[0]))


hours_in_day, E_array = SAFTE_1(sleep_times, init_reservoir)
start_t = int(hours_in_day[0])
end_t = int(hours_in_day[-1])

#plotting functions
plt.plot(hours_in_day,E_array,linewidth=1, color='k')
plt.ylabel("alertness")
xticks = range(start_t, end_t)
#xtick_labels =[]
xtick_labels = [t % 24 for t in xticks]
plt.xticks(xticks,xtick_labels)
plt.xlim([start_t,end_t])


plt.show()

#save fig
# plt.savefig('camp_practice.svg',figsize=(10,5))
