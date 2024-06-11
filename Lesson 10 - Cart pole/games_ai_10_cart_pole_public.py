import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam

# Create the CartPole environment
env = gym.make("CartPole-v1", render_mode="human")

# Get the size of state and action spaces
n_states = env.observation_space.shape[0]
print("n_states", n_states)
n_actions = env.action_space.__dict__["n"]
print("n_actions", n_actions)

# Build a simple neural network model
model = Sequential()
model.add(Input(shape=(n_states,)))
model.add(Dense(24, activation="relu"))
model.add(Dense(24, activation="relu"))
model.add(Dense(n_actions, activation="linear"))
model.compile(loss="mse", optimizer=Adam(learning_rate=0.001))

# Parameters
episodes = 2000
gamma = 0.95  # Discount factor
scores = []

# Training loop
for e in range(episodes):
    # Reset the environment to a new random initial state
    state = env.reset()
    # Reshape the state to a format that can be fed to the model
    state = np.reshape(state[0], [1, n_states])
    # print("state", state)

    # Flag indicating whether the episode has ended (e.g., the pole has fallen)
    terminated = False
    # Typically, this is a timelimit, but could also be used to indicate an agent physically going out of bounds.
    truncated = False
    # Just a simple time step counter, measuring the duration of the episode. The longer, the better.
    time = 0

    while not terminated and not truncated:
        print("time", time)

        # The model predicts the Q-values for the current state.
        # Q-values represent the model's estimate of the total reward that can be obtained,
        # starting from the current state and taking each possible action.
        prediction = model.predict(state, verbose=0)

        # Select the model's predicted action with the highest Q-value
        q_values = prediction[0]  # This is numpy array [[ a b ]] so we need [0]

        # Select the action with the highest Q-value as predicted by the model.
        # This is the action that the model believes will lead to the highest reward.
        action = np.argmax(q_values)

        # Execute the chosen action in the environment.
        # Get the next state, the reward received for taking the action, and whether the episode has ended.
        # The extra underscore absorbs additional value returned by env.step() that are not used here.
        next_state, reward, terminated, truncated, _ = env.step(action)
        reward = reward.__float__()
        # print("reward", reward)  # Always 1.0 in CartPole-v1
        # print("terminated", terminated)  # Happens when the pole falls or the cart goes out of bounds
        # print("truncated", truncated)  # Happens when time/score of 500 is reached

        # Reshape the state to a format that can be fed to the model
        next_state = np.reshape(next_state, [1, n_states])
        # print("next_state", next_state)

        if terminated:
            target = reward
        else:
            future_prediction = model.predict(next_state, verbose=0)
            # print("future_prediction", future_prediction)
            max_future_prediction = np.amax(future_prediction[0])
            # print("max_future_prediction", max_future_prediction)
            target = reward + gamma * max_future_prediction
        # print("target", target)

        target_f = prediction
        # print("target_f", target_f)

        target_f[0][action] = target
        # print("target_f", target_f)

        model.fit(state, target_f, epochs=1, verbose=0)

        state = next_state
        time += 1

    print(f"Episode: {e + 1}/{episodes}, Score: {time}")

    scores.append(time)
    if len(scores) % 10 == 0:
        print(f"Episode: {e + 1}/{episodes}, Score: {time}, Average score over the last 10 episodes: {np.mean(scores[-10:])}")
        plt.plot(scores)
        plt.xlabel("Episode")
        plt.ylabel("Score")
        plt.show()

if len(scores) > 100:
    print(f"Average score over the last 100 episodes: {np.mean(scores[-100:])}")
else:
    print(f"Average score: {np.mean(scores)}")

print("Training finished. Rendering some test episodes...")

for test_episode in range(5):
    state = env.reset()
    state = np.reshape(state[0], [1, n_states])
    terminated = False
    time = 0

    while not terminated:
        q_values = model.predict(state, verbose=0)[0]
        action = np.argmax(q_values)
        next_state, reward, terminated, _, _ = env.step(action)
        next_state = np.reshape(next_state, [1, n_states])
        state = next_state
        time += 1

    print(f"Test Episode {test_episode + 1}: Score = {time}")

env.close()
