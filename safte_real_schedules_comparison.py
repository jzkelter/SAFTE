
#uncomment these to export the figure as an svg
# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
from safte_help import SAFTE_1, SAFTE_mult



def repeat_safte_1(sleep_times):
    #parameters to input: Rt, Rc, SI, I 
    start_t = 60 * 4  # start at 4 am when most people are asleep

    params = {
    'Rt': 2880 - ( .85 * (60 * sleep_times[0][1] - start_t)),
    'Rc': 2880,
    'SI': 1,
    'I': 0,
    }


    final_E_array = []
    final_hours_in_day = []

    i = 0  # counter variable
    for s in sleep_times:
        print "i: ", i, ". init_reservoir: ", params['Rc']
        hours_in_day, E_array, params = SAFTE_1(s, params)
        final_E_array += E_array
        final_hours_in_day += [h + (24 * i) for h in hours_in_day]
        i += 1

    return final_hours_in_day, final_E_array


def safte_with_variable_sleep_schedule(sleep_times):

    hours_in_day, E_array = SAFTE_mult(sleep_times)

    return hours_in_day, E_array




sleep_times = [[23,7.0],[4,5],[2,8],[2,8],[23,9],[23,10]]
#sleep_times = [[23,7.0]]


# get the hours in day and the effectiveness
hours_in_day, E_array = repeat_safte_1(sleep_times)  # repeating SAFTE_1
hours_in_day_2, E_array_2 = safte_with_variable_sleep_schedule(sleep_times)  # using regular safte with a variable sleep_schedule


#plotting functions
plt.plot(hours_in_day,E_array,linewidth=1, color='k')
plt.plot(hours_in_day_2, E_array_2, linewidth=1, color='b')

plt.ylabel("alertness")
xticks = range(int(hours_in_day_2[0]), int(hours_in_day_2[-1]))
#xtick_labels =[]
xtick_labels = [t % 24 for t in xticks]
plt.xticks(xticks,xtick_labels)

#plt.legend(['repeat_safte_1', "safte_with_variable_sleep_schedule"], loc='best')
plt.show()

#save fig
# plt.savefig('camp_practice.svg',figsize=(10,5))
