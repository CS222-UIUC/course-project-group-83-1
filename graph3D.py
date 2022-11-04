import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation

'''
This function creates a 3D graph of the processed data
Parameters: processed_file (file that is reuturned from
sentiment analysis), event_name (string that is used to
name the file and one axis, the axis will be named "days
since [event_name]). 

The graph will be saved to a png and includes a legend of
the color mapping. The axis are as follows: x (Subjectivity),
y (Days Since Event), z (Polarity)
'''

def plot_3D(processed_file, event_name):
    df = pd.read_json(processed_file)
    ax = plt.axes(projection= "3d")
    dates_converted = (df['Date'] - df['Date'].min())  / np.timedelta64(1,'D')
    my_cmap = plt.get_cmap('viridis')
    a = ax.scatter(df["Subjectivity"], dates_converted.values, df["Polarity"], s = 0.02, cmap = my_cmap, c = df["Polarity"])
    plt.title("Visualization of Polarity and Subjectitivy in Relation to Time")
    ax.set_xlabel('Subjectivity')
    ax.set_ylabel('Days Since ' + event_name)
    ax.set_zlabel('Polarity')
    plt.colorbar(a, label= "Polarity")
    plt.savefig("3D_graph" + event_name.replace(" ", "") + ".png")

'''
This function can take a few minutes to complete.

This function creates a 3D animation from the graph 
created from the function above. The animation is a 
gif of the 3D graph rotated about the z-axis. 

Parameters: processed_file (file that is reuturned from
sentiment analysis), event_name (string that is used to
name the file and one axis, the axis will be named "days
since [event_name]). 

The graph will be saved to a gif file and includes a legend of
the color mapping. The axis are as follows: x (Subjectivity),
y (Days Since Event), z (Polarity)
'''

def animate_3D(processed_file, event_name):
    fig = plt.figure()
    df = pd.read_json(processed_file)
    ax = plt.axes(projection= "3d")
    dates_converted = (df['Date'] - df['Date'].min())  / np.timedelta64(1,'D')
    my_cmap = plt.get_cmap('viridis')
    a = ax.scatter(df["Subjectivity"], dates_converted.values, df["Polarity"], s = 0.02, cmap = my_cmap, c = df["Polarity"])
    plt.title("Visualization of Polarity and Subjectitivy in Relation to Time")
    ax.set_xlabel('Subjectivity')
    ax.set_ylabel('Days Since ' + event_name)
    ax.set_zlabel('Polarity')
    plt.colorbar(a, label= "Polarity")
    def rotate(angle):
        ax.view_init(azim=angle)
    rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0,362,2),interval=100, cache_frame_data = False)
    rot_animation.save("3D_animation" + event_name.replace(" ", "") + ".gif", writer='pillow')


#plot_3D("processed_2020_election_week.json", "2020 Election")
animate_3D("processed_2020_election_week.json", "2020 Election")
