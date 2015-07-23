

from safte_help import SAFTE_mult
import basic_math as bm


#methods for getting "typical" SAFTE output for a person
def many_days_of_average_sleep(sleep_times):
    """Ouput the average mental effectiveness using SAFTE of a person given past sleep times.
    This function averages all the sleeps and then runs SAFTE long enough to reach an equilibrium.
    Then it outputs the last day."""

    ave_sleep_times = bm.mean_sleep_times(sleep_times)

    #run SAFTE for many days 
    sleep_times = [ave_sleep_times] * 10
    hours_in_days, E_array_full = SAFTE_mult(sleep_times)

    #get the last day of the SAFTE outputs
    hours_in_1_day =  trim_to_first_x_days(hours_in_days, 1)
    E_array_1_day = trim_to_last_x_days(E_array_full,1)
    return hours_in_1_day, E_array_1_day

#*******helper funcions************
def trim_to_last_x_days(array_by_minute, num_days):
    minutes_in_days = 60 * 24 * num_days
    trimmed_array = array_by_minute[-minutes_in_days:len(array_by_minute)]
    return trimmed_array

def trim_to_first_x_days(array_by_minute, num_days):
    minutes_in_days = 60 * 24 * num_days
    trimmed_array = array_by_minute[0:minutes_in_days]
    return trimmed_array

def format_sleep_times(start_times, end_times):
    sleep_times = []

    for i in range(len(start_times)):
        sleep_times.append([start_times[i], end_times[i]])

    return sleep_times

print format_sleep_times(start_times,end_times)

