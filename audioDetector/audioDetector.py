#!/usr/bin/env python3

'''
Python script for detecting and timestamping occurence of cat sounds 
'''

import pyaudio
import wave
import re
import subprocess as sp
import sys

OPENSMILE_DIR = "."
inst = 1
timestamps = []

class testArff():
    
    def __init__(self, fi,wf,chunk):
        self.fi = int(fi)
        self.wf = wf
        self.chunk = chunk
        string = "java -cp /usr/share/java/weka.jar weka.classifiers.trees.J48 -T fin.arff -l samplej48.model -p 0 > bar.txt"
        sp.call(string,shell=True)
        with open('bar.txt') as f:
            self.s = f.readlines()[5:]

    def __iter__(self):
        self.m = 0
        self.count = 0
        self.acount = 0
        self.temp = 0
        self.flag = False
        return self

    def __next__(self):
        if(self.fi+self.m <= len(self.s)):
            global timestamps
            y = 0 
            n = 0
            for line in self.s[self.m:(self.fi+self.m)]:
                if line.strip():
                    if('1' in line[23:29].strip()):
                        y = y+1
                    else:
                        n = n+1
            self.m = self.m + self.fi
#Arbitrary Percent. Also cat/notcat have been interchanged.
            if(n/(y+n) > 0.75):
                if(self.flag == False):
                    self.flag = True
                    self.count += 1
                    self.temp = ((self.wf.tell() - self.chunk )/self.chunk) * 0.25
                else:
                    self.count +=1
                    self.acount = 0
                    if(self.count == 2):
                        timestamps.append(self.temp)
                return "  cat  "
            else:
                if(self.flag and self.acount == 0):
                    self.acount = 1
                elif(self.acount == 1):
                    self.count = 0
                    self.acount = 0
                    self.flag = False        
                return "not cat"
        else:
            raise StopIteration


def getNumInstances( fileName ):
    num = 0
    s = "java -cp /usr/share/java/weka.jar weka.core.Instances "+fileName
    out = sp.check_output(s,shell=True) 
    #get number of instances from the output
    out_str = out.decode('utf-8')
    m = re.search(r'(Num Instances:)?(\d+).*',out_str)
    if( m ):
        num = int(m.group(2))
    else:
        print("ELSE : Couldn't get number of instances")
        print(out_str)
    return num

def populateNomFile( inst, s ):
    sp.call("touch nominal.arff", shell=True)
    f = open("nominal.arff","w")
    f.write('@relation (null)\n@attribute catornot {yes,no}\n@data\n')
    for i in range(0,inst):
        f.write(s+"\n")

def genArff(filename):
    global inst
    string = OPENSMILE_DIR+"/SMILExtract -l 0 -C "+OPENSMILE_DIR+"/MFCC12_E_D_A.conf -I "+filename+" -O fileTemp.arff"
    sp.call(string, shell=True)
    inst = getNumInstances("./fileTemp.arff") 
    populateNomFile( inst, "?" )
    merge_str = "java -cp /usr/share/java/weka.jar weka.core.Instances merge fileTemp.arff nominal.arff > fin.arff"
    sp.call(merge_str, shell=True)


if __name__== "__main__":
        file1 = input("Enter audio file: ")
        OPENSMILE_DIR = input("Enter opensmile dir: ")
        wf = wave.open(file1,'rb')
        swidth = wf.getsampwidth() 
        chunk = wf.getframerate()//4
        nframes = wf.getnframes()
        genArff(file1)
        
        fi = (chunk * (inst/nframes)) // 1
        
        i = iter(testArff(fi,wf,chunk))
        data = wf.readframes(chunk)
        p = pyaudio.PyAudio()

        stream = p.open(format =
                            p.get_format_from_width(swidth),
                            channels = wf.getnchannels(),
                            rate = wf.getframerate(),
                            output = True)
        sp.call("clear")
        while(len(data) == chunk * swidth):
            stream.write(data)
            sys.stdout.write("\r"+next(i))
            sys.stdout.flush()
            data = wf.readframes(chunk)
        wf.close() 
        sp.call("clear")
        print("TIMESTAMPS OF CATS")
        for i in timestamps:
            print(i)
