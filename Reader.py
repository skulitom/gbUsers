import csv
from User import *
from matplotlib import pyplot as plt
import datetime
import numpy
import datetime
import statistics


PROP_SUM = 10
CUT_POINT = 0.4

MAX_DISTANCE = 100
DISTANCE_PROP = 0
WEEK_PROP = PROP_SUM - DISTANCE_PROP

DISTANCE_LEN_PROP = 5
DISTANCE_SPR_PROP = PROP_SUM - DISTANCE_LEN_PROP

MAX_NUM_HOURS = 5
MAX_DRIVES = 6
DAY_SPREAD_PROP = 10
DAY_QUANT_PROP = 0
DAY_CLUST_PROP = PROP_SUM - DAY_QUANT_PROP - DAY_SPREAD_PROP


standArray = [0,1,2,3,4,5,6,7,8,9,10]
results = []
coverageAr = []
top3precis = []
userNum = []


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
                   user.append_user(row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
           if not found:
               userList.append(User(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]))
   day_time_consts = []
   for user in userList:
       standard_approach(user)
       times = get_test_weekday_start_time(user)
       day_time_consts.append(get_day_time_consistency(times))
   fresult = polyfit(day_time_consts, top3precis, 1)
   print(fresult)
   plot(day_time_consts, coverageAr, 'Time Consistency', 'Coverage')


def plot(x, y, label2, label1):
   plt.plot(x, y, 'o')

   for i, txt in enumerate(userNum):
       plt.annotate(txt, (x[i], y[i]))

   z = numpy.polyfit(x, y, 1)
   p = numpy.poly1d(z)

   plt.plot(x, p(x), "r--")
   title = label1+' vs '+ label2
   plt.title(title)
   plt.ylabel(label1)
   plt.xlabel(label2)

   plt.legend()

   plt.grid(True, color='k')

   plt.show()


def standard_approach(user):
   userNum.append(user.userID)
   std_coverage(user)
   std_top3precision(user)


def get_day_time_consistency(times):
   good_times = get_half_good_times(times)
   bad_times = get_half_bad_times(times)
   #print(times[:int(len(times)/2)])
   if len(times) > 2:
       if bad_times < 1:
           return 0 + 0.5*get_day_time_consistency(times[:int(len(times)/2)]) + 0.5*get_day_time_consistency(times[int(len(times)/2):])
       else:
           return bad_times/good_times + 0.5*get_day_time_consistency(times[:int(len(times)/2)]) + 0.5*get_day_time_consistency(times[int(len(times)/2):])
   else:
       return 0


def get_half_good_times(times):
   day_times = [False] * 24
   for time in times[:int(len(times)/2)]:
       hour = time.hour if time.minute < 30 else time.hour+1
       day_times[hour] = True
   return sum(day_times)


def get_half_bad_times(times):
   bad_sum = 0
   good_day_times = [False] * 24
   bad_day_times = [False] * 24
   for time in times[:int(len(times)/2)]:
       hour = time.hour if time.minute < 30 else time.hour+1
       good_day_times[hour] = True
   for time in times[int(len(times)/2):]:
       hour = time.hour if time.minute < 30 else time.hour+1
       bad_day_times[hour] = True
   for i in range(0, 24):
       if good_day_times[i] != bad_day_times[i]:
           bad_sum += 1
   return bad_sum


def std_coverage(user):
   N = len(remove_na(user.isPredicted))
   sumNum = remove_na(user.numpred)
   resultSum = []
   for val in sumNum:
       if val != '0':
           resultSum.append(val)

   coverageAr.append(len(resultSum)/N)


def remove_na(inputAr):
   outputAr = []
   for value in inputAr:
       if value != 'NA':
           outputAr.append(value)
   return outputAr


def polyfit(x, y, degree):
   fresults = {}

   coeffs = numpy.polyfit(x, y, degree)
   fresults['polynomial'] = coeffs.tolist()
   p = numpy.poly1d(coeffs)

   yhat = p(x)
   ybar = numpy.sum(y)/len(y)
   ssreg = numpy.sum((yhat-ybar)**2)
   sstot = numpy.sum((y - ybar)**2)
   fresults['determination'] = ssreg / sstot

   return fresults


