#!/usr/bin/python3

import reservationapi
import configparser


# Load the configuration file containing the URLs and keys
config = configparser.ConfigParser()
config.read("api.ini")

# Create an API object to communicate with the hotel API
hotel  = reservationapi.ReservationApi(config['hotel']['url'],
                                       config['hotel']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

# Your code goes here

band  = reservationapi.ReservationApi(config['band']['url'],
                                       config['band']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))


# one second delay after each request sent to server
#check for earliest open hotel slot n
# check if slot is also available in band, if not, return to start and check for slot after n
# if available book both
# get slots held for both - wait some time
# retry booking from start with earlier slot
#


r = hotel.get_slots_held()
print(r.json())

b = band.get_slots_held()
print(b.json())


n = 1
slotH = 1
slotB = 1

while n < 400:

    #add a second delay
    time.sleep(1)
    r = hotel.reserve_slot(slotH)
    print(r.json())

    if (r.status_code == 200):
        #book common slot
        x = band.reserve_slot(slotB)
        if(x.status_code == 200):
            continue
        elif(x.status_code != 200):
            #if common slot unavailable, release hotel booking for that slot
            r = hotel.release_slot(slotH)
            continue
    elif (r.status_code != 200):
        hotel._send_request(r,"")
        slotH +=1
        slotB +=1

    n+=1


h = hotel.get_slots_held()
print(h.json())

b = band.get_slots_held()
print(b.json())
