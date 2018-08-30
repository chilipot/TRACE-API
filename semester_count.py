import os
import time
import sys


dir = r"C:\Users\dangu\OneDrive\Computer Files\Documents\GitHub\TRACE-API\downloads"
onlyfiles = next(os.walk(dir))[2] #dir is your directory path as string

semesters = {
    "201840_Summer_1_2018": 0,
    "Law_Quarter_-_Spring_2018": 0,
    "Law_Semester_-_Spring_2018": 0,
    "201830_Spring_2018": 0,
    "Spring_A_-_First_Half_2018": 0,
    "Law_Quarter_-_Winter_2018": 0,
    "MLS_Fall_2017": 0,
    "201810_Fall_2017": 0,
    "Law_Semester_-_Fall_2017": 0,
    "Law_Quarter_-_Fall_2017": 0,
    "Fall_A_2017": 0,
    "MLS_Semester_B_-_Summer_2017": 0,
    "201760_Summer_2_2017": 0,
    "201750_Full_Summer_2017": 0,
    "Law_Quarter_-_Summer_2017": 0,
    "MLS_Semester_A_-_Summer_2017": 0,
    "201740_Summer_1_2017": 0,
    "Law_Special_-_Summer_2017": 0,
    "Law_Quarter_-_Spring_2017": 0,
    "Law_Semester_-_Spring_2017": 0,
    "201730_Spring_2017": 0,
    "MLS_Semester_A_-_Spring_2017": 0,
    "Spring_A_201730": 0,
    "Law_Quarter_-_Winter_2017": 0,
    "MLS_Semester_B_-_Fall_2016": 0,
    "201710_Fall_2016": 0,
    "Law_Semester_-_Fall_2016": 0,
    "Law_Quarter_-_Fall_2016": 0,
    "MLS_Semester_A_-_Fall_2016": 0,
    "Fall_A_201710": 0,
    "201660_Summer_2_2016": 0,
    "Summer_2016_Law_Semester": 0,
    "201650_Full_Summer_2016": 0,
    "Law_Quarter_-_Summer_2016": 0,
    "201640_Summer_1_2016": 0,
    "Law_Quarter_-_Spring_2016": 0,
    "Law_Semester_-_Spring_2016": 0,
    "201630_Spring_2016": 0,
    "201630_Spring_A_2016": 0,
    "Law_Quarter_-_Winter_2016": 0,
    "201610_Fall_2015": 0,
    "Law_Semester_-_Fall_2015": 0,
    "Law_Quarter_-_Fall_2015": 0,
    "201610_Fall_A_2015": 0,
    "201560_Summer_2_2015": 0,
    "201550_Full_Summer_2015": 0,
    "Summer_2015_Law_Quarter": 0,
    "Law_Quarter_-_Summer_2015": 0
}

count = 0
files = 0

for file in onlyfiles:
    found = False
    for key in semesters:
        if str(key) in str(file):
            count += 1
            semesters[key] += 1
            found = True
    if not found:
        print(file)
    files += 1

print(count)
print(files)
for key in semesters:
    print(key, semesters[key])
