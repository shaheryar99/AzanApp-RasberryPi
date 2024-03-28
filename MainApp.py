from datetime import date, timedelta, datetime
import json
import os
import requests
import time
#import simpleaudio as sa
import pygame

# Midnight + 10 minutes to account for date change
midnight = datetime.now().replace(hour=00, minute=10).strftime("%H:%M")

dummyTime = datetime.now().replace(hour=3, minute=51).strftime("%H:%M")
dummyTime1 = datetime.now().replace(hour=3, minute=57).strftime("%H:%M")
dummyTime2 = datetime.now().replace(hour=1, minute=5).strftime("%H:%M")

reqParameters = {'latitude' : '51.049999', 'longitude' : '-114.066666', 'method' : '0'}

#CHECK DIFFERENCE BETWEEN STRFTIME LINES 12,13 and 14, AND STRPTIME 56, 60, 62.

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

#azan = sa.WaveObject.from_wave_file("Azan.wav")

pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound("Azan.wav")

while True:
    # Current Time
    timeNow = datetime.now().strftime("%H:%M")

    timings = dataParsed['data']['timings']

    fajr = timings['Fajr']
    zuhr = timings['Dhuhr']
    magrib = timings['Maghrib']

    fajrtime = datetime.strptime(fajr, '%H:%M')
    addFive = timedelta(minutes=6)
    fajrtime = fajrtime + addFive

    zuhrtime = datetime.strptime(zuhr, '%H:%M')

    magribtime = datetime.strptime(magrib, '%H:%M')
    minusTwo = timedelta(minutes=1)
    magribtime = magribtime - minusTwo

    fajrTimeString = fajrtime.strftime("%H:%M")
    zuhrTimeString = zuhrtime.strftime("%H:%M")
    magribTimeString = magribtime.strftime("%H:%M")

    print(timeNow)
    print("Populated Timings:", fajrTimeString, zuhrTimeString, magribTimeString)

    if (timeNow == fajrTimeString):
        print("Playing Azan for Fajr")
        #play_azan = azan.play()
        #play_azan.wait_done()
        sound.play()

    elif (timeNow == zuhrTimeString):
        print("Playing Azan for Zuhr")
        #play_azan = azan.play()
        #play_azan.wait_done()
        sound.play()

    elif (timeNow == magribTimeString):
        print("Playing Azan for Magrib")
        #play_azan = azan.play()
        #play_azan.wait_done()
        sound.play()

    elif (timeNow == midnight):
        dataParsed = populateTimings()
        print("Populated Timings:", fajrTimeString, zuhrTimeString, magribTimeString)

    #elif (timeNow == dummyTime):
        #play_azan = azan.play()
        #play_azan.wait_done()
         #sound.play()

    #elif (timeNow == dummyTime1):
        #play_azan = azan.play()
        #play_azan.wait_done()
        #sound.play()

    time.sleep(60)

