#!/usr/bin/env python3
import os
import subprocess
from time import sleep

capacity = '/sys/class/power_supply/BAT1/capacity'
charger = '/sys/class/power_supply/ACAD/online'

fhca = open(capacity, 'r')
fhch = open(charger, 'r')

def sendNotify(icon, title, text):
    environ = dict()
    xpub = subprocess.check_output('/usr/bin/xpub').decode()
    for env in xpub.split('\n'):
        z = env.split('=')
        environ.update({z[0]: z[1]})
    text = text.replace('\'', '\\\'')
    subprocess.check_output(f'{xpub.replace(nl, " ")} su {environ["XUSER"]} -c $\'/usr/bin/notify-send -u critical -i {icon} -a "Battery status" "{title}" "{text}"\'', shell=True)
    print('sent', text)
    return True

dead = False
critical = False
caution = False

try:
    while True:
        sleep(1)
        fhca.seek(0) # Seek to position 0
        fhch.seek(0) # !!
        status = int(fhca.read().strip()) # Read percentage of battery and convert to integer
        connected = bool(int(fhch.read().strip())) # Read battery connection status and convert to boolean
        nl = '\n'
        if not connected: # If charger isn't connected:
            print('we aren\'t connected')
            if status <= 3: # If battery is at or below 3%,
                dead = False
                critical = False
                caution = False
                try:
                    subprocess.check_output(['/usr/bin/systemctl', 'hibernate']) # Hibernate the system immediately.
                except:
                    pass
            elif status <= 5: # If battery is at or below 5%, 
                if not dead: # and the dead notification hasn't already fired off:
                    if status >= 4: # and battery is above 4%, 
                        sendNotify('battery-missing', f'Battery is at {status}%', 'This laptop will hibernate shortly. Charge your laptop now.') # Send notification to user
                        dead = True
                        critical = False
                        caution = False
            elif status <= 9:
                if not critical:
                    if status >= 6:
                        print('send')
                        sendNotify('battery-empty', f'Battery is at {status}%', 'This laptop\'s battery is very low. Please charge your laptop soon.')
                        dead = False
                        critical = True
                        caution = False
            elif status <= 15:
                if not caution:
                    if status >= 10:
                        sendNotify('battery-caution', f'Battery is at {status}%', 'This laptop\'s battery is low. Consider plugging your laptop to a charger.')
                        dead = False
                        critical = False
                        caution = True
finally:
    fhca.close()
    fhch.close()