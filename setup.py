import zipfile
import re
import os

SETUP_DIR = "data/"

import os.path
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

