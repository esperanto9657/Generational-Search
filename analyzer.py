#!/usr/bin/env python2
## -*- coding: utf-8 -*-

import triton
import pintool
import heapq
#import os
#import pickle
import concolic
#import threading
#import time

Triton = pintool.getTritonContext()
PC = []

class Seed:
  def __init__(self, model, bound):
    self.model = model
    self.bound = bound

def search(inputSeed):
  workList = [[0, inputSeed]]
  heapq.heapify(workList)
  runCheck(inputSeed)
  while len(workList) > 0:
    item = heapq.heappop(workList)
    childs = expandExecution(item[1])
    while len(childs) > 0:
      newItem = childs.pop()
      runCheck(newItem)
      heapq.heappush(workList, [score(newItem), newItem])
  return "0"

def expandExecution(item):
  childs = []
  ast = Triton.getAstContext()
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
  concolic.computePathConstraint()
  print(PC)
  for j in range(item.bound, len(PC)):
    if not PC[j].isMultipleBranches():
      continue
    constraint_list = ast.equal(ast.bvtrue(), ast.bvtrue())
    for i in range(j):
      if PC[i].isMultipleBranches():
        constraint_list = ast.land(constraint_list, PC[i].getTakenPredicate())
    for branch_constraint in PC[j].getBranchConstraints():
      if not branch_constraint["isTaken"]:
        newPath = ast.land(constraint_list, branch_constraint["constraint"])
        model = Triton.getModel(newPath)
        if model:
          newModel = item.model.update(zip(model.keys(),model.values()))
          newItem = Seed(newModel, j)
          childs.append(newItem)
  return childs
  
def runCheck(item):
  return

def score(item):
  score = 0
  return score

def symbolize_inputs(tid):
  rdi = pintool.getCurrentRegisterValue(Triton.registers.rdi) # argc
  rsi = pintool.getCurrentRegisterValue(Triton.registers.rsi) # argv

  # for each string in argv
  while rdi > 1:
    addr = pintool.getCurrentMemoryValue(rsi + ((rdi-1)*triton.CPUSIZE.QWORD), triton.CPUSIZE.QWORD)
    # symbolize the current argument string (including the terminating NULL)
    c = None
    s = ''
    while c != 0:
      c = pintool.getCurrentMemoryValue(addr)
      s += chr(c)
      Triton.setConcreteMemoryValue(addr, c)
      Triton.convertMemoryToSymbolicVariable(triton.MemoryAccess(addr, triton.CPUSIZE.BYTE)).setComment('argv[%d][%d]' % (rdi-1, len(s)-1))
      addr += 1
    rdi -= 1
    print 'Symbolized argument %d: %s' % (rdi, s)

def getCons():
  global PC
  PC = Triton.getPathConstraints()
  print(PC)
  #for bc in PC:
  #  print(bc.getBranchConstraints())

def computePathConstraint():
  Triton.setArchitecture(triton.ARCH.X86_64)
  Triton.enableMode(triton.MODE.ALIGNED_MEMORY, True)
  pintool.startAnalysisFromSymbol("main")
  pintool.insertCall(symbolize_inputs, pintool.INSERT_POINT.ROUTINE_ENTRY, "main")
  pintool.insertCall(getCons, pintool.INSERT_POINT.FINI)
  pintool.runProgram()
  return

def main():
  with open("log.txt", "w") as out:
    out.write(search(Seed({1, "good"}, 0)))

if __name__ == "__main__":
  main()