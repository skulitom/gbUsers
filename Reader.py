import csv
from User import *
import datetime
import statistics


PROP_SUM = 10
CUT_POINT = 0.4

MAX_DISTANCE = 100
DISTANCE_PROP = 9
WEEK_PROP = PROP_SUM - DISTANCE_PROP

DISTANCE_LEN_PROP = 5
DISTANCE_SPR_PROP = PROP_SUM - DISTANCE_LEN_PROP


def main():
    print("Program Start")
    userList = []
    userStats = [0, 0]
    with open('train_set.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        firstRow = False
        for row in readCSV:
            found = False
            if not firstRow:
                firstRow = True
                continue
            for user in userList:
                if user.userID == row[1]:
                    found = True
                    user.append_user(row[2], row[3], row[5], row[6], row[7], row[8], row[9], row[10])
            if not found:
                userList.append(User(row[1], row[2], row[3], row[5], row[6], row[7], row[8], row[9], row[10]))
    for user in userList:
        user_analysis(user)
        if user.gbUser == 0:
            userStats[0] += 1
        else:
            userStats[1] += 1
    print("there are", userStats[0], "good users and", userStats[1],  "bad users")


def user_analysis(user):
    distanceVal = distance_analysis(user)
    weekVal = week_analysis(user)
    result = (DISTANCE_PROP*distanceVal + WEEK_PROP*weekVal)/100
    print(result)
    if result > CUT_POINT:
        user.gbUser = 1
    else:
        user.gbUser = 0


def distance_analysis(user):
    return DISTANCE_LEN_PROP * distance_length(user) + DISTANCE_SPR_PROP * distance_spread(user)


def distance_length(user):
    meanDistance = statistics.mean(user.distance)
    if meanDistance >= MAX_DISTANCE:
        return 1
    else:
        return meanDistance/MAX_DISTANCE


def distance_spread(user):
    meanDistance = statistics.mean(user.distance)
    sdDistance = statistics.stdev(user.distance)
    if sdDistance >= meanDistance:
        return 1
    else:
        return sdDistance/meanDistance


def week_analysis(user):
    return week_spread(user) + week_quantity(user) + week_cluster(user)


def week_spread(user):
    return 0


def week_quantity(user):
    return 0


def week_cluster(user):
    return 0


def get_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


if __name__ == '__main__':
    main()