
#uncomment these to export the figure as an svg
# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
from safte_help import SAFTE

num_days = int(raw_input('enter number of days: '))
to_sleep_time = float(raw_input('enter bed time: '))
wake_time = float(raw_input('enter wake time: '))



hours_in_day, E_array = SAFTE(num_days, to_sleep_time, wake_time)
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


#save fig
#plt.savefig('camp_practice.svg',figsize=(10,5))



while int(raw_input('enter 1 to add another graph, 0 to continue: ')):
	to_sleep_time = float(raw_input('enter new bed time: '))
	wake_time = float(raw_input('enter new wake time: '))
	hours_in_day, E_array = SAFTE(num_days, to_sleep_time, wake_time)
	plt.plot(hours_in_day, E_array, linewidth=2.5, color='b')


game_start = raw_input('enter a game time if you want (otherwise just hit enter): ')
if game_start:
	game_start = float(game_start)
	game_end = game_start + 3.2
	plt.plot([game_start,game_start], [min(E_array),max(E_array)], '--', color = 'k', linewidth=2)
	plt.plot([game_start + 3.2 ,game_start + 3.2], [min(E_array),max(E_array)], '--', color = 'k', linewidth=2)

plt.legend(['current schedule', "proposed schedule", "game time"], loc='best')
plt.show()

#save fig
# plt.savefig('camp_practice.svg',figsize=(10,5))
