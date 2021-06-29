import csv
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
from utils import *
from sleepdetectors import SLEEP_DETECTOR
from configs import *



Stat = namedtuple("Stat","Interval_Type  Interval  Start_Date  Start_Day  Start_Time  End_Date  End_Day  End_Time  Duration  Off_Wrist  Off_Wrist_Per  Total_AC  Avg_AC_min  Avg_AC_epoch  Std_AC  Max_AC  Inv_Time_AC  Invalid_AC_Per  Inv_Time_SW  Invalid_SW_Per  Onset_Latency  Snooze_Time  Efficiency  WASO  Wake_Time  Wake_Per  Wake_Bouts_Num  Avg_Wake_B  Sleep_Time  Sleep_Per  Sleep_Bouts_Num  Avg_Sleep_B  Immobile_Time  Immobile_Per  Imm_Bouts_Num  Avg_Imm_Bout  Mobile_Time  Mobile_Num  Mob_Bouts  Avg_Mob_Bout  Onemin_Imm_B_Num  Onemin_Imm_B_Per  Fragmentation  Exposure_White  Avg_White  Std_White  Max_White  TALT_White  Inv_Time_White  Invalid_White_Per  Exposure_Red  Avg_Red  Std_Red  Max_Red  TALT_Red  Inv_Time_Red  Invalid_Red_Per  Exposure_Green  Avg_Green  Std_Green  Max_Green  TALT_Green  Inv_Time_Green  Invalid_Green_per  Exposure_Blue  Avg_Blue  Std_Blue  Max_Blue  TALT_Blue  Inv_Time_Blue  Invalid_Blue_Per no_value")
Interval = namedtuple("Interval","Line Epoch Day Seconds Date Time Off_Wrist_Status Activity Marker White_Light Red_Light Green_Light Blue_Light SleepWake Mobility Interval_Status SW_Status no_value")



def load_file(data_file = DATA_FILE):
    stats = []
    intervals = []
    
    with open(data_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")

        for line in csv_reader:      
            if len(line) > 0 and line[0] == "DAILY":  
                stats.append(Stat(*line))
            elif len(line) == 18:
                intervals.append(Interval(*line))
    intervals = intervals[1:]
    return stats, intervals




valid_days = []
def log(*args):
    if LOGGING:
        print(*args)

def find_valid_days(data_file = DATA_FILE):
    stats, intervals = load_file(DATA_FILE)
    print(len(stats))
    print(len(intervals))
    ed = END_DAY if END_DAY >= 0 else len(stats)
    for day in range(START_DAY, ed + 1):
    
        day_intervals = [interval for interval in intervals if int(interval.Seconds)//86400 + 1 == day]
        times = [parse_time(interval.Time) for interval in day_intervals]
        activities = [float(interval.Activity) for interval in day_intervals]
        asleeps, blurred = SLEEP_DETECTOR(np.array(activities))


        if not less_than_four(stats[day - 1]):
            log(f"{day_intervals[0].Date} has more than 4 hours of off-wrist")
            continue
        
        max_count = 0
        cur_count = 0
    
        for asleep in asleeps:
            if asleep == 0:
                cur_count += 1
            else:
                if cur_count > max_count:
                    max_count = cur_count
                cur_count = 0
        
        if cur_count > max_count:
            max_count = cur_count
        if max_count > hours_to_intervals(MAX_SLEEP_HOURS):
            log(f"{day_intervals[0].Date} has too many sleep hours")
            continue


        for i in range(len(asleeps)):
            if day_intervals[i].Off_Wrist_Status == "1":
                asleeps[i] = AWAKE_NUM
        invalid_day = False

        for i in range(len(day_intervals)):
            if (i + PADDING < len(asleeps) and asleeps[i + PADDING] == 0) or (i - PADDING >= 0 and asleeps[i - PADDING] == 0):
                if day_intervals[i].Off_Wrist_Status == "1":
                    invalid_day = True
                    log(f"{day_intervals[0].Date} has off-wrist near a sleep period")
                    break
        if not invalid_day:
            valid_days.append(day_intervals[0].Date)

        if PLOTTING:
            plt.plot(times, activities)
            plt.plot(times, asleeps)
            if blurred is not None:
                plt.plot(times, blurred)
            plt.title(f"DAY {day}: {day_intervals[0].Date}")
            plt.show()
    return valid_days

if __name__ == "__main__":
    df = input("Enter file name: ")
    if len(df) == 0:
        df = DATA_FILE
    else:
        valid_days = find_valid_days(df)

    print("Valid Dates: ")
    for date in valid_days:
        print(f"\t{date}")
    print(f"Number of Valid Days: {len(valid_days)}")



