from agents.simple_deep_q_agent import SimpleDeepQAgent
from game.snake import SnakeGame
from rl.snake import SnakeMDP


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = SimpleDeepQAgent()
    game = SnakeMDP(show_game=True)

    state, reward, done = game.reset()

    while True:

        action = agent.get_action(state)

        state_, reward, done = game.step(action)
        score = game.reward_sum()

        agent.train_short_memory(state, action, reward, state_, done)

        # remember
        agent.remember(state, action, reward, state_, done)

        state = state_

        if done:
            # train long memory, plot result
            state, reward, done = game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                # agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(reward)
            total_score += reward
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
