import csv
from User import *
import statistics


MAX_DISTANCE = 20


def main():
    print("Program Start")
    userList = []
    userStats = [0, 0]
    with open('train_set.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            found = False
            for user in userList:
                if user.userID == row[1]:
                    found = True
                    user.appendUser(row[2], row[3], row[5], row[6], row[7], row[8], row[9], row[10])
            if not found:
                userList.append(User(row[1], row[2], row[3], row[5], row[6], row[7], row[8], row[9], row[10]))
    for user in userList:
        userAnalysis(user)
        if user.gbUser == 0:
            userStats[0] += 1
        else:
            userStats[1] += 1
    print("there are ", userStats[0], "good users and ", userStats[1],  " bad users")


def userAnalysis(user):
    distanceAnalysis(user)


def distanceAnalysis(user):
    print("empty")

if __name__ == '__main__':
    main()