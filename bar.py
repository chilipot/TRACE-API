import os
import time
import sys


dir = r"C:\Users\dangu\OneDrive\Computer Files\Documents\GitHub\TRACE-API\downloads"
onlyfiles = next(os.walk(dir))[2] #dir is your directory path as string



while len(onlyfiles) <=26270:
    onlyfiles = next(os.walk(dir))[2]
    p = len(onlyfiles)/26270.0
    sys.stdout.write("\r%f%%" %  p)
    sys.stdout.flush()
