from configs import *
from scipy.ndimage import gaussian_filter1d


def mean_threshold(arr_activities):
    WINDOW_SIZE = hours_to_intervals(2)
    THRESHOLD = 40
    asleeps = [0 if arr_activities[i - int(WINDOW_SIZE/2): i + int(WINDOW_SIZE/2)].mean() < THRESHOLD else AWAKE_NUM for i in range(len(arr_activities))]
    return asleeps, None

def mean_std_threshold(arr_activities):
    WINDOW_SIZE = hours_to_intervals(1.5)
    THRESHOLD = 60
    asleeps = [0 if arr_activities[i - int(WINDOW_SIZE/2): i + int(WINDOW_SIZE/2)].mean() + arr_activities[i - int(WINDOW_SIZE/2): i + int(WINDOW_SIZE/2)].std() < THRESHOLD else AWAKE_NUM for i in range(len(arr_activities))]
    return asleeps, None

def gaussian_blur_threshold(arr_activities):
    std = arr_activities.std()/4
    THRESHOLD = 50
    blurred = gaussian_filter1d(arr_activities, std)
    asleeps = [0 if b < THRESHOLD else AWAKE_NUM for b in blurred]
    return asleeps, blurred

def low_activity_threshold(arr_activities):
    WINDOW_SIZE = hours_to_intervals(2)
    THRESHOLD = 0.7 * WINDOW_SIZE
    LOW_ACTIVITY_THRESHOLD = 2
    asleeps = [0 if len(list(filter(lambda a: a < LOW_ACTIVITY_THRESHOLD , arr_activities[i - int(WINDOW_SIZE/2): i + int(WINDOW_SIZE/2)]))) > THRESHOLD else AWAKE_NUM for i in range(len(arr_activities))]
    return asleeps, None

SLEEP_DETECTOR = low_activity_threshold