def std_top3precision(user):
   sumNum = remove_na(user.numpred)
   resultSum = []
   for val in sumNum:
       if val != '0':
           resultSum.append(val)
   rankVal = remove_na(user.rank)
   sumRank = 0
   for val in rankVal:
       if val == '1' or val == '2' or val == '3':
           sumRank += 1
   top3precis.append(sumRank/len(resultSum))


def user_analysis(user):
   distanceVal = distance_analysis(user)
   weekVal = week_analysis(user)
   #result = (DISTANCE_PROP*distanceVal + WEEK_PROP*weekVal)/100
   result = 1 - (DISTANCE_PROP * distanceVal + WEEK_PROP * weekVal) / 100
   results.append(result)
   if result > CUT_POINT:
       user.gbUser = 1
   else:
       user.gbUser = 0


def distance_analysis(user):
   return DISTANCE_LEN_PROP * distance_length(user) + DISTANCE_SPR_PROP * distance_spread(user)


def distance_length(user):
   meanDistance = statistics.mean(get_test_distance(user))
   if meanDistance >= MAX_DISTANCE:
       return 1
   elif meanDistance <=1:
       return 0
   else:
       return meanDistance/MAX_DISTANCE


def get_test_distance(user):
   testDistance = []
   i = 0
   while user.isPredicted[i] != 'TRUE' and i < len(user.distance):
       testDistance.append(user.distance[i])
       i+=1
   return testDistance


def distance_spread(user):
   testDist = get_test_distance(user)
   upQuort = numpy.percentile(testDist, 75)
   lwQuort = numpy.percentile(testDist, 25)
   return (upQuort-lwQuort)/(upQuort+lwQuort)


def week_analysis(user):
   return DAY_SPREAD_PROP * day_spread(user) + DAY_QUANT_PROP * day_quantity(user) + DAY_CLUST_PROP * day_cluster(user)


def get_test_start_time(user):
   start_time = []
   i = 0
   while user.isPredicted[i] != 'TRUE' and i < len(user.sTimestamp):
       start_datetime = datetime.datetime.fromtimestamp(user.sTimestamp[i]/1000)
       start_time.append(start_datetime)
       i+=1
   return start_time

def get_test_end_time(user):
   endTime = []
   i = 0
   while user.isPredicted[i] != 'TRUE' and i < len(user.sTimestamp):
       endDatetime = datetime.datetime.fromtimestamp(user.fTimestamp[i]/1000)
       endTime.append(endDatetime)
       i+=1
   return endTime


def get_test_weekday_start_time(user):
   all_start_times = get_test_start_time(user)
   return_times = []
   for time in all_start_times:
       if time.weekday() < 5:
           return_times.append(time)
   return return_times

def get_time_difference(startTime, endTime):
   h = 0
   m = endTime.minute - startTime.minute
   if m < 0:
       m = (60-startTime.minute) + endTime.minute
   if endTime.day != startTime.day:
       h = endTime.hour + (24 - startTime.hour)
   else:
       h = endTime.hour - startTime.hour
   return h + (m/60)

def day_spread(user):
   startTimeArray = get_test_start_time(user)
   endTimeArray = get_test_end_time(user)
   data = []
   time = 0
   day = 0
   for i in range(0, len(startTimeArray)):
       if i == 0:
           day = startTimeArray[i].day
           time += get_time_difference(startTimeArray[i], endTimeArray[i])
       elif day == startTimeArray[i].day:
           time += get_time_difference(startTimeArray[i], endTimeArray[i])
       else:
           data.append(time)
           time = get_time_difference(startTimeArray[i], endTimeArray[i])
           day = startTimeArray[i].day
   mean = statistics.mean(data)
   if mean < 1:
       return 1
   elif mean > MAX_NUM_HOURS:
       return 0
   return 1-(mean/MAX_NUM_HOURS)


def day_quantity(user):
   return 0


def day_cluster(user):
   return 0


def get_datetime(timestamp):
   return datetime.datetime.fromtimestamp(timestamp)


if __name__ == '__main__':
   main()
