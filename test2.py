from telnetlib import DET
import numpy as np, matplotlib.pyplot as plt, time
plt.style.use('ggplot')

ENV_SIZE = 5

TARGET_STATE = (4, 4)
ENEMY_STATE = (3, 3)
WALLS = [(1, 1)]
AGENT_STATE = (0, 0)
DETERMINISTIC = True

class State:
   def __init__(self, state = AGENT_STATE):
      self.board = np.zeros([ENV_SIZE, ENV_SIZE])
      for wall in WALLS:
         self.board[wall[0], wall[1]] = -1
      self.state = state
      self.isEnd = False
      self.determine = DETERMINISTIC

   def giveReward(self):
      if self.state==TARGET_STATE:
         return 100
      elif self.state==ENEMY_STATE:
         return -50
      else:
         return -1

   def isEndFunc(self):
      if (self.state==TARGET_STATE) or (self.state==ENEMY_STATE):
         self.isEnd = True

   def nxtPosition(self, action):
      if self.determine:
         if action=='up':
            nxtState = (self.state[0]-1, self.state[1])
         elif action=='down':
            nxtState = (self.state[0]+1, self.state[1])
         elif action=='left':
            nxtState = (self.state[0], self.state[1]-1)
         else:
            nxtState = (self.state[0], self.state[1]+1)
         if (nxtState[0]>=0) and (nxtState[0]<(ENV_SIZE-1)):
            if (nxtState[1]>=0) and (nxtState[1]<(ENV_SIZE-1)):
               if nxtState not in WALLS:
                  return nxtState
               else:
                  print("WALL DETECTED")
         return self.state

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
   
   def chooseAction(self):
      max_next_reward = 0
      action = ""
      if np.random.uniform(0, 1)<=self.exp_rate:
         action = np.random.choice(self.actions)
      else:
         for a in self.actions:
            next_reward = self.state_values[self.State.nxtPosition(a)]
            if next_reward>=max_next_reward:
               action = a
               max_next_reward = next_reward
      return action
   
   def takeAction(self, action):
      position = self.State.nxtPosition(action)
      return State(state=position)
   
   def reset(self):
      self.states = []
      self.State = State()

   def play(self, rounds=10):
      i=0
      while i<= rounds:
         if self.State.isEndFunc():
            reward = self.State.giveReward()
            self.state_values[self.State.state] = reward
            print(f"Game ended - Reward: {reward}")
            for s in reversed(self.states):
               reward = self.state_values[s]+self.lr*(reward-self.state_values[s])
               self.state_values[s] = round(reward, 3)
            self.reset()
            i+=1
            print(f"i: {i}")
         else:
            action = self.chooseAction()
            self.states.append(self.State.nxtPosition(action))
            print(f"current position {self.State.state} - action: {action}")
            self.State = self.takeAction(action)
            self.State.isEndFunc()
            print(f"next state: {self.State.state}")
            print('----------------------------')
            if i%5==0:
               # time.sleep(2)
               plt.suptitle(f'Round {i}/{rounds}')
               plt.xlim(-1, ENV_SIZE+1)
               plt.ylim(-1, ENV_SIZE+1)
               # plot borders
               plt.plot([0, 0], [ENV_SIZE, 0], color='black', linewidth=2)
               plt.plot([0, ENV_SIZE], [ENV_SIZE, ENV_SIZE], color='black', linewidth=2)
               plt.plot([ENV_SIZE, ENV_SIZE], [ENV_SIZE, 0], color='black', linewidth=2)
               plt.plot([ENV_SIZE, 0], [0, 0], color='black', linewidth=2)
               # plot blobs instances
               plt.scatter(self.State.state[0], self.State.state[1], color='blue', label='Agent')
               plt.scatter(TARGET_STATE[0], TARGET_STATE[1], color='green', label='Target')
               plt.scatter(ENEMY_STATE[0], ENEMY_STATE[1], color='red', label='Enemy')
               # plot walls
               for wall in WALLS:
                  plt.scatter(wall[0], wall[1], color='black', label='Wall', marker='x')
               plt.legend(loc='upper left')
               plt.pause(.1)
               plt.clf()

   def showValues(self):
      for i in range(0, BOARD_ROWS):
         print('----------------------------------')
         out = '| '
         for j in range(0, BOARD_COLS):
            out += str(self.state_values[(i, j)]).ljust(6) + ' | '
         print(out)
      print('----------------------------------')


if __name__ == '__main__':
   agent = Agent()
   agent.play(20)
   print(agent.showValues())