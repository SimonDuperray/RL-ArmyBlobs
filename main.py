from classes.Blob import Blob
from classes.Warzone import Warzone
from classes.BlobTypes import BlobTypes

import matplotlib.pyplot as plt

ENV_SIZE = 20
ITERATIONS = 10
SHOW_EVERY = 2

warzone = Warzone(size=ENV_SIZE)
warzone.build_wall((0, 14), 5, 6)
warzone.build_wall((5, 9), 2, 5)
warzone.build_wall((15, 0), 5, 5)
warzone.add_agent(Blob(ENV_SIZE, BlobTypes.PLAYER, x=1, y=1))
warzone.add_target(Blob(ENV_SIZE, BlobTypes.TARGET, x=18, y=18))
warzone.add_enemy(Blob(ENV_SIZE, BlobTypes.ENEMY, range=4, x=10, y=10))
warzone.add_enemy(Blob(ENV_SIZE, BlobTypes.ENEMY, range=2, x=17, y=10))
for it in range(ITERATIONS):
   warzone.train()
   if it % SHOW_EVERY == 0:
      warzone.run()
warzone.train()
# plt.imshow(rm, cmap='hot', interpolation='nearest')
# plt.show()
# print(warzone)