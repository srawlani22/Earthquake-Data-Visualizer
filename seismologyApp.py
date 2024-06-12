from matplotlib.backends.backend_qt5agg import  NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QScrollArea
from obspy.clients.fdsn import Client
from obspy import read_events
from eventVisualizer import SeismogramPlot

# class to get data for the UI
# the constructor connects to the TEXNET client and gets the origin time of the event from the xml file
class SeismologyApp(QMainWindow):
    def __init__(self, event_file):
        super().__init__()

        self.setWindowTitle("Seismological Data Visualization")
        self.setGeometry(100, 100, 1200, 800)

        # Read event data from QuakeML file
        self.event = read_events(event_file)[0]
        origin_time = self.event.origins[0].time

        # Retrieve seismogram data from TEXNET client
        self.client = Client("TEXNET")
        self.streams = self.getSeismograms(origin_time)

        # Setup UI
        self.initUI()

    # method to extract z channel data from the stations
    def getSeismograms(self, origin_time):
        # add the stations below for which we need the data displayed on the UI
        stations = ['PB20', 'PB25', 'PB23', 'PB31', 'PB33', 'PB40', 'PB23','PB07','Pb24','PB07','PB44','PB11','PB42','PB38','PB35','PB10','PB12', 'PB28','PB29']
        streams = []
        for station in stations:
            try:
                # Retrieve Z channel data (HHZ) from 1 minute before to 2 minutes after the event origin time
                st = self.client.get_waveforms(network="TX", station=station, location="00",
                                               channel="HHZ", starttime=origin_time - 60,
                                               endtime=origin_time + 120)
                # Preprocess data: remove mean and apply high-pass filter
                st.detrend(type="demean")
                st.filter("highpass", freq=0.1)
                streams.append(st)
            except Exception as e:
                print(f"Could not retrieve data for station {station}: {e}")
        return streams

    # method to make the UI that contains the seismogram, makes it interative and adds the UI features along with the toolbar
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create scroll area for plot
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # Add SeismogramPlot to scrollable content
        self.plotter = SeismogramPlot(self.scroll_content, streams=self.streams, origin_time=self.event.origins[0].time)
        self.scroll_layout.addWidget(self.plotter)

        self.scroll_area.setWidget(self.scroll_content)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.scroll_area)

        # Add navigation toolbar
        self.toolbar = NavigationToolbar(self.plotter, self)
        self.layout.addWidget(self.toolbar)

        # Show maximized window
        self.showMaximized()
