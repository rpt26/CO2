import time
import aranet4
from datetime import datetime
import os.path

file_name = '/home/pi/CO2_data.csv'

if not os.path.isfile(file_name):
    with open(file_name, 'wt') as f:
        f.write('seconds since epoch,sensor,CO2\n')

#You'll need your own MAC addresses in here
dev_macs = {1:"C0:D0:55:50:2A:FE",
            2:"D7:AA:F7:05:B2:8D",
            3:"F2:E6:AE:EE:B5:11",
            4:"DE:39:66:24:24:6E"}

aranets = {}
flags = {}
for i in dev_macs:
    try:
        ar4 = aranet4.Aranet4(dev_mac)
        aranets[i] = ar4
        flags[i] = True
        print(f"Connected sensor {i}")
    except:
        flags[i] = False
        print(f"couldn't connect to sensor {i}")

time_stamp = time.time()
while True:
    for i in aranets:
        try:
            ar4 = aranets[i]
            co2 = ar4.currentReadings()['co2']
            point = f"{time.time()},{i},{co2}\n"

            print(datetime.fromtimestamp(time.time()))
            print(point)
            with open(file_name,'at') as f:
                f.write(point)

        except:
            flags[i] = False
            print(f"Couldn't read sensor {i}")
            pass
        time.sleep(1)

    for i in flags:
        flag = flags[i]
        if flag == False:
            print(f"Attempting to reconnect sensor {i}")
            dev_mac = dev_macs[i]
            try:
                aranets[i] = aranet4.Aranet4(dev_mac)
                flags[i] = True
                print(f"Reconnected sensor {i}")
            except:
                flags[i] = False
                print(f"Couldn't reconnect sensor {i}, will try again after taking new readings")
