import pintool
import pickle

blockList = set()
score = 0

def computeScore(inst):
  global score
  if inst.isControlFlow() and inst.getAddress() not in blockList:
    score += 1
  
def writeScore():
  with open("/media/sf_SharedFolder/awft/score.txt", "w") as data:
    data.write(score)

def main():
  global blockList
  with open("/media/sf_SharedFolder/awft/blocklist.pkl", "rb") as data:
    blockList = pickle.load(data)
  pintool.startAnalysisFromSymbol("main")
  pintool.insertCall(computeScore, pintool.INSERT_POINT.BEFORE)
  pintool.insertCall(writeScore, pintool.INSERT_POINT.FINI)
  pintool.runProgram()

if __name__ == "__main__":
  main()