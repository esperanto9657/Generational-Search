import triton
import pintool
import heapq
import pickle
import copy
import os

FILE_PATH = "/media/sf_SharedFolder/Generational-Search/"
SAMPLE_PATH = "/media/sf_SharedFolder/Generational-Search/example1.out "
Triton = pintool.getTritonContext()
workList = []
seed = None
blockList = set()
controlFlow = False

class Seed:
  def __init__(self, model = None, bound = 0):
    self.model = model if model else {}
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
            newSeed = Seed(newModel, j + 1)
            childs.append(newSeed)
  with open(FILE_PATH + "blocklist.pkl", "wb") as data:
    print(blockList)
    pickle.dump(blockList, data)
  with open(FILE_PATH + "childlist.pkl", "wb") as data:
    pickle.dump(childs, data)

def computeBlockCoverage(inst):
  global blockList
  global controlFlow
  if controlFlow:
    blockList.add(hex(inst.getAddress()))
    controlFlow = False
  if inst.isControlFlow():
    controlFlow = True

def main():
  global workList
  global seed
  global blockList
  if os.path.exists(FILE_PATH + "blocklist.pkl"):
    with open(FILE_PATH + "blocklist.pkl", "rb") as data:
      blockList = pickle.load(data)
  with open(FILE_PATH + "worklist.pkl", "rb") as data:
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