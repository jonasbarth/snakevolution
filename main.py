from env import SnakeEnv
import time
from human_agent import HumanAgent


env = SnakeEnv(600, 600)
env.reset()

#agent = HumanAgent(env)
#agent.play()



env.step(1)
env.snake.add_tail()
env.step(1)
env.snake.add_tail()
env.step(1)
env.snake.add_tail()
env.step(1)
env.snake.add_tail()
env.step(1)
env.snake.add_tail()
env.step(1)
env.snake.add_tail()
env.step(1)
env.snake.add_tail()

for n in range(20):
    state, reward, done = env.step(1)

    if done:
        break




env.wn.mainloop()
