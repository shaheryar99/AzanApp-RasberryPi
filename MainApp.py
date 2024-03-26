from datetime import date, timedelta, datetime
import json
import os
import requests
import time
from playsound import playsound
import simpleaudio as sa

# Midnight + 10 minutes to account for date change
midnight = datetime.now().replace(hour=00, minute=10).strftime("%H:%M")

dummyTime = datetime.now().replace(hour=1, minute=3).strftime("%H:%M")
dummyTime1 = datetime.now().replace(hour=1, minute=4).strftime("%H:%M")
dummyTime2 = datetime.now().replace(hour=1, minute=5).strftime("%H:%M")

reqParameters = {'latitude' : '51.049999', 'longitude' : '-114.066666', 'method' : '0'}

# Populate timings
def populateTimings():
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

dataParsed = populateTimings()

azan = sa.WaveObject.from_wave_file("Azan.wav")

while True:
    # Current Time
    timeNow = datetime.now().strftime("%H:%M")

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

    print("Populated Timings -- ", "Fajr:", fajrtime.time(), "Zuhr:", zuhrtime.time(), "Magrib:", magribtime.time())

    if (timeNow == fajrtime):
        print("Playing Azan for Fajr")
        play_azan = azan.play()
        play_azan.wait_done()

    elif (timeNow == zuhrtime):
        print("Playing Azan for Zuhr")
        play_azan = azan.play()
        play_azan.wait_done()

    elif (timeNow == magribtime):
        print("Playing Azan for Magrib")
        play_azan = azan.play()
        play_azan.wait_done()

    elif (timeNow == midnight):
        dataParsed = populateTimings()
        print("Populated Timings:", fajrtime.time(), zuhrtime.time(), magribtime.time())

    time.sleep(60)

