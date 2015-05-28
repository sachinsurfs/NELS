'''To generate ARFF files and append them to a single arff file given a directory containing sounds'''

import os
import re
import subprocess

def getNumInstances( fileName ):
    num = 0
    s = "java -cp /usr/share/java/weka/weka.jar weka.core.Instances "+fileName
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

def populateNomFile( inst, catornot ):
    os.system("touch "+DATASET_DIR+"/nominal.arff")
    f = open(DATASET_DIR+"/nominal.arff","w")
    print(inst, catornot)
    f.write('@relation (null)\n@attribute catornot {yes,no}\n@data\n')
    for i in range(0,inst):
        f.write(catornot+"\n")
OPENSMILE_DIR = input("Enter opensmile directory : ")
read_dir = input("Enter directory to be read : ")
DATASET_DIR = input("Enter directory to save datasets : ")
catornot = input("Is it a cat sound or not? : ")
i = 1
j = 1
append_string = ""
append_file = ""
for dirname, dirnames, filenames in os.walk(read_dir):
    for filename in filenames:
        abspath = dirname+"/"+filename
        string = OPENSMILE_DIR+"/SMILExtract -C "+OPENSMILE_DIR+"/MFCC12_E_D_A.conf -I "+abspath+" -O "+DATASET_DIR+"/arff"+str(i)+".arff"
        print(string)
        os.system(string)
        inst = getNumInstances( DATASET_DIR+"/arff"+str(i)+".arff" ) 
        populateNomFile( inst, catornot )
        merge_str = "java -cp /usr/share/java/weka/weka.jar weka.core.Instances merge "+DATASET_DIR+"/arff"+str(i)+".arff "+DATASET_DIR+"/nominal.arff > "+DATASET_DIR+"/merge_file.arff"
        os.system(merge_str)
        os.system("cat "+DATASET_DIR+"/merge_file.arff > "+DATASET_DIR+"/arff"+str(i)+".arff")
        if( i == 1 ):
            print(i)
            pass
        elif( i == 2 ):
            os.system("java -cp /usr/share/java/weka/weka.jar weka.core.Instances append "+DATASET_DIR+"/arff1.arff "+DATASET_DIR+"/arff2.arff > "+DATASET_DIR+"/final.arff")
            print(i)
        else:
            os.system("java -cp /usr/share/java/weka/weka.jar weka.core.Instances append "+DATASET_DIR+"/arff"+str(i)+".arff "+DATASET_DIR+"/final.arff > "+DATASET_DIR+"/final_temp.arff")
            os.system("cat "+DATASET_DIR+"/final_temp.arff > "+DATASET_DIR+"/final.arff")
            print(i)
        i += 1
        j += 1
