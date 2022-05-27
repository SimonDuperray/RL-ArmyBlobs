from classes.Blob import Blob
from classes.Warzone import Warzone
from classes.BlobTypes import BlobTypes
import matplotlib.pyplot as plt, numpy as np

ENV_SIZE = 20
EPISODES = 10
SHOW_EVERY = 2
EPSILON = 0.9
EPS_DECAY = 1e-3
EPISODES = 30000
SHOW_EVERY = 3000
EPS_DECAY = 0.9998
LEARNING_RATE = 0.1
DISCOUNT = 0.95
ENEMY_PENALTY = 300
TARGET_REWARD = 100
MOOVE_PENALTY = 1
# ===
BOARD_COLS = 5
BOARD_ROWS = 5
ENV_SIZE = 5

WIN_STATE = (5, 5)
ENEMY_STATE = (4, 4)
START = (1, 1)
DETERMINISTIC = True

# WALLS = [(2, 2), (3, 3), (4, 4)]
TARGET_REWARD = 100
MOOVE_PENALTY = 1
ENEMY_PENALTY = 50

class State:
   def __init__(self, state=START):
      self.board = np.full([BOARD_ROWS+1, BOARD_COLS+1], -MOOVE_PENALTY)
      self.board[ENEMY_STATE[0], ENEMY_STATE[1]] = -ENEMY_PENALTY
      self.board[WIN_STATE[0], WIN_STATE[1]] = TARGET_REWARD
      self.state = state
      self.isEnd = False
      self.determine = DETERMINISTIC

   def give_reward(self):
      if self.state == WIN_STATE:
         return TARGET_REWARD
      elif self.state == ENEMY_STATE:
         return ENEMY_PENALTY
      else:
         return -MOOVE_PENALTY

   def is_end(self):
      if(self.state==WIN_STATE or self.state==ENEMY_STATE):
         self.isEnd = True

   def next_position(self, action):
      if action=="up":
         next_state = (self.state[0]-1, self.state[1])
      elif action=="down":
         next_state = (self.state[0]+1, self.state[1])
      elif action=="left":
         next_state = (self.state[0], self.state[1]-1)
      else:
         next_state = (self.state[0], self.state[1]+1)
      
      if (next_state[0]>=0) and (next_state[0]<=ENV_SIZE-1):
         if (next_state[1]>=0) and (next_state[1]<=ENV_SIZE-1):
            if next_state != ENEMY_STATE:
               return next_state
      return self.state

   def show_board(self):
      self.board[self.state] = 1
      for i in range(0, ENV_SIZE):
         print('-----------------')
         out = '| '
         for j in range(0, ENV_SIZE):
            if self.board[i, j] == 1:
               token = '*'
            if self.board[i, j] == -1:
               token = 'z'
            if self.board[i, j] == 0:
               token = '0'
            out += token + ' | '
         print(out)
      print('-----------------')

class Agent:
   def __init__(self):
      self.states = []
      self.actions = ['up', 'down', 'left', 'right']
      self.State = State()
      self.lr = 0.2
      self.exp_rate = 0.3
      self.state_values = {}
      for i in range(ENV_SIZE):
         for j in range(ENV_SIZE):
            self.state_values[(i, j)] = 0

   def choose_action(self):
      max_next_reward = 0
      action = ""
      if np.random.uniform(0, 1)<=self.exp_rate:
         action = np.random.choice(self.actions)
      else:
         for a in self.actions:
            next_reward = self.state_values[self.State.next_position(a)]
            if next_reward>=max_next_reward:
               action = a
               max_next_reward = next_reward
      return action

   def take_action(self, action):
      position = self.State.next_position(action)
      return State(state=position)

   def reset(self):
      self.states = []
      self.State = State()

   def play(self, rounds=10):
      i=0
      while i<rounds:
         if self.State.is_end:
            reward = self.State.give_reward()
            self.state_values[self.State.state] = reward
            print(f"Game Ended - Reward: {reward}")
            for s in reversed(self.states):
               reward = self.state_values[s]+self.lr*(reward-self.state_values[s])
               self.state_values[s] = round(reward, 3)
            self.reset()
            i+=1
         else:
            action = self.choose_action()
            self.states.append(self.State.next_position(action))
            print(f"current position {self.State.state} - action: {action}")
            self.State = self.take_action(action)
            self.State.is_end()
            print(f"next state: {self.State.state}")
            print('-----------------')
            # plot env
            plt.suptitle(f"Round {i}")
            plt.xlim(-1, ENV_SIZE+1)
            plt.ylim(-1, ENV_SIZE+1)
            plt.plot([0, 0], [ENV_SIZE, 0], color="black", linewidth=2)
            plt.plot([0, ENV_SIZE], [ENV_SIZE, ENV_SIZE], color="black", linewidth=2)
            plt.plot([ENV_SIZE, ENV_SIZE], [ENV_SIZE, 0], color="black", linewidth=2)
            plt.plot([ENV_SIZE, 0], [0, 0], color="black", linewidth=2)
            plt.scatter(self.State.state[1], self.State.state[0], color='b')
            plt.scatter(WIN_STATE[0], WIN_STATE[1], color='green')
            plt.Scatter(ENEMY_STATE[0], ENEMY_STATE[1], color='red', marker='x')
            plt.pause(0.1)
            plt.clf()

   def show_values(self):
      for i in range(0, ENV_SIZE):
         print('----------------------------------')
         out = '| '
         for j in range(0, ENV_SIZE):
            out += str(self.state_values[(i, j)])+' | '
         print(out)
      print('----------------------------------')


if __name__ == "__main__":
   agent = Agent()
   agent.play(50)
   print(agent.show_values())

# epsilon = 0.9

# warzone = Warzone(size=ENV_SIZE)
# warzone.build_wall((0, 14), 5, 6)
# warzone.build_wall((5, 9), 2, 5)
# warzone.build_wall((15, 0), 5, 5)
# warzone.add_agent(Blob(ENV_SIZE, BlobTypes.PLAYER, x=1, y=1))
# warzone.add_target(Blob(ENV_SIZE, BlobTypes.TARGET, x=18, y=18))
# warzone.add_enemy(Blob(ENV_SIZE, BlobTypes.ENEMY, range=4, x=10, y=10))
# warzone.add_enemy(Blob(ENV_SIZE, BlobTypes.ENEMY, range=2, x=17, y=10))
# warzone.run()
# warzone.train()
# plt.imshow(warzone.get_rewards_map(), cmap='hot', interpolation='nearest')
# plt.show()
# print(warzone)
