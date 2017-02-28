#file writer for float values
#import pickle
from array import array
#x=1
entries=input("How Many Entries?  ")
#x<11
print ("Enter frequencies in Hz, with no decimal points")
#fout = open("freq.dat", "a")
#while True:
for i in range(1,entries+1):
      print i
      freq=input("Frequency ")
          
      freq_array=array("f",[freq])
#fout.write(freq)
 #         frq=float(freq)
      with open("freqtest.dat", "ab") as x:
#                 pickle.dump(frq, x)p
          freq_array.tofile(x)    
#pickle.dump(freq, open ("freq.dat", "a+b"))
#x=x+1
#next
#fout.close()


