import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt

# class to implement all features of the UI
# the constructor sets the frame for the UI and
class SeismogramPlot(FigureCanvas):
    def __init__(self, parent=None, streams=[], origin_time=None):
        # Define figure dimensions based on the number of streams and desired width and height
        station_height = 0.5  # Height per station in inches
        station_width = 30  # Width per station in inches
        fig_height = len(streams) * station_height  # Total figure height
        fig_width = station_width  # Total figure width

        self.fig, self.ax = plt.subplots(len(streams), 1, sharex=True, figsize=(fig_width, fig_height))
        super(SeismogramPlot, self).__init__(self.fig)
        self.setParent(parent)

        self.streams = streams
        self.origin_time = origin_time

        self.plotSeismograms()
        self.fig.tight_layout()

    # method to plot all the seismograms with matplotlib
    def plotSeismograms(self):
        # Plot each seismogram stream
        for i, stream in enumerate(self.streams):
            for tr in stream:
                times = tr.times("matplotlib")  # Convert times to matplotlib format
                self.ax[i].plot(times, tr.data, 'k', linewidth=0.5)  # Plot the data
                self.ax[i].set_ylabel(tr.stats.station)  # Set station label on the right
                self.ax[i].yaxis.set_label_position("right")
                self.ax[i].yaxis.tick_right()
                self.ax[i].get_yaxis().set_ticks([])  # Remove y-ticks for clarity

        # Format x-axis to show time
        self.ax[-1].xaxis_date()
        self.ax[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y(%H:%M:%S)'))
        self.fig.autofmt_xdate()

        # Connect scroll event for zooming
        self.fig.canvas.mpl_connect('scroll_event', self.onScroll)

    # method to zoom on mouse scroll
    def onScroll(self, event):
        # Ensure event data is valid
        if event.xdata is None or event.ydata is None:
            return

        # Define scale factor for zooming
        scale_factor = 1.1
        if event.button == 'up':
            scale_factor = 1 / scale_factor

        # Apply zoom to each axis
        for ax in self.fig.axes:
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata
            ydata = event.ydata

            new_xlim = [xdata - (xdata - cur_xlim[0]) / scale_factor, xdata + (cur_xlim[1] - xdata) / scale_factor]
            new_ylim = [ydata - (ydata - cur_ylim[0]) / scale_factor, ydata + (cur_ylim[1] - ydata) / scale_factor]

            ax.set_xlim(new_xlim)
            ax.set_ylim(new_ylim)
        self.draw()

    # method to zoom and pan using keyboard
    def keyPressEvent(self, event):
        # Define panning step
        pan_step = 0.05
        if event.key() == Qt.Key_Left:
            self.pan('left', pan_step)
        elif event.key() == Qt.Key_Right:
            self.pan('right', pan_step)
        elif event.key() == Qt.Key_Up:
            self.pan('up', pan_step)
        elif event.key() == Qt.Key_Down:
            self.pan('down', pan_step)
        self.draw()

    # method to pan - move the seismogram left and right
    def pan(self, direction, step):
        # Apply panning based on direction
        for ax in self.fig.axes:
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            if direction == 'left':
                new_xlim = [cur_xlim[0] - step, cur_xlim[1] - step]
                ax.set_xlim(new_xlim)
            elif direction == 'right':
                new_xlim = [cur_xlim[0] + step, cur_xlim[1] + step]
                ax.set_xlim(new_xlim)
            elif direction == 'up':
                new_ylim = [cur_ylim[0] + step, cur_ylim[1] + step]
                ax.set_ylim(new_ylim)
            elif direction == 'down':
                new_ylim = [cur_ylim[0] - step, cur_ylim[1] - step]
                ax.set_ylim(new_ylim)

