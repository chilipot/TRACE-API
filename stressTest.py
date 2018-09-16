#!/usr/bin/python

import threading
import time
import webbrowser
import os
import requests

exitFlag = 0
a = 100
f = 0
g = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      global f, g
      print("Starting " + self.name)
      r = requests.get("https://trace-api.herokuapp.com/report?pageNumber="+ str(self.threadID) + "&pageSize=250", timeout=120)
      try:
          r.json()
          g += 1
          print("ok: " + str(g) + " failed: " + str(f))
      except:
          f += 1
          print("ok: " + str(g) + " failed: " + str(f))
      # f = open('helloworld.html','w')
      #
      # f.write(r.text)
      # f.close()
      #
      #   #Change path to reflect file location
      # filename = 'file:///'+os.getcwd()+'/' + 'helloworld.html'
      # webbrowser.open_new_tab(filename)
      # print("Exiting " + self.name)


for i in range(a):
    thread = myThread(i, "Thread-" + str(i))
    thread.start()
# # Create new threads
# thread1 = myThread(1, "Thread-1")
# thread2 = myThread(2, "Thread-2")
# thread3 = myThread(3, "Thread-3")
# thread4 = myThread(4, "Thread-4")
# thread5 = myThread(5, "Thread-5")
# thread6 = myThread(6, "Thread-6")
#
# # Start new Threads
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()
# thread6.start()

print("Exiting Main Thread")
