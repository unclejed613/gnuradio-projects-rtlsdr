##!/usr/bin/env python

from array import *
import os
import struct
stats = os.stat('freqtest.dat')
file_size = stats.st_size
#print('file size ', +file_size, ' bytes')
entries = file_size/4
#print('file has ', +entries, +' entries')
freq_array = array('f', [])                #create an array to hold the entries
for a in range(0, file_size, 4):                  #read the entries sequentially from the file
    with open('freqtest.dat', 'rb') as f:
        f.seek(a)
        bytes = f.read(4)
        freq = struct.unpack('<f', bytes)
        b = (a/4) +1
#        frq(b) = str(freq[0])
        print('Frequency: ' + str((a/4)+1) + ' ' + str(freq[0]))  #print the entries as they are read
        freq_array.append(freq[0])                                #and add them to the array
        f.close()

x = raw_input('continue? (y to modify freqs in the list, n to go to adding freqs)')
while x != "n":
#    print(x)
    fm = int(input('freq to modify: '))                 #we want to modify a particular frequency
    current_freq = freq_array[fm-1]
    print('current freq is: ', + current_freq)          #we want to replace it with a new value
    new_freq = input('new frequency:  ')
    freq_array[fm-1] = new_freq
    for indx in range(len(freq_array)):                 #print the modified list
        print(indx+1, +freq_array[indx])
    x = raw_input("do you want to change another frequency? ")

x = raw_input('continue? (y to add freqs to the list, n to save the list and exit)')    #second part... we may want to add new frequencies to the list

while x != "n":                                         #similar to the modify loop
    new_freq = input('new frequency:  ')
    freq_array.append(new_freq)                         #except we append the frequency at the end
    for indx in range(len(freq_array)):                 #and as before print the modified list
        print(indx+1, +freq_array[indx])
    x = raw_input("do you want to add another frequency? ")
print freq_array                                        #this is here as a troubleshooting tool
f = open('freqtest.dat', 'wb')                          #everything done? dump the array to the file (overwrites
f.write(freq_array)                                     #the old one)
f.close()
