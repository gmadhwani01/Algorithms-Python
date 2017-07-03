import glob
import random
import dpll
import time

def load(fn):
  f = open(fn, 'r')
  data = f.read()
  f.close()
  clauses = []
  lines = data.split("\n")
  for line in lines:
    if len(line) == 0 or line[0] in ['c', 'p', '%', '0']:
      continue
    clause = [int(x) for x in line.split()[0:-1]]
    clauses.append({x for x in clause})
  return clauses


files = [(fn, True) for fn in glob.glob("sat_tests/SAT/*.cnf")] + [(fn, False) for fn in glob.glob("sat_tests/UNSAT/*.cnf")]
random.shuffle(files)

for (fn, sat) in files:
  print(fn, end = ': ')
  s = dpll.Solver(load(fn))
  start=time.time()
  assert(s.solve() == sat)
  end=time.time()-start
  
  print("passed ",end)



