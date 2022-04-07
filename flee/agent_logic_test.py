import sys
import random

if __name__ == "__main__":

    start_windspeed = 0
    end_windspeed = 0
    current_windspeed = 0
    days = 0
    movechance = 0.0

    days = int(sys.argv[1])
    start_windspeed = int(sys.argv[2])
    end_windspeed = int(sys.argv[3])
    

    for t in range(0, days):
        if (current_windspeed <= end_windspeed):
            start_windspeed += 5
            print(t, start_windspeed)
            if (start_windspeed >= 90):
                movechance = 1
                print(movechance)
            elif (start_windspeed >= 80):
                movechance = 0.8
                print(movechance)
            elif (start_windspeed >= 70):
                movechance = 0.7
                print(movechance)
            elif (start_windspeed >= 60):
                movechance =0.6
                print(movechance)
            elif (start_windspeed >= 50):
                movechance=0.5
                print(movechance)
            elif(start_windspeed >= 40):
                movechance=0.4
                print(movechance)
            else:
                movechance = 0.001
                print(movechance)            



    

