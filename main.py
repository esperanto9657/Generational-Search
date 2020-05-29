import triton
import pintool

Triton = pintool.getTritonContext()

class Seed:
  def __init__(self, model, bound):
    self.model = model
    self.bound = bound

def search(inputSeed):
  workList = []
  scores = []
  runCheck(inputSeed)
  while len(workList) > 0:
    item = workList.pop()
    childs = expandExecution(item)
    while len(childs) > 0:
      newItem = childs.pop()
      runCheck(newItem)
      scores.append(score(newItem))
      workList.append(newItem)
  return sorted(scores)

def expandExecution(item):
  childs = []
  ast = Triton.getAstContext()
  constraint_list = ast.equal(ast.bvtrue(), ast.bvtrue())
  PC = computePathConstraint(item)
  for j in range(item.bound, len(PC)):
    if not PC[j].isMultipleBranches():
      continue
    for branch_constraint in PC[j].getBranchConstraints():
      newPath = ast.land(constraint_list, branch_constraint[¨constraint¨])
      if branch_constraint[¨isTaken¨]:
        constraint_list = newPath
      else:
        model = Triton.getModel(newPath)
        if model:
          newModel = item.model.update(zip(model.keys(),model.values()))
          newItem = Seed(newModel, j)
          childs.append(newItem)
  return childs
  
def runCheck(item):

def score(item):
  score = 0
  return score

def computePathConstraint(item):
  Triton.setArchitecture(triton.ARCH.X86_64)
  Triton.enableMode(triton.MODE.ALIGNED_MEMORY)
  pintool.startAnalysisFromSymbol(´main´)
  pintool.insertCall(symbolize_inputs, pintools.INSERT_POINT.ROUTINE_ENTRY, ´top´)
  pintool.runProgram()
  PC = Triton.getPathConstraints()
  return PC

def main():
  with open(¨log.txt¨, ¨w¨) as out:
    out.write(search())

if __name__ == ´__main__´:
  main()
