from env import SnakeEnv
import time


env = SnakeEnv(600, 600)
env.reset()


for n in range(1):
    env.step(1)
   


env.wn.mainloop()