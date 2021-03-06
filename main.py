import numpy as np, matplotlib.pyplot as plt, math
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
plt.style.use('ggplot')

# global variables
BOARD_ROWS = 10
BOARD_COLS = 10
TARGET_STATE = (0, BOARD_COLS-1)
ENEMIES_STATES = [
   ((2, 3), 2),
   ((6, 3), 1),
   ((6, 0), 1),
   ((6, 1), 1),
   ((6, 4), 1),
   ((6, 5), 1)
]
START = (8, 0)
WALLS = [
   ((1, 2), 1, 2),
   ((5, 5), 5, 2)
]
DETERMINISTIC = True


def get_points_in_wall(walls):
   pts = []
   for wall in walls:
      x = wall[0][0]
      y = wall[0][1]
      w = wall[1]
      h = wall[2]
      for xi in range(x, x+w+1):
         for yi in range(y, y+h+1):
            pts.append((xi, yi))
   return list(dict.fromkeys(pts))

def is_in_enemy_range(enemy, agent_state):
   # for enemy in enemies:
      # print(f"enemy[0][1]: {type(enemy[0][1])} - enemy[0][0]: {type(enemy[0][0])} - agent[1]: {type(agent_state[1])} - agent[0]: {type(agent_state[0])} - enemy[1]: {type(enemy[1])}")
      # print(f"enemy: {enemy} - agent: {agent_state}")
   if round(math.dist((enemy[0][1], enemy[0][0]), (agent_state[1], agent_state[0])), 2)<float(enemy[1]):
      return True
   return False

class State:
   def __init__(self, state=START):
      self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
      for wall in WALLS:
         self.board[wall[0], wall[1]]=-1
      self.state = state
      self.isEnd = False
      self.determine = DETERMINISTIC

   def giveReward(self):
      for enemy in ENEMIES_STATES:
         if self.state==enemy[0]:
            return -1
         if is_in_enemy_range(enemy, self.state):
            return -0.5
      if self.state == TARGET_STATE:
         return 1
      # elif self.state in ENEMIES_STATES:
         # return -1
      else:
         return 0

   def isEndFunc(self):
      if (self.state == TARGET_STATE) or (self.state in ENEMIES_STATES):
         self.isEnd = True

   def nxtPosition(self, action):
      """
      action: up, down, left, right
      -------------
      0 | 1 | 2| 3|
      1 |
      2 |
      return next position
      """
      if self.determine:
         if action == "up":
            nxtState = (self.state[0] - 1, self.state[1])
         elif action == "down":
            nxtState = (self.state[0] + 1, self.state[1])
         elif action == "left":
            nxtState = (self.state[0], self.state[1] - 1)
         else:
            nxtState = (self.state[0], self.state[1] + 1)
         # if next state legal
         if (nxtState[0] >= 0) and (nxtState[0] <= (BOARD_ROWS)):
            if (nxtState[1] >= 0) and (nxtState[1] <= (BOARD_COLS)):
               if nxtState not in get_points_in_wall(WALLS):
                  return nxtState
         return self.state

   def showBoard(self):
      self.board[self.state] = 1
      for i in range(0, BOARD_ROWS):
         print('-----------------------')
         out = '| '
         for j in range(0, BOARD_COLS):
            if self.board[i, j] == 1:
               token = '*'
            if self.board[i, j] == -1:
               token = 'z'
            if self.board[i, j] == 0:
               token = '0'
            out += token + ' | '
         print(out)
      print('-----------------------')


# Agent of player

