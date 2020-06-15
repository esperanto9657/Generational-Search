#!/usr/bin/env python2
## -*- coding: utf-8 -*-

import triton
import pintool
import heapq
import os
import pickle
import copy
#import concolic
#import threading
#import time

Triton = pintool.getTritonContext()

class Seed:
  def __init__(self, model = {}, bound = 0):
    self.model = model
    self.bound = bound

seed = None
workList = []

def search():
  while len(workList) > 0:
    global seed
    seed = heapq.heappop(workList)[1]
    expandExecution(seed)

def runCheck(seed):
  return

def score(seed):
  score = 0
  return score

def symbolize_inputs(tid):
  rdi = pintool.getCurrentRegisterValue(Triton.registers.rdi) # argc
  rsi = pintool.getCurrentRegisterValue(Triton.registers.rsi) # argv
  global seed
  seed = Seed()

  # for each string in argv
  while rdi > 1:
    addr = pintool.getCurrentMemoryValue(rsi + ((rdi-1)*triton.CPUSIZE.QWORD), triton.CPUSIZE.QWORD)
    # symbolize the current argument string (including the terminating NULL)
    c = None
    s = ''
    i = 0
    while c != 0:
      c = pintool.getCurrentMemoryValue(addr)
      print(c)
      s += chr(c)
      seed.model[long(i)] = chr(c)
      i += 1
      Triton.setConcreteMemoryValue(addr, c)
      Triton.convertMemoryToSymbolicVariable(triton.MemoryAccess(addr, triton.CPUSIZE.BYTE)).setComment('argv[%d][%d]' % (rdi-1, len(s)-1))
      addr += 1
    rdi -= 1
    print 'Symbolized argument %d: %s' % (rdi, s)
'''
def set_inputs(tid):
  rdi = pintool.getCurrentRegisterValue(Triton.registers.rdi) # argc
  rsi = pintool.getCurrentRegisterValue(Triton.registers.rsi) # argv
  print(rdi)
  print(rsi)
  global seed
  
  while rdi > 1:
    addr = pintool.getCurrentMemoryValue(rsi + ((rdi-1)*triton.CPUSIZE.QWORD), triton.CPUSIZE.QWORD)
    for v in seed.model.values():
      Triton.setConcreteMemoryValue(addr, ord(v))
      Triton.convertMemoryToSymbolicVariable(triton.MemoryAccess(addr, triton.CPUSIZE.BYTE))
      addr += 1
    rdi -= 1
    print 'Symbolized argument %d: %s' % (rdi, s)
'''
def computePathConstraint():
  childs = []
  ast = Triton.getAstContext()
  PC = Triton.getPathConstraints()
  print(PC)
  for j in range(seed.bound, len(PC)):
    if not PC[j].isMultipleBranches():
      continue
    constraint_list = ast.equal(ast.bvtrue(), ast.bvtrue())
    for i in range(j):
      if PC[i].isMultipleBranches():
        for branch_constraint in PC[i].getBranchConstraints():
          if branch_constraint["isTaken"]:
            constraint_list = ast.land([constraint_list, branch_constraint["constraint"]])
    for branch_constraint in PC[j].getBranchConstraints():
      if not branch_constraint["isTaken"]:
        newPath = ast.land([constraint_list, branch_constraint["constraint"]])
        model = Triton.getModel(newPath)
        print(seed.model)
        if model:
          for i in model.keys():
            if model[i].getValue() < 0x80:
              model[i] = chr(model[i].getValue())
            else:
              del model[i]
          newModel = copy.deepcopy(seed.model)
          newModel.update(model)
          print(newModel)
          newSeed = Seed(newModel, j + 1)
          childs.append(newSeed)
  while len(childs) > 0:
    newSeed = childs.pop()
    runCheck(newSeed)
    heapq.heappush(workList, [-score(newSeed), newSeed])
  with open("/media/sf_SharedFolder/awft/worklist.pkl", "wb") as data:
    pickle.dump(workList, data)

def expandExecution(seed = None):
  #thread = threading.Thread(target = computePathConstraint)
  #thread.start()
  #thread.join()
  #concolic.computePathConstraint()
  #with open("PC.pkl", "rb") as pc:
  #  PC = pickle.load(pc)
  #pid = os.fork()
  #if not pid:
  #  computePathConstraint()
  #else:
  #  os.waitpid(pid, 0)
  #concolic.computePathConstraint()
  Triton.setArchitecture(triton.ARCH.X86_64)
  Triton.enableMode(triton.MODE.ALIGNED_MEMORY, True)
  pintool.startAnalysisFromSymbol("main")
  if seed is None:
    pintool.insertCall(symbolize_inputs, pintool.INSERT_POINT.ROUTINE_ENTRY, "main")
  else:
    #pintool.insertCall(set_inputs, pintool.INSERT_POINT.ROUTINE_ENTRY, "main")
    print(seed)
  pintool.insertCall(computePathConstraint, pintool.INSERT_POINT.FINI)
  pintool.runProgram()
  return

def main():
  if not os.path.exists("/media/sf_SharedFolder/awft/worklist.pkl"):
    expandExecution()
  else:
    with open("/media/sf_SharedFolder/awft/worklist.pkl", "rb") as data:
      global workList
      workList = pickle.load(data)
    for i in workList:
      print(i[1].model)
    search()

if __name__ == "__main__":
  main()