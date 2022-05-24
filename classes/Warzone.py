import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import Rectangle
from matplotlib import style

style.use('ggplot')

ENV_SIZE = 20
START_FOOD_POSITION = 19
START_PLAYER_POSITION = 2
RANGE = 2

class Warzone:
   def __init__(self, size):
      self.size = size
      self.fig = self.init_environment()

   def init_environment(self):
      fig = plt.figure()
      fig.suptitle(f"({self.size}), {self.size}) Environment")
      plt.xlim(-self.size/10, self.size+self.size/10)
      plt.ylim(-self.size/10, self.size+self.size/10)
      plt.gcf().gca().set_aspect(1)
      return fig

   def run(self):
      plt.show()