class Agent:

   def __init__(self):
      self.states = []
      self.actions = ["up", "down", "left", "right"]
      self.State = State()
      self.lr = 0.2
      self.exp_rate = 0.3
      self.cumulative_mooves = 0
      # initial state reward
      self.state_values = {}
      for i in range(BOARD_ROWS+1):
         for j in range(BOARD_COLS+1):
            self.state_values[(i, j)] = 0  # set initial value to 0
      # self.times_in_range = 0
      

   def chooseAction(self):
      # choose action with most expected value
      mx_nxt_reward = 0
      action = ""

      if np.random.uniform(0, 1) <= self.exp_rate:
         action = np.random.choice(self.actions)
      else:
         # greedy action
         for a in self.actions:
            # if the action is deterministic
            nxt_reward = self.state_values[self.State.nxtPosition(a)]
            if nxt_reward >= mx_nxt_reward:
               action = a
               mx_nxt_reward = nxt_reward
      return action

   def takeAction(self, action):
      position = self.State.nxtPosition(action)
      self.cumulative_mooves+=1
      return State(state=position)

   def is_tired(self):
      return self.cumulative_mooves==200

   def reset(self):
      self.states = []
      self.State = State()

   def play(self, rounds=10):
      fig = plt.figure()
      ax = fig.add_subplot(111, projection='3d')
      i = 0
      while i < rounds+1:
         axs, ays, azs = [], [], []
         # to the end of game back propagate reward
         if self.State.isEnd:
            # back propagate
            reward = self.State.giveReward()
            # if reward==-0.5:
            #    self.times_in_range+=1
            # explicitly assign end state to reward values
            self.state_values[self.State.state] = reward  # this is optional
            # print("Game End Reward", reward)
            for s in reversed(self.states):
               reward = self.state_values[s] + self.lr * (reward - self.state_values[s])
               self.state_values[s] = round(reward, 3)
            self.reset()
            i += 1
         else:
            # for j in range(200):
            action = self.chooseAction()
            # append trace
            self.states.append(self.State.nxtPosition(action))
            # print("current position {} action {}".format(self.State.state, action))
            # by taking the action, it reaches the next state
            self.State = self.takeAction(action)
            axs.append(self.State.state[1])
            ays.append(self.State.state[0])
            azs.append(0)
            # mark is end
            self.State.isEndFunc()
            if self.is_tired():
               self.cumulative_mooves = 0
               i+=1
            else:
               # print("nxt state", self.State.state)
               # print("---------------------")
               if i%5000==0:
               # if i==rounds-1:
                  fig.suptitle(f"Round {i}/{rounds} - Mooves: {self.cumulative_mooves}/200")
                  ax.set_xlim(-1, BOARD_COLS+1)
                  ax.set_ylim(-1, BOARD_ROWS+1)
                  ax.set_xlabel('x axis')
                  ax.set_ylabel('y axis')
                  ax.set_zlabel('z axis')

                  ax.set_zlim(0,3)
                  # plot borders
                  ax.plot([0, BOARD_COLS], [0, 0], color='black')
                  ax.plot([0, 0], [0, BOARD_ROWS], color='black')
                  ax.plot([BOARD_COLS, BOARD_COLS], [0, BOARD_ROWS], color='black')
                  ax.plot([0, BOARD_COLS], [BOARD_ROWS, BOARD_ROWS], color='black')
                  # scatter enemy
                  for enemy in ENEMIES_STATES:
                     ax.scatter(enemy[0][1], enemy[0][0], marker='x', color='red', label='enemy')
                     enemy_range = Circle((enemy[0][1], enemy[0][0]), radius=enemy[1], facecolor='red', alpha=.1)
                     ax.add_patch(enemy_range)
                     art3d.pathpatch_2d_to_3d(enemy_range, z=0, zdir="z")
                     # enemy_range = Circle((enemy[0][1], enemy[0][0]), radius=enemy[1], facecolor='red', alpha=.1)
                     # ax.add_patch(enemy_range)
                     # art3d.pathpatch_2d_to_3d(enemy_range, z=0.3, zdir="z")
                  # plot walls
                  for wall in WALLS:
                     x = wall[0][0]
                     y = wall[0][1]
                     w = wall[1]
                     h = wall[2]
                     # down
                     ax.plot([x, x], [y, y+h], [0,0], color='black', linewidth=.3)
                     ax.plot([x, x+w], [y, y], [0,0], color='black', linewidth=.3)
                     ax.plot([x, x+w], [y+h, y+h], [0,0], color='black', linewidth=.3)
                     ax.plot([x+w, x+w], [y, y+h], [0,0], color='black', linewidth=.3)
                     # corners
                     ax.plot([x, x], [y, y], [0,.5], color='black', linewidth=.3)
                     ax.plot([x+w, x+w], [y, y], [0,.5], color='black', linewidth=.3)
                     ax.plot([x, x], [y+h, y+h], [0,.5], color='black', linewidth=.3)
                     ax.plot([x+w, x+w], [y+h, y+h], [0,.5], color='black', linewidth=.3)
                     # top
                     ax.plot([x, x], [y, y+h], [.5,.5], color='black', linewidth=.3)
                     ax.plot([x, x+w], [y, y], [.5,.5], color='black', linewidth=.3)
                     ax.plot([x, x+w], [y+h, y+h], [.5,.5], color='black', linewidth=.3)
                     ax.plot([x+w, x+w], [y, y+h], [.5,.5], color='black', linewidth=.3)
                  # plot agent
                  ax.plot([ays[-1], ays[-1]], [axs[-1], axs[-1]], [0, .2], color='blue', alpha=1, linewidth=2, label='agent')
                  # scatter target
                  ax.scatter(TARGET_STATE[0], TARGET_STATE[1], color='green', marker='<', label="target", s=50)
                  plt.legend(loc='upper left')
                  plt.gca().invert_yaxis()
                  plt.draw()
                  plt.pause(.1)
                  ax.clear()

   def showValues(self):
      li = ['----------' for _ in range(BOARD_ROWS)]
      lines = ''.join(li)
      for i in range(0, BOARD_ROWS+1):
         print(lines)
         out = '| '
         for j in range(0, BOARD_COLS+1):
            out += str(self.state_values[(i, j)]).ljust(6) + ' | '
         print(out)
      print(lines)


if __name__ == "__main__":
   print(get_points_in_wall(WALLS))
   ag = Agent()
   ag.play(20000)
   print(ag.showValues())