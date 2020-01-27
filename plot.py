import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl

def set_plot_defaults():
    x_size = 10

    mpl.rcParams['figure.figsize'] = [x_size, x_size/1.61]
    mpl.rcParams['figure.dpi'] = 80
    mpl.rcParams['savefig.dpi'] = 100

    mpl.rcParams['font.size'] = 14
    mpl.rcParams['legend.fontsize'] = 'medium'
    mpl.rcParams['axes.labelsize'] = 16
    mpl.rcParams['figure.titlesize'] = 'large'
    return
