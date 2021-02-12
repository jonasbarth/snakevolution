from environment.env import SnakeEnv


class HumanAgent:

    def __init__(self, env: SnakeEnv):
        self.env = env


    def play(self):
        self.env.reset()
        wn = self.env.wn

        wn.onkeypress(self.w, "w")
        wn.onkeypress(self.d, "d")
        wn.onkeypress(self.s, "s")
        wn.onkeypress(self.a, "a")

        wn.listen()
        wn.mainloop()

    def w(self):
        self.env.step(0)

    def d(self):
        self.env.step(1)

    def s(self):
        self.env.step(2)

    def a(self):
        self.env.step(3)

