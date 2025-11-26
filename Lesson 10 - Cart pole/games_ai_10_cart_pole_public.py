import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam

# Create the CartPole environment
env = gym.make("CartPole-v1", render_mode="human")

# Get the size of state and action spaces
n_states: int = env.observation_space.shape[0]
print(f"n_states = {n_states}")
n_actions: int = env.action_space.__dict__["n"]
print(f"n_actions = {n_actions}")

# Build a simple neural network model
model = Sequential()
model.add(Input(shape=(n_states,)))
model.add(Dense(24, activation=tf.nn.relu))
model.add(Dense(24, activation=tf.nn.relu))
model.add(Dense(n_actions, activation="linear"))  # no activation function
model.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=0.001))

# Parameters
episodes: int = 2000
gamma: float = 0.95  # Discount factor
scores: list[int] = []

# Training loop
for episode in range(episodes):
    # Reset the environment to a new random initial state
    state_full: tuple[np.ndarray, dict] = env.reset()
    # Reshape the state to a format that can be fed to the model
    state: np.ndarray = np.reshape(state_full[0], [1, n_states])
    # print(f"state = {state}")

    # Flag indicating whether the episode has ended (e.g., the pole has fallen)
    terminated: bool = False
    # Typically, this is a timelimit, but could also be used to indicate an agent physically going out of bounds.
    truncated: bool = False
    # Just a simple time step counter, measuring the duration of the episode. The longer, the better.
    time: int = 0

    while not terminated and not truncated:
        print(f"time = {time}")

        # The model predicts the Q-values for the current state.
        # Q-values represent the model's estimate of the total reward that can be obtained,
        # starting from the current state and taking each possible action.
        prediction: np.ndarray = model.predict(state, verbose=False)

        # Select the model's predicted action with the highest Q-value
        q_values: np.ndarray = prediction[0]  # This is numpy array [[ a b ]] so we need [0]

        # Select the action with the highest Q-value as predicted by the model.
        # This is the action that the model believes will lead to the highest reward.
        # argmax function returns index of the value which is higher
        action: int = np.argmax(q_values).item()
        # print(f"action = {action}")

        # Execute the chosen action in the environment.
        # Get the next state, the reward received for taking the action, and whether the episode has ended.
        # The extra underscore absorbs additional value returned by env.step() that are not used here.
        next_state, reward, terminated, truncated, _ = env.step(action)
        reward: float = reward.__float__()
        # print(f"reward = {reward}")  # Always 1.0 in CartPole-v1
        # print(f"terminated = {terminated}")  # Happens when the pole falls or the cart goes out of bounds
        # print(f"truncated = {truncated}")  # Happens when time/score of 500 is reached

        # Reshape the state to a format that can be fed to the model
        next_state: np.ndarray = np.reshape(next_state, [1, n_states])
        # print(f"next_state = {next_state}")

        if terminated:
            target = reward
        else:
            future_prediction: np.ndarray = model.predict(next_state, verbose=False)
            # print(f"future_prediction = {future_prediction}")
            max_future_prediction: float = np.amax(future_prediction[0])
            # print(f"max_future_prediction = {max_future_prediction}")
            target = reward + gamma * max_future_prediction
        # print(f"target = {target}")

        target_f: np.ndarray = prediction
        # print(f"target_f = {target_f}")

        target_f[0][action] = target
        # print(f"target_f = {target_f}")

        model.fit(state, target_f, epochs=1, verbose=False)

        state = next_state
        time += 1

    episodes_string: str = f"{episode + 1}/{episodes}"
    print(f"Episode: {episodes_string}, Score: {time}")

    scores.append(time)
    if len(scores) % 10 == 0:
        mean_value: float = np.mean(scores[-10:]).item()
        print(f"Episode: {episodes_string}, Score: {time}, Average score over the last 10 episodes: {mean_value}")
        plt.plot(scores)
        plt.xlabel("Episode")
        plt.ylabel("Score")
        # plt.show()
        plt.show(block=False)
        plt.pause(0.1)

if len(scores) > 100:
    print(f"Average score over the last 100 episodes: {np.mean(scores[-100:])}")
else:
    print(f"Average score: {np.mean(scores)}")

print("Training finished. Rendering some test episodes...")

for test_episode in range(5):
    state_test_full: tuple[np.ndarray, dict] = env.reset()
    state_test: np.ndarray = np.reshape(state_test_full[0], [1, n_states])
    terminated: bool = False
    time: int = 0

    while not terminated:
        q_values: np.ndarray = model.predict(state_test, verbose=False)[0]
        action = np.argmax(q_values).item()
        next_state, reward, terminated, _, _ = env.step(action)
        next_state = np.reshape(next_state, [1, n_states])
        state_test = next_state
        time += 1

    print(f"Test Episode {test_episode + 1}: Score = {time}")

env.close()
