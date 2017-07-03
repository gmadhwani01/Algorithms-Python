import wumpus


width = 10

blocks = set()

for x in range(width+1):
  blocks.add((0, x))
  blocks.add((x, 0))
  blocks.add((width,x))
  blocks.add((x, width))

gold = {(8,8)}
pits = {(1,3)}
wumpus_location = {(7,7)}
initial_location = (1,1)

world1 = wumpus.WumpusWorld(blocks = blocks, gold = gold, wumpus = wumpus_location, pits = pits, initial_location = initial_location)

