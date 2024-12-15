# Example 01

import numpy as np
import matplotlib.pyplot as plt
import random

# Define the function to generate random data
def generate_data():
    return random.randint(0, 10)

# Set up the plot
fig, ax = plt.subplots()
ax.set_title("Real-time Time Series Plot")
ax.set_xlabel("Time")
ax.set_ylabel("Value")
line, = ax.plot([], [])

# Initialize the data
x_vals = []
y_vals = []

# Start the real-time plot
#while True:
for i in range(10):
    # Generate a new data point
    new_x = i
    new_y = generate_data()

    # Append the new data point to the existing data
    x_vals.append(new_x)
    y_vals.append(new_y)

    # Update the plot with the new data point
    #line.set_data(x_vals, y_vals)
    ax.relim()
    ax.autoscale_view()

    # Redraw the updated plot
    fig.canvas.draw()
    plt.plot( x_vals, y_vals, 'ro-', label='E(Y|X=x)')

    # Pause for a short interval to show the updated plot
    plt.pause(0.01)
    # plt.close() 

plt.show()

# Example 02

import plotly.graph_objs as go
from plotly.subplots import make_subplots
from collections import deque
import random

# Initialize the figure
fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name='Difference of Means'), row=1, col=1)

# Set up the deque to store the data
max_length = 1000  # Set the maximum number of points to display
x_data = deque(maxlen=max_length)
y_data = deque(maxlen=max_length)

# Define the callback function to update the plot
def update_trace(new_data):
    x_data.append(new_data[0])
    y_data.append(new_data[1])
    fig.data[0].x = list(x_data)
    fig.data[0].y = list(y_data)
    fig.update_layout(title='Trace Plot - Difference of Means')

# Simulate adding new data in real time
for i in range(3):
    new_data = [i, random.randint(-10, 10)]
    update_trace(new_data)

    fig.show()

