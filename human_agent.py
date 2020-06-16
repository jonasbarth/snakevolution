

class HumanAgent:

    def __init__(self, env):
        self.env = env


    def play(self):
        self.env.reset()
        wn = self.env.wn

        wn.onkeypress(self.env.step(0), "w")
        wn.onkeypress(self.env.step(1), "d")
        wn.onkeypress(self.env.step(2), "s")
        wn.onkeypress(self.env.step(3), "a")

