import matplotlib.pyplot as plt, numpy as np, math
from matplotlib.patches import Rectangle, Circle
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
      self.rm = None
      self.q_values = np.zeros((self.size, self.size, 4))
      self.actions = ['up', 'right', 'down', 'left']
      self.epsilon = 0.9
      self.discount_factor = 0.9
      self.learning_rate = 0.9

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
      fig.suptitle(f"({self.size}, {self.size}) Environment")
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

   def get_points_in_range(self, blob_enemy):
      # circle = Circle((blob_enemy.x, blob_enemy.y), radius=blob_enemy.range)
      # points = [(x, y) for x, y in zip([i for i in range(self.size)], [i for i in range(self.size)]) if circle.contains_point([x, y])]
      # return points
      pts = []
      p = (blob_enemy.x, blob_enemy.y)
      r = blob_enemy.range
      for i in range(1, r+1):
         pts.append(
            (p[0]-i, p[1])
         )
         pts.append(
            (p[0], p[1]-i)
         )
         pts.append(
            (p[0]+i, p[1])
         )
         pts.append(
            (p[0], p[1]+i)
         )
      print(f"pts in range: {pts}")
      return pts

   def add_enemy(self, blob_enemy):
      ranged_points = self.get_points_in_range(blob_enemy)
      self.enemies.append({
         'blob_enemy': blob_enemy,
         'ranged_points': ranged_points
      })
      f = self.fig.gca()
      f.scatter(self.enemies[-1]['blob_enemy'].x, self.enemies[-1]['blob_enemy'].y, color='red', marker="<")
      range_ = plt.Circle((self.enemies[-1]['blob_enemy'].x, self.enemies[-1]['blob_enemy'].y), self.enemies[-1]['blob_enemy'].range, color='red', fill=True, alpha=0.2)
      f.add_artist(range_)

   def is_existing_path(self):
      pass

   def is_in_enemies_range(self, x, y):
      for en in self.enemies:
         if math.sqrt((x-en.x)**2 + (y-en.y)**2) <= en.range:
            return True
      return False

   def get_rewards_map(self):
      rm = np.full((self.size+1, self.size+1), -1.)
      pts_in_walls = self.__points_in_walls
      for pt_in_wall in pts_in_walls:
         rm[self.size-pt_in_wall[1], pt_in_wall[0]] = -100.
      # targets
      for target in self.targets:
         rm[self.size-target.y, target.x] = 100.
      # enemies
      for enemy in self.enemies:
         rm[self.size-enemy['blob_enemy'].y, enemy['blob_enemy'].x] = -50.
         for r in enemy['ranged_points']:
            rm[self.size-r[1], r[0]] = -20.
      self.rm = rm
      return self.rm

   def is_terminal_state(self, current_row_index, current_col_index):
      if self.rm[current_col_index, current_row_index] == -1.:
         return False
      else:
         return True

   def get_starting_location(self):
      current_row_index = np.random.randint(self.size)
      current_column_index = np.random.randint(self.size)
      while self.is_terminal_state(current_row_index, current_column_index):
         current_row_index = np.random.randint(self.size)
         current_column_index = np.random.randint(self.size)
      return current_row_index, current_column_index

   def get_next_action(self, current_row_index, current_column_index, epsilon):
      if np.random.random() < epsilon:
         return np.argmax(self.q_values[current_row_index, current_column_index])
      else:
         return np.random.randint(4)

   def get_next_location(self, current_row_index, current_column_index, action_index):
      new_row_index = current_row_index
      new_column_index = current_column_index
      if self.actions[action_index] == 'up' and current_row_index > 0:
         new_row_index -= 1
      elif self.actions[action_index] == 'right' and current_column_index < self.size - 1:
         new_column_index += 1
      elif self.actions[action_index] == 'down' and current_row_index < self.size - 1:
         new_row_index += 1
      elif self.actions[action_index] == 'left' and current_column_index > 0:
         new_column_index -= 1
      return new_row_index, new_column_index

   def get_shortest_path(self, start_row_index, start_column_index):
      #return immediately if this is an invalid starting location
      if self.is_terminal_state(start_row_index, start_column_index):
         return []
      else: #if this is a 'legal' starting location
         current_row_index, current_column_index = start_row_index, start_column_index
         shortest_path = []
         shortest_path.append([current_row_index, current_column_index])
         #continue moving along the path until we reach the goal (i.e., the item packaging location)
         while not self.is_terminal_state(current_row_index, current_column_index):
            #get the best action to take
            action_index = self.get_next_action(current_row_index, current_column_index, 1.)
            #move to the next location on the path, and add the new location to the list
            current_row_index, current_column_index = self.get_next_location(current_row_index, current_column_index, action_index)
            shortest_path.append([current_row_index, current_column_index])
         return shortest_path

   def train(self):
      for episode in range(1000):
         #get the starting location for this episode
         row_index, column_index = self.get_starting_location()
         #continue taking actions (i.e., moving) until we reach a terminal state
         #(i.e., until we reach the item packaging area or crash into an item storage location)
         while not self.is_terminal_state(row_index, column_index):
            #choose which action to take (i.e., where to move next)
            action_index = self.get_next_action(row_index, column_index, self.epsilon)
            #perform the chosen action, and transition to the next state (i.e., move to the next location)
            old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
            row_index, column_index = self.get_next_location(row_index, column_index, action_index)
            #receive the reward for moving to the new state, and calculate the temporal difference
            reward = self.rm[row_index, column_index]
            old_q_value = self.q_values[old_row_index, old_column_index, action_index]
            temporal_difference = reward + (self.discount_factor * np.max(self.q_values[row_index, column_index])) - old_q_value
            #update the Q-value for the previous state and action pair
            new_q_value = old_q_value + (self.learning_rate * temporal_difference)
            self.q_values[old_row_index, old_column_index, action_index] = new_q_value
      print('Training complete!')

   def run(self):
      plt.show()