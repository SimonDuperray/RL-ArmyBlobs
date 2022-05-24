import matplotlib.pyplot as plt, numpy as np, math
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
      self.walls = []
      self.__points_in_walls = []
      self.fig = self.init_environment()
      self.draw_limits()
      self.agents = []
      self.targets = []
      self.enemies = []

   def __str__(self):
      return f"""
         - Warzone Size: {self.size}x{self.size}
         - Walls: {self.walls}
         - Points in walls: {self.__points_in_walls}
         - Agents: {[ag.__str__() for ag in self.agents]}
         - Targets: {[tar.__str__() for tar in self.targets]}
         - Enemies: {[ene.__str__() for ene in self.enemies]}
      """

   def init_environment(self):
      fig = plt.figure()
      fig.suptitle(f"({self.size}), {self.size}) Environment")
      plt.xlim(-self.size/10, self.size+self.size/10)
      plt.ylim(-self.size/10, self.size+self.size/10)
      plt.gcf().gca().set_aspect(1)
      return fig

   def draw_limits(self):
      f = self.fig.gca()
      f.plot([0, 0], [0, ENV_SIZE], color='black')
      f.plot([0, ENV_SIZE], [0, 0], color='black')
      f.plot([0, ENV_SIZE], [ENV_SIZE, ENV_SIZE], color='black')
      f.plot([ENV_SIZE, ENV_SIZE], [0, ENV_SIZE], color='black')

   def add_point(self, x, y, color=None, marker=None):
      f = self.fig.gca()
      f.scatter(x, y)

   def build_wall(self, p, w, h):
      f = self.fig.gca()
      f.add_patch(Rectangle((p[0], p[1]), w, h, facecolor="black", fill=True))
      self.walls.append({
         "p": p,
         "w": w,
         "h": h
      })
      self.__points_in_walls.append(self.compute_points_in_walls(p, w, h))

   def compute_points_in_walls(self, p, w, h):
      pts = []
      for i in range(p[0], p[0]+w+1):
         for j in range(p[1], p[1]+h+1):
            pts.append((i, j))
      all_points = self.points_in_walls+pts
      self.__points_in_walls = list(dict.fromkeys(all_points))

   @property
   def points_in_walls(self):
      return self.__points_in_walls

   def get_walls(self):
      return self.walls

   def add_agent(self, blob_agent):
      self.agents.append(blob_agent)
      f = self.fig.gca()
      f.scatter(self.agents[-1].x, self.agents[-1].y, color='blue', marker='<')

   def add_target(self, blob_target):
      self.targets.append(blob_target)
      f = self.fig.gca()
      f.scatter(self.targets[-1].x, self.targets[-1].y, color='green')

   def add_enemy(self, blob_enemy):
      self.enemies.append(blob_enemy)
      f = self.fig.gca()
      f.scatter(self.enemies[-1].x, self.enemies[-1].y, color='red', marker="<")
      range_ = plt.Circle((self.enemies[-1].x, self.enemies[-1].y), RANGE, color='red', fill=True, alpha=0.2)
      f.add_artist(range_)

   def is_existing_path(self):
      pass

   def is_in_enemies_range(self, x, y):
      for en in self.enemies:
         if math.sqrt((x-en.x)**2 + (y-en.y)**2) <= en.range:
            return True
      return False

   def run(self):
      plt.show()