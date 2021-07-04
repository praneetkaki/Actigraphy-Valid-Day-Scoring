import csv
from collections import namedtuple
from tkinter.constants import OFF
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

def find_valid_days(data_file = DATA_FILE):
    log_str = ""
    def log(*args):
        if LOGGING:
            nonlocal log_str
            print(*args)
            log_str += " ".join([str(arg) for arg in args]) + "\n"
    
    valid_days = []
    stats, intervals = load_file(data_file)
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

        if not grayed_out_day(stats[day - 1]):
            log(f"{day_intervals[0].Date} has more than 2 hours of grayed out invalid data")
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

        off_wrists = []
        for i in range(len(asleeps)):
            if day_intervals[i].Off_Wrist_Status == "1":
                asleeps[i] = AWAKE_NUM
                off_wrists.append(OFF_WRIST_NUM) 
            else:
                off_wrists.append(None)
        invalid_day = False

        #TODO: Fix this
        asleeps2 = np.array(asleeps)
        consec_sleep_intervals = 0
        consec_awake_intervals = 0
        for i in range(len(asleeps2)):
            if asleeps2[i] == 0:
                consec_sleep_intervals += 1
            else: #if NOT asleep
                if consec_sleep_intervals > 0 and consec_sleep_intervals < MIN_SLEEP_AWAKE_PERIOD_TIME:
                    asleeps2[i - consec_sleep_intervals:i] = AWAKE_NUM
                consec_sleep_intervals = 0
        for i in range(len(asleeps2)):
            if asleeps2[i] == 0:
                if consec_awake_intervals > 0 and consec_awake_intervals < MIN_SLEEP_AWAKE_PERIOD_TIME:
                    asleeps2[i - consec_awake_intervals :i] = 0
                consec_awake_intervals = 0

            else: #if NOT asleep
                consec_awake_intervals += 1


        consec_off_wrist_time = 0
        current_off_wrist_status = False
        false_to_true = False

        for i in range(len(day_intervals)):
            if day_intervals[i].Off_Wrist_Status == "1":
                if not current_off_wrist_status and (i - PADDING >= 0 and asleeps[i - PADDING] == 0):
                    false_to_true = True
                current_off_wrist_status = True
                consec_off_wrist_time += 1
            else: #if it is NOT off wrist
                if current_off_wrist_status and consec_off_wrist_time >= hours_to_intervals(1):
                    if false_to_true:
                        invalid_day = True
                        log(f"{day_intervals[0].Date} has off-wrist within 10 minutes of a wake time")
                        break
                    if i + PADDING < len(asleeps) and asleeps[i + PADDING] == 0:
                        invalid_day = True
                        log(f"{day_intervals[0].Date} has off-wrist within 10 minutes of a bedtime")
                        break
                false_to_true = False
                current_off_wrist_status = False
                consec_off_wrist_time = 0
        if not invalid_day:
            if false_to_true:
                invalid_day = True
                log(f"{day_intervals[0].Date} has off-wrist within 10 minutes of a wake time")
            if i + PADDING < len(asleeps) and asleeps[i + PADDING] == 0:
                invalid_day = True
                log(f"{day_intervals[0].Date} has off-wrist within 10 minutes of a bedtime")
    
        if not invalid_day:
            valid_days.append(day_intervals[0].Date)

        if PLOTTING:
            plt.plot(times, activities, label = "Activity")
            plt.plot(times, asleeps, label = "Awake")
            plt.plot(times, off_wrists, label = "Off Wrist Status")
            plt.plot(times, asleeps2, label = "Asleeps 2")
            if blurred is not None:
                plt.plot(times, blurred)
            plt.title(f"DAY {day}: {day_intervals[0].Date}")
            plt.legend()
            plt.show()
    return valid_days, log_str


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

