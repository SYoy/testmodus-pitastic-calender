import pandas
import numpy
import random
from csv_reading_writing import *
from getDate import * 
from datetime import datetime
#from Adafruit_Thermal import *
#import RPi.GPIO as GPIO

##GPIO.setwarnings(False) # Ignore warning for now
##GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
##GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
##GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # same for pin 12
##
##GPIO.setup(23, GPIO.OUT) # LED 1
##GPIO.setup(24, GPIO.OUT) # LED 2
##
##GPIO.output(24, GPIO.HIGH) # Show Status
##GPIO.output(23, GPIO.HIGH) # Light during Initialization
## Initialize the variables and lists from config.csv file
date_list,num_left_list,special = read_from_config()
last_time_used = [date_list[-1]]
current_num_left = num_left_list[-1]
last_special = special[-1]

num_left = int(current_num_left)

## Load the poems list and get variables from librarian.csv file
hot_poems_list, used_poems_list, always_usable_list = read_from_librarian()

#get current date and update num_left
day, month, year, today = getDate()
num_left += days_between(last_time_used, today)
if today == "25-12-2018":
    num_left += 10

#write update to config.csv
write_to_config([today[0],str(num_left),""])

#### Data Initialization completed ####

## Initialize the printer and buttons
#
##printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
##printer.writeBytes(0x1B, 0x21, 0x1)
##GPIO.output(23, GPIO.LOW)

## Define what happens if button gets pushed
#
##def button_callback(channel): # Get poem from normal list - count - update config,librarian
##    print("Button 1 was pushed!")
##    GPIO.output(23, GPIO.HIGH)
##    if num_left > 0:
##        print_poem()
##        printer.print("Du hast noch {} Tokens".format(num_left-1))
##        print_poem(setting="special") if today in special
##        num_left -= 1
##        write_to_config([today,str(num_left),""]
##    else:
##        printer.print("Leider hast du keine Tokens mehr,")
##        printer.print("versuche es mit dem anderen Knopf oder")
##        printer.print("warte bis morgen.")
##    GPIO.output(23, GPIO.LOW)
##                        
##def button_callback2(channel): # Get poem from always usable list - Shakespeare?
##    GPIO.output(23, GPIO.HIGH)
##    print("Button 2 was pushed!")
##    print_poem(setting="always")
##    print_poem(setting="special") if today in special
##    GPIO.output(23, GPIO.LOW)

                        
def button1(): # Get poem from normal list - count - update config,librarian
    global num_left
    print("Button 1 was pushed!")
##    GPIO.output(23, GPIO.HIGH)
    if num_left > 0:
        print_poem(setting="poems")
        print("Du hast noch {} Tokens".format(num_left-1))
        if today in special:
            print_poem(setting="special")
        num_left -= 1
        write_to_config([today,str(num_left),""])
    else:
        print("Leider hast du keine Tokens mehr,")
        print("versuche es mit dem anderen Knopf oder")
        print("warte bis morgen.")
##    GPIO.output(23, GPIO.LOW)
                        
def button2(): # Get poem from always usable list - Shakespeare?
##    GPIO.output(23, GPIO.HIGH)
    global today
    global special
    print("Button 2 was pushed!")
    print_poem(setting="always")
    if today in special:
        print_poem(setting="special")
##    GPIO.output(23, GPIO.LOW)
    
## Printing Function
def print_poem( setting="poems" ):
    global hot_poems_list
    global always_usable_list
    global used_poems_list
    lines = []

    # define what to print with regard to setting
    if setting=="poems":
        chosen_index = random.randrange(len(hot_poems_list))
        chosen_poem = int(hot_poems_list[chosen_index])
        folder="poems"
    elif setting=="always":
        chosen_index = random.randrange(len(always_usable_list))
        chosen_poem = always_usable_list[chosen_index]
        folder="always_usable"
    elif setting=="special":
        chosen_poem = today
        folder="special"
        
    with open ("{}\{}.txt".format(folder, str(chosen_poem))) as f:
        lines = f.readlines()
    # Some sonnets have a trailing blank line.
    # Get rid of newlines, etc, println() adds them anyway
    lines = [k.strip() for k in lines]
    if lines[0] == "":
       lines = lines[1:len(lines)]
    if lines[-1] == "":
        lines = lines[0:-1]
    print(lines)
    # Add an empty line between the sonnet and the couplet
    rest = lines[14:16] if setting=="always_usable" else ""
    print("REST\n")
    print(rest)
    print("REST\n")
    lines = lines[0:14] + [""] + rest if setting=="always_usable" else lines
    print(lines)
    # exit()
    # and indent the couplet
    lines[-1] = "\t" + lines[-1]
    lines[-2] = "\t" + lines[-2]

##    for k in lines:
##        # empty line: print a newline
##        if not len(k): 
##            printer.println()
##            continue
##        # Set length according to whether or not first char is a tab
##        maxlength = 42
##        if k[0] == "\t":
##            maxlength = 40
##
##        # split long lines into two, and get the right number of tabs
##        if len(k) > maxlength:
##            if k[0] == "\t":
##                str1 = "\t"
##                str2 = "\t\t"
##            else:
##                str1 = ""
##                str2 = "\t"
##
##            k = k.strip().split()
##
##            for j in k:
##                if len(str1) < 30:
##                    str1 += (j) + " "
##                else:
##                    str2 += (j) + " "
##            printer.println(str1)
##            printer.println(str2)
##        else:
##            printer.println(k)

##    printer.feed(6)
    # update to lists:
    if setting=="poems":
        used_poems_list.append(chosen_poem)
        del hot_poems_list[chosen_index]
        write_to_librarian(hot_poems_list,used_poems_list)

## connect event to button push
##GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback)
##GPIO.add_event_detect(12,GPIO.RISING,callback=button_callback2)
   
                       
## running and waiting for input to Quit Run
##message = input("Press enter to quit\n\n")

## EoFile -- clean up everything
##GPIO.cleanup()
##printer.sleep()      # Tell printer to sleep
##printer.wake()       # Call wake() before printing again, even if reset
##printer.setDefault() # Restore printer to defaults
##GPIO.output(23, GPIO.LOW)



