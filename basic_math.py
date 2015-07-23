def mean(nlist):
    return float(sum(nlist)) / len(nlist)


def mean_bed_time(nlist):
    times = []
    for n in nlist:
        if n < 7:
            times.append(n)
        elif n > 20:
            times.append(n - 24)

    return mean(times)


def mean_sleep_times(sleep_times):
    bed_times = [s[0] for s in sleep_times]
    wake_times = [s[1] for s in sleep_times]    
    return [mean_bed_time(bed_times), mean(wake_times)]

