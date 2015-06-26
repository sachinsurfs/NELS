import os
import subprocess
import re

def getNumInstances( fileName ):
   num = 0
   s = "java -cp /usr/share/java/weka.jar weka.core.Instances "+fileName ##run this on command line
   out = subprocess.check_output(s,shell=True) 
   #get number of instances from the output
   out_str = out.decode('utf-8')
   m = re.search(r'(Num Instances:)?(\d+).*',out_str)
   if( m ):
       print(m.group(0))
       num = int(m.group(2))
   else:
       print("ELSE : Couldn't get number of instances")
       print(out_str)
   return num


def mergeFiles():

   '''
   the function merges all the final.arff files into a single finale.arff file
   '''


def populateNomFile(inst, catornot, DEST_DIR):
   '''
   populates the nominal.arff file
   '''
   os.system("touch "+DEST_DIR+"/nominal.arff")
   print(inst, catornot)
   f = open(DEST_DIR+"/nominal.arff", 'w')
   f.write('@relation (null)\n@attribute catornot {yes, no}\n@data\n\n')
   for i in range(0, inst):
      f.write(catornot+'\n')


def fillSoundDirectory(directory, catornot, DEST_DIR):
   i=1
   j=1 ## variable to hold the destination directory
   for dir_path, dirname, filename in os.walk(directory):
      for file_name in filename:
   
         abs_path = dir_path+"/"+file_name; # obtains the full path of the file
         string = OPENSMILE+"/SMILExtract -C "+OPENSMILE+"/MFCC12_E_D_A.conf -I "+abs_path+" -O "+DEST_DIR+"/arff"+str(i)+".arff"
         print(string)
         os.system(string)
         inst = getNumInstances(DEST_DIR+"/arff"+str(i)+".arff")
         populateNomFile(inst, catornot, DEST_DIR)
         merge_str = "java -cp /usr/share/java/weka.jar weka.core.Instances merge "+DEST_DIR+"/arff"+str(i)+".arff "+DEST_DIR+"/nominal.arff > "+DEST_DIR+"/merge_file.arff"
         print(merge_str)
         os.system(merge_str)
         os.system("cat "+DEST_DIR+"/merge_file.arff > "+DEST_DIR+"/arff"+str(i)+".arff")
         if(os.stat(DEST_DIR+"/arff"+str(i)+".arff").st_size==0):
            continue
         if(i==1):
            print(i)
            pass
         elif(i==2):
            ##merge the arff1.arff and arff2.arff
            merge_string = "java -cp /usr/share/java/weka.jar weka.core.Instances append "+DEST_DIR+"/arff1.arff "+DEST_DIR+"/arff2.arff > "+DEST_DIR+"/final.arff"
            os.system(merge_string)
         else:
             merge_string = "java -cp /usr/share/java/weka.jar weka.core.Instances append "+DEST_DIR+"/arff"+str(i)+".arff "+DEST_DIR+"/final.arff > "+DEST_DIR+"/final_temp.arff"
             os.system(merge_string)
             os.system("cat "+DEST_DIR+"/final_temp.arff > "+DEST_DIR+"/final.arff")
         i = i+1
   


OPENSMILE = '/home/syed/CCBD/sound_intenship/openSMILE-2.1.0/openSMILE-2.1.0/bin/linux_x64_standalone_static';
READ_DIR = input('Enter the directory to read : ')
## DEST_DIR = input('Enter the directory to save datasets : ')
CAT_DIR = input('Enter the directory with the cat sound: ')

## generate the yes for the cat directory and generate the no for other directories ofsound

for dir_path, dirnames, filename in os.walk(READ_DIR):
   if(dir_path == CAT_DIR and dir_path != READ_DIR and os.listdir(dir_path)!=[]):
      string = "mkdir "+dir_path+"_output"
      os.system(string)
      fillSoundDirectory(dir_path, 'yes', dir_path+"_output")
   elif(dir_path != CAT_DIR and dir_path != READ_DIR and os.listdir(dir_path)!=[]):
      string = "mkdir "+dir_path+"_output"
      os.system(string)
      fillSoundDirectory(dir_path, 'no', dir_path+"_output")
   else:
      print("Could not read directory")
      pass
      
numFiles = 1
os.system("touch "+READ_DIR+"/finale.arff")
os.system("touch "+READ_DIR+"/temp_finale.arff")
for dir_path, dirnames, filename in os.walk(READ_DIR):
   if ('final.arff' in filename):
      ##if(os.stat(dir_path+"/final.arff").st_size==0):
        ## continue
      if(numFiles == 1):
         string = "cat "+dir_path+"/final.arff > "+READ_DIR+"/finale.arff"
         os.system(string)
      else:
         string = "java -cp /usr/share/java/weka.jar weka.core.Instances append "+dir_path+"/final.arff "+READ_DIR+"/finale.arff > "+READ_DIR+"/temp_finale.arff"
         os.system(string)
         os.system("cat "+READ_DIR+"/temp_finale.arff > "+READ_DIR+"/finale.arff")
      numFiles = numFiles + 1   
