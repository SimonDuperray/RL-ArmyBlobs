import matplotlib.pyplot as plt, numpy as np, time
from matplotlib.patches import Rectangle
from matplotlib import style
from classes.Blob import Blob
from classes.BlobTypes import BlobTypes

style.use('ggplot')

ENV_SIZE = 20
START_FOOD_POSITION = 19
START_PLAYER_POSITION = 2
RANGE = 2

def create_environment(env_size):
   fig = plt.figure()
   fig.suptitle(f'{env_size}x{env_size} Environment')
   plt.xlim(-env_size/10, env_size+env_size/10)
   plt.ylim(-env_size/10, env_size+env_size/10)
   plt.gcf().gca().set_aspect(1)
   return fig

def add_point(fig, x, y):
   fig.gca().scatter(x, y, color='red')

def draw_limits(fig, size):
   f = fig.gca()
   f.plot([0, 0], [0, ENV_SIZE], color='black')
   f.plot([0, ENV_SIZE], [0, 0], color='black')
   f.plot([0, ENV_SIZE], [ENV_SIZE, ENV_SIZE], color='black')
   f.plot([ENV_SIZE, ENV_SIZE], [0, ENV_SIZE], color='black')

def build_rect_wall(fig, p1, width, height):
   f = fig.gca()
   f.add_patch(Rectangle((p1[0], p1[1]), width, height, facecolor="black", fill=True))

def scatter_player(fig, player):
   fig.gca().scatter(player.x, player.y, color='blue', marker="<")

def scatter_enemy(fig, enemy):
   fig.gca().scatter(enemy.x, enemy.y, color="red", marker="x")
   enemy_border = plt.Circle((enemy.x, enemy.y), enemy.range, facecolor="red", fill=True, alpha=0.2, edgecolor="red")
   plt.gcf().gca().add_artist(enemy_border)

def scatter_target(fig, target):
   fig.gca().scatter(target.x, target.y, color='green')

def generate_blobs(n_players=1, n_targets=1, n_enemies=2):
   target = Blob(env_size=ENV_SIZE, blob_type=BlobTypes.TARGET, x=START_FOOD_POSITION, y=START_FOOD_POSITION)
   player = Blob(env_size=ENV_SIZE, blob_type=BlobTypes.PLAYER, x=START_PLAYER_POSITION, y=START_PLAYER_POSITION)
   e1 = Blob(env_size=ENV_SIZE, blob_type=BlobTypes.ENEMY, range=RANGE, x=5, y=15)
   e2 = Blob(env_size=ENV_SIZE, blob_type=BlobTypes.ENEMY, range=RANGE, x=10, y=10)

   return target, player, e1, e2

def generate_environment():
   fig = create_environment(ENV_SIZE)
   draw_limits(fig, ENV_SIZE)
   build_rect_wall(fig, (0, 11), 2, 9)
   build_rect_wall(fig, (11, 6), 6, 3)
   scatter_target(fig, target)
   scatter_player(fig, player)
   scatter_enemy(fig, e1)
   scatter_enemy(fig, e2)

   return fig

target, player, e1, e2 = generate_blobs()
fig = generate_environment()

plt.show()