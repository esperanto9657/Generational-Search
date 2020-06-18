import triton
import pintool
import heapq
import pickle
import copy
import os
import time
#import threading

Triton = pintool.getTritonContext()
workList = []
seed = None
blockList = set()

class Seed:
  def __init__(self, model = {}, bound = 0):
    self.model = model
    self.bound = bound

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

def expandExecution():
  childs = []
  ast = Triton.getAstContext()
  PC = Triton.getPathConstraints()
  if(seed.bound < len(PC)):
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
  with open("/media/sf_SharedFolder/awft/blocklist.pkl", "wb") as data:
    pickle.dump(blockList, data)

def computeBlockCoverage(inst):
  global blockList
  if inst.isControlFlow():
    blockList.add(inst.getAddress())

def runCheck(seed):
  return

def score(seed):
  os.system("~/triton/pin-2.14-71313-gcc.4.4.7-linux/source/tools/Triton/build/triton /media/sf_SharedFolder/awft/score.py /media/sf_SharedFolder/awft/example1.out " + ''.join(seed.model.values()[:-1]))
  time.sleep(0.5)
  with open("/media/sf_SharedFolder/awft/score.txt", "w") as data:
    score = int(data.read(data))
  return score

def main():
  global workList
  global seed
  with open("/media/sf_SharedFolder/awft/worklist.pkl", "rb") as data:
    workList = pickle.load(data)
  seed = heapq.heappop(workList)[1]
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
  Triton.setArchitecture(triton.ARCH.X86_64)
  Triton.enableMode(triton.MODE.ALIGNED_MEMORY, True)
  pintool.startAnalysisFromSymbol("main")
  pintool.insertCall(symbolize_inputs, pintool.INSERT_POINT.ROUTINE_ENTRY, "main")
  pintool.insertCall(computeBlockCoverage, pintool.INSERT_POINT.BEFORE)
  pintool.insertCall(expandExecution, pintool.INSERT_POINT.FINI)
  pintool.runProgram()

if __name__ == "__main__":
  main()