#!/usr/bin/env python2
## -*- coding: utf-8 -*-

import heapq
import pickle
import os
import time

class Seed:
  def __init__(self, model = {}, bound = 0):
    self.model = model
    self.bound = bound

workList = [[0, Seed({0L: chr(0x67), 1L: chr(0x6F), 2L: chr(0x6F), 3L: chr(0x64), 4L: chr(0)}, 0)]]

def search():
  global workList
  with open("/media/sf_SharedFolder/awft/worklist.pkl", "wb") as data:
    pickle.dump(workList, data)
  while len(workList) > 0:
    seed = heapq.heappop(workList)[1]
    os.system("~/triton/pin-2.14-71313-gcc.4.4.7-linux/source/tools/Triton/build/triton /media/sf_SharedFolder/awft/concolic.py /media/sf_SharedFolder/awft/example1.out " + ''.join(seed.model.values()[:-1]))
    time.sleep(1)
    with open("/media/sf_SharedFolder/awft/worklist.pkl", "rb") as data:
      workList = pickle.load(data)

def main():
  search()

if __name__ == "__main__":
  main()