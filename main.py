from calendar import c
import numpy as np, matplotlib.pyplot as plt
plt.style.use('ggplot')

# global variables
BOARD_ROWS = 5
BOARD_COLS = 5
TARGET_STATE = (4, 4)
LOSE_STATES = [(1, 3)]
START = (4, 0)
WALLS = [
   ((1, 2), 1, 2)
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
            pts.append((yi, xi))
   return list(dict.fromkeys(pts))

class State:
   def __init__(self, state=START):
      self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
      for wall in WALLS:
         self.board[wall[0], wall[1]]=-1
      self.state = state
      self.isEnd = False
      self.determine = DETERMINISTIC
      self.impossible_points = []

   def giveReward(self):
      if self.state == TARGET_STATE:
         return 1
      elif self.state in LOSE_STATES:
         return -1
      else:
         return 0

   def isEndFunc(self):
      if (self.state == TARGET_STATE) or (self.state in LOSE_STATES):
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

      # initial state reward
      self.state_values = {}
      for i in range(BOARD_ROWS+1):
         for j in range(BOARD_COLS+1):
            self.state_values[(i, j)] = 0  # set initial value to 0

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
      return State(state=position)

   def reset(self):
      self.states = []
      self.State = State()

   def play(self, rounds=10):
      i = 0
      while i < rounds+1:
         # to the end of game back propagate reward
         if self.State.isEnd:
            # back propagate
            reward = self.State.giveReward()
            # explicitly assign end state to reward values
            self.state_values[self.State.state] = reward  # this is optional
            # print("Game End Reward", reward)
            for s in reversed(self.states):
               reward = self.state_values[s] + self.lr * (reward - self.state_values[s])
               self.state_values[s] = round(reward, 3)
            self.reset()
            i += 1
         else:
            action = self.chooseAction()
            # append trace
            self.states.append(self.State.nxtPosition(action))
            # print("current position {} action {}".format(self.State.state, action))
            # by taking the action, it reaches the next state
            self.State = self.takeAction(action)
            # mark is end
            self.State.isEndFunc()
            # print("nxt state", self.State.state)
            # print("---------------------")
            if i%2500==0:
               plt.suptitle(f"Round {i}/{rounds}")
               plt.xlim(-1, BOARD_COLS+1)
               plt.ylim(-1, BOARD_ROWS+1)
               # plot borders
               plt.plot([0, BOARD_COLS], [0, 0], color='black')
               plt.plot([0, 0], [0, BOARD_ROWS], color='black')
               plt.plot([BOARD_COLS, BOARD_COLS], [0, BOARD_ROWS], color='black')
               plt.plot([0, BOARD_COLS], [BOARD_ROWS, BOARD_ROWS], color='black')
               for loose in LOSE_STATES:
                  plt.scatter(loose[1], loose[0], marker='x', color='red', label='loose')
               for wall in WALLS:
                  # plt.scatter(wall[1], wall[0], marker='x', color='black', label='wall')
                  x = wall[0][0]
                  y = wall[0][1]
                  w = wall[1]
                  h = wall[2]
                  plt.plot([x, x], [y, y+h], color='black')
                  plt.plot([x, x+w], [y, y], color='black')
                  plt.plot([x, x+w], [y+h, y+h], color='black')
                  plt.plot([x+w, x+w], [y, y+h], color='black')
               plt.scatter(self.State.state[1], self.State.state[0], color='blue', label="agent")
               plt.scatter(TARGET_STATE[1], TARGET_STATE[0], color='green', marker='<', label="target")
               plt.legend(loc='upper left')
               plt.gca().invert_yaxis()
               plt.pause(.1)
               plt.clf()

   def showValues(self):
      for i in range(0, BOARD_ROWS+1):
         print('-------------------------------------------------------')
         out = '| '
         for j in range(0, BOARD_COLS+1):
            out += str(self.state_values[(i, j)]).ljust(6) + ' | '
         print(out)
      print('-------------------------------------------------------')


if __name__ == "__main__":
   ag = Agent()
   ag.play(10000)
   print(ag.showValues())