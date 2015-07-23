import matplotlib.pyplot as plt
from safte_help import SAFTE_1, SAFTE_mult, repeat_safte_1
import basic_math as bm
from operator import add


#global variable
# sleep_times = [[1.28,8.98],[23.4,5.33], [23.4,5.33], [23.4,5.33]] 
sleep_times2 = ([[0,8]] * 8) 
# sleep_times = [[1.28,8.98],[23.4,5.33],[23.71,6.01],[22.15,5.25],[21.95,6.86]]

#methods for getting "typical" SAFTE output for a person
def many_days_of_average_sleep(sleep_times):
    """Ouput the average mental effectiveness using SAFTE of a person given past sleep times.
    This function averages all the sleeps and then runs SAFTE long enough to reach an equilibrium.
    Then it outputs the last day."""

    ave_IB_times = bm.mean_sleep_times(sleep_times)
    ave_sleep_times = ave_sleep_from_ave_TIB(ave_IB_times)

    #run SAFTE for many days 
    sleep_times = [ave_sleep_times] * 10
    hours_in_days, E_array_full = SAFTE_mult(sleep_times)

    #get the last day of the SAFTE outputs
    hours_in_1_day =  trim_to_first_x_days(hours_in_days, 1)
    E_array_1_day = trim_to_last_x_days(E_array_full,1)

    mean_sleep = ave_sleep_times[1] - ave_sleep_times[0]
    print "ave sleep: ",  mean_sleep ,"\t ME_max: ", max(E_array_1_day)
    return [hours_in_1_day, E_array_1_day]


def average_of_many_days(sleep_times):
    """Ouput the average mental effectiveness using SAFTE of a person given past sleep times.
    This function runs safte_mult(i.e. peaks are picked once based on average) for all the days, and then averages them."""

    n_days = len(sleep_times)
    n_starting_ave_days = 3
    ave_sleep_times = bm.mean_sleep_times(sleep_times) # get average sleep times
    sleep_times = [ave_sleep_times] * n_starting_ave_days + sleep_times  # we will run a few days of average sleep first, then the actual sleep to acount for unknown past

    hours_in_days, E_array_full = SAFTE_mult(sleep_times) # get safte output
    hours_in_1_day = trim_to_first_x_days(hours_in_days, 1) # get just one day of hours in day array

    E_array_trimmed = trim_to_last_x_days(E_array_full, n_days)
    E_array_averaged = average_sub_lists(E_array_trimmed, n_days)



    return [hours_in_1_day, E_array_averaged]


def ave_repeat_safte_1(sleep_times):
    """Ouput the average mental effectiveness using SAFTE of a person given past sleep times.
    This function runs repeat_safte_1 (i.e. peaks are picked every day) for all the days, and then averages them."""
    n_days = len(sleep_times)

    hours_in_days, E_array_full = repeat_safte_1(sleep_times) # get safte output

    hours_in_1_day = trim_to_first_x_days(hours_in_days, 1) # get just one day of hours in day array
    E_array_averaged = average_sub_lists(E_array_full, n_days)


    return [hours_in_1_day, E_array_averaged]

#*******end of "typical" SAFTE methods


#*******helper funcions************
def trim_to_last_x_days(array_by_minute, num_days):
    minutes_in_days = 60 * 24 * num_days
    trimmed_array = array_by_minute[-minutes_in_days:len(array_by_minute)]
    return trimmed_array

def trim_to_first_x_days(array_by_minute, num_days):
    minutes_in_days = 60 * 24 * num_days
    trimmed_array = array_by_minute[0:minutes_in_days]
    return trimmed_array

def split_list(list1, num_new_lists):
    sub_list_len = len(list1) / num_new_lists
    list_of_lists = []

    for n in range(num_new_lists):
        i0 = sub_list_len * n
        i1 = sub_list_len * (n + 1) 
        list_of_lists.append(list1[i0:i1])

    return list_of_lists

def average_sub_lists(list1, n_sub_lists):
    sub_lists = split_list(list1, n_sub_lists)
    summed_lists = [sum(x) for x in zip(*sub_lists)]
    average_sub_list = [x / n_sub_lists for x in summed_lists]
    return average_sub_list

def plot_arrays(arrays):

    for a in arrays:
        plt.plot(a[0],a[1])

    plt.show()

def sum_lists(lists):
    """input a list of lists of numbers. sum them elementwise"""
    return [sum(x) for x in zip(*lists)]

def ave_sleep_from_ave_TIB(IB_times):
    #takes in the average TIB and gives an average of time asleep
    TIB = IB_times[1] - IB_times[0]
    TST = 0.84 * TIB + 0.395
    wake_time = IB_times[1]
    sleep_time = wake_time - TST

    return [sleep_time, wake_time] 


#************end helper functions************


def max_ME_different_sleep():
    arrays = []
    for w in range(9,2,-1):
        sleep_times = [[0, w]] * 7
        arrays.append(many_days_of_average_sleep(sleep_times))

    plot_arrays(arrays)



max_ME_different_sleep()
# arrays = [many_days_of_average_sleep(sleep_times2)]
# plot_arrays(arrays)


