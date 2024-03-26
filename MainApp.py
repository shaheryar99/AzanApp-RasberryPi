from datetime import date, timedelta, datetime
import json
import os
import requests
import time
from playsound import playsound
import multiprocessing
import simpleaudio as sa

# Midnight + 10 minutes to account for date change
midnight = datetime.now().replace(hour=00, minute=10).strftime("%H:%M")

dummyTime = datetime.now().replace(hour=1, minute=3).strftime("%H:%M")
dummyTime1 = datetime.now().replace(hour=1, minute=4).strftime("%H:%M")
dummyTime2 = datetime.now().replace(hour=1, minute=5).strftime("%H:%M")

reqParameters = {'latitude' : '51.049999', 'longitude' : '-114.066666', 'method' : '0'}

# Populate timings the first time program is launched so it is not waiting for midnight
def firstTime():
        timeNow = datetime.now().strftime("%H:%M")
        dateToday = date.today()
        year = dateToday.year
        month = dateToday.month
        day = dateToday.day

        yearstr = str(year)
        monthstr = str(month)
        daystr = str(day)

        datestring = daystr + "-" + monthstr + "-" + yearstr

        getData = requests.get('https://api.aladhan.com/v1/timings/' + datestring, params=reqParameters)
        dataParsed = getData.json()
        return dataParsed

dataParsed = firstTime()

wave_object = sa.WaveObject.from_wave_file("Azan.wav")
print("Playing")

play_object = wave_object.play()
play_object.wait_done()

while True:
    # Current Time
    timeNow = datetime.now().strftime("%H:%M")

    # In the top most while loop
    timings = dataParsed['data']['timings']

    fajr = timings['Fajr']
    zuhr = timings['Dhuhr']
    magrib = timings['Maghrib']

    fajrtime = datetime.strptime(fajr, '%H:%M')
    addFive = timedelta(minutes=9)
    fajrtime = fajrtime + addFive

    zuhrtime = datetime.strptime(zuhr, '%H:%M')

    magribtime = datetime.strptime(magrib, '%H:%M')
    minusTwo = timedelta(minutes=2)
    magribtime = magribtime - minusTwo

    #print(fajrtime.time(), zuhrtime.time(), magribtime.time())

    if (timeNow == fajrtime):
        print("Fajr Time")

    elif (timeNow == zuhrtime):
        dataParsed = firstTime()
        print("TIME REACHED.")

    elif (timeNow == magribtime):
        print("Got to second dummy time")

    time.sleep(60)

