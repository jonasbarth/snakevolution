from env import SnakeEnv
import time
from human_agent import Human_Agent


env = SnakeEnv(600, 600)

agent = HumanAgent(env)

agent.play()
   


env.wn.mainloop()