import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation

'''
Help with animations from : https://stackoverflow.com/questions/43180357/how-to-rotate-a-3d
-plot-in-python-or-as-a-animation-rotate-3-d-view-using-mou
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
