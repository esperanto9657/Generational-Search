import triton
import pintool
import pickle

blockList = set()
score = 0
Triton = pintool.getTritonContext()
controlFlow = False

def computeScore(inst):
  global score
  global controlFlow
  if controlFlow:
    controlFlow = False
    if hex(inst.getAddress()) not in blockList:
      score += 1
  if inst.isControlFlow():
    controlFlow = True
  
def outputScore():
  print(score)

def main():
  global blockList
  with open("/media/sf_SharedFolder/awft/blocklist.pkl", "rb") as data:
    blockList = pickle.load(data)
  Triton.setArchitecture(triton.ARCH.X86_64)
  Triton.enableMode(triton.MODE.ALIGNED_MEMORY, True)
  pintool.startAnalysisFromSymbol("main")
  pintool.insertCall(computeScore, pintool.INSERT_POINT.BEFORE)
  pintool.insertCall(outputScore, pintool.INSERT_POINT.FINI)
  pintool.runProgram()

if __name__ == "__main__":
  main()