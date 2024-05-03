import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D 
from itertools import combinations
import mpl_toolkits.mplot3d.proj3d as proj3d
from matplotlib.patches import FancyArrowPatch


#This code produces a quaternary plot diagram for
#trajectories. The intended application is Evolutionary Game Theory
#diagrams, but the code can be used for other things, of course.

#This solution is somewhat inspired by the accepted solution in 
#https://stackoverflow.com/questions/57467943/
#how-to-make-3d-4-variable-ternary-pyramid-plot-in-r-or-python

#and mainly by the article

#Shimura, Toshiaki and Kemp, Anthony I.S.. "Tetrahedral plot diagram: 
#A geometrical solution for quaternary systems" American Mineralogist, 
#vol. 100, no. 11-12, 2015, pp. 2545-2547. https://doi.org/10.2138/am-2015-5371



fig = plt.figure()
ax = fig.add_axes(Axes3D(fig)) 
ax.set_axis_off()
vertices = [
            [0,0,0],
            [1,0,0],
            [0.5,np.sqrt(3)/2,0],
            [0.5,np.sqrt(3)/6, np.sqrt(6)/3]
        ]
    

class TrajectoryArrow(FancyArrowPatch):
    #Apparently there's not an easy way to plot a customizable arrow
    #to indicate the trajectory direction using matplotlib (may be a skill issue, though ='/)
    #So below is the a code I ended up making heavily inspired in solutions by the community.
    
    #References:
    #https://gist.github.com/WetHat/1d6cd0f7309535311a539b42cccca89c

    #https://stackoverflow.com/questions/11140163/plotting-a-3d-cube-a-sphere-and-a-vector

    #https://stackoverflow.com/questions/22867620/
    #putting-arrowheads-on-vectors-in-a-3d-plot?noredirect=1&lq=1

    #https://github.com/matplotlib/matplotlib/issues/21688
      
    def __init__(self, delta_x, delta_y, delta_z, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_z = delta_z

    def do_3d_projection(self, renderer=None):
        xp, yp, zp = proj3d.proj_transform(self.delta_x, 
                                           self.delta_y, 
                                           self.delta_z, 
                                           self.axes.M
                                           )
        
        self.set_positions((xp[0], yp[0]),(xp[1], yp[1]))
        return np.min(zp)

           
def quaternary_to_coord(r, l, t, f):
    x = (r + 1.0 - l)/2.0
    y = t*np.sqrt(3.0)/2.0 + f*np.sqrt(3.0)/6.0
    z = f*np.sqrt(6.0)/3.0
    return [x,y,z]

def load_file(file_name):
    try:
        file = open(file_name, 'r')
        return file
    except IOError as error:
        print(error)
     
def plot_axis():
    axis_color = "black"
    edges = combinations(vertices, 2)
    for edge in edges:
        #print(line)
        edge_array = np.transpose(np.array(edge))
        ax.plot3D(edge_array[0], edge_array[1],
                edge_array[2], color = axis_color)
    
def draw_labels(labels):
    ax.text(vertices[1][0] - 0.09, vertices[0][1] - 0.09, vertices[0][2] - 0.09,
             labels[0], horizontalalignment = 'center', size  = 15)
    ax.text(vertices[0][0] + 0.09, vertices[1][1] - 0.09, vertices[1][2] - 0.09,
             labels[1], horizontalalignment = 'center', size  = 15)
    ax.text(vertices[2][0] +-0.09, vertices[2][1] + 0.09, vertices[2][2] - 0.09,
             labels[2], horizontalalignment = 'center', size  = 15)
    ax.text(vertices[3][0], vertices[3][1], vertices[3][2] + 0.09,
             labels[3], horizontalalignment = 'center', size  = 15)
    


def plot_dot(x, y, z, begin, end):
    if begin:
        ax.scatter(x[0], y[0], z[0], s=30, facecolor = "white", edgecolors="black", label = "Begin")
    if end:
        ax.scatter( x[-1], y[-1], z[-1], s=30, marker="d", facecolor = "white", edgecolors="black", label = "End")


def plot(file_name, **kwargs):

    defaultKwargs = {'arrow_color' : 'black',
                     'arrow_pos' : 2000,
                     'show_begin_point' : True,
                     'show_end_point' : False,
                     'labels' : ('R', 'L', 'T', 'F')}  
               
    kwargs = { **defaultKwargs, **kwargs }   

    
    file = load_file(file_name)
    x, y, z = [], [], []
    values = []
    lineData = []
    for line in file.readlines():
        values = line.split()
        lineData = quaternary_to_coord(
                float(values[0]), 
                float(values[1]),
                float(values[2]),
                float(values[3])
                )
        x.append(lineData[0])
        y.append(lineData[1])
        z.append(lineData[2])

    plot_axis()

    draw_labels(kwargs['labels'])
    k = kwargs['arrow_pos']
    #The the approach I took originally was to plot an arrow with quiver, though the lack of customization
    #is kind of a problem. It works, though.

    #ax.quiver(x[k], y[k], z[k], x[k+1]-x[k], y[k+1]-y[k], z[k+1]-z[k], 
    #         pivot = "middle", length = 40,
    #       lw = 1.5, arrow_length_ratio = 1, color = "k")


    #It's necessary a lot of tinkering with the properties of the arrow
    #to get a good looking result.
    arrow = TrajectoryArrow((x[k], x[k+1]), (y[k], y[k+1]), (z[k], z[k+1]), mutation_scale=7, 
                            arrowstyle = "simple, head_length = .7", color = kwargs['arrow_color'])
    
    
    ax.add_artist(arrow)
    
    ax.plot(x, y, z, color = "black", linewidth = 1.0, label = "Trajectory")
    plot_dot(x, y, z, kwargs['show_begin_point'], kwargs['show_end_point'])
    ax.legend()

def show():
    plt.show()
    


plot("data.dat", labels=('TB', 'TD', 'LB', 'LD'), arrow_pos=5500)
show()