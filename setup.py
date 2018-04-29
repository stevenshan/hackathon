import zipfile
import re
import os
import sys
from shutil import copyfile

SETUP_DIR = "data/"

def dataFiles():
    if not os.path.isfile("setup/SensorData.zip"):
        raise ValueError("Sensor data file missing.")

    if not os.path.exists(SETUP_DIR):
        os.makedirs(SETUP_DIR)
    else:
        raise ValueError("Setup directory already exists.")

    if not os.path.exists(SETUP_DIR + "periodic"):
        os.makedirs(SETUP_DIR + "periodic")

    if not os.path.exists(SETUP_DIR + "session"):
        os.makedirs(SETUP_DIR + "session")

    print("Unzipping data file...")
    zip_ref = zipfile.ZipFile("setup/SensorData.zip", 'r')
    zip_ref.extractall(SETUP_DIR)
    zip_ref.close()

    SESSION = re.compile("^SESSION")
    PERIODIC = re.compile("^PERIODIC")

    print("Moving files...")
    dir_list = os.listdir(SETUP_DIR)
    length = len(dir_list)
    checkpoint = length // 20
    count = 0
    for file in dir_list:
        count += 1
        if count % checkpoint == 0:
            print(str(int((count * 1.0 / length) * 100)) + "%")

        filename = file
        file = SETUP_DIR + file
        if not os.path.isfile(file):
            continue

        if len(SESSION.findall(filename)) != 0:
            os.rename(file, SETUP_DIR + "session/" + filename)
        elif len(PERIODIC.findall(filename)) != 0:
            os.rename(file, SETUP_DIR + "periodic/" + filename)

def sessionData():
    print("Unzipping session data file...")
    zip_ref = zipfile.ZipFile("setup/sessionData.zip", 'r')
    zip_ref.extractall(SETUP_DIR)
    zip_ref.close()

def periodicDataJSON(): 
    print("Unzipping periodic data json file...")

    zip_ref = zipfile.ZipFile("setup/periodicData1.zip", 'r')
    zip_ref.extractall(SETUP_DIR)
    zip_ref.close()

def periodicDataPKL():
    print("Unzipping periodic data pickle file...")
    zip_ref = zipfile.ZipFile("setup/periodicData2.zip", 'r')
    zip_ref.extractall(SETUP_DIR)
    zip_ref.close()

def printUsage():
    print("Usage: python setup.py [all|data|sessionData|periodicDataJSON|periodicDataPKL]")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        printUsage()
        exit() 

    argument = sys.argv[1]
    if argument == "all":
        dataFiles()
        sessionData()
        periodicDataJSON()
        periodicDataPKL()
        copyfile("setup/Makefile", SETUP_DIR + "Makefile")
    elif argument == "data":
        dataFiles()
    elif argument == "sessionData":
        sessionData()
    elif argument == "periodicDataJSON":
        periodicDataJSON()
    elif argument == "periodicDataPKL":
        periodicDataPKL()
    else:
        printUsage()

