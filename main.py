# Author: Sparsh Rawlani
# Purpose: Assessment for Software Developer Role at University of Texas Austin's Bureau of Economic Geology.
# Date: 06/11/2024
# Short Description: The project plots the event origin time from the qml file given. In order to run the code,
#                    you would just need to replace the destination address of the QuakeMl(xml) file in line 19 of this script.
# Refrences Used:
# 1. https://docs.obspy.org/packages/autogen/obspy.core.event.read_events.html
# 2. https://docs.obspy.org/packages/autogen/obspy.clients.fdsn.client.Client.get_waveforms.html
# 3. https://matplotlib.org/stable/plot_types/basic/plot.html#sphx-glr-plot-types-basic-plot-py
# 4. https://doc.qt.io/qtforpython-6/overviews/qtcharts-zoomlinechart-example.html
# 5. https://www.geeksforgeeks.org/qt-alignment-in-pyqt5/

from seismologyApp import SeismologyApp
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    quake_ml_file = r'C:\Users\Sparsh\Desktop\Technical_Exercise\Technical_Exercise\texnet2023vxae.xml'
    main_window = SeismologyApp(quake_ml_file)
    sys.exit(app.exec_())
