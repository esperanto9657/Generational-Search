#!/usr/bin/env python2
## -*- coding: utf-8 -*-

import heapq
import pickle
import subprocess

class Seed:
  def __init__(self, model = None, bound = 0):
    self.model = model if model else {}
    self.bound = bound

SAMPLE_PATH = "/media/sf_SharedFolder/awft/example1.out "
workList = [[0, Seed({0: 'g', 1: 'o', 2: 'o', 3: 'd', 4: chr(0)}, 0)]]

def search():
  global workList
  with open("/media/sf_SharedFolder/awft/worklist.pkl", "wb") as data:
    pickle.dump(workList, data)
  while len(workList) > 0:
    seed = heapq.heappop(workList)[1]
    subprocess.check_call("~/triton/pin-2.14-71313-gcc.4.4.7-linux/source/tools/Triton/build/triton /media/sf_SharedFolder/awft/concolic.py " + SAMPLE_PATH + ''.join(seed.model.values()[:-1]), shell = True)
    with open("/media/sf_SharedFolder/awft/childlist.pkl", "rb") as data:
      childs = pickle.load(data)
    while len(childs) > 0:
      newSeed = childs.pop()
      heapq.heappush(workList, [-score(newSeed), newSeed])
    for i in workList:
      print(i[0], i[1].model)
    with open("/media/sf_SharedFolder/awft/worklist.pkl", "wb") as data:
      pickle.dump(workList, data)

def score(newSeed):
  score = int(subprocess.check_output("~/triton/pin-2.14-71313-gcc.4.4.7-linux/source/tools/Triton/build/triton /media/sf_SharedFolder/awft/score.py " + SAMPLE_PATH + ''.join(newSeed.model.values()[:-1]), shell = True).strip())
  return score

def main():
  search()

if __name__ == "__main__":
  main()