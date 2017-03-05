#!/usr/bin/env python

from array import *
import os
import struct
import sys
stats = os.stat('freqtest.dat')
file_size = stats.st_size
print('file size ', +file_size, ' bytes')
entries = file_size/4
print("file has " + str(entries) +" entries")
#freq_array = array('f', []) 
def FreqArrayInit():
    global freq_array
    freq_array = array('f', [])                #create an array to hold the entries

def GetFreqs():
#    freq_array = array('f', [])
    stats = os.stat('freqtest.dat')
    file_size = stats.st_size
    for a in range(0, file_size, 4):
#        print(a)        #read the entries sequentially from the file
        with open('freqtest.dat', 'rb') as f:
            f.seek(a)
            bytes = f.read(4)
            freq = struct.unpack('<f', bytes)
#            b = (a/4) +1
#           frq(b) = str(freq[0])
            print('Frequency: ' + str((a/4)+1) + ' ' + str(freq[0]))  #print the entries as they are read
            freq_array.append(freq[0])                                #and add them to the array
            f.close()
    Chooser()
            
def DumpFreqs():
    print('writing...  ')
    print(freq_array)    
    f = open('freqtest.dat', '+wb')                          #everything done? dump the array to the file (overwrites
    f.write(freq_array)                                    #the old one)
#    freq_array.tofile(f)
    f.close()
    Chooser()
    

def ModifyFreqs():
    fm = int(input('freq to modify: '))                 #we want to modify a particular frequency
    current_freq = freq_array[fm-1]
    print('current freq is: ', + current_freq)          #we want to replace it with a new value
    new_freq = float(input('new frequency:  '))
    freq_array[fm-1] = new_freq
    for indx in range(len(freq_array)):                 #print the modified list
        print(indx+1, +freq_array[indx])
#    x = raw_input("do you want to change another frequency? ")
    Chooser()
    

def AppendFreqs():
    new_freq = float(input('new frequency:  '))
    freq_array.append(new_freq)                         #except we append the frequency at the end
    for indx in range(len(freq_array)):                 #and as before print the modified list
        print(indx+1, +freq_array[indx])
    Chooser()
    
def RemoveFreq():
    fm = int(input('freq to remove: '))                 #we want to modify a particular frequency
    current_freq = freq_array[fm-1]
    print('current freq is: ', + current_freq)
    print('removing freq')
    freq_array.pop(fm-1)
    Chooser()
    

    
        

def Chooser():
    x = input('(C)hange  (A)ppend  (R)emove (W)rite  (P)rint (L)oad (Q)uit')
    if x == 'c':
        ModifyFreqs()
    elif x == 'a':
        AppendFreqs()
    elif x == 'w':
        DumpFreqs()
    elif x == 'q':
        GoodBye()
    elif x == 'r':
        RemoveFreq()
    elif x == "l":
#        freq_array = array('f', [])
        FreqArrayInit()
        GetFreqs()        
    elif x == 'p':
        PrintFreqs()
    else:
        Chooser()

def PrintFreqs():
    print(freq_array)
    Chooser()
        
def GoodBye():
    print('exiting......')
    sys.exit()
    
FreqArrayInit()
GetFreqs()

Chooser()
