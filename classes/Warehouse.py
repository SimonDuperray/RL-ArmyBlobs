import numpy as np
from classes.Blob import Blob
from classes.BlobTypes import BlobTypes

ENV_SIZE = 20

agent = Blob(ENV_SIZE, BlobTypes.PLAYER, x=1, y=1)
targets = [Blob(ENV_SIZE, BlobTypes.TARGET, x=18, y=18)]
enemies = [Blob(ENV_SIZE, BlobTypes.ENEMY, range=4, x=10, y=10)]

AGENT_N = 1
TARGETS_N = len(targets)
ENEMIES_N = len(enemies)

q_table = {}
vec = []

for tar in targets:
   vec.append(agent-tar)
for en in enemies:
   vec.append(agent-en)

print(vec)