import datetime
import math
from dateutil.rrule import rrule, WEEKLY, MO, TU, WE, TH, FR, SU, SA


# def get_days(RecurrDays, RecurrPeriod):

def get_days(recure_game_type):
    try:
        recure_game_type_arr = recure_game_type.split("_")
        RecurrPeriod = int((datetime.datetime.strptime(recure_game_type_arr[1],
                                                       "%Y-%m-%d").date() - datetime.date.today()).days)

        if RecurrPeriod > 0:
            # recur_days = recur_model.get_days(RecurrDays=game_data[i]['gm_recurr_type'][2:],
            #                                     RecurrPeriod=math.ceil(RecurrPeriod / 7))
            RecurrDays = recure_game_type_arr[2:]
            RecurrPeriod = math.ceil(RecurrPeriod / 7)
            days = [MO, TU, WE, TH, FR, SU, SA]
            Recur_days = []
            recur_dates = []
            recur_days = []
            for i in days:
                if str(i).lower() in str(RecurrDays).lower():
                    Recur_days.append(i)
            for j in Recur_days:
                dates = list(rrule(freq=WEEKLY, count=RecurrPeriod, dtstart=datetime.date.today(), byweekday=j))
                recur_dates.append(dates)
            for i in range(len(Recur_days)):
                for j in range(RecurrPeriod):
                    if recur_dates[i][j]:
                        recur_days.append(str(recur_dates[i][j]).split(" ")[0])
            return recur_days
        else:
            return ""
    except Exception as e:
        return e.__str__()
